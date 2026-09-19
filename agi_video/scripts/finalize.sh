#!/bin/bash
# finalize.sh — gap repair (re-render missing frames) + ffmpeg mux -> download/AGI_explainer_final.mp4
set -u
ROOT=/home/z/my-project
AGI=$ROOT/agi_video
TMP=$AGI/agivideo_tmp
export LIBGL_ALWAYS_SOFTWARE=1
export __EGL_VENDOR_LIBRARY_FILENAMES="$TMP/gllibs/usr/share/glvnd/egl_vendor.d/50_mesa.json"
[ -f "$__EGL_VENDOR_LIBRARY_FILENAMES" ] || export __EGL_VENDOR_LIBRARY_FILENAMES="$TMP/gllibs/etc/glvnd/egl_vendor.d/50_mesa.json"
export LD_LIBRARY_PATH="$TMP/gllibs/usr/lib/x86_64-linux-gnu:${LD_LIBRARY_PATH:-}"

echo "== gap check =="
MISSING=$(for ((i=1;i<=20110;i++)); do [ -f "$AGI/frames/final/f$(printf %05d $i).jpg" ] || echo $i; done)
if [ -n "$MISSING" ]; then
  echo "missing: $(echo $MISSING | wc -w) frames — repairing"
  # repair in small contiguous runs of up to 64
  echo "$MISSING" | python3 -c "
import sys
runs, prev, start = [], None, None
for tok in sys.stdin.read().split():
    f = int(tok)
    if prev is None or f != prev + 1:
        if start is not None: runs.append((start, prev))
        start = f
    prev = f
if start is not None: runs.append((start, prev))
for a, b in runs:
    s = a
    while s <= b:
        e = min(b, s + 63)
        print(s, e)
        s = e + 1
" > /tmp/repair_runs.txt
  while read -r S E; do
    "$TMP/blender/blender" -b -noaudio "$AGI/final_scene.blend" \
      -o "//frames/final/f#####" -s $S -e $E -a 2>&1 | tail -1
  done < /tmp/repair_runs.txt
else
  echo "no gaps — 20110/20110 complete"
fi

echo "== mux =="
FF=$(command -v ffmpeg || python3 -c "import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())")
"$FF" -y -framerate 24 -i "$AGI/frames/final/f%05d.jpg" \
  -i "$AGI/audio/narration_AGI_locked_837s.wav" \
  -c:v libx264 -preset medium -crf 19 -pix_fmt yuv420p \
  -c:a aac -b:a 192k -shortest \
  "$ROOT/download/AGI_explainer_final.mp4" 2>&1 | tail -3
cp -f "$ROOT/download/AGI_explainer_final.mp4" "$AGI/AGI_explainer_final.mp4" 2>/dev/null || true
ls -la "$ROOT/download/AGI_explainer_final.mp4"
echo "FINALIZE DONE"
