"""Evaluate camera x-fcurve directly + dump keys 11200-12500."""
import bpy

cam = bpy.data.objects.get("main_cam")
fc = None
for f in cam.animation_data.action.fcurves:
    if f.data_path == "location" and f.array_index == 0:
        fc = f
print("fc.evaluate(11400) =", round(fc.evaluate(11400), 3))
print("fc.evaluate(11300) =", round(fc.evaluate(11300), 3))
print("fc.evaluate(12000) =", round(fc.evaluate(12000), 3))
print("fc.evaluate(12270) =", round(fc.evaluate(12270), 3))
print("fc.evaluate(12300) =", round(fc.evaluate(12300), 3))
keys = [(int(k.co[0]), round(k.co[1], 2)) for k in fc.keyframe_points
        if 11000 <= k.co[0] <= 12600]
print("keys 11000-12600:", keys)
# sample: which key comes right after 11238?
allk = sorted([(k.co[0], k.co[1]) for k in fc.keyframe_points])
for i, (fr, val) in enumerate(allk):
    if fr >= 11238:
        print("next keys after 11238:", [(round(a, 1), round(b, 2)) for a, b in allk[i:i+5]])
        break
