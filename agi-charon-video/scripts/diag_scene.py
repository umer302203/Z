"""Diagnose why frames render empty: camera, visibility, object positions."""
import bpy

sc = bpy.context.scene
sc.frame_set(1)

cam = sc.camera
print("CAMERA:", cam.name if cam else None,
      "loc:", tuple(round(v, 2) for v in cam.matrix_world.translation) if cam else "-")

vis = [ob for ob in bpy.data.objects
       if not ob.hide_render and ob.type in ("MESH", "EMPTY", "LIGHT", "CAMERA")]
print("VISIBLE objects at frame 1:", len(vis))

meshes = [ob for ob in vis if ob.type == "MESH"]
print("visible meshes:", len(meshes))
for ob in meshes[:10]:
    bb = [ob.matrix_world @ __import__("mathutils").Vector(c) for c in ob.bound_box]
    xs = [v.x for v in bb]; ys = [v.y for v in bb]; zs = [v.z for v in bb]
    print("  %-24s loc=(%.0f,%.0f,%.0f) x[%.0f..%.0f] y[%.0f..%.0f] z[%.0f..%.0f]" % (
        ob.name, ob.matrix_world.translation.x, ob.matrix_world.translation.y,
        ob.matrix_world.translation.z, min(xs), max(xs), min(ys), max(ys), min(zs), max(zs)))

# camera lens / clip
cd = cam.data
print("lens:", cd.lens, "clip:", cd.clip_start, cd.clip_end)
print("engine:", sc.render.engine)
