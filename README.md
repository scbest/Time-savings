# Time-savings

A small collection of automation tools.

- [YouTube Video Generator](#youtube-video-generator) — turn a topic into an algorithm-optimized packaging brief (titles, thumbnail, hook, retention outline).
- [Kids Shoe Price Monitor](#kids-shoe-price-monitor) — watch product URLs and alert on price drops.

---

# YouTube Video Generator

The hardest part of long-form video is *starting*. This tool removes the blank-page
problem: give it a topic and it hands you a ready-to-shoot brief that's optimized for
how the YouTube algorithm actually behaves right now — title candidates scored for
click-through, a thumbnail brief, a 15-second hook, and a retention-structured outline.

The "what YouTube rewards right now" knowledge lives in `youtube_playbook.json`, which
is re-researched periodically (see [Staying current](#staying-current)) so the advice
tracks the algorithm instead of going stale.

## Usage

```bash
python3 video_generator.py "how to start a youtube channel"
python3 video_generator.py "beginner sourdough bread" --audience "busy parents" --count 6
python3 video_generator.py "home espresso setup" --json   # machine-readable
```

Flags:

- `--audience "..."` — who the video is for; tunes a few phrasings.
- `--count N` — how many title candidates to show (default 6).
- `--json` — emit the full brief as JSON instead of the formatted view.

## What you get

| Section | What it does |
|---------|--------------|
| Title candidates | Six formulas filled with your topic, each **scored 0–100** against current CTR heuristics (length, numbers, power words, curiosity gap, keyword placement) and ranked. |
| Thumbnail brief | The current rules — face-forward, ≤4 words, high contrast, phone-first. |
| Hook | Four proven 15-second openers written for your topic. |
| Retention outline | A segment-by-segment 6–10 min skeleton with the job and tactic for each beat. |
| Optimize-for + benchmarks | The current ranking signals and the CTR/retention numbers to judge yourself against. |

## Staying current

`youtube_playbook.json` carries a `last_updated` date. The generator **warns you when
it's stale** (older than `refresh_interval_days`, default 30). To refresh it, follow
[`refresh_playbook.md`](refresh_playbook.md) — a fixed protocol that researches the
latest algorithm behavior, updates the JSON, and opens a PR. A recurring job runs this
automatically; you can also trigger it by hand (see that doc).

---

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
