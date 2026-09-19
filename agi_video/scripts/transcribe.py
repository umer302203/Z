#!/usr/bin/env python3
"""faster-whisper transcription with word timestamps → transcript_timestamps.json"""
import json, sys, os

WAV = sys.argv[1] if len(sys.argv) > 1 else "/home/z/my-project/agi_video/audio/narration_AGI_locked_837s.wav"
OUT = sys.argv[2] if len(sys.argv) > 2 else "/home/z/my-project/agi_video/reports/transcript_timestamps.json"

def main():
    from faster_whisper import WhisperModel
    model = WhisperModel("small", device="cpu", compute_type="int8")
    segments, info = model.transcribe(WAV, word_timestamps=True, vad_filter=True)
    words = []
    segs = []
    for s in segments:
        seg = {"start": round(s.start, 3), "end": round(s.end, 3), "text": s.text.strip(), "words": []}
        for w in (s.words or []):
            token = w.word.strip()
            if token:
                seg["words"].append({"w": token, "start": round(w.start, 3), "end": round(w.end, 3)})
                words.append({"w": token, "start": round(w.start, 3), "end": round(w.end, 3)})
        segs.append(seg)
    data = {"language": info.language, "duration": round(info.duration, 3),
            "wav": WAV, "segments": segs, "words": words}
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as f:
        json.dump(data, f, indent=1)
    print(f"TRANSCRIBED: lang={info.language} dur={info.duration:.2f}s words={len(words)} segs={len(segs)} -> {OUT}")

if __name__ == "__main__":
    main()
