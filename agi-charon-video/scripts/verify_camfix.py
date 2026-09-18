"""Verify camera hold fix: evaluate camera at formerly-drifting frames."""
import sys

sys.path.insert(0, "/home/z/my-project/scripts")
import bpy  # noqa

checks = [
    (11400, 12001.9, "S13 hold (was 12083.57 - drift)"),
    (16770, 17001.9, "S17 hold (was 16005 - wrong key fixed)"),
    (18600, 18000.4, "S18 hold"),
    (21810, 21000.0, "S21 hold (only start key)"),
    (22950, 22001.0, "S22 hold"),
    (24060, 23000.0, "S23 hold"),
    (25050, 23000.0, "S24 hold (was drifting)"),
]
sc = bpy.context.scene
cam = bpy.data.objects.get("main_cam")
ok = 0
for f, want_x, label in checks:
    sc.frame_set(f)
    dg = bpy.context.evaluated_depsgraph_get()
    ev = None
    for o in dg.objects:
        if o.original.name == cam.name:
            ev = o
            break
    x = ev.matrix_world.to_translation().x
    good = abs(x - want_x) < 3.0
    ok += good
    print("f%d %-38s x=%10.2f want~%8.1f %s"
          % (f, label, x, want_x, "OK" if good else "FAIL"))
print("PASSED %d/%d" % (ok, len(checks)))
