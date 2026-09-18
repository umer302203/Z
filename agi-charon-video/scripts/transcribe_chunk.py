"""Transcribe ONE chunk (foreground) -> data/chunks/words_XX.json with global times.

Usage: python3.13 transcribe_chunk.py <idx>
"""
import json
import os
import sys

from faster_whisper import WhisperModel

BASE = "/home/z/my-project"
MANIFEST = f"{BASE}/data/chunks/manifest.json"
OUT_DIR = f"{BASE}/data/chunks"

idx = int(sys.argv[1])
with open(MANIFEST) as f:
    manifest = json.load(f)
chunk = [c for c in manifest if c["idx"] == idx][0]

model = WhisperModel("small", device="cpu", compute_type="int8", cpu_threads=2)
segments_iter, info = model.transcribe(
    chunk["path"],
    word_timestamps=True,
    beam_size=1,
    condition_on_previous_text=False,
    language="hi",
)

off = chunk["global_offset"]
core0, core1 = chunk["core_start"], chunk["core_end"]
words = []
segs = []
for seg in segments_iter:
    segs.append({
        "start": round(seg.start + off, 3),
        "end": round(seg.end + off, 3),
        "text": seg.text.strip(),
    })
    for w in seg.words or []:
        token = (w.word or "").strip()
        if not token:
            continue
        gw_start = w.start + off
        gw_end = w.end + off
        words.append({
            "w": token,
            "start": round(gw_start, 3),
            "end": round(gw_end, 3),
            "p": round(w.probability, 3),
            "core": 1 if (gw_start >= core0 - 0.15 and gw_end <= core1 + 0.15) else 0,
        })

out = {"idx": idx, "language": info.language, "words": words, "segments": segs}
with open(f"{OUT_DIR}/words_{idx:02d}.json", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False)
n_core = sum(1 for w in words if w["core"])
print(f"[chunk {idx}] words={len(words)} core={n_core} lang={info.language} "
      f"range={chunk['core_start']:.1f}-{chunk['core_end']:.1f}", flush=True)
