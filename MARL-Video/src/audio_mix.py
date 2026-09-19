#!/usr/bin/env python3
"""Audio mix: narration (master) + relevant SFX at event times + subtle ambient bed.
SFX ducked automatically during speech regions (attack 60ms, release 400ms)."""
import json, wave, os
import numpy as np

SR = 48000
VID = "/home/z/my-project/work/marl_video"
DUR = 779.357
N = int(DUR * SR)

# ---------- narration ----------
w = wave.open(f"{VID}/../../download/drive_folder_1/multi_agent_reinforcement_learning_charon_final.wav")
narr = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32767.0
w.close()
narr = np.interp(np.linspace(0, len(narr)/24000.0, N, dtype=np.float32), (np.arange(len(narr))/24000.0).astype(np.float32), narr).astype(np.float32)
narr *= 0.92 / max(np.max(np.abs(narr)), 1e-9)

# ---------- speech mask for ducking ----------
tr = json.load(open(f"{VID}/transcript_hi_words.json"))
mask = np.zeros(N, dtype=bool)
for wd in tr["words"]:
    a = max(0, int((wd["start"]-0.12) * SR))
    b = min(N, int((wd["end"]+0.22) * SR))
    mask[a:b] = True

# smooth duck envelope: 1.0 -> DUCK during speech (vectorized)
def smooth_env(mask, atk_ms=60, rel_ms=400):
    from scipy.ndimage import minimum_filter1d
    from scipy.signal import lfilter
    raw = np.where(mask, 0.0, 1.0)
    ka = int(SR*atk_ms/1000) | 1
    fast = minimum_filter1d(raw, size=ka, origin=-(ka//2))   # instant-ish drop
    a = 1.0 - np.exp(-1.0/(SR*0.13))                          # ~400ms rise via one-pole
    return lfilter([a], [1, -(1-a)], fast)

print("Building duck envelope...", flush=True)
duck = smooth_env(mask).astype(np.float32)
duck = 0.24 + 0.76*duck   # floor 0.24 during speech
np.save(f"{VID}/audio/duck.npy", duck)

# ---------- SFX events ----------
SFX_DIR = f"{VID}/sfx"
sfx_cache = {}
def load(name):
    if name not in sfx_cache:
        ww = wave.open(f"{SFX_DIR}/{name}.wav")
        d = np.frombuffer(ww.readframes(ww.getnframes()), np.int16).astype(np.float32)/32767.0
        ww.close()
        sfx_cache[name] = d
    return sfx_cache[name]

E = []
def ev(t, name, g=0.4):
    E.append((t, name, g))

# transitions
for t in [0.30, 19.94, 26.10, 46.72, 55.18, 86.12, 91.48, 127.66, 149.02, 200.32,
          239.02, 281.48, 304.94, 325.54, 348.08, 370.02, 451.50, 506.14, 547.88,
          589.88, 634.52, 679.92, 721.44]:
    ev(t, "whoosh", 0.5)
# scene beats
ev(5.10, "pop", .4); ev(5.6, "pop", .3); ev(6.1, "pop", .3)
ev(7.24, "tick", .35); ev(8.04, "pop", .3); ev(8.84, "pop", .3)
ev(10.36, "click", .4); ev(13.34, "glide", .45); ev(14.46, "glide", .3)
ev(16.26, "pulse", .4); ev(18.02, "chime", .5)
ev(21.40, "sparkle", .4); ev(23.82, "sparkle", .45)
ev(31.76, "pop", .35); ev(36.38, "pulse", .4); ev(37.90, "pulse", .4)
ev(40.30, "chime", .45); ev(40.90, "thud", .4); ev(43.26, "riser", .35)
ev(46.9, "mech", .4); ev(48.40, "chime", .4); ev(50.88, "thud", .5)
ev(52.20, "mech", .35); ev(53.76, "sparkle", .4)
ev(60.06, "sweep", .35); ev(62.44, "click", .4); ev(65.16, "click", .3)
ev(69.16, "glide", .35); ev(73.78, "mech", .3); ev(79.12, "pulse", .4)
ev(87.88, "mech", .4)
ev(93.00, "chime", .35); ev(94.66, "thud", .45); ev(96.74, "glide", .4)
ev(97.58, "chime", .45); ev(98.76, "chime", .4)
ev(102.68, "drone", .5); ev(104.24, "sweep", .35); ev(107.78, "chime", .3)
ev(110.78, "thud", .4); ev(112.76, "tick", .3); ev(113.76, "tick", .3)
ev(114.50, "mech", .35)
ev(129.58, "riser", .35); ev(137.06, "click", .35); ev(138.52, "pulse", .35)
ev(140.94, "pulse", .35)
ev(153.36, "chime", .45); ev(158.54, "pop", .4); ev(158.75, "pop", .3)
ev(158.95, "pop", .3); ev(159.15, "pop", .3)
ev(161.96, "chime", .4); ev(166.50, "click", .35); ev(168.24, "mech", .4)
ev(169.70, "sweep", .35); ev(174.52, "pop", .35); ev(175.54, "thud", .4)
ev(185.18, "chime", .35); ev(186.26, "chime", .35); ev(195.78, "tick", .35)
ev(197.46, "thud", .3)
ev(202.56, "tick", .4); ev(204.22, "tick", .4); ev(206.54, "drone", .45)
ev(208.50, "click", .3); ev(210.32, "chime", .5); ev(215.12, "pulse", .4)
ev(218.16, "pop", .35); ev(219.5, "tick", .3); ev(219.8, "tick", .3); ev(220.1, "tick", .3)
ev(225.34, "pop", .3); ev(229.30, "pulse", .4); ev(237.86, "chime", .4)
ev(245.78, "pop", .35); ev(246.88, "pop", .35); ev(253.30, "thud", .3)
ev(255.56, "chime", .35); ev(260.38, "pulse", .4); ev(262.66, "glide", .35)
ev(271.40, "click", .3); ev(273.04, "pulse", .4)
ev(286.14, "pop", .35); ev(288.06, "click", .3); ev(288.20, "click", .25)
ev(288.34, "click", .25); ev(288.48, "click", .25)
ev(295.38, "pulse", .4); ev(300.50, "thud", .45); ev(303.64, "chime", .45)
ev(307.78, "pop", .35); ev(312.06, "thud", .35); ev(315.14, "click", .35)
ev(317.14, "thud", .4); ev(320.98, "chime", .45)
ev(326.70, "drone", .5); ev(326.9, "drone", .3); ev(327.1, "drone", .3)
ev(331.88, "sweep", .35); ev(340.20, "riser", .4); ev(343.44, "pulse", .45)
ev(345.00, "glide", .35)
ev(349.40, "pop", .35); ev(350.34, "pulse", .4); ev(357.68, "pulse", .35)
ev(362.70, "whoosh", .4); ev(363.00, "sweep", .35)
ev(365.04, "click", .3); ev(369.14, "click", .3)
ev(373.30, "tick", .35); ev(386.04, "thud", .35)
ev(392.14, "tick", .35); ev(395.68, "riser", .3)
ev(403.58, "tick", .35); ev(406.20, "mech", .35); ev(408.00, "thud", .4)
ev(413.28, "tick", .35); ev(424.36, "click", .3); ev(436.70, "thud", .3)
ev(440.12, "mech", .35)
ev(453.50, "sparkle", .4); ev(458.62, "pulse", .35); ev(460.74, "chime", .4)
ev(471.56, "whoosh", .4)
ev(482.50, "pop", .3); ev(484.12, "pop", .3); ev(485.90, "pop", .3); ev(487.46, "pop", .3)
ev(496.64, "tick", .35); ev(499.48, "sparkle", .35); ev(505.00, "chime", .4)
ev(508.68, "pop", .35); ev(508.9, "pop", .3); ev(509.1, "pop", .3)
ev(511.96, "sweep", .35); ev(513.62, "click", .3); ev(515.12, "click", .3)
ev(517.86, "thud", .35); ev(520.02, "thud", .3); ev(522.66, "chime", .4)
ev(526.38, "pulse", .4); ev(528.04, "pulse", .35); ev(529.94, "mech", .3)
ev(531.60, "chime", .5); ev(538.40, "pulse", .35); ev(546.92, "chime", .4)
ev(552.02, "riser", .3); ev(558.90, "thud", .4); ev(560.74, "whoosh", .35)
ev(563.92, "pop", .3); ev(565.36, "thud", .35); ev(568.90, "pulse", .35)
ev(576.18, "thud", .3); ev(580.38, "sweep", .3); ev(583.02, "chime", .35)
ev(584.84, "click", .3); ev(586.02, "riser", .3)
ev(592.92, "thud", .35); ev(598.64, "thud", .3)
ev(602.46, "click", .35); ev(602.71, "click", .3); ev(602.96, "click", .3)
ev(608.50, "pop", .35); ev(610.76, "thud", .3); ev(614.08, "pulse", .35)
ev(616.28, "chime", .4); ev(621.36, "chime", .35)
ev(624.14, "thud", .35); ev(626.82, "thud", .35); ev(630.30, "chime", .4)
ev(636.60, "pop", .35); ev(641.58, "chime", .3); ev(644.56, "chime", .3)
ev(650.02, "thud", .3); ev(653.84, "pulse", .4); ev(657.34, "thud", .3)
ev(662.64, "chime", .4); ev(670.18, "pop", .3); ev(675.06, "chime", .35)
ev(677.84, "whoosh", .4)
ev(682.06, "tick", .35); ev(684.00, "thud", .3); ev(687.14, "tick", .3)
ev(691.76, "tick", .3); ev(692.54, "tick", .3); ev(693.64, "tick", .3)
ev(698.06, "tick", .3); ev(699.04, "tick", .3); ev(708.10, "tick", .3)
ev(710.52, "pop", .3); ev(712.98, "pulse", .4); ev(715.62, "chime", .4)
ev(727.90, "pop", .3); ev(729.02, "pop", .3); ev(730.44, "pop", .3)
ev(731.98, "pop", .3); ev(733.90, "pop", .3)
ev(736.32, "pulse", .4); ev(739.54, "chime", .4)
ev(742.06, "click", .3); ev(743.86, "click", .3); ev(744.68, "pop", .3)
ev(748.36, "thud", .4); ev(755.68, "chime", .45); ev(756.46, "tick", .3)
ev(758.30, "pop", .3); ev(760.78, "sparkle", .4); ev(766.10, "riser", .35)
ev(771.76, "chime", .4); ev(777.68, "resolve", .55)

print(f"{len(E)} SFX events", flush=True)
sfx_track = np.zeros(N, np.float32)
for (t, name, g) in E:
    d = load(name)
    i0 = int(t*SR)
    i1 = min(N, i0+len(d))
    if i1 > i0:
        np.add(sfx_track[i0:i1], (d[:i1-i0]*np.float32(g)).astype(np.float32), out=sfx_track[i0:i1], casting="unsafe")
sfx_track /= max(np.max(np.abs(sfx_track)), 1e-9)
sfx_track *= 0.42   # SFX bus level well under narration

# ---------- ambient bed (very low) ----------
print("Ambient bed...", flush=True)
rng = np.random.default_rng(42)
taxis = (np.arange(N, dtype=np.float32)/SR)
bed = (np.sin(2*np.pi*110*taxis).astype(np.float32)*0.5 + np.sin(2*np.pi*165.2*taxis).astype(np.float32)*0.3
       + np.sin(2*np.pi*220.5*taxis+1.3).astype(np.float32)*0.2)
lfo = (0.6 + 0.4*np.sin(2*np.pi*0.05*taxis)).astype(np.float32)
bed *= lfo * 0.5
from scipy.ndimage import uniform_filter1d
bed += uniform_filter1d(rng.standard_normal(N, dtype=np.float32), size=1200).astype(np.float32)*np.float32(38.0)  # smoothed noise ~ same scale
bed /= max(np.max(np.abs(bed)), 1e-9)
bed *= 0.055

# ---------- mix ----------
duck_bed = 0.35 + 0.65*duck   # bed ducks deeper
mix = narr + sfx_track*duck + bed*duck_bed.astype(np.float32)
# safety limiter
mix = np.tanh(mix*1.12)/np.tanh(1.12)
peak = np.max(np.abs(mix))
mix *= 0.95/peak
print(f"peak before norm {peak:.3f} -> normalized 0.95", flush=True)

# ---------- write stereo 48k ----------
st = np.stack([mix, mix], axis=1)
pcm = (st*32767).astype(np.int16)
with wave.open(f"{VID}/audio/final_mix.wav", "wb") as o:
    o.setnchannels(2); o.setsampwidth(2); o.setframerate(SR)
    o.writeframes(pcm.tobytes())

# QC report (vectorized)
speech_rms = np.sqrt(np.mean(mix[mask]**2)) if mask.any() else 0
sil = ~mask
# find silence runs > 1.5s via diff
padded = np.concatenate([[False], sil, [False]])
edges = np.flatnonzero(np.diff(padded.astype(np.int8)))
starts, ends = edges[0::2], edges[1::2]
sil_regions = [(a, b) for a, b in zip(starts, ends) if b - a > SR*1.5]
if sil_regions:
    idx = np.concatenate([np.arange(a, min(b, a+SR*3)) for a, b in sil_regions[:20]])
    sil_rms = float(np.sqrt(np.mean(mix[idx]**2)))
else:
    sil_rms = 0.0
report = {
    "duration_s": DUR,
    "sfx_events": len(E),
    "speech_regions_pct": round(float(mask.mean()*100), 1),
    "rms_during_speech": round(float(speech_rms), 4),
    "rms_in_pauses": round(float(sil_rms), 4),
    "duck_floor": 0.24,
    "peak": 0.95,
    "clipping": False,
}
json.dump(report, open(f"{VID}/audio/mix_report.json", "w"), indent=1)
print("MIX DONE:", report)
