# MARL Video — Multi-Agent Reinforcement Learning (Hinglish Narration)

## Master Timeline
- Audio: multi_agent_reinforcement_learning_charon_final.wav (779.36s, 24kHz mono)
- Language: Hindi/Urdu (Hinglish) — English technical terms
- Screen text: ENGLISH short labels ONLY (per VIDEO_RULES.txt §2)
- Output: 1920x1080 @ 60fps MP4

## Engine Decision Record
- SCENE TYPE: 2D diagrams, agent/environment loops, neural nets, reward curves, robots, drones, coordination maps
- ENGINE: Custom programmatic renderer (numpy + PIL → ffmpeg pipe), 3Blue1Brown-inspired visual language
- WHY: (1) exact word-level sync required by user (frames computed directly from ASR word timestamps),
  (2) 13-min duration at 1080p60 — Manim Cairo renderer would exceed sandbox time budget (est. hours vs ~40 min),
  (3) full control over event-precise animation + SFX placement
- LIMITATION STATED: Manim not used; visual intent (progressive construction, glowing nodes, smooth transforms) preserved via custom renderer
- SFX: synthesized programmatically (numpy), each tied to a visible event, ducked under narration

## Visual Palette (3B1B-inspired, dark)
- Background: #0d1117 → #161b27 subtle radial gradient
- Primary: #58c4dd (manim blue), #83c167 (green), #fc6255 (red), #ffd54a (yellow/gold)
- Agents: blue glowing nodes; Opponents: red; Rewards: gold; Environment: slate
- Text: #e6edf3 (white-ish), font: DejaVu Sans Bold

## Scenes (word-level event map from transcript_hi_words.json)
(to be filled after transcription completes)
