#!/usr/bin/env python3
"""Scan all seq frames for 'empty' shots (flat background, no content).
Flags contiguous ranges with tiny pixel variance. Outputs render/empty_ranges.txt
"""
import json
import os

import numpy as np
from PIL import Image

BASE = "/home/z/my-project"
SEQ = f"{BASE}/render/seq"
plan = json.load(open(f"{BASE}/data/frame_plan.json"))
needed = plan["needed"]

def content_score(path):
    im = Image.open(path).convert("L").resize((80, 45))
    a = np.asarray(im, dtype=np.int16)
    # dominant value = background
    vals, counts = np.unique(a, return_counts=True)
    bg = vals[counts.argmax()]
    diff = np.abs(a - bg) > 12
    return float(diff.mean())

# scan every needed frame (unique rendered frames only)
empty = []  # (frame, score)
for fr in needed:
    p = f"{SEQ}/f{fr:06d}.jpg"
    if not os.path.exists(p):
        continue
    s = content_score(p)
    if s < 0.004:  # <0.4% pixels differ from bg
        empty.append(fr)

# group contiguous (in timeline, allow small gaps)
groups = []
for fr in empty:
    if groups and fr - groups[-1][1] <= 45:  # gap tolerance 1.5s
        groups[-1][1] = fr
    else:
        groups.append([fr, fr])

with open(f"{BASE}/render/empty_ranges.txt", "w") as f:
    for a, b in groups:
        dur = (b - a) / 30.0
        line = f"EMPTY f{a:06d}-f{b:06d}  {a/30:.1f}s-{b/30:.1f}s  ({dur:.1f}s)"
        print(line)
        f.write(line + "\n")
print(f"[scan] {len(empty)} empty frames in {len(groups)} ranges "
      f"(of {len(needed)} unique)")
