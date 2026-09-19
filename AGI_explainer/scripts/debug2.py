"""debug2.py — ground truth: fcurve keys + depsgraph-evaluated hide + test renders.
Run: blender -b final_scene.blend -P scripts/debug2.py"""
import bpy

scene = bpy.context.scene
TEST_FRAMES = (121, 3601)

for name in ('core', 'title', 'lk0', 'base'):
    ob = bpy.data.objects.get(name)
    if not ob:
        print(f'{name}: NOT FOUND')
        continue
    ad = ob.animation_data
    print(f'=== {name}: hide_render keys:')
    if ad and ad.action:
        for fc in ad.action.fcurves:
            if 'hide_render' in fc.data_path:
                print('   ', [(int(k.co[0]), round(k.co[1], 2)) for k in
                              fc.keyframe_points])
                for fr in TEST_FRAMES:
                    print(f'    evaluate({fr}) = {fc.evaluate(fr):.3f}')
    else:
        print('    no animation data')

for fr in TEST_FRAMES:
    scene.frame_set(fr)
    dg = bpy.context.evaluated_depsgraph_get()
    vis, hid = [], []
    for ob in bpy.data.objects:
        if ob.type == 'CAMERA':
            continue
        oe = ob.evaluated_get(dg)
        (vis if not oe.hide_render else hid).append(ob.name)
    print(f'--- frame {fr}: EVAL visible={len(vis)} hidden={len(hid)}')
    print('    vis:', sorted(vis)[:10])

for fr in TEST_FRAMES:
    scene.frame_set(fr)
    scene.render.filepath = f'/home/z/my-project/AGI_explainer/renders/preview/test_f{fr}.jpg'
    bpy.ops.render.render(write_still=True)
    print('rendered test frame', fr)
