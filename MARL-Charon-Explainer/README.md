# MARL-Charon-Explainer

Audio-first Manim explainer video: **"Multi-Agent Reinforcement Learning"** (13 min).

Generated 100% locally (no cloud AI APIs): the supplied narration audio is the
master timeline; transcription, visual planning, Manim code generation,
rendering, assembly and QC all ran locally in the Z.ai environment.

## Structure

| Path | Purpose |
|---|---|
| `input/original_audio.wav` | MASTER AUDIO (supplied, preserved bit-exact, md5 28a03e119cbf3dc5c818af297ace5bbb) |
| `input/working_audio_16k.wav` | 16 kHz processing copy for transcription only |
| `transcript/transcript_timestamps.json` | Sentence + word-level timestamps (faster-whisper small, int8, local) |
| `transcript/transcript_readable.txt` | Human-readable transcript |
| `planning/visual_scene_plan.json` | 33-scene visual director plan with word-anchored event map |
| `scenes/common.py` | Sync engine (frame-exact 60 fps timing) + visual library |
| `scenes/scene_001..033.py` | One Manim scene per plan entry |
| `output/final_video.mp4` | FINAL DELIVERABLE - 1920x1080 @ 60 fps, original narration |
| `logs/` | Transcription + render logs |
| `scripts/` | Pipeline scripts (plan builder, renderer, assembler, validator) |
| `VIDEO_RULES.txt` | Master production rules followed by this project |

## Pipeline

audio → local ASR (word timestamps) → semantic scene segmentation (33 scenes)
→ visual plan (word-level event map) → Manim CE 0.18.1 code (frame-snapped
SyncedScene timing) → render 1080p60 → per-scene frame-exact conformance →
concat → mux ORIGINAL audio (never regenerated).

## Key facts

- Audio duration: 779.357 s; final video: 779.367 s (frame-grid aligned)
- 33 scenes, 46,762 frames, H.264 + AAC 192k
- Topic: Multi-Agent RL - football analogy, RL loop, MARL definition,
  cooperation/competition, non-stationarity, credit assignment, delayed
  reward, partial observability, applications (traffic/warehouse/drones),
  CTDE, limitations, stability, communication, exploration, evaluation,
  future + responsibility.
