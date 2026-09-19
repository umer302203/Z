"""Shots S13-S24: tools -> conclusion."""
import math
import bpy
from . import common as C
from . import kit as K
from . import props
from .kit import f


def _find(root_dup, name):
    stack = [root_dup]
    while stack:
        ob = stack.pop()
        if ob.name == name or ob.name.startswith(name):
            return ob
        stack.extend(ob.children)
    return None


# ------------------------------------------------------------------ S13 tools
def s13(idx, lib, assets):
    st = K.Stage(idx, "S13")
    O = st.O
    st.pad("pad", 7.2, 4.0)
    st.lights((1.0, -3.8, 4.8), look=(0, 0, 1.1))
    tiles = [("BROWSER", "magnifier", "teal", 358.9), ("CALCULATOR", "gear", "orange", 361.1),
             ("CODE", "code", "purple", 363.0), ("DATABASE", "db", "green", 364.9),
             ("CAMERA", "camera", "blue", 367.4), ("SENSORS", "eye", "red", 369.4)]
    for i, (txt, ic, colr, t) in enumerate(tiles):
        x = -2.9 + (i % 3) * 1.05
        z = 1.75 - (i // 3) * 0.85
        node_objs = K.node("s13_t%d" % i, (0.9, 0.62), O(x, 0, z), colr,
                           label_text=txt, label_size=0.058, col_target=st.col)
        K.pop_scale(node_objs, t)
        ic_objs = K.icon("s13_i%d" % i, ic, O(x, -0.05, z - 0.08), colr, 0.13, st.col)
        K.pop_scale(ic_objs, t + 0.15)
    # loop diagram
    cx, cz = 1.9, 1.25
    loop_nodes = [("THINK", "blue", (-0.62, 0.62)), ("ACT", "orange", (0.62, 0.62)),
                  ("OBSERVE", "teal", (0.62, -0.62)), ("UPDATE", "purple", (-0.62, -0.62))]
    lt = [375.9, 377.0, 378.2, 379.0]
    for i, (txt, colr, (dx, dz)) in enumerate(loop_nodes):
        objs = K.node("s13_l%d" % i, (0.56, 0.3), O(cx + dx, 0, cz + dz), colr,
                      label_text=txt, label_size=0.065, col_target=st.col)
        K.pop_scale(objs, lt[i])
    for i in range(4):
        (dx0, dz0) = loop_nodes[i][2]
        (dx1, dz1) = loop_nodes[(i + 1) % 4][2]
        ln = K.line3d("s13_la%d" % i, O(cx + dx0 * 0.82, 0, cz + dz0 * 0.82),
                      O(cx + dx1 * 0.82, 0, cz + dz1 * 0.82), r=0.013, color="gray",
                      col_target=st.col)
        K.pop_scale(ln, lt[i] + 0.2)
    pulse = C.sphere("s13_pulse", 0.05, loc=O(cx - 0.62, -0.1, cz + 0.62), m=K.mats()["cyan"],
                     segs=10, rings=8, col_target=st.col)
    K.pop_scale([pulse], 379.6)
    for i in range(3):
        K.move([pulse], 379.8 + i * 2.2, 380.6 + i * 2.2, (1.24, 0, -1.24))
        K.move([pulse], 380.6 + i * 2.2, 381.4 + i * 2.2, (1.24, 0, 1.24))
        K.move([pulse], 381.4 + i * 2.2, 382.2 + i * 2.2, (-1.24, 0, 1.24))
        K.move([pulse], 382.2 + i * 2.2, 383.0 + i * 2.2, (-1.24, 0, -1.24))
    # mismatch chip
    mism = K.node("s13_mism", (1.2, 0.24), O(cx, 0, 0.45), "red",
                  label_text="CALC \u2260 ANSWER \u2192 RECHECK", label_size=0.055,
                  col_target=st.col)
    K.pop_scale(mism, K.W("मैच", 0, 386.4))
    # failure chips
    fails = [("WRONG SITE", "red", 395.4), ("WRONG DATA", "orange", 398.7),
             ("WRONG INPUT", "purple", 400.7), ("MISREAD", "gray", 404.9)]
    for i, (txt, colr, t) in enumerate(fails):
        objs = K.node("s13_f%d" % i, (0.56, 0.2), O(-2.9 + i * 0.68, 0.6, 0.5),
                      colr, label_text=txt, label_size=0.05, col_target=st.col)
        K.pop_scale(objs, t)
    shield = K.icon("s13_shield", "shield", O(cx + 0.75, 0, 0.42), "green", 0.2, st.col)
    K.pop_scale(shield, K.W("वेरिफिकेशन", 0, 405.6))
    lbl = K.label_y("s13_sl", "VERIFY + PERMISSIONS", 0.07, O(cx + 0.75, -0.3, 0.12),
                    color="ink", col_target=st.col, font=K.FONT_EN)
    K.pop_scale([lbl], 406.2)
    cam = assets["cam"]
    K.set_cam_kf(cam, 356.2, (-0.5, -4.6, 1.7), (-0.5, 0, 1.25), st.off3())
    K.cam_path(cam, 372.9, 374.6, (-0.5, -4.6, 1.7), (1.9, -4.0, 1.6), (-0.5, 0, 1.25), (1.9, 0, 1.25), st.off3())
    return {"id": "S13", "t0": 356.2, "t1": 408.1,
            "motion": [[358.9, 370.2], [375.9, 379.6], [379.8, 386.4], [386.4, 387.1],
                       [395.4, 405.6], [372.9, 374.6]]}


# ------------------------------------------------------------------ S14 hallucination
def s14(idx, lib, assets):
    st = K.Stage(idx, "S14")
    O = st.O
    st.pad("pad", 5.6, 3.6)
    st.lights((2.0, -3.5, 4.2), look=(0, 0, 1.1))
    bubble = K.node("s14_b", (2.2, 0.55), O(-0.5, 0, 1.55), "cyan",
                    label_text="THIS ANSWER IS 100% RIGHT!", label_size=0.075,
                    col_target=st.col)
    K.pop_scale(bubble, K.W("जबाब", 1, 411.6))
    cite_labels = ["[1] FakeSource 2019", "[2] WrongDate.org", "[3] Dr. XYZ (NOT REAL)"]
    cites = []
    ct = [418.4, 420.9, 423.5]
    for i, (txt, t) in enumerate(zip(cite_labels, ct)):
        card = C.box("s14_c%d" % i, (1.15, 0.04, 0.24), loc=O(1.35, 0, 1.85 - i * 0.38),
                     m=K.mats()["white"], bevel=0.01, col_target=st.col)
        K.pop_scale([card], t - 0.35)
        t1 = K.label_y("s14_ct%d" % i, txt, 0.055, O(1.35, -0.035, 1.85 - i * 0.38),
                       color="ink", col_target=st.col, font=K.FONT_EN)
        K.pop_scale([t1], t - 0.3)
        cx = K.icon("s14_cx%d" % i, "cross", O(2.02, 0, 1.85 - i * 0.38), "red", 0.09, st.col)
        K.pop_scale(cx, t)
        cites += [card, t1, cx]
    # probability bars 426.2
    bars = []
    import random
    random.seed(7)
    for i in range(6):
        h = 0.2 + (i % 3) * 0.22
        b = C.box("s14_pb%d" % i, (0.16, 0.06, h), loc=O(-1.6 + i * 0.28, -0.4, 0.75 + h / 2),
                  m=K.mats()["blue"], col_target=st.col)
        K.pop_scale([b], 426.4 + i * 0.08)
        bars.append(b)
    lblp = K.label_y("s14_plbl", "LIKELY WORDS...", 0.08, O(-1.0, -0.4, 0.35), color="ink",
                     col_target=st.col, font=K.FONT_EN)
    K.pop_scale([lblp], 427.8)
    # self-monitor panel
    panel = K.node("s14_panel", (1.7, 0.3), O(0.3, -0.75, 1.7), "purple",
                   label_text="SELF-MONITORING", label_size=0.075, col_target=st.col)
    K.pop_scale(panel, K.W("मूनिटरिंग", 0, 431.5))
    chips = [("LOW EVIDENCE", "orange", 434.8), ("VERIFY FIRST", "teal", 438.6),
             ("HUMAN HELP", "blue", 442.0)]
    for i, (txt, colr, t) in enumerate(chips):
        objs = K.node("s14_sc%d" % i, (0.72, 0.22), O(-0.6 + i * 0.85, -0.75, 1.32),
                      colr, label_text=txt, label_size=0.055, col_target=st.col)
        K.pop_scale(objs, t)
    badge = K.icon("s14_badge", "check", O(1.45, -0.75, 1.7), "green", 0.16, st.col)
    K.pop_scale(badge, K.W("बेहविर", 0, 444.1))
    # doctor mini-scene
    doc = C.copy_hierarchy(assets["surgeon"]["root"], st.col, O(-1.9, 0.35, 0))
    K.pop_scale([doc], 446.8)
    test = K.icon("s14_test", "magnifier", O(-1.2, -0.35, 1.6), "teal", 0.16, st.col)
    K.pop_scale(test, K.W("तैस्त", 0, 447.6))
    op2 = K.node("s14_op", (0.85, 0.22), O(-0.85, -0.35, 1.55), "blue",
                 label_text="2nd OPINION", label_size=0.055, col_target=st.col)
    K.pop_scale(op2, 451.0)
    spec = K.arrow("s14_arr", O(-0.35, -0.3, 1.5), O(0.35, -0.3, 1.5), color="purple",
                   col_target=st.col)
    K.pop_scale(spec, 453.0)
    specl = K.label_y("s14_specl", "SPECIALIST", 0.07, O(0.75, -0.35, 1.5), color="purple",
                      col_target=st.col, font=K.FONT_EN)
    K.pop_scale([specl], 453.6)
    cam = assets["cam"]
    K.set_cam_kf(cam, 409.0, (0.0, -4.3, 1.6), (0, 0, 1.25), st.off3())
    K.cam_path(cam, 446.4, 447.6, (0.0, -4.3, 1.6), (-1.4, -3.6, 1.4), (0, 0, 1.25), (-1.4, 0, 0.95), st.off3())
    return {"id": "S14", "t0": 409.0, "t1": 455.6,
            "motion": [[411.6, 412.3], [418.0, 424.2], [426.4, 427.4], [431.5, 432.2],
                       [434.8, 442.7], [444.1, 444.8], [446.8, 447.5], [447.6, 448.3],
                       [451.0, 453.7], [446.4, 447.6]]}


# ------------------------------------------------------------------ S15 continual learning
def s15(idx, lib, assets):
    st = K.Stage(idx, "S15")
    O = st.O
    st.pad("pad", 6.4, 3.6)
    st.lights((1.5, -3.5, 4.5), look=(0, 0, 1.0))
    # timeline bar
    bar = C.box("s15_bar", (5.0, 0.05, 0.08), loc=O(0, -1.4, 0.25), m=K.mats()["gray"],
                col_target=st.col)
    K.pop_scale([bar], 456.2)
    # student + growing subject stack
    stu = C.copy_hierarchy(assets["student"]["root"], st.col, O(-2.4, 0.3, 0))
    K.pop_scale([stu], 456.8)
    subj = ["MATH", "SCIENCE", "HISTORY", "ART"]
    for i, s in enumerate(subj):
        b = C.box("s15_sub%d" % i, (0.5, 0.36, 0.14), loc=O(-2.4, -0.5, 0.2 + i * 0.16),
                  m=K.mats()["blue"] if i % 2 == 0 else K.mats()["teal"], bevel=0.015,
                  col_target=st.col)
        K.pop_scale([b], K.W("सब्ज्ट्", i, 464.6 + i * 0.4))
    # AI zone: knowledge blocks + shield
    ai = K.node("s15_ai", (1.0, 0.5), O(0.9, 0.25, 1.35), "purple", label_text="AI SYSTEM",
                label_size=0.075, col_target=st.col)
    K.pop_scale(ai, 469.3)
    shield = K.icon("s15_shield", "shield", O(1.75, 0.15, 1.5), "green", 0.2, st.col)
    K.pop_scale(shield, K.W("प्रिजव", 0, 471.6))
    # catastrophic forgetting 475.9-484.3
    chem = C.box("s15_chem", (0.5, 0.36, 0.14), loc=O(0.9, -0.35, 1.0), m=K.mats()["green"],
                 bevel=0.015, col_target=st.col)
    chemt = K.label_y("s15_chemt", "CHEMISTRY+", 0.055, O(0.9, -0.39, 1.0), color="white",
                      col_target=st.col, font=K.FONT_EN)
    K.pop_scale([chem, chemt], 476.6)
    mathb = C.box("s15_mathb", (0.5, 0.36, 0.14), loc=O(0.15, -0.35, 1.0), m=K.mats()["blue"],
                  bevel=0.015, col_target=st.col)
    matht = K.label_y("s15_matht", "MATH", 0.06, O(0.15, -0.39, 1.0), color="white",
                      col_target=st.col, font=K.FONT_EN)
    K.pop_scale([mathb, matht], 477.4)
    K.move([mathb, matht], 479.6, 481.0, (0, 0, -0.72))
    for ob in [mathb, matht]:
        C.kf_color(ob, f(479.4), (0.62, 0.64, 0.66, 1))
    warn = K.label_y("s15_warn", "CATASTROPHIC FORGETTING!", 0.09, O(0.9, -0.5, 0.42),
                     color="red", col_target=st.col, font=K.FONT_EN)
    K.pop_scale([warn], 481.6)
    # mitigation 488.4-503: replay + safe update valve
    replay = K.icon("s15_replay", "memory", O(2.4, 0, 1.35), "blue", 0.2, st.col)
    K.pop_scale(replay, 489.2)
    rellbl = K.label_y("s15_rellbl", "REPLAY OLD SKILLS", 0.07, O(2.4, -0.35, 0.95),
                       color="ink", col_target=st.col, font=K.FONT_EN)
    K.pop_scale([rellbl], 490.0)
    a1 = K.arrow("s15_a1", O(2.15, 0, 1.35), O(1.45, 0.1, 1.35), color="blue", col_target=st.col)
    K.pop_scale(a1, 490.8)
    valve = K.icon("s15_valve", "lock", O(3.1, 0, 1.85), "orange", 0.16, st.col)
    K.pop_scale(valve, 492.0)
    vlbl = K.label_y("s15_vlbl", "SAFE SLOW UPDATES", 0.065, O(3.1, -0.35, 1.55),
                     color="ink", col_target=st.col, font=K.FONT_EN)
    K.pop_scale([vlbl], 492.7)
    cam = assets["cam"]
    K.set_cam_kf(cam, 455.6, (-1.2, -4.2, 1.5), (-1.0, 0, 0.9), st.off3())
    K.cam_path(cam, 469.0, 470.4, (-1.2, -4.2, 1.5), (1.2, -3.8, 1.5), (-1.0, 0, 0.9), (1.2, 0, 1.1), st.off3())
    return {"id": "S15", "t0": 455.6, "t1": 503.0,
            "motion": [[456.2, 456.8], [456.8, 457.4], [464.6, 466.4], [469.3, 469.9],
                       [471.6, 472.2], [476.6, 477.8], [479.6, 481.0], [481.6, 482.3],
                       [489.2, 493.4], [469.0, 470.4]]}


# ------------------------------------------------------------------ S16 MoE
def s16(idx, lib, assets):
    st = K.Stage(idx, "S16")
    O = st.O
    st.pad("pad", 6.4, 3.8)
    st.lights((1.5, -3.5, 4.5), look=(0, 0, 1.0))
    # hospital
    hosp = C.box("s16_hosp", (1.4, 0.7, 1.0), loc=O(-2.3, 0.1, 0.5), m=K.mats()["white"],
                 bevel=0.04, col_target=st.col)
    cross_v = C.box("s16_cv", (0.12, 0.06, 0.4), loc=O(-2.3, -0.28, 1.25), m=K.mats()["red"],
                    col_target=st.col)
    cross_h = C.box("s16_ch", (0.4, 0.06, 0.12), loc=O(-2.3, -0.28, 1.25), m=K.mats()["red"],
                    col_target=st.col)
    K.pop_scale([hosp, cross_v, cross_h], 503.8)
    doc1 = K.node("s16_d1", (0.6, 0.26), O(-2.75, -0.45, 1.35), "blue",
                  label_text="AI DR", label_size=0.06, col_target=st.col)
    doc2 = K.node("s16_d2", (0.6, 0.26), O(-1.9, -0.45, 1.35), "teal",
                  label_text="BONE DR", label_size=0.055, col_target=st.col)
    K.pop_scale(doc1 + doc2, 505.9)
    # router + experts
    router = K.node("s16_router", (0.85, 0.4), O(0, 0, 1.75), "orange",
                    label_text="ROUTER", label_size=0.075, col_target=st.col)
    K.pop_scale(router, K.W("राईअटर", 0, 514.0))
    experts = [("MATH", "blue", 516.5), ("CODING", "purple", 517.5), ("LANGUAGE", "green", 518.5)]
    exp_objs = {}
    for i, (txt, colr, t) in enumerate(experts):
        objs = K.node("s16_e%d" % i, (0.75, 0.4), O(-1.1 + i * 1.1, 0, 0.6), colr,
                      label_text=txt, label_size=0.065, col_target=st.col)
        K.pop_scale(objs, t)
        exp_objs[txt] = objs
    inp = K.node("s16_in", (0.85, 0.26), O(-1.15, 0, 2.35), "gray",
                 label_text="2+2/2 = ? (MATH)", label_size=0.05, col_target=st.col)
    K.pop_scale(inp, 515.5)
    a1 = K.arrow("s16_a0", O(-0.7, 0, 2.3), O(-0.1, 0, 1.95), color="gray", col_target=st.col)
    K.pop_scale(a1, 515.9)
    # path lights: router -> math expert only
    p1 = K.arrow("s16_p1", O(-0.25, 0, 1.6), O(-0.85, 0, 0.85), color="blue", col_target=st.col)
    K.pop_scale(p1, 519.5)
    glow = K.glow_ring("s16_glow", 0.5, O(-1.1, 0, 0.6), "yellow", st.col, tube=0.016)
    K.pop_scale([glow], 519.9)
    # resource gauge
    gbar = C.box("s16_gb", (1.3, 0.05, 0.16), loc=O(1.55, 0, 1.75), m=K.mats()["lgray"],
                 col_target=st.col)
    gfill = C.box("s16_gf", (1.2, 0.06, 0.12), loc=O(0.98, 0, 1.75), m=K.mats()["green"],
                  col_target=st.col)
    gfill.scale = (0.02, 1, 1)
    gfill.keyframe_insert("scale", frame=f(524.6))
    gfill.scale = (1, 1, 1)
    gfill.keyframe_insert("scale", frame=f(527.4))
    K.pop_scale([gbar], 524.4)
    glbl = K.label_y("s16_glbl", "RESOURCES SAVED", 0.065, O(1.55, -0.3, 1.5), color="ink",
                     col_target=st.col, font=K.FONT_EN)
    K.pop_scale([glbl], 525.2)
    # risks
    risks = [("WRONG EXPERT", "red", 529.6), ("UNEQUAL LOAD", "orange", 533.0),
             ("\u2260 HUMAN INTELLIGENCE", "gray", 535.2)]
    for i, (txt, colr, t) in enumerate(risks):
        objs = K.node("s16_r%d" % i, (1.0, 0.22), O(0.15, -0.75, 1.15 - i * 0.34),
                      colr, label_text=txt, label_size=0.05, col_target=st.col)
        K.pop_scale(objs, t)
    cam = assets["cam"]
    K.set_cam_kf(cam, 503.3, (-2.0, -4.2, 1.4), (-2.2, 0, 0.8), st.off3())
    K.cam_path(cam, 513.4, 515.0, (-2.0, -4.2, 1.4), (0.4, -4.0, 1.55), (-2.2, 0, 0.8), (0.3, 0, 1.15), st.off3())
    return {"id": "S16", "t0": 503.3, "t1": 538.9,
            "motion": [[503.8, 504.5], [505.9, 506.6], [514.0, 519.0], [519.5, 520.6],
                       [524.4, 527.4], [529.6, 536.0], [513.4, 515.0]]}


# ------------------------------------------------------------------ S17 transfer
def s17(idx, lib, assets):
    st = K.Stage(idx, "S17")
    O = st.O
    st.pad("pad", 6.8, 3.8)
    st.lights((1.5, -3.5, 4.5), look=(0, 0, 0.9))

    def bike(name, x, z=0.36, colr="blue"):
        w1 = C.torus(name + "_w1", 0.17, 0.03, loc=O(x, 0, z), rot=(0, math.radians(90), 0),
                     m=K.mats()["dark"], col_target=st.col)
        w2 = C.torus(name + "_w2", 0.17, 0.03, loc=O(x + 0.62, 0, z), rot=(0, math.radians(90), 0),
                     m=K.mats()["dark"], col_target=st.col)
        f1 = C.cyl(name + "_f1", 0.02, 0.5, loc=O(x + 0.31, 0, z + 0.12),
                   rot=(0, math.radians(70), 0), m=K.mats()[colr], verts=8, col_target=st.col)
        h = C.cyl(name + "_h", 0.025, 0.34, loc=O(x + 0.12, 0, z + 0.3),
                  rot=(math.radians(30), 0, 0), m=K.mats()[colr], verts=8, col_target=st.col)
        return [w1, w2, f1, h]
    b1 = bike("s17_bike", -2.5, colr="teal")
    stu = C.copy_hierarchy(assets["student"]["root"], st.col, O(-2.25, 0.0, 0.28))
    for ob in [stu]:
        ob.scale = (1, 1, 1)
    K.pop_scale(b1, 541.8)
    K.pop_scale([stu], 542.2)
    moto = bike("s17_moto", -0.9, colr="orange")
    K.pop_scale(moto, K.W("motorcycle", 0, 545.2))
    arc = K.arrow("s17_arc", O(-2.1, -0.4, 1.3), O(-0.7, -0.4, 1.3), r=0.02, color="purple",
                  col_target=st.col)
    K.pop_scale(arc, K.W("transfer", 0, 549.9))
    lbl = K.label_y("s17_lbl", "BALANCE + ROAD + STEERING", 0.07, O(-1.5, -0.4, 1.55),
                    color="purple", col_target=st.col, font=K.FONT_EN)
    K.pop_scale([lbl], 548.0)
    # maths -> physics
    m1 = K.node("s17_m", (0.6, 0.24), O(1.3, 0.1, 1.45), "blue", label_text="MATH PATTERNS",
                label_size=0.05, col_target=st.col)
    m2 = K.node("s17_p", (0.7, 0.24), O(2.45, 0.1, 1.45), "green", label_text="PHYSICS",
                label_size=0.06, col_target=st.col)
    K.pop_scale(m1, 552.8)
    K.pop_scale(m2, 554.0)
    a2 = K.arrow("s17_a2", O(1.62, 0.1, 1.45), O(2.05, 0.1, 1.45), color="green", col_target=st.col)
    K.pop_scale(a2, 554.8)
    # AI transfer diagram
    ta = K.node("s17_ta", (0.62, 0.24), O(1.0, 0.1, 0.8), "teal", label_text="TASK A",
                label_size=0.055, col_target=st.col)
    rep = K.node("s17_rep", (0.8, 0.24), O(1.85, 0.1, 0.8), "purple", label_text="REPRESENTATION",
                 label_size=0.045, col_target=st.col)
    tb = K.node("s17_tb", (0.62, 0.24), O(2.75, 0.1, 0.8), "orange", label_text="TASK B",
                label_size=0.055, col_target=st.col)
    K.pop_scale(ta, 558.0)
    K.pop_scale(rep, 558.6)
    K.pop_scale(tb, 559.2)
    # failures
    f1 = K.node("s17_f1", (1.3, 0.22), O(-1.4, -0.7, 0.5), "red",
                label_text="GAME \u2192 BUSINESS: FAIL", label_size=0.045, col_target=st.col)
    K.pop_scale(f1, K.W("business", 0, 566.4))
    f2 = K.node("s17_f2", (1.3, 0.22), O(-1.4, -0.7, 0.22), "orange",
                label_text="LAB DATA \u2260 REAL ROAD", label_size=0.045, col_target=st.col)
    K.pop_scale(f2, K.W("रोट", 0, 568.9))
    gnd = K.node("s17_gnd", (1.1, 0.26), O(1.9, -0.7, 0.36), "blue",
                 label_text="GROUNDING NEEDED", label_size=0.05, col_target=st.col)
    K.pop_scale(gnd, K.W("ग्रूंटिंग", 0, 572.0))
    cam = assets["cam"]
    K.set_cam_kf(cam, 538.9, (-0.8, -4.4, 1.35), (-0.8, 0, 0.8), st.off3())
    K.cam_path(cam, 557.0, 558.6, (-0.8, -4.4, 1.35), (1.9, -3.8, 1.3), (-0.8, 0, 0.8), (1.9, 0, 1.0), st.off3())
    return {"id": "S17", "t0": 538.9, "t1": 577.0,
            "motion": [[541.8, 542.5], [545.2, 545.9], [548.0, 550.6], [552.8, 555.5],
                       [558.0, 559.9], [566.4, 569.6], [572.0, 572.7], [557.0, 558.6]]}


# ------------------------------------------------------------------ S18 ARCHITECTURE (hero)
def s18(idx, lib, assets):
    st = K.Stage(idx, "S18")
    O = st.O
    st.pad("pad", 7.4, 5.0, color="floor2")
    st.lights((2.0, -4.0, 5.0), look=(0, 0, 1.3), fill_loc=(-3, -2, 3))
    R = 2.0
    mods = [
        ("PERCEPTION", "teal", 90), ("WORKING MEM", "cyan", 50),
        ("LONG-TERM MEM", "blue", 10), ("PLANNER", "orange", -30),
        ("WORLD MODEL", "purple", -70), ("TOOLS", "green", -110),
        ("FEEDBACK", "gray", -150), ("CONT. LEARNING", "yellow", 170),
        ("VERIFICATION", "red", 130),
    ]
    appear_t = [583.7, 591.3, 593.3, 596.5, 598.6, 601.2, 604.1, 607.4, 610.3]
    mod_pos = {}
    mod_objs = {}
    for i, (txt, colr, ang) in enumerate(mods):
        a = math.radians(ang)
        x, z = R * math.cos(a) * 1.25, R * math.sin(a) * 0.72 + 1.35
        objs = K.node("s18_m%d" % i, (0.78, 0.4), O(x, 0, z), colr,
                      label_text=txt, label_size=0.052, col_target=st.col)
        K.pop_scale(objs, appear_t[i])
        mod_pos[txt] = (x, z)
        mod_objs[txt] = objs
    core = K.node("s18_core", (1.15, 1.15), O(0, 0, 1.35), "blue",
                  label_text="TRANSFORMER", label_size=0.085, col_target=st.col)
    K.pop_scale(core, K.W("रीजनिंग", 0, 587.4))
    ring = K.glow_ring("s18_ring", 0.78, O(0, 0, 1.35), "cyan", st.col, tube=0.02)
    K.pop_scale([ring], 588.4)
    # connections
    conns = []
    for txt, (x, z) in mod_pos.items():
        ln = K.line3d("s18_c_" + txt[:6], O(x * 0.86, 0, 1.35 + (z - 1.35) * 0.86),
                      O(x * 0.62, 0, 1.35 + (z - 1.35) * 0.62), r=0.012, color="lgray",
                      col_target=st.col)
        K.pop_scale(ln, 613.1)
        conns.append((txt, ln))
    # flow pulses 612.9-635
    flow_seq = [
        ("PERCEPTION", K.W("भेद्द", 0, 615.5)), ("PLANNER", K.W("समजा", 0, 618.3)),
        ("TOOLS", K.W("अक्षें", 0, 620.4)), ("FEEDBACK", K.W("मिल", 1, 622.3)),
        ("WORLD MODEL", K.W("अंदाजा", 1, 624.5)), ("VERIFICATION", K.W("कह", 0, 627.2)),
    ]
    pulses = []
    for j, (txt, t) in enumerate(flow_seq):
        x, z = mod_pos[txt]
        p = C.sphere("s18_p%d" % j, 0.055, loc=O(x * 0.86, -0.12, 1.35 + (z - 1.35) * 0.86),
                     m=K.mats()["cyan"], segs=10, rings=8, col_target=st.col)
        K.pop_scale([p], t)
        K.move([p], t + 0.15, t + 1.1, (-x * 0.24, 0.12, -(z - 1.35) * 0.24))
        pulses.append(p)
    nxt = K.node("s18_next", (0.9, 0.26), O(0, -0.9, 0.45), "green",
                 label_text="NEXT STEP CHOSEN", label_size=0.055, col_target=st.col)
    K.pop_scale(nxt, K.W("नेक", 0, 633.5))
    cam = assets["cam"]
    K.set_cam_kf(cam, 577.0, (0.0, -5.6, 1.0), (0, 0, 1.1), st.off3())
    K.cam_path(cam, 580.4, 583.4, (0.0, -5.6, 1.0), (0.0, -4.9, 1.7), (0, 0, 1.1), (0, 0, 1.35), st.off3())
    K.cam_path(cam, 612.6, 614.0, (0.0, -4.9, 1.7), (0.4, -4.5, 1.85), (0, 0, 1.35), (0.1, 0, 1.35), st.off3())
    return {"id": "S18", "t0": 577.0, "t1": 635.0,
            "motion": [[580.4, 583.4], [583.7, 611.0], [613.1, 613.9], [615.5, 634.6],
                       [612.6, 614.0]]}


# ------------------------------------------------------------------ S19 coordination
def s19(idx, lib, assets):
    st = K.Stage(idx, "S19")
    O = st.O
    st.pad("pad", 7.0, 4.4, color="floor2")
    st.lights((2.0, -4.0, 5.0), look=(0, 0, 1.2))
    mods = [("MEMORY", -2.3, 1.75), ("PLANNER", -0.8, 1.75), ("WORLD MODEL", 0.8, 1.75),
            ("TOOLS", 2.3, 1.75), ("CONT. LEARNING", -1.5, 0.85), ("SYSTEM", 1.5, 0.85)]
    cols = ["blue", "orange", "purple", "green", "yellow", "teal"]
    mod_objs = []
    for i, (txt, x, z) in enumerate(mods):
        objs = K.node("s19_m%d" % i, (0.85, 0.38), O(x, 0, z), cols[i],
                      label_text=txt, label_size=0.055, col_target=st.col)
        K.pop_scale(objs, 635.6 + i * 0.12)
        mod_objs.append(objs)
    fails = [("WRONG DETAIL SAVED", "MEMORY", 643.2), ("WRONG GOAL", "PLANNER", 647.8),
             ("BAD PREDICTION", "WORLD MODEL", 651.9), ("MISUSE", "TOOLS", 654.0),
             ("UNSAFE UPDATE", "CONT. LEARNING", 656.5)]
    for i, (txt, target, t) in enumerate(fails):
        x = [m[1] for m in mods if m[0] == target][0]
        z = [m[2] for m in mods if m[0] == target][0]
        cx = K.icon("s19_fx%d" % i, "cross", O(x, -0.1, z + 0.33), "red", 0.13, st.col)
        K.pop_scale(cx, t)
        lbl = K.label_y("s19_fl%d" % i, txt, 0.042, O(x, -0.12, z - 0.3), color="red",
                        col_target=st.col, font=K.FONT_EN)
        K.pop_scale([lbl], t + 0.15)
    # lab vs real
    lab = K.node("s19_lab", (0.8, 0.26), O(-0.9, -0.55, 0.42), "green",
                 label_text="LAB: GOOD \u2713", label_size=0.055, col_target=st.col)
    real = K.node("s19_real", (1.0, 0.26), O(0.9, -0.55, 0.42), "red",
                  label_text="REAL WORLD: WEAK \u2717", label_size=0.045, col_target=st.col)
    K.pop_scale(lab, 660.8)
    K.pop_scale(real, 661.6)
    # company org chart
    dept = ["SALES", "ENG", "QA", "OPS"]
    dobjs = []
    for i, d in enumerate(dept):
        objs = K.node("s19_d%d" % i, (0.55, 0.24), O(-1.2 + i * 0.8, 0.55, 2.35), "blue",
                      label_text=d, label_size=0.055, col_target=st.col)
        K.pop_scale(objs, 664.0 + i * 0.15)
        dobjs.append(objs)
    for i in range(3):
        ln = K.line3d("s19_dl%d" % i, O(-0.85 + i * 0.8, 0.5, 2.35), O(-0.45 + i * 0.8, 0.5, 2.35),
                      r=0.014, color="red", col_target=st.col)
        K.pop_scale(ln, 672.0 + i * 0.1)
    fail = K.label_y("s19_fail", "PROJECT FAIL!", 0.1, O(0, 0.4, 2.7), color="red",
                     col_target=st.col, font=K.FONT_EN)
    K.pop_scale([fail], 673.6)
    needs = [("COMMUNICATION", "blue", 675.4), ("PRIORITIES", "teal", 676.6),
             ("PERMISSIONS", "orange", 677.8), ("FEEDBACK", "green", 678.9)]
    for i, (txt, colr, t) in enumerate(needs):
        objs = K.node("s19_n%d" % i, (0.68, 0.2), O(-1.7 + i * 1.1, -1.0, 1.3),
                      colr, label_text=txt, label_size=0.05, col_target=st.col)
        K.pop_scale(objs, t)
    cam = assets["cam"]
    K.set_cam_kf(cam, 635.0, (0.0, -4.6, 1.6), (0, 0, 1.2), st.off3())
    K.cam_path(cam, 663.4, 664.6, (0.0, -4.6, 1.6), (0.0, -4.2, 1.8), (0, 0, 1.2), (0, 0.3, 1.9), st.off3())
    K.cam_path(cam, 674.8, 676.0, (0.0, -4.2, 1.8), (0.0, -4.4, 1.4), (0, 0.3, 1.9), (0, -0.4, 1.2), st.off3())
    return {"id": "S19", "t0": 635.0, "t1": 683.4,
            "motion": [[635.6, 636.4], [643.2, 657.6], [660.8, 662.2], [664.0, 674.4],
                       [675.4, 679.6], [663.4, 664.6], [674.8, 676.0]]}


# ------------------------------------------------------------------ S20 big transformer
def s20(idx, lib, assets):
    st = K.Stage(idx, "S20")
    O = st.O
    st.pad("pad", 6.4, 3.6)
    st.lights((1.5, -3.5, 4.5), look=(0, 0, 1.1))
    core = K.node("s20_core", (1.5, 1.2), O(-1.7, 0, 1.3), "blue",
                  label_text="BIGGER TRANSFORMER", label_size=0.07, col_target=st.col)
    K.pop_scale(core, 683.6)
    K.move(core, 684.4, 689.9, (0, 0, 0.35))
    bars = []
    for i in range(4):
        h = 0.25 + i * 0.22
        b = C.box("s20_b%d" % i, (0.2, 0.06, h), loc=O(-2.55 + i * 0.3, -0.4, 0.45 + h / 2),
                  m=K.mats()["cyan"], col_target=st.col)
        K.pop_scale([b], 690.5 + i * 0.25)
        bars.append(b)
    lblb = K.label_y("s20_lblb", "CAPABILITIES \u2191", 0.075, O(-2.1, -0.4, 1.55), color="ink",
                     col_target=st.col, font=K.FONT_EN)
    K.pop_scale([lblb], 691.6)
    # car with engine
    body = C.box("s20_car", (1.6, 0.6, 0.32), loc=O(1.7, 0, 0.36), m=K.mats()["red"],
                 bevel=0.08, col_target=st.col)
    cab = C.box("s20_cab", (0.8, 0.55, 0.3), loc=O(1.85, 0, 0.66), m=K.mats()["red"],
                bevel=0.07, col_target=st.col)
    wheels = []
    for sx in (-1, 1):
        w = C.torus("s20_w%d" % sx, 0.16, 0.05, loc=O(1.7 + sx * 0.5, -0.28, 0.16),
                    rot=(0, math.radians(90), 0), m=K.mats()["dark"], col_target=st.col)
        w2 = C.torus("s20_w2%d" % sx, 0.16, 0.05, loc=O(1.7 + sx * 0.5, 0.28, 0.16),
                     rot=(0, math.radians(90), 0), m=K.mats()["dark"], col_target=st.col)
        wheels += [w, w2]
    eng = C.box("s20_eng", (0.5, 0.45, 0.35), loc=O(1.55, 0, 0.95), m=K.mats()["orange"],
                bevel=0.04, col_target=st.col)
    K.pop_scale([body, cab] + wheels, 693.6)
    K.pop_scale([eng], K.W("एंजन", 0, 694.6))
    parts = [("MEMORY = STORAGE", "blue", 695.6, -0.5, 1.7), ("PLANNING = GPS", "purple", 696.6, 0.1, 1.95),
             ("VERIFY = BRAKES", "green", 697.6, 0.7, 1.6)]
    part_objs = []
    for txt, colr, t, dx, dz in parts:
        objs = K.node("s20_p%s%d" % (txt[:3], int(dz * 10)), (0.85, 0.24), O(2.9 + dx * 0.4, -0.3, dz),
                      colr, label_text=txt, label_size=0.042, col_target=st.col)
        K.pop_scale(objs, t)
        part_objs.append(objs)
    dash1 = K.line3d("s20_d1", O(2.35, -0.3, 0.85), O(2.6, -0.3, 1.5), r=0.008, color="red",
                     col_target=st.col)
    K.pop_scale(dash1, 698.6)
    nlbl = K.label_y("s20_nlbl", "AUTO-CONNECT NAHI HOTE", 0.065, O(1.7, -0.55, 1.35),
                     color="red", col_target=st.col)
    K.pop_scale([nlbl], 699.2)
    eng_l = ["MEMORY MGMT", "LONG PLANNING", "GROUNDING", "VERIFICATION", "SAFE LEARNING"]
    for i, txt in enumerate(eng_l):
        objs = K.node("s20_el%d" % i, (0.62, 0.18), O(-2.6 + i * 0.52, -0.85, 0.35),
                      "gray", label_text=txt, label_size=0.036, col_target=st.col)
        K.pop_scale(objs, 700.5 + i * 0.12)
    cam = assets["cam"]
    K.set_cam_kf(cam, 683.4, (-1.0, -4.0, 1.5), (-1.7, 0, 1.2), st.off3())
    K.cam_path(cam, 693.3, 694.6, (-1.0, -4.0, 1.5), (1.7, -4.0, 1.3), (-1.7, 0, 1.2), (1.7, 0, 0.8), st.off3())
    return {"id": "S20", "t0": 683.4, "t1": 702.3,
            "motion": [[683.6, 690.0], [690.5, 691.5], [693.6, 694.2], [694.6, 698.0],
                       [700.5, 701.2], [693.3, 694.6]]}


# ------------------------------------------------------------------ S21 open question
def s21(idx, lib, assets):
    st = K.Stage(idx, "S21")
    O = st.O
    st.pad("pad", 6.4, 3.8)
    st.lights((1.5, -3.5, 4.5), look=(0, 0, 1.2))
    p1 = K.node("s21_p1", (1.5, 0.6), O(-1.4, 0, 1.55), "blue",
                label_text="ONE GIANT MODEL?", label_size=0.07, col_target=st.col)
    p2 = K.node("s21_p2", (1.5, 0.6), O(1.4, 0, 1.55), "purple",
                label_text="A GROUP OF MODELS?", label_size=0.065, col_target=st.col)
    K.pop_scale(p1, 703.0)
    K.pop_scale(p2, 705.0)
    q1 = K.icon("s21_q1", "question", O(-1.4, -0.05, 2.05), "blue", 0.14, st.col)
    K.pop_scale(q1, 704.0)
    q2 = K.icon("s21_q2", "question", O(1.4, -0.05, 2.05), "purple", 0.14, st.col)
    K.pop_scale(q2, 706.0)
    orb = K.label_y("s21_orb", "OR SOMETHING ELSE?", 0.1, O(0, -0.5, 1.05), color="orange",
                    col_target=st.col)
    K.pop_scale([orb], K.W("अलग", 0, 719.6))
    # speculation collage
    mini = K.node("s21_mini", (1.0, 0.5), O(0, 0.4, 1.85), "teal",
                  label_text="TRANSFORMER + EXPERTS + MEMORY + PLANNER", label_size=0.035,
                  col_target=st.col)
    K.pop_scale(mini, 714.0)
    # no-guarantee stamps
    stamps = [("WORLD MODEL \u2260 CONSCIOUSNESS", 725.2), ("MEMORY \u2260 UNDERSTANDING", 727.8),
              ("TEXT \u2260 RELIABLE ACTION", 730.4), ("MORE LANGUAGE \u2260 REAL LEARNING", 733.2)]
    for i, (txt, t) in enumerate(stamps):
        objs = K.node("s21_s%d" % i, (1.35, 0.22), O(-1.5 + (i % 2) * 3.0, -0.7, 0.72 - (i // 2) * 0.34),
                      "red", label_text=txt, label_size=0.042, col_target=st.col)
        K.pop_scale(objs, t)
    cam = assets["cam"]
    K.set_cam_kf(cam, 702.3, (0.0, -4.3, 1.6), (0, 0, 1.3), st.off3())
    return {"id": "S21", "t0": 702.3, "t1": 737.8,
            "motion": [[703.0, 706.6], [714.0, 714.7], [725.2, 734.0]]}


# ------------------------------------------------------------------ S22 prep questions
def s22(idx, lib, assets):
    st = K.Stage(idx, "S22")
    O = st.O
    st.pad("pad", 5.6, 3.6)
    st.lights((1.5, -3.5, 4.5), look=(0, 0, 1.0))
    stu = C.copy_hierarchy(assets["student"]["root"], st.col, O(-1.7, 0.3, 0))
    K.pop_scale([stu], 743.0)
    dsk = C.box("s22_desk", (0.9, 0.6, 0.04), loc=O(-1.7, -0.35, 0.74), m=K.mats()["white"],
                bevel=0.01, col_target=st.col)
    cards = []
    for i in range(4):
        c = C.box("s22_card%d" % i, (0.3, 0.015, 0.2), loc=O(-1.7, -0.4, 0.86 + i * 0.022),
                  rot=(0, 0, math.radians(-4 + i * 3)), m=K.mats()["yellow"], bevel=0.005,
                  col_target=st.col)
        K.pop_scale([c], 743.6 + i * 0.4)
        cards.append(c)
    for i, c in enumerate(cards):
        K.move([c], 748.0 + i * 1.6, 748.8 + i * 1.6, (0.35, 0.15, 0.05))
    tchr = K.node("s22_tchr", (0.85, 0.24), O(-0.2, 0.35, 1.75), "blue",
                  label_text="TEACHER", label_size=0.055, col_target=st.col)
    K.pop_scale(tchr, 751.0)
    quiz = K.node("s22_quiz", (0.7, 0.22), O(-0.2, 0.35, 1.4), "green",
                  label_text="QUIZZES", label_size=0.06, col_target=st.col)
    K.pop_scale(quiz, 753.0)
    # question stream into big ? 760.8-774.2
    bigq = K.icon("s22_bigq", "question", O(1.7, 0, 1.3), "orange", 0.3, st.col)
    K.pop_scale(bigq, 761.4)
    funnel = []
    for i in range(5):
        q = K.icon("s22_q%d" % i, "question", O(0.1 + i * 0.25, -0.3, 0.7 + (i % 2) * 0.5),
                   "purple", 0.09, st.col)
        K.pop_scale(q, 763.0 + i * 1.3)
        K.move(q, 764.0 + i * 1.3, 765.4 + i * 1.3, (1.35 - i * 0.25, 0.3, 0.6 - (i % 2) * 0.5))
        funnel.append(q)
    arch = K.label_y("s22_arch", "WHICH ARCHITECTURE?", 0.1, O(0, -0.8, 1.85), color="ink",
                     col_target=st.col)
    K.pop_scale([arch], K.W("अरेट्टेक्छीर", 0, 774.6) if False else 773.0)
    cam = assets["cam"]
    K.set_cam_kf(cam, 737.8, (-1.2, -3.8, 1.4), (-1.2, 0, 1.0), st.off3())
    K.cam_path(cam, 760.6, 762.4, (-1.2, -3.8, 1.4), (1.0, -3.8, 1.5), (-1.2, 0, 1.0), (1.4, 0, 1.2), st.off3())
    return {"id": "S22", "t0": 737.8, "t1": 774.2,
            "motion": [[743.0, 745.2], [748.0, 754.0], [761.4, 762.2], [763.0, 770.0],
                       [760.6, 762.4]]}


# ------------------------------------------------------------------ S23 AGI cycle
def s23(idx, lib, assets):
    st = K.Stage(idx, "S23")
    O = st.O
    st.pad("pad", 6.4, 4.0)
    st.lights((1.5, -3.5, 4.8), look=(0, 0, 1.2))
    # crossed meters 794.4-800.1
    meters = ["MORE TEXT", "MORE PARAMS", "MORE FLUENCY"]
    for i, txt in enumerate(meters):
        objs = K.node("s23_m%d" % i, (0.8, 0.24), O(-1.9 + i * 0.75, 0.5, 1.95), "gray",
                      label_text=txt, label_size=0.045, col_target=st.col)
        K.pop_scale(objs, 794.6 + i * 0.35)
        cx = K.icon("s23_cx%d" % i, "cross", O(-1.9 + i * 0.75, 0.42, 2.2), "red", 0.1, st.col)
        K.pop_scale(cx, 796.0 + i * 0.35)
    chips = [("WORKING MEM", "cyan", 777.3), ("LONG-TERM MEM", "blue", 778.3),
             ("PLANNING", "orange", 779.3), ("WORLD MODEL", "purple", 780.3)]
    for i, (txt, colr, t) in enumerate(chips):
        objs = K.node("s23_c%d" % i, (0.66, 0.2), O(-1.8 + i * 1.15, 0.55, 1.45),
                      colr, label_text=txt, label_size=0.05, col_target=st.col)
        K.pop_scale(objs, t)
    # the six-step cycle
    cyc = [("SEE", "teal", 800.8), ("REMEMBER", "blue", 801.7), ("PLAN", "orange", 802.6),
           ("ACT", "green", 803.5), ("CHECK", "red", 804.4), ("SAFE UPDATE", "purple", 805.6)]
    pos = []
    for i in range(6):
        a = math.radians(90 - i * 60)
        pos.append((2.0 * math.cos(a) * 0.85, 1.15 + 1.05 * math.sin(a)))
    for i, (txt, colr, t) in enumerate(cyc):
        x, z = pos[i]
        objs = K.node("s23_s%d" % i, (0.6, 0.3), O(x, 0, z), colr,
                      label_text=txt, label_size=0.052, col_target=st.col)
        K.pop_scale(objs, t)
        if i > 0:
            x0, z0 = pos[i - 1]
            ln = K.line3d("s23_l%d" % i, O(x0 * 0.88, 0, 1.15 + (z0 - 1.15) * 0.88),
                          O(x * 0.88, 0, 1.15 + (z - 1.15) * 0.88), r=0.013, color="gray",
                          col_target=st.col)
            K.pop_scale(ln, t)
    x0, z0 = pos[5]
    ln = K.line3d("s23_l0", O(x0 * 0.88, 0, 1.15 + (z0 - 1.15) * 0.88),
                  O(pos[0][0] * 0.88, 0, 1.15 + (pos[0][1] - 1.15) * 0.88), r=0.013,
                  color="gray", col_target=st.col)
    K.pop_scale(ln, 806.6)
    title = K.label_y("s23_t", "COMPLETE SYSTEM CYCLE", 0.1, O(0, -0.7, 2.15), color="ink",
                      col_target=st.col, font=K.FONT_EN)
    K.pop_scale([title], K.W("कमप्लीट", 1, 806.9))
    cam = assets["cam"]
    K.set_cam_kf(cam, 774.2, (0.0, -4.4, 1.55), (0, 0, 1.25), st.off3())
    K.cam_path(cam, 794.2, 795.4, (0.0, -4.4, 1.55), (0.0, -4.0, 1.45), (0, 0, 1.25), (0, 0, 1.2), st.off3())
    return {"id": "S23", "t0": 774.2, "t1": 809.8,
            "motion": [[777.3, 781.0], [794.6, 797.2], [800.8, 806.0], [794.2, 795.4]]}


# ------------------------------------------------------------------ S24 conclusion
def s24(idx, lib, assets):
    st = K.Stage(idx, "S24")
    O = st.O
    st.pad("pad", 7.0, 4.6, color="floor2")
    st.lights((2.0, -4.0, 5.0), look=(0, 0, 1.3), fill_loc=(-3, -2, 3))
    core = K.node("s24_core", (1.1, 1.1), O(0, 0, 1.35), "blue",
                  label_text="TRANSFORMER", label_size=0.08, col_target=st.col)
    K.pop_scale(core, K.W("सिस्तम", 3, 810.4))
    ring = K.glow_ring("s24_ring", 0.75, O(0, 0, 1.35), "cyan", st.col, tube=0.02)
    K.pop_scale([ring], K.W("कोर", 0, 818.6))
    mods = [("MEMORY", 130), ("PLANNING", 90), ("WORLD MODELS", 50),
            ("TOOLS", -130), ("LEARNING", -90), ("VERIFICATION", -50)]
    objs_all = []
    for i, (txt, ang) in enumerate(mods):
        a = math.radians(ang)
        x, z = 1.9 * math.cos(a), 1.35 + 1.0 * math.sin(a)
        objs = K.node("s24_m%d" % i, (0.7, 0.32), O(x, 0, z), "teal" if i % 2 else "blue",
                      label_text=txt, label_size=0.045, col_target=st.col)
        K.pop_scale(objs, 820.9 + i * 0.35)
        ln = K.line3d("s24_l%d" % i, O(x * 0.8, 0, 1.35 + (z - 1.35) * 0.8),
                      O(x * 0.6, 0, 1.35 + (z - 1.35) * 0.6), r=0.01, color="lgray",
                      col_target=st.col)
        K.pop_scale(ln, 821.2 + i * 0.35)
        objs_all.append(objs)
    t1 = K.label_y("s24_t1", "CONNECTED COGNITIVE SYSTEM", 0.12, O(0, -0.6, 2.45), color="ink",
                   col_target=st.col, font=K.FONT_EN)
    K.pop_scale([t1], K.W("कनेक्टेड", 0, 815.2))
    t2 = K.label_y("s24_t2", "POWERFUL AI: YES - COMPLETE AGI: NOT YET", 0.075,
                   O(0, -0.6, 0.42), color="orange", col_target=st.col, font=K.FONT_EN)
    K.pop_scale([t2], K.W("कम्ठीत", 0, 835.2))
    cam = assets["cam"]
    K.set_cam_kf(cam, 809.8, (0.0, -4.8, 1.65), (0, 0, 1.3), st.off3())
    K.cam_path(cam, 812.0, 815.0, (0.0, -4.8, 1.65), (0.0, -4.3, 1.5), (0, 0, 1.3), (0, 0, 1.35), st.off3())
    return {"id": "S24", "t0": 809.8, "t1": 838.0,
            "motion": [[810.4, 811.0], [812.0, 815.0], [815.2, 815.9], [818.6, 819.3],
                       [820.9, 824.0], [835.2, 835.9], [812.0, 815.0]]}


def build_all(idx0, lib, assets):
    shots = []
    shots.append(s13(idx0 + 0, lib, assets))
    shots.append(s14(idx0 + 1, lib, assets))
    shots.append(s15(idx0 + 2, lib, assets))
    shots.append(s16(idx0 + 3, lib, assets))
    shots.append(s17(idx0 + 4, lib, assets))
    shots.append(s18(idx0 + 5, lib, assets))
    shots.append(s19(idx0 + 6, lib, assets))
    shots.append(s20(idx0 + 7, lib, assets))
    shots.append(s21(idx0 + 8, lib, assets))
    shots.append(s22(idx0 + 9, lib, assets))
    shots.append(s23(idx0 + 10, lib, assets))
    shots.append(s24(idx0 + 11, lib, assets))
    return shots
