"""Render worker: renders an assigned list of frames from the built .blend.

Usage (inside blender):
  blender -b render/agi_video.blend -P scripts/render_worker.py -- <needed.txt> <worker_id> <outdir> <line_start> <line_end>
Renders JPEG (quality 92) as f%06d.jpg
"""
import bpy
import os
import sys
import time

argv = sys.argv[sys.argv.index("--") + 1:]
list_path, worker_id, out_dir = argv[0], argv[1], argv[2]
start_line = int(argv[3]) if len(argv) > 3 else 0
end_line = int(argv[4]) if len(argv) > 4 else 10**9

with open(list_path) as f:
    frames = [int(x) for x in f.read().split() if x.strip()]
frames = frames[start_line:end_line]

os.makedirs(out_dir, exist_ok=True)
sc = bpy.context.scene
sc.render.engine = "BLENDER_WORKBENCH"
sh = sc.display.shading
sh.light = "STUDIO"
sh.show_cavity = True
sh.show_object_outline = True
if os.environ.get("WB_SHADOWS", "1") == "1":
    sh.show_shadows = True
else:
    sh.show_shadows = False
sc.render.image_settings.file_format = "JPEG"
sc.render.image_settings.quality = 92
sc.render.resolution_x = int(os.environ.get("OUT_W", "1280"))
sc.render.resolution_y = int(os.environ.get("OUT_H", "720"))
sc.render.film_transparent = False

t0 = time.time()
done = 0
for fr in frames:
    sc.frame_set(fr)
    sc.render.filepath = os.path.join(out_dir, "f%06d.jpg" % fr)
    bpy.ops.render.render(write_still=True)
    done += 1
    if done % 25 == 0:
        rate = done / max(time.time() - t0, 0.001)
        print("[worker %s] %d/%d (%.2f f/s)" % (worker_id, done, len(frames), rate), flush=True)

print("[worker %s] DONE %d frames in %.1fs" % (worker_id, done, time.time() - t0), flush=True)
