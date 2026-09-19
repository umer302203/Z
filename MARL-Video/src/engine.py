#!/usr/bin/env python3
"""
MARL Video Engine — 3Blue1Brown-inspired programmatic renderer.
Anti-aliased numpy/PIL primitives, glow sprites, easing, particles.
Renders 1920x1080 @ 60fps frames piped to ffmpeg.
"""
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1920, 1080
FPS = 60

# ---------------- palette ----------------
BG_TOP = (13, 17, 23)        # dark slate
BG_BOT = (22, 27, 39)
BLUE   = (88, 196, 221)      # agents
BLUE_D = (48, 120, 150)
GREEN  = (131, 193, 103)     # rewards/success
RED    = (252, 98, 85)       # opponents/penalty
GOLD   = (255, 213, 74)      # reward gold
PURPLE = (199, 146, 234)
WHITE  = (230, 237, 243)
GREY   = (139, 148, 158)
ORANGE = (255, 158, 61)
TEAL   = (63, 185, 168)

_font_cache = {}
_text_cache = {}

def get_font(size):
    if size not in _font_cache:
        _font_cache[size] = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", size)
    return _font_cache[size]

def ease(t, mode="inout"):
    """t in 0..1 -> eased 0..1"""
    if t <= 0: return 0.0
    if t >= 1: return 1.0
    if mode == "inout":
        return 3*t*t - 2*t*t*t
    if mode == "out":
        return 1 - (1-t)**3
    if mode == "outexpo":
        return 1 if t >= 1 else 1 - 2**(-10*t)
    if mode == "in":
        return t*t*t
    if mode == "back":
        c = 1.70158 * 1.2
        return 1 + (c+1)*(t-1)**3 + c*(t-1)**2
    if mode == "bounce":
        return 1 - (1-t)**2
    return t

def clamp01(x): return 0.0 if x < 0 else (1.0 if x > 1 else x)

def win(t, t0, t1):
    """1 while t in [t0,t1]"""
    return 1.0 if t0 <= t <= t1 else 0.0

def ramp(t, t0, dur, mode="inout"):
    """0->1 over [t0, t0+dur]"""
    return ease(clamp01((t - t0) / max(dur, 1e-6)), mode)

def fade(t, t0, t1, fin=0.4, fout=0.4):
    """smooth in/out window"""
    a = ramp(t, t0, fin)
    b = 1 - ramp(t, t1 - fout, fout)
    return a * b

# ---------------- background ----------------
def make_background(seed=7):
    """Pre-rendered dark gradient + vignette + faint grid + subtle stars/particles."""
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    cx, cy = W/2, H/2
    g = (yy / H)
    bg = np.zeros((H, W, 3), np.float32)
    for i in range(3):
        bg[..., i] = BG_TOP[i] + (BG_BOT[i] - BG_TOP[i]) * g
    # radial darkening at edges (vignette)
    r = np.sqrt(((xx-cx)/(W*0.62))**2 + ((yy-cy)/(H*0.62))**2)
    v = 1 - 0.35*np.clip(r-0.55, 0, 1)
    bg *= v[..., None]
    # faint grid
    grid = (np.sin(xx/120*np.pi) > 0.995) | (np.sin(yy/120*np.pi) > 0.995)
    bg[grid] += 4
    # subtle noise
    rng = np.random.default_rng(seed)
    bg += rng.normal(0, 1.1, bg.shape).astype(np.float32)
    return np.clip(bg, 0, 255)

# ---------------- glow sprites ----------------
def make_glow(radius, color, glow_scale=2.6, core_alpha=1.0):
    """RGBA float sprite: bright core + soft gaussian glow. size = diameter."""
    gr = int(radius * glow_scale)
    size = gr * 2 + 1
    yy, xx = np.mgrid[0:size, 0:size].astype(np.float32)
    d = np.sqrt((xx - gr)**2 + (yy - gr)**2)
    core = np.clip(1 - d/ (radius+0.5), 0, 1) ** 0.7
    glow = np.exp(-(d/(radius*0.75))**2 * 1.2) * 0.55
    a = np.clip(core*core_alpha + glow, 0, 1)
    sprite = np.zeros((size, size, 4), np.float32)
    for i in range(3):
        sprite[..., i] = color[i]
    sprite[..., 3] = a * 255
    return sprite

def paste(frame, sprite, x, y, mode="over"):
    """paste RGBA float sprite centered at (x,y). mode: over|add"""
    h, w = sprite.shape[:2]
    x0, y0 = int(round(x - w/2)), int(round(y - h/2))
    x1, y1 = x0 + w, y0 + h
    fx0, fy0 = max(0, -x0), max(0, -y0)
    fx1, fy1 = w - max(0, x1 - W), h - max(0, y1 - H)
    if fx1 <= fx0 or fy1 <= fy0: return
    x0, y0 = max(0, x0), max(0, y0)
    x1, y1 = min(W, x1), min(H, y1)
    roi = frame[y0:y1, x0:x1]
    sp = sprite[fy0:fy1, fx0:fx1]
    a = (sp[..., 3:4] / 255.0)
    if mode == "add":
        frame[y0:y1, x0:x1] = np.clip(roi + sp[..., :3] * (sp[..., 3:4]/255.0), 0, 255)
    else:
        frame[y0:y1, x0:x1] = roi*(1-a) + sp[..., :3]*a

# ---------------- anti-aliased primitives (numpy, ROI-based) ----------------
def _roi(frame, x0, y0, x1, y1):
    x0, y0 = int(max(0, x0)), int(max(0, y0))
    x1, y1 = int(min(W, x1)), int(min(H, y1))
    return x0, y0, frame[y0:y1, x0:x1]

def draw_line(frame, p1, p2, color, width=3.0, alpha=1.0, dash=None):
    """anti-aliased line via segment distance field."""
    x1f, y1f = p1; x2f, y2f = p2
    pad = width + 3
    x0, y0, roi = _roi(frame, min(x1f,x2f)-pad, min(y1f,y2f)-pad, max(x1f,x2f)+pad, max(y1f,y2f)+pad)
    if roi.size == 0: return
    yy, xx = np.mgrid[y0:y0+roi.shape[0], x0:x0+roi.shape[1]].astype(np.float32)
    dx, dy = x2f-x1f, y2f-y1f
    L2 = dx*dx + dy*dy
    if L2 < 1e-6:
        t = np.zeros_like(xx)
    else:
        t = np.clip(((xx-x1f)*dx + (yy-y1f)*dy)/L2, 0, 1)
    px, py = x1f + t*dx, y1f + t*dy
    d = np.sqrt((xx-px)**2 + (yy-py)**2)
    cov = np.clip(width/2 + 0.5 - d, 0, 1)
    if dash is not None and dash > 0:
        seg = np.sqrt((xx-px)**2+(yy-py)**2)  # distance along approx (use t*L)
        along = t * np.sqrt(L2)
        cov *= ((along // dash) % 2 == 0)
    a = (cov * alpha)[..., None]
    col = np.array(color, np.float32)
    frame[y0:y0+roi.shape[0], x0:x0+roi.shape[1]] = roi*(1-a) + col*a

def draw_circle(frame, cx, cy, radius, color, alpha=1.0, width=0):
    """filled anti-aliased circle; width>0 => ring."""
    pad = radius + width + 4
    x0, y0, roi = _roi(frame, cx-pad, cy-pad, cx+pad, cy+pad)
    if roi.size == 0: return
    yy, xx = np.mgrid[y0:y0+roi.shape[0], x0:x0+roi.shape[1]].astype(np.float32)
    d = np.sqrt((xx-cx)**2 + (yy-cy)**2)
    if width > 0:
        band = np.abs(d - radius)
        cov = np.clip(width/2 + 0.5 - band, 0, 1)
    else:
        cov = np.clip(radius + 0.5 - d, 0, 1)
    a = (cov * alpha)[..., None]
    col = np.array(color, np.float32)
    frame[y0:y0+roi.shape[0], x0:x0+roi.shape[1]] = roi*(1-a) + col*a

def draw_rect(frame, x0, y0, x1, y1, color, alpha=1.0, width=0, radius=0):
    """filled/outline rounded rect, anti-aliased via PIL on ROI at 2x."""
    if x1 < x0: x0, x1 = x1, x0
    if y1 < y0: y0, y1 = y1, y0
    pad = 6
    rx0, ry0 = int(max(0, x0-pad)), int(max(0, y0-pad))
    rx1, ry1 = int(min(W, x1+pad)), int(min(H, y1+pad))
    rw, rh = rx1-rx0, ry1-ry0
    if rw <= 0 or rh <= 0: return
    S = 2
    img = Image.new("RGBA", (rw*S, rh*S), (0,0,0,0))
    d = ImageDraw.Draw(img)
    box = [(x0-rx0)*S, (y0-ry0)*S, (x1-rx0)*S, (y1-ry0)*S]
    col = tuple(int(c) for c in color)
    if width > 0:
        d.rounded_rectangle(box, radius=radius*S, outline=col+(int(255*alpha),), width=int(width*S))
    else:
        d.rounded_rectangle(box, radius=radius*S, fill=col+(int(255*alpha),))
    img = img.resize((rw, rh), Image.LANCZOS)
    arr = np.asarray(img, np.float32)
    a = arr[..., 3:4]/255
    frame[ry0:ry1, rx0:rx1] = frame[ry0:ry1, rx0:rx1]*(1-a) + arr[..., :3]*a

def draw_polyline(frame, pts, color, width=3.0, alpha=1.0, dash=None):
    for i in range(len(pts)-1):
        draw_line(frame, pts[i], pts[i+1], color, width, alpha, dash=dash)

def draw_arrow(frame, p1, p2, color, width=3.0, alpha=1.0, head=14.0):
    """line + filled arrowhead stopping at target edge."""
    x1f, y1f = p1; x2f, y2f = p2
    dx, dy = x2f-x1f, y2f-y1f
    L = np.hypot(dx, dy) or 1
    ux, uy = dx/L, dy/L
    e2 = (x2f - ux*head*0.8, y2f - uy*head*0.8)
    draw_line(frame, p1, e2, color, width, alpha)
    # head triangle
    px, py = -uy, ux
    tri = [(x2f, y2f), (x2f - ux*head + px*head*0.5, y2f - uy*head + py*head*0.5),
           (x2f - ux*head - px*head*0.5, y2f - uy*head - py*head*0.5)]
    _fill_poly(frame, tri, color, alpha)

def _fill_poly(frame, pts, color, alpha):
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    pad = 4
    rx0, ry0 = int(max(0, min(xs)-pad)), int(max(0, min(ys)-pad))
    rx1, ry1 = int(min(W, max(xs)+pad)), int(min(H, max(ys)+pad))
    rw, rh = rx1-rx0, ry1-ry0
    if rw <= 0 or rh <= 0: return
    S = 2
    img = Image.new("L", (rw*S, rh*S), 0)
    d = ImageDraw.Draw(img)
    d.polygon([((x-rx0)*S, (y-ry0)*S) for x, y in pts], fill=255)
    img = img.resize((rw, rh), Image.LANCZOS)
    a = (np.asarray(img, np.float32)/255 * alpha)[..., None]
    col = np.array(color, np.float32)
    frame[ry0:ry1, rx0:rx1] = frame[ry0:ry1, rx0:rx1]*(1-a) + col*a

def draw_poly_fill(frame, pts, color, alpha=1.0):
    _fill_poly(frame, pts, color, alpha)

# ---------------- text ----------------
def draw_text(frame, text, x, y, size=40, color=WHITE, alpha=1.0, anchor="mm", glow=False):
    """cached text sprite paste. anchor: mm|lm|rm|ma (PIL anchors)."""
    key = (text, size, color, anchor)
    spr = _text_cache.get(key)
    if spr is None:
        f = get_font(size)
        tmp = Image.new("RGBA", (10, 10))
        d = ImageDraw.Draw(tmp)
        bbox = d.textbbox((0, 0), text, font=f, anchor=anchor)
        tw, th = bbox[2]-bbox[0]+16, bbox[3]-bbox[1]+16
        img = Image.new("RGBA", (tw, th), (0,0,0,0))
        d = ImageDraw.Draw(img)
        d.text((8-bbox[0], 8-bbox[1]), text, font=f, fill=color+(255,), anchor=anchor)
        spr = np.asarray(img, np.float32)
        if len(_text_cache) > 400:
            _text_cache.clear()
        _text_cache[key] = spr
    ox = {"mm": 0, "lm": 8, "rm": -8, "ma": 0}.get(anchor, 0)
    oy = {"mm": 0, "lm": 0, "rm": 0, "ma": 8}.get(anchor, 0)
    spr2 = spr
    if alpha < 1:
        spr2 = spr.copy()
        spr2[..., 3] *= alpha
    paste(frame, spr2, x+ox, y+oy, mode="add" if glow else "over")

# ---------------- particles ----------------
class Particles:
    def __init__(self, n, seed=0):
        rng = np.random.default_rng(seed)
        self.p = rng.uniform(0, [W, H], (n, 2)).astype(np.float32)
        self.v = (rng.standard_normal((n, 2)) * 8).astype(np.float32)
        self.n = n
        self.base = np.clip(rng.uniform(0.25, 1.0, n), 0, 1)
    def step(self, dt, drift=(0, -6), wrap=True):
        self.p += (self.v + np.array(drift, np.float32)) * dt
        self.v *= 0.995
        if wrap:
            self.p[:, 0] %= W
            self.p[:, 1] %= H
    def draw(self, frame, color=GREY, size=1.6, alpha=0.5):
        for i in range(self.n):
            a = alpha * self.base[i]
            draw_circle(frame, self.p[i,0], self.p[i,1], size, color, a)

# ---------------- renderer ----------------
class Renderer:
    def __init__(self, out_path, total_frames):
        import subprocess
        self.proc = subprocess.Popen([
            "ffmpeg", "-y", "-v", "error",
            "-f", "rawvideo", "-pix_fmt", "rgb24",
            "-s", f"{W}x{H}", "-r", str(FPS),
            "-i", "-",
            "-c:v", "libx264", "-preset", "medium", "-crf", "18",
            "-pix_fmt", "yuv420p",
            out_path,
        ], stdin=subprocess.PIPE)
        self.total = total_frames
        self.frame_i = 0
        self.bg = make_background()
    def new_frame(self):
        return self.bg.copy()
    def write(self, frame):
        self.proc.stdin.write(np.clip(frame, 0, 255).astype(np.uint8).tobytes())
        self.frame_i += 1
        if self.frame_i % (FPS*10) == 0:
            pct = self.frame_i / self.total * 100
            print(f"  RENDER {pct:.0f}%  ({self.frame_i}/{self.total})", flush=True)
    def close(self):
        self.proc.stdin.close()
        self.proc.wait()
