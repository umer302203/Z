#!/usr/bin/env bash
# encode_chunks.sh — Resume-safe chunked final encode.
# Encodes video-only chunks with ass word-overlay burned, PTS-shifted per chunk
# so overlay events stay at ABSOLUTE times (setpts before ass filter).
# Usage: encode_chunks.sh <chunkA> <chunkB>   (encodes those chunk indices, waits)
# Each chunk = TOTAL/8 frames. Existing complete chunk files are skipped.
set -e
BASE="/home/z/my-project"
SEQ="$BASE/render/seq"
OUTD="$BASE/render/chunks"
ASS="$BASE/data/word_overlay.ass"
TOTAL=25135
FPS=30
NCH=8
PER=$(( (TOTAL + NCH - 1) / NCH ))
mkdir -p "$OUTD"

encode_chunk() {
  local ci=$1
  local f0=$(( ci * PER + 1 ))
  local n=$PER
  if [ $(( f0 + n - 1 )) -gt $TOTAL ]; then n=$(( TOTAL - f0 + 1 )); fi
  [ "$n" -le 0 ] && return 0
  local out="$OUTD/chunk_$ci.mp4"
  if [ -f "$out" ] && [ "$(stat -c%s "$out")" -gt 100000 ]; then
    echo "[chunk $ci] exists ($(stat -c%s "$out") bytes) — skip"
    return 0
  fi
  local t0=$(python3 -c "print(($f0-1)/$FPS)")
  echo "[chunk $ci] frames $f0..$((f0+n-1)) (n=$n) t0=${t0}s"
  ffmpeg -y -hide_banner -loglevel error -nostats \
    -framerate $FPS -start_number $f0 -i "$SEQ/f%06d.jpg" \
    -frames:v "$n" \
    -vf "setpts=(PTS-STARTPTS)+${t0}/TB,ass=${ASS}" \
    -an -c:v libx264 -preset veryfast -crf 20 -pix_fmt yuv420p \
    -threads 1 \
    "$out"
  echo "[chunk $ci] done: $(stat -c%s "$out") bytes"
}

for c in "$@"; do
  encode_chunk "$c" &
done
wait
echo "[encode] chunks $* complete"
