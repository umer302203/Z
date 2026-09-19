"""Find offset: which seq frame does chunk_7 frame 0 actually contain?
Compares downscaled luminance hashes."""
import os

import numpy as np
from PIL import Image

BASE = "/home/z/my-project"
SEQ = f"{BASE}/render/seq"

def sig(path):
    im = Image.open(path).convert("L").resize((32, 18))
    return np.asarray(im, dtype=np.float32)

# extract candidate frames from chunk_7 at local indices 0, 500, 3055
os.system(
    "ffmpeg -y -hide_banner -loglevel error -nostdin "
    "-i %s/render/chunks/chunk_7.mp4 -vf select='eq(n\\,0)+eq(n\\,500)+eq(n\\,3055)' "
    "-vsync 0 %s/render/qc/ch7_probe_%%d.jpg" % (BASE, BASE)
)

for tag, local in [("1", 0), ("2", 500), ("3", 3055)]:
    p = f"{BASE}/render/qc/ch7_probe_{tag}.jpg"
    if not os.path.exists(p):
        print("missing", p)
        continue
    s = sig(p)
    best = (1e9, -1)
    # search seq frames around expected positions
    expected = 21995 + local
    for fr in range(max(1, expected - 400), min(25135, expected + 400), 1):
        sp = f"{SEQ}/f{fr:06d}.jpg"
        if not os.path.exists(sp):
            continue
        d = float(np.abs(sig(sp) - s).mean())
        if d < best[0]:
            best = (d, fr)
        if d < 0.5:
            break
    print(f"chunk7[{local}] expected_seq={expected} MATCHES seq_f{best[1]} (dist={best[0]:.2f})")
