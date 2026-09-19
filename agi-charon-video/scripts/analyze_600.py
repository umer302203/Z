"""Analyze t_600.mp4: find first position where encode is flat but seq has content."""
import subprocess

import numpy as np
from PIL import Image


def cf(p):
    a = np.asarray(Image.open(p).convert("L"), dtype=np.int16)
    vals, counts = np.unique(a, return_counts=True)
    bg = vals[counts.argmax()]
    return round(float((np.abs(a - bg) > 12).mean()), 3)


prof = np.load("/home/z/my-project/render/qc/seq_profile.npy")
for pos in [0, 50, 100, 150, 200, 250, 300, 400, 500, 550, 599]:
    subprocess.run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-nostdin",
        "-i", "/home/z/my-project/render/qc/t_600.mp4",
        "-vf", "select=eq(n\\,%d)" % pos, "-vsync", "0", "-frames:v", "1",
        "/home/z/my-project/render/qc/p6_%d.jpg" % pos,
    ], check=True, cwd="/home/z/my-project")
    fr = 21995 + pos
    e = cf("/home/z/my-project/render/qc/p6_%d.jpg" % pos)
    s = float(prof[fr])
    flag = "OK " if abs(e - s) < 0.03 else "DIFF"
    print("pos %3d (seq f%d): encode=%.3f seq=%.3f  %s" % (pos, fr, e, s, flag))
