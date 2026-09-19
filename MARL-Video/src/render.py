#!/usr/bin/env python3
"""Master renderer: 1920x1080 @ 60fps, scenes dispatched by absolute time."""
import sys, time, subprocess
import numpy as np
sys.path.insert(0, "/home/z/my-project/scripts")
import json
from engine import Renderer, W, H, FPS, make_background
import scenes_a, scenes_b

OUT = "/home/z/my-project/work/marl_video/renders"
ANCH = json.load(open("/home/z/my-project/work/marl_video/anchors.json"))

DRAW = scenes_a.DRAW_A + scenes_b.DRAW_B
TOTAL = 779.357
N_FRAMES = int(TOTAL * FPS)

def dispatch(frame, t):
    for (t0, t1, fn) in DRAW:
        if t0 <= t < t1:
            fn(frame, t, ANCH)
            return
    # fallback: background only

def main(start_s, end_s, out_name):
    n0 = int(start_s * FPS)
    n1 = min(int(end_s * FPS), N_FRAMES)
    total = n1 - n0
    r = Renderer(f"{OUT}/{out_name}", total)
    bg = r.bg
    buf = np.empty_like(bg)
    t_start = time.time()
    for n in range(n0, n1):
        t = n / FPS
        np.copyto(buf, bg)
        dispatch(buf, t)
        r.write(buf)
    r.close()
    dur = time.time() - t_start
    print(f"DONE {out_name}: {total} frames in {dur:.0f}s ({total/dur:.1f} fps)", flush=True)

if __name__ == "__main__":
    a, b, name = float(sys.argv[1]), float(sys.argv[2]), sys.argv[3]
    main(a, b, name)
