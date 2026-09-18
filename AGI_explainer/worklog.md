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

---
Task ID: 6
Agent: main (Super Z)
Task: v3 build-debug-QC cycle -> render launch + GitHub backup live

Work Log:
- Repo Z layout: ONLY AGI_explainer/ folder (user rule: shared repo, per-bot folders). Remote 'backup', credential.helper disabled locally, force-push done, autocommit pushes every 5 min.
- Transcript: 389 segments, 837.84s (LOCKED match). Anchors: MIN_ANCHOR_T=33.0 skips surgeon analogy (module words cluster there); s20 uses LAST 'question' (772.6s). Sequences REORDERED to narration topic order (s01, s02 Key Question 34.8s, s04 Transformer 40.8s, s12, s03 Bigger 58.8s, ... s07 Hallucination 408.9s, s18, s20). 18/18 anchored.
- Bugs found & fixed during preview QC (5 build iterations):
  1. all seqs coexist at origin -> vis_keys() hold-style hide_render/hide_viewport keys per window
  2. camera euler bezier flips -> rotation_mode QUATERNION + LINEAR interpolation (bezier overshoot dipped r 26->19)
  3. quaternion double-cover: consecutive keys dot<0 -> component-lerp passes near zero -> aim flips 180° -> hemisphere alignment (negate when dot<0) + shot() returns last q
  4. shared boundary frames overwritten by next shot -> jump-cut keying (shot owns [a0,b0], next starts b0+1)
  5. scale_in() read ob.scale AFTER setting 0.001 -> titles/links/nodes microscopic -> capture target BEFORE zeroing
  6. text mirrored -> rot (90°,0,180°) faces +Y camera side; camera front arc a in [-1.05,1.05]
- Final QC: AGI Architecture / Grounding (chain) / Hallucination / Open Question all render correctly, readable, composed. Validation ALL PASS (20110 frames, 168 obj, 80 shots, TEXT 37/37).

Stage Summary:
- RENDER LAUNCHED (2 lanes, daemonize): lane A 1-10055, lane B 10056-20110, ~8-9h -> finalize.sh (gap repair + ffmpeg mux) -> download/AGI_explainer_final.mp4.
- Backup live: repo Z /AGI_explainer/ — commits + pushes automatic.
