#!/usr/bin/env python3
"""Synthesize relevant, purposeful SFX for MARL video.
Every sound maps to a visible event family (VIDEO_RULES §11):
  whoosh     -> camera/scene transition
  pop        -> object appearance
  click      -> tool/UI activation / decision made
  chime      -> reward / verified result
  thud       -> collision / penalty
  pulse      -> data flow between nodes
  sweep      -> sensor scan / verification scan
  mech       -> robot mechanical movement
  glide      -> object movement / route drawing
  sparkle    -> emergence / new concept
  drone      -> drone/flight ambience
  riser      -> building up / training progress
All: 48kHz mono, short, restrained, mixed under narration.
"""
import numpy as np
import wave
import os

SR = 48000
OUT = "/home/z/my-project/work/marl_video/sfx"
os.makedirs(OUT, exist_ok=True)

def save(name, sig, peak=0.5):
    sig = np.asarray(sig, dtype=np.float64)
    m = np.max(np.abs(sig)) or 1.0
    sig = sig / m * peak
    # gentle fade edges to avoid clicks
    n = len(sig)
    f = min(240, n // 10)
    env = np.ones(n)
    env[:f] = np.linspace(0, 1, f)
    env[-f:] = np.linspace(1, 0, f)
    sig *= env
    data = (sig * 32767).astype(np.int16)
    with wave.open(f"{OUT}/{name}.wav", "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes(data.tobytes())
    print(f"  {name}.wav  {n/SR*1000:6.0f} ms")

def t(dur): return np.linspace(0, dur, int(SR*dur), endpoint=False)

def bandnoise(dur, lo, hi, seed=0):
    rng = np.random.default_rng(seed)
    n = rng.standard_normal(int(SR*dur))
    spec = np.fft.rfft(n)
    freqs = np.fft.rfftfreq(len(n), 1/SR)
    mask = (freqs >= lo) & (freqs <= hi)
    spec[~mask] = 0
    out = np.fft.irfft(spec, len(n))
    return out / (np.max(np.abs(out)) or 1)

def env_ad(n, a, d, curve=3.0):
    """attack-decay envelope"""
    e = np.ones(n)
    ai = max(1, int(a*SR)); di = max(1, int(d*SR))
    e[:ai] = np.linspace(0, 1, ai)
    if di < n:
        e[-di:] = np.linspace(1, 0, di)**curve
    return e

# 1. soft whoosh (transition) — filtered noise sweep, 0.55s
x = t(0.55)
noise = bandnoise(0.55, 300, 3000, seed=1)
sweep = np.sin(2*np.pi*(200 + 900*x/0.55)*x*0.5)  # subtle tone sweep
env = np.concatenate([np.linspace(0,1,int(0.28*SR)), np.linspace(1,0,int(0.27*SR))**1.5])
save("whoosh", noise*env[:len(noise)] + 0.18*sweep*env[:len(sweep)], peak=0.42)

# 2. pop reveal — quick sine blip with pitch drop, 0.12s
x = t(0.12)
f = 880*np.exp(-x*10)
sig = np.sin(2*np.pi*np.cumsum(f)/SR)*env_ad(len(x), 0.004, 0.09)
save("pop", sig, peak=0.38)

# 3. click (UI/tool activation) — 30ms filtered tick
x = t(0.05)
sig = bandnoise(0.05, 1500, 6000, seed=2)*env_ad(len(x), 0.001, 0.04)
save("click", sig, peak=0.32)

# 4. chime confirm — two-note pleasant major dyad, 0.5s
x = t(0.5)
s1 = np.sin(2*np.pi*784*x)*np.exp(-x*7)
s2 = np.sin(2*np.pi*1175*x)*np.exp(-(x-0.07).clip(0)*7)*(x>0.07)
save("chime", s1+s2, peak=0.36)

# 5. thud penalty — low freq knock, 0.25s
x = t(0.25)
f = 120*np.exp(-x*14)+45
sig = np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-x*18)
sig += bandnoise(0.25, 60, 300, seed=3)*np.exp(-x*22)*0.5
save("thud", sig, peak=0.5)

# 6. data pulse — soft digital blip pair, 0.22s
x = t(0.22)
a = np.sin(2*np.pi*620*x)*env_ad(len(x), 0.003, 0.08)
b = np.zeros_like(x); i0 = int(0.1*SR)
b[i0:] = np.sin(2*np.pi*930*x[:-i0])*env_ad(len(x)-i0, 0.003, 0.08)
save("pulse", a+b, peak=0.3)

# 7. sweep scan — rising tonal sweep, 0.45s
x = t(0.45)
f = 500 + 1400*(x/0.45)**1.6
sig = np.sin(2*np.pi*np.cumsum(f)/SR)*env_ad(len(x), 0.06, 0.22)
sig += bandnoise(0.45, 800, 4000, seed=4)*env_ad(len(x), 0.05, 0.3)*0.25
save("sweep", sig, peak=0.3)

# 8. mech move — servo-ish: damped tone + gear noise, 0.4s
x = t(0.4)
sig = np.sin(2*np.pi*95*x)*env_ad(len(x), 0.05, 0.3)
sig += bandnoise(0.4, 200, 900, seed=5)*env_ad(len(x), 0.04, 0.32)*0.45
save("mech", sig, peak=0.34)

# 9. glide — smooth sliding tone for route drawing, 0.6s
x = t(0.6)
f = 340 + 220*np.sin(2*np.pi*1.2*x)
sig = np.sin(2*np.pi*np.cumsum(f)/SR)*env_ad(len(x), 0.08, 0.25)
save("glide", sig, peak=0.26)

# 10. sparkle — tiny arpeggio of 3 high notes, 0.45s
x = t(0.45)
sig = np.zeros_like(x)
for i, f0 in enumerate([1320, 1760, 2217]):
    i0 = int(i*0.09*SR)
    seg = np.sin(2*np.pi*f0*x[:-i0] if i0 else 2*np.pi*f0*x)*np.exp(-(x[:-i0] if i0 else x)*9)
    sig[i0:] += seg
save("sparkle", sig, peak=0.28)

# 11. drone hum — soft rotor texture, 0.8s
x = t(0.8)
sig = np.sin(2*np.pi*70*x + 3*np.sin(2*np.pi*13.5*x))*env_ad(len(x), 0.15, 0.35)
sig += bandnoise(0.8, 90, 240, seed=6)*env_ad(len(x), 0.12, 0.4)*0.4
save("drone", sig, peak=0.3)

# 12. riser — training progress building, 1.0s
x = t(1.0)
f = 180 + 500*(x/1.0)**2
sig = np.sin(2*np.pi*np.cumsum(f)/SR)*env_ad(len(x), 0.5, 0.28)
save("riser", sig, peak=0.26)

# 13. success resolve — final chord (C-E-G) soft, 0.9s
x = t(0.9)
sig = sum(np.sin(2*np.pi*f*x)*np.exp(-x*3.2) for f in (523.25, 659.25, 784.0, 1046.5))
save("resolve", sig, peak=0.34)

# 14. subtle tick — timeline/step marker, 0.07s
x = t(0.07)
save("tick", np.sin(2*np.pi*1150*x)*env_ad(len(x), 0.002, 0.05), peak=0.24)

print("All SFX synthesized in", OUT)
