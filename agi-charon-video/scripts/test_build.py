"""Sanity test: build robot + surgeon + props + Devanagari text, render preview."""
import sys
sys.path.insert(0, "/home/z/my-project/scripts")
import bpy
from build import common as C
from build import robot, props, surgeon

C.clear_default_scene()
C.setup_workbench_scene()
sc = bpy.context.scene

# load Devanagari-capable font for 3D text
try:
    f = bpy.data.fonts.load("/home/z/.fonts/NotoSansDevanagari-Bold.ttf")
    C.DEVANAGARI_FONT = f
    print("FONT_LOADED:", f.name)
except Exception as e:
    print("FONT_FAIL:", e)

lib = C.get_library()

# robot at origin
r = robot.build_robot(lib)
print("ROBOT_OK objects=", len(r["objects"]))

# apple + table + cup
props.build_table(lib)
props.build_apple(lib, loc=None) if False else None
props.build_cup(lib)

# surgeon + desk + calc + book
surgeon.build_surgeon(lib)
surgeon.build_desk(lib)
surgeon.build_calculator(lib)
surgeon.build_stethoscope(lib)
surgeon.build_scalpel(lib)
surgeon.build_syringe(lib)
print("SURGEON_OK")

props.build_book(lib, title="TEST")
print("BOOK_OK")

# Devanagari text test in scene
if hasattr(C, "DEVANAGARI_FONT") and C.DEVANAGARI_FONT:
    import math as _m
    t = C.text3d("hi_test", "ध्यान और मेमरी", 0.3, loc=(0, -3, 1.6), rot=(_m.radians(90), 0, 0),
                 m=C.mat("txt", (0.1, 0.1, 0.2, 1)))
    if C.DEVANAGARI_FONT:
        t.data.font = C.DEVANAGARI_FONT

# stage copies: robot+table+apple stage at x=0
st0, off0 = C.new_stage(0, "T0")
robot_copy = C.copy_hierarchy(r["root"], st0, (off0, 0, 0))
C.ground("g0", m=C.mat("floor", (0.88, 0.89, 0.92, 1)), col_target=st0)

# surgeon stage at x=1000 (surgeon behind desk: y=+0.3)
st1, off1 = C.new_stage(1, "T1")
surg_root = [o for o in lib.objects if o.name.startswith("surgeon_root")]
if surg_root:
    C.copy_hierarchy(surg_root[0], st1, (off1 + 2.0, 0.30, 0))
desk_objs = [o for o in lib.objects if o.name.startswith("desk_")]
for o in desk_objs:
    C.stage_copy(o, st1, (off1 + 2.0, -0.15, 0))
calc_objs = [o for o in lib.objects if o.name.startswith("calc_")]
for o in calc_objs:
    C.stage_copy(o, st1, (off1 + 1.35, -0.35, 0.78))
C.ground("g1", m=C.mat("floor", (0.88, 0.89, 0.92, 1)), loc=(off1 + 2, 0, 0), col_target=st1)

# lights + camera + visibility
lights0 = C.scene_lights((4, -5, 6), stage_off=(off0, 0, 0), col_target=st0)
for L in lights0.values():
    C.aim_light(L, (0, 0, 1), (off0, 0, 0))
lights1 = C.scene_lights((off1 + 6, -5, 6), stage_off=(0, 0, 0), col_target=st1)
for L in lights1.values():
    C.aim_light(L, (off1 + 2, 0, 1), (0, 0, 0))

# hide library
for ob in lib.objects:
    ob.hide_render = True
    ob.hide_viewport = True

cam = C.make_camera("cam", (3.4, -4.2, 2.0), (0, 0, 1.0), lens=45)
cam2 = C.make_camera("cam2", (off1 + 4.5, -4.0, 1.8), (off1 + 2.0, 0, 1.1), lens=40)

sc.camera = cam
sc.frame_set(1)
sc.render.filepath = "/tmp/test_robot.png"
bpy.ops.render.render(write_still=True)
sc.camera = cam2
sc.render.filepath = "/tmp/test_surgeon.png"
bpy.ops.render.render(write_still=True)
print("TEST_DONE")
