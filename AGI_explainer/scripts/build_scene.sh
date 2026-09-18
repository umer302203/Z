#!/bin/bash
# build_scene.sh — build final_scene.blend from specs + LOCKED narration (v3)
export LD_LIBRARY_PATH=/home/z/my-project/agivideo_tmp/gllibs/extract/usr/lib/x86_64-linux-gnu:$LD_LIBRARY_PATH
export LIBGL_ALWAYS_SOFTWARE=1
export __EGL_VENDOR_LIBRARY_FILENAMES=/home/z/my-project/agivideo_tmp/gllibs/extract/usr/share/glvnd/egl_vendor.d/50_mesa.json
cd /home/z/my-project/AGI_explainer
exec /home/z/my-project/agivideo_tmp/blender-4.5.3-linux-x64/blender -b -P scripts/scene_generator.py
