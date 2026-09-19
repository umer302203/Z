#!/bin/bash
# Atomic segment replacement with verification BEFORE any mv.
# Usage: bash replace_segs.sh <pair> [<pair> ...]   e.g. seg1_r4 seg7_r3
set -e
R=/home/z/my-project/work/marl_video/renders
FPS=60

verify() {  # verify <file> <min_frames>
  local f=$1 min=$2
  local n=$(ffprobe -v error -select_streams v:0 -count_frames \
            -show_entries stream=nb_read_frames -of csv=p=0 "$R/$f" 2>/dev/null)
  if [ -z "$n" ] || [ "$n" -lt "$min" ]; then
    echo "FAIL $f: frames=$n (need >=$min)"; exit 1
  fi
  echo "OK   $f: $n frames"
}

echo "== VERIFY PHASE (nothing moved yet) =="
for pair in "$@"; do
  case $pair in
    seg7*) min=3560 ;;   # 720-779.357
    *)     min=7195 ;;   # 120s segments
  esac
  verify "${pair}.mp4" "$min"
done

echo "== REPLACE PHASE =="
for pair in "$@"; do
  base="${pair%_*}"                     # seg1_r4 -> seg1
  mv "$R/${pair}.mp4" "$R/${base}.mp4"
  echo "moved ${pair}.mp4 -> ${base}.mp4"
done

echo "== FINAL CHECK =="
ls -la "$R"/seg?.mp4
