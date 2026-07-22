---
name: youtube-brief
description: Generate an algorithm-optimized YouTube long-form video brief (scored title candidates, a thumbnail brief, a 15-second hook, and a retention-structured outline) from a topic, using this repo's video_generator.py and the current youtube_playbook.json. Use whenever the user asks for YouTube video ideas, titles, thumbnails, hooks, packaging, or a "video brief" for a topic — e.g. "/youtube-brief how to start a channel", "give me titles for a sourdough video", "package a video about home espresso".
---

# YouTube video brief

Turn a topic into a ready-to-shoot packaging brief that's optimized for how the
YouTube algorithm behaves right now. This runs entirely in the current Claude Code
session — which means it uses the user's Claude subscription, no API key.

## Inputs

- **topic** (required): what the video is about. If the user didn't give one, ask for it.
- **audience** (optional): who it's for (e.g. "busy parents").
- **count** (optional): how many title candidates (default 6).

## Steps

Run these from the repository root (the directory containing `video_generator.py`).

1. **Always produce the scored template brief first** — it's instant, free, and
   gives CTR-scored titles plus the current benchmarks and algorithm signals:

   ```bash
   python3 video_generator.py "<topic>" [--audience "<audience>"] [--count <N>]
   ```

   Show the user this output.

2. **Then upgrade the copy in-session.** Because this Claude Code session already
   runs on the user's subscription, you (Claude) can write original, non-formulaic
   copy directly — no need to shell out to `claude -p`. Read `youtube_playbook.json`
   and use its current guidance (algorithm signals, title formulas, thumbnail rules,
   hook patterns, retention structure, benchmarks) to write:
   - `count` original, specific, grammatical **titles** (each ≤ ~60 chars, keyword
     front-loaded, opening a curiosity gap the thumbnail doesn't repeat), noting the
     formula and why each works;
   - a **thumbnail concept** (one focal point, ≤ 4 words of text, high contrast,
     face-forward when it fits);
   - **4 hook options** for the first 15 seconds, written as spoken lines;
   - a **6–10 minute retention outline** (segment, timestamp, goal, tactic), with a
     fresh open-loop/pattern-interrupt roughly every 40–60 seconds and a continuation
     CTA at the end.

   Ground every choice in the playbook — the whole point is that the copy tracks the
   *current* algorithm, not generic advice.

3. If the user only wants the fast version, stop after step 1. If they want polished
   copy, do step 2.

## Notes

- Equivalent one-shot CLI path (also on the subscription): `python3 video_generator.py
  "<topic>" --llm` shells out to the `claude` CLI. Prefer writing the copy inline
  (step 2) when you're already in a Claude Code session — it's faster and avoids a
  second spawn.
- If `youtube_playbook.json` reports itself stale, mention it — the advice may be dated
  and the monthly refresh can be run (`refresh_playbook.md`).
- Keep the output skimmable: titles ranked best-first, then thumbnail, hook, outline.
