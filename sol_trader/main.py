"""
SOL swing trading workflow — orchestrator.
Fetches signals, evaluates thresholds, fires alerts with tax context.
"""

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from sol_trader import signals, tax, alerts
from sol_trader.executor import AlertOnlyExecutor

CONFIG_PATH = Path(__file__).parent.parent / "sol_config.json"
STATE_PATH = Path(__file__).parent.parent / "sol_state.json"

DEFAULTS = {
    "fixed_dollar_amount": 100.0,
    "buy_threshold": 0.45,
    "sell_threshold": -0.45,
    "alert_cooldown_hours": 12,
    "short_term_tax_rate": 0.32,
    "long_term_tax_rate": 0.15,
    "execution_mode": "alert_only",
}


def load_config():
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH) as f:
            return {**DEFAULTS, **json.load(f)}
    return DEFAULTS


def load_state():
    if STATE_PATH.exists():
        with open(STATE_PATH) as f:
            return json.load(f)
    return {"last_buy_alert": None, "last_sell_alert": None}


def save_state(state):
    with open(STATE_PATH, "w") as f:
        json.dump(state, f, indent=2)


def _cooldown_active(last_alert_iso, cooldown_hours):
    if not last_alert_iso:
        return False
    last = datetime.fromisoformat(last_alert_iso)
    if last.tzinfo is None:
        last = last.replace(tzinfo=timezone.utc)
    elapsed_hours = (datetime.now(timezone.utc) - last).total_seconds() / 3600
    return elapsed_hours < cooldown_hours


def _write_github_output(**kwargs):
    path = os.environ.get("GITHUB_OUTPUT")
    if path:
        with open(path, "a") as f:
            for k, v in kwargs.items():
                f.write(f"{k}={v}\n")


def main():
    config = load_config()
    state = load_state()
    now = datetime.now(timezone.utc).isoformat()

    print(f"[SOL Trader] {now}")

    # --- Fetch market data ---
    print("\nFetching OHLCV data...")
    try:
        ohlcv = signals.fetch_ohlcv()
        print(f"  {len(ohlcv)} candles received")
    except Exception as e:
        print(f"  ERROR: {e}")
        sys.exit(1)

    print("Fetching Fear & Greed index...")
    try:
        fg_value = signals.fetch_fear_greed()
        print(f"  Index: {fg_value}/100")
    except Exception as e:
        print(f"  WARNING: {e} — using neutral (50)")
        fg_value = 50

    # --- Compute signal ---
    signal = signals.compute_signal(
        ohlcv,
        fg_value,
        buy_threshold=config["buy_threshold"],
        sell_threshold=config["sell_threshold"],
    )
    action = signal["action"]
    score = signal["composite_score"]
    price = signal["current_price"]
    bd = signal["breakdown"]

    print(f"\nSignal: {action}  score={score:+.4f}  price=${price:,.2f}")
    print(f"  RSI={bd['rsi']}  EMA={bd['ema_score']:+.2f}  MACD={bd['macd_score']:+.2f}  F&G={bd['fear_greed_score']:+.2f}")

    # --- Holdings summary ---
    holdings = tax.get_holdings_summary()
    print(f"  Holdings: {holdings['total_sol']:.4f} SOL  avg_basis=${holdings['avg_cost_per_sol']:,.2f}")

    executor = AlertOnlyExecutor()  # Swap for a live executor to enable auto-trading

    # --- BUY ---
    if action == "BUY":
        if _cooldown_active(state.get("last_buy_alert"), config["alert_cooldown_hours"]):
            print(f"\n[COOLDOWN] Buy alert suppressed (<{config['alert_cooldown_hours']}h since last)")
        else:
            print("\nBUY signal — sending alert")
            amount = config["fixed_dollar_amount"]
            executor.execute_buy(amount, price)

            title, body = alerts.format_buy_alert(signal, holdings, amount)
            alerts.notify(title, body, labels=["sol-signal", "buy"])

            state["last_buy_alert"] = now
            save_state(state)

    # --- SELL ---
    elif action == "SELL":
        if _cooldown_active(state.get("last_sell_alert"), config["alert_cooldown_hours"]):
            print(f"\n[COOLDOWN] Sell alert suppressed (<{config['alert_cooldown_hours']}h since last)")
        elif holdings["total_sol"] == 0:
            print("\nSELL signal — no holdings, skipping")
        else:
            print("\nSELL signal — sending alert with tax impact")
            # Sell fixed_dollar_amount worth (or all holdings if less)
            qty_to_sell = min(
                holdings["total_sol"],
                config["fixed_dollar_amount"] / price,
            )
            tax_impact = tax.estimate_sell_impact(
                qty_to_sell,
                price,
                short_term_rate=config["short_term_tax_rate"],
                long_term_rate=config["long_term_tax_rate"],
            )
            executor.execute_sell(qty_to_sell, price)

            title, body = alerts.format_sell_alert(signal, tax_impact, config["fixed_dollar_amount"])
            alerts.notify(title, body, labels=["sol-signal", "sell"])

            state["last_sell_alert"] = now
            save_state(state)

    # --- HOLD ---
    else:
        print(f"\nHOLD — score {score:+.4f} within neutral band [{config['sell_threshold']}, {config['buy_threshold']}]")

    _write_github_output(action=action, score=score, price=price)


if __name__ == "__main__":
    main()
