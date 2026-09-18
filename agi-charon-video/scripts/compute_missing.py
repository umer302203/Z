"""Compute remaining frames: needed.txt minus already-rendered files.
Writes render/todo_<wid>.txt lists split across N workers.
Usage: python3 scripts/compute_missing.py [nworkers]
"""
import os
import sys

BASE = "/home/z/my-project"
R = f"{BASE}/render"

with open(f"{R}/needed.txt") as f:
    needed = [int(x) for x in f.read().split() if x.strip()]

done = set()
for d in os.listdir(R):
    if d.startswith("worker") and os.path.isdir(f"{R}/{d}"):
        for fn in os.listdir(f"{R}/{d}"):
            if fn.startswith("f") and fn.endswith(".jpg"):
                try:
                    done.add(int(fn[1:7]))
                except ValueError:
                    pass

missing = [fr for fr in needed if fr not in done]
n = max(1, int(sys.argv[1]) if len(sys.argv) > 1 else 2)

# split round-robin for load balance
lists = [[] for _ in range(n)]
for i, fr in enumerate(missing):
    lists[i % n].append(fr)

for i, lst in enumerate(lists):
    with open(f"{R}/todo_w{i}.txt", "w") as f:
        f.write("\n".join(map(str, lst)) + "\n")
    print(f"[missing] worker{i}: {len(lst)} frames")

print(f"[missing] total needed={len(needed)} done={len(done & set(needed))} missing={len(missing)}")
