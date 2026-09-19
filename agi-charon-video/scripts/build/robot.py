"""Humanoid robot builder v2 (SKILL 15-22).

All children authored in PARENT-LOCAL coordinates via C.parent_to(..., keep_world=False)
-> pivot rotations always orbit the true joint center.

Height ~1.73m, feet exactly on z=0, facing -Y.
"""
import math
import bpy
from mathutils import Vector
from . import common as C

SHELL = DARK = JOINT = CYAN = HAND = FOOT = None


def _mats():
    global SHELL, DARK, JOINT, CYAN, HAND, FOOT
    SHELL = C.mat("robot_shell", (0.84, 0.86, 0.89, 1), spec=0.5, rough=0.35)
    DARK = C.mat("robot_dark", (0.10, 0.11, 0.13, 1), spec=0.35, rough=0.5)
    JOINT = C.mat("robot_joint", (0.25, 0.26, 0.28, 1), spec=0.4, rough=0.45)
    CYAN = C.mat("robot_cyan", (0.05, 0.85, 0.95, 1), spec=0.7, rough=0.2)
    HAND = C.mat("robot_hand", (0.32, 0.33, 0.36, 1), spec=0.3, rough=0.55)
    FOOT = C.mat("robot_foot", (0.18, 0.19, 0.21, 1), spec=0.3, rough=0.5)


def _pivot(name, loc, parent, target_col):
    e = bpy.data.objects.new(name, None)
    e.empty_display_type = "SPHERE"
    e.empty_display_size = 0.03
    e.location = loc
    target_col.objects.link(e)
    if parent is not None:
        C.parent_to(e, parent, keep_world=False)
    return e


def _capsule_arm(name, length, r, m, target_col):
    """Arm segment along -Z from its pivot: local coords."""
    parts = []
    c = C.cyl(name + "_seg", r, length, loc=(0, 0, -length / 2), m=m, col_target=target_col)
    s0 = C.sphere(name + "_capTop", r, loc=(0, 0, -0.004), m=m, segs=16, rings=12, col_target=target_col)
    s1 = C.sphere(name + "_capBot", r, loc=(0, 0, -length), m=m, segs=16, rings=12, col_target=target_col)
    parts += [c, s0, s1]
    return parts


def _hand(side, wrist_pivot, target_col):
    """Palm + 4 fingers (2 segments each) + thumb, along -Z (local to wrist)."""
    parts = []
    palm = C.box("hand_%s_palm" % side, (0.10, 0.04, 0.11), loc=(0, 0, -0.052),
                 m=HAND, bevel=0.014, col_target=target_col)
    C.parent_to(palm, wrist_pivot, keep_world=False)
    parts.append(palm)
    fingers = []
    for i in range(4):
        x = -0.036 + i * 0.024
        knuckle = _pivot("f%d_%s_kn" % (i, side), (x, 0, -0.108), wrist_pivot, target_col)
        seg1 = C.box("f%d_%s_s1" % (i, side), (0.021, 0.03, 0.05),
                     loc=(0, 0, -0.025), m=HAND, bevel=0.007, col_target=target_col)
        C.parent_to(seg1, knuckle, keep_world=False)
        mid = _pivot("f%d_%s_mid" % (i, side), (0, 0, -0.05), knuckle, target_col)
        seg2 = C.box("f%d_%s_s2" % (i, side), (0.019, 0.027, 0.042),
                     loc=(0, 0, -0.021), m=HAND, bevel=0.006, col_target=target_col)
        C.parent_to(seg2, mid, keep_world=False)
        parts += [seg1, seg2]
        fingers.append((knuckle, mid))
    thumb_p = _pivot("thumb_%s_p" % side, (-0.052 if side == "L" else 0.052, -0.012, -0.032),
                     wrist_pivot, target_col)
    thumb_p.rotation_euler = (0, math.radians(-38 if side == "L" else 38),
                              math.radians(28 if side == "L" else -28))
    tseg1 = C.box("thumb_%s_s1" % side, (0.022, 0.03, 0.048), loc=(0, 0, -0.024), m=HAND,
                  bevel=0.007, col_target=target_col)
    C.parent_to(tseg1, thumb_p, keep_world=False)
    parts.append(tseg1)
    return parts, fingers, thumb_p


def build_robot(target_col, name_prefix="robot"):
    """Build robot at origin (feet z=0), facing -Y."""
    _mats()
    objs = []
    pivots = {}

    root = _pivot(name_prefix + "_root", (0, 0, 0), None, target_col)

    # pelvis / waist / chest
    pelvis = C.box(name_prefix + "_pelvis", (0.30, 0.20, 0.14), loc=(0, 0, 0.845), m=DARK,
                   bevel=0.03, col_target=target_col)
    C.parent_to(pelvis, root, keep_world=False)
    waist = C.cyl(name_prefix + "_waist", 0.085, 0.10, loc=(0, 0, 0.965), m=JOINT, verts=20,
                  col_target=target_col)
    C.parent_to(waist, root, keep_world=False)
    chest = C.box(name_prefix + "_chest", (0.40, 0.24, 0.38), loc=(0, 0, 1.23), m=SHELL,
                  bevel=0.055, col_target=target_col)
    C.parent_to(chest, root, keep_world=False)
    objs += [pelvis, waist, chest]

    chest_panel = C.box(name_prefix + "_chestPanel", (0.28, 0.02, 0.24), loc=(0, -0.125, 0.02),
                        m=DARK, bevel=0.015, col_target=target_col)
    C.parent_to(chest_panel, chest, keep_world=False)
    core = C.cyl(name_prefix + "_chestCore", 0.05, 0.032, loc=(0, -0.148, 0.02),
                 rot=(math.radians(90), 0, 0), m=CYAN, verts=20, col_target=target_col)
    C.parent_to(core, chest, keep_world=False)
    objs += [chest_panel, core]
    for i in range(3):
        for sx in (-1, 1):
            v = C.box(name_prefix + "_vent", (0.02, 0.19, 0.022),
                      loc=(sx * 0.205, 0, 0.10 - i * 0.05), m=DARK, col_target=target_col)
            C.parent_to(v, chest, keep_world=False)

    # neck & head
    neck_p = _pivot(name_prefix + "_neck", (0, 0, 1.44), root, target_col)
    pivots["neck"] = neck_p
    neck = C.cyl(name_prefix + "_neckSeg", 0.045, 0.08, loc=(0, 0, 0.03), m=JOINT, verts=16,
                 col_target=target_col)
    C.parent_to(neck, neck_p, keep_world=False)
    head = C.box(name_prefix + "_head", (0.26, 0.24, 0.22), loc=(0, 0, 0.18), m=SHELL,
                 bevel=0.055, col_target=target_col)
    C.parent_to(head, neck_p, keep_world=False)
    face = C.box(name_prefix + "_face", (0.21, 0.02, 0.15), loc=(0, -0.115, 0.005), m=DARK,
                 bevel=0.02, col_target=target_col)
    C.parent_to(face, head, keep_world=False)
    eyes = []
    for sx, sname in ((-1, "L"), (1, "R")):
        housing = C.cyl(name_prefix + "_eyeHousing_%s" % sname, 0.030, 0.018,
                        loc=(sx * 0.052, -0.012, 0.028), rot=(math.radians(90), 0, 0),
                        m=DARK, verts=20, col_target=target_col)
        C.parent_to(housing, face, keep_world=False)
        lens = C.cyl(name_prefix + "_eyeLens_%s" % sname, 0.019, 0.012,
                     loc=(sx * 0.052, -0.024, 0.028), rot=(math.radians(90), 0, 0),
                     m=CYAN, verts=18, col_target=target_col)
        C.parent_to(lens, face, keep_world=False)
        eyes.append(lens)
    for sx, sname in ((-1, "L"), (1, "R")):
        ear = C.cyl(name_prefix + "_ear_%s" % sname, 0.032, 0.02,
                    loc=(sx * 0.138, 0, 0.005), rot=(0, math.radians(90), 0), m=JOINT,
                    verts=16, col_target=target_col)
        C.parent_to(ear, head, keep_world=False)
    antenna = C.cyl(name_prefix + "_antenna", 0.006, 0.05, loc=(0, 0.07, 0.13), m=JOINT,
                    verts=10, col_target=target_col)
    C.parent_to(antenna, head, keep_world=False)
    ant_tip = C.sphere(name_prefix + "_antennaTip", 0.014, loc=(0, 0.07, 0.168), m=CYAN,
                       segs=12, rings=8, col_target=target_col)
    C.parent_to(ant_tip, antenna, keep_world=False)
    objs += [neck, head, face, antenna, ant_tip] + eyes

    # arms
    for sx, sname in ((-1, "L"), (1, "R")):
        sh_p = _pivot(name_prefix + "_shoulder_%s" % sname, (sx * 0.235, 0, 1.40), root, target_col)
        pivots["shoulder_%s" % sname] = sh_p
        sh_h = C.sphere(name_prefix + "_shoulderHousing_%s" % sname, 0.075, loc=(0, 0, 0),
                        m=SHELL, segs=18, rings=12, col_target=target_col)
        C.parent_to(sh_h, sh_p, keep_world=False)
        up = _capsule_arm(name_prefix + "_upperarm_%s" % sname, 0.26, 0.052, SHELL, target_col)
        for p in up:
            C.parent_to(p, sh_p, keep_world=False)
        el_p = _pivot(name_prefix + "_elbow_%s" % sname, (0, 0, -0.28), sh_p, target_col)
        pivots["elbow_%s" % sname] = el_p
        el = C.sphere(name_prefix + "_elbowJoint_%s" % sname, 0.062, loc=(0, 0, 0), m=JOINT,
                      segs=16, rings=12, col_target=target_col)
        C.parent_to(el, el_p, keep_world=False)
        fo = _capsule_arm(name_prefix + "_forearm_%s" % sname, 0.24, 0.046, SHELL, target_col)
        for p in fo:
            C.parent_to(p, el_p, keep_world=False)
        wr_p = _pivot(name_prefix + "_wrist_%s" % sname, (0, 0, -0.26), el_p, target_col)
        pivots["wrist_%s" % sname] = wr_p
        wr = C.cyl(name_prefix + "_wristJoint_%s" % sname, 0.040, 0.03, loc=(0, 0, 0), m=JOINT,
                   verts=16, col_target=target_col)
        C.parent_to(wr, wr_p, keep_world=False)
        hand_parts, fingers, thumb = _hand(sname, wr_p, target_col)
        objs += hand_parts
        pivots["hand_%s" % sname] = wr_p
        pivots["fingers_%s" % sname] = fingers
        pivots["thumb_%s" % sname] = thumb

    # legs
    for sx, sname in ((-1, "L"), (1, "R")):
        hip_p = _pivot(name_prefix + "_hip_%s" % sname, (sx * 0.105, 0, 0.79), root, target_col)
        pivots["hip_%s" % sname] = hip_p
        hip_h = C.sphere(name_prefix + "_hipHousing_%s" % sname, 0.075, loc=(0, 0, 0), m=SHELL,
                         segs=18, rings=12, col_target=target_col)
        C.parent_to(hip_h, hip_p, keep_world=False)
        thigh = C.cyl(name_prefix + "_thigh_%s" % sname, 0.062, 0.28, loc=(0, 0, -0.16), m=SHELL,
                      verts=18, col_target=target_col)
        C.parent_to(thigh, hip_p, keep_world=False)
        knee_p = _pivot(name_prefix + "_knee_%s" % sname, (0, 0, -0.34), hip_p, target_col)
        pivots["knee_%s" % sname] = knee_p
        knee = C.sphere(name_prefix + "_kneeJoint_%s" % sname, 0.068, loc=(0, 0, 0), m=JOINT,
                        segs=16, rings=12, col_target=target_col)
        C.parent_to(knee, knee_p, keep_world=False)
        shin = C.cyl(name_prefix + "_shin_%s" % sname, 0.052, 0.28, loc=(0, 0, -0.17), m=SHELL,
                     verts=18, col_target=target_col)
        C.parent_to(shin, knee_p, keep_world=False)
        ank_p = _pivot(name_prefix + "_ankle_%s" % sname, (0, 0, -0.36), knee_p, target_col)
        pivots["ankle_%s" % sname] = ank_p
        ank = C.cyl(name_prefix + "_ankleJoint_%s" % sname, 0.038, 0.04, loc=(0, 0, 0), m=JOINT,
                    verts=14, col_target=target_col)
        C.parent_to(ank, ank_p, keep_world=False)
        foot = C.box(name_prefix + "_foot_%s" % sname, (0.11, 0.24, 0.065),
                     loc=(0, -0.055, -0.045), m=FOOT, bevel=0.02, col_target=target_col)
        C.parent_to(foot, ank_p, keep_world=False)
        sole = C.box(name_prefix + "_sole_%s" % sname, (0.115, 0.25, 0.02),
                     loc=(0, -0.055, -0.081), m=DARK, bevel=0.008, col_target=target_col)
        C.parent_to(sole, ank_p, keep_world=False)
        objs += [hip_h, thigh, knee, shin, ank, foot, sole]

    return {"root": root, "pivots": pivots, "eyes": eyes, "chest_core": core,
            "objects": objs, "head": head, "chest": chest}
