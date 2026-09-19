#!/bin/bash
# build_scene.sh — env-wrapped headless Blender build + validation + text audit
set -u
ROOT=/home/z/my-project
AGI=$ROOT/agi_video
TMP=$AGI/agivideo_tmp
export LIBGL_ALWAYS_SOFTWARE=1
export __EGL_VENDOR_LIBRARY_FILENAMES="$TMP/gllibs/usr/share/glvnd/egl_vendor.d/50_mesa.json"
[ -f "$__EGL_VENDOR_LIBRARY_FILENAMES" ] || export __EGL_VENDOR_LIBRARY_FILENAMES="$TMP/gllibs/etc/glvnd/egl_vendor.d/50_mesa.json"
export LD_LIBRARY_PATH="$TMP/gllibs/usr/lib/x86_64-linux-gnu:${LD_LIBRARY_PATH:-}"
mkdir -p "$AGI/reports" "$AGI/frames/final"
"$TMP/blender/blender" -b -noaudio \
  -P "$AGI/scripts/scene_generator.py" 2>&1 | tail -40
echo "== TEXT AUDIT =="
"$TMP/blender/blender" -b -noaudio "$AGI/final_scene.blend" \
  -P "$AGI/scripts/verify_text.py" -- "$AGI/final_scene.blend" 2>&1 | rg "TEXT_AUDIT|BAD"
