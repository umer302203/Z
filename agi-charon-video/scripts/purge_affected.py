"""Purge rendered frames for shots whose 3D text was changed (re-render needed)."""
import json
import os

BASE = "/home/z/my-project"
AFFECTED = {"S05", "S08", "S11", "S12", "S14", "S17", "S19", "S21", "S22", "S23", "S24"}

plan = json.load(open(f"{BASE}/data/shot_plan.json"))
purge = []
for s in plan["shots"]:
    if s["id"] in AFFECTED:
        f0 = int(s["t0"] * 30) + 1
        f1 = int(s["t1"] * 30)
        purge.append((s["id"], f0, f1))

removed = 0
for wid in ("worker0", "worker1"):
    d = f"{BASE}/render/{wid}"
    if not os.path.isdir(d):
        continue
    for fn in os.listdir(d):
        if fn.startswith("f") and fn.endswith(".jpg"):
            try:
                fr = int(fn[1:7])
            except ValueError:
                continue
            for sid, f0, f1 in purge:
                if f0 <= fr <= f1:
                    os.remove(os.path.join(d, fn))
                    removed += 1
                    break

print("[purge] removed", removed, "stale frames from shots:", ", ".join(s[0] for s in purge))
