#!/usr/bin/env python3
"""verify_text.py — standalone TEXT RULE audit of a .blend (runs in Blender).
TEXT RULE: every on-screen string <=3 words (alnum tokens; symbols allowed)."""
import bpy, sys, os

BLEND = sys.argv[sys.argv.index("--") + 1] if "--" in sys.argv else "/home/z/my-project/agi_video/final_scene.blend"

def text_words(body):
    n = 0
    for tok in body.split():
        if any(c.isalnum() for c in tok):
            n += 1
    return n

bpy.ops.wm.open_mainfile(filepath=BLEND)
txts = [o for o in bpy.data.objects if o.type == 'FONT']
bad, report = [], []
for o in txts:
    body = o.get("text_body", o.data.body)
    n = text_words(body)
    mark = "OK " if n <= 3 else "BAD"
    report.append(f"{mark} [{n}] {body!r}")
    if n > 3:
        bad.append(body)
print("\n".join(report))
print(f"TEXT_AUDIT: {'PASS' if not bad else 'FAIL'} ({len(txts)} strings, {len(bad)} violations)")
if bad:
    sys.exit(2)
