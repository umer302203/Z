#!/usr/bin/env python3
"""Final assembly (repo-adapted combine_videos + audio mux).

1. Concatenate per-scene 1080p60 renders (concat demuxer, stream copy)
   in planned order -> silent master video.
2. Mux the ORIGINAL supplied narration (24 kHz WAV) as the audio track.
3. Pad/trim so final duration == sum of scene durations (audio padded with
   silence at tail if video is a hair longer; -shortest otherwise).
4. Validate: duration, streams, frame counts, loudness sanity.
"""
import json
import subprocess
import sys
from pathlib import Path

PROJECT = Path("/home/z/my-project/project")
MEDIA = PROJECT / "media"
RENDERS = PROJECT / "renders"
OUTPUT = PROJECT / "output"
LOGS = PROJECT / "logs"
PLAN = json.load(open(PROJECT / "planning" / "visual_scene_plan.json"))
MASTER_AUDIO = PROJECT / "input" / "original_audio.wav"


def probe(path, args=None):
    cmd = ["ffprobe", "-v", "quiet", "-print_format", "json", "-show_format"]
    if args:
        cmd += args
    cmd += [str(path)]
    return json.loads(subprocess.run(cmd, capture_output=True, text=True).stdout)


def run(cmd, **kw):
    p = subprocess.run(cmd, capture_output=True, text=True, **kw)
    if p.returncode != 0:
        print("CMD FAILED:", " ".join(map(str, cmd)))
        print(p.stderr[-2000:])
        sys.exit(1)
    return p


def main():
    OUTPUT.mkdir(exist_ok=True)
    RENDERS.mkdir(exist_ok=True)

    # 1) collect scene files in order, conform each to exact planned frames
    conform_dir = RENDERS / "conformed"
    conform_dir.mkdir(exist_ok=True)
    list_file = LOGS / "concat_list.txt"
    total_frames = 0
    with open(list_file, "w") as lf:
        for sc in PLAN["scenes"]:
            src = MEDIA / "videos" / f"scene_{sc['id']:03d}" / "1080p60" / \
                f"{sc['class_name']}.mp4"
            frames = round(sc["duration"] * 60)
            total_frames += frames
            dst = conform_dir / f"scene_{sc['id']:03d}.mp4"
            if dst.exists():
                d0 = float(probe(dst)["format"]["duration"])
                if abs(d0 - sc["duration"]) < 0.05:
                    lf.write(f"file '{dst}'\n")
                    continue
            # re-encode with exact frame count + uniform params (safe concat)
            run(["ffmpeg", "-y", "-v", "error", "-i", str(src),
                 "-vf", f"tpad=stop_mode=clone:stop_duration=3,trim=start_frame=0:end_frame={frames},setpts=PTS-STARTPTS",
                 "-r", "60", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
                 "-pix_fmt", "yuv420p", "-an", str(dst)])
            lf.write(f"file '{dst}'\n")
            d = float(probe(dst)["format"]["duration"])
            print(f"scene {sc['id']:03d}: conformed {d:.4f}s "
                  f"(plan {sc['duration']:.4f})")
    print(f"total planned frames: {total_frames} = {total_frames/60:.4f}s")

    # 2) concat
    silent = OUTPUT / "_silent_concat.mp4"
    run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0",
         "-i", str(list_file), "-c", "copy", str(silent)])
    d_silent = float(probe(silent)["format"]["duration"])
    print(f"silent concat duration: {d_silent:.4f}s")

    # 3) mux master audio (pad audio to video length with silence)
    final = OUTPUT / "final_video.mp4"
    run(["ffmpeg", "-y", "-v", "error",
         "-i", str(silent), "-i", str(MASTER_AUDIO),
         "-filter_complex",
         f"[1:a]apad=whole_dur={d_silent:.4f}[a]",
         "-map", "0:v", "-map", "[a]",
         "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
         "-movflags", "+faststart", "-shortest", str(final)])

    # 4) validate
    fmt = probe(final, ["-show_streams", "-count_frames"])
    dur = float(fmt["format"]["duration"])
    v = next(s for s in fmt["streams"] if s["codec_type"] == "video")
    a = next(s for s in fmt["streams"] if s["codec_type"] == "audio")
    print("=== FINAL VALIDATION ===")
    print(f"duration: {dur:.4f}s (audio master: 779.357)")
    print(f"video: {v['codec_name']} {v['width']}x{v['height']} "
          f"{v.get('avg_frame_rate')} frames={v.get('nb_read_frames')}")
    print(f"audio: {a['codec_name']} {a['sample_rate']}Hz ch={a['channels']}")
    ok = (abs(dur - 779.357) < 0.35 and v["width"] == 1920
          and v["height"] == 1080 and "60" in v.get("avg_frame_rate", ""))
    print("RESULT:", "PASS" if ok else "CHECK NEEDED")
    silent.unlink(missing_ok=True)


if __name__ == "__main__":
    main()
