"""scene_generator.py — v3.1 orchestrator.
wav duration probe -> transcript anchor ORDERING (narration topic order) ->
monotonic 20 windows -> build specs -> 80-shot camera bake -> VSE narration ->
validation report -> save blend -> preview stills.
Run: blender -b -P scripts/scene_generator.py"""
import json
import math
import os
import random
import wave

import bpy

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)                     # .../AGI_explainer
AUDIO = os.path.join(ROOT, 'audio',
                     'narration_AGI_locked_837s.wav')
TRANS = os.path.join(ROOT, 'reports', 'transcript_timestamps.json')
WINJ = os.path.join(ROOT, 'reports', 'sequence_windows.json')
BLEND = os.path.join(ROOT, 'final_scene.blend')
PREV = os.path.join(ROOT, 'renders', 'preview')
REPORT = os.path.join(ROOT, 'reports', 'validation_report.txt')

FPS = 24
SHOTS_TOTAL = 80
MIN_WIN_F = 6 * FPS                              # 6s floor per sequence

import sys
sys.path.insert(0, HERE)
import lib_scene as L                            # noqa: E402
from specs import SEQ                            # noqa: E402


def probe_wav(path):
    with wave.open(path, 'rb') as w:
        dur = w.getnframes() / float(w.getframerate())
    return dur


def load_words():
    if not os.path.exists(TRANS):
        return []
    with open(TRANS, encoding='utf-8') as f:
        d = json.load(f)
    words = []
    for seg in d.get('segments', []):
        for wd in seg.get('words', []):
            words.append((wd['w'].lower().strip(), float(wd['start'])))
    return words


MIN_ANCHOR_T = 33.0   # skip opening surgeon analogy — module words cluster there


def spec_time(spec, words):
    """Anchor time >= MIN_ANCHOR_T (real discussion, not the analogy).
    mode 'first' -> earliest eligible stem hit; 'last' -> latest."""
    if not spec['anchors']:
        return None
    mode = 'last' if spec.get('last') else 'first'
    seq = words if mode == 'first' else reversed(words)
    best = None
    for stem in spec['anchors']:
        for w, t in seq:
            if w.startswith(stem) and t >= MIN_ANCHOR_T:
                if best is None:
                    best = t
                elif mode == 'first':
                    best = min(best, t)
                else:
                    best = max(best, t)
                break
    return best


def vis_keys(ob, f0, f1):
    """hold-style visibility keys (prevents linear bool interpolation leaks)."""
    for prop in ('hide_render', 'hide_viewport'):
        def kf(fr, val):
            setattr(ob, prop, val)
            ob.keyframe_insert(prop, frame=fr)
        if f0 <= 2:
            kf(1, False)
        else:
            kf(1, True)
            kf(f0 - 1, True)
            kf(f0, False)
        kf(f1, False)
        kf(f1 + 1, True)


def order_sequences(words):
    """Reorder inner sequences to follow the narration's topic order.
    s01 stays first, s20 last, unanchored mids inserted evenly."""
    n = len(SEQ)
    first, last = SEQ[0], SEQ[-1]
    mids = SEQ[1:n - 1]
    timed, flex = [], []
    for idx, spec in enumerate(mids):
        t = spec_time(spec, words)
        if t is None:
            flex.append(spec)
        else:
            timed.append((t, idx, spec))
    timed.sort(key=lambda p: (p[0], p[1]))
    ordered_mids = [s for _, _, s in timed]
    # spread flexible sequences evenly through the ordered list
    total = len(ordered_mids) + len(flex)
    for j, spec in enumerate(flex):
        pos = max(1, min(len(ordered_mids),
                         round((j + 1) * len(ordered_mids) / (len(flex) + 1))))
        ordered_mids.insert(pos + j, spec)       # keep prior inserts stable
    return [first] + ordered_mids + [last]


def compute_windows(total_f, words, ordered):
    """Monotonic windows: anchor bounds clamped forward to keep >= MIN_WIN_F;
    unanchored mids interpolated between neighbours."""
    n = len(ordered)
    MINF = MIN_WIN_F
    b = [None] * (n + 1)
    b[0], b[n] = 1, total_f
    for i in range(1, n):
        t = spec_time(ordered[i], words)
        if t is not None:
            f = int(t * FPS) + 1
            f = max(f, b[i - 1] + MINF if b[i - 1] else f)
            f = min(f, total_f - MINF * (n - i))  # leave room for the tail
            b[i] = max(f, 2)
    known = [i for i, v in enumerate(b) if v is not None]
    for k in range(len(known) - 1):
        i0, i1 = known[k], known[k + 1]
        v0, v1 = b[i0], b[i1]
        for j in range(i0 + 1, i1):
            b[j] = int(v0 + (v1 - v0) * (j - i0) / (i1 - i0))
    # backward safety: strictly increasing
    for i in range(n - 1, 0, -1):
        if b[i] >= b[i + 1]:
            b[i] = b[i + 1] - MINF
    for i in range(1, n + 1):
        if b[i] <= b[i - 1]:
            b[i] = b[i - 1] + 2
    anchored = sum(1 for i in range(1, n) if spec_time(ordered[i], words))
    return b, anchored


def bake_camera(cam, windows, total_f):
    n = len(windows) - 1
    total_dur = sum(windows[i + 1] - windows[i] for i in range(n))
    counts = [max(2, round(SHOTS_TOTAL *
                           (windows[i + 1] - windows[i]) / total_dur))
              for i in range(n)]
    while sum(counts) > SHOTS_TOTAL:
        counts[max(range(n), key=lambda i: counts[i])] -= 1
    while sum(counts) < SHOTS_TOTAL:
        counts[min(range(n), key=lambda i: counts[i])] += 1
    shots = 0
    prev_q = None
    for i in range(n):
        f0, f1 = windows[i], windows[i + 1]
        rng = random.Random(f0 * 7 + i)
        step = (f1 - f0) / counts[i]
        for k in range(counts[i]):
            # jump-cut keying: shot k owns [a0, b0]; next shot starts b0+1
            a0 = int(f0 + k * step) + (1 if k > 0 else 0)
            if k < counts[i] - 1:
                b0 = int(f0 + (k + 1) * step)
            else:
                b0 = f1 - 1 if i < n - 1 else f1
            if b0 <= a0:
                b0 = a0 + 1
            a = rng.uniform(-1.05, 1.05)   # front arc — text stays readable
            r = rng.uniform(15.0, 26.0)
            z = rng.uniform(3.5, 9.0)
            kind = 'wide' if k == 0 else rng.choice(
                ['push', 'pull', 'orbL', 'orbR', 'pan', 'low', 'wide'])
            t0 = (rng.uniform(-1.0, 1.0), 0, rng.uniform(1.8, 3.4))
            if kind == 'wide':
                r = rng.uniform(23.0, 28.0)
                p0 = L.orbit_pos(a, r, z * 0.9)
                p1 = L.orbit_pos(a + rng.uniform(-0.18, 0.18), r * 1.02, z)
                t1 = t0
            elif kind == 'push':
                p0 = L.orbit_pos(a, r, z)
                p1, t1 = L.orbit_pos(a, r * 0.62, z * 0.8), t0
            elif kind == 'pull':
                p0 = L.orbit_pos(a, r * 0.62, z * 0.8)
                p1 = L.orbit_pos(a, r * 1.15, z)
                t1 = t0
            elif kind == 'orbL':
                p0 = L.orbit_pos(a, r, z)
                p1, t1 = L.orbit_pos(a + 0.55, r, z), t0
            elif kind == 'orbR':
                p0 = L.orbit_pos(a, r, z)
                p1, t1 = L.orbit_pos(a - 0.55, r, z), t0
            elif kind == 'pan':
                p0 = L.orbit_pos(a, r, z)
                p1 = p0
                t1 = (t0[0] + rng.uniform(-3, 3), t0[1], t0[2])
            else:
                p0 = L.orbit_pos(a, r * 1.05, 2.4)
                p1 = L.orbit_pos(a + 0.2, r * 1.0, 2.7)
                t1 = (t0[0], 0, t0[2] + 1.2)
            prev_q = L.shot(cam, a0, b0, p0, p1, t0, t1, align=prev_q)
            shots += 1
    # CRITICAL: default BEZIER overshoots orbit paths (location dips inside
    # the stage; quaternion components swing wildly). Linear = true glide.
    for fc in cam.animation_data.action.fcurves:
        for kp in fc.keyframe_points:
            kp.interpolation = 'LINEAR'
    return shots


def add_audio(sc):
    se = sc.sequence_editor_create()
    try:
        snd = se.strips.new_sound('narration', AUDIO, 1, 1)
    except AttributeError:
        snd = se.sequences.new_sound('narration', AUDIO, 1, 1)
    return snd


def validate(sc, windows, n_shots, snd, total_f):
    objs = list(bpy.data.objects)
    anim = sum(1 for o in objs if o.animation_data)
    texts = [o for o in objs if o.get('text_body')]
    import re
    words_ok = 0
    for o in texts:
        toks = re.findall(r"[A-Za-z0-9]+", o['text_body'])
        words_ok += 1 if len(toks) <= 3 else 0
    gates = []
    ok_audio = snd is not None and snd.frame_duration > 1
    gates.append(('AUDIO', ok_audio,
                  f'strip frames={getattr(snd, "frame_duration", 0)}'))
    mono = all(windows[i] < windows[i + 1] for i in range(len(windows) - 1))
    gates.append(('TIMELINE', mono and len(windows) == 21,
                  f'20 windows cover 1..{total_f}'))
    gates.append(('OBJECTS', len(objs) > 100, f'{len(objs)} objects, '
                  f'{anim} animated'))
    gates.append(('CAMERA', n_shots >= 60 and sc.camera is not None,
                  f'{n_shots} shots baked'))
    gates.append(('TEXT', words_ok == len(texts) and len(texts) >= 20,
                  f'{words_ok}/{len(texts)} strings <= 3 words'))
    gates.append(('RENDER', sc.render.engine == 'BLENDER_WORKBENCH'
                  and sc.render.resolution_x == 1280,
                  'Workbench 1280x720@24'))
    lines = ['# SCENE VALIDATION (v3.1)', '']
    allpass = True
    for name, ok, detail in gates:
        allpass &= ok
        lines.append(f'{name}: {"PASS" if ok else "FAIL"} — {detail}')
    lines.append('')
    lines.append('ALL PASS' if allpass else 'HAS FAILURES')
    with open(REPORT, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines) + '\n')
    print('\n'.join(lines))
    return allpass


def main():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    dur = probe_wav(AUDIO)
    total_f = int(dur * FPS) + 2
    print(f'AUDIO {dur:.2f}s -> {total_f} frames @ {FPS}fps')
    words = load_words()
    print(f'transcript words: {len(words)}')
    ordered = order_sequences(words)
    print('sequence order (narration topic order):')
    for i, spec in enumerate(ordered):
        print(f'  {i + 1:2d}. {spec["id"]} {spec["title"]}')
    windows, anchored = compute_windows(total_f, words, ordered)
    print(f'anchor-driven bounds: {anchored}/18')

    L.scene_setup(total_f)
    cam = L.cam_make()
    for i, spec in enumerate(ordered):
        f0, f1 = windows[i], windows[i + 1]
        before = set(bpy.data.objects)
        spec['build'](f0, f1)
        # sequence isolation: objects visible ONLY inside their window
        for ob in set(bpy.data.objects) - before:
            vis_keys(ob, f0, f1)

    n_shots = bake_camera(cam, windows, total_f)
    snd = add_audio(bpy.context.scene)
    validate(bpy.context.scene, windows, n_shots, snd, total_f)

    with open(WINJ, 'w', encoding='utf-8') as f:
        json.dump([[ordered[i]['id'], windows[i], windows[i + 1]]
                   for i in range(len(ordered))], f, indent=1)

    os.makedirs(PREV, exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=BLEND)
    print('BLEND SAVED', BLEND)

    for t in (5, 60, 150, 260, 380, 500, 620, 760, 830):
        fr = min(total_f, int(t * FPS) + 1)
        bpy.context.scene.frame_set(fr)
        bpy.context.scene.render.filepath = os.path.join(
            PREV, f'p_t{fr:05d}.jpg')
        bpy.ops.render.render(write_still=True)
    print('PREVIEWS DONE')
    print(f'GENERATOR OK: {total_f} frames, {n_shots} shots, '
          f'{len(ordered)} sequences')


main()
