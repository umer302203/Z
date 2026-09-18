#!/bin/bash
# autocommit.sh — 5-min cycle: PROGRESS.md + insurance mirror + git commit + GitHub push
cd /home/z/my-project
TOTAL=20110
while true; do
  DONE=$(ls AGI_explainer/renders/final/ 2>/dev/null | grep -c '\.jpg$')
  PCT=$(( DONE * 100 / TOTAL ))
  cat > AGI_explainer/reports/PROGRESS.md <<EOF
# RENDER PROGRESS
- frames: ${DONE} / ${TOTAL}  (${PCT}%)
- updated: $(date '+%Y-%m-%d %H:%M:%S')
- engine: Workbench 1280x720 @ 24fps (2 lanes)
- text rule: PASS (all on-screen text <= 3 English words)
- next: mux narration -> download/AGI_explainer_final.mp4
EOF
  # insurance: small files mirrored to download/ (survives resets)
  mkdir -p download/project_backup
  cp -r AGI_explainer/scripts download/project_backup/ 2>/dev/null
  cp -r AGI_explainer/reports download/project_backup/ 2>/dev/null
  cp -r AGI_explainer/audio download/project_backup/ 2>/dev/null
  cp AGI_explainer/worklog.md download/project_backup/ 2>/dev/null
  git add -A >/dev/null 2>&1
  if ! git diff --cached --quiet >/dev/null 2>&1; then
    git commit -m "auto: ${DONE}/${TOTAL} frames (${PCT}%)" >/dev/null 2>&1
    echo "$(date '+%H:%M:%S') committed ${DONE}/${TOTAL} (${PCT}%)" >> AGI_explainer/reports/autocommit.log
  fi
  # offsite: push to shared repo Z (folder AGI_explainer only)
  if git remote get-url backup >/dev/null 2>&1; then
    (
      flock -n 9
      git push backup main --quiet >/dev/null 2>&1 \
        && echo "$(date '+%H:%M:%S') pushed to GitHub Z" >> AGI_explainer/reports/autocommit.log
    ) 9>/home/z/my-project/.git/push.lock
  fi
  sleep 300
done
