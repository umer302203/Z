#!/usr/bin/env python3
"""kit.py — shared visual vocabulary for MARL scenes (rebuilt).
All primitives render via engine anti-aliased primitives. Every element that
takes (t, t0) fades in over ~0.35s starting exactly at its word-anchor t0."""
import numpy as np
from PIL import Image, ImageDraw
from engine import (W, H, draw_circle, draw_line, draw_arrow, draw_rect, draw_text,
                    draw_polyline, draw_poly_fill, ease, ramp, clamp01, fade,
                    paste, make_glow,
                    BLUE, RED, GREEN, GOLD, PURPLE, WHITE, GREY, ORANGE, TEAL, BLUE_D)

def _p(t, t0, dur=0.35):
    """appear progress 0..1 starting at t0."""
    if t < t0: return 0.0
    return ease(clamp01((t - t0) / dur))

def _tint(color, a_bg=0.14):
    """chip fill: dark blend of the accent color."""
    base = np.array([16, 20, 28], np.float32)
    c = np.array(color, np.float32)
    return tuple((c * a_bg + base * (1 - a_bg)).astype(int))

# ---------------- nodes ----------------
def agent_node(f, x, y, t, t0, color, r, alpha=1.0, pulse=0.0):
    a = _p(t, t0) * alpha
    if a <= 0: return
    g = make_glow(max(6, int(r * 1.6)), color)
    g[..., 3] *= a
    paste(f, g, x, y, "add")
    draw_circle(f, x, y, r, color, a)
    if pulse > 0:
        pr = r + 6 + pulse * 10
        draw_circle(f, x, y, pr, color, a * 0.5 * (1 - pulse), width=2)

def robot_icon(f, x, y, t, t0, color, size, dirx=0, diry=0, alpha=1.0):
    """rounded square tile + glowing core; optional direction nose."""
    a = _p(t, t0) * alpha
    if a <= 0: return
    s = size * 1.15
    draw_rect(f, x - s, y - s, x + s, y + s, _tint(color, 0.22), a, width=0, radius=7)
    draw_rect(f, x - s, y - s, x + s, y + s, color, a * 0.9, width=2, radius=7)
    cr = size * 0.42
    draw_circle(f, x, y, cr, color, a)
    draw_circle(f, x, y, cr * 0.45, WHITE, a * 0.85)
    if dirx or diry:
        nx, ny = x + dirx * s, y + diry * s
        draw_line(f, (x + dirx * s * 0.2, y + diry * s * 0.2), (nx, ny), color, 2.5, a * 0.9)

def drone_icon(f, x, y, t, t0, size, alpha=1.0):
    """mini rounded tile body + center dot (matches shipped drone glyph)."""
    a = _p(t, t0) * alpha
    if a <= 0: return
    s = size * 0.85
    draw_rect(f, x - s, y - s, x + s, y + s, _tint(TEAL, 0.25), a, width=0, radius=5)
    draw_rect(f, x - s, y - s, x + s, y + s, TEAL, a * 0.95, width=2, radius=5)
    draw_circle(f, x, y, size * 0.30, WHITE, a * 0.9)

def human_icon(f, x, y, size, t, t0, color, alpha=1.0):
    a = _p(t, t0) * alpha
    if a <= 0: return
    draw_circle(f, x, y - size * 0.45, size * 0.30, color, a)
    draw_poly_fill(f, [(x - size * 0.55, y + size * 0.6), (x + size * 0.55, y + size * 0.6),
                       (x + size * 0.32, y - size * 0.05), (x - size * 0.32, y - size * 0.05)], color, a * 0.9)

def brain_icon(f, x, y, size, t, t0, color):
    a = _p(t, t0)
    if a <= 0: return
    g = make_glow(int(size * 1.2), color); g[..., 3] *= a * 0.5
    paste(f, g, x, y, "add")
    draw_circle(f, x, y, size * 0.72, color, a)
    draw_circle(f, x - size * 0.30, y - size * 0.10, size * 0.30, WHITE, a * 0.25)
    draw_circle(f, x + size * 0.30, y - size * 0.10, size * 0.30, WHITE, a * 0.25)
    draw_line(f, (x, y - size * 0.7), (x, y + size * 0.7), _tint(color, 0.0), 2, a * 0.5)

def shield_icon(f, x, y, size, t, t0, color, check_on=True):
    a = _p(t, t0)
    if a <= 0: return
    s = size
    pts = [(x - s * 0.8, y - s * 0.55), (x + s * 0.8, y - s * 0.55),
           (x + s * 0.65, y + s * 0.25), (x, y + s * 0.85), (x - s * 0.65, y + s * 0.25)]
    draw_poly_fill(f, pts, _tint(color, 0.20), a)
    draw_polyline(f, pts + [pts[0]], color, 2.5, a)
    if check_on:
        draw_polyline(f, [(x - s * 0.32, y), (x - s * 0.08, y + s * 0.26), (x + s * 0.40, y - s * 0.28)],
                      GREEN, 4.5, a)

def lock_icon(f, x, y, size, t, t0, color):
    a = _p(t, t0)
    if a <= 0: return
    s = size
    draw_rect(f, x - s * 0.75, y - s * 0.1, x + s * 0.75, y + s * 0.85, _tint(color, 0.2), a, width=0, radius=4)
    draw_rect(f, x - s * 0.75, y - s * 0.1, x + s * 0.75, y + s * 0.85, color, a, width=2.5, radius=4)
    draw_circle(f, x, y - s * 0.25, s * 0.45, color, a, width=2.5)
    draw_circle(f, x, y + s * 0.32, s * 0.12, color, a)

def box_icon(f, x, y, size, t, t0, color, alpha=1.0):
    """crate: square outline with diagonal braces."""
    a = _p(t, t0) * alpha
    if a <= 0: return
    s = size
    draw_rect(f, x - s, y - s, x + s, y + s, _tint(color, 0.18), a, width=0, radius=3)
    draw_rect(f, x - s, y - s, x + s, y + s, color, a * 0.95, width=2.5, radius=3)
    draw_polyline(f, [(x - s, y - s), (x + s, y + s)], color, 2, a * 0.8)
    draw_polyline(f, [(x + s, y - s), (x - s, y + s)], color, 2, a * 0.8)

def clock_icon(f, x, y, size, t, t0, frac=0.5, color=None):
    color = color or GOLD
    a = _p(t, t0)
    if a <= 0: return
    s = size
    draw_circle(f, x, y, s, _tint(color, 0.15), a)
    draw_circle(f, x, y, s, color, a, width=2.5)
    ang = -np.pi / 2 + clamp01(frac) * 2 * np.pi
    draw_line(f, (x, y), (x + np.cos(ang) * s * 0.72, y + np.sin(ang) * s * 0.72), color, 2.5, a)
    draw_circle(f, x, y, 2.5, color, a)

def ball(f, x, y, r, color, alpha=1.0):
    if alpha <= 0: return
    g = make_glow(int(r * 1.5), color); g[..., 3] *= alpha * 0.6
    paste(f, g, x, y, "add")
    draw_circle(f, x, y, r, color, alpha)
    draw_circle(f, x - r * 0.28, y - r * 0.28, r * 0.30, WHITE, alpha * 0.55)

def flag(f, x, y, t, t0, color, size, alpha=1.0):
    a = _p(t, t0) * alpha
    if a <= 0: return
    s = size
    draw_line(f, (x, y), (x, y - s * 2.1), GREY, 3.0, a)
    draw_poly_fill(f, [(x, y - s * 2.1), (x + s * 1.35, y - s * 1.65), (x, y - s * 1.2)], color, a)

def view_cone(f, x, y, ang, spread, length, t, t0, color, alpha=0.3):
    a = _p(t, t0)
    if a <= 0: return
    al = alpha * a
    pts = [(x, y)]
    n = 14
    for i in range(n + 1):
        th = ang - spread / 2 + spread * i / n
        pts.append((x + np.cos(th) * length, y + np.sin(th) * length))
    draw_poly_fill(f, pts, color, al * 0.55)
    draw_polyline(f, [pts[0], pts[1]], color, 1.5, al * 0.5)
    draw_polyline(f, [pts[0], pts[-1]], color, 1.5, al * 0.5)

def grid_world(f, x0, y0, x1, y1, n, t, t0, alpha):
    if alpha <= 0: return
    a = _p(t, t0) * alpha
    if a <= 0: return
    draw_rect(f, x0, y0, x1, y1, GREY, a * 0.55, width=1.5, radius=10)
    for i in range(1, n):
        fx = x0 + (x1 - x0) * i / n
        draw_line(f, (fx, y0 + 4), (fx, y1 - 4), GREY, 1.0, a * 0.30)
    for j in range(1, n):
        fy = y0 + (y1 - y0) * j / n
        draw_line(f, (x0 + 4, fy), (x1 - 4, fy), GREY, 1.0, a * 0.30)

def mini_net(f, x, y, t, t0, layers, wspread, hstep, color):
    a = _p(t, t0)
    if a <= 0: return
    pos = []
    for li, n in enumerate(layers):
        lx = x + (li - (len(layers) - 1) / 2) * wspread
        col = []
        for i in range(n):
            ly = y + (i - (n - 1) / 2) * hstep
            col.append((lx, ly))
        pos.append(col)
    for a1, a2 in zip(pos, pos[1:]):
        for p1 in a1:
            for p2 in a2:
                draw_line(f, p1, p2, color, 1.2, a * 0.30)
    for col in pos:
        for (px, py) in col:
            draw_circle(f, px, py, 4.5, color, a)

def vs_divider(f, x, y, h, t, t0):
    a = _p(t, t0)
    if a <= 0: return
    draw_line(f, (x, y - h / 2), (x, y + h / 2), GREY, 2.0, a * 0.6)
    draw_circle(f, x, y, 16, (24, 30, 40), a)
    draw_circle(f, x, y, 16, GREY, a * 0.8, width=1.5)
    draw_text(f, "VS", x, y - 1, 18, WHITE, a)

# ---------------- marks ----------------
def cross(f, x, y, size, t, t0, color=RED, width=4.0, alpha=1.0):
    a = _p(t, t0) * alpha
    if a <= 0: return
    draw_line(f, (x - size, y - size), (x + size, y + size), color, width, a)
    draw_line(f, (x - size, y + size), (x + size, y - size), color, width, a)

def check(f, x, y, size, t, t0, color=GREEN, width=5.0, alpha=1.0):
    a = _p(t, t0) * alpha
    if a <= 0: return
    draw_polyline(f, [(x - size, y), (x - size * 0.25, y + size * 0.65), (x + size, y - size * 0.6)],
                  color, width, a)

def pulse_ring(f, x, y, t, t0, color, r0=12, r1=80, alpha=0.9):
    if t < t0: return
    p = clamp01((t - t0) / 0.9)
    if p >= 1: return
    draw_circle(f, x, y, r0 + (r1 - r0) * p, color, alpha * (1 - p), width=3)

# ---------------- text panels ----------------
def chip(f, text, x, y, t, t0, color, size=24, alpha=1.0, pad=None):
    """rounded chip: colored border, dark tinted fill, colored uppercase text."""
    a = _p(t, t0) * alpha
    if a <= 0: return
    s = str(text)
    wpx = int(len(s) * size * 0.62) + 2 * (pad if pad is not None else int(size * 0.55))
    hpx = int(size * 1.55)
    draw_rect(f, x - wpx / 2, y - hpx / 2, x + wpx / 2, y + hpx / 2, _tint(color, 0.16), a, width=0, radius=10)
    draw_rect(f, x - wpx / 2, y - hpx / 2, x + wpx / 2, y + hpx / 2, color, a * 0.85, width=2, radius=10)
    draw_text(f, s, x, y - 1, size, color, a)

def chip_box(f, text, x0, y0, x1, y1, t, t0, color, size=24, alpha=1.0):
    a = _p(t, t0) * alpha
    if a <= 0: return
    draw_rect(f, x0, y0, x1, y1, _tint(color, 0.14), a, width=0, radius=12)
    draw_rect(f, x0, y0, x1, y1, color, a * 0.8, width=2, radius=12)
    if text:
        draw_text(f, str(text), (x0 + x1) / 2, (y0 + y1) / 2 - 1, size, color, a)

def meter(f, x, y, w, label, frac, t, t0, color, size=20):
    """label above a rounded track; fill animates with the appear ramp."""
    a = _p(t, t0)
    if a <= 0: return
    h = size * 0.55
    draw_text(f, label, x, y - h * 1.5 - 2, size, WHITE, a, anchor="ls")
    draw_rect(f, x, y, x + w, y + h, GREY, a * 0.22, width=0, radius=int(h / 2))
    fw = w * clamp01(frac) * a
    if fw > h / 2:
        draw_rect(f, x, y, x + fw, y + h, color, a * 0.95, width=0, radius=int(h / 2))

# ---------------- fx ----------------
def glow(f, x, y, r, color, alpha, scale=1.0):
    if alpha <= 0: return
    g = make_glow(max(4, int(r)), color, glow_scale=2.6 * scale)
    g[..., 3] *= clamp01(alpha)
    paste(f, g, x, y, "add")

def fx_slice(f, t, t0, dur=0.5, color=WHITE, n=7):
    """transition wipe slices; subtle diagonal streaks."""
    if t < t0 or t > t0 + dur: return
    p = (t - t0) / dur
    for i in range(n):
        xx = W * (p * 1.6 - 0.3 + i * 0.16)
        draw_line(f, (xx, 0), (xx - 160, H), color, 26, 0.05 * (1 - p))
