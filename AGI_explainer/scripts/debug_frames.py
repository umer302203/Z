"""debug_frames.py — evaluate scene visibility at preview frames.
Run: blender -b final_scene.blend -P scripts/debug_frames.py"""
import bpy

TEST = (121, 3601, 12001, 18241)

with open('/home/z/my-project/AGI_explainer/reports/sequence_windows.json') as f:
    wins = [(r[0], r[1], r[2]) for r in json.load(open(
        '/home/z/my-project/AGI_explainer/reports/sequence_windows.json'))] \
        if False else None

import json
wins = json.load(open('/home/z/my-project/AGI_explainer/reports/'
                      'sequence_windows.json'))

def owner(fr):
    for sid, a, b in wins:
        if a <= fr <= b:
            return f'{sid} [{a}-{b}]'
    return '??'

scene = bpy.context.scene
for fr in TEST:
    scene.frame_set(fr)
    vis = [o.name for o in bpy.data.objects
           if o.type != 'CAMERA' and not o.hide_render]
    cam = scene.camera
    print(f'--- frame {fr} owner={owner(fr)} visible={len(vis)}')
    print(f'    cam loc=({cam.location.x:.1f},{cam.location.y:.1f},'
          f'{cam.location.z:.1f})')
    print('    first vis:', vis[:8])
