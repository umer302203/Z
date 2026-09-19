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
  bash "$AGI/scripts/mesa_fetch.sh"
else echo "mesa cached"; fi

echo "== [3/5] faster-whisper =="
python3 -c "import faster_whisper" 2>/dev/null || python3 -m pip install --quiet faster-whisper

echo "== [4/5] ffmpeg =="
command -v ffmpeg >/dev/null || (apt-get install -y ffmpeg 2>/dev/null || pip install --quiet imageio-ffmpeg)

echo "== [5/5] transcribe =="
if [ ! -f "$AGI/reports/transcript_timestamps.json" ]; then
  python3 "$AGI/scripts/transcribe.py" "$AGI/audio/narration_AGI_locked_837s.wav" \
          "$AGI/reports/transcript_timestamps.json"
else echo "transcript cached"; fi

echo "== ENV READY =="
ls -la "$TMP/blender/blender" "$AGI/reports/transcript_timestamps.json" 2>&1
