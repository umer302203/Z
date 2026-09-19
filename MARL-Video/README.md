# MARL-Video — Multi-Agent Reinforcement Learning explainer (13 min)

Dedicated project folder (per VIDEO_RULES.txt §17). Final deliverable:
**1920x1080 @ 60fps, 779.35s (12:59), h264+aac** — a fully programmatic
3Blue1Brown-style explainer with **word-level sync** (text appears exactly when its
word is spoken) and **semantic sound effects** (234 SFX events bound to the same
word-synced anchors).

## Structure

| Folder | Contents |
|--------|----------|
| `audio/` | `narration.wav` — source narration (24kHz mono); `mix_report.json` — final mix stats |
| `transcript/` | Hindi/Urdu word-level transcript (`transcript_hi_readable.txt`, `transcript_hi_words.json`) + `anchors.json` (238 visual anchors at word onsets) |
| `plan/` | `scenes.md` — visual plan / scene table |
| `src/` | Full pipeline source (Python): transcription → event map → render engine → scenes → SFX → mix → finalize → QC |
| `sfx/` | 14 synthesized sound-effect kits (numpy-generated WAVs) |
| `qc/` | `QC_REPORT.md` + contact sheets + fix-verification frames |
| `final/` | Final video (1080p, split into <100MB parts for GitHub + 720p preview) + rejoin instructions |
| `VIDEO_RULES.txt` | Copy of the production rules this project follows |

## Pipeline (how to rebuild)

```bash
# 1. transcript + word timestamps (faster-whisper)
python3 src/transcribe_marl.py            # -> transcript_hi_words.json
python3 src/fix_gaps.py                   # re-transcribe ASR-skipped regions, merge
python3 src/build_eventmap.py             # -> anchors.json (238 word-synced anchors)

# 2. sound effects + mix (234 events at word times, speech-aware ducking)
python3 src/make_sfx.py                   # -> sfx/*.wav
python3 src/audio_mix.py                  # -> audio/final_mix.wav

# 3. render (any absolute time range; run ranges in parallel)
python3 src/render.py 0   120 seg1.mp4
python3 src/render.py 120 240 seg2.mp4
#   ... seg3-seg6 at 120s each, seg7 = 720..779.357

# 4. finalize: concat segments + mux audio
python3 src/finalize.py                   # -> final MP4

# 5. QC
python3 src/smoke_test.py && python3 src/qc_final.py
```

Requirements: Python 3.10+, numpy, pillow, scipy, faster-whisper, ffmpeg on PATH.
Rendering is deterministic (every frame is a pure function of absolute time), so
segments re-render independently with zero seam risk.

## Key design points

- **Word-level sync**: 238 anchors from whisper word timestamps; ASR-skipped gaps were
  re-transcribed separately and merged so no spoken region is left unsynced.
- **Relevant SFX**: each sound maps to a semantic event (chip appear, panel slide,
  verified moment, drone patrol, fail thud...), not random decoration; ducked under
  narration with a speech-aware envelope.
- **Rules compliance**: English-only short screen labels, no subtitles/progress bars,
  no fabricated logos or official interfaces, old scenes cleared before new ones.
