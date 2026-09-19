#!/usr/bin/env python3
"""Re-transcribe missed speech regions (81.4-91.5, 102.3-108.8) and merge into transcript."""
import json, wave
import numpy as np
from faster_whisper import WhisperModel

AUDIO = "/home/z/my-project/download/drive_folder_1/multi_agent_reinforcement_learning_charon_final.wav"
TR = "/home/z/my-project/work/marl_video/transcript_hi_words.json"

# read audio regions and save temp wavs
regions = [(79.0, 92.5), (100.5, 110.5)]
paths = []
for i, (a, b) in enumerate(regions):
    w = wave.open(AUDIO)
    sr = w.getframerate()
    w.setpos(int(a*sr))
    data = w.readframes(int((b-a)*sr))
    out = f"/home/z/my-project/work/marl_video/chunks/regap_{i}.wav"
    ow = wave.open(out, "wb")
    ow.setnchannels(1); ow.setsampwidth(2); ow.setframerate(sr)
    ow.writeframes(data); ow.close()
    paths.append((out, a))

model = WhisperModel("small", device="cpu", compute_type="int8")
d = json.load(open(TR))
new_segs, new_words = [], []
for (path, off) in paths:
    segs_iter, info = model.transcribe(path, language="hi", word_timestamps=True, beam_size=5,
        initial_prompt="multi-agent reinforcement learning, warehouse robots, traffic, drones, cooperation, competition")
    for seg in segs_iter:
        new_segs.append({"start": round(seg.start+off,3), "end": round(seg.end+off,3), "text": seg.text.strip(),
                         "words": [{"word": w.word.strip(), "start": round(w.start+off,3), "end": round(w.end+off,3), "prob": round(w.probability,3)} for w in (seg.words or [])]})
        new_words.extend(new_segs[-1]["words"])
        print(f"  [{seg.start+off:.2f}-{seg.end+off:.2f}] {seg.text.strip()}")

# merge: replace segments/words overlapping the regions
all_segs = [s for s in d["segments"] if not any(s["start"] >= a-1 and s["end"] <= b+1 for (a,b) in regions)] + new_segs
all_segs.sort(key=lambda s: s["start"])
all_words = []
for s in all_segs:
    all_words.extend(s.get("words", []))
d["segments"] = all_segs
d["words"] = all_words
json.dump(d, open(TR, "w"), indent=1, ensure_ascii=False)
print(f"\nMERGED: {len(all_words)} words, {len(all_segs)} segments")
