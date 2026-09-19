#!/usr/bin/env python3
"""Finalize v2: old mux (seg1-3, seg7 intact) + new seg4/5/6 -> concat -> mux.
Old corrected.mp4 is keyframe-aligned at segment boundaries (120s each),
so stream-copy splits at 360 and 720 are exact."""
import subprocess, os, sys

VID = "/home/z/my-project/work/marl_video/renders"
OLD = "/home/z/my-project/work/marl_video/renders/corrected_prev.mp4"
OUT = "/home/z/my-project/download/MARL_explainer_final_corrected.mp4"
MIX = "/home/z/my-project/work/marl_video/audio/final_mix.wav"

segs = [f"{VID}/partA_0_360.mp4", f"{VID}/seg4_r5.mp4", f"{VID}/seg5_r5.mp4",
        f"{VID}/seg6_r5.mp4", f"{VID}/partB_720_end.mp4"]
for s in [f"{VID}/seg4_r5.mp4", f"{VID}/seg5_r5.mp4", f"{VID}/seg6_r5.mp4"]:
    if not os.path.exists(s):
        print("MISSING:", s); sys.exit(1)

def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print("FAIL:", " ".join(cmd[:6]), "\n", r.stderr[-600:]); sys.exit(1)

# 1) split old mux at keyframe boundaries (0-360, 720-end)
if not os.path.exists(f"{VID}/partA_0_360.mp4"):
    run(["ffmpeg","-y","-v","error","-i",OLD,"-t","360","-c","copy",f"{VID}/partA_0_360.mp4"])
if not os.path.exists(f"{VID}/partB_720_end.mp4"):
    run(["ffmpeg","-y","-v","error","-ss","720","-i",OLD,"-c","copy",f"{VID}/partB_720_end.mp4"])
print("split ok", flush=True)

# 2) concat all five parts
with open(f"{VID}/concat_v2.txt","w") as f:
    for s in segs: f.write(f"file '{s}'\n")
run(["ffmpeg","-y","-v","error","-f","concat","-safe","0","-i",f"{VID}/concat_v2.txt",
     "-c","copy",f"{VID}/video_silent_v2.mp4"])
print("concat ok", flush=True)

# 3) mux audio
run(["ffmpeg","-y","-v","error","-i",f"{VID}/video_silent_v2.mp4","-i",MIX,
     "-c:v","copy","-c:a","aac","-b:a","192k","-shortest",OUT])
print("mux ok", flush=True)

# 4) verify
r = subprocess.run(["ffprobe","-v","error","-show_entries",
    "format=duration,size:stream=codec_name,width,height,r_frame_rate",
    "-of","default=nw=1",OUT], capture_output=True, text=True)
print(r.stdout)
