"""Generate SINGLE-WORD English overlay (ASS) from words.json + gloss_final.json.

Rule (user requirement): screen par koi subtitles NAHI, koi poori lines NAHI,
sirf ONE English word at a time — the word being spoken right now.

Display policy:
  - only content words (gloss non-empty, prob >= MIN_P)
  - word appears at its exact audio start -> stays until next displayed word
  - cleared after HOLD_MAX if a silence gap follows (no text during silence)
  - uppercase, bold, letter-spaced, bottom-center, NO box (not subtitle look)
"""
import json
import re

BASE = "/home/z/my-project"
MIN_P = 0.50     # skip low-confidence ASR words
HOLD_MAX = 2.5   # max seconds a word stays during gaps
ACRONYMS = {"agi": "AGI", "ai": "AI"}

# USER RULE: on-screen text = SINGLE ENGLISH WORDS ONLY.
# Blocklist: romanized Hindi/Urdu + garbled ASR artifacts that leaked through
# the gloss map (ASCII words bypass the Devanagari script filter).
BLOCKLIST = {"ANDAZA", "INSAAN", "KAAM", "POORANI", "ISI", "PO", "NAHIN",
             "HAI", "HAIN", "KA", "KI", "KE", "KO", "SE", "PAR", "BHI",
             "YA", "YAHI", "WAHI", "KUCH", "JO", "TO", "HI", "NA"}
# garbled ASR spelling -> proper English display
REMAP = {"CHEKK": "CHECK", "CHEK": "CHECK", "CHEQUE": "CHECK"}

PUNCT = "।.,!?;:\"'()[]{}-–—…"


def strip_punct(w):
    return w.strip(PUNCT).strip()


def ts(sec):
    ms = max(0, int(round(sec * 1000)))
    h, rem = divmod(ms, 3600000)
    m, rem = divmod(rem, 60000)
    s, ms = divmod(rem, 1000)
    return "%d:%02d:%02d.%02d" % (h, m, s, ms // 10)


def build_events(words, gloss):
    """Chain: each displayed word holds until the next displayed word starts."""
    shown = []  # (start, end_open, text)
    for w in words:
        if w.get("p", 1.0) < MIN_P:
            continue
        key = strip_punct(w["w"])
        g = gloss.get(key, "")
        if not g:
            continue
        if g.upper() in BLOCKLIST:
            continue
        g = REMAP.get(g.upper(), g)
        g = ACRONYMS.get(g, g)
        shown.append({"start": w["start"], "end_spoken": w["end"], "text": g})

    events = []
    for i, s in enumerate(shown):
        if i + 1 < len(shown):
            nxt = shown[i + 1]["start"]
            end = min(nxt, s["start"] + HOLD_MAX) if (nxt - s["end_spoken"]) > HOLD_MAX else nxt
            # if next comes continuously, hold until it starts
            if (nxt - s["end_spoken"]) <= HOLD_MAX:
                end = nxt
        else:
            end = min(s["end_spoken"] + 1.2, s["start"] + HOLD_MAX)
        if end <= s["start"]:
            end = s["start"] + 0.15
        events.append((s["start"], end, s["text"]))
    return events


def main():
    data = json.load(open(f"{BASE}/data/words.json", encoding="utf-8"))
    gloss = json.load(open(f"{BASE}/data/gloss_final.json", encoding="utf-8"))
    dur = data["duration"]

    events = build_events(data["words"], gloss)
    print(f"[overlay] {len(events)} word events (of {len(data['words'])} spoken words)")

    header = f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1280
PlayResY: 720
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Word,DejaVu Sans,46,&H00FFFFFF,&H00FFFFFF,&H00141414,&H90000000,1,0,0,0,100,100,2.5,0,1,2.2,1.2,2,60,60,34,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    lines = []
    for (t0, t1, text) in events:
        t1 = min(t1, dur)
        disp = text.upper()
        # safety: never render Devanagari / non-latin on screen
        if not re.fullmatch(r"[A-Z0-9][A-Z0-9 &'-]*", disp):
            continue
        lines.append("Dialogue: 0,%s,%s,Word,,0,0,0,,{\\fsp2.5}%s" %
                     (ts(t0), ts(t1), disp))

    with open(f"{BASE}/data/word_overlay.ass", "w", encoding="utf-8") as f:
        f.write(header + "\n".join(lines) + "\n")
    print(f"[overlay] wrote {BASE}/data/word_overlay.ass ({len(lines)} events)")


if __name__ == "__main__":
    main()
