#!/usr/bin/env python3
"""Split long audio into chunks at silence points for reliable chunked ASR.

1. ffmpeg silencedetect -> silence list
2. choose cut points near evenly spaced targets (prefer within 1.2s)
3. ffmpeg -ss/-to per chunk -> data/chunks/chunk_XX.wav (16k mono)
Writes data/chunks/manifest.json
"""
import json
import os
import re
import subprocess

BASE = "/home/z/my-project"
AUDIO = f"{BASE}/upload/what_architecture_could_ai_need_for_agi_charon.wav"
OUT_DIR = f"{BASE}/data/chunks"
N_TARGET = 12
DURATION = 837.84


def detect_silences():
    cmd = [
        "ffmpeg", "-i", AUDIO, "-af",
        "silencedetect=noise=-32dB:d=0.35", "-f", "null", "-",
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    err = r.stderr
    starts = [float(m) for m in re.findall(r"silence_start: ([0-9.]+)", err)]
    ends = [float(m) for m in re.findall(r"silence_end: ([0-9.]+)", err)]
    return starts, ends


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    starts, ends = detect_silences()
    # midpoints of silences = ideal cut points
    cuts = []
    for i in range(min(len(starts), len(ends))):
        if ends[i] > starts[i]:
            cuts.append((starts[i] + ends[i]) / 2)
    if not cuts:
        cuts = [DURATION * i / (N_TARGET + 1) for i in range(1, N_TARGET + 1)]

    targets = [DURATION * (i + 1) / (N_TARGET + 1) for i in range(N_TARGET)]
    chosen = []
    last = 3.0
    for t in targets:
        best = min(cuts, key=lambda c: abs(c - t))
        if abs(best - t) > 1.5 or best <= last + 8 or best >= DURATION - 8:
            best = t
        if best > last + 8 and best < DURATION - 8:
            chosen.append(best)
            last = best

    bounds = [0.0] + chosen + [DURATION]
    manifest = []
    for i in range(len(bounds) - 1):
        a, b = bounds[i], bounds[i + 1]
        # small context overlap
        ss = max(0.0, a - 1.0)
        to = min(DURATION, b + 1.0)
        path = f"{OUT_DIR}/chunk_{i:02d}.wav"
        cmd = ["ffmpeg", "-y", "-i", AUDIO, "-ss", f"{ss:.3f}", "-to", f"{to:.3f}",
               "-ac", "1", "-ar", "16000", "-c:a", "pcm_s16le", path]
        subprocess.run(cmd, capture_output=True, text=True)
        manifest.append({
            "idx": i, "path": path, "global_offset": round(ss, 3),
            "core_start": round(a, 3), "core_end": round(b, 3),
            "file_start": round(ss, 3), "file_end": round(to, 3),
        })
    with open(f"{OUT_DIR}/manifest.json", "w") as f:
        json.dump(manifest, f, indent=1)
    print(f"[split] {len(manifest)} chunks; bounds={[round(b,1) for b in bounds]}")


if __name__ == "__main__":
    main()
