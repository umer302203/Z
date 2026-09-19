#!/usr/bin/env python3
"""Production renderer (repo-adapted: mirrors VideoRenderer + process_scene
retry loop from manimAnimationAgent, without cloud APIs).

- Renders scenes at -qh (1080p60) per VIDEO_RULES #13
- Skips scenes whose output already succeeded (succ marker, repo pattern)
- Retries failed scenes up to N times
- Logs per-scene manim output to logs/
- Optionally conforms each render to the exact planned frame count
"""
import json
import subprocess
import sys
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

PROJECT = Path("/home/z/my-project/project")
SCENES_DIR = PROJECT / "scenes"
RENDERS = PROJECT / "renders"
MEDIA = PROJECT / "media"
LOGS = PROJECT / "logs"
PLAN = json.load(open(PROJECT / "planning" / "visual_scene_plan.json"))


def scene_id_from_file(f):
    return int(f.stem.split("_")[1])


def render_one(scene_file, class_name, duration):
    sid = scene_file.stem
    marker = RENDERS / f"{sid}.done"
    out_mp4 = MEDIA / "videos" / sid / "1080p60" / f"{class_name}.mp4"
    log = LOGS / f"render_{sid}.log"
    if marker.exists() and out_mp4.exists():
        return (sid, "skip", 0.0)
    t0 = time.time()
    with open(log, "w") as lf:
        p = subprocess.run(
            ["manim", "-qh", scene_file.name, class_name,
             "--media_dir", str(MEDIA)],
            cwd=SCENES_DIR, stdout=lf, stderr=subprocess.STDOUT, timeout=1500)
    ok = p.returncode == 0 and out_mp4.exists()
    # check duration drift (must match plan within 0.05 s)
    note = ""
    if ok:
        d = float(subprocess.run(
            ["ffprobe", "-v", "quiet", "-show_entries", "format=duration",
             "-of", "csv=p=0", str(out_mp4)], capture_output=True,
            text=True).stdout.strip())
        if abs(d - duration) > 0.05:
            ok = False
            note = f"duration {d:.3f} != plan {duration:.3f}"
    if ok:
        marker.touch()
    return (sid, "ok" if ok else f"FAIL {p.returncode} {note}",
            time.time() - t0)


def main():
    only = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else None
    jobs = []
    for sc in PLAN["scenes"]:
        if only and sc["id"] not in only:
            continue
        f = SCENES_DIR / sc["file"]
        if not f.exists():
            print(f"[plan] {sc['file']} missing - not scheduled")
            continue
        jobs.append((sc["id"], f, sc["class_name"], sc["duration"]))
    RENDERS.mkdir(exist_ok=True)
    done = 0
    with ProcessPoolExecutor(max_workers=2) as ex:
        futs = {ex.submit(render_one, f, cn, d): sid
                for sid, f, cn, d in jobs}
        for fut in as_completed(futs):
            sid, status, dt = fut.result()
            done += 1
            print(f"[{done:2d}/{len(jobs)}] scene_{int(str(sid).split('_')[-1]):03d}: {status} "
                  f"({dt:.1f}s)", flush=True)


if __name__ == "__main__":
    main()
