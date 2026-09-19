"""Dump fcurve modifiers + NLA tracks on main_cam."""
import bpy

cam = bpy.data.objects.get("main_cam")
ad = cam.animation_data
act = ad.action
print("ACTION:", act.name)
for fc in act.fcurves:
    mods = list(fc.modifiers)
    if mods:
        for m in mods:
            print("FC", fc.data_path, fc.array_index, "MOD:", m.type, m.name)
    else:
        print("FC", fc.data_path, fc.array_index, "no modifiers")

print("NLA TRACKS:", len(ad.nla_tracks))
for tr in ad.nla_tracks:
    print("  track:", tr.name, "mute:", tr.mute, "strips:", len(tr.strips))
    for s in tr.strips:
        print("    strip:", s.name, "action:", s.action.name if s.action else None,
              "frame range:", round(s.frame_start, 1), "-", round(s.frame_end, 1),
              "extrap:", s.extrapolation, "blend:", s.blend_type)

# Also: evaluate camera world loc CORRECTLY at f11400 via depsgraph
sc = bpy.context.scene
sc.frame_set(11400)
dg = bpy.context.evaluated_depsgraph_get()
ev = dg.objects.get(cam.name, None)
if ev is None:
    for o in dg.objects:
        if o.original.name == cam.name:
            ev = o
            break
print("EVALUATED LOC @11400:", [round(v, 3) for v in ev.matrix_world.to_translation()])
