"""Benchmark Workbench render speed at 1080p and 720p with a moderately complex scene."""
import bpy
import time
import math

sc = bpy.context.scene
sc.render.engine = "BLENDER_WORKBENCH"
sh = sc.display.shading
sh.light = "STUDIO"
sh.show_shadows = True
sh.show_cavity = True
sh.show_object_outline = True

# Build test scene: grid of objects with varied colors
colors = [(0.8, 0.2, 0.2, 1), (0.2, 0.6, 0.3, 1), (0.2, 0.3, 0.8, 1),
          (0.9, 0.7, 0.1, 1), (0.8, 0.8, 0.85, 1), (0.1, 0.1, 0.12, 1)]
for ix in range(8):
    for iy in range(8):
        x = ix % 2
        bpy.ops.mesh.primitive_cube_add(size=0.8, location=(ix * 1.1, iy * 1.1, 0.4))
        ob = bpy.context.object
        mat = bpy.data.materials.new("m")
        mat.diffuse_color = colors[(ix + iy) % len(colors)]
        ob.data.materials.append(mat)
bpy.ops.mesh.primitive_plane_add(size=40, location=(4, 4, 0))

# Camera
cam_data = bpy.data.cameras.new("cam")
cam = bpy.data.objects.new("cam", cam_data)
sc.collection.objects.link(cam)
cam.location = (4, -10, 6)
cam.rotation_euler = (math.radians(60), 0, 0)
sc.camera = cam

sc.render.resolution_x = 1920
sc.render.resolution_y = 1080
sc.render.filepath = "/tmp/bench1080_"

t = time.time()
for i in range(3):
    sc.render.filepath = "/tmp/bench1080_%d.png" % i
    bpy.ops.render.render(write_still=True)
dt1080 = (time.time() - t) / 3
print("AVG_1080P=%.2fs" % dt1080)

sc.render.resolution_x = 1280
sc.render.resolution_y = 720
t = time.time()
for i in range(3):
    sc.render.filepath = "/tmp/bench720_%d.png" % i
    bpy.ops.render.render(write_still=True)
dt720 = (time.time() - t) / 3
print("AVG_720P=%.2fs" % dt720)

print("EST_25135_FRAMES_1080P=%.1f_hours" % (dt1080 * 25135 / 3600))
print("EST_5000_FRAMES_1080P=%.1f_hours" % (dt1080 * 5000 / 3600))
print("EST_5000_FRAMES_720P=%.1f_hours" % (dt720 * 5000 / 3600))
