#!/bin/bash
# autocommit.sh — 300s loop: PROGRESS.md -> commit -> push -> insurance copy to download/
set -u
ROOT=/home/z/my-project
AGI=$ROOT/agi_video
FB=$AGI/frames/final
cd "$ROOT"
while true; do
  N=$(ls "$FB" 2>/dev/null | wc -l)
  P=$((N * 100 / 20110))
  {
    echo "# AGI Explainer render progress"
    echo "- frames: $N / 20110 ($P%)"
    echo "- updated: $(date -u '+%Y-%m-%d %H:%M:%SZ')"
  } > "$AGI/PROGRESS.md"
  git add "$AGI/PROGRESS.md" 2>/dev/null
  git commit -q -m "auto: $N/20110 frames ($P%)" 2>/dev/null
  flock /tmp/agipush.lock git push backup main 2>&1 | rg -v "^Hint|hint:" || true
  # insurance mirrors (download/ survives resets)
  mkdir -p "$ROOT/download/project_backup"
  cp -f "$AGI/worklog.md" "$AGI/PROGRESS.md" "$ROOT/download/project_backup/" 2>/dev/null
  cp -rf "$AGI/scripts" "$ROOT/download/project_backup/" 2>/dev/null
  cp -rf "$AGI/reports" "$ROOT/download/project_backup/" 2>/dev/null
  sleep 300
done
