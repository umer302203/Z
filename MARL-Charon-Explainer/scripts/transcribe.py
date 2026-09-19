#!/usr/bin/env python3
"""Local transcription with faster-whisper (no cloud APIs) - RESUMABLE.
Processes audio in chunks, checkpoints after each chunk, and merges into
transcript/transcript_timestamps.json with sentence segments + word timestamps.
"""
import json
import subprocess
import sys
import time
from pathlib import Path

from faster_whisper import WhisperModel

PROJECT = Path("/home/z/my-project/project")
AUDIO_16K = PROJECT / "input" / "working_audio_16k.wav"
ORIGINAL = "multi_agent_reinforcement_learning_charon_final.wav"
OUT = PROJECT / "transcript" / "transcript_timestamps.json"
PARTIAL = PROJECT / "transcript" / "transcript_partial.json"
TMP = PROJECT / "transcript" / "_chunk.wav"
LOG = PROJECT / "logs" / "transcribe.log"

MODEL_SIZE = "small"
CHUNK_LEN = 200.0  # seconds per chunk


def log(msg):
    line = f"[{time.time()%100000:9.1f}] {msg}"
    print(line, flush=True)
    with open(LOG, "a") as f:
        f.write(line + "\n")


def probe_duration(path):
    out = subprocess.run(
        ["ffprobe", "-v", "quiet", "-print_format", "json", "-show_format", str(path)],
        capture_output=True, text=True).stdout
    return float(json.loads(out)["format"]["duration"])


def load_partial():
    if PARTIAL.exists():
        with open(PARTIAL) as f:
            return json.load(f)
    return {"segments": []}


def save_partial(data):
    PARTIAL.parent.mkdir(parents=True, exist_ok=True)
    with open(PARTIAL, "w") as f:
        json.dump(data, f, ensure_ascii=False)


def main():
    total_dur = probe_duration(AUDIO_16K)
    data = load_partial()
    start_from = 0.0
    if data["segments"]:
        start_from = data["segments"][-1]["end"]
    log(f"Total duration {total_dur:.2f}s, resuming from {start_from:.2f}s")

    model = WhisperModel(MODEL_SIZE, device="cpu", compute_type="int8")
    log("Model loaded")

    chunk_idx = 0
    while start_from < total_dur - 0.05:
        chunk_end = min(start_from + CHUNK_LEN, total_dur)
        # extract chunk
        subprocess.run(
            ["ffmpeg", "-y", "-v", "error", "-ss", f"{start_from:.3f}",
             "-to", f"{chunk_end:.3f}", "-i", str(AUDIO_16K),
             "-c:a", "pcm_s16le", str(TMP)],
            check=True)
        segments_iter, info = model.transcribe(
            str(TMP), language="en", beam_size=5, word_timestamps=True,
            vad_filter=True, vad_parameters={"min_silence_duration_ms": 400},
            condition_on_previous_text=False)
        n_before = len(data["segments"])
        for seg in segments_iter:
            words = [{"word": w.word.strip(),
                      "start": round(float(w.start) + start_from, 3),
                      "end": round(float(w.end) + start_from, 3)}
                     for w in (seg.words or [])]
            if not seg.text.strip():
                continue
            data["segments"].append({
                "id": n_before + len(data["segments"]) - n_before,
                "start": round(float(seg.start) + start_from, 3),
                "end": round(float(seg.end) + start_from, 3),
                "text": seg.text.strip(),
                "words": words,
            })
        data["segments"][-len(data["segments"]) + n_before:] = data["segments"][n_before:]
        for i, s in enumerate(data["segments"]):
            s["id"] = i
        save_partial(data)
        log(f"chunk {chunk_idx}: [{start_from:.2f} -> {chunk_end:.2f}] "
            f"+{len(data['segments'])-n_before} segs (total {len(data['segments'])})")
        start_from = chunk_end
        chunk_idx += 1

    # Finalize
    for i, s in enumerate(data["segments"]):
        s["id"] = i
    result = {
        "source_audio": {
            "original_filename": ORIGINAL,
            "source_location": "https://drive.google.com/drive/folders/11c_Ij3zX1Vz14luQtL719eaGmDv9GSin",
            "original_format": "wav (pcm_s16le, 24000 Hz, mono)",
            "duration": round(total_dur, 2),
            "preserved_copy": "input/original_audio.wav",
            "processing_copy": "input/working_audio_16k.wav",
        },
        "model": {"name": "faster-whisper", "size": MODEL_SIZE, "compute": "int8",
                  "device": "cpu", "local": True},
        "language": "en",
        "segments": data["segments"],
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT, "w") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    n_words = sum(len(s["words"]) for s in data["segments"])
    log(f"DONE: {len(data['segments'])} segments, {n_words} words -> {OUT}")


if __name__ == "__main__":
    main()
