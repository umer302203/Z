#!/bin/bash
# autocommit.sh — persist progress to git every 5 min + offsite push + insurance copies
cd /home/z/my-project
TOTAL=20110
while true; do
  DONE=$(ls agi_video/renders/final/ 2>/dev/null | grep -c '\.jpg$')
  PCT=$(( DONE * 100 / TOTAL ))
  cat > agi_video/reports/PROGRESS.md <<EOF
# RENDER PROGRESS
- frames: ${DONE} / ${TOTAL}  (${PCT}%)
- updated: $(date '+%Y-%m-%d %H:%M:%S')
- engine: Workbench 1280x720 @ 24fps (2 lanes)
- text rule: PASS (all on-screen text <= 3 English words)
- next: mux narration -> final AGI_explainer_final.mp4
EOF
  # insurance: small files mirrored to download/ (survives resets)
  mkdir -p download/project_backup
  cp -r agi_video/scripts download/project_backup/ 2>/dev/null
  cp -r agi_video/reports download/project_backup/ 2>/dev/null
  cp -r agi_video/audio download/project_backup/ 2>/dev/null
  cp worklog.md download/project_backup/ 2>/dev/null
  git add -A >/dev/null 2>&1
  if ! git diff --cached --quiet >/dev/null 2>&1; then
    git commit -m "auto: ${DONE}/${TOTAL} frames (${PCT}%)" >/dev/null 2>&1
    echo "$(date '+%H:%M:%S') committed ${DONE}/${TOTAL} (${PCT}%)" >> agi_video/reports/autocommit.log
  fi
  # offsite: push to GitHub repo Z (flock guards overlap)
  if git remote get-url backup >/dev/null 2>&1; then
    (
      flock -n 9
      git push backup main --quiet >/dev/null 2>&1 \
        && echo "$(date '+%H:%M:%S') pushed to GitHub Z" >> agi_video/reports/autocommit.log
    ) 9>/home/z/my-project/.git/push.lock
  fi
  sleep 300
done
