"""Debug: close-up renders of robot chest/head + print child world positions."""
import sys
sys.path.insert(0, "/home/z/my-project/scripts")
import bpy
from build import common as C
from build import robot

C.clear_default_scene()
C.setup_workbench_scene()
sc = bpy.context.scene
lib = C.get_library()
r = robot.build_robot(lib)

# print world positions of key parts
bpy.context.view_layer.update()
for name in ("robot_chest", "robot_chestPanel", "robot_chestCore", "robot_head",
             "robot_face", "robot_eyeLens_L", "robot_neckSeg", "robot_vent",
             "robot_pelvis", "robot_waist", "robot_sole_L"):
    ob = bpy.data.objects.get(name)
    if ob:
        print("POS %-22s world=%s parent=%s" % (
            name, tuple(round(v, 3) for v in ob.matrix_world.translation), ob.parent.name if ob.parent else "-"))
    else:
        print("POS %-22s MISSING" % name)

st0, off0 = C.new_stage(0, "T0")
C.copy_hierarchy(r["root"], st0, (off0, 0, 0))
C.ground("g0", m=C.mat("floor", (0.88, 0.89, 0.92, 1)), col_target=st0)
lights = C.scene_lights((3, -4, 5), stage_off=(off0, 0, 0), col_target=st0)
for L in lights.values():
    C.aim_light(L, (0, 0, 1.2), (off0, 0, 0))
for ob in lib.objects:
    ob.hide_render = True
    ob.hide_viewport = True

cam = C.make_camera("cam", (1.2, -2.2, 1.55), (0, 0, 1.35), lens=50)
sc.camera = cam
sc.frame_set(1)
sc.render.filepath = "/tmp/dbg_chest.png"
bpy.ops.render.render(write_still=True)
print("DEBUG_DONE")
