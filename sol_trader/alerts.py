"""
Alert formatting and delivery for SOL trading signals.
Currently delivers via GitHub Issues. Extend notify() to add email, SMS, etc.
"""

import json
import os
import urllib.request

_FG_LABELS = [
    (0, 25, "Extreme Fear"),
    (26, 45, "Fear"),
    (46, 55, "Neutral"),
    (56, 75, "Greed"),
    (76, 100, "Extreme Greed"),
]


def _fg_label(value):
    for lo, hi, label in _FG_LABELS:
        if lo <= value <= hi:
            return label
    return "Unknown"


def _score_bar(score):
    """10-char visual bar: -1.0 = all empty, +1.0 = all filled."""
    filled = round((score + 1.0) / 2.0 * 10)
    filled = max(0, min(10, filled))
    return "▓" * filled + "░" * (10 - filled)


def _signal_table(bd):
    return (
        "| Indicator | Value | Score |\n"
        "|-----------|-------|-------|\n"
        f"| RSI (14) | {bd['rsi'] if bd['rsi'] is not None else 'N/A'} | {bd['rsi_score']:+.2f} |\n"
        f"| EMA 20/50 | crossover | {bd['ema_score']:+.2f} |\n"
        f"| MACD | crossover | {bd['macd_score']:+.2f} |\n"
        f"| Fear & Greed | {bd['fear_greed_index']} — {_fg_label(bd['fear_greed_index'])} | {bd['fear_greed_score']:+.2f} |\n"
        f"\n**Technical (70%):** {bd['tech_weighted']:+.4f} &nbsp; "
        f"**Sentiment (30%):** {bd['sentiment_weighted']:+.4f}"
    )


def format_buy_alert(signal, holdings, fixed_dollar_amount):
    price = signal["current_price"]
    score = signal["composite_score"]
    bd = signal["breakdown"]
    qty = fixed_dollar_amount / price

    title = f"SOL BUY Signal — ${price:,.2f} (score {score:+.2f})"
    body = f"""## SOL Buy Signal

**Current Price:** ${price:,.2f}
**Signal Score:** {score:+.2f} `{_score_bar(score)}`
**Suggested Buy:** ${fixed_dollar_amount:.2f} ≈ {qty:.4f} SOL

### Signal Breakdown

{_signal_table(bd)}

### Tax Context (if you buy)

- New lot: **{qty:.4f} SOL** at ${price:,.2f} — cost basis **${fixed_dollar_amount:.2f}**
- Current holdings: **{holdings['total_sol']:.4f} SOL** across {holdings['open_lots']} lot(s)
- Avg cost basis: **${holdings['avg_cost_per_sol']:,.2f}/SOL** (before this buy)
- Holding period clock starts today — short-term rates apply for < 1 year

---
*This is an alert only — no trade has been executed.*
"""
    return title, body


def format_sell_alert(signal, tax_impact, fixed_dollar_amount):
    price = signal["current_price"]
    score = signal["composite_score"]
    bd = signal["breakdown"]

    title = f"SOL SELL Signal — ${price:,.2f} (score {score:+.2f})"

    if "error" in tax_impact:
        tax_section = f"⚠️ {tax_impact['error']} — nothing to sell."
    else:
        tax_section = _format_tax_table(tax_impact)

    body = f"""## SOL Sell Signal

**Current Price:** ${price:,.2f}
**Signal Score:** {score:+.2f} `{_score_bar(score)}`

### Signal Breakdown

{_signal_table(bd)}

### Tax Impact — FIFO Estimate

{tax_section}

---
*This is an alert only — no trade has been executed. Consult a tax professional.*
"""
    return title, body


def _format_tax_table(t):
    rows = [
        "| Item | Amount |",
        "|------|--------|",
        f"| SOL quantity | {t['qty_sol']:.4f} SOL |",
        f"| Gross proceeds | ${t['proceeds']:,.2f} |",
        f"| Cost basis | ${t['total_cost_basis']:,.2f} |",
        f"| **Total gain / loss** | **${t['total_gain_loss']:+,.2f}** |",
        f"| Short-term gain (≤1 yr) | ${t['short_term_gain']:+,.2f} |",
        f"| Long-term gain (>1 yr) | ${t['long_term_gain']:+,.2f} |",
        f"| **Estimated tax** | **${t['estimated_tax']:,.2f}** ({t['effective_rate']}% of proceeds) |",
        f"| Net after estimated tax | ${t['net_after_tax']:,.2f} |",
    ]
    lines = "\n".join(rows)

    lot_lines = []
    for lot in t.get("lots_consumed", []):
        term_icon = "📅" if lot["term"] == "long_term" else "⏱"
        lot_lines.append(
            f"- Lot `{lot['lot_id']}`: {lot['qty']:.4f} SOL bought {lot['bought']} "
            f"({lot['held_days']}d, {term_icon} {lot['term'].replace('_', '-')}) "
            f"— gain/loss: **${lot['gain_loss']:+,.2f}**"
        )

    if lot_lines:
        return lines + "\n\n**Lots consumed (FIFO):**\n" + "\n".join(lot_lines)
    return lines


def create_github_issue(title, body, labels=None):
    token = os.environ.get("GITHUB_TOKEN")
    repo = os.environ.get("GITHUB_REPOSITORY")
    if not token or not repo:
        print("  [SKIP] Cannot create issue — missing GITHUB_TOKEN or GITHUB_REPOSITORY")
        return None

    url = f"https://api.github.com/repos/{repo}/issues"
    payload = json.dumps({"title": title, "body": body, "labels": labels or ["sol-signal"]}).encode()
    req = urllib.request.Request(
        url,
        data=payload,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            result = json.loads(resp.read())
            issue_url = result.get("html_url", "")
            print(f"  Created issue: {issue_url}")
            return issue_url
    except Exception as e:
        print(f"  Failed to create issue: {e}")
        return None


def notify(title, body, labels=None):
    """Deliver an alert. Add additional channels here (email, SMS, webhook, etc.)."""
    create_github_issue(title, body, labels)
