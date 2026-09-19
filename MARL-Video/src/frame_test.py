#!/usr/bin/env python3
"""Render single frames with the rebuilt pipeline for style-fidelity comparison.
Usage: python3 frame_test.py <t> [<t> ...]"""
import sys, json
import numpy as np
sys.path.insert(0, "/home/z/my-project/scripts")
from engine import Renderer, W, H, FPS, make_background
from PIL import Image
import scenes_a, scenes_b

ANCH = json.load(open("/home/z/my-project/work/marl_video/anchors.json"))
DRAW = scenes_a.DRAW_A + scenes_b.DRAW_B

def render_frame(t):
    for (t0, t1, fn) in DRAW:
        if t0 <= t < t1:
            frame = make_background()
            fn(frame, t, ANCH)
            return frame
    return make_background()

for t in [float(x) for x in sys.argv[1:]]:
    fr = render_frame(t)
    img = Image.fromarray(np.clip(fr, 0, 255).astype(np.uint8))
    out = f"/home/z/my-project/work/marl_video/qc/kitmatch_t{t}.png"
    img.save(out)
    print("saved", out)
