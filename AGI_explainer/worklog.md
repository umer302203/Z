# Worklog

---
Task ID: 5 (reset #3 recovery — full history: v1 lost reset #1 ~11:20, v2 lost reset #2 12:13, v2-rebuild lost reset #3 ~15:00)
Agent: main (Super Z)
Task: secure offsite backup FIRST, then v3 rebuild of AGI explainer pipeline

Survived reset #3:
- upload/ (root mount): what_architecture_could_ai_need_for_agi_charon.wav (40,216,398 B, 837.84s = LOCKED narration, matches v1 duration exactly) + why_ai_hallucinates_charon_corrected.wav (26,789,838 B, 558.12s, DIFFERENT topic — alt video, backed up too)
- conversation knowledge: full v1/v2 pipeline specs, proven env recipe, known bug fixes

Decisions:
- AGI wav drives this project's build (topic + duration match LOCKED input). Hallucinates wav = alt video offer to user.
- GITHUB-FIRST: repo umer302203/Z (user-created; token cannot create repos). Every source file pushed immediately after write. Env binaries stay in agivideo_tmp/ (gitignored, re-downloadable).

v3 rebuild plan:
1. secure wavs + scaffold -> push Z
2. env: blender 4.5.3 LTS + trixie mesa 25.0.7 (sid 26.2.3 BROKE EGL — proven versions only) + faster-whisper + ffmpeg
3. code: lib_scene, assets, seq_a..seq_e (20 sequences), scene_generator (wav duration probe + transcript phrase anchors + proportional fallback, 80-shot camera bake lens 44), build_scene.sh, render_final.sh, verify_text.py, daemonize.py (double-fork PPID=1), autocommit.sh (5-min commit + flock push), finalize.sh (gap repair + ffmpeg mux)
4. transcribe AGI wav -> transcript_timestamps.json -> build -> TEXT RULE verify (<=3 English words on screen) -> render 2 lanes 20110 frames 720p24 Workbench -> mux -> download/AGI_explainer_final.mp4
Known bug fixes to re-apply: world.color RGB tuple, chip 6-tuple loc, matrix_world.translation (not world_location), C_GROUND imports, no horizon wall, camera widened 26/19/13.5/24 units, anim thresholds 400.
