#!/usr/bin/env python3
"""Dense smoke test: render every 0.25s across full timeline -> catches all scene bugs."""
import sys, time
sys.path.insert(0, "/home/z/my-project/scripts")
import numpy as np
import json
from render import dispatch
from engine import make_background

bg = make_background()
t0 = time.time()
n = 0
t = 0.0
while t < 779.36:
    f = bg.copy()
    try:
        dispatch(f, t)
    except Exception as e:
        print(f"ERROR at t={t:.2f}: {type(e).__name__}: {e}")
        raise
    n += 1
    t += 0.25
print(f"SMOKE OK: {n} frames tested in {time.time()-t0:.0f}s")
