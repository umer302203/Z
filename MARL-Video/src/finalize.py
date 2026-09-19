#!/usr/bin/env python3
"""Finalize: concat segment MP4s + mux mixed audio -> final MP4 (1920x1080@60)."""
import subprocess, os, sys

VID = "/home/z/my-project/work/marl_video/renders"
OUT = "/home/z/my-project/download"
os.makedirs(OUT, exist_ok=True)

segs = ["seg1.mp4", "seg2.mp4", "seg3.mp4", "seg4.mp4", "seg5.mp4", "seg6.mp4", "seg7.mp4"]
missing = [s for s in segs if not os.path.exists(f"{VID}/{s}")]
if missing:
    print("MISSING:", missing); sys.exit(1)

# concat list
with open(f"{VID}/concat.txt", "w") as f:
    for s in segs:
        f.write(f"file '{VID}/{s}'\n")

# concat (all same codec/params -> stream copy)
r = subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0",
                    "-i", f"{VID}/concat.txt", "-c", "copy", f"{VID}/video_silent.mp4"],
                   capture_output=True, text=True)
if r.returncode != 0:
    print("CONCAT FAIL:", r.stderr[-500:]); sys.exit(1)
print("concat ok")

# mux audio
r = subprocess.run(["ffmpeg", "-y", "-v", "error",
                    "-i", f"{VID}/video_silent.mp4",
                    "-i", "/home/z/my-project/work/marl_video/audio/final_mix.wav",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                    "-shortest", f"{OUT}/MARL_explainer_final.mp4"],
                   capture_output=True, text=True)
if r.returncode != 0:
    print("MUX FAIL:", r.stderr[-500:]); sys.exit(1)
print("mux ok")

# verify
r = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                    "format=duration,size:stream=codec_name,width,height,r_frame_rate",
                    "-of", "default=noprint_wrappers=1", f"{OUT}/MARL_explainer_final.mp4"],
                   capture_output=True, text=True)
print(r.stdout)
