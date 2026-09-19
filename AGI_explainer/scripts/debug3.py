"""debug3.py — decisive: is hide_viewport breaking Workbench renders?
Run: blender -b final_scene.blend -P scripts/debug3.py"""
import bpy
from mathutils import Vector

scene = bpy.context.scene
cams = [o.name for o in bpy.data.objects if o.type == 'CAMERA']
print('cameras:', cams, '| scene.camera:', scene.camera.name)
print('lens:', scene.camera.data.lens, 'sensor:',
      scene.camera.data.sensor_width)

scene.frame_set(121)
cam = scene.camera
mw = cam.matrix_world
inv = mw.inverted()
for name in ('core', 'title', 'GROUND'):
    ob = bpy.data.objects[name]
    p = inv @ ob.matrix_world.translation   # camera space
    print(f'{name}: cam-space {tuple(round(v, 2) for v in p)}')

# render A: as-is
scene.render.filepath = ('/home/z/my-project/AGI_explainer/renders/'
                         'preview/testA_f121.jpg')
bpy.ops.render.render(write_still=True)

# render B: hide_viewport force-cleared on ALL objects
for ob in bpy.data.objects:
    ob.hide_viewport = False
scene.render.filepath = ('/home/z/my-project/AGI_explainer/renders/'
                         'preview/testB_f121.jpg')
bpy.ops.render.render(write_still=True)
print('DEBUG3 DONE')
