"""
Kids Shoe Price Monitor
Checks configured product URLs for price changes and creates alerts.
"""

import json
import os
import re
import sys
import urllib.request
import urllib.error
from datetime import datetime, timezone
from pathlib import Path

CONFIG_PATH = Path(__file__).parent / "config.json"
HISTORY_PATH = Path(__file__).parent / "price_history.json"


def load_config():
    with open(CONFIG_PATH) as f:
        return json.load(f)


def load_history():
    if HISTORY_PATH.exists():
        with open(HISTORY_PATH) as f:
            return json.load(f)
    return {}


def save_history(history):
    with open(HISTORY_PATH, "w") as f:
        json.dump(history, f, indent=2)


def fetch_page(url):
    """Fetch a webpage with a browser-like user agent."""
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
    }
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8", errors="replace")


def extract_price_amazon(html):
    """Extract price from Amazon product page."""
    patterns = [
        r'"priceAmount":\s*"?([\d.]+)"?',
        r'class="a-price-whole">([\d,]+)</span>.*?class="a-price-fraction">(\d+)',
        r'id="priceblock_ourprice"[^>]*>\s*\$?([\d,.]+)',
        r'id="priceblock_dealprice"[^>]*>\s*\$?([\d,.]+)',
        r'"price":\s*"?\$?([\d.]+)"?',
        r'class="a-offscreen">\s*\$?([\d,.]+)',
    ]
    for pattern in patterns:
        match = re.search(pattern, html)
        if match:
            groups = match.groups()
            if len(groups) == 2:
                price_str = groups[0].replace(",", "") + "." + groups[1]
            else:
                price_str = groups[0].replace(",", "")
            try:
                return float(price_str)
            except ValueError:
                continue
    return None


def extract_price_nike(html):
    """Extract price from Nike.com product page."""
    patterns = [
        r'"currentPrice":\s*([\d.]+)',
        r'"price":\s*"?\$?([\d.]+)"?',
        r'data-test="product-price"[^>]*>\s*\$?([\d,.]+)',
        r'class="product-price[^"]*"[^>]*>\s*\$?([\d,.]+)',
    ]
    for pattern in patterns:
        match = re.search(pattern, html)
        if match:
            try:
                return float(match.group(1).replace(",", ""))
            except ValueError:
                continue
    return None


def extract_price_zappos(html):
    """Extract price from Zappos product page."""
    patterns = [
        r'"price":\s*"?\$?([\d.]+)"?',
        r'class="price"[^>]*>\s*\$?([\d,.]+)',
        r'"amount":\s*"?([\d.]+)"?',
    ]
    for pattern in patterns:
        match = re.search(pattern, html)
        if match:
            try:
                return float(match.group(1).replace(",", ""))
            except ValueError:
                continue
    return None


def extract_price_generic(html):
    """Try to extract a price from any page using common patterns."""
    patterns = [
        r'"price":\s*"?\$?([\d]+\.[\d]{2})"?',
        r'"amount":\s*"?([\d]+\.[\d]{2})"?',
        r'class="[^"]*price[^"]*"[^>]*>\s*\$?([\d,.]+\.[\d]{2})',
        r'itemprop="price"[^>]*content="([\d.]+)"',
        r'\$\s*([\d,]+\.\d{2})',
    ]
    prices = []
    for pattern in patterns:
        for match in re.finditer(pattern, html, re.IGNORECASE):
            try:
                price = float(match.group(1).replace(",", ""))
                if 1.0 < price < 500.0:  # reasonable shoe price range
                    prices.append(price)
            except (ValueError, IndexError):
                continue
    if prices:
        return min(prices)  # return lowest found price
    return None


EXTRACTORS = {
    "amazon": extract_price_amazon,
    "nike": extract_price_nike,
    "zappos": extract_price_zappos,
    "generic": extract_price_generic,
}


def check_price(product):
    """Check the current price of a product. Returns (price, error)."""
    source = product.get("source", "generic")
    extractor = EXTRACTORS.get(source, extract_price_generic)

    try:
        html = fetch_page(product["url"])
        price = extractor(html)
        if price is None:
            return None, f"Could not extract price from {source} page"
        return price, None
    except urllib.error.HTTPError as e:
        return None, f"HTTP error {e.code}: {e.reason}"
    except urllib.error.URLError as e:
        return None, f"URL error: {e.reason}"
    except Exception as e:
        return None, f"Error: {e}"


def create_github_issue(title, body):
    """Create a GitHub issue using the GITHUB_TOKEN env var."""
    token = os.environ.get("GITHUB_TOKEN")
    repo = os.environ.get("GITHUB_REPOSITORY")
    if not token or not repo:
        print(f"  [SKIP] Cannot create issue — missing GITHUB_TOKEN or GITHUB_REPOSITORY")
        return

    url = f"https://api.github.com/repos/{repo}/issues"
    data = json.dumps({"title": title, "body": body, "labels": ["price-drop"]}).encode()
    req = urllib.request.Request(
        url,
        data=data,
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
            print(f"  Created issue: {result.get('html_url', 'OK')}")
    except Exception as e:
        print(f"  Failed to create issue: {e}")


def main():
    config = load_config()
    history = load_history()
    now = datetime.now(timezone.utc).isoformat()

    products = config.get("products", [])
    if not products:
        print("No products configured. Edit config.json to add products.")
        return

    alerts = []

    for product in products:
        name = product["name"]
        url = product["url"]
        target = product.get("target_price")

        # Skip example entries
        if "EXAMPLE" in url:
            print(f"[SKIP] {name} — example URL, skipping")
            continue

        print(f"[CHECK] {name}")
        price, error = check_price(product)

        if error:
            print(f"  Error: {error}")
            continue

        print(f"  Current price: ${price:.2f}")

        # Update history
        key = url
        if key not in history:
            history[key] = {
                "name": name,
                "prices": [],
                "lowest_price": None,
                "last_alert": None,
            }

        entry = history[key]
        entry["prices"].append({"date": now, "price": price})

        # Keep last 90 days of history (360 checks at 6hr intervals)
        entry["prices"] = entry["prices"][-360:]

        prev_lowest = entry.get("lowest_price")
        if prev_lowest is None or price < prev_lowest:
            entry["lowest_price"] = price

        # Check for alert conditions
        if target and price <= target:
            prev_prices = [p["price"] for p in entry["prices"][:-1]]
            last_alert = entry.get("last_alert")

            # Only alert if price just dropped or hasn't been alerted in 24h
            should_alert = True
            if last_alert:
                from datetime import timedelta
                last_dt = datetime.fromisoformat(last_alert)
                now_dt = datetime.fromisoformat(now)
                if (now_dt - last_dt).total_seconds() < 86400:
                    should_alert = False

            if should_alert:
                print(f"  ALERT: ${price:.2f} is at or below target ${target:.2f}!")
                alert_info = {
                    "name": name,
                    "url": url,
                    "price": price,
                    "target": target,
                    "lowest_ever": entry["lowest_price"],
                }
                alerts.append(alert_info)
                entry["last_alert"] = now
        elif target:
            print(f"  Above target (${target:.2f}), no alert")

    save_history(history)

    # Send notifications
    if alerts:
        for alert in alerts:
            title = f"Price Drop: {alert['name']} is now ${alert['price']:.2f}"
            body = (
                f"## Price Drop Alert\n\n"
                f"**{alert['name']}** has dropped to **${alert['price']:.2f}**\n\n"
                f"- Target price: ${alert['target']:.2f}\n"
                f"- Lowest ever: ${alert['lowest_ever']:.2f}\n"
                f"- [Buy now]({alert['url']})\n\n"
                f"_Checked at {now}_"
            )
            if config.get("notification", {}).get("create_issue", True):
                create_github_issue(title, body)

        print(f"\n{len(alerts)} price drop alert(s) sent!")
    else:
        print("\nNo price drop alerts.")

    # Set output for GitHub Actions
    github_output = os.environ.get("GITHUB_OUTPUT")
    if github_output:
        with open(github_output, "a") as f:
            f.write(f"alerts_count={len(alerts)}\n")
            f.write(f"products_checked={len(products)}\n")


if __name__ == "__main__":
    main()
