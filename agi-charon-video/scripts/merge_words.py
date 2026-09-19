"""Merge per-chunk word JSONs -> data/words.json (core words only, deduped, sorted)."""
import glob
import json

BASE = "/home/z/my-project"

all_words = []
all_segs = []
lang = "hi"
for path in sorted(glob.glob(f"{BASE}/data/chunks/words_*.json")):
    with open(path, encoding="utf-8") as f:
        d = json.load(f)
    lang = d.get("language", lang)
    for w in d["words"]:
        if w.get("core", 1) == 1:
            all_words.append((w["start"], w["end"], w))
    for s in d["segments"]:
        all_segs.append(s)

all_words.sort(key=lambda x: (x[0], x[1]))
words = [w for _, _, w in all_words]

# drop exact duplicates (same start & word) from tiny overlaps
deduped = []
for w in words:
    if deduped and abs(w["start"] - deduped[-1]["start"]) < 0.02 and w["w"] == deduped[-1]["w"]:
        continue
    deduped.append(w)

# ensure monotonic non-overlapping ends (clamp)
for i in range(1, len(deduped)):
    if deduped[i]["start"] < deduped[i - 1]["end"] - 0.001:
        mid = (deduped[i]["start"] + deduped[i - 1]["end"]) / 2
        deduped[i - 1]["end"] = round(mid, 3)
        deduped[i]["start"] = round(mid, 3)

all_segs.sort(key=lambda s: s["start"])
text = " ".join(s["text"] for s in all_segs)

out = {
    "language": lang,
    "duration": 837.84,
    "text": text,
    "words": deduped,
    "segments": all_segs,
}
with open(f"{BASE}/data/words.json", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)

print(f"[merge] words={len(deduped)} segments={len(all_segs)} lang={lang}")
print(f"[merge] first={deduped[0]['w']}@{deduped[0]['start']} last={deduped[-1]['w']}@{deduped[-1]['start']}")
