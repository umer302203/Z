"""Props: apple (SKILL 23), wooden table (SKILL 24), book, cup, tray."""
import math
import bpy
from mathutils import Vector
from . import common as C


def build_apple(target_col, name="apple", r=0.055):
    """Organic apple: asymmetric body, top depression, stem. Sits with bottom at z=0."""
    skin = C.mat("apple_skin", (0.72, 0.10, 0.08, 1), spec=0.55, rough=0.35)
    stem_m = C.mat("apple_stem", (0.30, 0.19, 0.10, 1), rough=0.7)

    bpy.ops.mesh.primitive_uv_sphere_add(radius=r, segments=28, ring_count=20,
                                         location=(0, 0, r * 0.92))
    ob = bpy.context.object
    ob.name = name
    # organic asymmetry: scale + slight lobe deformation via vertex displacement
    me = ob.data
    for v in me.vertices:
        n = v.co.copy()
        n.normalize()
        # squash bottom, dimple top
        if v.co.z > r * 0.75:
            v.co.z -= (v.co.z - r * 0.75) * 0.55          # upper depression
        if v.co.z < -r * 0.6:
            v.co.z *= 0.82                                 # lower indentation
        # subtle lobes
        ang = math.atan2(v.co.y, v.co.x)
        v.co.x += 0.012 * r * math.cos(2 * ang) * (v.co.z / r)
        v.co.y += 0.012 * r * math.sin(2 * ang) * (v.co.z / r)
        # overall slight non-uniform scale
        v.co.x *= 1.04
        v.co.y *= 0.97
    C.apply_mat(ob, skin)
    C.ob_color(ob, skin.diffuse_color)
    bpy.ops.object.shade_smooth()
    C.link_to(ob, target_col)

    stem = C.cyl(name + "_stem", 0.004, 0.035, loc=(0, 0, r * 0.95 + 0.012),
                 rot=(math.radians(8), math.radians(6), 0), m=stem_m, verts=8,
                 col_target=target_col)
    return ob


def build_table(target_col, name="table", w=1.5, d=0.8, h=0.74):
    """Rectangular wooden table: top + apron + 4 inset square legs. Feet at z=0."""
    wood = C.mat("wood_mid", (0.45, 0.28, 0.15, 1), rough=0.65, spec=0.2)
    wood_dark = C.mat("wood_dark", (0.34, 0.20, 0.11, 1), rough=0.65, spec=0.2)
    top = C.box(name + "_top", (w, d, 0.045), loc=(0, 0, h), m=wood, bevel=0.008,
                col_target=target_col)
    apron = C.box(name + "_apron", (w - 0.12, d - 0.12, 0.07), loc=(0, 0, h - 0.055),
                  m=wood_dark, col_target=target_col)
    legs = []
    lx, ly = w / 2 - 0.09, d / 2 - 0.09
    for sx in (-1, 1):
        for sy in (-1, 1):
            lg = C.box("%s_leg_%d%d" % (name, sx, sy), (0.055, 0.055, h - 0.045),
                       loc=(sx * lx, sy * ly, (h - 0.045) / 2), m=wood_dark, bevel=0.006,
                       col_target=target_col)
            legs.append(lg)
    return [top, apron] + legs


def build_book(target_col, name="book", w=0.24, d=0.32, t=0.05, cover_rgba=(0.10, 0.15, 0.35, 1),
               title=None):
    """Hardcover: cover boards + spine + page block slightly inset. Spine along -X? Spine at back edge (-Y)."""
    cover = C.mat(name + "_cover", cover_rgba, rough=0.5, spec=0.3)
    paper = C.mat(name + "_paper", (0.93, 0.90, 0.82, 1), rough=0.8, spec=0.05)
    spine_m = C.mat(name + "_spine", tuple(c * 0.72 for c in cover_rgba[:3]) + (1,), rough=0.5)
    objs = []
    # page block
    pg = C.box(name + "_pages", (w - 0.008, d - 0.02, t - 0.008), loc=(0, -0.002, 0), m=paper,
               col_target=target_col)
    # front/back covers (slightly bigger)
    fc = C.box(name + "_coverF", (w, d, t * 0.30), loc=(0, 0, (t - t * 0.30) / 2), m=cover,
               bevel=0.006, col_target=target_col)
    bc = C.box(name + "_coverB", (w, d, t * 0.30), loc=(0, 0, -(t - t * 0.30) / 2), m=cover,
               bevel=0.006, col_target=target_col)
    # spine (wraps -Y edge)
    sp = C.box(name + "_spine", (w, 0.024, t + 0.004), loc=(0, -(d / 2) + 0.006, 0), m=spine_m,
               bevel=0.008, col_target=target_col)
    objs += [pg, fc, bc, sp]
    if title:
        tm = C.mat(name + "_title", (0.92, 0.88, 0.70, 1))
        t3 = C.text3d(name + "_titleTxt", title, w * 0.11,
                      loc=(0, -(d / 2) - 0.004, 0), rot=(math.radians(90), 0, 0), m=tm,
                      col_target=target_col)
        t3.rotation_euler = (math.radians(90), 0, math.radians(180))
        t3.location = (0, -(d / 2) - 0.005, t * 0.28)
        objs.append(t3)
    return objs


def build_cup(target_col, name="cup", r=0.042, h=0.10):
    ceramic = C.mat("cup_white", (0.90, 0.89, 0.86, 1), rough=0.35, spec=0.4)
    body = C.cyl(name + "_body", r, h, loc=(0, 0, h / 2), m=ceramic, verts=28, col_target=target_col)
    inner = C.cyl(name + "_inner", r * 0.82, h * 0.5, loc=(0, 0, h * 0.72),
                  m=C.mat("cup_inner", (0.75, 0.73, 0.70, 1)), verts=24, col_target=target_col)
    handle = C.torus(name + "_handle", r * 0.55, 0.008, loc=(r + 0.012, 0, h * 0.55),
                     rot=(0, math.radians(90), 0), m=ceramic, col_target=target_col)
    return [body, inner, handle]


def build_tray(target_col, name="tray", w=0.42, d=0.30):
    steel = C.mat("steel", (0.72, 0.74, 0.78, 1), spec=0.7, rough=0.25)
    base = C.box(name + "_base", (w, d, 0.012), loc=(0, 0, 0.006), m=steel, col_target=target_col)
    rims = []
    for sx, sy, sw, sd, dx, dy in (
        (0, -d / 2 + 0.008, w, 0.014, 0, 0),
        (0, d / 2 - 0.008, w, 0.014, 0, 0),
        (-w / 2 + 0.008, 0, 0.014, d - 0.02, 0, 0),
        (w / 2 - 0.008, 0, 0.014, d - 0.02, 0, 0),
    ):
        r = C.box(name + "_rim", (sw, sd, 0.03), loc=(dx, dy, 0.018), m=steel, col_target=target_col)
        rims.append(r)
    return [base] + rims
