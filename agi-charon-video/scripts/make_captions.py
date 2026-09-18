"""Generate word-level karaoke ASS captions from data/words.json.

Grouping: max 6 words / 3.6s per caption line, break at punctuation.
Karaoke: \k centisecond durations (Primary = spoken/highlight, Secondary = upcoming).
Font/RTL chosen based on transcript language.
"""
import json
import os
import sys

BASE = "/home/z/my-project"

PUNCT_BREAK = ("。", "！", "？", ".", "!", "?", "؟", "|")
FONT_MAP = {
    "en": ("DejaVu Sans", False),
    "hi": ("Noto Sans Devanagari", False),
    "ur": ("Noto Nastaliq Urdu", True),
    "pa": ("Noto Sans Gurmukhi", False),
    "bn": ("Noto Sans Bengali", False),
}


def group_lines(words, max_words=6, max_gap=0.8, max_dur=3.8):
    lines = []
    cur = []
    for w in words:
        cur.append(w)
        text_joined = "".join(x["w"] for x in cur) if False else " ".join(x["w"] for x in cur)
        dur = w["end"] - cur[0]["start"]
        big_gap = cur[-1]["w"].endswith(tuple(PUNCT_BREAK))
        if len(cur) >= max_words or dur >= max_dur or big_gap:
            lines.append(cur)
            cur = []
    if cur:
        lines.append(cur)
    return lines


def ts(sec):
    ms = int(round(sec * 1000))
    h, rem = divmod(ms, 3600000)
    m, rem = divmod(rem, 60000)
    s, ms = divmod(rem, 1000)
    return "%d:%02d:%02d.%02d" % (h, m, s, ms // 10)


def main():
    with open(f"{BASE}/data/words.json", encoding="utf-8") as f:
        data = json.load(f)

    lang = data.get("language", "en")
    font, rtl = FONT_MAP.get(lang, ("DejaVu Sans", False))
    words = data["words"]
    lines = group_lines(words)

    fs = 46 if not rtl else 40
    primary = "&H0000E5FF"    # BGR: warm yellow highlight (spoken)
    secondary = "&H00F0F0F0"  # near white (upcoming)
    back = "&HA0000000"

    header = f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1280
PlayResY: 720
WrapStyle: 0
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Karaoke,{font},{fs},{primary},{secondary},&H00202020,{back},1,0,0,0,100,100,0,0,1,2,1,2,60,60,42,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    events = []
    for ln in lines:
        t0 = max(0.0, ln[0]["start"] - 0.05)
        t1 = min(data["duration"], ln[-1]["end"] + 0.35)
        parts = []
        prev_end = ln[0]["start"]
        for i, w in enumerate(ln):
            gap_cs = max(0, int(round((w["start"] - prev_end) * 100)))
            if gap_cs > 0:
                parts.append("{\\k%d}%s" % (gap_cs, " "))
            dur_cs = max(1, int(round((w["end"] - w["start"]) * 100)))
            parts.append("{\\k%d}%s" % (dur_cs, w["w"]))
            prev_end = w["end"]
        text = "".join(parts)
        events.append("Dialogue: 0,%s,%s,Karaoke,,0,0,0,,%s" % (ts(t0), ts(t1), text))

    os.makedirs(f"{BASE}/data", exist_ok=True)
    with open(f"{BASE}/data/captions.ass", "w", encoding="utf-8") as f:
        f.write(header + "\n".join(events) + "\n")

    print(f"[captions] lang={lang} font={font} rtl={rtl} lines={len(lines)} words={len(words)}")
    print(f"[captions] wrote {BASE}/data/captions.ass")


if __name__ == "__main__":
    main()
