"""Find the actual temporal shift of chunk_7 vs seq via content-profile correlation."""
import os

import numpy as np
from PIL import Image

BASE = "/home/z/my-project"
SEQ = f"{BASE}/render/seq"

# content profile of ALL seq frames (cache by inode: hardlinked dupes = same value)
ino_cache = {}
prof = np.zeros(25136)
for fr in range(1, 25136):
    p = f"{SEQ}/f{fr:06d}.jpg"
    st = os.stat(p)
    if st.st_ino in ino_cache:
        prof[fr] = ino_cache[st.st_ino]
        continue
    a = np.asarray(Image.open(p).convert("L").resize((64, 36)), dtype=np.int16)
    vals, counts = np.unique(a, return_counts=True)
    bg = vals[counts.argmax()]
    v = float((np.abs(a - bg) > 12).mean())
    ino_cache[st.st_ino] = v
    prof[fr] = v
np.save(f"{BASE}/render/qc/seq_profile.npy", prof)
print("seq profile done. unique inodes:", len(ino_cache))

# extract every 50th frame from chunk_7_test (63 frames)
os.system(
    "ffmpeg -y -hide_banner -loglevel error -nostdin -i %s/render/chunks/chunk_7_test.mp4 "
    "-vf select='not(mod(n\\,50))' -vsync 0 %s/render/qc/c7p_%%03d.jpg" % (BASE, BASE)
)
cprof = []
files = sorted(os.listdir(f"{BASE}/render/qc"))
cfiles = [f for f in files if f.startswith("c7p_")]
print("extracted", len(cfiles), "probe frames")
for fn in cfiles:
    a = np.asarray(Image.open(f"{BASE}/render/qc/{fn}").convert("L").resize((64, 36)), dtype=np.int16)
    vals, counts = np.unique(a, return_counts=True)
    bg = vals[counts.argmax()]
    cprof.append(float((np.abs(a - bg) > 12).mean()))

cp = np.array(cprof)
# chunk pos i corresponds to expected seq frame 21995 + i*50
# try shifts: chunk pos p shows seq frame 21995 + p*50 + shift
best = None
for shift in range(-3000, 3001, 5):
    idx = 21995 + np.arange(len(cp)) * 50 + shift
    idx = np.clip(idx, 1, 25135)
    d = np.abs(cp - prof[idx]).mean()
    if best is None or d < best[0]:
        best = (d, shift)
print("BEST SHIFT:", best[1], "err:", round(best[0], 4))
