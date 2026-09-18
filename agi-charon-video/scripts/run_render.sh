#!/usr/bin/env bash
# run_render.sh — Full render orchestration:
#   frame plan -> parallel workers -> single-word English overlay -> ffmpeg mux
set -e
BASE="/home/z/my-project"
BL="$BASE/software/blender-4.2.23-linux-x64/blender"
export LD_LIBRARY_PATH="$BASE/software/xvfb/egl/rootfs/usr/lib/x86_64-linux-gnu:${LD_LIBRARY_PATH:-}"
export LIBGL_ALWAYS_SOFTWARE=1
export GALLIUM_DRIVER=llvmpipe
export __EGL_VENDOR_LIBRARY_FILENAMES="$BASE/software/xvfb/egl/rootfs/usr/share/glvnd/egl_vendor.d/50_mesa.json"
unset DISPLAY

WORKERS="${WORKERS:-2}"

echo "[run] 1/5 frame plan ..."
python3 "$BASE/scripts/plan_frames.py"

NEEDED=$(wc -l < "$BASE/render/needed.txt")
echo "[run]    frames to render: $NEEDED"

echo "[run] 2/5 rendering with $WORKERS workers ..."
CHUNK=$(( (NEEDED + WORKERS - 1) / WORKERS ))
PIDS=()
for i in $(seq 0 $((WORKERS-1))); do
  S=$(( i * CHUNK ))
  E=$(( S + CHUNK ))
  rm -rf "$BASE/render/worker$i"
  "$BL" -b "$BASE/render/agi_video.blend" -P "$BASE/scripts/render_worker.py" -- \
    "$BASE/render/needed.txt" "w$i" "$BASE/render/worker$i" "$S" "$E" \
    > "$BASE/render/worker$i.log" 2>&1 &
  PIDS+=($!)
  echo "[run]    worker$i frames[$S:$E) pid=$!"
done
FAIL=0
for p in "${PIDS[@]}"; do wait "$p" || FAIL=1; done
if [ "$FAIL" = "1" ]; then echo "[run] WORKER FAILED - check render/worker*.log"; exit 1; fi

echo "[run] 3/5 single-word English overlay ..."
python3 "$BASE/scripts/make_wordoverlay.py"

echo "[run] 4/5 assemble ..."
python3 "$BASE/scripts/assemble.py"

echo "[run] 5/5 done -> $BASE/download/agi_architecture_720p_synced.mp4"
