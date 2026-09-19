#!/usr/bin/env python3
"""QC: extract frames at event times + verify sync + build contact sheets."""
import subprocess, os, json, sys
import numpy as np
from PIL import Image

VID = "/home/z/my-project/work/marl_video"
FINAL = "/home/z/my-project/download/MARL_explainer_final.mp4"
QC = f"{VID}/qc"
os.makedirs(f"{QC}/final_frames", exist_ok=True)

anchors = json.load(open(f"{VID}/anchors.json"))

# sample of word-synced event times to verify visually
check_times = [0.8, 7.3, 13.4, 18.0, 23.8, 40.3, 48.4, 50.9, 62.4, 87.9,
               94.7, 102.7, 110.8, 129.6, 158.5, 175.5, 206.5, 218.2, 245.8,
               288.1, 317.1, 343.4, 349.4, 386.0, 413.3, 440.1, 471.6, 487.5,
               508.7, 522.7, 529.9, 563.9, 583.0, 602.5, 624.1, 653.8, 675.1,
               692.5, 710.5, 728.0, 748.4, 766.1, 777.7]

def extract(t, name):
    out = f"{QC}/final_frames/{name}"
    r = subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", str(t), "-i", FINAL,
                        "-frames:v", "1", out], capture_output=True, text=True)
    return r.returncode == 0

ok = 0
for i, t in enumerate(check_times):
    if extract(t, f"qc_{i:02d}_t{t:07.2f}.png"):
        ok += 1
print(f"extracted {ok}/{len(check_times)} frames")

# contact sheets (8 per sheet)
files = sorted(f for f in os.listdir(f"{QC}/final_frames") if f.startswith("qc_"))
imgs = [Image.open(f"{QC}/final_frames/{f}").resize((480, 270)) for f in files]
per = 8
for s in range(0, len(imgs), per):
    batch = imgs[s:s+per]
    grid = Image.new("RGB", (480*2, 270*4), (0, 0, 0))
    for i, im in enumerate(batch):
        grid.paste(im, ((i % 2)*480, (i//2)*270))
    grid.save(f"{QC}/final_sheet_{s//per}.png")
print(f"{len(imgs)} frames in {(len(imgs)+per-1)//per} sheets")

# audio-video duration match
r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                    "-of", "default=noprint_wrappers=1:nokey=1", FINAL],
                   capture_output=True, text=True)
print("final duration:", r.stdout.strip())
