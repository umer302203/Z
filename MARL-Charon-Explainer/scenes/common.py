"""Shared framework for all MARL explainer scenes.

Provides:
  - SyncedScene: frame-exact timing mixin (all durations snapped to 1/60 s)
  - Style constants + reusable visual builders (panels, chips, agents,
    robots, drones, cars, lights, bubbles, meters, mazes, arrows ...)

Design rules (VIDEO_RULES.txt): dark background, short English labels,
no full-sentence subtitles, no overlaps, arrows connect outer edges,
objects enter/exit cleanly.
"""
import math

import numpy as np

from manim import (
    Scene, VGroup, VMobject, Group, Mobject, Dot, Circle, Ellipse, Line, DashedLine,
    Arrow, Rectangle, RoundedRectangle, Square, Polygon, Triangle, Arc, ArcBetweenPoints,
    AnnularSector, Sector, Text, MathTex, Tex, Paragraph, MarkupText, SVGMobject,
    FadeIn, FadeOut, Write, Create, DrawBorderThenFill, GrowArrow, GrowFromCenter,
    GrowFromPoint, Transform, ReplacementTransform, TransformFromCopy, MoveAlongPath,
    Rotate, Indicate, Flash, FocusOn, Wiggle, Succession, LaggedStart,
    AnimationGroup, Wait, CurvesAsSubmobjects, ShowPassingFlash,
    LEFT, RIGHT, UP, DOWN, UL, UR, DL, DR, ORIGIN, PI, TAU, DL as DOWNLEFT,
    interpolate_color, manim_colors,
    config as global_config,
)

# ---------------------------------------------------------------- style ----
BG = "#0b0e14"
INK = "#e6edf3"          # primary light text
MUT = "#8b949e"          # muted grey text
BLUE = "#58a6ff"
GREEN = "#3fb950"
ORANGE = "#f0883e"
RED = "#f85149"
PURPLE = "#bc8cff"
YELLOW = "#e3b341"
TEAL = "#39c5cf"
PANEL_BG = "#151b23"
PANEL_BG2 = "#10161d"
GRIDC = "#21262d"
FONT = "sans-serif"

global_config.background_color = BG

# ------------------------------------------------------------- timing ----
FPS = 60


def snap(t):
    """Snap a duration/timestamp to the 1/60 s frame grid."""
    return round(t * FPS) / FPS


class SyncedScene(Scene):
    """Timing-accurate scene base.

    Bookkeeping mirrors manim's integer-frame rendering: because every
    duration is snapped to 1/60 s, manim renders exactly round(d*60) frames
    per play/wait call, so our clock equals the rendered clock.
    """
    DURATION = 0.0

    def setup(self):
        self._t = 0.0

    def now(self):
        return self._t

    def wait_until(self, t):
        t = snap(t)
        dt = round(t * FPS) / FPS - self._t
        if dt > 0:
            frames = round(dt * FPS)
            if frames > 0:
                self.wait(frames / FPS)
            self._t = snap(self._t + frames / FPS)

    def play_at(self, t, *anims, run_time=1.0):
        """Start animations at scene-relative time t (audio-anchored).

        If a previous animation is still running at t (schedule overlap),
        the event starts immediately instead of rewinding the clock —
        overruns are logged so schedules can be tightened.
        """
        t = snap(t)
        rt = max(snap(run_time), 1 / FPS)
        if self._t > t + 1e-9:
            import sys
            print(f"[timing] overlap: event scheduled {t:.3f} starts at "
                  f"{self._t:.3f} (+{self._t - t:.3f}s late)", file=sys.stderr)
            t = self._t
        self.wait_until(t)
        self.play(*anims, run_time=rt)
        self._t = snap(t + rt)

    def play_now(self, *anims, run_time=1.0):
        """Play immediately (no scheduled start) but keep the clock exact."""
        rt = max(snap(run_time), 1 / FPS)
        self.play(*anims, run_time=rt)
        self._t = snap(self._t + rt)

    def finish(self):
        self.wait_until(self.DURATION)


# ------------------------------------------------------------- basics ----
def label(txt, size=30, color=INK, weight="BOLD", opacity=1.0, font=FONT):
    return Text(txt, font=font, font_size=size, color=color, weight=weight,
                stroke_width=0, opacity=opacity)


def small_label(txt, color=MUT, size=22):
    return label(txt, size=size, color=color, weight="NORMAL")


def panel(w, h, stroke=GRIDC, fill=PANEL_BG, opacity=0.85, radius=0.14, sw=2.5):
    return RoundedRectangle(corner_radius=radius, width=w, height=h,
                            stroke_color=stroke, stroke_width=sw,
                            fill_color=fill, fill_opacity=opacity)


def chip(txt, color=BLUE, size=24, pad=0.22, fill=PANEL_BG, txt_color=None,
         opacity=1.0, weight="BOLD"):
    t = label(txt, size=size, color=txt_color or color, weight=weight)
    if opacity < 1.0:
        t.set_opacity(opacity)
    body = RoundedRectangle(
        corner_radius=0.12, width=t.width + 2 * pad, height=t.height + 0.30,
        stroke_color=color, stroke_width=2.0,
        fill_color=color, fill_opacity=0.10 * opacity)
    g = VGroup(body, t)
    return g


def dot(c, r=0.11, color=BLUE, opacity=1.0):
    return Dot(point=c, radius=r, color=color, fill_opacity=opacity)


def safe_vg(*items):
    return VGroup(*items)


# ------------------------------------------------------------ arrows ----
def edge_arrow(a, b, color=BLUE, buff=0.12, sw=3.0, tip=0.22, dashed=False,
               path_arc=None):
    cls = DashedLine if dashed else Line
    kw = {}
    if path_arc is not None:
        kw["path_arc"] = path_arc
    base = cls(a.get_edge_center(_dir_to(a, b)) if isinstance(a, VMobject) else a,
               b.get_edge_center(_dir_to(b, a)) if isinstance(b, VMobject) else b,
               stroke_color=color, stroke_width=sw, **kw)
    arr = Arrow(base.get_start(), base.get_end(), buff=0.0, color=color,
                stroke_width=sw, max_tip_length_to_length_ratio=0.45,
                tip_length=tip)
    if path_arc is not None:
        arr = Arrow(base.get_start(), base.get_end(), buff=0.0, color=color,
                    stroke_width=sw, path_arc=path_arc,
                    max_tip_length_to_length_ratio=0.45, tip_length=tip)
    return arr


def _dir_to(a, b):
    try:
        v = b.get_center() - a.get_center()
        if abs(v[0]) < 1e-6 and abs(v[1]) < 1e-6:
            return RIGHT
        ang = math.atan2(v[1], v[0])
        # quantize to 8 directions to avoid grazing corners
        k = round(ang / (PI / 4))
        return [RIGHT, DR + RIGHT, DR, DR + DOWN, DOWN, DL + DOWN, DL, DL + LEFT,
                LEFT, UL + LEFT, UL, UL + UP, UP, UR + UP, UR, UR + RIGHT][k % 16]
    except Exception:
        return RIGHT


def arrow_label(arr, txt, color=INK, size=20, gap=0.16, flip=False):
    """Place a small label beside an arrow's midpoint, offset perpendicular
    so it never sits on the line (VIDEO_RULES #22)."""
    t = small_label(txt, color=color, size=size)
    v = np.array(arr.get_end()) - np.array(arr.get_start())
    n = np.linalg.norm(v[:2]) or 1.0
    perp = np.array([-v[1] / n, v[0] / n, 0.0])
    if flip:
        perp = -perp
    off = perp * (t.height / 2 + gap)
    t.move_to(np.array(arr.get_center()) + off)
    return t


# ------------------------------------------------------------ icons ----
def agent_node(txt="A", color=BLUE, r=0.30, size=26):
    c = Circle(radius=r, color=color, stroke_width=3.0, fill_color=color,
               fill_opacity=0.18)
    t = label(txt, size=size, color=color)
    if t.height > 2 * r * 0.9:
        t.scale_to_fit_height(2 * r * 0.9)
    return VGroup(c, t.move_to(c.get_center()))


def robot_icon(color=BLUE, scale=1.0):
    body = RoundedRectangle(corner_radius=0.06, width=0.52, height=0.36,
                            stroke_color=color, stroke_width=2.6,
                            fill_color=color, fill_opacity=0.15)
    head = Rectangle(width=0.30, height=0.10, stroke_color=color,
                     stroke_width=2.4, fill_color=color, fill_opacity=0.15)
    head.move_to(body.get_top() + UP * 0.09)
    eye = dot(head.get_center(), r=0.030, color=color)
    w1 = Rectangle(width=0.12, height=0.07, stroke_color=color, stroke_width=2.0,
                   fill_color=color, fill_opacity=0.3)
    w2 = w1.copy()
    w1.move_to(body.get_bottom() + DOWN * 0.05 + LEFT * 0.14)
    w2.move_to(body.get_bottom() + DOWN * 0.05 + RIGHT * 0.14)
    g = VGroup(body, head, eye, w1, w2)
    g.scale(scale)
    return g


def drone_icon(color=TEAL, scale=1.0):
    body = RoundedRectangle(corner_radius=0.05, width=0.30, height=0.13,
                            stroke_color=color, stroke_width=2.4,
                            fill_color=color, fill_opacity=0.2)
    arm_l = Line(body.get_left(), body.get_left() + UL * 0.16,
                 stroke_color=color, stroke_width=2.4)
    arm_r = Line(body.get_right(), body.get_right() + UR * 0.16,
                 stroke_color=color, stroke_width=2.4)
    rot_l = Line(arm_l.get_end() + LEFT * 0.12, arm_l.get_end() + RIGHT * 0.12,
                 stroke_color=color, stroke_width=2.0)
    rot_r = Line(arm_r.get_end() + LEFT * 0.12, arm_r.get_end() + RIGHT * 0.12,
                 stroke_color=color, stroke_width=2.0)
    g = VGroup(body, arm_l, arm_r, rot_l, rot_r)
    g.scale(scale)
    return g


def car_icon(color=ORANGE, scale=1.0):
    body = RoundedRectangle(corner_radius=0.08, width=0.56, height=0.20,
                            stroke_color=color, stroke_width=2.4,
                            fill_color=color, fill_opacity=0.18)
    cab = RoundedRectangle(corner_radius=0.06, width=0.26, height=0.12,
                           stroke_color=color, stroke_width=2.0,
                           fill_color=color, fill_opacity=0.25)
    cab.move_to(body.get_center() + UP * 0.10)
    wh = dot(body.get_center() + DOWN * 0.10 + LEFT * 0.16, r=0.045, color=color)
    wh2 = dot(body.get_center() + DOWN * 0.10 + RIGHT * 0.16, r=0.045, color=color)
    g = VGroup(body, cab, wh, wh2)
    g.scale(scale)
    return g


def traffic_light(state="red", scale=1.0):
    box = RoundedRectangle(corner_radius=0.05, width=0.16, height=0.42,
                           stroke_color=MUT, stroke_width=2.0,
                           fill_color=PANEL_BG2, fill_opacity=0.9)
    r = dot(box.get_center() + UP * 0.13, r=0.05,
            color=RED if state == "red" else "#3a3f47")
    y = dot(box.get_center(), r=0.05,
            color=YELLOW if state == "yellow" else "#3a3f47")
    g = dot(box.get_center() + DOWN * 0.13, r=0.05,
            color=GREEN if state == "green" else "#3a3f47")
    out = VGroup(box, r, y, g)
    out.scale(scale)
    return out


def flag_icon(color=GREEN, scale=1.0):
    pole = Line(ORIGIN, UP * 0.44, stroke_color=MUT, stroke_width=2.6)
    tri = Polygon(UP * 0.44, UP * 0.36 + RIGHT * 0.26, UP * 0.30,
                  stroke_color=color, stroke_width=2.0,
                  fill_color=color, fill_opacity=0.8)
    g = VGroup(pole, tri)
    g.scale(scale)
    return g


def bolt_icon(color=YELLOW, scale=1.0):
    b = Polygon([-0.06, 0.16, 0], [0.05, 0.02, 0], [-0.01, 0.02, 0],
                [0.07, -0.16, 0], [-0.04, -0.02, 0], [0.0, -0.02, 0],
                [-0.08, 0.16, 0],
                stroke_color=color, stroke_width=2.0,
                fill_color=color, fill_opacity=0.85)
    g = VGroup(b)
    g.scale(scale)
    return g


def eye_icon(color=MUT, scale=1.0):
    outer = Arc(radius=0.16, start_angle=PI, angle=PI, stroke_color=color,
                stroke_width=2.6).reverse_direction()
    lower = Arc(radius=0.16, start_angle=PI, angle=-PI, stroke_color=color,
                stroke_width=2.6)
    pupil = dot(ORIGIN, r=0.045, color=color)
    g = VGroup(outer, lower, pupil)
    g.scale(scale)
    return g


def bubble(txt, color=BLUE, size=20, pad=0.16, tail="down"):
    t = label(txt, size=size, color=color, weight="NORMAL")
    body = RoundedRectangle(corner_radius=0.08, width=t.width + 2 * pad,
                            height=t.height + 2 * pad * 0.75,
                            stroke_color=color, stroke_width=2.0,
                            fill_color=color, fill_opacity=0.10)
    body.move_to(t.get_center())
    g = VGroup(body, t)
    if tail:
        p = Polygon(ORIGIN, RIGHT * 0.10 + DOWN * 0.12, RIGHT * 0.20,
                    stroke_color=color, stroke_width=2.0,
                    fill_color=color, fill_opacity=0.4)
        if tail == "down":
            p.move_to(body.get_bottom() + DOWN * 0.06).shift(LEFT * 0.08)
            p.flip(RIGHT)
        else:
            p.move_to(body.get_top() + UP * 0.06).shift(LEFT * 0.08)
        g.add(p)
    return g


def polyline_check(color=GREEN, scale=1.0, sw=4.0):
    a = Line(ORIGIN, DOWN * 0.10 + RIGHT * 0.12, stroke_color=color, stroke_width=sw)
    b = Line(DOWN * 0.10 + RIGHT * 0.12, UP * 0.18 + RIGHT * 0.40,
             stroke_color=color, stroke_width=sw)
    g = VGroup(a, b)
    g.scale(scale)
    g.move_to(ORIGIN)
    return g


def polyline_cross(color=RED, scale=1.0, sw=4.0):
    l1 = Line(UL * 0.14, DR * 0.14, stroke_color=color, stroke_width=sw)
    l2 = Line(DL * 0.14, UR * 0.14, stroke_color=color, stroke_width=sw)
    g = VGroup(l1, l2)
    g.scale(scale)
    return g


def bar_meter(w=2.2, h=0.16, value=0.5, color=GREEN, bgc=PANEL_BG2):
    bg = RoundedRectangle(corner_radius=h / 2, width=w, height=h,
                          stroke_color=GRIDC, stroke_width=1.5,
                          fill_color=bgc, fill_opacity=0.9)
    fw = max(0.02, (w - 0.03) * max(0.0, min(1.0, value)))
    fg = RoundedRectangle(corner_radius=h / 2 - 0.01, width=fw, height=h - 0.03,
                          stroke_width=0, fill_color=color, fill_opacity=0.95)
    fg.move_to(bg.get_left() + RIGHT * (0.015 + fw / 2))
    return VGroup(bg, fg)


def mini_grid(x0, y0, nx, ny, cell=0.5, color=GRIDC, sw=1.6):
    g = VGroup()
    for i in range(nx + 1):
        g.add(Line([x0 + i * cell, y0, 0], [x0 + i * cell, y0 + ny * cell, 0],
                   stroke_color=color, stroke_width=sw))
    for j in range(ny + 1):
        g.add(Line([x0, y0 + j * cell, 0], [x0 + nx * cell, y0 + j * cell, 0],
                   stroke_color=color, stroke_width=sw))
    return g


def title_footer(title_txt, color=BLUE):
    """Small top-left scene tag. Reserved safe area, never overlaps center."""
    c = chip(title_txt, color=color, size=19)
    c.to_corner(UL, buff=0.30)
    return c


def cleanup(*groups, run_time=0.5, shift=DOWN * 0.12):
    """Fade out groups (scene lifecycle exit)."""
    anims = [FadeOut(g, shift=shift) for g in groups if g is not None]
    return anims
