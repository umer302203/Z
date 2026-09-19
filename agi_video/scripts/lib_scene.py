"""Scene library v4 — Blender 4.5 Workbench, 1280x720@24fps. All proven fixes applied."""
import bpy, math, random
from mathutils import Vector

FPS = 24
RES_X, RES_Y = 1280, 720
LENS = 40.0

# Palette (hex)
PAL = {
    "bg":      "#1B1E28",
    "ground":  "#232734",
    "white":   "#E8EAF2",
    "cyan":    "#4FC3F7",
    "orange":  "#FF9E3D",
    "green":   "#7ED957",
    "red":     "#EF5350",
    "purple":  "#B388FF",
    "yellow":  "#FFD54F",
    "gray":    "#8A93A8",
    "deep":    "#2E3450",
}

def hx(h, a=1.0):
    h = h.lstrip("#")
    return (int(h[0:2], 16) / 255, int(h[2:4], 16) / 255, int(h[4:6], 16) / 255, a)

def rgba(name):
    return hx(PAL[name])

# ---------- scene ----------
def scene_setup(total_frames):
    sc = bpy.context.scene
    sc.render.engine = 'BLENDER_WORKBENCH'
    sc.display.shading.light = 'STUDIO'
    sc.display.shading.color_type = 'OBJECT'
    try:
        sc.display.shading.background_type = 'WORLD'
    except Exception:
        pass
    sc.render.resolution_x = RES_X
    sc.render.resolution_y = RES_Y
    sc.render.resolution_percentage = 100
    sc.render.fps = FPS
    sc.render.image_settings.file_format = 'JPEG'
    sc.render.image_settings.quality = 92
    sc.frame_start = 1
    sc.frame_end = total_frames
    try:
        sc.world.color = hx(PAL["bg"])
    except Exception:
        try:
            sc.world.color = hx(PAL["bg"])[:3]
        except Exception:
            pass
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    # ground
    bpy.ops.mesh.primitive_plane_add(size=400, location=(0, 0, -2.01))
    g = bpy.context.object
    g.name = "GROUND"
    g.color = rgba("ground")

def cam_make(name="CAM"):
    cd = bpy.data.cameras.new(name)
    cd.lens = LENS
    ob = bpy.data.objects.new(name, cd)
    bpy.context.collection.objects.link(ob)
    ob.location = (0, -12, 6)
    ob.rotation_euler = (math.radians(65), 0, 0)
    bpy.context.scene.camera = ob
    return ob

# ---------- builders (all return object; text objects carry ob['text_body']) ----------
def box(loc=(0, 0, 0), size=(2, 2, 2), name="Box", color="cyan"):
    bpy.ops.mesh.primitive_cube_add(location=loc)
    ob = bpy.context.object
    ob.name = name
    ob.scale = (size[0] / 2, size[1] / 2, size[2] / 2)
    ob.color = rgba(color)
    return ob

def sphere(loc=(0, 0, 0), r=1.0, name="Sphere", color="orange"):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r, location=loc, segments=32, ring_count=16)
    ob = bpy.context.object
    ob.name = name
    ob.color = rgba(color)
    return ob

def cyl(loc=(0, 0, 0), r=1.0, d=2.0, name="Cyl", color="green"):
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=d, location=loc, vertices=32)
    ob = bpy.context.object
    ob.name = name
    ob.color = rgba(color)
    return ob

def torus(loc=(0, 0, 0), R=2.0, r=0.35, name="Torus", color="purple"):
    bpy.ops.mesh.primitive_torus_add(major_radius=R, minor_radius=r, location=loc)
    ob = bpy.context.object
    ob.name = name
    ob.color = rgba(color)
    return ob

def text3d(body, loc=(0, 0, 0), size=1.0, name="TXT", color="white", rot=(math.radians(65), 0, 0)):
    cd = bpy.data.curves.new(name + "_c", type='FONT')
    cd.body = body
    cd.size = size
    cd.align_x = 'CENTER'
    cd.align_y = 'CENTER'
    ob = bpy.data.objects.new(name, cd)
    bpy.context.collection.objects.link(ob)
    ob.location = loc
    ob.rotation_euler = rot
    ob.color = rgba(color)
    ob['text_body'] = body  # validation reads this
    return ob

def chip(loc, name="Chip", color="cyan", s=(1.6, 1.6, 0.5)):
    # loc: plain 3-tuple (proven fix — no Vector math here)
    bpy.ops.mesh.primitive_cube_add(location=loc)
    ob = bpy.context.object
    ob.name = name
    ob.scale = (s[0] / 2, s[1] / 2, s[2] / 2)
    ob.color = rgba(color)
    return ob

def sticky_note(loc, body, name="Note", color="yellow", size=1.2):
    n = box(loc, (size, size, 0.12), name, color)
    t = text3d(body, (loc[0], loc[1] - size / 2 - 0.35, loc[2] + 0.08), size * 0.34,
               name + "_t", "bg")
    return n, t

def crate(loc=(0, 0, 0), s=1.2, name="Crate", color="deep"):
    return box(loc, (s, s, s), name, color)

# ---------- animation helpers ----------
def _key(ob, prop, frame, **kw):
    for k, v in kw.items():
        ob[prop].keyframe_insert(k, frame=frame) if False else None
def kf_loc(ob, f, loc, ease="SINE", inp="AUTO"):
    ob.location = loc
    ob.keyframe_insert(data_path="location", frame=f)
def kf_scale(ob, f, s):
    ob.scale = s if hasattr(s, "__len__") else (s, s, s)
    ob.keyframe_insert(data_path="scale", frame=f)
def kf_rot(ob, f, rot):
    ob.rotation_euler = rot
    ob.keyframe_insert(data_path="rotation_euler", frame=f)
def move(ob, f0, f1, a, b):
    kf_loc(ob, f0, a)
    kf_loc(ob, f1, b)
def rise(ob, f0, f1, dz=2.0):
    a = tuple(ob.location)
    b = (a[0], a[1], a[2] + dz)
    move(ob, f0, f1, a, b)
def scale_in(ob, f0, f1, target=None):
    t = target if target else tuple(ob.scale)
    ob.scale = (0.001, 0.001, 0.001)
    ob.keyframe_insert(data_path="scale", frame=f0)
    ob.scale = t
    ob.keyframe_insert(data_path="scale", frame=f1)
def spin(ob, f0, f1, turns=1.0, axis="Z"):
    a = tuple(ob.rotation_euler)
    idx = {"X": 0, "Y": 1, "Z": 2}[axis]
    b = list(a)
    b[idx] += turns * 2 * math.pi
    kf_rot(ob, f0, a)
    kf_rot(ob, f1, b)

# ---------- camera ----------
def look_at(ob, target):
    d = Vector(target) - ob.location
    q = d.to_track_quat('-Z', 'Y')  # matrix-safe (proven)
    ob.rotation_euler = q.to_euler()

def orbit_pos(ang, r, z):
    return (r * math.sin(ang), -r * math.cos(ang), z)

def shot(cam, f0, f1, p0, p1, t0=None, t1=None):
    kf_loc(cam, f0, p0)
    kf_loc(cam, f1, p1)

# ---------- audio ----------
def add_audio(wav_path, total_frames):
    sc = bpy.context.scene
    if not sc.sequence_editor:
        sc.sequence_editor_create()
    se = sc.sequence_editor
    strip = se.sequences.new_sound("narr", wav_path, 1, 1)
    strip.volume = 1.0
    return strip
