#!/bin/bash
# finalize.sh — gap repair + frame count + mux narration -> final MP4 (v3)
set -e
cd /home/z/my-project/AGI_explainer
TOTAL=20110
mkdir -p reports
python3 - "$TOTAL" <<'PY'
import os, sys
total = int(sys.argv[1])
have = sorted(int(f[6:-4]) for f in os.listdir('renders/final')
              if f.startswith('agi_f_') and f.endswith('.jpg'))
have_set = set(have)
missing = [str(i) for i in range(1, total + 1) if i not in have_set]
print(f'frames on disk: {len(have)}/{total}; missing: {len(missing)}')
open('reports/missing_frames.txt', 'w').write(','.join(missing))
PY

if [ -s reports/missing_frames.txt ]; then
  export LD_LIBRARY_PATH=/home/z/my-project/agivideo_tmp/gllibs/extract/usr/lib/x86_64-linux-gnu:$LD_LIBRARY_PATH
  export LIBGL_ALWAYS_SOFTWARE=1
  export __EGL_VENDOR_LIBRARY_FILENAMES=/home/z/my-project/agivideo_tmp/gllibs/extract/usr/share/glvnd/egl_vendor.d/50_mesa.json
  B=/home/z/my-project/agivideo_tmp/blender-4.5.3-linux-x64/blender
  FRAMES=$(cat reports/missing_frames.txt)
  echo "gap repair: rendering $FRAMES"
  "$B" -b final_scene.blend -o //renders/final/agi_f_#### -F JPEG -f "$FRAMES"
fi

mkdir -p /home/z/my-project/download
ffmpeg -y -framerate 24 -start_number 1 -i renders/final/agi_f_%04d.jpg \
  -i audio/narration_AGI_locked_837s.wav \
  -c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p \
  -c:a aac -b:a 192k -shortest \
  /home/z/my-project/download/AGI_explainer_final.mp4
echo "FINAL MP4 DONE: /home/z/my-project/download/AGI_explainer_final.mp4"
