#!/usr/bin/env bash
# render_daemon.sh — resilient render supervisor.
# Recomputes missing frames, launches workers, restarts them if killed,
# and when everything is rendered: overlay + assemble. Then exits.
BASE="/home/z/my-project"
BL="$BASE/software/blender-4.2.23-linux-x64/blender"
export LD_LIBRARY_PATH="$BASE/software/xvfb/egl/rootfs/usr/lib/x86_64-linux-gnu:${LD_LIBRARY_PATH:-}"
export LIBGL_ALWAYS_SOFTWARE=1
export GALLIUM_DRIVER=llvmpipe
export __EGL_VENDOR_LIBRARY_FILENAMES="$BASE/software/xvfb/egl/rootfs/usr/share/glvnd/egl_vendor.d/50_mesa.json"
unset DISPLAY

WORKERS="${WORKERS:-2}"
ROUND=0

while true; do
  ROUND=$((ROUND+1))
  python3 "$BASE/scripts/compute_missing.py" "$WORKERS" > "$BASE/render/daemon_status.txt"
  MISSING=$(grep -oP 'missing=\K[0-9]+' "$BASE/render/daemon_status.txt" | tail -1)
  echo "[daemon $(date +%H:%M:%S)] round=$ROUND missing=$MISSING"
  if [ "$MISSING" = "0" ] || [ -z "$MISSING" ]; then
    echo "[daemon] ALL FRAMES DONE -> overlay + assemble"
    python3 "$BASE/scripts/make_wordoverlay.py" >> "$BASE/render/daemon_status.txt" 2>&1
    python3 "$BASE/scripts/assemble.py" >> "$BASE/render/daemon_status.txt" 2>&1
    echo "[daemon] ASSEMBLE FINISHED"
    break
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
      echo "[daemon]   worker$i -> $N frames (pid $!)"
    fi
  done

  # wait for ANY worker to exit, then loop recomputes missing
  if [ ${#PIDS[@]} -gt 0 ]; then
    wait -n 2>/dev/null || wait "${PIDS[0]}" 2>/dev/null || true
    sleep 2
    # kill stragglers so next round starts clean
    for p in "${PIDS[@]}"; do kill "$p" 2>/dev/null || true; done
    sleep 3
  else
    echo "[daemon] no work lists but missing>0? retry in 30s"
    sleep 30
  fi
done
