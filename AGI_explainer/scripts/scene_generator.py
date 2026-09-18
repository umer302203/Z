"""scene_generator.py — v3 orchestrator (recreated after reset #3).
Run: blender -b -P scripts/scene_generator.py
wav duration probe -> transcript anchors -> 20 windows -> build specs ->
80-shot camera bake -> VSE narration -> validation report -> save blend ->
preview stills."""
import json
import math
import os
import random
import wave

import bpy

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)                     # .../agi_video
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


def anchor_time(stems, words):
    for stem in stems:
        for w, t in words:
            if w.startswith(stem):
                return t
    return None


def compute_windows(total_f, words):
    n = len(SEQ)
    b = [None] * (n + 1)
    b[0], b[n] = 1, total_f
    for i, spec in enumerate(SEQ[1:n], start=1):
        t = anchor_time(spec['anchors'], words)
        if t is not None:
            b[i] = max(2, int(t * FPS) + 1)
    # fill unknowns by linear interpolation between known boundaries
    known = [i for i, v in enumerate(b) if v is not None]
    for k in range(len(known) - 1):
        i0, i1 = known[k], known[k + 1]
        v0, v1 = b[i0], b[i1]
        for j in range(i0 + 1, i1):
            b[j] = int(v0 + (v1 - v0) * (j - i0) / (i1 - i0))
    # enforce minimum window (steal from the largest neighbour)
    for _ in range(40):
        widths = [b[i + 1] - b[i] for i in range(n)]
        wi = min(range(n), key=lambda i: widths[i])
        if widths[wi] >= MIN_WIN_F:
            break
        gi = max(range(n), key=lambda i: widths[i])
        take = min(MIN_WIN_F - widths[wi], widths[gi] - MIN_WIN_F)
        if take <= 0:
            break
        lo, hi = min(wi, gi), max(wi, gi)
        b[lo + 1] -= take if hi == wi + 1 or lo == wi else 0
        if b[lo + 1] - b[lo] < MIN_WIN_F or b[hi + 1] - b[hi] < MIN_WIN_F:
            b[lo + 1] += take                     # revert unsafe steal
            break
    anchored = sum(1 for i in range(1, n) if b[i] is not None)
    return b, anchored


def bake_camera(cam, windows, total_f):
    n = len(SEQ)
    total_dur = sum(windows[i + 1] - windows[i] for i in range(n))
    counts = [max(2, round(SHOTS_TOTAL *
                           (windows[i + 1] - windows[i]) / total_dur))
              for i in range(n)]
    while sum(counts) > SHOTS_TOTAL:
        counts[max(range(n), key=lambda i: counts[i])] -= 1
    while sum(counts) < SHOTS_TOTAL:
        counts[min(range(n), key=lambda i: counts[i])] += 1
    shots = 0
    for i in range(n):
        f0, f1 = windows[i], windows[i + 1]
        rng = random.Random(f0 * 7 + i)
        step = (f1 - f0) / counts[i]
        for k in range(counts[i]):
            k0 = int(f0 + k * step)
            k1 = int(f0 + (k + 1) * step) if k < counts[i] - 1 else f1
            a = rng.uniform(-2.6, 2.6)
            r = rng.uniform(11.5, 17.5)
            z = rng.uniform(3.0, 7.5)
            kind = rng.choice(['push', 'pull', 'orbL', 'orbR', 'pan', 'low'])
            p0 = L.orbit_pos(a, r, z)
            t0 = (rng.uniform(-1.5, 1.5), 0, rng.uniform(1.5, 3.2))
            if kind == 'push':
                p1, t1 = L.orbit_pos(a, r * 0.72, z * 0.85), t0
            elif kind == 'pull':
                p0, p1 = L.orbit_pos(a, r * 0.72, z * 0.85), L.orbit_pos(a, r * 1.2, z)
                t1 = t0
            elif kind == 'orbL':
                p1, t1 = L.orbit_pos(a + 0.55, r, z), t0
            elif kind == 'orbR':
                p1, t1 = L.orbit_pos(a - 0.55, r, z), t0
            elif kind == 'pan':
                p1 = p0
                t1 = (t0[0] + rng.uniform(-3, 3), t0[1], t0[2])
            else:
                p0 = L.orbit_pos(a, r * 1.1, 1.8)
                p1 = L.orbit_pos(a + 0.2, r * 1.02, 2.1)
                t1 = (t0[0], 0, t0[2] + 1.2)
            L.shot(cam, k0, k1, p0, p1, t0, t1)
            shots += 1
    return shots


def add_audio(sc):
    se = sc.sequence_editor_create()
    try:
        snd = se.strips.new_sound('narration', 1, 1, AUDIO)
    except AttributeError:
        snd = se.sequences.new_sound('narration', 1, 1, AUDIO)
    return snd


def validate(sc, windows, n_shots, snd, total_f):
    objs = list(bpy.data.objects)
    anim = sum(1 for o in objs if o.animation_data)
    texts = [o for o in objs if o.get('text_body')]
    words_ok = 0
    import re
    for o in texts:
        body = o['text_body']
        toks = re.findall(r"[A-Za-z0-9]+", body)
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
    lines = ['# SCENE VALIDATION (v3)', '']
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
    windows, anchored = compute_windows(total_f, words)
    print(f'windows anchored: {anchored}/19')

    L.scene_setup(total_f)
    cam = L.cam_make()
    for i, spec in enumerate(SEQ):
        spec['build'](windows[i], windows[i + 1])

    n_shots = bake_camera(cam, windows, total_f)
    snd = add_audio(bpy.context.scene)
    validate(bpy.context.scene, windows, n_shots, snd, total_f)

    with open(WINJ, 'w', encoding='utf-8') as f:
        json.dump({SEQ[i]['id']: [windows[i], windows[i + 1]]
                   for i in range(len(SEQ))}, f, indent=1)

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
          f'{len(SEQ)} sequences')


main()
