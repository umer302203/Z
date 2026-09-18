#!/usr/bin/env bash
# finalize_video.sh — concat chunks -> mux audio -> verify -> final mp4 in download/
set -e
BASE="/home/z/my-project"
CD="$BASE/render/chunks"
OUT="$BASE/download/agi_architecture_720p_synced.mp4"
WAV="$BASE/upload/what_architecture_could_ai_need_for_agi_charon.wav"

# 1) concat list
: > "$CD/list.txt"
for i in 0 1 2 3 4 5 6 7; do echo "file 'chunk_$i.mp4'" >> "$CD/list.txt"; done

# 2) concat (stream copy) — skip if already done
if [ ! -f "$CD/video_full.mp4" ] || [ "$(stat -c%s "$CD/video_full.mp4")" -lt 5000000 ]; then
  ffmpeg -y -hide_banner -loglevel error -nostdin -f concat -safe 0 -i "$CD/list.txt" \
    -c copy "$CD/video_full.mp4"
fi
ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 "$CD/video_full.mp4"

# 3) mux audio + faststart
ffmpeg -y -hide_banner -loglevel error -nostdin -i "$CD/video_full.mp4" -i "$WAV" \
  -c:v copy -c:a aac -b:a 160k -ar 48000 -movflags +faststart -shortest "$OUT"

echo "---VERIFY---"
ffprobe -v error -show_entries format=duration,size -of default=nw=1 "$OUT"
ffprobe -v error -select_streams v:0 -show_entries stream=width,height,r_frame_rate,nb_frames -of default=nw=1 "$OUT"
ffprobe -v error -select_streams a:0 -show_entries stream=codec_name,sample_rate,channels -of default=nw=1 "$OUT"
ffprobe -v error -show_entries format=duration -of default=nw=1 "$OUT"
