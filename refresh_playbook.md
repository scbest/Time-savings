# Playbook Refresh Protocol

`youtube_playbook.json` is the brain of the video generator. YouTube changes what
it rewards, so this file has to be re-researched periodically or the generator
slowly gives dated advice. This document is the exact protocol the refresh job
(or a human) follows.

The generator warns you automatically when the playbook is older than its
`refresh_interval_days`, so a missed refresh is visible, not silent.

## When to run

- On the schedule set by the recurring refresh job (default: monthly).
- Any time YouTube announces a major change (Creator Insider, a Google blog post).

## The protocol

1. **Research the current state.** Run fresh web searches, prioritizing the last
   ~3 months. Cover:
   - How the recommendation/Browse/Suggested system currently ranks long-form.
   - Current CTR benchmarks and what counts as good.
   - Current retention thresholds (first 15-30s, average % viewed).
   - Title and thumbnail packaging best practices.
   - Any confirmed algorithm changes since `meta.last_updated`.
   Good sources: YouTube's own Creator Insider / blog, vidIQ, and reputable
   creator-analytics blogs. Treat any single blog as a claim, not gospel;
   prefer things ~2+ independent sources agree on.

2. **Update the JSON, section by section**, only where the research actually
   changed something:
   - `algorithm_signals.optimize_for_in_order` and `confirmed_changes_YYYY`
   - `benchmarks` (ctr, retention, length)
   - `title.formulas` / `power_words` / `scoring` params
   - `thumbnail.rules` / `text_word_max`
   - `hook.patterns`, `retention_structure`
   Keep the shape identical — the generator reads these keys by name. Change
   values and list items, not the structure.

3. **Bump the metadata**:
   - `meta.last_updated` = today
   - `meta.next_refresh_due` = today + `refresh_interval_days`
   - `meta.version` += 1
   - `meta.sources` = the URLs you actually used this round

4. **Append a changelog entry** to `changelog`: date, new version, and a
   one-line summary of what changed and why.

5. **Validate**: `python3 -c "import json; json.load(open('youtube_playbook.json'))"`
   then run `python3 video_generator.py "test topic"` and confirm it renders.

6. **Ship it as a PR** against the default branch so the change is reviewable —
   never overwrite the playbook silently. Title the PR `Refresh YouTube playbook (vN)`
   and put the changelog summary in the body.

## Automating it

The recurring refresh runs this protocol on a fresh scheduled session. If you
ever need to trigger it by hand, just start a session and paste:

> Follow refresh_playbook.md against this repo: research the current YouTube
> algorithm, update youtube_playbook.json, and open a PR.
