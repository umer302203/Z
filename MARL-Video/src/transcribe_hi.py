#!/usr/bin/env python3
"""Full transcription with word timestamps - language=hi (Hinglish narration)."""
import json
from faster_whisper import WhisperModel

AUDIO = "/home/z/my-project/download/drive_folder_1/multi_agent_reinforcement_learning_charon_final.wav"
OUT = "/home/z/my-project/work/marl_video/transcript_hi_words.json"

print("Loading multilingual small model...", flush=True)
model = WhisperModel("small", device="cpu", compute_type="int8")

segments_iter, info = model.transcribe(
    AUDIO,
    language="hi",
    word_timestamps=True,
    vad_filter=True,
    vad_parameters={"min_silence_duration_ms": 350},
    beam_size=5,
    initial_prompt="यह एक educational video है about multi-agent reinforcement learning, agents, environment, actions, rewards, policy, cooperation, competition, warehouse robots, drones.",
)

segments, words = [], []
for seg in segments_iter:
    seg_dict = {"start": round(seg.start, 3), "end": round(seg.end, 3), "text": seg.text.strip()}
    seg_words = []
    if seg.words:
        for w in seg.words:
            wd = {"word": w.word.strip(), "start": round(w.start, 3), "end": round(w.end, 3), "prob": round(w.probability, 3)}
            seg_words.append(wd)
            words.append(wd)
    seg_dict["words"] = seg_words
    segments.append(seg_dict)

with open(OUT, "w") as f:
    json.dump({"audio": AUDIO, "duration": info.duration, "language": info.language, "segments": segments, "words": words}, f, indent=1, ensure_ascii=False)
print(f"\nDONE: {len(words)} words, {len(segments)} segments -> {OUT}")
