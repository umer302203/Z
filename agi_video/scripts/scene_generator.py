"""scene_generator v4 — orchestrator:
wav probe → windows from transcript anchors → build 20 seqs → camera bake (80 shots)
→ audio strip → validate (6 gates) → sequence_windows.json → final_scene.blend → previews.
Run inside Blender:  blender -b -P scene_generator.py
"""
import bpy, json, math, os, sys, wave

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import lib_scene as L
import specs as S

ROOT = os.path.dirname(os.path.dirname(HERE))
WAV = os.path.join(ROOT, "agi_video", "audio", "narration_AGI_locked_837s.wav")
TRANSCRIPT = os.path.join(ROOT, "agi_video", "reports", "transcript_timestamps.json")
REPORTS = os.path.join(ROOT, "agi_video", "reports")
BLEND_OUT = os.path.join(ROOT, "agi_video", "final_scene.blend")
WINDOWS_JSON = os.path.join(REPORTS, "sequence_windows.json")
VALID_TXT = os.path.join(REPORTS, "validation.txt")

MIN_WIN_F = 144          # 6 s floor
N_SHOTS = 80

# ---------------- wav probe ----------------
def wav_duration(path):
    with wave.open(path, "rb") as w:
        return w.getnframes() / float(w.getframerate())

# ---------------- windows ----------------
def load_words():
    with open(TRANSCRIPT) as f:
        d = json.load(f)
    return d.get("words") or []

def anchor_time(stems, words, after_t):
    if not stems:
        return None
    for wd in words:
        t = wd["start"]
        if t <= after_t + 1e-6:
            continue
        tok = wd["w"].lower().strip(".,!?;:\"'()[]")
        for st in stems:
            if st in tok:          # stem substring match (hallucin, comput, unifi...)
                return t
    return None

def compute_windows(total_dur, words):
    n = len(S.SEQ)
    times = [0.0]
    after = 0.0
    for i in range(1, n):
        a = anchor_time(S.SEQ[i]["anchors"], words, after)
        if a is not None and a < total_dur - 30:
            times.append(a)
            after = a
        else:
            times.append(None)
    known = [i for i, t in enumerate(times) if t is not None]
    # interpolate unknowns between nearest known neighbors
    for i in range(1, n):
        if times[i] is None:
            prev_k = max([k for k in known if k < i], default=0)
            next_k = min([k for k in known if k > i], default=n)
            t0 = times[prev_k] if times[prev_k] is not None else 0.0
            t1 = times[next_k] if next_k < len(times) and times[next_k] is not None else total_dur
            span = max(1, next_k - prev_k)
            times[i] = t0 + (t1 - t0) * (i - prev_k) / span
    times.append(total_dur)
    times[0] = 0.0
    # monotonic clamp
    for i in range(1, len(times)):
        times[i] = max(times[i], times[i - 1] + 0.5)
    times[-1] = total_dur
    # frames
    fr = [max(1, round(t * L.FPS) + 1) for t in times]
    fr[0] = 1
    fr[-1] = int(total_dur * L.FPS) + 2
    # enforce 6 s floor: pull from next neighbor
    for i in range(1, len(fr)):
        if fr[i] - fr[i - 1] < MIN_WIN_F:
            fr[i] = fr[i - 1] + MIN_WIN_F
    # if overflow beyond end, squeeze backwards from the end
    if fr[-1] > int(total_dur * L.FPS) + 2:
        fr[-1] = int(total_dur * L.FPS) + 2
        for i in range(len(fr) - 2, 0, -1):
            if fr[i + 1] - fr[i] < MIN_WIN_F:
                fr[i] = max(1, fr[i + 1] - MIN_WIN_F)
    wins = []
    for i, sq in enumerate(S.SEQ):
        wins.append({"id": sq["id"], "title": sq["title"], "builder": sq.get("builder"),
                     "f0": fr[i], "f1": fr[i + 1],
                     "t0": round((fr[i] - 1) / L.FPS, 2),
                     "t1": round((fr[i + 1] - 1) / L.FPS, 2)})
    return wins

# ---------------- camera bake ----------------
def bake_camera(cam, wins):
    total_f = wins[-1]["f1"]
    lens = [w["f1"] - w["f0"] + 1 for w in wins]
    total_len = sum(lens)
    counts = [max(2, round(N_SHOTS * ln / total_len)) for ln in lens]
    diff = N_SHOTS - sum(counts)
    order = sorted(range(len(wins)), key=lambda i: -lens[i])
    i = 0
    while diff != 0:
        k = order[i % len(order)]
        if diff > 0:
            counts[k] += 1; diff -= 1
        elif counts[k] > 2:
            counts[k] -= 1; diff += 1
        i += 1
        if i > 500:
            break
    shots = []
    for wi, w in enumerate(wins):
        rng = random.Random(w["f0"] * 7 + wi)
        n = counts[wi]
        span = w["f1"] - w["f0"]
        edges = [w["f0"] + round(span * k / n) for k in range(n)] + [w["f1"]]
        for k in range(n):
            f0, f1 = edges[k], max(edges[k] + 12, edges[k + 1])
            kind = rng.choice(["push", "pull", "orbL", "orbR", "pan", "low"])
            shots.append((w["id"], kind, f0, f1, rng))
    for idx, (sid, kind, f0, f1, rng) in enumerate(shots):
        ang0 = rng.uniform(-0.55, 0.55)
        ang1 = ang0 + (0.5 if "L" in kind and kind == "orbL" else -0.5 if kind == "orbR" else rng.uniform(-0.25, 0.25))
        r0 = rng.uniform(14.0, 18.0); r1 = rng.uniform(12.5, 15.5)
        z0 = rng.uniform(5.0, 7.5);   z1 = rng.uniform(4.8, 6.8)
        if kind == "push":
            p0, p1 = L.orbit_pos(ang0, r0, z0), L.orbit_pos(ang0 + ang1 * 0.3, r1, z1)
        elif kind == "pull":
            p0, p1 = L.orbit_pos(ang0, r1, z1), L.orbit_pos(ang0 + ang1 * 0.3, r0, z0)
        elif kind in ("orbL", "orbR"):
            p0, p1 = L.orbit_pos(ang0, r0, z0), L.orbit_pos(ang1, r0, z1)
        elif kind == "pan":
            p0, p1 = L.orbit_pos(-0.5, r0, z0), L.orbit_pos(0.5, r0, z1)
        else:  # low
            p0, p1 = L.orbit_pos(ang0, r0, 2.4), L.orbit_pos(ang0 + 0.2, r1, 3.4)
        tgt = (0.0, -1.2, rng.uniform(0.3, 0.9))
        cam.location = p0
        L.look_at(cam, tgt)
        cam.keyframe_insert("location", frame=f0)
        cam.keyframe_insert("rotation_euler", frame=f0)
        cam.location = p1
        L.look_at(cam, tgt)
        cam.keyframe_insert("location", frame=f1)
        cam.keyframe_insert("rotation_euler", frame=f1)
    return shots

import random  # noqa: E402  (used in bake_camera)

# ---------------- validation ----------------
def text_words(body):
    n = 0
    for tok in body.split():
        if any(c.isalnum() for c in tok):
            n += 1
    return n

def validate(wins, shots):
    sc = bpy.context.scene
    gates = {}
    # AUDIO
    snd = [s for s in sc.sequence_editor.sequences if s.type == 'SOUND'] if sc.sequence_editor else []
    gates["AUDIO"] = (len(snd) == 1 and abs(snd[0].frame_final_duration - sc.frame_end) < 4000)
    # TIMELINE
    ok = wins[0]["f0"] == 1 and wins[-1]["f1"] == sc.frame_end
    for i in range(len(wins) - 1):
        if wins[i]["f1"] != wins[i + 1]["f0"]:
            ok = False
        if wins[i]["f1"] - wins[i]["f0"] < MIN_WIN_F:
            ok = False
    gates["TIMELINE"] = ok and len(wins) == 20
    # OBJECTS
    obs = [o for o in bpy.data.objects if o.name != "GROUND" and o.type != 'CAMERA']
    gates["OBJECTS"] = len(obs) >= 60
    # CAMERA
    cams = [o for o in bpy.data.objects if o.type == 'CAMERA']
    kf = cams[0].animation_data.action.fcurves if cams and cams[0].animation_data and cams[0].animation_data.action else []
    n_kf = sum(len(c.keyframe_points) for c in kf) if kf else 0
    gates["CAMERA"] = len(cams) == 1 and len(shots) >= 70 and n_kf >= 140
    # TEXT  (TEXT RULE: <=3 words per on-screen string)
    txts = [o for o in bpy.data.objects if o.type == 'FONT']
    bad = []
    for o in txts:
        body = o.get("text_body", o.data.body if o.type == 'FONT' else "")
        if text_words(body) > 3:
            bad.append(body)
    gates["TEXT"] = len(txts) >= 15 and not bad
    # RENDER
    gates["RENDER"] = (sc.render.engine == 'BLENDER_WORKBENCH'
                       and sc.render.resolution_x == 1280 and sc.render.resolution_y == 720
                       and sc.render.fps == 24)
    lines = []
    for k in ("AUDIO", "TIMELINE", "OBJECTS", "CAMERA", "TEXT", "RENDER"):
        lines.append(f"{k}: {'PASS' if gates[k] else 'FAIL'}")
    allpass = all(gates.values())
    lines.append(f"ALL: {'PASS' if allpass else 'FAIL'}")
    lines.append(f"objects={len(obs)} text_objects={len(txts)} bad_text={bad}")
    lines.append(f"shots={len(shots)} cam_kf={n_kf} frame_end={sc.frame_end}")
    with open(VALID_TXT, "w") as f:
        f.write("\n".join(lines) + "\n")
    print("VALIDATION:", " | ".join(lines[:7]))
    return allpass

# ---------------- previews ----------------
def previews(times):
    sc = bpy.context.scene
    outs = []
    for i, t in enumerate(times):
        fr = max(1, min(sc.frame_end, int(t * L.FPS) + 1))
        sc.frame_set(fr)
        sc.render.filepath = os.path.join(REPORTS, f"preview_{i}_{fr}.jpg")
        bpy.ops.render.render(write_still=True)
        outs.append(sc.render.filepath)
    return outs

# ---------------- per-seq visibility ----------------
def apply_visibility(seq_objs, wins, total_f):
    for w in wins:
        appear = max(1, w["f0"] - 6)
        gone = min(total_f, w["f1"] + 6)
        for ob in seq_objs.get(w["id"], []):
            if ob.type == 'CAMERA':
                continue
            for dp in ("hide_viewport", "hide_render"):
                try:
                    setattr(ob, dp, True)
                    ob.keyframe_insert(dp, frame=1)
                    setattr(ob, dp, False)
                    ob.keyframe_insert(dp, frame=appear)
                    setattr(ob, dp, True)
                    ob.keyframe_insert(dp, frame=gone)
                except Exception as e:
                    print("vis fail", ob.name, dp, e)
    print("VISIBILITY: applied to", sum(len(v) for v in seq_objs.values()), "objects")

# ---------------- main ----------------
def main():
    os.makedirs(REPORTS, exist_ok=True)
    dur = wav_duration(WAV)
    total_f = int(dur * L.FPS) + 2
    print(f"WAV {dur:.2f}s -> {total_f} frames")
    L.scene_setup(total_f)
    words = load_words() if os.path.exists(TRANSCRIPT) else []
    wins = compute_windows(dur, words)
    for w in wins:
        print(f'{w["id"]} {w["title"]}: f{w["f0"]}-{w["f1"]} ({w["t0"]}-{w["t1"]}s)')
    seq_objs = {}
    for i, w in enumerate(wins):
        fn = getattr(S, w.get("builder") or f"b_{w['id']}", None)
        if fn is None:
            raise RuntimeError(f"missing builder b_{w['id']}")
        before = {o.name for o in bpy.data.objects}
        fn(w["f0"], w["f1"])
        seq_objs[w["id"]] = [o for o in bpy.data.objects if o.name not in before]
    apply_visibility(seq_objs, wins, total_f)
    cam = L.cam_make()
    shots = bake_camera(cam, wins)
    L.add_audio(WAV, total_f)
    ok = validate(wins, shots)
    with open(WINDOWS_JSON, "w") as f:
        json.dump({"total_frames": total_f, "duration": dur, "windows": wins}, f, indent=1)
    bpy.ops.wm.save_as_mainfile(filepath=BLEND_OUT)
    print("SAVED", BLEND_OUT, "ALLPASS" if ok else "HASFAIL")
    previews([5, 60, 150, 260, 380, 500, 620, 760, 830])
    print("PREVIEWS DONE")

main()
