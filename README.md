# Kids Shoe Price Monitor

Automated price monitoring for kids shoes using GitHub Actions. No local hosting required — runs entirely on GitHub's infrastructure.

## How It Works

1. You add product URLs and target prices to `config.json`
2. A GitHub Actions workflow runs every 6 hours
3. When a price drops to or below your target, you get notified via GitHub Issue (and email if you have GitHub notifications enabled)
4. Price history is tracked over time in `price_history.json`

## Setup

1. **Fork or clone this repo**
2. **Edit `config.json`** — add the shoes you want to track:
   ```json
   {
     "products": [
       {
         "name": "Nike Revolution 6 Kids",
         "url": "https://www.amazon.com/dp/XXXXXXXXXX",
         "target_price": 35.00,
         "source": "amazon"
       }
     ],
     "check_interval_hours": 6
   }
   ```
3. **Enable GitHub Actions** in your repo settings
4. **Turn on GitHub notification emails** so you get alerts when issues are created

## Supported Sources

| Source     | How It Works                              |
|------------|-------------------------------------------|
| `amazon`   | Scrapes product page price                |
| `zappos`   | Scrapes product page price                |
| `nike`     | Scrapes Nike.com product page             |
| `generic`  | Attempts to extract price from any URL    |

## Manual Run

You can trigger a price check manually from the **Actions** tab → **Price Monitor** → **Run workflow**.

## Configuration

See `config.json` for all options. Key fields:

- `products[].name` — friendly name for notifications
- `products[].url` — direct product page URL
- `products[].target_price` — alert when price is at or below this
- `products[].source` — which parser to use
- `notification.create_issue` — create GitHub Issues on price drops (default: true)
