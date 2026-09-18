"""Check delta transforms, constraints, drivers on main_cam."""
import bpy

cam = bpy.data.objects.get("main_cam")
print("delta_location:", [round(v, 3) for v in cam.delta_location])
print("delta_scale:", [round(v, 3) for v in cam.delta_scale])
print("delta_rot:", [round(v, 4) for v in cam.delta_rotation_euler])
print("constraints:", len(cam.constraints))
for c in cam.constraints:
    print("  ", c.type, c.name, "influence:", getattr(c, "influence", "-"),
          "target:", getattr(c, "target", None))
ad = cam.animation_data
if ad:
    print("drivers:", len(ad.drivers))
    for d in ad.drivers:
        print("  driver:", d.data_path, d.array_index, "->", d.driver.expression[:60])
print("matrix_basis:", [round(v, 2) for v in cam.matrix_basis.to_translation()])
print("matrix_local:", [round(v, 2) for v in cam.matrix_local.to_translation()])
