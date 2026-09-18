"""Deep probe: main_cam fcurves, parent chain, local vs world loc at f11400."""
import bpy

cam = bpy.data.objects.get("main_cam")
print("PARENT:", cam.parent.name if cam.parent else None,
      "| parent type:", cam.parent.type if cam.parent else "-")
print("LOCAL LOC:", [round(v, 3) for v in cam.location])
print("WORLD LOC:", [round(v, 3) for v in cam.matrix_world.to_translation()])

p = cam.parent
while p:
    print("  parent:", p.name, "loc:", [round(v, 2) for v in p.location],
          "anim:", bool(p.animation_data and p.animation_data.action))
    p = p.parent

act = cam.animation_data.action if cam.animation_data else None
print("ACTION:", act.name if act else None, "| fcurves:", len(act.fcurves) if act else 0)
if act:
    for fc in act.fcurves:
        kp = fc.keyframe_points
        # keys within +/- 300 frames of 11400
        near = [(int(k.co[0]), round(k.co[1], 2)) for k in kp if 11100 <= k.co[0] <= 11700]
        print("  FC", fc.data_path, fc.array_index, "n_keys:", len(kp), "near_11400:", near[:6])

# what is at x=83.57 in stage-local space? check sweep objects
for c in bpy.data.collections:
    if "S13" in c.name:
        for ob in c.all_objects:
            lx = ob.matrix_world.to_translation().x - 12000
            if 60 < lx < 110:
                print("STAGE OBJ at local x=%.1f:" % lx, ob.name)
        break
print("---- objects named *sweep*/*cam* anywhere:")
for ob in bpy.data.objects:
    ln = ob.name.lower()
    if "sweep" in ln or "cam" in ln:
        print(" ", ob.name, ob.type, "loc:", [round(v, 2) for v in ob.location],
              "parent:", ob.parent.name if ob.parent else None)
