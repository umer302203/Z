"""specs v4 — 20 sequence builders + word-stem anchors for window computation.
TEXT RULE: every on-screen string <=3 words (symbols ok). Validation reads ob['text_body']."""
import math
from lib_scene import (box, sphere, cyl, torus, text3d, chip, sticky_note, crate,
                       kf_loc, kf_scale, kf_rot, move, rise, scale_in, spin, rgba, PAL)

# ---------------- sequence anchors (word stems searched in transcript) ----------------
SEQ = [
    {"id": "s01", "title": "AGI Architecture",   "builder": "b_s01", "anchors": None},
    {"id": "s02", "title": "Key Question",       "builder": "b_s02", "anchors": ("सवाल",)},
    {"id": "s03", "title": "Bigger Model",       "builder": "b_s03", "anchors": ("बिगर",)},
    {"id": "s04", "title": "Transformer = AGI?", "builder": "b_s04", "anchors": ("रेलिशिन",)},
    {"id": "s05", "title": "Reasoning Core",     "builder": "b_s05", "anchors": ("मीटिंग",)},
    {"id": "s06", "title": "Planning",           "builder": "b_s09", "anchors": ("पलान",)},
    {"id": "s07", "title": "World Model",        "builder": "b_s08", "anchors": ("वेट",)},
    {"id": "s08", "title": "Memory ≠ Smarts",    "builder": "b_s06", "anchors": ("डेटाबेज",)},
    {"id": "s09", "title": "Hallucination",      "builder": "b_s07", "anchors": ("गलत",)},
    {"id": "s10", "title": "Safety Layer",       "builder": "b_s14", "anchors": ("सेफ",)},
    {"id": "s11", "title": "Self Update",        "builder": "b_s12", "anchors": ("फुर्गेंतिं", "अपडेट", "update")},
    {"id": "s12", "title": "One Mind?",          "builder": "b_s19", "anchors": ("अक्टिवेट",)},
    {"id": "s13", "title": "The Stack",          "builder": "b_s18", "anchors": ("आरकिटेक्चर",)},
    {"id": "s14", "title": "Grounding",          "builder": "b_s13", "anchors": ("फीट्बाक",)},
    {"id": "s15", "title": "Goals",              "builder": "b_s15", "anchors": ("verific", "वेरिफिक")},
    {"id": "s16", "title": "Agents",             "builder": "b_s10", "anchors": ("specialis", "एक्सपर्ट")},
    {"id": "s17", "title": "Tools",              "builder": "b_s11", "anchors": ("instrument",)},
    {"id": "s18", "title": "Compute",            "builder": "b_s16", "anchors": None},
    {"id": "s19", "title": "Data",               "builder": "b_s17", "anchors": ("text",)},
    {"id": "s20", "title": "Open Question",      "builder": "b_s20", "anchors": ("कनेक्टेड", "connected")},
]

MIN_TITLE = {s["id"]: s["title"] for s in SEQ}

def _grid(xs, z, y=-1.2):
    return [(x, y, z) for x in xs]

# ---------------- builders: b_s01(f0, f1) ... b_s20(f0, f1) ----------------

def b_s01(f0, f1):
    m = (f0 + f1) // 2
    t = text3d("AGI Architecture", (0, -8.0, 3.2), 1.25, "T01", "white")
    scale_in(t, f0 + 5, f0 + 25, (1.5, 1.5, 1.5))
    a = box((-4.5, -1.2, 0.4), (2.4, 2.4, 2.4), "Core", "cyan")
    b = box((0, -1.2, 0.4), (2.4, 2.4, 2.4), "Mind", "purple")
    c = box((4.5, -1.2, 0.4), (2.4, 2.4, 2.4), "World", "orange")
    for ob, f in ((a, f0 + 30), (b, f0 + 55), (c, f0 + 80)):
        scale_in(ob, f, f + 22)
    spin(a, m, f1, 0.5)
    spin(c, m, f1, 0.5)

def b_s02(f0, f1):
    t = text3d("Key Question", (0, -8.0, 3.2), 1.25, "T02", "cyan")
    scale_in(t, f0 + 5, f0 + 25, (1.4, 1.4, 1.4))
    q = torus((0, -1.2, 1.2), 2.2, 0.4, "Qmark", "yellow")
    scale_in(q, f0 + 30, f0 + 60)
    spin(q, f0 + 70, f1, 1.0)
    n1, _ = sticky_note((-4, -1.0, 0.1), "What", "N02a", "yellow", 1.4)
    n2, _ = sticky_note((4, -1.0, 0.1), "Needed", "N02b", "orange", 1.4)
    scale_in(n1, f0 + 90, f0 + 110)
    scale_in(n2, f0 + 120, f0 + 140)

def b_s03(f0, f1):
    t = text3d("Bigger Model", (0, -8.0, 3.2), 1.25, "T03", "orange")
    scale_in(t, f0 + 5, f0 + 25, (1.4, 1.4, 1.4))
    sizes = [0.9, 1.4, 2.0, 2.7]
    for i, s in enumerate(sizes):
        ob = box((-5.4 + i * 3.6, -1.2, s / 2 - 1.2), (s, s, s), f"Sc{i}", ["gray", "cyan", "purple", "orange"][i])
        f = f0 + 30 + i * 45
        scale_in(ob, f, f + 25)

def b_s04(f0, f1):
    t = text3d("Transformer = AGI?", (0, -8.0, 3.2), 1.25, "T04", "purple")
    scale_in(t, f0 + 5, f0 + 25, (1.3, 1.3, 1.3))
    for i in range(4):
        c = chip((-4.8 + i * 3.2, -1.2, 1.6), f"Attn{i}", ["cyan", "purple", "cyan", "purple"][i], (2.2, 2.2, 0.6))
        scale_in(c, f0 + 40 + i * 35, f0 + 60 + i * 35)
        rise(c, f0 + 60 + i * 35, f0 + 90 + i * 35, 0.6)
    q = text3d("Enough?", (0, -1.0, -0.5), 1.0, "T04b", "red")
    scale_in(q, f1 - 60, f1 - 40, (1.0, 1.0, 1.0))

def b_s05(f0, f1):
    t = text3d("Reasoning Core", (0, -8.0, 3.2), 1.25, "T05", "green")
    scale_in(t, f0 + 5, f0 + 25, (1.4, 1.4, 1.4))
    steps = [(-4.8, 0), (-1.6, 1.1), (1.6, 0), (4.8, 1.1)]
    for i, (x, z) in enumerate(steps):
        s = sphere((x, -1.2, z + 0.4), 0.75, f"St{i}", "green")
        scale_in(s, f0 + 35 + i * 40, f0 + 55 + i * 40)
        if i > 0:
            px, pz = steps[i - 1][0], steps[i - 1][1]
            ln = cyl(((x + px) / 2, -1.2, (z + pz) / 2 + 0.4), 0.09,
                     math.hypot(x - px, z - pz), f"Lk{i}", "gray")
            ln.rotation_euler = (0, math.pi / 2, -math.atan2(z - pz, x - px))
            scale_in(ln, f0 + 55 + i * 40, f0 + 70 + i * 40)

def b_s06(f0, f1):
    t = text3d("Memory ≠ Smarts", (0, -4.5, 3.6), 1.35, "T06", "yellow")
    scale_in(t, f0 + 5, f0 + 25, (1.35, 1.35, 1.35))
    m = box((-4.2, -1.2, 0.4), (2.6, 2.6, 2.6), "Mem", "yellow")
    i = sphere((3.6, -1.2, 0.4), 1.5, "Intel", "cyan")
    scale_in(m, f0 + 35, f0 + 60)
    scale_in(i, f0 + 110, f0 + 135)
    spin(m, f0 + 70, f0 + 105, 0.6)

def b_s07(f0, f1):
    t = text3d("Hallucination", (0, -8.0, 3.2), 1.25, "T07", "red")
    scale_in(t, f0 + 5, f0 + 25, (1.4, 1.4, 1.4))
    b = sphere((0, -1.2, 0.6), 1.4, "Brain", "purple")
    scale_in(b, f0 + 30, f0 + 55)
    for i in range(5):
        f = sphere((-4 + i * 2, -1.2, 2.8 + (i % 2)), 0.22, f"Fog{i}", "red")
        f0i = f0 + 70 + i * 25
        kf_loc(f, f0i, f.location)
        kf_loc(f, f0i + 45, (f.location.x, f.location.y - 0.4, f.location.z + 1.2))
        scale_in(f, f0i, f0i + 10, (1, 1, 1))
    x = text3d("✗ Wrong", (0, -1.0, -1.2), 1.1, "T07b", "red")
    scale_in(x, f1 - 50, f1 - 30, (1.1, 1.1, 1.1))

def b_s08(f0, f1):
    t = text3d("World Model", (0, -8.0, 3.2), 1.25, "T08", "cyan")
    scale_in(t, f0 + 5, f0 + 25, (1.4, 1.4, 1.4))
    pl = sphere((0, -1.2, 0.2), 1.9, "Earth", "cyan")
    scale_in(pl, f0 + 30, f0 + 60)
    spin(pl, f0 + 60, f1, 1.2, "Z")
    ring = torus((0, -1.2, 0.2), 3.0, 0.12, "Orbit", "gray")
    ring.rotation_euler = (math.radians(70), 0, 0)
    scale_in(ring, f0 + 80, f0 + 100)
    m = box((5.2, -1.2, 0.4), (1.6, 1.6, 1.6), "Sim", "purple")
    scale_in(m, f0 + 130, f0 + 150)

def b_s09(f0, f1):
    t = text3d("Planning", (0, -8.0, 3.2), 1.25, "T09", "orange")
    scale_in(t, f0 + 5, f0 + 25, (1.4, 1.4, 1.4))
    for i in range(4):
        c = chip((-4.5 + i * 3.0, -1.2, 0.6), f"P{i+1}", "orange", (2.0, 2.0, 0.55))
        scale_in(c, f0 + 35 + i * 40, f0 + 55 + i * 40)
    g = sphere((4.5, -1.2, 2.6), 0.6, "Goal", "green")
    rise(g, f0 + 200, f0 + 240, 0.0)
    scale_in(g, f0 + 210, f0 + 230)

def b_s10(f0, f1):
    t = text3d("Agents", (0, -8.0, 3.2), 1.25, "T10", "purple")
    scale_in(t, f0 + 5, f0 + 25, (1.4, 1.4, 1.4))
    for i in range(3):
        a = box((-4.2 + i * 4.2, -1.2, 0.4), (1.8, 1.8, 1.8), f"Ag{i}", ["purple", "cyan", "green"][i])
        scale_in(a, f0 + 35 + i * 50, f0 + 60 + i * 50)
        spin(a, f0 + 80 + i * 50, f0 + 140 + i * 50, 0.5)

def b_s11(f0, f1):
    t = text3d("Tools", (0, -8.0, 3.2), 1.25, "T11", "green")
    scale_in(t, f0 + 5, f0 + 25, (1.4, 1.4, 1.4))
    h = box((-5.2, -1.2, 0.4), (1.8, 1.8, 1.8), "Hand", "white")
    scale_in(h, f0 + 30, f0 + 50)
    for i, (nm, col) in enumerate((("Search", "cyan"), ("API", "purple"), ("Code", "orange"))):
        tl = box((-1.7 + i * 3.4, -1.2, 0.3), (1.7, 1.7, 1.7), f"Tool{i}", col)
        scale_in(tl, f0 + 70 + i * 45, f0 + 95 + i * 45)

def b_s12(f0, f1):
    t = text3d("Self Update", (0, -8.0, 3.2), 1.25, "T12", "cyan")
    scale_in(t, f0 + 5, f0 + 25, (1.4, 1.4, 1.4))
    loop = torus((0, -1.2, 1.0), 2.3, 0.3, "Loop", "cyan")
    scale_in(loop, f0 + 30, f0 + 55)
    spin(loop, f0 + 55, f1, 2.0)
    for i in range(3):
        d = sphere((-4.5 + i * 4.5, -1.2, 1.0), 0.5, f"Data{i}", "orange")
        f0i = f0 + 90 + i * 60
        kf_loc(d, f0i, d.location)
        kf_loc(d, f0i + 50, (0, -1.2, 1.0))
        scale_in(d, f0i, f0i + 8, (1, 1, 1))

def b_s13(f0, f1):
    t = text3d("Grounding", (0, -8.0, 3.2), 1.25, "T13", "green")
    scale_in(t, f0 + 5, f0 + 25, (1.4, 1.4, 1.4))
    g = box((0, -1.2, -1.5), (12, 3, 0.6), "Real", "green")
    scale_in(g, f0 + 30, f0 + 50)
    for i in range(4):
        p = cyl((-4.5 + i * 3.0, -1.2, -0.4), 0.3, 2.0, f"Pin{i}", "white")
        scale_in(p, f0 + 70 + i * 35, f0 + 90 + i * 35)

def b_s14(f0, f1):
    t = text3d("Safety Layer", (0, -8.0, 3.2), 1.25, "T14", "red")
    scale_in(t, f0 + 5, f0 + 25, (1.4, 1.4, 1.4))
    sh = box((0, -1.2, 1.6), (7.4, 7.4, 0.4), "Shield", "red")
    sh.rotation_euler = (math.radians(70), 0, 0)
    scale_in(sh, f0 + 30, f0 + 60)
    core = sphere((0, -1.2, 0.2), 1.1, "Core", "cyan")
    scale_in(core, f0 + 80, f0 + 100)

def b_s15(f0, f1):
    t = text3d("Goals", (0, -8.0, 3.2), 1.25, "T15", "yellow")
    scale_in(t, f0 + 5, f0 + 25, (1.4, 1.4, 1.4))
    for i in range(3):
        n, _ = sticky_note((-3.8 + i * 3.8, -1.0, 0.6), ["Aim", "Plan", "Do"][i],
                           f"N15{i}", ["yellow", "orange", "green"][i], 1.5)
        scale_in(n, f0 + 35 + i * 45, f0 + 60 + i * 45)

def b_s16(f0, f1):
    t = text3d("Compute", (0, -8.0, 3.2), 1.25, "T16", "orange")
    scale_in(t, f0 + 5, f0 + 25, (1.4, 1.4, 1.4))
    for r in range(2):
        for c in range(4):
            ch = chip((-4.8 + c * 3.2, -1.2 + r * 2.6, 0.3), f"GPU{r}{c}",
                      ["orange", "deep"][r], (2.4, 2.0, 0.5))
            scale_in(ch, f0 + 35 + (r * 4 + c) * 22, f0 + 52 + (r * 4 + c) * 22)

def b_s17(f0, f1):
    t = text3d("Data", (0, -8.0, 3.2), 1.25, "T17", "cyan")
    scale_in(t, f0 + 5, f0 + 25, (1.4, 1.4, 1.4))
    for i in range(3):
        cr = crate((-3.6 + i * 3.6, -1.2, 0.0), 1.5, f"Cr{i}", ["cyan", "purple", "green"][i])
        scale_in(cr, f0 + 35 + i * 45, f0 + 60 + i * 45)
    q = text3d("Quality > Quantity", (0, -1.0, 2.6), 0.95, "T17b", "white")
    scale_in(q, f1 - 70, f1 - 45, (0.95, 0.95, 0.95))

def b_s18(f0, f1):
    t = text3d("The Stack", (0, -8.0, 3.2), 1.25, "T18", "white")
    scale_in(t, f0 + 5, f0 + 25, (1.4, 1.4, 1.4))
    layers = [("Reason", "green"), ("Memory", "yellow"), ("Agent", "purple"), ("Tools", "cyan"), ("Safety", "red")]
    for i, (nm, col) in enumerate(layers):
        L = box((0, -1.2, -0.8 + i * 1.0), (6.5 - i * 0.7, 2.4, 0.75), f"Lay{i}", col)
        scale_in(L, f0 + 35 + i * 35, f0 + 60 + i * 35)

def b_s19(f0, f1):
    t = text3d("One Mind?", (0, -8.0, 3.2), 1.25, "T19", "purple")
    scale_in(t, f0 + 5, f0 + 25, (1.4, 1.4, 1.4))
    one = sphere((0, -1.2, 0.8), 1.7, "One", "purple")
    scale_in(one, f0 + 30, f0 + 60)
    spin(one, f0 + 60, f1, 0.8)
    q = text3d("? Or Many", (0, -1.0, -1.1), 1.0, "T19b", "white")
    scale_in(q, f1 - 60, f1 - 35, (1.0, 1.0, 1.0))

def b_s20(f0, f1):
    t = text3d("Open Question", (0, -8.0, 3.2), 1.25, "T20", "cyan")
    scale_in(t, f0 + 5, f0 + 25, (1.5, 1.5, 1.5))
    m = (f0 + f1) // 2
    orb = torus((0, -1.2, 0.8), 2.6, 0.28, "O20", "cyan")
    scale_in(orb, f0 + 40, f0 + 70)
    spin(orb, f0 + 70, f1, 1.5)
    core = sphere((0, -1.2, 0.8), 0.9, "C20", "white")
    scale_in(core, f0 + 100, f0 + 125)
    end = text3d("→ Future", (0, -1.0, -1.3), 1.1, "T20b", "orange")
    scale_in(end, m + 40, m + 65, (1.1, 1.1, 1.1))

BUILDERS = {n: fn for n, fn in list(globals().items())
            if n.startswith("b_s") and callable(fn)}
