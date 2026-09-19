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

## Strict rules audit round 2 (user-requested full VIDEO_RULES compliance pass)

**Methods:** spelling sweep over all 285 screen-text strings (pyspellchecker + domain
whitelist, `src/` tooling), dense 2s-interval frame sampling of the full muxed video
(390 frames → 13 contact sheets), 22 scene-boundary before/after pairs, full-res zooms
on every suspect tile.

**Issues found and fixed (all re-rendered):**

| # | Where | Issue | Rule | Fix |
|---|-------|-------|------|-----|
| 1 | t≈65s | "OBSERVATION" chip overlapped incoming "POLICY = RULE..." card | §6/§8 | chip now exits (fade 64.7–65.1) before card enters at 65.16 |
| 2 | t≈143s | legend "COOP + COMP" (non-standard abbreviation) | §3/§2 | two proper labels: "COOPERATION" / "COMPETITION" beside their dots |
| 3 | t=373–414s | topic numbers "1./2./3./4." on limitation chips | §2 (no topic numbers) | prefixes removed → SAMPLE EFFICIENCY / SCALABILITY / REWARD DESIGN / EXPLAINABILITY |
| 4 | t≈612s | red X marks drawn on top of "SENSOR 1/2/3" words | §21 (marks never cover letters) | X moved beside each chip |
| 5 | t≈627s | "WRONG" X strike covered the word | §21 | X moved above the box |
| 6 | t≈627–634s | "WRONG DATA DISTURBS POLICY" collided with "TRUST + VERIFY + COST" chip | §6 | red chip moved up (y 740→660), 46px clearance |
| 7 | t≈752s | "WRONG GOAL = EFFICIENTLY WRONG" chip sat on the healthcare "+" icon | §6 | chip moved up (y 460→395), ~25px margins both sides |

**Clean after fixes:** dense smoke test re-run (3118 positions, 0 errors); all boundary
pairs show full old-scene removal before new-scene entry; spelling sweep clean (only
domain terms whitelisted); no fake logos; English-only labels; no subtitles/progress
bars/topic numbers; text stays supporting-role (~10%) vs visual storytelling (~90%).

## Strict rules audit round 3 — engine anchor bug + final full re-render

**New issue found post round 2 QC (frame t=143.5):** `engine.draw_text` pasted cached
text sprites centered regardless of anchor, so every `anchor="lm"/"rm"` label was
shifted LEFT by ~half its width (legend dots touched their labels; credit-scene
left-aligned labels off-position). Root cause in engine, not scene code.

**Fix:** sprite paste offset now compensates per anchor (`ox = ±(half_w + 8)` for
lm/rm). Blast radius audited: 14 lm/rm usages across seg1/2/4/5/6; seg3/seg7 contain
none. Single-frame tests at t=143 (legend) and t=165 (credits) verified the fix before
committing to a full re-render.

**Re-render:** all five affected segments re-rendered at 60fps (seg1/2/4/5/6, 7200
frames each; seg7 reused from round-2 fix build, seg3 pixel-identical). Segment
replacement script verifies frame counts BEFORE any move — this also closed the
round-2 process bug where `seg7_r3.mp4` was never moved over `seg7.mp4`, so the
t=752 fix was missing from that mux.

**Final mux verification (8/8 frames PASS, extracted from the shipped file):**

| Time | Check | Result |
|------|-------|--------|
| t=23.8 | title/chip regression (pixel-compare vs verified frame) | PASS — identical |
| t=65.4 | OBSERVATION chip exits before formula card | PASS |
| t=143.5 | legend "● COMPETITION / ● COOPERATION" anchored correctly | PASS |
| t=165 | credit-scene A/B/C/D labels centered | PASS |
| t=175.5 | CLEAR PATH left of ?-boxes | PASS |
| t=343.4 | SEARCH AREA vs COORDINATED COVERAGE separated | PASS |
| t=634 | comm scene: red chip clear, SENSOR X-marks beside chips, WRONG X above box | PASS |
| t=752.5 | "WRONG GOAL = EFFICIENTLY WRONG" fully above "+" icon (now in mux) | PASS |

ffprobe: h264 1920x1080 60fps + aac, 779.350s, 110,183,722 bytes.
Verification frames: `qc/fixcheck_r4/t*.png`.

## Full rules audit round 4 — 10 mandatory passes (§15) + workspace recovery

**Recovery:** container workspace was reset to an older snapshot; the project was
restored from the GitHub backup (sparse clone of MARL-Video/ only). The rejoined
deliverable was bit-exact (MD5 6b7b7e86…). Recovery exposed that `src/kit.py` had
never been committed — it was rebuilt from the engine primitives + call-site
inventory and validated (smoke test 3118 positions / 0 errors, style-fidelity
frames vs shipped mux). `audio/final_mix.wav` was regenerated; mix report identical.

**Ten passes executed on the corrected build:**

| # | Pass (§15) | Method | Result |
|---|------------|--------|--------|
| 1 | Storytelling flow | 7 contact sheets @5s over full 779s | PASS — continuous story, no section cards |
| 2 | Word-level sync | 10 anchors across timeline, before/onset composites | PASS — 10/10 exact at spoken word |
| 3 | Collision/overlap | sheets + full-res zooms on suspects | 4 violations found → fixed (below) |
| 4 | Spelling/overflow | AST sweep of 197 screen-text strings | PASS (SUBGOALS/SIM whitelisted domain terms) |
| 5 | Geometry coherence | 2D vector engine; shapes reviewed in sheets | PASS — no broken/floating shapes |
| 6 | Scene cleanup | 18 boundary before/after pairs | PASS — old scene fully gone in every pair |
| 7 | 1080p readability | 2x zoom crops (legend/credits/sensors/panel) | PASS after fixes |
| 8 | Audio clarity/ducking | volumedetect + mix report | PASS — peak 0.95 WAV (0.0dB AAC overshoot ≈0.01% samples, benign); duck floor 0.24 |
| 9 | Logo/icon accuracy | source grep + visual | PASS — zero external logos; neutral glyphs only |
| 10 | Export integrity | full decode (-xerror) + ffprobe | PASS — 0 decode errors, h264 1080p60 + aac |

**Violations found and fixed (§6/§21/§22 — re-rendered seg4/5/6):**

| # | Where | Issue | Fix |
|---|-------|-------|-----|
| 1 | t≈612–634 | SENSOR X-marks touched chip borders; SENSOR-3 X hit WRONG box corner | X-marks → x=748 (22px gap); WRONG box → (570–670, 760–800); X beside box |
| 2 | t≈442–451 | "SLOW DOWN FIRST" chip (y=800) overlapped "ENGINEERS NEED THE WHY" (y=820) | chip → (960, 755), 16px/26px clearances |
| 3 | t≈576–583 | driver dot + strike-X crossed "FIXED RULES" text | panel → (230–455, 585–660); strike below text; X beside text |
| 4 | t≈583–590 | "ADAPT" chip touched road bar; earlier reposition hit policy curve | chip → (330, 530) + arrow (270,570)–(390,570), verified against curve math |

**Final mux verification (15 frames):** 4 segment seams (360/480/600/720 ±0.2s — no
pop, style continuous), fix positions (443/587/628.5/634), regressions (23.8/143.5/752.5)
— all PASS. ffprobe: h264 1920×1080 60fps + aac, 779.4s.
