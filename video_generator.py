"""
YouTube Long-Form Video Generator
Turns a topic into an algorithm-optimized packaging brief: title candidates
(scored for CTR), a thumbnail brief, a 15-second hook, and a retention-structured
outline. All the "what YouTube rewards right now" logic lives in youtube_playbook.json,
which is refreshed periodically so this stays current as the algorithm changes.

Usage:
    python video_generator.py "how to start a youtube channel"
    python video_generator.py "beginner sourdough" --audience "busy parents" --count 6
    python video_generator.py "my topic" --json        # machine-readable output
"""

import argparse
import json
import re
import sys
from datetime import date, datetime
from pathlib import Path

PLAYBOOK_PATH = Path(__file__).parent / "youtube_playbook.json"

STOPWORDS = {
    "a", "an", "the", "to", "for", "of", "and", "or", "in", "on", "with",
    "how", "why", "your", "you", "my", "i", "is", "are", "that", "this",
    "without", "vs", "at", "by", "from", "into",
}


def load_playbook():
    if not PLAYBOOK_PATH.exists():
        sys.exit(f"Playbook not found at {PLAYBOOK_PATH}. Run the refresh job first.")
    with open(PLAYBOOK_PATH) as f:
        return json.load(f)


def playbook_freshness(playbook):
    """Return (days_old, is_stale, message) so the user knows if advice may be dated."""
    meta = playbook.get("meta", {})
    last = meta.get("last_updated")
    interval = meta.get("refresh_interval_days", 30)
    if not last:
        return None, True, "Playbook has no last_updated date."
    try:
        last_dt = datetime.strptime(last, "%Y-%m-%d").date()
    except ValueError:
        return None, True, f"Could not parse last_updated: {last}"
    days = (date.today() - last_dt).days
    stale = days > interval
    if stale:
        msg = (
            f"Playbook is {days} days old (refresh interval {interval}d). "
            f"Advice may be out of date - run the refresh job."
        )
    else:
        msg = f"Playbook current: updated {last} ({days}d ago)."
    return days, stale, msg


LEADING_INTENT = [
    "how to", "how do i", "how do you", "ways to", "tips to", "tips for",
    "guide to", "a guide to", "the guide to", "learn to", "learn how to",
    "best way to", "steps to",
]


def keywords(topic):
    """Pull content words from the topic, preserving order, dropping stopwords."""
    words = re.findall(r"[A-Za-z0-9']+", topic.lower())
    kept = [w for w in words if w not in STOPWORDS]
    return kept or words


def strip_intent(topic):
    """Remove a leading 'how to' / 'ways to' etc. so formulas don't double up."""
    t = topic.strip().lower()
    for prefix in sorted(LEADING_INTENT, key=len, reverse=True):
        if t.startswith(prefix + " "):
            return topic.strip()[len(prefix) + 1:]
    return topic.strip()


COMMON_VERBS = {
    "start", "make", "build", "grow", "learn", "create", "fix", "cook",
    "bake", "write", "draw", "edit", "run", "lose", "save", "get", "use",
    "set", "plan", "design", "record", "launch", "sell", "master", "play",
}


def topic_noun(topic):
    """A standalone noun phrase for the niche: the last 1-2 content words.
    'how to start a youtube channel' -> 'Youtube Channel'."""
    kw = keywords(strip_intent(topic))
    if not kw:
        kw = keywords(topic)
    tail = kw[-2:] if len(kw) >= 2 else kw
    return title_case(" ".join(tail))


def parse_topic(topic):
    """Normalize a topic into the pieces the templates need.

    is_action = the topic reads as a verb phrase ('start a channel'), so
    'How to {core}' works. Otherwise it's a noun ('sourdough bread') and we
    use noun-shaped templates instead. This keeps every title grammatical."""
    had_intent = strip_intent(topic) != topic.strip()
    core_words = keywords(strip_intent(topic))
    first = core_words[0] if core_words else ""
    is_action = had_intent or first in COMMON_VERBS
    return {
        "core": title_case(strip_intent(topic)),
        "core_lower": strip_intent(topic).lower(),
        "noun": topic_noun(topic),
        "is_action": is_action,
        "n": str(min(max(len(core_words) + 3, 5), 9)),
    }


def title_case(text):
    small = {"a", "an", "the", "to", "for", "of", "and", "or", "in", "on", "with", "without"}
    words = text.split()
    out = []
    for i, w in enumerate(words):
        if i != 0 and i != len(words) - 1 and w.lower() in small:
            out.append(w.lower())
        else:
            out.append(w[:1].upper() + w[1:] if w else w)
    return " ".join(out)


def build_titles(topic, playbook, audience=None):
    """Fill each current title formula with the topic to produce candidates."""
    p = parse_topic(topic)
    core, noun, action = p["core"], p["noun"], p["is_action"]
    pain = "Overthinking It" if not audience else "the Overwhelm"

    formulas = playbook["title"]["formulas"]
    candidates = []
    for f in formulas:
        name = f["name"]
        if name == "curiosity_gap":
            t = f"Why Most People Fail to {core}" if action else f"Why Your {noun} Isn't Working"
        elif name == "number_listicle":
            t = f"{p['n']} {noun} Tips That Actually Work"
        elif name == "how_to_outcome":
            t = (f"How to {core} (Without {pain})" if action
                 else f"How to Get {noun} Right (Without {pain})")
        elif name == "mistake_warning":
            t = f"The {noun} Mistake That Ruins Most People's Results"
        elif name == "i_tried_result":
            t = f"I Focused on {noun} for 30 Days - Here's What Happened"
        elif name == "contrarian":
            t = f"Stop Making {noun} Harder Than It Needs to Be"
        else:
            t = f"{core}: {f.get('template', '')}".strip(": ")
        candidates.append({"formula": name, "title": t, "why": f.get("why", "")})
    return candidates


def score_title(title, playbook):
    """Score a title 0-100 against the playbook's current CTR heuristics."""
    cfg = playbook["title"]["scoring"]
    power_words = [w.lower() for w in playbook["title"].get("power_words", [])]
    low = title.lower()
    n = len(title)
    lo, hi = cfg["ideal_char_range"]

    score = float(cfg.get("base_score", 50))
    reasons = []

    if n > hi:
        pen = (n - hi) * cfg["too_long_penalty_per_char_over"]
        score -= pen
        reasons.append(f"-{pen:.0f} too long ({n} chars; will truncate ~{hi})")
    elif n < lo:
        pen = (lo - n) * cfg["too_short_penalty_per_char_under"]
        score -= pen
        reasons.append(f"-{pen:.0f} short ({n} chars; room to add specificity)")
    else:
        bonus = cfg.get("in_range_bonus", 0)
        score += bonus
        reasons.append(f"+{bonus} length in range ({n} chars)")

    if re.search(r"\d", title):
        score += cfg["has_number_bonus"]
        reasons.append(f"+{cfg['has_number_bonus']} has a number")

    hit = next((w for w in power_words if re.search(rf"\b{re.escape(w)}\b", low)), None)
    if hit:
        score += cfg["has_power_word_bonus"]
        reasons.append(f"+{cfg['has_power_word_bonus']} power word ('{hit}')")

    if low.startswith(("why", "how", "the", "stop")) or "?" in title:
        score += cfg["curiosity_gap_bonus"]
        reasons.append(f"+{cfg['curiosity_gap_bonus']} opens a curiosity gap")

    letters = [c for c in title if c.isalpha()]
    if letters and sum(c.isupper() for c in letters) / len(letters) > 0.7:
        score -= cfg["all_caps_penalty"]
        reasons.append(f"-{cfg['all_caps_penalty']} reads as ALL CAPS")

    # keyword front-loading: first content word appears in first 3 words
    first_words = " ".join(title.split()[:3]).lower()
    kw = keywords(title)
    if kw and kw[0] in first_words:
        score += cfg["keyword_front_loaded_bonus"]
        reasons.append(f"+{cfg['keyword_front_loaded_bonus']} keyword front-loaded")

    score = max(0, min(cfg.get("max_score", 100), round(score)))
    return score, reasons


def build_hook(topic, playbook):
    p = parse_topic(topic)
    core, noun, action = p["core_lower"], p["noun"], p["is_action"]
    patterns = playbook["hook"]["patterns"]
    out = []
    for pat in patterns:
        name = pat["name"]
        if name == "promise_proof":
            line = (f"By the end of this you'll know exactly how to {core}. Here's proof it works:"
                    if action else
                    f"By the end of this you'll nail {noun} on the first try. Here's proof it works:")
        elif name == "contradiction":
            line = f"Everyone treats {noun} like it's complicated. That's exactly why most people never start."
        elif name == "cold_open_result":
            line = f"This is what {noun} looks like when it's done right. Let me show you how I got here."
        elif name == "cost_of_ignoring":
            line = (f"If you're trying to {core} the usual way, you're wasting hours. Here's the shortcut."
                    if action else
                    f"If you're struggling with {noun}, you're probably making one mistake. Here's the fix.")
        else:
            line = pat.get("example", "")
        out.append({"pattern": name, "line": line})
    return out


def render_human(topic, playbook, titles, hook, audience, count):
    P = playbook
    days, stale, fresh_msg = playbook_freshness(P)
    lines = []
    w = lines.append

    w("=" * 68)
    w(f"  VIDEO BRIEF:  {topic}")
    if audience:
        w(f"  Audience:     {audience}")
    w(f"  {fresh_msg}")
    w("=" * 68)

    # --- Titles, ranked ---
    w("\n## TITLE CANDIDATES (ranked by current CTR heuristics)\n")
    scored = []
    for c in titles:
        s, reasons = score_title(c["title"], P)
        scored.append((s, c, reasons))
    scored.sort(key=lambda x: x[0], reverse=True)
    for i, (s, c, reasons) in enumerate(scored[:count], 1):
        bar = "#" * (s // 10) + "-" * (10 - s // 10)
        w(f"{i}. [{s:>3}/100] [{bar}]  {c['title']}")
        w(f"        formula: {c['formula']}  |  {', '.join(reasons)}")
    w("\n   Tip: the title and thumbnail are ONE unit - don't repeat text between them.")

    # --- Thumbnail brief ---
    tb = P["thumbnail"]
    w("\n## THUMBNAIL BRIEF\n")
    w(f"   Spec: {tb['spec']}   |   Max text: {tb['text_word_max']} words")
    for m in tb["must_have"]:
        w(f"   - {m}")
    w("   Principles:")
    for pr in tb["principles"]:
        w(f"     * {pr}")

    # --- Hook ---
    w(f"\n## HOOK (first {P['hook']['first_seconds']}s) - pick one, say it before anything else\n")
    for h in hook:
        w(f"   [{h['pattern']}]")
        w(f"     \"{h['line']}\"")
    w("   Rules:")
    for pr in P["hook"]["principles"]:
        w(f"     * {pr}")

    # --- Retention outline ---
    rs = P["retention_structure"]
    w("\n## RETENTION-OPTIMIZED OUTLINE (aim 6-10 min)\n")
    for seg in rs["segments"]:
        w(f"   {seg['seconds']:>9}  {seg['name']}")
        w(f"              job:    {seg['job']}")
        w(f"              tactic: {seg['tactic']}")
    w("   Across the whole video:")
    for t in rs["tactics"]:
        w(f"     * {t}")

    # --- What the algorithm rewards right now ---
    al = P["algorithm_signals"]
    w("\n## WHAT TO OPTIMIZE FOR RIGHT NOW\n")
    w(f"   Equation: {al['primary_equation']}")
    for pri in al["optimize_for_in_order"]:
        w(f"     - {pri}")
    w("   Confirmed recent changes:")
    for ch in al["confirmed_changes_2026"]:
        w(f"     * {ch}")

    b = P["benchmarks"]
    w("\n## BENCHMARKS TO CHECK YOURSELF AGAINST\n")
    w(f"   CTR: weak {b['ctr_percent']['weak']}% / ok {b['ctr_percent']['ok']}% / "
      f"good {b['ctr_percent']['good']}% / great {b['ctr_percent']['great']}%")
    w(f"   Avg % viewed: floor {b['avg_percentage_viewed']['floor']}% / "
      f"target {b['avg_percentage_viewed']['target']}% / strong {b['avg_percentage_viewed']['strong']}%")
    w(f"   First 30s retention: target {b['first_30s_retention_percent']['target']}%")
    w(f"   Length: {b['ideal_length_minutes']['min']}-{b['ideal_length_minutes']['sweet_spot']} min sweet spot")

    if stale:
        w("\n" + "!" * 68)
        w("  " + fresh_msg)
        w("!" * 68)

    return "\n".join(lines)


def build_brief(topic, playbook, audience=None, count=6):
    titles = build_titles(topic, playbook, audience)
    scored = []
    for c in titles:
        s, reasons = score_title(c["title"], playbook)
        scored.append({**c, "score": s, "score_reasons": reasons})
    scored.sort(key=lambda x: x["score"], reverse=True)
    hook = build_hook(topic, playbook)
    days, stale, fresh_msg = playbook_freshness(playbook)
    return {
        "topic": topic,
        "audience": audience,
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "playbook_version": playbook.get("meta", {}).get("version"),
        "playbook_last_updated": playbook.get("meta", {}).get("last_updated"),
        "playbook_stale": stale,
        "titles": scored[:count],
        "thumbnail": playbook["thumbnail"],
        "hook": hook,
        "retention_structure": playbook["retention_structure"],
        "algorithm_signals": playbook["algorithm_signals"],
        "benchmarks": playbook["benchmarks"],
    }


def main():
    ap = argparse.ArgumentParser(
        description="Generate an algorithm-optimized YouTube video brief from a topic."
    )
    ap.add_argument("topic", help="What the video is about, e.g. 'how to start a youtube channel'")
    ap.add_argument("--audience", help="Who it's for, e.g. 'busy parents'", default=None)
    ap.add_argument("--count", type=int, default=6, help="How many title candidates to show")
    ap.add_argument("--json", action="store_true", help="Output machine-readable JSON")
    args = ap.parse_args()

    playbook = load_playbook()

    if args.json:
        brief = build_brief(args.topic, playbook, args.audience, args.count)
        print(json.dumps(brief, indent=2))
        return

    titles = build_titles(args.topic, playbook, args.audience)
    hook = build_hook(args.topic, playbook)
    print(render_human(args.topic, playbook, titles, hook, args.audience, args.count))


if __name__ == "__main__":
    main()
