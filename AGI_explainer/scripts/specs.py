"""specs.py — v3: 20 window-driven sequence specs + builders.
TEXT RULE: every string below <= 3 English words (+ symbols). English only.
Anchors = word stems searched in transcript (first match anchors window)."""
import math
from lib_scene import (box, sphere, cyl, torus, text3d, chip, crate,
                       rise, scale_in, spin, move, kf_scale,
                       C_INK, C_ACCENT, C_CYAN, C_GREEN, C_RED, C_PURPLE,
                       C_GREY, C_TEAL, C_AMBER, C_BLUE, C_BG)


def _title(f0, f1, body, z=5.8, size=1.5, color=C_INK):
    t = text3d('title', body, (0, 0, z), size=size, color=color)
    scale_in(t, f0 + 8, f0 + 26)
    return t


def b_s01(f0, f1):
    _title(f0, f1, "AGI Architecture", z=5.2, size=1.6)
    a = box('core', (0, 0, 2.2), (2.2, 2.2, 2.2), C_ACCENT)
    b = box('mid', (0, 0, 2.2), (3.4, 3.4, 3.4), C_PURPLE)
    c = box('shell', (0, 0, 2.2), (4.8, 4.8, 4.8), C_CYAN)
    spin(a, f0 + 20, f1, 2.0)
    spin(b, f0 + 20, f1, -1.2, 'Y')
    spin(c, f0 + 20, f1, 0.6)


def b_s02(f0, f1):
    q = text3d('qmark', "?", (0, 0, 2.4), size=4.2, color=C_ACCENT)
    scale_in(q, f0 + 8, f0 + 24)
    cols = [(C_CYAN, -5.0), (C_GREEN, -1.8), (C_PURPLE, 1.8), (C_RED, 5.0)]
    for i, (c, x) in enumerate(cols):
        b, t = chip(f'chip{i}', ["Reasoning", "Memory", "Agents", "Safety"][i],
                    (x, -1.5, 0.8), c)
        rise(b, f0 + 30 + i * 14, f0 + 60 + i * 14, 1.6)
        rise(t, f0 + 30 + i * 14, f0 + 60 + i * 14, 1.6)


def b_s03(f0, f1):
    _title(f0, f1, "Bigger Model")
    cols = [C_GREY, C_GREY, C_BLUE, C_BLUE, C_ACCENT]
    for i, c in enumerate(cols):
        s = box(f'st{i}', (-6 + i * 3, 0, 0.5 + i * 0.85),
                (2.4, 2.4, 1.0 + i * 1.7), c)
        rise(s, f0 + 10 + i * 12, f0 + 40 + i * 12, 0.4)
    n = text3d('note', "≠ AGI", (7.6, 0, 6.2), size=1.0, color=C_RED)
    scale_in(n, f0 + 90, f0 + 110)


def b_s04(f0, f1):
    _title(f0, f1, "Transformer = AGI?")
    for i in range(4):
        s = box(f'slab{i}', (0, 0, 1.0 + i * 1.35),
                (5.2, 3.2, 0.5), [C_CYAN, C_BLUE, C_PURPLE, C_CYAN][i])
        rise(s, f0 + 10 + i * 16, f0 + 42 + i * 16, 0.3)
        spin(s, f0 + 60, f1, 0.25, 'Z')
    b, t = chip('qkv', "Q · K · V", (-6.4, -1.2, 1.4), C_AMBER)
    rise(b, f0 + 90, f0 + 110, 1.2); rise(t, f0 + 90, f0 + 110, 1.2)
    b, t = chip('heads', "Heads", (6.4, -1.2, 1.4), C_GREEN)
    rise(b, f0 + 110, f0 + 130, 1.2); rise(t, f0 + 110, f0 + 130, 1.2)


def b_s05(f0, f1):
    _title(f0, f1, "Reasoning Core")
    pts = [(-6, 1.2), (-3.6, 2.4), (-1.2, 1.6), (1.2, 2.8),
           (3.6, 1.8), (6, 2.6)]
    for i, (x, z) in enumerate(pts):
        s = sphere(f'node{i}', (x, 0, z), 0.55,
                   C_CYAN if i % 2 else C_INK)
        scale_in(s, f0 + 10 + i * 14, f0 + 34 + i * 14)
    for i in range(5):
        x0, z0 = pts[i]; x1, z1 = pts[i + 1]
        cx, cz = (x0 + x1) / 2, (z0 + z1) / 2
        ln = math.hypot(x1 - x0, z1 - z0)
        ang = math.atan2(z1 - z0, x1 - x0)
        link = box(f'link{i}', (cx, 0, cz), (ln, 0.12, 0.12), C_GREY,
                   rot=(0, 0, ang))
        scale_in(link, f0 + 24 + i * 14, f0 + 44 + i * 14)


def b_s06(f0, f1):
    _title(f0, f1, "Memory ≠ Intelligence")
    box('rail1', (0, 0.4, 1.0), (11, 1.0, 0.22), C_GREY)
    box('rail2', (0, 0.4, 2.6), (11, 1.0, 0.22), C_GREY)
    cols = [C_RED, C_AMBER, C_GREEN, C_CYAN, C_PURPLE]
    for i, c in enumerate(cols):
        bk = box(f'book{i}', (-4 + i * 2, 0.4, 1.6),
                 (0.7, 1.4, 1.1), c)
        rise(bk, f0 + 12 + i * 12, f0 + 36 + i * 12, 0.25)
    w = text3d('warn', "≠", (0, -1.6, 4.6), size=2.0, color=C_RED)
    scale_in(w, f0 + 100, f0 + 120)


def b_s07(f0, f1):
    _title(f0, f1, "Hallucination", color=C_RED)
    base = box('fact', (0, 0, 1.5), (2.4, 2.4, 2.4), C_INK)
    rise(base, f0 + 10, f0 + 40, 0.3)
    g1 = box('glitch1', (0.7, 0.4, 3.6), (1.5, 1.5, 1.5), C_RED)
    g2 = box('glitch2', (-0.6, -0.3, 4.4), (1.1, 1.1, 1.1), C_RED)
    for i in range(4):
        f = f0 + 60 + i * 40
        kf_scale(g1, f, 1.5); kf_scale(g1, f + 18, 0.02)
        kf_scale(g2, f + 18, 0.02); kf_scale(g2, f + 36, 1.1)
    b, t = chip('risk', "Risk", (5.6, -1.2, 1.2), C_RED)
    rise(b, f0 + 150, f0 + 170, 1.0); rise(t, f0 + 150, f0 + 170, 1.0)


def b_s08(f0, f1):
    _title(f0, f1, "World Model")
    g = sphere('globe', (0, 0, 2.8), 2.4, C_TEAL)
    spin(g, f0 + 10, f1, 3.0)
    r = torus('ring', (0, 0, 2.8), 3.4, 0.12, C_AMBER,
              rot=(math.radians(75), 0, 0))
    spin(r, f0 + 10, f1, -2.0, 'Z')
    for i, ang in enumerate((0.6, 2.7, 4.8)):
        m = box(f'moon{i}', (math.sin(ang) * 3.4, math.cos(ang) * 3.4 * 0.3,
                             2.8 + math.cos(ang) * 3.2),
                (0.6, 0.6, 0.6), C_CYAN)
        rise(m, f0 + 40 + i * 20, f0 + 70 + i * 20, 0.5)


def b_s09(f0, f1):
    _title(f0, f1, "Planning")
    for i in range(4):
        s = box(f'step{i}', (-4.5 + i * 3, 0, 0.6 + i * 1.0),
                (2.4, 2.0, 1.2 + i * 2.0), C_GREEN)
        rise(s, f0 + 10 + i * 14, f0 + 38 + i * 14, 0.3)
    ar = box('arrow', (-6.5, 0, 6.6), (2.2, 0.3, 0.3), C_CYAN,
             rot=(0, 0, math.radians(-18)))
    move(ar, f0 + 40, f0 + 150, (7.0, 0, 5.2))


def b_s10(f0, f1):
    _title(f0, f1, "Agents")
    core = sphere('core', (0, 0, 2.4), 1.6, C_PURPLE)
    spin(core, f0 + 10, f1, 2.0)
    torus('orbit', (0, 0, 2.4), 4.2, 0.1, C_GREY,
          rot=(math.radians(90), 0, 0))
    cols = [C_CYAN, C_GREEN, C_RED, C_AMBER, C_BLUE, C_TEAL, C_ACCENT]
    for i, c in enumerate(cols):
        ang = 2 * math.pi * i / 7
        m = box(f'ag{i}', (math.sin(ang) * 4.2, math.cos(ang) * 4.2, 2.4),
                (0.8, 0.8, 0.8), c)
        scale_in(m, f0 + 20 + i * 10, f0 + 44 + i * 10)
        spin(m, f0 + 60, f1, 1.5)


def b_s11(f0, f1):
    _title(f0, f1, "Tools")
    crate('box', (0, 0, 1.3), 2.4, C_AMBER)
    w1 = box('w1', (-0.7, 0, 3.0), (0.35, 0.35, 1.8), C_GREY,
             rot=(0, math.radians(24), 0))
    w2 = cyl('w2', (0.8, 0.2, 2.9), 0.18, 2.0, C_CYAN,
             rot=(math.radians(70), 0, math.radians(30)))
    rise(w1, f0 + 30, f0 + 55, 0.5)
    rise(w2, f0 + 50, f0 + 75, 0.5)


def b_s12(f0, f1):
    _title(f0, f1, "Self Update")
    torus('loop', (0, 0, 0.25), 3.6, 0.16, C_CYAN,
          rot=(math.radians(90), 0, 0))
    for i in range(4):
        ang = math.pi / 2 * i
        n = box(f'n{i}', (math.sin(ang) * 3.6, math.cos(ang) * 3.6, 1.1),
                (0.9, 0.9, 0.9), [C_GREEN, C_AMBER, C_CYAN, C_PURPLE][i])
        rise(n, f0 + 14 + i * 16, f0 + 44 + i * 16, 0.4)
        spin(n, f0 + 60, f1, 2.0)


def b_s13(f0, f1):
    _title(f0, f1, "Grounding")
    box('base', (0, 0, 0.35), (7, 2.6, 0.7), C_GREY)
    for i in range(3):
        lk = torus(f'lk{i}', (0, 0, 1.6 + i * 1.15), 0.85, 0.2,
                   C_AMBER if i % 2 else C_GREY,
                   rot=(0, math.radians(90), 0))
        scale_in(lk, f0 + 20 + i * 18, f0 + 48 + i * 18)
    b, t = chip('facts', "Facts", (6.2, -1.2, 1.2), C_GREEN)
    rise(b, f0 + 100, f0 + 120, 1.0); rise(t, f0 + 100, f0 + 120, 1.0)


def b_s14(f0, f1):
    _title(f0, f1, "Safety Layer")
    sh = box('shield', (0, 0, 2.6), (3.4, 0.6, 4.4), C_BLUE)
    scale_in(sh, f0 + 10, f0 + 40)
    cr = box('crest', (0, -0.35, 3.4), (1.4, 0.25, 1.4), C_ACCENT)
    scale_in(cr, f0 + 46, f0 + 66)
    spin(sh, f0 + 80, f1, 0.4)


def b_s15(f0, f1):
    _title(f0, f1, "Goals")
    for i, (R, c) in enumerate(((3.4, C_INK), (2.3, C_GREY), (1.2, C_INK))):
        t = torus(f'tg{i}', (0, 0, 0.22), R, 0.16, c,
                  rot=(math.radians(90), 0, 0))
        scale_in(t, f0 + 12 + i * 18, f0 + 40 + i * 18)
    ctr = sphere('bull', (0, 0, 0.8), 0.8, C_RED)
    rise(ctr, f0 + 70, f0 + 100, 0.4)


def b_s16(f0, f1):
    _title(f0, f1, "Compute")
    for r, x in enumerate((-4.2, 0, 4.2)):
        for i in range(4):
            s = box(f'rk{r}_{i}', (x, 0, 0.5 + i * 1.05),
                    (2.6, 1.6, 0.4), C_GREY)
            rise(s, f0 + 10 + r * 14 + i * 8, f0 + 34 + r * 14 + i * 8, 0.25)
            d = box(f'led{r}_{i}', (x, -0.85, 0.5 + i * 1.05),
                    (0.16, 0.06, 0.16), C_GREEN if (r + i) % 2 else C_RED)
            scale_in(d, f0 + 60 + i * 6, f0 + 72 + i * 6)


def b_s17(f0, f1):
    _title(f0, f1, "Data")
    cols = [C_CYAN, C_AMBER, C_GREEN, C_PURPLE]
    for i in range(12):
        c = box(f'tok{i}', (-7.5 + i * 1.3, 0, 1.6),
                (0.42, 0.42, 0.42), cols[i % 4])
        move(c, f0 + i * 6, f1, (c.location.x + 9.0, 0, 1.6))


def b_s18(f0, f1):
    _title(f0, f1, "The Stack")
    cols = [C_CYAN, C_GREEN, C_PURPLE, C_RED, C_TEAL]
    for i, c in enumerate(cols):
        s = box(f'stack{i}', (0, 0, 0.6 + i * 1.25),
                (5.6, 3.4, 0.5), c)
        rise(s, f0 + 10 + i * 16, f0 + 40 + i * 16, 0.3)
    words = ["Reason", "Memory", "Agents", "Safe", "World"]
    for i, (c, w) in enumerate(zip(cols, words)):
        b, t = chip(f'lb{i}', w, (6.8, -1.0, 0.9 + i * 1.25), c)
        rise(b, f0 + 70 + i * 12, f0 + 92 + i * 12, 0.5)
        rise(t, f0 + 70 + i * 12, f0 + 92 + i * 12, 0.5)


def b_s19(f0, f1):
    _title(f0, f1, "One Mind?")
    L = sphere('mind_l', (-3.6, 0, 2.4), 1.5, C_CYAN)
    R = sphere('mind_r', (3.6, 0, 2.4), 1.5, C_AMBER)
    mid = (f0 + f1) // 2
    move(L, f0 + 20, mid, (-0.4, 0, 2.4))
    move(R, f0 + 20, mid, (0.4, 0, 2.4))
    m = sphere('mind', (0, 0, 2.4), 2.2, C_PURPLE)
    kf_scale(m, mid, 0.02)
    kf_scale(m, mid + 40, 2.2)
    spin(m, mid + 40, f1, 1.5)


def b_s20(f0, f1):
    _title(f0, f1, "Open Question", z=5.4, size=1.6)
    q = text3d('q2', "?", (0, 0, 2.6), size=4.4, color=C_ACCENT)
    scale_in(q, f0 + 10, f0 + 30)
    spin(q, f0 + 40, f1, 0.5)
    b, t = chip('agi', "AGI", (5.6, -1.2, 1.2), C_ACCENT)
    rise(b, f0 + 60, f0 + 80, 1.0); rise(t, f0 + 60, f0 + 80, 1.0)


SEQ = [
    dict(id='s01', title="AGI Architecture", anchors=(), build=b_s01),
    dict(id='s02', title="Key Question",
         anchors=("question", "missing", "need"), build=b_s02),
    dict(id='s03', title="Bigger Model",
         anchors=("bigger", "scal", "larger"), build=b_s03),
    dict(id='s04', title="Transformer = AGI?",
         anchors=("transformer", "attention"), build=b_s04),
    dict(id='s05', title="Reasoning Core",
         anchors=("reason", "logic", "think"), build=b_s05),
    dict(id='s06', title="Memory ≠ Intelligence",
         anchors=("memory", "remember", "store"), build=b_s06),
    dict(id='s07', title="Hallucination",
         anchors=("hallucin",), build=b_s07),
    dict(id='s08', title="World Model",
         anchors=("world", "simulat", "globe"), build=b_s08),
    dict(id='s09', title="Planning",
         anchors=("plan", "step", "subgoal"), build=b_s09),
    dict(id='s10', title="Agents",
         anchors=("agent", "swarm"), build=b_s10),
    dict(id='s11', title="Tools",
         anchors=("tool", "api", "call"), build=b_s11),
    dict(id='s12', title="Self Update",
         anchors=("self", "update", "learn", "loop"), build=b_s12),
    dict(id='s13', title="Grounding",
         anchors=("ground", "fact", "truth"), build=b_s13),
    dict(id='s14', title="Safety Layer",
         anchors=("safe", "guard", "harm", "align"), build=b_s14),
    dict(id='s15', title="Goals",
         anchors=("goal", "objective", "target"), build=b_s15),
    dict(id='s16', title="Compute",
         anchors=("comput", "gpu", "power", "hardware"), build=b_s16),
    dict(id='s17', title="Data",
         anchors=("data", "dataset", "token"), build=b_s17),
    dict(id='s18', title="The Stack",
         anchors=("stack", "layer", "combin", "integrat"), build=b_s18),
    dict(id='s19', title="One Mind?",
         anchors=("unify", "whole", "together", "single"), build=b_s19),
    dict(id='s20', title="Open Question",
         anchors=("question",), last=True, build=b_s20),
]
