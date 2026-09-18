"""Common Blender building helpers for the AGI explainer.

Rendering engine: BLENDER_WORKBENCH (software GL constraint).
Material system: per-object/material diffuse colors (Workbench color type 'MATERIAL'),
form depth via cavity + shadows + outline.

Stage system:
  Each SHOT gets its own stage collection placed at X = stage_index * STAGE_GAP.
  Assets are built once into a hidden LIBRARY collection and linked-copied per stage
  (linked duplicates share mesh data -> cheap). Only the active shot's stage is
  render-visible (hide_render keyframed for every object at build time).
"""
import bpy
import math
from mathutils import Vector, Euler, Matrix

FPS = 30
STAGE_GAP = 1000.0
LIB_COL_NAME = "LIBRARY"


# ---------------------------------------------------------------- collections
def col(name, parent=None):
    c = bpy.data.collections.get(name)
    if c is None:
        c = bpy.data.collections.new(name)
        bpy.context.scene.collection.children.link(c)
    if parent is not None:
        try:
            parent.children.link(c)
        except RuntimeError:
            pass
    return c


def unlink_from_scene_collection(ob):
    for c in list(ob.users_collection):
        c.objects.unlink(ob)


def parent_to(ob, P, keep_world=True):
    """Parent ob to P while keeping its authored world position.
    Requires view_layer update so P.matrix_world is current."""
    if keep_world:
        bpy.context.view_layer.update()
        inv = P.matrix_world.inverted()
        ob.parent = P
        ob.matrix_parent_inverse = inv
    else:
        ob.parent = P
    return ob


def link_to(ob, collection):
    unlink_from_scene_collection(ob)
    collection.objects.link(ob)


def get_library():
    return col(LIB_COL_NAME)


# ---------------------------------------------------------------- materials
_mat_cache = {}


def mat(name, rgba, spec=0.25, rough=0.6):
    """Workbench-visible material: sets material diffuse_color + spec color."""
    if name in _mat_cache:
        return _mat_cache[name]
    m = bpy.data.materials.get(name)
    if m is None:
        m = bpy.data.materials.new(name)
    m.diffuse_color = rgba
    m.metallic = 0.0
    m.roughness = rough
    try:
        m.specular_intensity = spec
    except AttributeError:
        pass
    _mat_cache[name] = m
    return m


def apply_mat(ob, m):
    ob.data.materials.clear()
    ob.data.materials.append(m)


def ob_color(ob, rgba):
    ob.color = rgba


# ---------------------------------------------------------------- primitives
def box(name, size, loc=(0, 0, 0), rot=None, m=None, bevel=0.0, col_target=None):
    """size=(x,y,z) full dimensions. Scale is baked into the MESH (object scale stays
    1,1,1) so that children parented to this object are not distorted by parent scale."""
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    ob = bpy.context.object
    ob.name = name
    ob.data.transform(Matrix.Diagonal((size[0], size[1], size[2], 1.0)))
    if rot:
        ob.rotation_euler = rot
    if bevel > 0:
        bev = ob.modifiers.new("bev", "BEVEL")
        bev.width = min(bevel, 0.35 * min(size))
        bev.segments = 3
        bev.limit_method = "ANGLE"
    if m is not None:
        apply_mat(ob, m)
        ob_color(ob, m.diffuse_color)
    if col_target is not None:
        link_to(ob, col_target)
    return ob


def cyl(name, r, depth, loc=(0, 0, 0), rot=None, m=None, verts=24, col_target=None):
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=depth, vertices=verts, location=loc)
    ob = bpy.context.object
    ob.name = name
    if rot:
        ob.rotation_euler = rot
    if m is not None:
        apply_mat(ob, m)
        ob_color(ob, m.diffuse_color)
    if col_target is not None:
        link_to(ob, col_target)
    return ob


def sphere(name, r, loc=(0, 0, 0), m=None, segs=24, rings=16, col_target=None, scale=None):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r, segments=segs, ring_count=rings, location=loc)
    ob = bpy.context.object
    ob.name = name
    if scale is not None:
        ob.data.transform(Matrix.Diagonal((scale[0], scale[1], scale[2], 1.0)))
    bpy.ops.object.shade_smooth()
    if m is not None:
        apply_mat(ob, m)
        ob_color(ob, m.diffuse_color)
    if col_target is not None:
        link_to(ob, col_target)
    return ob


def cone(name, r1, r2, depth, loc=(0, 0, 0), rot=None, m=None, verts=24, col_target=None):
    bpy.ops.mesh.primitive_cone_add(radius1=r1, radius2=r2, depth=depth, vertices=verts, location=loc)
    ob = bpy.context.object
    ob.name = name
    if rot:
        ob.rotation_euler = rot
    if m is not None:
        apply_mat(ob, m)
        ob_color(ob, m.diffuse_color)
    if col_target is not None:
        link_to(ob, col_target)
    return ob


def torus(name, major, minor, loc=(0, 0, 0), rot=None, m=None, col_target=None):
    bpy.ops.mesh.primitive_torus_add(major_radius=major, minor_radius=minor, location=loc)
    ob = bpy.context.object
    ob.name = name
    if rot:
        ob.rotation_euler = rot
    if m is not None:
        apply_mat(ob, m)
        ob_color(ob, m.diffuse_color)
    if col_target is not None:
        link_to(ob, col_target)
    return ob


def text3d(name, body, size, loc=(0, 0, 0), rot=None, m=None, align="CENTER", col_target=None,
           extrude=0.0, bold=False):
    fc = bpy.data.curves.new(name, type="FONT")
    fc.body = body
    fc.size = size
    fc.align_x = align
    fc.align_y = "CENTER"
    fc.extrude = extrude
    if bold:
        fc.offset = size * 0.03
    ob = bpy.data.objects.new(name, fc)
    ob.location = loc
    if rot:
        ob.rotation_euler = rot
    (col_target or bpy.context.scene.collection).objects.link(ob)
    if m is not None:
        fc.materials.append(m)
        ob.color = m.diffuse_color
    return ob


def join_objects(objs, name):
    """Join list of objects into one mesh (keeps first object's transform)."""
    if not objs:
        return None
    bpy.ops.object.select_all(action="DESELECT")
    for o in objs:
        o.select_set(True)
    bpy.context.view_layer.objects.active = objs[0]
    bpy.ops.object.join()
    ob = bpy.context.object
    ob.name = name
    return ob


# ---------------------------------------------------------------- stage system
def new_stage(idx, shot_id):
    """Create stage collection at X offset. Returns (collection, offset)."""
    c = col("STAGE_%s" % shot_id)
    off = idx * STAGE_GAP
    return c, off


def stage_copy(src_ob, stage, offset, name=None, loc=None, rot=None, scale=None,
               collection=None):
    """Linked duplicate into stage at world offset (library asset at origin)."""
    dup = src_ob.copy()  # linked mesh data
    stage_or_col = collection or stage
    stage_or_col.objects.link(dup)
    dup.name = name or (src_ob.name + "_c")
    base = Vector(src_ob.location)
    dup.location = base + Vector(offset) if loc is None else Vector(loc) + Vector(offset)
    if rot is not None:
        dup.rotation_euler = Euler(rot)
    else:
        dup.rotation_euler = src_ob.rotation_euler.copy()
    if scale is not None:
        dup.scale = scale if hasattr(scale, "__len__") else (scale, scale, scale)
    return dup


def copy_hierarchy(root, stage, offset, collection=None):
    """Copy an asset subtree (root + all descendants), preserving parenting."""
    c = collection or stage

    def rec(src, parent_dup):
        dup = src.copy()
        c.objects.link(dup)
        dup.parent = parent_dup
        if parent_dup is not None:
            dup.matrix_parent_inverse = src.matrix_parent_inverse.copy()
            dup.location = src.location
            dup.rotation_euler = src.rotation_euler.copy()
            dup.scale = src.scale.copy()
        else:
            dup.location = Vector(src.location) + Vector(offset)
        for ch in src.children:
            rec(ch, dup)
        return dup

    return rec(root, None)


# ---------------------------------------------------------------- keyframes
def kfv(ob, path, frame, vec):
    """Set vector property then keyframe whole path (location/rotation_euler/scale)."""
    setattr(ob, path, vec)
    ob.keyframe_insert(data_path=path, frame=frame)


def kf_scalar(ob, path, frame, value):
    setattr(ob, path, value)
    ob.keyframe_insert(data_path=path, frame=frame)


def kf_color(ob, frame, rgba):
    ob.color = rgba
    ob.keyframe_insert(data_path="color", frame=frame)


def kf_vis(objs, f_in, f_out):
    """Keyframe hide_render/hide_viewport so objs visible only in [f_in, f_out]."""
    f0 = max(1, int(f_in) - 1)
    f1 = int(f_out) + 1
    for ob in objs:
        for fr in (1, f0, f_in, f_out, f1):
            if f_in <= fr <= f_out:
                ob.hide_render = False
                ob.hide_viewport = False
            else:
                ob.hide_render = True
                ob.hide_viewport = True
            ob.keyframe_insert(data_path="hide_render", frame=fr)
            ob.keyframe_insert(data_path="hide_viewport", frame=fr)


def smooth(t):
    return t * t * (3 - 2 * t)


def easeout(t):
    return 1 - (1 - t) ** 3


def easein(t):
    return t ** 3


def lerp_v(v0, v1, t):
    return Vector(v0).lerp(Vector(v1), t)


# ---------------------------------------------------------------- camera & lights
def make_camera(name, loc, look_at, lens=40, stage_off=(0, 0, 0)):
    cd = bpy.data.cameras.new(name)
    cd.lens = lens
    cd.clip_start = 0.05
    cd.clip_end = 1500
    ob = bpy.data.objects.new(name, cd)
    bpy.context.scene.collection.objects.link(ob)
    place_camera(ob, loc, look_at, stage_off)
    return ob


def place_camera(ob, loc, look_at, stage_off=(0, 0, 0)):
    tgt = Vector(look_at) + Vector(stage_off)
    ob.location = Vector(loc) + Vector(stage_off)
    d = tgt - ob.location
    ob.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()


def scene_lights(key_loc, key_energy=3.0, fill_loc=None, fill_energy=0.8, stage_off=(0, 0, 0),
                 key_size=6.0, col_target=None, name="L"):
    """Area key + area fill (Workbench SCENE light mode)."""
    out = {}
    kd = bpy.data.lights.new(name + "_key", type="AREA")
    kd.energy = key_energy * 100
    kd.size = key_size
    key = bpy.data.objects.new(name + "_key", kd)
    (col_target or bpy.context.scene.collection).objects.link(key)
    key.location = Vector(key_loc) + Vector(stage_off)
    out["key"] = key
    if fill_loc is not None:
        fd = bpy.data.lights.new(name + "_fill", type="AREA")
        fd.energy = fill_energy * 100
        fd.size = key_size * 1.4
        fill = bpy.data.objects.new(name + "_fill", fd)
        (col_target or bpy.context.scene.collection).objects.link(fill)
        fill.location = Vector(fill_loc) + Vector(stage_off)
        out["fill"] = fill
    return out


def aim_light(ob, look_at, stage_off=(0, 0, 0)):
    tgt = Vector(look_at) + Vector(stage_off)
    d = tgt - ob.location
    ob.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()


def setup_workbench_scene():
    sc = bpy.context.scene
    sc.render.engine = "BLENDER_WORKBENCH"
    sh = sc.display.shading
    sh.light = "STUDIO"
    if hasattr(sh, "use_scene_lights"):
        sh.use_scene_lights = True
    if hasattr(sh, "use_scene_world"):
        sh.use_scene_world = False
    sh.show_shadows = True
    sh.shadow_intensity = 0.35
    sh.show_cavity = True
    sh.cavity_type = "WORLD"
    if hasattr(sh, "background_type"):
        sh.background_type = "VIEWPORT"
        sh.background_color = (0.93, 0.94, 0.96)
    sh.show_object_outline = True
    sh.color_type = "MATERIAL"
    sc.render.resolution_x = 1280
    sc.render.resolution_y = 720
    sc.render.fps = FPS
    sc.frame_start = 1
    sc.view_settings.view_transform = "Standard"
    return sc


def clear_default_scene():
    for ob in list(bpy.data.objects):
        bpy.data.objects.remove(ob, do_unlink=True)


def ground(name, size_x=60, size_y=60, loc=(0, 0, 0), m=None, col_target=None):
    return box(name, (size_x, size_y, 0.2), loc=(loc[0], loc[1], loc[2] - 0.1), m=m,
               col_target=col_target)
