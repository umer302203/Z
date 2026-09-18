#!/usr/bin/env bash
# render_chunk.sh — run ONE foreground render chunk (max CHUNK_SECONDS).
# Resumes automatically: computes missing frames, renders, exits; caller re-invokes.
# When zero frames missing -> overlay + assemble + exit 2 (signal done).
CHUNK_SECONDS="${CHUNK_SECONDS:-540}"
BASE="/home/z/my-project"
BL="$BASE/software/blender-4.2.23-linux-x64/blender"
export LD_LIBRARY_PATH="$BASE/software/xvfb/egl/rootfs/usr/lib/x86_64-linux-gnu:${LD_LIBRARY_PATH:-}"
export LIBGL_ALWAYS_SOFTWARE=1
export GALLIUM_DRIVER=llvmpipe
export __EGL_VENDOR_LIBRARY_FILENAMES="$BASE/software/xvfb/egl/rootfs/usr/share/glvnd/egl_vendor.d/50_mesa.json"
unset DISPLAY
WORKERS="${WORKERS:-2}"

python3 "$BASE/scripts/compute_missing.py" "$WORKERS" > "$BASE/render/daemon_status.txt"
MISSING=$(grep -oP 'missing=\K[0-9]+' "$BASE/render/daemon_status.txt" | tail -1)
echo "[chunk] missing=$MISSING"
if [ "$MISSING" = "0" ] || [ -z "$MISSING" ]; then
  echo "[chunk] ALL FRAMES DONE -> overlay + assemble"
  python3 "$BASE/scripts/make_wordoverlay.py"
  python3 "$BASE/scripts/assemble.py" && exit 2
  exit 3
fi

PIDS=()
for i in $(seq 0 $((WORKERS-1))); do
  N=$(grep -c "" "$BASE/render/todo_w$i.txt" 2>/dev/null || echo 0)
  if [ "$N" -gt 0 ]; then
    mkdir -p "$BASE/render/worker$i"
    "$BL" -b "$BASE/render/agi_video.blend" --factory-startup \
      -P "$BASE/scripts/render_worker.py" -- \
      "$BASE/render/todo_w$i.txt" "w$i" "$BASE/render/worker$i" 0 1000000000 \
      >> "$BASE/render/worker$i.log" 2>&1 &
    PIDS+=($!)
    echo "[chunk] worker$i -> $N frames (pid $!)"
  fi
done

T0=$(date +%s)
while true; do
  NOW=$(date +%s)
  if [ $((NOW - T0)) -ge "$CHUNK_SECONDS" ]; then
    echo "[chunk] time budget over"
    break
  fi
  ALIVE=0
  for p in "${PIDS[@]}"; do kill -0 "$p" 2>/dev/null && ALIVE=1; done
  if [ "$ALIVE" = "0" ]; then
    echo "[chunk] workers exited"
    break
  fi
  sleep 10
done
for p in "${PIDS[@]}"; do kill "$p" 2>/dev/null || true; done
sleep 2
W0=$(ls "$BASE/render/worker0" 2>/dev/null | wc -l)
W1=$(ls "$BASE/render/worker1" 2>/dev/null | wc -l)
echo "[chunk] progress: w0=$W0 w1=$W1 total=$((W0+W1))"
exit 0
