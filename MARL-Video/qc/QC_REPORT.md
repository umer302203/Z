# QC Report — MARL Explainer Video

Video: 1920x1080 @ 60fps, 779.35s (12:59), h264+aac
Engine: custom numpy/PIL renderer (see src/), deterministic frame dispatch by absolute time

## QC passes performed

1. **Dense smoke test (pre-render)** — all 3118 word-synced positions exercised across
   scene modules; zero draw errors; one dash divide-by-zero guarded.
2. **Contact sheets** — 43 QC frames extracted from the muxed timeline in 6 sheets
   (`sheets/final_sheet_*.png`), reviewed for overlap/legibility/composition.
3. **Full-res spot checks** on flagged timestamps, fixes applied, segments re-rendered:

| Time | Issue found | Fix | Status |
|------|-------------|-----|--------|
| t=23.8s | "COMPUTER PROGRAMS" chip overlapped "MULTI-AGENT" title | chip removed/repositioned | FIXED — `fix_t23.8.png` |
| t=175.5s | "CLEAR PATH" chip rendered on top of reward ?-boxes | moved left of boxes | FIXED — `fix_t175.5.png` |
| t=343.4s | "LARGE AREA" and "COORDINATED COVERAGE" at same position | title/chip separated | FIXED — `fix_t343.4.png` |
| 451.5–506s | recap scene cluttered | restructured into 4 clean phases (loop diagram → single vs multi → shared-world strip → final question) | FIXED — `recap_p1..p4.png` |

4. **Post-re-render verification** — frames re-extracted from the re-rendered segments
   (`fix_*.png`, `recap_*.png` in this folder) confirm every fix landed.
5. **Audio QC** — 234 SFX events at word-synced timestamps, speech-aware ducking
   (see `audio/mix_report.json`), peak level checked, no clipping.

## Word-level sync method

- faster-whisper transcription with word-level timestamps (Hindi/Urdu Hinglish narration,
  English technical terms), ASR-skipped regions re-transcribed and merged
  (warehouse intro ~86s, rescue-drones coverage ~102–108s).
- 238 visual anchors bound to word onsets (`transcript/anchors.json`); every text reveal
  and SFX event fires at the exact spoken moment of its anchor word.

## Final mux verification (post re-render)

- Concat (stream copy, identical codec params) + audio mux: **PASS**
- ffprobe: h264 1920x1080 60fps + aac 192k, duration **779.35s** (== narration length), 110MB
- Fixed positions re-checked **in the final muxed file** (t=23.8 / 175.5 / 343.4 / 455 / 475 / 488 / 500):
  all clean, no overlaps, recap phases intact.
- Deliverable: `download/MARL_explainer_final.mp4`; repo copies in `final/`
  (split parts + 720p preview).
