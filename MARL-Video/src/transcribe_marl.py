#!/usr/bin/env python3
"""Transcribe MARL narration audio with word-level timestamps using faster-whisper.
Audio is the master timeline -> output a word-level JSON event map.
"""
import json
import sys
from faster_whisper import WhisperModel

AUDIO = "/home/z/my-project/download/drive_folder_1/multi_agent_reinforcement_learning_charon_final.wav"
OUT = "/home/z/my-project/work/marl_video/transcript_words.json"

print("Loading model (small.en for accuracy)...", flush=True)
model = WhisperModel("small.en", device="cpu", compute_type="int8")

segments_iter, info = model.transcribe(
    AUDIO,
    language="en",
    word_timestamps=True,
    vad_filter=True,
    vad_parameters={"min_silence_duration_ms": 400},
    beam_size=5,
)

segments = []
words = []
for seg in segments_iter:
    seg_dict = {
        "start": round(seg.start, 3),
        "end": round(seg.end, 3),
        "text": seg.text.strip(),
    }
    seg_words = []
    if seg.words:
        for w in seg.words:
            wd = {
                "word": w.word.strip(),
                "start": round(w.start, 3),
                "end": round(w.end, 3),
                "prob": round(w.probability, 3),
            }
            seg_words.append(wd)
            words.append(wd)
    seg_dict["words"] = seg_words
    segments.append(seg_dict)
    done = seg.end
    print(f"  segment to {done:.1f}s / {info.duration:.1f}s  ({done/info.duration*100:.0f}%)", flush=True)

result = {
    "audio": AUDIO,
    "duration": info.duration,
    "language": info.language,
    "segments": segments,
    "words": words,
}
with open(OUT, "w") as f:
    json.dump(result, f, indent=1)

print(f"\nDONE: {len(words)} words, {len(segments)} segments -> {OUT}")
