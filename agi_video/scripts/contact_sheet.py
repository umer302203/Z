"""contact_sheet.py — render 14 stills across the video + ffmpeg tile grids.
Run inside Blender."""
import bpy, os, subprocess

AGI = "/home/z/my-project/agi_video"
OUT = os.path.join(AGI, "reports", "sheet")
os.makedirs(OUT, exist_ok=True)
sc = bpy.context.scene
FRAMES = [500, 2000, 3600, 5200, 6800, 8400, 10000, 11600, 13200, 14800, 16400, 18000, 19300, 20050]
paths = []
for f in FRAMES:
    sc.frame_set(f)
    p = os.path.join(OUT, f"c{f:05d}.jpg")
    sc.render.filepath = p
    bpy.ops.render.render(write_still=True)
    paths.append(p)
print("STILLS DONE:", len(paths))
