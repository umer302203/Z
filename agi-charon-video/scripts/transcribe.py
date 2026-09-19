#!/usr/bin/env python3.13
"""Word-level transcription of the AGI audio using faster-whisper.

Output: /home/z/my-project/data/words.json
{
  "language": "xx",
  "duration": 837.84,
  "text": "...",
  "words": [{"w": "word", "start": 0.0, "end": 0.21, "p": 0.97}, ...],
  "segments": [{"start":..., "end":..., "text": "..."}]
}
"""
import json
import os
import sys

from faster_whisper import WhisperModel

AUDIO = "/home/z/my-project/upload/what_architecture_could_ai_need_for_agi_charon.wav"
OUT = "/home/z/my-project/data/words.json"
MODEL_SIZE = os.environ.get("WHISPER_MODEL", "small")

os.makedirs(os.path.dirname(OUT), exist_ok=True)

print(f"[transcribe] loading model {MODEL_SIZE} (int8, cpu)...", flush=True)
model = WhisperModel(MODEL_SIZE, device="cpu", compute_type="int8", cpu_threads=2)

print("[transcribe] running transcription with word timestamps...", flush=True)
segments_iter, info = model.transcribe(
    AUDIO,
    word_timestamps=True,
    vad_filter=True,
    vad_parameters={"min_silence_duration_ms": 400},
    beam_size=1,
    condition_on_previous_text=False,
)

words = []
segments = []
full_text_parts = []


def save_partial():
    result = {
        "language": info.language,
        "language_probability": round(float(info.language_probability), 3),
        "duration": round(float(info.duration), 3),
        "text": " ".join(full_text_parts),
        "words": words,
        "segments": segments,
    }
    with open(OUT + ".partial", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False)


for seg in segments_iter:
    segments.append({
        "start": round(seg.start, 3),
        "end": round(seg.end, 3),
        "text": seg.text.strip(),
    })
    full_text_parts.append(seg.text.strip())
    for w in seg.words:
        token = (w.word or "").strip()
        if not token:
            continue
        words.append({
            "w": token,
            "start": round(w.start, 3),
            "end": round(w.end, 3),
            "p": round(w.probability, 3),
        })
    print(f"[seg {seg.start:7.1f}-{seg.end:7.1f}] {seg.text.strip()[:70]}", flush=True)
    save_partial()

result = {
    "language": info.language,
    "language_probability": round(float(info.language_probability), 3),
    "duration": round(float(info.duration), 3),
    "text": " ".join(full_text_parts),
    "words": words,
    "segments": segments,
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=1)

print(f"[transcribe] DONE language={info.language} words={len(words)} "
      f"segments={len(segments)} duration={info.duration:.1f}s", flush=True)
print("[transcribe] saved to", OUT, flush=True)
save_partial()
