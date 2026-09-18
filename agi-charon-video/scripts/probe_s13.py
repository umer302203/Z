"""Probe blend at frame 11400 (380s, S13): camera pose + stage object states."""
import bpy
import sys

sys.path.insert(0, "/home/z/my-project/scripts")

f = 11400
bpy.context.scene.frame_set(f)

# find the S13 stage and camera
cam = bpy.data.objects.get("main_cam") or [o for o in bpy.data.objects if o.type == "CAMERA"][0]
print("CAM:", cam.name)
mw = cam.matrix_world
loc = mw.to_translation()
print("CAM LOC:", [round(v, 2) for v in loc])
rot = mw.to_euler()
print("CAM ROT deg:", [round(__import__("math").degrees(a), 1) for a in rot])

# where does it look? camera -Z axis
import mathutils
d = (mw.to_3x3() @ mathutils.Vector((0, 0, -1))).normalized()
print("CAM FORWARD:", [round(v, 3) for v in d])
# point 4m along forward
p = loc + d * 4
print("LOOKS AT ~", [round(v, 2) for v in p])

# stage collections
for c in bpy.data.collections:
    if "S13" in c.name:
        print("STAGE COLLECTION:", c.name, "objects:", len(c.all_objects))
        n = 0
        for ob in c.all_objects:
            if ob.type == "MESH" and n < 40:
                s = ob.matrix_world.to_scale()
                v = ob.matrix_world.to_translation()
                print("  %-24s scale=(%.2f,%.2f,%.2f) loc=(%.1f,%.1f,%.1f) hide_render=%s"
                      % (ob.name, s.x, s.y, s.z, v.x, v.y, v.z, ob.hide_render))
                n += 1
        break
