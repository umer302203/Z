# AGI Video Production — Multi-Agent Worklog

---
Task ID: 1
Agent: main (Super Z)
Task: Environment setup + ASR + scene pipeline for 14-min Blender explainer video (word-level 100% sync)

Work Log:
- Audio probed: 837.84s, mono 24kHz 16-bit PCM (upload/what_architecture_could_ai_need_for_agi_charon.wav)
- No GPU, 2 CPU cores, 4.1GB RAM, 9.3GB disk — heavy constraints
- Blender NOT in apt (no root). Downloaded blender-4.2.23-linux-x64 tarball → software/ (extracted, zero missing libs)
- Xvfb not installable (no root) → apt-get download xvfb + dpkg -x user-space → runs on :99
- libEGL missing → apt-get download libegl1/libegl-mesa0/libglvnd0 + dpkg -x → user-space EGL works
- GL render verified: Workbench studio+shadows+cavity renders correctly (EGL headless, LIBGL_ALWAYS_SOFTWARE=1)
- Env recipe: LD_LIBRARY_PATH=software/xvfb/egl/rootfs/usr/lib/x86_64-linux-gnu, LIBGL_ALWAYS_SOFTWARE=1, GALLIUM_DRIVER=llvmpipe, __EGL_VENDOR_LIBRARY_FILENAMES=egl/rootfs/usr/share/glvnd/egl_vendor.d/50_mesa.json, unset DISPLAY
- Benchmark: 1080p=3.72s/f, 720p=1.64s/f → PLAN: 720p@30fps container, smart frame selection (motion=15fps unique, holds=1 frame), ffmpeg concat-demuxer exact time-slot assembly
- faster-whisper (py3.13, int8, small model) transcription with word_timestamps started in background → data/words.json
- User requirements: 720p accepted (env constraint), word-highlight karaoke captions, full SKILL-style geometry, git protection against server reset

Stage Summary:
- Blender headless rendering pipeline OPERATIONAL on constrained box
- Next: transcription results → line-by-line visual direction → modular Blender build scripts → smart-frame renderer → ASS captions → mux

---
Task ID: 2
Agent: main (Super Z)
Task: Continue pipeline + git protection + NEW requirement: screen text = single English words ONLY (no subtitles, no lines, no Devanagari)

Work Log:
- Git protection layer: audio tracked in git (un-ignored upload/*.wav), scripts/restore.sh (full env rebuild from git alone), scripts/run_render.sh orchestrator, BACKUP.md (GitHub push guide), download/agi_project_backup.bundle
- Transcription verified complete: data/words.json = 2271 words, language=hi, 837.84s, word-level timestamps + probability
- NEW on-screen text policy implemented: ONLY single English words at a time (user: "koi subtitles nhi... bas words likhna ha")
- LLM (glm-4) batch translation: 1155 unique Devanagari words → data/gloss_map.json (278 displayable initially)
- Context-verified manual overrides (~450 entries): garbled ASR loanwords fixed (अटेन्चन→attention, नूलज→knowledge, गोल→goal, पेशन→patient, जूट→lie, दिसाइट→decide...), Hinglish identity mapping (model/goal/AGI/robot/learning spoken in English → display as-is), function words blanked (Hindi + English stoplists)
- Final: data/gloss_final.json = 594 displayable words; scripts/make_gloss_fix.py (5-layer policy)
- scripts/make_wordoverlay.py: single-word ASS events (word start → next displayed word start, HOLD_MAX 2.5s during silences, uppercase, DejaVu Sans Bold 46, letter-spaced, bottom-center, NO box, Devanagari safety filter) → data/word_overlay.ass = 713 events
- assemble.py switched captions.ass → word_overlay.ass
- Scene rebuilt: BUILD_OK 24 shots, 1374 objects, 25135 frames
- CRITICAL BUG FOUND+FIXED: all frames rendered gray because main_cam had hide_render keyed f1..f23225 (sweep_stray_objects filed camera into STAGE_S23 by final X position, then kf_vis hid it outside S23). Fix: cameras excluded from sweep + hide fcurves removed + forced visible (build_video.py). Verified: f100 surgeon+desk+books renders correctly.
- Render launched: 6728 unique frames (26.8%), 2 workers, ~2h estimate

Stage Summary:
- Word-level sync chain COMPLETE: audio → whisper word timestamps → gloss map → single-word overlay at exact word times
- Camera-hide bug fixed; scene visually verified against SKILL spec (surgeon/scrubs/coat/stethoscope/desk/books)
- Rendering in progress → next: auto-assemble → final mp4 with burned word overlay

---
Task ID: 3
Agent: main (Super Z)
Task: GitHub backup to umer302203/Z (dedicated folder agi-charon-video/) + finish render + assemble final video

Work Log:
- User provided GitHub repo umer302203/Z + fine-grained PAT for backup (files ONLY under project folder, other AI folders untouched)
- Created scripts/push_backup.sh: fetch origin/main -> read-tree full project under agi-charon-video/ -> commit -> push (preserves remote content; token only in .git/config, never committed)
- Token 1 PUSH FAILED 403; Token 2 PUSH FAILED 403 — API probe: "Resource not accessible by personal access token" = fine-grained PAT lacks Contents:Read+Write (or repo not selected in token's Repository access). User must fix token settings. Push deferred, NOT blocking pipeline
- Render resumed via foreground chunks: 163 missing frames completed (6728/6728 unique = 25135 timeline frames @720p30)
- make_wordoverlay.py regenerated: 713 single-word English events (word-timestamp anchored)
- assemble.py launched detached: 25135/25135 frames hardlinked; ffmpeg x264 veryfast crf20 + ass burn + aac mux -> download/agi_architecture_720p_synced.mp4

Stage Summary:
- ALL frames rendered post English-only text fix
- Final mux in progress; backup push pending token fix (exact GitHub settings steps to be given to user)

---
Task ID: 4
Agent: main (Super Z)
Task: Fix empty-shot camera drift bug + cfr encode bug + overlay Hindi leaks -> FINAL VIDEO

Work Log:
- ROOT CAUSE 1 (empty shots, 2314 frames / 41 ranges): camera fcurve drifted BETWEEN shots — each shot's last cam key interpolated (bezier) toward the NEXT shot's first key (up to 1000 units across stages) leaving content frame during hold segments (S13: 21s empty, S21: 35s)
- FIX: CAM_HOLD_FIX post-pass in build_video.py — sets each shot's LAST camera key interpolation=CONSTANT (hold pose till shot end, hard-cut to next shot). Bug in v1: shared boundaries (t1==next t0) grabbed next shot's key; fixed with strict < f_hold-0.5. 144 keys set, verified 7/7 hold poses correct
- ROOT CAUSE 2 (chunk encodes flat): -fps_mode cfr + huge setpts PTS offset (up to 835s) corrupted CFR frame mapping -> chunks 4-7 all-flat. FIX: dropped cfr/-r flags (input already exact 30fps from image2); micro-tests isolated it
- ROOT CAUSE 3 (overlay leaks): romanized-Hindi words (ANDAZA/INSAAN/KAAM/POORANI/ISI/PO) bypassed Devanagari filter (ASCII). FIX: BLOCKLIST+REMAP in make_wordoverlay.py -> 707 events clean
- Purged 2576 affected frames, re-rendered all (6728/6728), relinked 25135/25135
- Re-encoded 8 chunks (no cfr) -> concat -> aac mux -> download/agi_architecture_720p_synced.mp4 (837.63s, 25135 frames, 1280x720@30, 29MB)
- QC: 6 formerly-empty frames now show full scenes (loop diagram, model comparison, cognitive system); overlay words English-only; scene 3D text English-only

Stage Summary:
- FINAL DELIVERABLE READY: download/agi_architecture_720p_synced.mp4
- Word-level sync chain: whisper word timestamps -> single-word English overlay burned at exact word times
- Pending: GitHub push blocked by token Contents:write permission (user to fix in token settings)
