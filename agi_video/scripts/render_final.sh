#!/bin/bash
# render_final.sh — 2-lane chunked render. Args: <lane A|B>
# Lane A: frames 1-10055, Lane B: 10056-20110. Chunks of 500, skip existing.
set -u
ROOT=/home/z/my-project
AGI=$ROOT/agi_video
TMP=$AGI/agivideo_tmp
LANE=${1:-A}
export LIBGL_ALWAYS_SOFTWARE=1
export __EGL_VENDOR_LIBRARY_FILENAMES="$TMP/gllibs/usr/share/glvnd/egl_vendor.d/50_mesa.json"
[ -f "$__EGL_VENDOR_LIBRARY_FILENAMES" ] || export __EGL_VENDOR_LIBRARY_FILENAMES="$TMP/gllibs/etc/glvnd/egl_vendor.d/50_mesa.json"
export LD_LIBRARY_PATH="$TMP/gllibs/usr/lib/x86_64-linux-gnu:${LD_LIBRARY_PATH:-}"

if [ "$LANE" = "A" ]; then F0=1;    F1=10055; else F0=10056; F1=20110; fi
CH=500
F=$F0
while [ $F -le $F1 ]; do
  E=$((F + CH - 1)); [ $E -gt $F1 ] && E=$F1
  # chunk skip: if all frames present, advance
  HAVE=$(for ((i=F;i<=E;i++)); do [ -f "$AGI/frames/final/f$(printf %05d $i).jpg" ] && echo x; done | wc -l)
  WANT=$((E - F + 1))
  if [ "$HAVE" -lt "$WANT" ]; then
    "$TMP/blender/blender" -b -noaudio "$AGI/final_scene.blend" \
      -o "//frames/final/f#####" -s $F -e $E -a 2>&1 | tail -2
  else
    echo "chunk $F-$E complete, skip"
  fi
  F=$((E + 1))
done
echo "LANE $LANE DONE"
