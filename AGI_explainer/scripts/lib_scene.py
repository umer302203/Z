"""lib_scene.py — v3 shared scene library (recreated after reset #3).
Workbench 1280x720 @ 24fps, OBJECT colors, proven fixes baked in:
world.color RGBA-tolerant, chip takes 3-tuple loc, matrix-safe look_at.
TEXT RULE: every on-screen string <= 3 English words + symbols."""
import math
import bpy
from mathutils import Vector

FPS = 24
RES_X, RES_Y = 1280, 720
LENS = 44

def hx(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4)) + (1.0,)

PAL = dict(
    bg=hx('0d1321'), ground=hx('1b2436'), ink=hx('eaf1fb'),
    accent=hx('ffb347'), cyan=hx('4fc3f7'), green=hx('66bb6a'),
    red=hx('ef5350'), purple=hx('ab7df6'), grey=hx('8a97a8'),
    teal=hx('26a69a'), amber=hx('ffca28'), blue=hx('42a5f5'),
)
C_BG = PAL['bg'];      C_GROUND = PAL['ground']; C_INK = PAL['ink']
C_ACCENT = PAL['accent']; C_CYAN = PAL['cyan'];   C_GREEN = PAL['green']
C_RED = PAL['red'];    C_PURPLE = PAL['purple']; C_GREY = PAL['grey']
C_TEAL = PAL['teal'];  C_AMBER = PAL['amber'];   C_BLUE = PAL['blue']

def _link(ob):
    bpy.context.scene.collection.objects.link(ob)
    return ob

def scene_setup(total_frames):
    sc = bpy.context.scene
    sc.render.engine = 'BLENDER_WORKBENCH'
    sc.display.render_aa = '5'
    sh = sc.display.shading
    sh.light = 'STUDIO'
    sh.color_type = 'OBJECT'
    sh.show_shadows = True
    sh.show_cavity = True
    sh.background_type = 'WORLD'
    w = bpy.data.worlds.new('World')
    sc.world = w
    try:
        w.color = C_BG            # RGBA accepted in 4.x
    except (TypeError, ValueError):
        w.color = C_BG[:3]        # RGB fallback (proven fix)
    sc.render.resolution_x = RES_X
    sc.render.resolution_y = RES_Y
    sc.render.fps = FPS
    sc.frame_start = 1
    sc.frame_end = total_frames
    sc.render.image_settings.file_format = 'JPEG'
    sc.render.image_settings.quality = 92
    bpy.ops.mesh.primitive_plane_add(size=500, location=(0, 0, 0))
    g = bpy.context.active_object
    g.name = 'GROUND'
    g.color = C_GROUND
    return sc

def cam_make():
    cd = bpy.data.cameras.new('Cam')
    cd.lens = LENS
    cd.clip_end = 3000
    cam = _link(bpy.data.objects.new('Cam', cd))
    cam.rotation_mode = 'QUATERNION'   # slerp between shots — no euler flips
    bpy.context.scene.camera = cam
    return cam

# ---------- primitive builders (color set, linked) ----------
def box(name, loc, size, color, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc, rotation=rot)
    ob = bpy.context.active_object
    ob.name = name
    ob.scale = size
    ob.color = color
    return ob

def sphere(name, loc, r, color, seg=24):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r, segments=seg,
                                         ring_count=max(8, seg // 2),
                                         location=loc)
    ob = bpy.context.active_object
    ob.name = name
    ob.color = color
    return ob

def cyl(name, loc, r, depth, color, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=depth,
                                        location=loc, rotation=rot)
    ob = bpy.context.active_object
    ob.name = name
    ob.color = color
    return ob

def torus(name, loc, R, r, color, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_torus_add(major_radius=R, minor_radius=r,
                                     location=loc, rotation=rot)
    ob = bpy.context.active_object
    ob.name = name
    ob.color = color
    return ob

def text3d(name, body, loc, size=1.0, color=C_INK,
           rot=(math.radians(90), 0, 0)):
    cu = bpy.data.curves.new(name, type='FONT')
    cu.body = body
    cu.align_x = 'CENTER'
    cu.align_y = 'CENTER'
    cu.size = size
    cu.extrude = 0.02
    cu.fill_mode = 'BOTH'
    ob = _link(bpy.data.objects.new(name, cu))
    ob.location = loc
    ob.rotation_euler = rot
    ob.color = color
    ob['text_body'] = body
    return ob

def chip(name, txt, loc, color):
    """colored slab + word; loc is a plain (x, y, z) 3-tuple (proven fix)."""
    b = box(name + '_slab', loc, (2.6, 0.25, 0.9), color)
    t = text3d(name + '_txt', txt, (loc[0], loc[1] - 0.2, loc[2]),
               size=0.42, color=C_BG)
    return b, t

def sticky_note(name, txt, loc, color, size=1.4):
    b = box(name + '_pad', loc, (size, size * 0.75, 0.08), color,
            rot=(0, 0, math.radians(-4)))
    t = text3d(name + '_txt', txt, (loc[0], loc[1] - 0.05, loc[2] + 0.08),
               size=size * 0.22, color=C_BG)
    return b, t

def crate(name, loc, s, color):
    b = box(name, loc, (s, s, s), color)
    lid = box(name + '_lid', (loc[0], loc[1], loc[2] + s / 2 + 0.05),
              (s * 1.06, s * 1.06, 0.1), C_BG)
    return b, lid

# ---------- animation helpers ----------
def kf_loc(ob, f, p):
    ob.location = Vector(p)
    ob.keyframe_insert('location', frame=f)

def kf_scale(ob, f, s):
    ob.scale = s if hasattr(s, '__len__') else (s, s, s)
    ob.keyframe_insert('scale', frame=f)

def kf_rot(ob, f, r):
    ob.rotation_euler = r
    ob.keyframe_insert('rotation_euler', frame=f)

def move(ob, f0, f1, p1):
    kf_loc(ob, f0, ob.location.copy())
    kf_loc(ob, f1, p1)

def rise(ob, f0, f1, h):
    p = ob.location.copy()
    kf_loc(ob, f0, p)
    kf_loc(ob, f1, (p.x, p.y, p.z + h))

def scale_in(ob, f0, f1):
    kf_scale(ob, f0, 0.001)
    kf_scale(ob, f1, ob.scale.copy())

def spin(ob, f0, f1, turns=1.0, axis='Z'):
    r0 = ob.rotation_euler.copy()
    idx = {'X': 0, 'Y': 1, 'Z': 2}[axis]
    r1 = r0.copy()
    r1[idx] += math.radians(360.0 * turns)
    kf_rot(ob, f0, r0)
    kf_rot(ob, f1, r1)

# ---------- camera ----------
def look_at(ob, target):
    d = Vector(target) - ob.location
    if d.length < 1e-6:
        return
    q = d.to_track_quat('-Z', 'Y')
    ob.rotation_quaternion = q          # authoritative when mode=QUATERNION
    ob.rotation_euler = q.to_euler()    # keep euler channel in sync

def shot(cam, f0, f1, p0, p1, t0, t1):
    """one contiguous camera move; quaternion slerp between ends."""
    cam.location = Vector(p0)
    look_at(cam, t0)
    q0 = cam.rotation_quaternion.copy()
    cam.location = Vector(p1)
    look_at(cam, t1)
    q1 = cam.rotation_quaternion.copy()
    cam.location = Vector(p0)
    cam.rotation_quaternion = q0
    cam.keyframe_insert('location', frame=f0)
    cam.keyframe_insert('rotation_quaternion', frame=f0)
    cam.location = Vector(p1)
    cam.rotation_quaternion = q1
    cam.keyframe_insert('location', frame=f1)
    cam.keyframe_insert('rotation_quaternion', frame=f1)

def orbit_pos(ang, r, z):
    return (math.sin(ang) * r, math.cos(ang) * r, z)
