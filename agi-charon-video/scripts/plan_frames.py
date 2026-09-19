"""Smart frame planner.

Reads data/shot_plan.json (shots with motion windows) and produces:
  - data/frame_plan.json : which frames get rendered + their timeline slots
  - render/needed.txt    : one frame number per line (for workers)

Strategy:
  - Inside motion windows: render every MOTION_STEP-th frame (default 2 -> 15fps unique)
  - Outside motion windows (holds): render exactly one frame per hold region
  - Boundaries between shots are cuts; hold boundary frames are always included
"""
import json
import math
import os
import sys

BASE = "/home/z/my-project"
FPS = 30
MOTION_STEP = int(os.environ.get("MOTION_STEP", "2"))


def main():
    with open(f"{BASE}/data/shot_plan.json", encoding="utf-8") as f:
        plan = json.load(f)

    fps = plan.get("fps", FPS)
    total = plan["total_frames"]
    needed = []  # sorted unique frame numbers

    for shot in plan["shots"]:
        f0 = max(1, int(math.ceil(shot["t0"] * fps)))
        f1 = min(total, int(math.floor(shot["t1"] * fps)))
        windows = shot.get("motion", [])
        # normalize windows into frame ranges, clip to shot range
        franges = []
        for w in windows:
            w0 = max(f0, int(math.ceil(w[0] * fps)))
            w1 = min(f1, int(math.floor(w[1] * fps)))
            if w1 >= w0:
                franges.append((w0, w1))
        franges.sort()
        # merge overlaps
        merged = []
        for r in franges:
            if merged and r[0] <= merged[-1][1] + 1:
                merged[-1] = (merged[-1][0], max(merged[-1][1], r[1]))
            else:
                merged.append(r)

        # hold regions = gaps between merged windows
        cursor = f0
        for (w0, w1) in merged:
            if w0 > cursor:
                needed.append(cursor)          # single frame for whole hold
            for fr in range(w0, w1 + 1, MOTION_STEP):
                needed.append(fr)
            # ensure last motion frame exists for clean cut
            if (w1 - w0) % MOTION_STEP != 0:
                needed.append(w1)
            cursor = w1 + 1
        if cursor <= f1:
            needed.append(cursor)

    needed = sorted(set(needed))
    os.makedirs(f"{BASE}/render", exist_ok=True)
    with open(f"{BASE}/render/needed.txt", "w") as f:
        f.write("\n".join(str(x) for x in needed) + "\n")

    with open(f"{BASE}/data/frame_plan.json", "w") as f:
        json.dump({
            "fps": fps,
            "total_frames": total,
            "needed_count": len(needed),
            "needed": needed,
        }, f)

    est_h = len(needed) * 1.64 / 3600  # 720p estimate
    print(f"[plan] total={total} needed={len(needed)} ({100*len(needed)/total:.1f}%) est_render_hours={est_h:.2f}")


if __name__ == "__main__":
    main()
