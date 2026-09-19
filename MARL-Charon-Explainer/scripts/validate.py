#!/usr/bin/env python3
"""Phase 13 validation suite (VIDEO_RULES final passes, automated).

1. Export integrity: full decode test, no errors.
2. Frame sampling across the entire timeline -> detect blank/black stretches.
3. Scene boundary checks: transition frames should be dark (clean lifecycle).
4. Event-time frames: extract frames at planned visual events for review.
5. Audio checks: RMS across thirds of the video, tail silence check.
6. Duration & stream conformance.
"""
import json
import subprocess
from pathlib import Path

import numpy as np

PROJECT = Path("/home/z/my-project/project")
FINAL = PROJECT / "output" / "final_video.mp4"
FRAMES = PROJECT / "logs" / "qc_frames"
FRAMES.mkdir(parents=True, exist_ok=True)
PLAN = json.load(open(PROJECT / "planning" / "visual_scene_plan.json"))


def sh(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


print("== 1) Full decode test ==")
p = sh(["ffmpeg", "-v", "error", "-i", str(FINAL), "-f", "null", "-"])
print("decode errors:", "NONE" if not p.stderr.strip() else p.stderr[:500])

print("== 2) Frame sampling (every 4s -> mean luminance) ==")
# decode luminance at fps=1/4, check for long dark stretches
p = sh(["ffmpeg", "-i", str(FINAL), "-vf", "fps=1/4,scale=64:36",
        "-f", "rawvideo", "-pix_fmt", "gray", "-"])
data = np.frombuffer(p.stdout, dtype=np.uint8)
n = len(data) // (64 * 36)
lums = data[:n * 64 * 36].reshape(n, 64 * 36).mean(axis=1)
dark = lums < 6
# report dark runs longer than 2 samples (8s) excluding final fade
runs = []
start = None
for i, d in enumerate(dark):
    if d and start is None:
        start = i
    elif not d and start is not None:
        runs.append((start * 4, i * 4))
        start = None
if start is not None:
    runs.append((start * 4, n * 4))
print(f"samples: {n}, mean lum overall: {lums.mean():.1f}")
print(f"dark runs (>8s): {[(a, b) for a, b in runs if b - a > 8]}")
print(f"final fade region dark: {dark[-6:].tolist() if n >= 6 else 'n/a'}")

print("== 3) Scene boundary darkness (clean transitions) ==")
bad_bounds = []
for sc in PLAN["scenes"][:-1]:
    t = sc["end"] - 0.08  # last frame before cut
    p = sh(["ffmpeg", "-ss", f"{t:.3f}", "-i", str(FINAL), "-frames:v", "1",
            "-f", "rawvideo", "-pix_fmt", "gray", "-s", "64x36", "-"])
    if p.stdout:
        lum = np.frombuffer(p.stdout, dtype=np.uint8).mean()
        if lum > 40:
            bad_bounds.append((sc["id"], round(lum, 1)))
print("boundaries not dark:", bad_bounds if bad_bounds else "ALL CLEAN")

print("== 4) Event frames extraction ==")
count = 0
for sc in PLAN["scenes"]:
    for ev in sc["events"][:2]:
        t = min(ev["t_abs"] + 0.5, sc["end"] - 0.15)
        out = FRAMES / f"s{sc['id']:03d}_t{ev['t_abs']:07.2f}.png"
        sh(["ffmpeg", "-y", "-v", "error", "-ss", f"{t:.3f}", "-i", str(FINAL),
            "-frames:v", "1", str(out)])
        count += 1
print(f"extracted {count} event frames -> {FRAMES}")

print("== 5) Audio checks ==")
p = sh(["ffmpeg", "-i", str(FINAL), "-map", "0:a", "-f", "s16le",
        "-ac", "1", "-ar", "8000", "-"])
audio = np.frombuffer(p.stdout, dtype=np.int16).astype(np.float32) / 32768
seg = len(audio) // 3
for i in range(3):
    rms = float(np.sqrt((audio[i * seg:(i + 1) * seg] ** 2).mean()))
    print(f"third {i+1} RMS: {rms:.4f}")
tail_rms = float(np.sqrt((audio[-8000:] ** 2).mean()))
print(f"tail 1s RMS: {tail_rms:.4f} (small = natural end, not cut)")

print("== 6) Conformance ==")
fmt = json.loads(sh(["ffprobe", "-v", "quiet", "-print_format", "json",
                     "-show_format", "-show_streams", str(FINAL)]).stdout)
v = next(s for s in fmt["streams"] if s["codec_type"] == "video")
a = next(s for s in fmt["streams"] if s["codec_type"] == "audio")
checks = {
    "duration_within_0.35s_of_audio": abs(float(fmt["format"]["duration"]) - 779.357) < 0.35,
    "resolution_1920x1080": v["width"] == 1920 and v["height"] == 1080,
    "fps_60": v["avg_frame_rate"] == "60/1",
    "codec_h264_aac": v["codec_name"] == "h264" and a["codec_name"] == "aac",
    "has_audio_stream": True,
}
for k, val in checks.items():
    print(f"{k}: {'PASS' if val else 'FAIL'}")
print("ALL CHECKS DONE")
