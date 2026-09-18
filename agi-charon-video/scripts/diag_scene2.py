"""Diagnose at frame 100: camera keyframes + object scales over time."""
import bpy

sc = bpy.context.scene
cam = sc.camera

print("== CAMERA FCURVES ==")
for fc in cam.animation_data.action.fcurves if cam.animation_data else []:
    kp = fc.keyframe_points
    samples = ["f%d=%.1f" % (int(k.co[0]), k.co[1]) for k in kp[:6]]
    print("  %s[%d]: %s" % (fc.data_path, fc.array_index, " ".join(samples)))

sc.frame_set(100)
print("== FRAME 100 ==")
print("cam loc:", tuple(round(v, 2) for v in cam.matrix_world.translation))

for name in ("s01_bookA0", "s01_calc_body", "s01_desk", "pad"):
    ob = bpy.data.objects.get(name)
    if ob:
        print("  %s scale=%s hide_render=%s" % (name, tuple(round(s, 3) for s in ob.scale), ob.hide_render))

# sample scale fcurve of one object
ob = bpy.data.objects.get("s01_bookA0")
if ob and ob.animation_data:
    for fc in ob.animation_data.action.fcurves:
        kps = ["f%d=%.2f" % (int(k.co[0]), k.co[1]) for k in fc.keyframe_points[:8]]
        print("  bookA0 %s[%d]: %s" % (fc.data_path, fc.array_index, " ".join(kps)))
        break

# count meshes with non-degenerate world bbox at frame 100
from mathutils import Vector
good = 0
for ob in bpy.data.objects:
    if ob.type != "MESH" or ob.hide_render:
        continue
    bb = [ob.matrix_world @ Vector(c) for c in ob.bound_box]
    ext = max(max(v[i] for v in bb) - min(v[i] for v in bb) for i in range(3))
    if ext > 0.01:
        good += 1
print("non-degenerate meshes at f100:", good)
