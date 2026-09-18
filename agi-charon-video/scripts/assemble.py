"""Assemble final video:
1. Build render/seq/%06d.jpg via hardlinks from worker outputs per frame_plan
2. ffmpeg: sequence + audio + single-word English overlay burn -> download/final mp4
"""
import json
import os
import subprocess
import sys

BASE = "/home/z/my-project"
OUT_W = 1280
OUT_H = 720
FPS = 30

seq_dir = f"{BASE}/render/seq"
frames_dirs = [d for d in os.listdir(f"{BASE}/render") if d.startswith("worker")]
print("[assemble] worker dirs:", frames_dirs)


def find_frame(fr):
    for d in frames_dirs:
        p = os.path.join(f"{BASE}/render", d, "f%06d.jpg" % fr)
        if os.path.exists(p):
            return p
    return None


def main():
    with open(f"{BASE}/data/frame_plan.json") as f:
        plan = json.load(f)
    needed = plan["needed"]
    total = plan["total_frames"]

    os.makedirs(seq_dir, exist_ok=True)
    # clear old links
    for x in os.listdir(seq_dir):
        os.remove(os.path.join(seq_dir, x))

    missing = []
    idx = 0  # pointer into needed
    links = 0
    last_src = None
    for fr in range(1, total + 1):
        while idx < len(needed) and needed[idx] < fr:
            idx += 1
        if idx < len(needed) and needed[idx] == fr:
            src = find_frame(fr)
            if src is None:
                missing.append(fr)
                src = last_src
            else:
                last_src = src
            dst = os.path.join(seq_dir, "f%06d.jpg" % fr)
            if src:
                os.link(src, dst)
                links += 1
        else:
            # hold frame: hardlink the most recent rendered frame
            dst = os.path.join(seq_dir, "f%06d.jpg" % fr)
            if last_src:
                os.link(last_src, dst)
                links += 1

    if missing:
        print("[assemble] WARNING missing rendered frames:", missing[:20], "count=", len(missing))

    print(f"[assemble] linked {links}/{total} frames")

    audio = f"{BASE}/upload/what_architecture_could_ai_need_for_agi_charon.wav"
    out = f"{BASE}/download/agi_architecture_720p_synced.mp4"
    cmd = [
        "ffmpeg", "-y",
        "-framerate", str(FPS), "-i", f"{seq_dir}/f%06d.jpg",
        "-i", audio,
        "-vf", f"ass={BASE}/data/word_overlay.ass",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
        "-pix_fmt", "yuv420p", "-fps_mode", "cfr",
        "-c:a", "aac", "-b:a", "160k", "-ar", "48000",
        "-movflags", "+faststart",
        "-shortest",
        out,
    ]
    if os.environ.get("LINK_ONLY"):
        print("[assemble] LINK_ONLY: skip ffmpeg (chunked encoder handles encode)")
        return
    print("[assemble] running ffmpeg ...")
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stderr[-3000:])
        sys.exit(1)
    print("[assemble] DONE ->", out)


if __name__ == "__main__":
    main()
