"""Shots S01-S12: surgeon -> world model. Every event time comes from the
transcript (words.json), so visuals land exactly while the line is spoken."""
import math
import bpy
from . import common as C
from . import kit as K
from . import props
from . import surgeon as surgeon_mod
from .kit import f


def _find(root_dup, name):
    """Find object by base name inside a copied hierarchy."""
    stack = [root_dup]
    while stack:
        ob = stack.pop()
        if ob.name == name or ob.name.startswith(name):
            return ob
        stack.extend(ob.children)
    return None


# ------------------------------------------------------------------ S01 surgeon
def s01(idx, lib, assets):
    st = K.Stage(idx, "S01")
    O = st.O
    st.pad("pad", 5.2, 4.2)
    st.lights((2.5, -3.5, 4.5), look=(0, 0, 1.0), fill_loc=(-3, -2, 3))

    # surgeon behind desk
    surg = C.copy_hierarchy(assets["surgeon"]["root"], st.col, O(0.0, 0.45, 0))
    # desk (fresh build, shifted onto stage)
    desk_parts = surgeon_mod.build_desk(st.col, "s01_desk")
    for o in desk_parts:
        o.location = (o.location[0] + st.off + 0.15, o.location[1] - 0.45, o.location[2])
    # books stack left + standing pair
    stack = [(0.24, 0.30, 0.045, (0.10, 0.15, 0.35, 1)),
             (0.22, 0.28, 0.04, (0.42, 0.10, 0.10, 1)),
             (0.20, 0.26, 0.035, (0.12, 0.34, 0.18, 1))]
    zb = 0.80
    bx, by = -0.45, -0.40
    book_objs = []
    for i, (w, d, t, rgba) in enumerate(stack):
        zc = zb + sum(s[2] for s in stack[:i]) + t / 2
        b = C.box("s01_bookA%d" % i, (w, d, t), loc=O(bx + (i % 2) * 0.012, by, zc),
                  m=K.mats()["dark"], bevel=0.006, col_target=st.col)
        b.color = rgba
        pages = C.box("s01_bookAp%d" % i, (w - 0.012, d - 0.02, t - 0.008),
                      loc=O(bx + (i % 2) * 0.012, by + 0.004, zc),
                      m=K.mats()["white"], col_target=st.col)
        book_objs += [b, pages]
    K.pop_scale(book_objs, 0.6)
    # instrument tray right
    tray = props.build_tray(st.col, "s01_tray")
    for o in tray:
        o.location = (o.location[0] + st.off + 1.05, o.location[1] - 0.45, o.location[2] + 0.80)
    steth = surgeon_mod.build_stethoscope(st.col, "s01_steth", tray_y=-0.45)
    for o in steth:
        o.location = (o.location[0] + st.off + 1.02, o.location[1], o.location[2] + 0.805)
    sc_items = surgeon_mod.build_scalpel(st.col, "s01_scalpel")
    for o in sc_items:
        o.location = (o.location[0] + st.off + 1.18, o.location[1] - 0.28, o.location[2] + 0.81)
    syr = surgeon_mod.build_syringe(st.col, "s01_syringe")
    for o in syr:
        o.location = (o.location[0] + st.off + 1.0, o.location[1] - 0.62, o.location[2] + 0.81)
    K.pop_scale(tray + steth + sc_items + syr, K.W("अंश्रूमेंट्स", 0, 3.6))
    # calculator
    calc = surgeon_mod.build_calculator(st.col, "s01_calc")
    for o in calc:
        o.location = (o.location[0] + st.off + 0.35, o.location[1] - 0.68, o.location[2] + 0.80)
    K.pop_scale(calc, K.W("क्यल्कूलेटर", 0, 5.0))

    # surgeon diagnosis gesture 6.8-8.9
    shR = _find(surg, "surgeon_shoulder_R")
    elR = _find(surg, "surgeon_elbow_R")
    if shR:
        K.pivot_rot(shR, 6.8, 8.2, (math.radians(-95), 0, math.radians(-15)))
        K.pivot_rot(shR, 8.6, 9.2, (math.radians(95), 0, math.radians(15)))
    if elR:
        K.pivot_rot(elR, 7.2, 8.2, (0, math.radians(-35), 0))

    # floating "missing capability" icons above right
    icons = []
    icons += [("memory", K.icon("s01_ic_mem", "memory", O(1.7, -0.6, 2.05), "blue", 0.16, st.col), K.W("हिस्ट्री", 0, 9.6)),
              ("plan", K.icon("s01_ic_plan", "gear", O(2.05, -0.6, 1.85), "purple", 0.16, st.col), K.W("plan", 1, 12.5)),
              ("check", K.icon("s01_ic_chk", "check", O(2.35, -0.6, 2.1), "orange", 0.14, st.col), K.W("check", 0, 14.6)),
              ("learn", K.icon("s01_ic_lrn", "book", O(2.0, -0.6, 2.3), "green", 0.15, st.col), K.W("सीखे", 0, 16.5))]
    for _, objs, t in icons:
        K.pop_scale(objs, t)
    # red question mark above surgeon at 19.8
    q = K.icon("s01_q", "question", O(0.0, 0.2, 2.25), "red", 0.22, st.col)
    K.pop_scale(q, 19.8, max_s=1.2)
    # four capability chips 23.1-30.6
    chips = [("MEMORY", "blue", 27.0), ("PLANNING", "purple", 28.2),
             ("CHECKING", "orange", 29.3), ("FEEDBACK", "green", 30.3)]
    chip_objs = []
    for i, (txt, colr, t) in enumerate(chips):
        objs = K.node("s01_chip%d" % i, (0.62, 0.2), O(-0.9 + i * 0.62, -1.15, 2.15),
                      colr, label_text=txt, label_size=0.085, col_target=st.col)
        K.pop_scale(objs, t)
        chip_objs += objs

    cam = assets["cam"]
    K.set_cam_kf(cam, 0.0, (0.4, -4.4, 1.75), (0.2, 0, 1.05), st.off3())
    K.set_cam_kf(cam, 9.2, (0.6, -3.0, 1.7), (0.4, 0, 1.25), st.off3())
    K.set_cam_kf(cam, 19.6, (0.5, -2.7, 1.55), (0.2, 0.1, 1.45), st.off3())
    K.cam_path(cam, 23.2, 25.0, (0.5, -3.3, 1.7), (0.5, -3.7, 1.85), (0.2, 0.1, 1.45), (0.2, -0.4, 1.7), st.off3())

    return {"id": "S01", "t0": 0.0, "t1": 34.0,
            "motion": [[0.6, 1.0], [3.5, 5.6], [6.8, 9.2], [9.4, 10.2], [12.3, 13.0],
                       [14.5, 15.2], [16.4, 17.2], [19.8, 21.2], [23.2, 25.0],
                       [27.0, 30.8]]}


# ------------------------------------------------------------------ S02 transformers
def s02(idx, lib, assets):
    st = K.Stage(idx, "S02")
    O = st.O
    st.pad("pad", 5.0, 3.6)
    st.lights((2.5, -3.5, 4.5), look=(0, 0, 1.2))

    core = K.node("s02_core", (1.5, 1.1), O(0, 0, 1.3), "blue", label_text="TRANSFORMER",
                  label_size=0.12, col_target=st.col)
    # inner grid of mini cubes
    cells = []
    for ix in range(4):
        for iy in range(2):
            c = C.box("s02_cell%d%d" % (ix, iy), (0.16, 0.06, 0.16),
                      loc=O(-0.51 + ix * 0.34, -0.045, 1.06 + iy * 0.3),
                      m=K.mats()["lgray"], col_target=st.col)
            cells.append(c)
    K.pop_scale(core, 34.6)
    # pattern cells flip on 42.1-46.3
    t0 = K.W("पाट्टन", 0, 43.0)
    for i, c in enumerate(cells):
        K.pop_scale([c], t0 + i * 0.14, max_s=1.0)
        c.color = (0.2, 0.5, 0.9, 1) if (i % 3) else (0.95, 0.75, 0.2, 1)
        C.kf_color(c, f(t0 + i * 0.14), c.color)

    chips = [("LANGUAGE", "teal", 40.35), ("IMAGES", "purple", 40.75),
             ("CODE", "orange", 41.1), ("REASONING", "green", 41.5)]
    for i, (txt, colr, t) in enumerate(chips):
        objs = K.node("s02_chip%d" % i, (0.6, 0.2), O(-1.55 + i * 1.03, -0.8, 0.55),
                      colr, label_text=txt, label_size=0.08, col_target=st.col)
        K.pop_scale(objs, t)
    # chat bubbles Q/A
    q = K.icon("s02_q", "chat", O(-0.85, -0.5, 0.62), "gray", 0.2, st.col)
    a = K.icon("s02_a", "chat", O(0.85, -0.5, 0.62), "cyan", 0.2, st.col)
    K.pop_scale(q, K.W("सवाल", 1, 46.5))
    K.pop_scale(a, K.W("समरी", 0, 47.6))

    cam = assets["cam"]
    K.set_cam_kf(cam, 34.0, (0.0, -4.3, 1.5), (0, 0, 1.2), st.off3())
    K.cam_path(cam, 41.8, 48.5, (0.0, -4.3, 1.5), (0.0, -3.6, 1.35), (0, 0, 1.2), (0, 0, 1.1), st.off3())
    return {"id": "S02", "t0": 34.0, "t1": 49.5,
            "motion": [[34.5, 35.1], [40.3, 41.8], [42.1, 46.6], [46.4, 48.2], [41.8, 48.5]]}


# ------------------------------------------------------------------ S03 limits
def s03(idx, lib, assets):
    st = K.Stage(idx, "S03")
    O = st.O
    st.pad("pad", 5.0, 3.6)
    st.lights((2.5, -3.5, 4.5), look=(0, 0, 1.2))
    core = K.node("s03_core", (1.7, 1.2), O(0, 0, 1.35), "gray", label_text="PATTERNS?",
                  label_size=0.13, col_target=st.col)
    qs = []
    for i in range(4):
        q = K.icon("s03_q%d" % i, "question", O(-1.2 + i * 0.8, -0.4 - (i % 2) * 0.5, 1.0 + (i % 3) * 0.55),
                   "orange", 0.17, st.col)
        qs.append(q)
        K.pop_scale(q, 50.5 + i * 1.6)
        K.move(q, 51.0 + i * 1.6, 88.0, (0, 0, 0.55))
    cam = assets["cam"]
    K.set_cam_kf(cam, 49.5, (0.0, -4.2, 1.6), (0, 0, 1.3), st.off3())
    K.cam_path(cam, 60.0, 88.0, (0.0, -4.2, 1.6), (0.0, -4.6, 1.75), (0, 0, 1.3), (0, 0, 1.4), st.off3())
    return {"id": "S03", "t0": 49.5, "t1": 93.4,
            "motion": [[50.5, 55.0], [60.0, 88.0]]}


# ------------------------------------------------------------------ S04 cup focus
def s04(idx, lib, assets):
    st = K.Stage(idx, "S04")
    O = st.O
    st.pad("pad", 4.6, 3.4)
    st.lights((2.0, -3.0, 4.0), look=(0, 0, 0.8))
    tbl = props.build_table(st.col, "s04_table", w=1.3, d=0.7, h=0.72)
    for o in tbl:
        o.location = (o.location[0], o.location[1] - 0.1, o.location[2])
    cup = props.build_cup(st.col, "s04_cup")
    for o in cup:
        o.location = (o.location[0] - 0.15, o.location[1] - 0.1, o.location[2] + 0.7425)
    distractors = []
    bk = C.box("s04_bk", (0.26, 0.2, 0.05), loc=O(0.42, -0.12, 0.775), m=K.mats()["blue"],
               bevel=0.008, col_target=st.col)
    ball = C.sphere("s04_ball", 0.05, loc=O(-0.62, -0.05, 0.79), m=K.mats()["orange"],
                    segs=16, rings=12, col_target=st.col)
    distractors = [bk, ball]
    # focus ring + spotlight cone on cup at 98.7
    ring = K.glow_ring("s04_ring", 0.16, O(-0.15, -0.1, 0.752), "yellow", st.col, tube=0.014)
    cone = C.cone("s04_cone", 0.34, 0.12, 1.3, loc=O(-0.15, -0.1, 1.42),
                  rot=(math.pi, 0, 0), m=K.mats()["yellow"], verts=18, col_target=st.col)
    K.pop_scale([ring, cone], K.W("फोकस", 0, 98.8))
    K.pop_scale(distractors, 94.6)
    cam = assets["cam"]
    K.set_cam_kf(cam, 93.4, (0.0, -3.4, 1.35), (0, 0, 0.75), st.off3())
    K.cam_path(cam, 98.8, 101.4, (0.0, -3.4, 1.35), (-0.1, -2.2, 1.1), (0, 0, 0.75), (-0.15, -0.1, 0.8), st.off3())
    return {"id": "S04", "t0": 93.4, "t1": 101.6,
            "motion": [[94.6, 95.2], [98.8, 101.4]]}


# ------------------------------------------------------------------ S05 attention
def s05(idx, lib, assets):
    st = K.Stage(idx, "S05")
    O = st.O
    st.pad("pad", 5.2, 3.4)
    st.lights((2.0, -3.0, 4.2), look=(0, 0, 1.2))
    toks = [("ROBOT", "blue"), ("CUP", "orange"), ("LIFTS", "teal"), ("UP", "purple")]
    tok_objs = []
    for i, (txt, colr) in enumerate(toks):
        objs = K.node("s05_tok%d" % i, (0.5, 0.34), O(-1.5 + i * 1.0, 0, 1.35), colr,
                      label_text=txt, label_size=0.13, col_target=st.col)
        K.pop_scale(objs, 102.6 + i * 0.5)
        tok_objs.append(objs)
    # connection lines 104.7-109
    lines = []
    for i in range(3):
        ln = K.line3d("s05_ln%d" % i, O(-1.24 + i * 1.0, 0, 1.35), O(-0.76 + i * 1.0, 0, 1.35),
                      r=0.014, color="gray", col_target=st.col)
        K.pop_scale(ln, 104.9 + i * 0.5)
        lines += ln
    # weighted thick line robot->cup at 109.3 ("जाडा इंपोट्टन्स")
    big = K.line3d("s05_big", O(-1.22, 0, 1.27), O(-0.78, 0, 1.27), r=0.035, color="orange",
                   col_target=st.col)
    K.pop_scale(big, K.W("इंपोट्टन्स", 0, 109.4))
    ring = K.glow_ring("s05_ring", 0.34, O(-1.5, 0, 1.35), "yellow", st.col, tube=0.016)
    K.pop_scale([ring], K.W("रिलेटिड", 0, 110.8))
    # next token predict 112.3-116.8
    nxt = K.node("s05_next", (0.5, 0.34), O(1.6, 0, 1.35), "gray", col_target=st.col)
    K.pop_scale(nxt, 112.5)
    qm = K.icon("s05_q", "question", O(1.6, -0.05, 1.35), "red", 0.1, st.col)
    K.pop_scale(qm, 113.2)
    fill = K.node("s05_fill", (0.5, 0.34), O(1.6, 0, 1.35), "green",
                  label_text="ANSWER", label_size=0.13, col_target=st.col)
    K.pop_scale(fill, K.W("जबाब", 2, 115.4))
    K.move(fill, 115.4, 115.5, (0, 0, 0))
    lbl = K.label_y("s05_w", "WEIGHTS", 0.11, O(0, -0.7, 0.72), color="orange", col_target=st.col, font=K.FONT_EN)
    K.pop_scale([lbl], K.W("वीट", 0, 120.4) if False else 117.4)
    cam = assets["cam"]
    K.set_cam_kf(cam, 101.6, (0.1, -3.8, 1.6), (0, 0, 1.3), st.off3())
    K.cam_path(cam, 104.7, 109.0, (0.1, -3.8, 1.6), (0.1, -3.2, 1.45), (0, 0, 1.3), (0, 0, 1.35), st.off3())
    return {"id": "S05", "t0": 101.6, "t1": 119.6,
            "motion": [[102.6, 104.2], [104.9, 106.5], [109.3, 110.0], [110.8, 111.4],
                       [112.5, 113.8], [115.4, 116.0], [117.4, 118.0], [104.7, 109.0]]}


# ------------------------------------------------------------------ S06 training
def s06(idx, lib, assets):
    st = K.Stage(idx, "S06")
    O = st.O
    st.pad("pad", 5.2, 3.6)
    st.lights((2.0, -3.0, 4.2), look=(0, 0, 1.2))
    core = K.node("s06_core", (1.1, 1.1), O(0.9, 0, 1.25), "blue", label_text="MODEL",
                  label_size=0.11, col_target=st.col)
    K.pop_scale(core, 120.5)
    # data icons fly in 122.1-131
    kinds = [("book", "orange", 126.2), ("chat", "teal", 127.2), ("code", "purple", 128.4),
             ("db", "green", 129.6), ("camera", "red", 130.4)]
    fly = []
    for i, (kind, colr, t) in enumerate(kinds):
        objs = K.icon("s06_ic%d" % i, kind, O(-1.7, -0.5, 0.75 + i * 0.28), colr, 0.16, st.col)
        K.pop_scale(objs, t - 0.6)
        K.move(objs, t, t + 1.6, (2.05, 0.35, (0.9 - 0.75 - i * 0.28) * 0.35 + (1.25 - 0.75 - i * 0.28) * 0.0 + (1.25 - (0.75 + i * 0.28)) * 0.55))
        fly += objs
    # number grid adjusts 137.5-139.7
    grid = []
    for ix in range(3):
        for iy in range(3):
            c = C.box("s06_g%d%d" % (ix, iy), (0.14, 0.05, 0.14),
                      loc=O(-1.35 + ix * 0.24, 0, 0.95 + iy * 0.24),
                      m=K.mats()["cyan"], col_target=st.col)
            K.pop_scale([c], 137.6 + (ix * 3 + iy) * 0.09)
            zz = 1.0 + (ix + iy) % 3 * 0.28
            c.scale = (1, 1, 1)
            c.keyframe_insert("scale", frame=f(137.6 + (ix * 3 + iy) * 0.09))
            c.scale = (1, 1, zz)
            c.keyframe_insert("scale", frame=f(139.0 + (ix * 3 + iy) * 0.09))
            grid.append(c)
    chips = [("GRAMMAR", "teal", 140.3), ("STYLE", "purple", 141.3),
             ("FACTS", "orange", 142.3), ("REASONING", "green", 143.3)]
    for i, (txt, colr, t) in enumerate(chips):
        objs = K.node("s06_chip%d" % i, (0.56, 0.18), O(-1.6 + i * 0.44, -0.75, 0.5),
                      colr, label_text=txt, label_size=0.062, col_target=st.col)
        K.pop_scale(objs, t)
    # capacity meter 144.9-148.6
    bar_bg = C.box("s06_bar", (1.5, 0.06, 0.16), loc=O(0.9, -0.55, 0.42), m=K.mats()["lgray"],
                   col_target=st.col)
    bar_fg = C.box("s06_barf", (1.4, 0.07, 0.12), loc=O(0.2, -0.55, 0.42), m=K.mats()["green"],
                   col_target=st.col)
    bar_fg.scale = (0.02, 1, 1)
    bar_fg.keyframe_insert("scale", frame=f(145.2))
    bar_fg.scale = (1, 1, 1)
    bar_fg.keyframe_insert("scale", frame=f(148.2))
    K.pop_scale([bar_bg], 145.0)
    cam = assets["cam"]
    K.set_cam_kf(cam, 120.0, (0.0, -4.4, 1.5), (0, 0, 1.15), st.off3())
    K.cam_path(cam, 137.5, 141.0, (0.0, -4.4, 1.5), (-0.4, -3.6, 1.3), (0, 0, 1.15), (-0.6, 0, 1.1), st.off3())
    return {"id": "S06", "t0": 120.0, "t1": 148.6,
            "motion": [[120.5, 121.1], [126.2, 131.5], [137.6, 140.0], [140.3, 144.0],
                       [145.2, 148.2], [137.5, 141.0]]}


# ------------------------------------------------------------------ S07 training stops
def s07(idx, lib, assets):
    st = K.Stage(idx, "S07")
    O = st.O
    st.pad("pad", 4.6, 3.2)
    st.lights((2.0, -3.0, 4.0), look=(0, 0, 1.2))
    core = K.node("s07_core", (1.4, 1.1), O(0, 0, 1.3), "blue", label_text="TRAINED MODEL",
                  label_size=0.11, col_target=st.col)
    cells = []
    for ix in range(4):
        for iy in range(2):
            c = C.box("s07_c%d%d" % (ix, iy), (0.18, 0.06, 0.18),
                      loc=O(-0.55 + ix * 0.36, -0.045, 1.08 + iy * 0.3),
                      m=K.mats()["cyan"], col_target=st.col)
            cells.append(c)
    K.pop_scale(core + cells, 149.6)
    # cells pulse 152.6-156.8 (updates), then freeze
    for i, c in enumerate(cells):
        K.move([c], 152.8 + i * 0.12, 153.4 + i * 0.12, (0, 0, 0.05))
        K.move([c], 153.4 + i * 0.12, 154.0 + i * 0.12, (0, 0, -0.05))
    lock = K.icon("s07_lock", "lock", O(1.15, -0.35, 1.6), "red", 0.18, st.col)
    K.pop_scale(lock, K.W("ख़द्म", 0, 156.9))
    chip = K.node("s07_chip", (0.9, 0.22), O(0, -0.8, 0.55), "orange",
                  label_text="UPDATES STOP", label_size=0.085, col_target=st.col)
    K.pop_scale(chip, 157.3)
    cam = assets["cam"]
    K.set_cam_kf(cam, 149.1, (0.0, -3.9, 1.55), (0, 0, 1.25), st.off3())
    K.cam_path(cam, 156.9, 158.0, (0.0, -3.9, 1.55), (0.15, -3.3, 1.45), (0, 0, 1.25), (0.3, 0, 1.35), st.off3())
    return {"id": "S07", "t0": 149.1, "t1": 158.2,
            "motion": [[149.6, 150.2], [152.8, 154.2], [156.9, 157.6], [156.9, 158.0]]}


# ------------------------------------------------------------------ S08 context
def s08(idx, lib, assets):
    st = K.Stage(idx, "S08")
    O = st.O
    st.pad("pad", 4.8, 3.2)
    st.lights((2.0, -3.0, 4.0), look=(0, 0, 1.1))
    b1 = K.node("s08_b1", (1.7, 0.4), O(-0.35, 0, 1.45), "lgray", label_text="MY PROJECT BLUEPRINT - REMEMBER?",
                label_size=0.075, label_color="ink", col_target=st.col)
    K.pop_scale(b1, K.W("पहली", 0, 161.7))
    eye = K.icon("s08_eye", "eye", O(-1.35, -0.3, 1.15), "blue", 0.2, st.col)
    K.pop_scale(eye, 163.0)
    ln = K.line3d("s08_ln", O(-1.15, -0.3, 1.12), O(-0.7, -0.05, 1.3), r=0.012, color="blue",
                  col_target=st.col)
    K.pop_scale(ln, 163.2)
    b2 = K.node("s08_b2", (1.7, 0.4), O(0.55, 0, 1.0), "cyan", label_text="YES, YOU TOLD ME...",
                label_size=0.08, col_target=st.col)
    K.pop_scale(b2, K.W("जबाद", 2, 164.3))
    chip = K.node("s08_chip", (1.0, 0.24), O(0, -0.7, 0.6), "orange",
                  label_text="CONTEXT", label_size=0.1, col_target=st.col)
    K.pop_scale(chip, K.W("कुन्टेक्स्त", 0, 165.6))
    cam = assets["cam"]
    K.set_cam_kf(cam, 158.4, (0.0, -3.6, 1.35), (0, 0, 1.15), st.off3())
    return {"id": "S08", "t0": 158.4, "t1": 166.9,
            "motion": [[161.7, 162.3], [163.0, 163.6], [164.3, 164.9], [165.6, 166.2]]}


# ------------------------------------------------------------------ S09 meeting + memory wall
def s09(idx, lib, assets):
    st = K.Stage(idx, "S09")
    O = st.O
    st.pad("pad", 7.2, 3.6)
    st.lights((1.0, -3.5, 4.5), look=(0, 0, 1.0), fill_loc=(-2, -2, 3))

    # Zone A: employee + meeting (x=-2.3)
    emp = C.copy_hierarchy(assets["student"]["root"], st.col, O(-2.3, 0.25, 0))
    tbl = C.box("s09_tbl", (0.9, 0.6, 0.04), loc=O(-2.3, -0.35, 0.74), m=K.mats()["white"],
                bevel=0.01, col_target=st.col)
    for sx in (-1, 1):
        lg = C.box("s09_tl%d" % sx, (0.05, 0.05, 0.72), loc=O(-2.3 + sx * 0.38, -0.35, 0.36),
                   m=K.mats()["gray"], col_target=st.col)
    boss_b = K.node("s09_boss", (1.35, 0.42), O(-2.3, -0.75, 1.5), "orange",
                    label_text="PROJECT BLUE — FRIDAY", label_size=0.062, col_target=st.col)
    K.pop_scale(boss_b, K.W("रिएबाट", 0, 172.8))
    note = C.box("s09_note", (0.22, 0.02, 0.16), loc=O(-2.05, -0.28, 1.02), m=K.mats()["yellow"],
                 bevel=0.008, col_target=st.col)
    K.pop_scale([note], K.W("यूज", 0, 176.6))
    cab = C.box("s09_cab", (0.5, 0.4, 1.1), loc=O(-3.25, -0.4, 0.55), m=K.mats()["gray"],
                bevel=0.02, col_target=st.col)
    K.pop_scale([cab], 178.9)
    q = K.icon("s09_q", "question", O(-2.3, 0.1, 2.0), "red", 0.16, st.col)
    K.pop_scale(q, K.W("याद नहीं", 0, 182.2) if False else 182.3)
    clock = K.icon("s09_clock", "clock", O(-1.55, -0.5, 1.7), "purple", 0.17, st.col)
    K.pop_scale(clock, 183.2)
    # Zone B: whiteboard sticky (x=0)
    wb = C.box("s09_wb", (1.3, 0.05, 0.9), loc=O(0, 0.35, 1.35), m=K.mats()["white"],
               bevel=0.01, col_target=st.col)
    K.pop_scale([wb], 184.4)
    stick = C.box("s09_stick", (0.3, 0.02, 0.3), loc=O(0, 0.28, 1.35), rot=(math.radians(-6), 0, 0),
                  m=K.mats()["yellow"], bevel=0.006, col_target=st.col)
    K.pop_scale([stick], K.W("तमप्ररी", 0, 185.6))
    lbl = K.label_y("s09_wbl", "AI CONTEXT = TEMP", 0.075, O(0, 0.27, 1.68), color="ink",
                    col_target=st.col, font=K.FONT_EN)
    K.pop_scale([lbl], 186.6)
    # Zone C: memory wall (x=2.3)
    wall = C.box("s09_wall", (1.7, 0.08, 1.3), loc=O(2.3, 0.3, 1.25), m=K.mats()["lgray"],
                 bevel=0.015, col_target=st.col)
    K.pop_scale([wall], 189.8)
    blocks = []
    for ix in range(4):
        for iy in range(3):
            b = C.box("s09_mb%d%d" % (ix, iy), (0.3, 0.1, 0.26),
                      loc=O(1.85 + ix * 0.3, 0.2, 0.85 + iy * 0.32),
                      m=K.mats()["blue"], col_target=st.col)
            blocks.append(b)
    for i, b in enumerate(blocks[:6]):
        K.pop_scale([b], 190.5 + i * 0.25)
    stamps = [("SAVE", "green", 197.0), ("IGNORE", "gray", 199.5), ("UPDATE", "orange", 202.0),
              ("RETRIEVE", "blue", 204.0), ("CONFLICT", "red", 206.6)]
    for i, (txt, colr, t) in enumerate(stamps):
        objs = K.node("s09_st%d" % i, (0.52, 0.2), O(1.72 + i * 0.3, -0.12, 1.98),
                      colr, label_text=txt, label_size=0.055, col_target=st.col)
        K.pop_scale(objs, t, max_s=1.0)
    cam = assets["cam"]
    K.set_cam_kf(cam, 166.9, (-2.3, -3.4, 1.5), (-2.3, 0, 1.15), st.off3())
    K.cam_path(cam, 184.2, 185.6, (-2.3, -3.4, 1.5), (0.0, -3.4, 1.5), (-2.3, 0, 1.15), (0, 0, 1.3), st.off3())
    K.cam_path(cam, 196.6, 198.2, (0.0, -3.4, 1.5), (2.3, -3.2, 1.45), (0, 0, 1.3), (2.3, 0, 1.25), st.off3())
    return {"id": "S09", "t0": 166.9, "t1": 209.3,
            "motion": [[172.8, 173.5], [176.6, 177.2], [178.9, 179.5], [182.3, 184.0],
                       [184.4, 185.0], [185.6, 186.2], [186.6, 187.2], [189.8, 191.2],
                       [197.0, 207.4], [184.2, 185.6], [196.6, 198.2]]}


# ------------------------------------------------------------------ S10 student memory
def s10(idx, lib, assets):
    st = K.Stage(idx, "S10")
    O = st.O
    st.pad("pad", 5.4, 3.6)
    st.lights((2.0, -3.5, 4.2), look=(0, 0, 1.0))
    stu = C.copy_hierarchy(assets["student"]["root"], st.col, O(-0.6, 0.3, 0))
    dsk = C.box("s10_desk", (1.0, 0.65, 0.04), loc=O(-0.6, -0.35, 0.74), m=K.mats()["white"],
                bevel=0.01, col_target=st.col)
    card = C.box("s10_card", (0.34, 0.02, 0.22), loc=O(-0.6, -0.42, 0.88), m=K.mats()["white"],
                 bevel=0.006, col_target=st.col)
    K.pop_scale([card], 210.2)
    txt = K.label_y("s10_cardT", "25 × 4 = ?", 0.075, O(-0.6, -0.45, 0.88), color="ink",
                    col_target=st.col, font=K.FONT_EN)
    K.pop_scale([txt], 210.4)
    steps = []
    for i in range(3):
        s = K.node("s10_step%d" % i, (0.3, 0.22), O(-1.35 + i * 0.42, 0.35, 2.0),
                   "cyan", label_text=str(i + 1), label_size=0.1, col_target=st.col)
        K.pop_scale(s, 212.2 + i * 0.5)
        steps += s
    th = []
    for i in range(2):
        b = K.icon("s10_th%d" % i, "chat", O(-0.15 + i * 0.5, 0.2, 1.85 + i * 0.3), "purple",
                   0.14, st.col)
        K.pop_scale(b, 214.6 + i * 0.6)
        th += b
    fr = K.label_y("s10_fr", "½ + ¾", 0.13, O(0.9, -0.35, 1.1), color="ink", col_target=st.col)
    K.pop_scale([fr], K.W("फ्रक्ष्ट्शन्स", 0, 219.6))
    tick = K.icon("s10_tick", "check", O(1.15, -0.35, 1.25), "green", 0.12, st.col)
    K.pop_scale(tick, 221.4)
    # three memory boxes
    boxes = [("WORKING", "cyan", 226.4), ("LONG-TERM", "blue", 228.7), ("SKILL", "green", 232.1)]
    for i, (txt, colr, t) in enumerate(boxes):
        objs = K.node("s10_mb%d" % i, (0.72, 0.4), O(-1.35 + i * 1.0, -0.55, 0.5),
                      colr, label_text=txt, label_size=0.07, col_target=st.col)
        K.pop_scale(objs, t)
    cross = K.icon("s10_cross", "cross", O(1.35, -0.35, 1.1), "red", 0.14, st.col)
    K.pop_scale(cross, K.W("अकेली", 0, 234.5))
    gears = [("RETRIEVE", "blue", 243.0), ("ORGANIZE", "teal", 243.9),
             ("UPDATE", "orange", 244.7), ("VERIFY", "green", 245.4)]
    for i, (txt, colr, t) in enumerate(gears):
        objs = K.node("s10_g%d" % i, (0.5, 0.18), O(-0.95 + i * 0.62, -0.9, 1.6),
                      colr, label_text=txt, label_size=0.055, col_target=st.col)
        K.pop_scale(objs, t)
    cam = assets["cam"]
    K.set_cam_kf(cam, 209.6, (-0.6, -3.4, 1.5), (-0.6, 0, 1.1), st.off3())
    K.cam_path(cam, 225.9, 227.4, (-0.6, -3.4, 1.5), (0.0, -3.8, 1.45), (-0.6, 0, 1.1), (0, -0.2, 1.0), st.off3())
    return {"id": "S10", "t0": 209.6, "t1": 246.0,
            "motion": [[210.2, 210.8], [212.2, 213.8], [214.6, 215.8], [219.6, 220.2],
                       [221.4, 222.0], [226.4, 232.8], [234.5, 235.1], [243.0, 246.0],
                       [225.9, 227.4]]}


# ------------------------------------------------------------------ S11 planning
def s11(idx, lib, assets):
    st = K.Stage(idx, "S11")
    O = st.O
    st.pad("pad", 7.0, 3.6)
    st.lights((1.0, -3.5, 4.5), look=(0, 0, 1.0))
    goal = K.node("s11_goal", (0.72, 0.42), O(-2.9, 0, 1.35), "orange",
                  label_text="REPORT", label_size=0.09, col_target=st.col)
    K.pop_scale(goal, 248.6)
    steps = [("UNDERSTAND", "blue", 259.9), ("SOURCES", "teal", 264.6), ("CHECK", "purple", 266.8),
             ("NOTES", "cyan", 267.6), ("OUTLINE", "green", 269.8), ("DRAFT", "orange", 271.0),
             ("VERIFY", "red", 273.0)]
    node_objs = []
    for i, (txt, colr, t) in enumerate(steps):
        objs = K.node("s11_st%d" % i, (0.56, 0.36), O(-2.0 + i * 0.72, 0, 1.35 + (i % 2) * 0.22),
                      colr, label_text=txt, label_size=0.058, col_target=st.col)
        K.pop_scale(objs, 250.4 + i * 0.85)
        node_objs.append(objs)
        if i > 0:
            ln = K.line3d("s11_ln%d" % i, O(-2.0 + (i - 1) * 0.72 + 0.3, 0, 1.35 + ((i - 1) % 2) * 0.22),
                          O(-2.0 + i * 0.72 - 0.3, 0, 1.35 + (i % 2) * 0.22),
                          r=0.011, color="gray", col_target=st.col)
            K.pop_scale(ln, 250.6 + i * 0.85)
    # agent orb walks the chain
    orb = C.sphere("s11_orb", 0.09, loc=O(-2.9, -0.35, 1.35), m=K.mats()["cyan"], segs=16,
                   rings=12, col_target=st.col)
    K.pop_scale([orb], 259.5)
    for i in range(7):
        K.move([orb], 259.9 + i * 2.15, 260.9 + i * 2.15, (0.72, 0, (i % 2) * 0.22 - ((i + 1) % 2) * 0.0))
    # back-arrow loop at 275.4 (verify -> search)
    back = K.arrow("s11_back", O(1.85, 0, 1.72), O(-1.35, 0, 1.72), r=0.014, color="red",
                   col_target=st.col)
    K.pop_scale(back, 275.5)
    # loop ring label
    loop = K.label_y("s11_loop", "GOAL → RESULT LOOP", 0.09, O(0, -0.75, 0.62), color="purple",
                     col_target=st.col, font=K.FONT_EN)
    K.pop_scale([loop], K.W("लूप", 0, 276.4))
    # checklist + clock 278.5-291.5
    paper = C.box("s11_paper", (0.6, 0.03, 0.8), loc=O(2.6, 0.1, 1.15), m=K.mats()["white"],
                  bevel=0.008, col_target=st.col)
    K.pop_scale([paper], 278.7)
    for i in range(4):
        ln = C.box("s11_pl%d" % i, (0.4, 0.005, 0.03), loc=O(2.5, 0.08, 1.4 - i * 0.14),
                   m=K.mats()["gray"], col_target=st.col)
        K.pop_scale([ln], 279.2 + i * 0.3)
    clock = K.icon("s11_clock", "clock", O(3.2, -0.3, 1.75), "purple", 0.2, st.col)
    K.pop_scale(clock, K.W("दिनो", 0, 282.0))
    risks = [("DEADLINE", "red", 286.3), ("MISSING", "orange", 287.3),
             ("CHANGE", "purple", 288.6), ("FAILURE", "gray", 289.8)]
    for i, (txt, colr, t) in enumerate(risks):
        objs = K.node("s11_r%d" % i, (0.5, 0.18), O(2.25 + (i % 2) * 0.62, -0.6, 0.72 - (i // 2) * 0.3),
                      colr, label_text=txt, label_size=0.055, col_target=st.col)
        K.pop_scale(objs, t)
    planner = K.node("s11_planner", (0.9, 0.44), O(3.0, 0.35, 2.2), "blue",
                     label_text="PLANNER", label_size=0.075, col_target=st.col)
    K.pop_scale(planner, K.W("प्लानर", 0, 293.2))
    a1 = K.arrow("s11_pa", O(2.55, 0.35, 2.2), O(1.95, 0.35, 2.2), color="blue", col_target=st.col)
    K.pop_scale(a1, 294.8)
    cam = assets["cam"]
    K.set_cam_kf(cam, 246.5, (0.0, -4.6, 1.7), (0, 0, 1.25), st.off3())
    K.cam_path(cam, 259.8, 261.5, (0.0, -4.6, 1.7), (-0.6, -3.7, 1.55), (0, 0, 1.25), (-0.6, 0, 1.3), st.off3())
    K.cam_path(cam, 278.4, 280.0, (-0.6, -3.7, 1.55), (2.5, -3.7, 1.5), (-0.6, 0, 1.3), (2.6, 0.1, 1.2), st.off3())
    return {"id": "S11", "t0": 246.5, "t1": 297.4,
            "motion": [[248.6, 249.2], [250.4, 256.6], [259.5, 261.0], [259.9, 275.0],
                       [275.5, 276.2], [276.4, 277.0], [278.7, 280.6], [282.0, 282.8],
                       [286.3, 290.4], [293.2, 295.4], [259.8, 261.5], [278.4, 280.0]]}


# ------------------------------------------------------------------ S12 world model
def s12(idx, lib, assets):
    st = K.Stage(idx, "S12")
    O = st.O
    st.pad("pad", 8.0, 3.8)
    st.lights((1.0, -3.8, 4.8), look=(0, 0, 1.0), fill_loc=(-1, -2, 3))

    # Zone A: road crossing (x=-2.6)
    road = C.box("s12_road", (3.4, 1.0, 0.05), loc=O(-2.6, -0.2, 0.025), m=K.mats()["road"],
                 col_target=st.col)
    K.pop_scale([road], 304.6)
    for i in range(5):
        m_ = C.box("s12_mark%d" % i, (0.22, 0.05, 0.051), loc=O(-3.9 + i * 0.66, -0.2, 0.052),
                   m=K.mats()["white"], col_target=st.col)
    car_body = C.box("s12_car", (0.62, 0.34, 0.2), loc=O(-4.0, -0.2, 0.19), m=K.mats()["red"],
                     bevel=0.05, col_target=st.col)
    car_top = C.box("s12_cartop", (0.3, 0.3, 0.16), loc=O(-4.0, -0.2, 0.37), m=K.mats()["red"],
                    bevel=0.04, col_target=st.col)
    wheels = []
    for sx in (-1, 1):
        for sy in (-1, 1):
            w = C.cyl("s12_wh%d%d" % (sx, sy), 0.09, 0.05, loc=O(-4.0 + sx * 0.2, -0.2 + sy * 0.18, 0.09),
                      rot=(math.radians(90), 0, 0), m=K.mats()["dark"], verts=14, col_target=st.col)
            wheels.append(w)
    K.pop_scale([car_body, car_top] + wheels, 305.2)
    K.move([car_body, car_top] + wheels, 306.0, 312.0, (2.2, 0, 0))
    K.move([car_body, car_top] + wheels, 313.9, 317.5, (0.35, 0, 0))
    # person
    per = C.copy_hierarchy(assets["student"]["root"], st.col, O(-2.6, 0.42, 0))
    K.pop_scale([per], 305.0)
    dist = K.label_y("s12_dist", "DISTANCE? SPEED?", 0.1, O(-3.1, -0.2, 1.05), color="orange",
                     col_target=st.col)
    K.pop_scale([dist], K.W("door", 0, 314.1))
    K.move([dist], 315.5, 317.0, (0.9, 0, 0))
    # person crosses at 317.8
    K.move([per], 317.9, 321.0, (0, -0.75, 0))

    # Zone B: robot + table + cup (x=1.6)
    tbl = props.build_table(st.col, "s12_table", w=1.1, d=0.7, h=0.72)
    for o in tbl:
        o.location = (o.location[0] + 2.2, o.location[1], o.location[2])
    rob = C.copy_hierarchy(assets["robot"]["root"], st.col, O(1.35, 0.15, 0))
    cup = props.build_cup(st.col, "s12_cup")
    for o in cup:
        o.location = (o.location[0] + 2.05, o.location[1] - 0.05, o.location[2] + 0.7425)
    K.pop_scale([rob], K.W("रोबाट", 0, 318.4))
    K.pop_scale(cup, 319.0)
    # callouts on words: position/weight/grip/edge
    co = [("POSITION", "blue", 319.6), ("WEIGHT", "teal", 320.4), ("GRIP", "orange", 321.2),
          ("EDGE", "purple", 322.0)]
    for i, (txt, colr, t) in enumerate(co):
        objs = K.node("s12_co%d" % i, (0.52, 0.18), O(1.45 + i * 0.42, -0.55, 1.55),
                      colr, label_text=txt, label_size=0.055, col_target=st.col)
        K.pop_scale(objs, t)
    ring = K.glow_ring("s12_ring", 0.13, O(2.05, -0.05, 0.748), "orange", st.col, tube=0.013)
    K.pop_scale([ring], K.W("कम्जोर", 0, 328.6))
    # arm reach + lift: rotate right shoulder/elbow of copy
    shR = _find(rob, "robot_shoulder_R")
    elR = _find(rob, "robot_elbow_R")
    if shR:
        K.pivot_rot(shR, 330.9, 332.4, (math.radians(-78), 0, math.radians(-8)))
    if elR:
        K.pivot_rot(elR, 331.4, 332.6, (0, math.radians(-28), 0))
    # cup lift follows hand
    K.move(cup, 332.5, 333.6, (0.05, 0.18, 0.16))
    K.move(cup, 333.8, 335.4, (0.05, 0.1, 0.14))
    chk = K.icon("s12_chk", "check", O(2.75, -0.4, 1.55), "green", 0.14, st.col)
    K.pop_scale(chk, K.W("उठाया", 0, 333.6))
    crs = K.icon("s12_crs", "cross", O(3.0, -0.4, 1.3), "red", 0.12, st.col)
    K.pop_scale(crs, K.W("नीचे", 0, 335.0))
    # Zone C: prediction engine panel (x=4.6)
    gear = K.icon("s12_gear", "gear", O(4.6, 0, 1.45), "purple", 0.22, st.col)
    K.pop_scale(gear, K.W("प्रटिक्छन", 0, 336.4))
    lbl = K.label_y("s12_plbl", "PREDICTION ENGINE", 0.1, O(4.6, -0.35, 1.0), color="ink",
                    col_target=st.col, font=K.FONT_EN)
    K.pop_scale([lbl], 337.0)
    br = K.icon("s12_br", "brain", O(3.9, 0, 2.0), "gray", 0.16, st.col)
    K.pop_scale(br, 338.6)
    cx = K.icon("s12_cx", "cross", O(3.9, 0, 2.0), "red", 0.14, st.col)
    K.pop_scale(cx, K.W("कच्च्चनेस", 0, 339.2))
    iff = K.node("s12_if", (0.6, 0.24), O(4.25, -0.4, 1.9), "blue", label_text="IF ACTION",
                 label_size=0.06, col_target=st.col)
    thn = K.node("s12_then", (0.6, 0.24), O(5.05, -0.4, 1.9), "green", label_text="THEN RESULT",
                 label_size=0.055, col_target=st.col)
    K.pop_scale(iff, 346.9)
    K.pop_scale(thn, 347.8)
    wr = K.node("s12_wrong", (1.15, 0.24), O(4.6, -0.4, 0.6), "red",
                label_text="MAY BE WRONG → REAL CHECK", label_size=0.045, col_target=st.col)
    K.pop_scale(wr, 353.5)
    cam = assets["cam"]
    K.set_cam_kf(cam, 297.7, (-2.6, -3.6, 1.5), (-2.6, 0, 0.7), st.off3())
    K.cam_path(cam, 317.7, 318.6, (-2.6, -3.6, 1.5), (1.7, -3.6, 1.5), (-2.6, 0, 0.7), (1.7, 0, 0.8), st.off3())
    K.cam_path(cam, 332.4, 333.4, (1.7, -3.6, 1.5), (1.85, -2.6, 1.25), (1.7, 0, 0.8), (2.0, -0.05, 0.9), st.off3())
    K.cam_path(cam, 336.2, 337.4, (1.85, -2.6, 1.25), (4.6, -3.4, 1.55), (2.0, -0.05, 0.9), (4.6, 0, 1.3), st.off3())
    return {"id": "S12", "t0": 297.7, "t1": 355.6,
            "motion": [[304.6, 305.8], [306.0, 312.0], [313.9, 317.5], [314.1, 315.2],
                       [315.5, 317.0], [317.9, 321.0], [318.4, 319.6], [322.0, 322.8],
                       [328.6, 329.2], [330.9, 332.6], [332.5, 335.4], [333.6, 335.6],
                       [336.4, 337.6], [338.6, 339.8], [346.9, 348.4], [353.5, 354.2],
                       [317.7, 318.6], [332.4, 333.4], [336.2, 337.4]]}


def build_all(idx0, lib, assets):
    shots = []
    shots.append(s01(idx0 + 0, lib, assets))
    shots.append(s02(idx0 + 1, lib, assets))
    shots.append(s03(idx0 + 2, lib, assets))
    shots.append(s04(idx0 + 3, lib, assets))
    shots.append(s05(idx0 + 4, lib, assets))
    shots.append(s06(idx0 + 5, lib, assets))
    shots.append(s07(idx0 + 6, lib, assets))
    shots.append(s08(idx0 + 7, lib, assets))
    shots.append(s09(idx0 + 8, lib, assets))
    shots.append(s10(idx0 + 9, lib, assets))
    shots.append(s11(idx0 + 10, lib, assets))
    shots.append(s12(idx0 + 11, lib, assets))
    return shots
