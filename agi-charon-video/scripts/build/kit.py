"""Scene construction kit: nodes, icons, arrows, floors, animation helpers.

All label text uses the loaded Devanagari font (Hindi) or DejaVu (Latin/symbols).
Timing: every event time is seconds; converted to frames with round(t*FPS).
"""
import math
import bpy
from mathutils import Vector, Euler
from . import common as C

FPS = 30
FONT_HI = None   # Devanagari
FONT_EN = None   # DejaVu Sans (default fallback)
CURRENT_STAGE = None  # default link target for kit-created objects

try:
    FONT_HI = bpy.data.fonts.load("/home/z/.fonts/NotoSansDevanagari-Bold.ttf")
except Exception:
    FONT_HI = None
try:
    FONT_EN = bpy.data.fonts.load("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")
except Exception:
    FONT_EN = None


def f(t):
    """seconds -> frame number"""
    return max(1, int(round(t * FPS)))


_WORDS = None


def _load_words():
    global _WORDS
    if _WORDS is None:
        import json
        with open("/home/z/my-project/data/words.json", encoding="utf-8") as fh:
            _WORDS = json.load(fh)["words"]
    return _WORDS


def W(sub, occ=0, fallback=None):
    """Start time of the occ-th word containing substring `sub` (Hindi or Latin)."""
    n = 0
    for w in _load_words():
        if sub in w["w"]:
            if n == occ:
                return w["start"]
            n += 1
    return fallback if fallback is not None else 0.0


class Stage:
    """Per-shot stage wrapper auto-offsetting X by idx*STAGE_GAP."""

    def __init__(self, idx, shot_id):
        self.col, self.off = C.new_stage(idx, shot_id)
        self.idx = idx
        global CURRENT_STAGE
        CURRENT_STAGE = self.col

    def O(self, x, y, z):
        return (x + self.off, y, z)

    def off3(self):
        return (self.off, 0, 0)

    def pad(self, name, w, d, color="floor", loc=(0, 0, 0)):
        return floor_pad(name, w, d, loc=(loc[0] + self.off, loc[1], loc[2]),
                         col_target=self.col, color=color)

    def lights(self, key_loc, look=(0, 0, 1), key_energy=3.0, fill_loc=None):
        ls = C.scene_lights((key_loc[0] + self.off, key_loc[1], key_loc[2]),
                            key_energy=key_energy, fill_loc=(
                                fill_loc[0] + self.off, fill_loc[1], fill_loc[2]) if fill_loc else None,
                            col_target=self.col, name="L%d" % self.idx)
        for L in ls.values():
            C.aim_light(L, (look[0] + self.off, look[1], look[2]))
        return ls


# ---------------------------------------------------------------- materials
def _m(name, rgba, spec=0.3, rough=0.5):
    return C.mat(name, rgba, spec=spec, rough=rough)


M = {}


def mats():
    if M:
        return M
    M["white"] = _m("k_white", (0.95, 0.95, 0.96, 1))
    M["panel"] = _m("k_panel", (0.98, 0.98, 1.0, 1), rough=0.4)
    M["dark"] = _m("k_dark", (0.16, 0.17, 0.20, 1))
    M["ink"] = _m("k_ink", (0.10, 0.11, 0.14, 1))
    M["blue"] = _m("k_blue", (0.16, 0.38, 0.85, 1))
    M["teal"] = _m("k_teal", (0.06, 0.55, 0.60, 1))
    M["green"] = _m("k_green", (0.15, 0.62, 0.30, 1))
    M["orange"] = _m("k_orange", (0.92, 0.52, 0.10, 1))
    M["red"] = _m("k_red", (0.85, 0.18, 0.14, 1))
    M["purple"] = _m("k_purple", (0.55, 0.25, 0.80, 1))
    M["yellow"] = _m("k_yellow", (0.95, 0.80, 0.15, 1))
    M["cyan"] = _m("k_cyan", (0.05, 0.75, 0.85, 1))
    M["gray"] = _m("k_gray", (0.55, 0.57, 0.60, 1))
    M["lgray"] = _m("k_lgray", (0.82, 0.84, 0.88, 1))
    M["floor"] = _m("k_floor", (0.90, 0.91, 0.94, 1), rough=0.8)
    M["floor2"] = _m("k_floor2", (0.85, 0.87, 0.91, 1), rough=0.8)
    M["road"] = _m("k_road", (0.30, 0.31, 0.34, 1), rough=0.9)
    M["skin"] = _m("k_skin", (0.87, 0.66, 0.52, 1))
    return M


# ---------------------------------------------------------------- text
def label(name, text, size, loc, color=None, rot=None, align="CENTER", col_target=None,
          font=None, extrude=0.004):
    mats()
    col_target = col_target or CURRENT_STAGE
    m = color if isinstance(color, type(bpy.data.materials)) else (M.get(color or "ink"))
    t = C.text3d(name, text, size, loc=loc, rot=rot, m=m, align=align, col_target=col_target,
                 extrude=extrude)
    fnt = font or (FONT_HI if FONT_HI else FONT_EN)
    if fnt:
        t.data.font = fnt
    return t


def label_y(name, text, size, loc, color=None, col_target=None, font=None):
    """Text standing upright, readable from -Y camera."""
    return label(name, text, size, loc, color=color,
                 rot=(math.radians(90), 0, 0), col_target=col_target, font=font)


# ---------------------------------------------------------------- structures
def node(name, size, loc, color="blue", label_text=None, label_size=0.11,
         label_color=None, col_target=None, z=0.0):
    """Floating rounded panel node with optional label on front (-Y)."""
    mats()
    col_target = col_target or CURRENT_STAGE
    m = M.get(color, M["blue"])
    b = C.box(name, (size[0], 0.06, size[1]), loc=(loc[0], loc[1], loc[2] + z), m=m,
              bevel=0.025, col_target=col_target)
    objs = [b]
    if label_text:
        t = label_y(name + "_lbl", label_text, label_size,
                    (loc[0], loc[1] - 0.041, loc[2] + z), color=label_color or "white",
                    col_target=col_target)
        objs.append(t)
    return objs


def chip_row(name, texts, x0, y, z, gap, color, label_size=0.09, col_target=None):
    objs = []
    for i, txt in enumerate(texts):
        w = max(0.16, 0.075 * len(txt) ** 0.92)
        objs += node("%s_%d" % (name, i), (w, 0.16), (x0 + i * gap, y, z), color,
                     label_text=txt, label_size=label_size, col_target=col_target)
    return objs


def floor_pad(name, w, d, loc=(0, 0, 0), col_target=None, color="floor"):
    mats()
    return C.box(name, (w, d, 0.06), loc=(loc[0], loc[1], loc[2] - 0.03), m=M[color],
                 bevel=0.03, col_target=col_target)


def arrow(name, p0, p1, r=0.016, color="gray", col_target=None, head=0.07):
    """Straight arrow from p0 to p1 (world local to stage)."""
    mats()
    col_target = col_target or CURRENT_STAGE
    m = M.get(color, M["gray"])
    p0, p1 = Vector(p0), Vector(p1)
    d = p1 - p0
    L = d.length
    if L < 1e-6:
        return []
    dirn = d.normalized()
    shaft_L = max(0.01, L - head)
    mid = p0 + dirn * (shaft_L / 2)
    shaft = C.cyl(name + "_shaft", r, shaft_L, loc=tuple(mid),
                  rot=dirn.to_track_quat("Z", "Y").to_euler(), m=m, verts=12,
                  col_target=col_target)
    tip_loc = p0 + dirn * (shaft_L + head / 2)
    tip = C.cone(name + "_tip", r * 2.4, 0.001, head, loc=tuple(tip_loc),
                 rot=dirn.to_track_quat("Z", "Y").to_euler(), m=m, verts=12,
                 col_target=col_target)
    return [shaft, tip]


def line3d(name, p0, p1, r=0.008, color="gray", col_target=None):
    mats()
    col_target = col_target or CURRENT_STAGE
    m = M.get(color, M["gray"])
    p0, p1 = Vector(p0), Vector(p1)
    d = p1 - p0
    L = d.length
    if L < 1e-6:
        return []
    mid = (p0 + p1) / 2
    c = C.cyl(name, r, L, loc=tuple(mid), rot=d.normalized().to_track_quat("Z", "Y").to_euler(),
              m=m, verts=8, col_target=col_target)
    return [c]


def icon(name, kind, loc, color="blue", s=0.12, col_target=None):
    """Simple 3D icon glyphs. loc = center. Returns [objs]."""
    mats()
    col_target = col_target or CURRENT_STAGE
    m = M.get(color, M["blue"])
    x, y, z = loc
    objs = []
    if kind == "book":
        b1 = C.box(name + "_c1", (s, 0.03, s * 0.72), loc=(x - s * 0.18, y, z), rot=(0, math.radians(14), 0), m=m, col_target=col_target)
        b2 = C.box(name + "_c2", (s, 0.03, s * 0.72), loc=(x + s * 0.18, y, z), rot=(0, math.radians(-14), 0), m=m, col_target=col_target)
        objs = [b1, b2]
    elif kind == "gear":
        g = C.cyl(name + "_g", s * 0.55, s * 0.28, loc=(x, y, z), rot=(math.radians(90), 0, 0), m=m, verts=16, col_target=col_target)
        objs = [g]
        for i in range(6):
            a = i * math.pi / 3
            t_ = C.box(name + "_t%d" % i, (s * 0.22, s * 0.26, s * 0.22),
                       loc=(x + s * 0.62 * math.cos(a), y, z + s * 0.62 * math.sin(a)),
                       rot=(0, 0, a), m=m, col_target=col_target)
            objs.append(t_)
    elif kind == "brain":
        b = C.sphere(name + "_b", s * 0.55, loc=(x, y, z), m=m, segs=16, rings=12, col_target=col_target)
        objs = [b]
    elif kind == "chat":
        c1 = C.box(name + "_c", (s, 0.05, s * 0.62), loc=(x, y, z), m=m, bevel=s * 0.14, col_target=col_target)
        tail = C.cone(name + "_t", s * 0.14, 0.001, s * 0.22, loc=(x - s * 0.22, y, z - s * 0.38),
                      rot=(math.radians(-90), 0, 0), m=m, verts=10, col_target=col_target)
        objs = [c1, tail]
    elif kind == "magnifier":
        ring = C.torus(name + "_r", s * 0.4, s * 0.09, loc=(x + s * 0.1, y, z + s * 0.1), rot=(math.radians(90), 0, 0), m=m, col_target=col_target)
        handle = C.cyl(name + "_h", s * 0.07, s * 0.55, loc=(x - s * 0.28, y, z - s * 0.28),
                       rot=(0, math.radians(45), 0), m=m, verts=8, col_target=col_target)
        objs = [ring, handle]
    elif kind == "db":
        c1 = C.cyl(name + "_c1", s * 0.5, s * 0.3, loc=(x, y, z + s * 0.3), m=m, verts=16, col_target=col_target)
        c2 = C.cyl(name + "_c2", s * 0.5, s * 0.3, loc=(x, y, z), m=m, verts=16, col_target=col_target)
        c3 = C.cyl(name + "_c3", s * 0.5, s * 0.3, loc=(x, y, z - s * 0.3), m=m, verts=16, col_target=col_target)
        objs = [c1, c2, c3]
    elif kind == "camera":
        b = C.box(name + "_b", (s, s * 0.4, s * 0.7), loc=(x, y, z), m=m, bevel=s * 0.08, col_target=col_target)
        lens = C.cyl(name + "_l", s * 0.2, s * 0.12, loc=(x, y - s * 0.25, z), rot=(math.radians(90), 0, 0), m=M["dark"], verts=14, col_target=col_target)
        objs = [b, lens]
    elif kind == "code":
        t1 = label_y(name + "_t", "</>", s * 1.4, (x, y, z), color=None, col_target=col_target, font=FONT_EN)
        if t1:
            t1.data.materials.clear()
            t1.data.materials.append(m)
            t1.color = m.diffuse_color
        objs = [t1]
    elif kind == "question":
        q = label_y(name + "_q", "?", s * 2.2, (x, y, z), color=color, col_target=col_target, font=FONT_EN)
        objs = [q]
    elif kind == "check":
        ck = label_y(name + "_ck", "\u2713", s * 1.8, (x, y, z), color=color, col_target=col_target, font=FONT_EN)
        objs = [ck]
    elif kind == "cross":
        ck = label_y(name + "_cx", "\u2717", s * 1.8, (x, y, z), color=color, col_target=col_target, font=FONT_EN)
        objs = [ck]
    elif kind == "lock":
        b = C.box(name + "_b", (s * 0.8, s * 0.4, s * 0.6), loc=(x, y, z - s * 0.2), m=m, bevel=s * 0.08, col_target=col_target)
        ring = C.torus(name + "_r", s * 0.28, s * 0.07, loc=(x, y, z + s * 0.25), rot=(0, 0, 0), m=m, col_target=col_target)
        objs = [b, ring]
    elif kind == "clock":
        face = C.cyl(name + "_f", s * 0.55, s * 0.12, loc=(x, y, z), rot=(math.radians(90), 0, 0), m=m, verts=20, col_target=col_target)
        h1 = C.box(name + "_h1", (s * 0.06, s * 0.1, s * 0.4), loc=(x, y - s * 0.08, z + s * 0.16), m=M["white"], col_target=col_target)
        h2 = C.box(name + "_h2", (s * 0.32, s * 0.1, s * 0.05), loc=(x + s * 0.13, y - s * 0.08, z), m=M["white"], col_target=col_target)
        objs = [face, h1, h2]
    elif kind == "shield":
        b = C.box(name + "_b", (s, s * 0.18, s * 1.2), loc=(x, y, z), m=m, bevel=s * 0.12, col_target=col_target)
        objs = [b]
    elif kind == "globe":
        g = C.sphere(name + "_g", s * 0.55, loc=(x, y, z), m=m, segs=18, rings=12, col_target=col_target)
        ring = C.torus(name + "_r", s * 0.55, s * 0.03, loc=(x, y, z), rot=(math.radians(20), 0, math.radians(30)), m=M["lgray"], col_target=col_target)
        objs = [g, ring]
    elif kind == "memory":
        b1 = C.box(name + "_b1", (s, s * 0.3, s * 0.3), loc=(x, y, z + s * 0.34), m=m, bevel=s * 0.05, col_target=col_target)
        b2 = C.box(name + "_b2", (s, s * 0.3, s * 0.3), loc=(x, y, z), m=m, bevel=s * 0.05, col_target=col_target)
        b3 = C.box(name + "_b3", (s, s * 0.3, s * 0.3), loc=(x, y, z - s * 0.34), m=m, bevel=s * 0.05, col_target=col_target)
        objs = [b1, b2, b3]
    elif kind == "eye":
        e = C.sphere(name + "_e", s * 0.4, loc=(x, y, z), scale=(1.4, 0.5, 1.0), m=m, segs=16, rings=10, col_target=col_target)
        p = C.sphere(name + "_p", s * 0.18, loc=(x, y - s * 0.16, z), m=M["dark"], segs=12, rings=8, col_target=col_target)
        objs = [e, p]
    elif kind == "wrench":
        h = C.cyl(name + "_h", s * 0.1, s, loc=(x, y, z), rot=(0, math.radians(90), math.radians(45)), m=m, verts=10, col_target=col_target)
        ring = C.torus(name + "_r", s * 0.22, s * 0.08, loc=(x + s * 0.32, y, z + s * 0.32), m=m, col_target=col_target)
        objs = [h, ring]
    return objs


def glow_ring(name, r, loc, color="yellow", col_target=None, tube=0.012):
    mats()
    col_target = col_target or CURRENT_STAGE
    t = C.torus(name, r, tube, loc=loc, rot=(math.radians(90), 0, 0), m=M.get(color, M["yellow"]),
                col_target=col_target)
    return t


# ---------------------------------------------------------------- animation helpers
def pop_scale(objs, t_appear, t_full=None, max_s=1.0):
    """Scale 0.001 -> max_s pop at t_appear (no hide keys: scale-zero = invisible).
    Object stays at 0.001 for all frames before the pop (first key holds)."""
    t_full = t_full if t_full is not None else t_appear + 0.28
    f1, f2 = f(t_appear), f(t_full)
    for ob in objs:
        ob.scale = (0.001,) * 3
        ob.keyframe_insert("scale", frame=f1)
        ob.scale = (max_s,) * 3
        ob.keyframe_insert("scale", frame=f2)


def move(objs, t0, t1, dloc, ease="smooth"):
    """Move objs by dloc (delta) between t0..t1 (absolute world keyframes)."""
    fa, fb = f(t0), f(t1)
    for ob in objs:
        if ob.type == "EMPTY":
            continue
        p0 = Vector(ob.location)
        p1 = p0 + Vector(dloc)
        ob.location = p0
        ob.keyframe_insert("location", frame=fa)
        ob.location = p1
        ob.keyframe_insert("location", frame=fb)


def move_to(objs, t0, t1, loc_to, ease="smooth"):
    fa, fb = f(t0), f(t1)
    for ob in objs:
        if ob.type == "EMPTY":
            continue
        p0 = Vector(ob.location)
        p1 = Vector(loc_to) + (p0 - Vector(loc_to)) * 0  # placeholder
        ob.location = p0
        ob.keyframe_insert("location", frame=fa)
        ob.location = Vector(loc_to)
        ob.keyframe_insert("location", frame=fb)


def pivot_rot(pivot, t0, t1, euler_delta, ease="smooth"):
    """Rotate a pivot empty (parented children follow)."""
    fa, fb = f(t0), f(t1)
    e0 = Euler(pivot.rotation_euler)
    e1 = Euler((e0.x + euler_delta[0], e0.y + euler_delta[1], e0.z + euler_delta[2]))
    pivot.rotation_euler = e0
    pivot.keyframe_insert("rotation_euler", frame=fa)
    pivot.rotation_euler = e1
    pivot.keyframe_insert("rotation_euler", frame=fb)


def rise(objs, t0, t1, dz):
    move(objs, t0, t1, (0, 0, dz))


def fade_color(objs, t, rgba):
    for ob in objs:
        if ob.type in ("MESH", "FONT", "CURVE"):
            C.kf_color(ob, f(t), rgba)


def set_cam_kf(cam, t, loc, look_at, stage_off=(0, 0, 0)):
    """Hard-cut camera keyframe at time t (constant interpolation for cuts)."""
    fr = f(t)
    C.place_camera(cam, loc, look_at, stage_off)
    cam.keyframe_insert("location", frame=fr)
    cam.keyframe_insert("rotation_euler", frame=fr)


def cam_path(cam, t0, t1, loc0, loc1, look0, look1, stage_off=(0, 0, 0)):
    """Smooth camera move between t0..t1."""
    fa, fb = f(t0), f(t1)
    C.place_camera(cam, loc0, look0, stage_off)
    cam.keyframe_insert("location", frame=fa)
    cam.keyframe_insert("rotation_euler", frame=fa)
    # compute end rotation by placing then reading
    C.place_camera(cam, loc1, look1, stage_off)
    rot1 = tuple(cam.rotation_euler)
    cam.location = Vector(loc1) + Vector(stage_off)
    cam.keyframe_insert("location", frame=fb)
    cam.rotation_euler = rot1
    cam.keyframe_insert("rotation_euler", frame=fb)
