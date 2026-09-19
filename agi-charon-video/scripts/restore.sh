#!/usr/bin/env bash
# restore.sh — Rebuild the FULL production environment from this git repo alone.
# Use after a server reset:  git clone <repo> && cd my-project && bash scripts/restore.sh
set -e
BASE="/home/z/my-project"
cd "$BASE"

echo "[restore] 1/4 Blender 4.2.23 ..."
if [ ! -x software/blender-4.2.23-linux-x64/blender ]; then
  mkdir -p software
  curl -L -o /tmp/blender.tar.xz \
    https://download.blender.org/release/Blender4.2/blender-4.2.23-linux-x64.tar.xz
  tar -xJf /tmp/blender.tar.xz -C software/
  rm /tmp/blender.tar.xz
fi
echo "[restore]    blender: $(software/blender-4.2.23-linux-x64/blender --version 2>/dev/null | head -1 || echo FAILED)"

echo "[restore] 2/4 user-space EGL + Xvfb (no root needed) ..."
mkdir -p software/xvfb/debs software/xvfb/egl/rootfs
if [ ! -d software/xvfb/egl/rootfs/usr/lib/x86_64-linux-gnu ]; then
  cd software/xvfb/debs
  apt-get download xvfb libegl1 libegl-mesa0 libglvnd0 libgl1 libglx0 libx11-6 \
    libxext6 libxdamage1 libxfixes3 libxshmfence1 libxxf86vm1 libdrm2 2>/dev/null || true
  for d in *.deb; do dpkg -x "$d" ../egl/rootfs/; done
  cd "$BASE"
fi

echo "[restore] 3/4 python deps (faster-whisper for re-transcription) ..."
pip install -q faster-whisper 2>/dev/null || echo "  (transcription already done: data/words.json is in git)"

echo "[restore] 4/4 rebuild Blender scene from scripts ..."
export LD_LIBRARY_PATH="$BASE/software/xvfb/egl/rootfs/usr/lib/x86_64-linux-gnu:${LD_LIBRARY_PATH:-}"
export LIBGL_ALWAYS_SOFTWARE=1
export GALLIUM_DRIVER=llvmpipe
unset DISPLAY
"$BASE/software/blender-4.2.23-linux-x64/blender" -b --factory-startup \
  -P "$BASE/scripts/build_video.py" 2>&1 | tail -3

echo "[restore] DONE. Next: bash scripts/run_render.sh"
