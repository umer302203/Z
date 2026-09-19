#!/bin/bash
# render_final.sh — 2-lane parallel render, 20110 frames, Workbench JPEG (v3)
export LD_LIBRARY_PATH=/home/z/my-project/agivideo_tmp/gllibs/extract/usr/lib/x86_64-linux-gnu:$LD_LIBRARY_PATH
export LIBGL_ALWAYS_SOFTWARE=1
export __EGL_VENDOR_LIBRARY_FILENAMES=/home/z/my-project/agivideo_tmp/gllibs/extract/usr/share/glvnd/egl_vendor.d/50_mesa.json
cd /home/z/my-project/AGI_explainer
mkdir -p renders/final
B=/home/z/my-project/agivideo_tmp/blender-4.5.3-linux-x64/blender
"$B" -b final_scene.blend -s 1     -e 10055 -o //renders/final/agi_f_#### -F JPEG -a &
"$B" -b final_scene.blend -s 10056 -e 20110 -o //renders/final/agi_f_#### -F JPEG -a &
wait
echo "RENDER LANES COMPLETE $(date)"
