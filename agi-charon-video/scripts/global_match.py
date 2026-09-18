"""Global match: find seq frames identical to chunk_7 probe frames."""
import os

import numpy as np
from PIL import Image

BASE = "/home/z/my-project"
SEQ = f"{BASE}/render/seq"

def sig(path):
    return np.asarray(Image.open(path).convert("L").resize((32, 18)), dtype=np.float32)

sigs = {}
for fr in range(1, 25136):
    p = f"{SEQ}/f{fr:06d}.jpg"
    sigs[fr] = sig(p)

for tag, local, expected in [("1", 0, 21995), ("2", 500, 22495), ("3", 3055, 25050)]:
    p = f"{BASE}/render/qc/ch7_probe_{tag}.jpg"
    s = sig(p)
    dists = [(float(np.abs(sigs[fr] - s).mean()), fr) for fr in range(1, 25136)]
    dists.sort()
    print(f"chunk7[{local}] expected={expected} top5:", [(f, round(d, 2)) for d, f in dists[:5]])
