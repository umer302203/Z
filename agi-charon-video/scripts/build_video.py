"""Master builder: constructs ALL shots, keyframes visibility + camera,
saves render/agi_video.blend and data/shot_plan.json.

Run: blender -b --factory-startup -P scripts/build_video.py
"""
import json
import math
import os
import sys

sys.path.insert(0, "/home/z/my-project/scripts")

import bpy  # noqa
from build import common as C
from build import kit as K
from build import props, robot as robot_mod, surgeon as surgeon_mod
from build import scenes_a, scenes_b

BASE = "/home/z/my-project"
FPS = 30
DURATION = 837.84
TOTAL = int(round(DURATION * FPS))  # 25135.2 -> 25136


def sweep_stray_objects():
    """Any object left in the scene root collection gets filed into the stage
    whose X-region contains it (or LIBRARY if x < 0). Cameras excluded!"""
    scene_col = bpy.context.scene.collection
    strays = [ob for ob in scene_col.objects if ob.type != "CAMERA"]
    for ob in strays:
        x = ob.matrix_world.translation.x if ob.parent is None else 0.0
        idx = int(math.floor((x + 500.0) / 1000.0))
        if idx < 0:
            C.link_to(ob, C.get_library())
        else:
            # find stage collection by index
            name = "STAGE_S%02d" % (idx + 1)
            tgt = bpy.data.collections.get(name)
            if tgt is None:
                tgt = bpy.data.collections.get("LIBRARY")
            C.link_to(ob, tgt)


def main():
    C.clear_default_scene()
    C.setup_workbench_scene()
    sc = bpy.context.scene
    lib = C.get_library()
    for ob_col in (lib,):
        pass

    # ---------- library assets
    rob = robot_mod.build_robot(lib, "robot")
    surg = surgeon_mod.build_surgeon(lib, "surgeon")
    # student variant: navy sweater, no coat/cap/steth
    stud = surgeon_mod.build_surgeon(lib, "student",
                                     scrub_rgba=(0.22, 0.28, 0.52, 1),
                                     with_cap=False, coat=False)
    assets = {"robot": rob, "surgeon": surg, "student": stud}

    # ---------- global camera (keyframed across all shots)
    cam = C.make_camera("main_cam", (0, -5, 2), (0, 0, 1), lens=42)
    assets["cam"] = cam
    sc.camera = cam

    # ---------- build shots
    shots = []
    shots += scenes_a.build_all(0, lib, assets)     # S01..S12 -> stages 0..11
    shots += scenes_b.build_all(12, lib, assets)    # S13..S24 -> stages 12..23
    shots.sort(key=lambda s: s["t0"])

    sweep_stray_objects()

    # hide library at render time
    for ob in lib.objects:
        ob.hide_render = True
        ob.hide_viewport = True

    # ---------- FIX: camera must NEVER be hidden for render
    cam.hide_render = False
    cam.hide_viewport = False
    if cam.animation_data and cam.animation_data.action:
        ad = cam.animation_data.action
        for fc in list(ad.fcurves):
            if fc.data_path in ("hide_render", "hide_viewport"):
                ad.fcurves.remove(fc)
    # also make sure the camera is not inside a stage collection
    for coll in list(bpy.data.collections):
        if cam.name in [o.name for o in coll.objects]:
            coll.objects.unlink(cam)
    C.link_to(cam, lib)
    cam.hide_render = False
    cam.hide_viewport = False

    # ---------- per-shot visibility keyframes
    for i, shot in enumerate(shots):
        stage_col = bpy.data.collections.get("STAGE_%s" % shot["id"])
        if stage_col is None:
            print("MISSING STAGE COL for", shot["id"])
            continue
        f_in = max(1, K.f(shot["t0"]) if i > 0 else 1)
        f_out = min(TOTAL, K.f(shot["t1"]) - 1 if i < len(shots) - 1 else TOTAL)
        objs = list(stage_col.objects)
        # include children linked elsewhere (all our stuff is linked into stage col)
        C.kf_vis(objs, f_in, f_out)
        print("VIS %-4s frames %d-%d objects=%d" % (shot["id"], f_in, f_out, len(objs)))

    # scene frame range
    sc.frame_start = 1
    sc.frame_end = TOTAL

    # ---------- FIX: HOLD each shot's last camera pose till shot end, then
    # HARD-CUT to the next shot's first key. Kills the stage-to-stage drift
    # that produced empty frames between a shot's last cam key and its end.
    _act = cam.animation_data.action
    _shots = sorted(shots, key=lambda s: s["t0"])
    _nfix = 0
    for _s in _shots:
        _f_hold = min(int(round(_s["t1"] * FPS)), TOTAL)
        for _fc in _act.fcurves:
            if _fc.data_path not in ("location", "rotation_euler"):
                continue
            _last = None
            for _k in _fc.keyframe_points:
                # STRICTLY before shot end: at shared boundaries (t1 == next
                # t0) the key AT f_hold belongs to the NEXT shot!
                if _k.co[0] < _f_hold - 0.5:
                    _last = _k
                else:
                    break
            if _last is not None and _last.interpolation != "CONSTANT":
                _last.interpolation = "CONSTANT"
                _nfix += 1
    print("CAM_HOLD_FIX: %d keys set CONSTANT" % _nfix)

    # ---------- save
    os.makedirs(f"{BASE}/render", exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=f"{BASE}/render/agi_video.blend")

    plan = {"fps": FPS, "duration": DURATION, "total_frames": TOTAL, "shots": shots}
    with open(f"{BASE}/data/shot_plan.json", "w") as fjson:
        json.dump(plan, fjson, indent=1)

    print("BUILD_OK shots=%d objects=%d total_frames=%d" % (
        len(shots), len(bpy.data.objects), TOTAL))


main()
