#!/usr/bin/env python3
"""Test language detection on first 90s of audio."""
from faster_whisper import WhisperModel
import json

model = WhisperModel("small", device="cpu", compute_type="int8")

# detect language
segs_iter, info = model.transcribe(
    "/home/z/my-project/download/drive_folder_1/multi_agent_reinforcement_learning_charon_final.wav",
    word_timestamps=False, vad_filter=True, beam_size=5,
)
print("Detected language:", info.language, "prob:", round(info.language_probability, 3))

out = []
for seg in list(segs_iter)[:14]:
    out.append(f"[{seg.start:7.2f}-{seg.end:7.2f}] {seg.text.strip()}")
print("\n".join(out))
