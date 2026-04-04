---
name: trends
description: Show recent daily tech trend summaries from substack/daily_trends.md. Use when the user wants to see what's been trending.
argument-hint: [time period, e.g. "today", "last 3 days", "this week"]
allowed-tools: Read Bash
---

# Daily Trends Reader

Read the trend data from `substack/daily_trends.md` and summarize it for the requested time period.

## Your Task

1. Read the file `substack/daily_trends.md` from the project root
2. Filter entries to match the requested time period: **$ARGUMENTS** (default to "today" if no argument given)
3. Summarize the findings directly in chat — do NOT tell the user to open a file

## Output Format

For each day in the requested range, present:

### [Date]

**Top Trending Topics**
- Topic — platform — why it's trending (1 sentence)

**Best How-To Content**
- Title/topic — platform — what it covers (1 sentence)

**Post Ideas For You**
- Suggested topic — why it fits your content themes (1 sentence)

Keep it scannable. No filler. The user is reading this on mobile.
