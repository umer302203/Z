"""Purge worker-dir frames affected by the camera hold fix.
Affected = [last_cam_key_frame .. shot_end] per shot (camera changed there).
"""
import bpy  # noqa
import os
import sys

sys.path.insert(0, "/home/z/my-project/scripts")

BASE = "/home/z/my-project"
FPS = 30

with open(f"{BASE}/data/shot_plan.json") as f:
    plan = json = __import__("json").load(f)
shots = sorted(plan["shots"], key=lambda s: s["t0"])
with open(f"{BASE}/render/needed.txt") as f:
    needed = set(int(x) for x in f.read().split() if x.strip())

# last cam key frame per shot, from the blend
cam = bpy.data.objects.get("main_cam")
act = cam.animation_data.action
all_keys = sorted(k.co[0] for fc in act.fcurves
                  if fc.data_path == "location" for k in fc.keyframe_points)

windows = []
for i, s in enumerate(shots):
    f_end = min(int(round(s["t1"] * FPS)), 25135)
    lastk = max((k for k in all_keys if k < f_end - 0.5), default=None)
    if lastk is None:
        continue
    windows.append((int(lastk), f_end, s["id"]))

total = 0
for a, b, sid in windows:
    n = len([fr for fr in needed if a <= fr <= b])
    total += n
    print("purge %s f%d-f%d: %d unique" % (sid, a, b, n))

purged = 0
for d in ("worker0", "worker1"):
    dp = f"{BASE}/render/{d}"
    if not os.path.isdir(dp):
        continue
    for fn in os.listdir(dp):
        if not (fn.startswith("f") and fn.endswith(".jpg")):
            continue
        try:
            fr = int(fn[1:7])
        except ValueError:
            continue
        if any(a <= fr <= b for a, b, _ in windows):
            os.remove(f"{dp}/{fn}")
            purged += 1
print("PURGED %d files (affected unique=%d)" % (purged, total))
