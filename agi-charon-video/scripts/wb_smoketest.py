"""Workbench GL render smoke test under Xvfb."""
import bpy
import time

sc = bpy.context.scene
sc.render.engine = "BLENDER_WORKBENCH"
sc.display.shading.light = "STUDIO"
sc.display.shading.show_shadows = True
sc.display.shading.show_cavity = True
sc.render.resolution_x = 640
sc.render.resolution_y = 360
sc.render.filepath = "/tmp/wb_test.png"

t = time.time()
bpy.ops.render.render(write_still=True)
dt = time.time() - t
print("RENDER_SECONDS=%.2f" % dt)

# GPU/GL backend info
prefs = bpy.context.preferences_addons.get("cycles")
try:
    import gpu
    gpu.state.blend_set("ALPHA")
    print("GPU_MODULE_OK")
except Exception as e:
    print("GPU_MODULE_FAIL:", e)
