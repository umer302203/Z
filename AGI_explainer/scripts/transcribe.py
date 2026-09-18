"""transcribe.py — faster-whisper small/int8, word timestamps -> JSON.
Usage: python3 transcribe.py <audio.wav> <out.json>"""
import json, sys

from faster_whisper import WhisperModel

audio, out = sys.argv[1], sys.argv[2]
model = WhisperModel("small", device="cpu", compute_type="int8")
segments, info = model.transcribe(audio, word_timestamps=True, language="en",
                                  vad_filter=True)
segs = []
for s in segments:
    segs.append({
        "start": round(s.start, 3),
        "end": round(s.end, 3),
        "text": s.text.strip(),
        "words": [{"w": w.word.strip(), "start": round(w.start, 3),
                   "end": round(w.end, 3)} for w in (s.words or [])],
    })
data = {"language": info.language, "duration": round(info.duration, 2),
        "segments": segs}
with open(out, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=1)
print(f"TRANSCRIPT OK: {len(segs)} segments, {info.duration:.2f}s, "
      f"lang={info.language} -> {out}")
