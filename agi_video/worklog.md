# AGI Explainer — Multi-Reset Recovery Worklog (v4)

## Project
- Topic: "What architecture could AI need for AGI"
- Narration: audio/narration_AGI_locked_837s.wav — 837.84s LOCKED (matches v1 input)
- Output: 1280x720 @ 24fps Workbench, 20,110 frames, final = frames + narration mux
- Alt asset (NOT this project): audio/alt_why_ai_hallucinates_558s.wav (558.12s, different topic)

## Hard Rules
- On-screen text: English only, NO subtitles, NO full lines — ONLY short words (<=3 words + symbols)
- Timing authority = narration wav; meaning-based segmentation via word-stem anchors
- GITHUB-FIRST: every file pushed to repo Z immediately after write
- Repo Z is MULTI-TENANT: ONLY agi_video/** is mine; nothing of mine outside that folder
- Daemonization: double-fork only (fork/setsid/fork, PPID=1) — plain nohup/setsid die

## Reset History (rebuilds)
- Reset #1, #2: v1/v2 losses → led to upload/ root-mount + download/ insurance
- Reset #3 (~Sep 18): v3 GITHUB-FIRST rebuild started; push failed 403 (old token)
- Reset #4 (Sep 19 ~00:57): everything wiped again except upload/, download/, skills/
  → v4: NEW token works (push:true verified), wav pushed to Z FIRST, all code re-pushed as written

## Proven Environment Recipe (rebuild exactly this)
- blender-4.5.3-linux-x64 tarball
- Mesa GL from Debian TRIXXIE (25.0.7) — sid 26.2.3 BROKE EGL, do not use
- LIBGL_ALWAYS_SOFTWARE=1, __EGL_VENDOR_LIBRARY_FILENAMES=mesaegl.json
- faster-whisper small/int8, word_timestamps=True, vad_filter
- ffmpeg for mux

## v4 File Map (all inside agi_video/)
- scripts/transcribe.py   — wav → reports/transcript_timestamps.json
- scripts/lib_scene.py    — FPS/geometry/anim helpers, ob['text_body'] tagging
- scripts/specs.py        — 20 builders b_s01..b_s20 + SEQ anchors
- scripts/scene_generator.py — windows→build→camera bake→validate→blend
- scripts/verify_text.py  — AST-level TEXT RULE audit (<=3 words)
- scripts/setup_env.sh    — 5-stage env rebuild (idempotent)
- scripts/daemonize.py    — double-fork launcher
- scripts/autocommit.sh   — 300s loop: PROGRESS.md → commit → push → insurance copy
- scripts/build_scene.sh  — env-wrapped blender build
- scripts/render_final.sh — 2-lane chunked render (A:1-10055, B:10056-20110)
- scripts/finalize.sh     — gap repair + ffmpeg mux → download/AGI_explainer_final.mp4

## Known Bug Fixes (re-apply in any rewrite)
- world.color RGBA try/except RGB fallback (4.5 API)
- chip() takes plain 3-tuple loc (not Vector math)
- look_at via to_track_quat('-Z','Y') — matrix-safe
- text3d stores ob['text_body'] at creation (validation reads stored strings)
- 6s floor per sequence window (MIN_WIN_F=144)
- Camera bake: seeded RNG random.Random(f0*7+i), counts ∝ window length

## Status Log
- [v4] 2026-09-19: token OK, wav pushed to Z, code rebuild in progress
