#!/bin/bash
# setup_env.sh v3 — full environment rebuild after server reset #3 (2026-09-18)
# Blender 4.5.3 LTS + trixie mesa (PROVEN — sid 26.2.3 broke EGL) + faster-whisper + ffmpeg + transcribe
set -e
LOG=/home/z/my-project/setup_env.log
mkdir -p /home/z/my-project/agivideo_tmp
exec > >(tee -a $LOG) 2>&1

echo "=== [1/5] Blender 4.5.3 LTS ==="
cd /home/z/my-project/agivideo_tmp
if [ ! -x blender-4.5.3-linux-x64/blender ]; then
  curl -sL -o blender.tar.xz https://download.blender.org/release/Blender4.5/blender-4.5.3-linux-x64.tar.xz
  tar xf blender.tar.xz && rm blender.tar.xz
fi
blender-4.5.3-linux-x64/blender --version | head -1

echo "=== [2/5] mesa GL libs (headless Workbench EGL) ==="
mkdir -p gllibs && cd gllibs
if [ ! -d extract/usr/lib/x86_64-linux-gnu ]; then
  URL=http://deb.debian.org/debian
  idx=$(mktemp)
  curl -s "$URL/dists/trixie/main/binary-amd64/Packages.gz" | zcat > $idx || true
  curl -s "$URL/dists/sid/main/binary-amd64/Packages.gz" | zcat >> $idx || true
  for pkg in libgl1 libglx0 libegl1 libegl-mesa0 libgbm1 libdrm2 libglapi-mesa \
             libx11-6 libxext6 libxfixes3 libxdamage1 libxcomposite1 libxrandr2 \
             libxi6 libxxf86vm1 libxcb1 libxkbcommon0 libxshmfence1 libexpat1 \
             libx11-xcb1 libxau6 libxdmcp6 libwayland-client0 libwayland-cursor0 \
             libwayland-egl1 libwayland-server0 libxinerama1 libxcursor1 \
             mesa-libgallium; do
    fn=$(grep -A20 "^Package: $pkg\$" $idx | grep "^Filename:" | head -1 | cut -d' ' -f2)
    [ -n "$fn" ] && curl -s -o "$(basename $fn)" "$URL/$fn" && echo "got $pkg" || echo "MISS $pkg"
  done
  mkdir -p extract
  for d in *.deb; do dpkg-deb -x "$d" extract/ 2>/dev/null || true; done
  rm -f *.deb $idx
fi
ls extract/usr/lib/x86_64-linux-gnu/ | wc -l
echo "MESA OK"

echo "=== [3/5] faster-whisper ==="
pip install --quiet faster-whisper 2>&1 | tail -1 || true
python3 -c "import faster_whisper; print('faster-whisper OK')"

echo "=== [4/5] ffmpeg ==="
which ffmpeg && ffmpeg -version | head -1

echo "=== [5/5] transcribe LOCKED AGI narration ==="
python3 /home/z/my-project/agi_video/scripts/transcribe.py \
  /home/z/my-project/agi_video/audio/narration_AGI_locked_837s.wav \
  /home/z/my-project/agi_video/reports/transcript_timestamps.json
echo "SETUP COMPLETE"
