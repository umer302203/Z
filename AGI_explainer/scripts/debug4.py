"""debug4.py — dump camera fcurves: keys + evaluated state at 121.
Run: blender -b final_scene.blend -P scripts/debug4.py"""
import bpy
from mathutils import Vector

scene = bpy.context.scene
cam = scene.camera
ad = cam.animation_data
print('action:', ad.action.name if ad and ad.action else None)
if ad and ad.action:
    for fc in ad.action.fcurves:
        kfs = [(int(k.co[0]), round(k.co[1], 2)) for k in fc.keyframe_points]
        ev = round(fc.evaluate(121), 3)
        print(f'{fc.data_path}[{fc.array_index}] n={len(kfs)} '
              f'first4={kfs[:4]} last2={kfs[-2:]} eval121={ev}')

scene.frame_set(121)
dg = bpy.context.evaluated_depsgraph_get()
ce = cam.evaluated_get(dg)
mw = ce.matrix_world
print('eval loc:', tuple(round(v, 2) for v in mw.translation))
fwd = mw.to_3x3() @ Vector((0, 0, -1))
print('aim dir:', tuple(round(v, 3) for v in fwd))
# direction from camera to origin (where cubes are)
to_origin = -mw.translation
print('dir to origin:', tuple(round(v, 3) for v in to_origin.normalized()))
