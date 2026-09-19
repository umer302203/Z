"""Render 3 test frames from the real scene + debug camera transform."""
import bpy
from mathutils import Vector

sc = bpy.context.scene
cam = sc.camera

print("parent:", cam.parent.name if cam.parent else None)
print("matrix_basis loc:", tuple(round(v, 2) for v in cam.matrix_basis.translation))
if cam.parent:
    print("parent loc:", tuple(round(v, 2) for v in cam.parent.matrix_world.translation))

for fr in (100, 600, 5000):
    sc.frame_set(fr)
    bpy.context.view_layer.update()
    w = cam.matrix_world.translation
    print("f%d cam world=(%.2f,%.2f,%.2f) basis=(%.2f,%.2f,%.2f)" % (
        fr, w.x, w.y, w.z,
        cam.matrix_basis.translation.x, cam.matrix_basis.translation.y,
        cam.matrix_basis.translation.z))
    sc.render.filepath = "/tmp/diag_f%d.png" % fr
    bpy.ops.render.render(write_still=True)

print("RENDER3_OK")
