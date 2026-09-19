#!/bin/bash
# setup_env.sh v4 — idempotent 5-stage environment rebuild (PROVEN recipe)
#   1) blender-4.5.3-linux-x64   2) mesa GL from Debian TRIXXIE (sid BREAKS EGL!)
#   3) pip faster-whisper        4) ffmpeg check   5) transcribe locked narration
set -u
ROOT=/home/z/my-project
AGI=$ROOT/agi_video
TMP=$AGI/agivideo_tmp
mkdir -p "$TMP" "$AGI/reports" "$AGI/audio"
cd "$TMP"

echo "== [1/5] blender =="
if [ ! -x "$TMP/blender/blender" ]; then
  if [ ! -f blender-4.5.3-linux-x64.tar.xz ]; then
    curl -sL -o blender-4.5.3-linux-x64.tar.xz \
      https://download.blender.org/release/Blender4.5/blender-4.5.3-linux-x64.tar.xz
  fi
  tar -xf blender-4.5.3-linux-x64.tar.xz
  rm -rf blender; mv blender-4.5.3-linux-x64 blender
  echo "blender OK"
else echo "blender cached"; fi

echo "== [2/5] mesa (TRIXIE!) =="
if [ ! -f "$TMP/gllibs/.done" ]; then
  mkdir -p gllibs/extract && cd gllibs/extract
  for suite in trixie sid; do
    echo "-- index $suite --"
    for m in main main-all; do
      curl -s "https://deb.debian.org/debian/dists/$suite/$m/binary-amd64/Packages.gz" | gzip -d > "P_$suite_$m.txt" 2>/dev/null || true
    done
    cat P_*.txt > all.txt || true
    # extract only the .deb urls we need
    rg -o 'https://[^ ]*\.deb' all.txt | rg -i 'mesa|libgl1|libegl|libgbm|libdrm|libx11|libxcb|libxext|libxfixes|libwayland|libxxf86|libxdamage|libsensors|libicu|libxml2|libzstd|liblzma|libllvm|libedit|libz3|libelf|libexpat|libglapi|libxshmfence|libva|libvdpau|libnuma|libudev|libpciaccess|libcrypt|libbsd|libmd|libunwind|libcurl|libbrotli|libnghttp|librtmp|libssh|libpsl|libldap|libb2|libkrb5|libkeyutils|libcom-err|libk5crypto|libgssapi|libtinfo|libmd4c|libdouble-conversion|libpcre2' | sort -u > debs.txt || true
    while read -r u; do
      f=$(basename "$u")
      [ -f "$f" ] || curl -sL -o "$f" "$u" || true
    done < debs.txt
    for d in *.deb; do
      [ -e "$d" ] && dpkg-deb -x "$d" ../ 2>/dev/null || true
    done
    [ -f ../usr/lib/x86_64-linux-gnu/libEGL.so.1 ] && echo "mesa from $suite OK" && break
  done
  touch ../.done
  cd "$TMP"
else echo "mesa cached"; fi

echo "== [3/5] faster-whisper =="
python3 -c "import faster_whisper" 2>/dev/null || pip install --quiet faster-whisper

echo "== [4/5] ffmpeg =="
command -v ffmpeg >/dev/null || (apt-get install -y ffmpeg 2>/dev/null || pip install --quiet imageio-ffmpeg)

echo "== [5/5] transcribe =="
if [ ! -f "$AGI/reports/transcript_timestamps.json" ]; then
  python3 "$AGI/scripts/transcribe.py" "$AGI/audio/narration_AGI_locked_837s.wav" \
          "$AGI/reports/transcript_timestamps.json"
else echo "transcript cached"; fi

echo "== ENV READY =="
ls -la "$TMP/blender/blender" "$AGI/reports/transcript_timestamps.json" 2>&1
