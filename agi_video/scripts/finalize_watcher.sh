#!/bin/bash
# finalize_watcher.sh — wait until all 20110 frames exist, then run finalize.sh once
set -u
FB=/home/z/my-project/agi_video/frames/final
while true; do
  N=$(ls "$FB" 2>/dev/null | wc -l)
  if [ "$N" -ge 20110 ]; then
    echo "$(date -u '+%H:%M:%S') all frames present — running finalize"
    bash /home/z/my-project/agi_video/scripts/finalize.sh
    break
  fi
  sleep 120
done
