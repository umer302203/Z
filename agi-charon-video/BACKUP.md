# Backup & Restore Guide (server-reset protection)

## Kya protected hai (git repo me)
- `scripts/` — poora pipeline (build, render, overlay, assemble, restore)
- `data/words.json` — 2271 words + timestamps (100% sync ki foundation)
- `data/shot_plan.json`, `data/frame_plan.json` — scene timing
- `upload/what_architecture_could_ai_need_for_agi_charon.wav` — SOURCE AUDIO (39MB)
- `worklog.md` — multi-agent work history
- `scripts/restore.sh` — ek command me environment rebuild

## Kya git me NAHI hai (regenerable)
- `software/` (Blender 1.3GB) → `restore.sh` dobara download karta hai
- `render/` frames + .blend → scripts se rebuild hote hain
- Final MP4 → assemble.py se banta hai

## Server reset ke baad restore (3 steps)
```bash
git clone <YOUR_REPO_URL> my-project && cd my-project
bash scripts/restore.sh          # Blender + EGL + scene rebuild (~10 min)
bash scripts/run_render.sh       # render + overlay + mux
```

## GitHub push (recommended — abhi kar lo)
Local git server-reset se nahi bachta (same disk). Remote push karo:

1. GitHub par new repo banao (private): `agi-video-pipeline`
2. Phir:
```bash
cd /home/z/my-project
git remote add origin https://github.com/<YOUR_USER>/agi-video-pipeline.git
git push -u origin main
```
3. Har milestone ke baad: `git push`

## Offline bundle
`download/agi_project_backup.zip` — poora git repo (bundle format) —
restore: `git clone agi_project_backup.bundle my-project`
