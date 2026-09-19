"""Surgeon scene assets (SKILL 12): surgeon, desk, medical books, instruments, calculator.

Educational flat-shaded style but real proportions and part structure.
Surgeon total height ~1.72m, standing at origin facing -Y.
"""
import math
import bpy
from mathutils import Vector
from . import common as C

SCRUB = COAT = SKIN = HAIR = SHOE = STEEL = DARKPLAST = None


def _mats():
    global SCRUB, COAT, SKIN, HAIR, SHOE, STEEL, DARKPLAST
    SCRUB = C.mat("scrub_teal", (0.10, 0.42, 0.42, 1), rough=0.75, spec=0.1)
    COAT = C.mat("coat_white", (0.92, 0.93, 0.95, 1), rough=0.7, spec=0.15)
    SKIN = C.mat("skin", (0.87, 0.66, 0.52, 1), rough=0.55, spec=0.25)
    HAIR = C.mat("hair", (0.16, 0.11, 0.08, 1), rough=0.7)
    SHOE = C.mat("shoe", (0.15, 0.15, 0.17, 1), rough=0.6)
    STEEL = C.mat("steel", (0.72, 0.74, 0.78, 1), spec=0.7, rough=0.25)
    DARKPLAST = C.mat("calc_dark", (0.13, 0.13, 0.15, 1), rough=0.5, spec=0.3)


def _pivot(name, loc, parent, target_col):
    e = bpy.data.objects.new(name, None)
    e.empty_display_type = "SPHERE"
    e.empty_display_size = 0.025
    e.location = loc
    target_col.objects.link(e)
    if parent is not None:
        C.parent_to(e, parent, keep_world=False)
    return e


def build_surgeon(target_col, name_prefix="surgeon", scrub_rgba=None, coat_rgba=None,
                  with_cap=True, coat=True):
    """Standing surgeon/student at origin, feet z=0, facing -Y. Returns pivots dict."""
    _mats()
    global SCRUB, COAT
    if scrub_rgba:
        SCRUB = C.mat(name_prefix + "_scrub", scrub_rgba, rough=0.75, spec=0.1)
    if coat_rgba:
        COAT = C.mat(name_prefix + "_coat", coat_rgba, rough=0.7, spec=0.15)
    piv = {"objects": []}
    objs = piv["objects"]

    root = _pivot(name_prefix + "_root", (0, 0, 0), None, target_col)
    piv["root"] = root

    # ---- legs
    for sx, sname in ((-1, "L"), (1, "R")):
        hip_p = _pivot("%s_hip_%s" % (name_prefix, sname), (sx * 0.09, 0, 0.86), root, target_col)
        piv["hip_%s" % sname] = hip_p
        thigh = C.cyl("%s_thigh_%s" % (name_prefix, sname), 0.065, 0.36,
                      loc=(0, 0, -0.19), m=SCRUB, verts=16, col_target=target_col)
        C.parent_to(thigh, hip_p, keep_world=False)
        knee_p = _pivot("%s_knee_%s" % (name_prefix, sname), (0, 0, -0.38), hip_p, target_col)
        piv["knee_%s" % sname] = knee_p
        shin = C.cyl("%s_shin_%s" % (name_prefix, sname), 0.052, 0.34,
                     loc=(0, 0, -0.18), m=SCRUB, verts=16, col_target=target_col)
        C.parent_to(shin, knee_p, keep_world=False)
        shoe = C.box("%s_shoe_%s" % (name_prefix, sname), (0.10, 0.24, 0.07),
                     loc=(0, -0.045, -0.385), m=SHOE, bevel=0.02, col_target=target_col)
        C.parent_to(shoe, knee_p, keep_world=False)
        objs += [thigh, shin, shoe]

    # ---- torso (scrub top, tapered: upper wider)
    chest = C.box(name_prefix + "_chest", (0.36, 0.20, 0.44), loc=(0, 0, 1.12), m=SCRUB,
                  bevel=0.05, col_target=target_col)
    C.parent_to(chest, root, keep_world=False)
    objs.append(chest)
    # white coat panels (front open coat: two side slabs)
    if coat:
        coatL = C.box(name_prefix + "_coatL", (0.10, 0.215, 0.50), loc=(-0.14, 0.005, -0.06),
                      m=COAT, bevel=0.02, col_target=target_col)
        coatR = C.box(name_prefix + "_coatR", (0.10, 0.215, 0.50), loc=(0.14, 0.005, -0.06),
                      m=COAT, bevel=0.02, col_target=target_col)
        C.parent_to(coatL, chest, keep_world=False)
        C.parent_to(coatR, chest, keep_world=False)
        objs += [coatL, coatR]

    # stethoscope around neck: torus + chestpiece
    if coat:
        sto_tube = C.torus(name_prefix + "_steth", 0.13, 0.012, loc=(0, 0.02, 0.18),
                           rot=(math.radians(75), 0, 0), m=C.mat("steth_dark", (0.12, 0.12, 0.14, 1), rough=0.6),
                           col_target=target_col)
        C.parent_to(sto_tube, chest, keep_world=False)
        sto_disc = C.cyl(name_prefix + "_stethDisc", 0.032, 0.014, loc=(0.09, -0.115, -0.17),
                         rot=(math.radians(90), 0, 0), m=STEEL, verts=20, col_target=target_col)
        C.parent_to(sto_disc, chest, keep_world=False)
        objs += [sto_tube, sto_disc]

    # ---- arms
    for sx, sname in ((-1, "L"), (1, "R")):
        sh_p = _pivot("%s_shoulder_%s" % (name_prefix, sname), (sx * 0.205, 0, 1.28), root, target_col)
        piv["shoulder_%s" % sname] = sh_p
        delt = C.sphere("%s_delt_%s" % (name_prefix, sname), 0.062, loc=(0, 0, 0), m=COAT,
                        segs=16, rings=12, col_target=target_col)
        C.parent_to(delt, sh_p, keep_world=False)
        upper = C.cyl("%s_upperarm_%s" % (name_prefix, sname), 0.048, 0.24,
                      loc=(0, 0, -0.13), m=COAT, verts=14, col_target=target_col)
        C.parent_to(upper, sh_p, keep_world=False)
        el_p = _pivot("%s_elbow_%s" % (name_prefix, sname), (0, 0, -0.26), sh_p, target_col)
        piv["elbow_%s" % sname] = el_p
        fore = C.cyl("%s_forearm_%s" % (name_prefix, sname), 0.042, 0.22,
                     loc=(0, 0, -0.12), m=SCRUB, verts=14, col_target=target_col)
        C.parent_to(fore, el_p, keep_world=False)
        wr_p = _pivot("%s_wrist_%s" % (name_prefix, sname), (0, 0, -0.24), el_p, target_col)
        piv["wrist_%s" % sname] = wr_p
        palm = C.box("%s_palm_%s" % (name_prefix, sname), (0.075, 0.03, 0.085),
                     loc=(0, 0, -0.045), m=SKIN, bevel=0.012, col_target=target_col)
        C.parent_to(palm, wr_p, keep_world=False)
        thumb = C.box("%s_thumb_%s" % (name_prefix, sname), (0.02, 0.025, 0.04),
                      loc=(sx * -0.045, -0.008, -0.025), rot=(0, math.radians(sx * 30), 0),
                      m=SKIN, bevel=0.006, col_target=target_col)
        C.parent_to(thumb, wr_p, keep_world=False)
        objs += [delt, upper, fore, palm, thumb]

    # ---- neck & head
    neck = C.cyl(name_prefix + "_neck", 0.042, 0.09, loc=(0, 0, 1.39), m=SKIN, verts=14,
                 col_target=target_col)
    C.parent_to(neck, root, keep_world=False)
    head = C.sphere(name_prefix + "_head", 0.105, loc=(0, 0, 1.50), m=SKIN, segs=24, rings=18,
                    col_target=target_col, scale=(0.92, 1.0, 1.06))
    C.parent_to(head, root, keep_world=False)
    objs += [neck, head]
    # hair cap (back hemisphere)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.108, segments=20, ring_count=14,
                                         location=(0, 0.008, 0.015))
    hair = bpy.context.object
    hair.name = name_prefix + "_hair"
    me = hair.data
    for v in me.vertices:
        if v.co.y < -0.005:  # cut face area
            v.co.z = -0.02 if v.co.y < -0.06 else v.co.z
            v.co.y = max(v.co.y, -0.004) if v.co.z < 0.02 else v.co.y
    C.apply_mat(hair, HAIR)
    C.ob_color(hair, HAIR.diffuse_color)
    bpy.ops.object.shade_smooth()
    C.parent_to(hair, head, keep_world=False)
    C.link_to(hair, target_col)
    objs.append(hair)
    # surgical cap
    if with_cap:
        cap = C.sphere(name_prefix + "_cap", 0.104, loc=(0, 0.012, 0.03), m=SCRUB, segs=20, rings=14,
                       col_target=target_col, scale=(0.96, 0.95, 0.8))
        C.parent_to(cap, head, keep_world=False)
        objs.append(cap)
    # nose
    nose = C.cone(name_prefix + "_nose", 0.016, 0.004, 0.035, loc=(0, -0.105, -0.015),
                  rot=(math.radians(-95), 0, 0), m=SKIN, verts=10, col_target=target_col)
    C.parent_to(nose, head, keep_world=False)
    objs.append(nose)
    # eyes
    for sx, sname in ((-1, "L"), (1, "R")):
        eye = C.sphere("%s_eye_%s" % (name_prefix, sname), 0.011,
                       loc=(sx * 0.038, -0.094, 0.015), m=C.mat("eye_dark", (0.06, 0.05, 0.05, 1)),
                       segs=12, rings=8, col_target=target_col)
        C.parent_to(eye, head, keep_world=False)
        objs.append(eye)
    # ears
    for sx, sname in ((-1, "L"), (1, "R")):
        ear = C.sphere("%s_ear_%s" % (name_prefix, sname), 0.018,
                       loc=(sx * 0.098, 0, 0.0), m=SKIN, segs=10, rings=8, col_target=target_col)
        C.parent_to(ear, head, keep_world=False)
        objs.append(ear)
    # mouth
    mouth = C.box(name_prefix + "_mouth", (0.035, 0.01, 0.006), loc=(0, -0.10, -0.045),
                  m=C.mat("mouth", (0.55, 0.28, 0.25, 1)), col_target=target_col)
    C.parent_to(mouth, head, keep_world=False)
    objs.append(mouth)

    return piv


def build_desk(target_col, name="desk", w=1.9, d=0.85, h=0.76):
    """Office desk: top, two panel legs, back modesty panel."""
    desk_m = C.mat("desk_wood", (0.55, 0.38, 0.24, 1), rough=0.6, spec=0.2)
    panel_m = C.mat("desk_panel", (0.42, 0.28, 0.18, 1), rough=0.6)
    top = C.box(name + "_top", (w, d, 0.04), loc=(0, 0, h), m=desk_m, bevel=0.008,
                col_target=target_col)
    pl = C.box(name + "_panelL", (0.03, d - 0.10, h - 0.05), loc=(-w / 2 + 0.06, 0, (h - 0.04) / 2),
               m=panel_m, col_target=target_col)
    pr = C.box(name + "_panelR", (0.03, d - 0.10, h - 0.05), loc=(w / 2 - 0.06, 0, (h - 0.04) / 2),
               m=panel_m, col_target=target_col)
    back = C.box(name + "_back", (w - 0.16, 0.025, h * 0.55), loc=(0, d / 2 - 0.05, h * 0.52),
                 m=panel_m, col_target=target_col)
    return [top, pl, pr, back]


def build_calculator(target_col, name="calc", w=0.16, d=0.24, h=0.022):
    """Desk calculator: body, screen bezel + display, 4x5 button grid."""
    body_m = C.mat("calc_body", (0.30, 0.31, 0.34, 1), rough=0.5, spec=0.3)
    screen_m = C.mat("calc_screen", (0.55, 0.72, 0.52, 1), spec=0.6, rough=0.2)
    btn_m = C.mat("calc_btn", (0.62, 0.63, 0.66, 1), rough=0.45, spec=0.35)
    btn_fn = C.mat("calc_btnFn", (0.85, 0.62, 0.15, 1), rough=0.45)

    body = C.box(name + "_body", (w, d, h), loc=(0, 0, h / 2), m=body_m, bevel=0.004,
                 col_target=target_col)
    bezel = C.box(name + "_bezel", (w * 0.86, d * 0.30, 0.006), loc=(0, d * 0.30, h),
                  m=DARKPLAST, col_target=target_col)
    screen = C.box(name + "_screen", (w * 0.74, d * 0.22, 0.004), loc=(0, d * 0.30, h + 0.004),
                   m=screen_m, col_target=target_col)
    objs = [body, bezel, screen]
    # buttons 4 cols x 5 rows
    for r_ in range(5):
        for c_ in range(4):
            x = -w * 0.30 + c_ * (w * 0.20)
            y = d * 0.06 - r_ * (d * 0.115)
            mm = btn_fn if (r_ == 4 and c_ in (0, 3)) else btn_m
            b = C.box("%s_btn_%d%d" % (name, r_, c_), (w * 0.15, d * 0.08, 0.008),
                      loc=(x, y, h + 0.004), m=mm, bevel=0.002, col_target=target_col)
            objs.append(b)
    return objs


def build_stethoscope(target_col, name="steth", tray_y=0.0):
    """Coiled stethoscope lying flat: torus arc tube + Y-tubes + chestpiece."""
    dark = C.mat("steth_dark2", (0.12, 0.12, 0.14, 1), rough=0.6)
    objs = []
    main = C.torus(name + "_loop", 0.10, 0.010, loc=(0, tray_y, 0.012),
                   rot=(0, 0, 0), m=dark, col_target=target_col)
    objs.append(main)
    head_disc = C.cyl(name + "_disc", 0.032, 0.014, loc=(0.115, tray_y, 0.010), m=STEEL,
                      verts=20, col_target=target_col)
    objs.append(head_disc)
    ear_tubes = []
    for sx in (-1, 1):
        t = C.cyl(name + "_earTube", 0.008, 0.14, loc=(sx * 0.05, tray_y + 0.10, 0.010),
                  rot=(0, math.radians(90), math.radians(sx * 20)), m=dark, verts=10,
                  col_target=target_col)
        ear_tubes.append(t)
    objs += ear_tubes
    return objs


def build_scalpel(target_col, name="scalpel"):
    handle_m = C.mat("scalpel_handle", (0.85, 0.86, 0.88, 1), spec=0.6, rough=0.3)
    blade_m = C.mat("scalpel_blade", (0.92, 0.94, 0.97, 1), spec=0.8, rough=0.15)
    handle = C.box(name + "_handle", (0.018, 0.11, 0.008), loc=(0, 0, 0.008), m=handle_m,
                   bevel=0.003, col_target=target_col)
    blade = C.cone(name + "_blade", 0.009, 0.0008, 0.045, loc=(0, -0.075, 0.008),
                   rot=(0, 0, math.radians(-90)), m=blade_m, verts=12, col_target=target_col)
    blade.rotation_euler = (math.radians(90), 0, 0)
    blade.location = (0, -0.072, 0.009)
    return [handle, blade]


def build_syringe(target_col, name="syringe"):
    barrel_m = C.mat("syringe_barrel", (0.85, 0.90, 0.92, 1), spec=0.4, rough=0.2)
    plunger_m = C.mat("syringe_plunger", (0.25, 0.28, 0.32, 1), rough=0.5)
    needle_m = C.mat("syringe_needle", (0.90, 0.92, 0.95, 1), spec=0.8, rough=0.15)
    barrel = C.cyl(name + "_barrel", 0.011, 0.09, loc=(0, 0, 0.014),
                   rot=(0, math.radians(90), 0), m=barrel_m, verts=18, col_target=target_col)
    plunger = C.cyl(name + "_plunger", 0.004, 0.07, loc=(0.065, 0, 0.014),
                    rot=(0, math.radians(90), 0), m=plunger_m, verts=10, col_target=target_col)
    flange = C.box(name + "_flange", (0.006, 0.032, 0.032), loc=(-0.046, 0, 0.014), m=barrel_m,
                   col_target=target_col)
    needle = C.cyl(name + "_needle", 0.0012, 0.035, loc=(-0.062, 0, 0.014),
                   rot=(0, math.radians(90), 0), m=needle_m, verts=8, col_target=target_col)
    return [barrel, plunger, flange, needle]
