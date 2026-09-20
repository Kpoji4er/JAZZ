"""Build the JazzHat_SSh68 character element source scene (headless Blender).

Reads the official JA3 sample appearance scene, replaces its sample clothing with a
procedural SSh-68 helmet fitted to the male skull and saves a self-contained source
.blend plus placeholder textures.

CharacterHat is a rigid attach, not skinned clothing. AppearancePreset.HatSpot
defaults to Head, so the exporter origin must sit on the Head bone and the mesh
must be in that bone's local space. Inheriting Male animations plus world-space
verts at skull height stacks the Head offset twice and floats the helmet.

Usage:
    blender -b <SampleMaleModel>.blend -P build_sh68_helmet.py -- --out <source_dir>
"""
import argparse
import math
import os
import random
import sys

import bmesh
import bpy
from mathutils import Vector

ENTITY = "JazzHat_SSh68"
MESH_NAME = "mesh"
STATE = "idle"
HEAD_BONE = "Bip001 Head"
REAR_DROP = 0.35
SAMPLE_CLOTHING = (
    "top_suit", "top_suit_LOD1", "top_hands", "top_hands_LOD1",
    "bottom_pants.001", "bottom_pants_LOD1.001", "Origin_bottom",
)
TEX_SIZE = 512


def parse_args():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", required=True, help="source directory for .blend and textures")
    return parser.parse_args(argv)


def find_objects():
    armature = bpy.data.objects.get("Bip001")
    origin = bpy.data.objects.get("Origin_top")
    body = bpy.data.objects.get("M_BaseMesh Skin_BIP")
    missing = [n for n, o in (("Bip001", armature), ("Origin_top", origin), ("body", body)) if not o]
    if missing:
        raise SystemExit(f"sample scene is missing: {', '.join(missing)}")
    return armature, origin, body


def drop_sample_clothing():
    for name in SAMPLE_CLOTHING:
        obj = bpy.data.objects.get(name)
        if obj:
            bpy.data.objects.remove(obj, do_unlink=True)
    reference = bpy.data.objects.get("M_BaseMesh Skin_BIP.001")
    if reference:
        bpy.data.objects.remove(reference, do_unlink=True)


def head_metrics(body):
    """World-space measurements of the skull cap the helmet has to sit on.

    Head-bone weights reach down to the jaw, so the cross-section is taken above the
    ear line only; otherwise the helmet inherits the width of the neck.
    """
    group = body.vertex_groups.get(HEAD_BONE)
    if not group:
        raise SystemExit(f"base body has no vertex group {HEAD_BONE!r}")
    matrix = body.matrix_world
    points = []
    for vert in body.data.vertices:
        for item in vert.groups:
            if item.group == group.index and item.weight > 0.5:
                points.append(matrix @ vert.co)
                break
    if not points:
        raise SystemExit("no vertices are weighted to the head bone")
    z_lo = min(p.z for p in points)
    z_hi = max(p.z for p in points)
    ear_line = z_lo + (z_hi - z_lo) * 0.55
    skull = [p for p in points if p.z >= ear_line]
    lo = Vector((min(p.x for p in skull), min(p.y for p in skull), ear_line))
    hi = Vector((max(p.x for p in skull), max(p.y for p in skull), z_hi))
    return lo, hi


def helmet_profile():
    """(radius factor, height factor, rear drop) from crown to rim.

    SSh-68: a shell that stays close to the skull down to the brow line, then turns
    into a short outward flare. Exponents below 1 bulge the mid elevations so the
    occiput does not poke through the ellipsoid.
    """
    dome = []
    steps = 9
    for i in range(steps + 1):
        angle = (math.pi / 2.0) * (i / steps)
        dome.append((math.sin(angle) ** 0.82 * 1.02, math.cos(angle) ** 1.15, 0.0))
    skirt = [
        (1.05, 0.06, 0.6),
        (1.11, 0.03, 1.0),
        (1.18, 0.00, 1.0),
    ]
    return dome + skirt


def build_helmet_mesh(center, radius_x, radius_y, height):
    segments = 28
    profile = helmet_profile()
    mesh = bpy.data.meshes.new(f"{ENTITY}_mesh")
    bm = bmesh.new()
    uv_layer = bm.loops.layers.uv.new("UVChannel_1")

    rings = []
    for r_factor, z_factor, rear_drop in profile:
        ring = []
        for s in range(segments):
            theta = 2.0 * math.pi * s / segments
            # Exporter axis_forward=Y: +Y is the face. SSh-68 brim hangs at the occiput (-Y).
            rear = (0.5 - 0.5 * math.sin(theta)) * rear_drop * REAR_DROP
            x = math.cos(theta) * r_factor * radius_x
            y = math.sin(theta) * r_factor * radius_y
            z = (z_factor - rear) * height
            ring.append(bm.verts.new(center + Vector((x, y, z))))
        rings.append(ring)
    bm.verts.ensure_lookup_table()

    apex = bm.verts.new(center + Vector((0.0, 0.0, profile[0][1] * height)))
    for s in range(segments):
        nxt = (s + 1) % segments
        bm.faces.new((apex, rings[0][nxt], rings[0][s]))
    for i in range(len(rings) - 1):
        for s in range(segments):
            nxt = (s + 1) % segments
            bm.faces.new((rings[i][s], rings[i][nxt], rings[i + 1][nxt], rings[i + 1][s]))

    total = len(rings)
    for face in bm.faces:
        for loop in face.loops:
            co = loop.vert.co - center
            u = (math.atan2(co.y, co.x) / (2.0 * math.pi)) % 1.0
            v = 1.0 - (co.z / height * 0.5 + 0.5)
            loop[uv_layer].uv = (u, max(0.0, min(1.0, v)))

    bmesh.ops.solidify(bm, geom=bm.faces[:], thickness=-radius_x * 0.045)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(mesh)
    bm.free()

    for poly in mesh.polygons:
        poly.use_smooth = True
    obj = bpy.data.objects.new(ENTITY, mesh)
    bpy.context.scene.collection.objects.link(obj)
    for collection in bpy.data.collections:
        if collection.name.endswith("_EXPORT"):
            collection.objects.link(obj)
            bpy.context.scene.collection.objects.unlink(obj)
            break
    return obj


def make_head_origin(armature):
    """Unparented empty at the Head bone. CharacterHat attaches to the Head spot, so
    this empty becomes the entity origin; world-space skull verts then become
    Head-local after parenting with keep-transform.
    """
    rest = armature.data.bones.get(HEAD_BONE)
    if not rest:
        raise SystemExit(f"armature has no bone {HEAD_BONE!r}")
    empty = bpy.data.objects.new("Origin_hat", None)
    empty.empty_display_type = "PLAIN_AXES"
    bpy.context.scene.collection.objects.link(empty)
    # Head spot on the unit is world-aligned (hats stay upright). Copy location
    # only: bone axes would map the dome onto world X and lay the helmet on its side.
    empty.location = armature.matrix_world @ rest.head_local
    bpy.context.view_layer.update()
    print(f"[JAZZ] Head origin loc={tuple(round(v, 4) for v in empty.location)} world={tuple(round(v, 4) for v in empty.matrix_world.translation)}")
    return empty


def make_texture(out_dir, suffix, rgb, jitter, size=TEX_SIZE):
    path = os.path.join(out_dir, f"{ENTITY}_{suffix}.tga")
    image = bpy.data.images.new(f"{ENTITY}_{suffix}", width=size, height=size, alpha=False)
    rng = random.Random(6819)
    pixels = [0.0] * (size * size * 4)
    for i in range(size * size):
        noise = (rng.random() - 0.5) * jitter
        pixels[i * 4 + 0] = max(0.0, min(1.0, rgb[0] + noise))
        pixels[i * 4 + 1] = max(0.0, min(1.0, rgb[1] + noise))
        pixels[i * 4 + 2] = max(0.0, min(1.0, rgb[2] + noise))
        pixels[i * 4 + 3] = 1.0
    image.pixels.foreach_set(pixels)
    image.filepath_raw = path
    image.file_format = "TARGA"
    image.save()
    return image


def build_material(helmet, out_dir):
    material = bpy.data.materials.new(name=f"{ENTITY}_mtl")
    material.use_nodes = True
    helmet.data.materials.append(material)
    settings = material.hgm_settings
    settings.base_color = make_texture(out_dir, "Base", (0.196, 0.208, 0.145), 0.03)
    # A flat normal map larger than 4x4 makes AssetsProcessor warn about wasted space.
    settings.normal_map = make_texture(out_dir, "Norm", (0.5, 0.5, 1.0), 0.0, size=4)
    settings.roughness_metallic_map = make_texture(out_dir, "RM", (0.72, 0.0, 0.08), 0.05)
    settings.cast_shadows = True
    settings.receive_shadows = True
    return material


def apply_hge_settings(helmet):
    helmet.hge_export = True
    settings = helmet.hge_obj_settings
    settings.entity = ENTITY
    settings.mesh = MESH_NAME
    settings.state = STATE
    settings.lod = 1
    settings.lod_distance = 0
    settings.inherit_animation = "None"
    errors = settings.get_errors()
    if errors:
        raise SystemExit(f"HGE validation failed: {errors}")
    print(f"[JAZZ] hge name: {settings.get_hge_name()}")


def main():
    args = parse_args()
    out_dir = os.path.abspath(args.out)
    os.makedirs(out_dir, exist_ok=True)

    armature, origin, body = find_objects()
    lo, hi = head_metrics(body)
    print(f"[JAZZ] skull bbox min={tuple(round(v, 3) for v in lo)} max={tuple(round(v, 3) for v in hi)}")
    # The shell is worn over a liner, so it clears the skull by about a centimetre.
    clearance = 0.010
    radius_x = (hi.x - lo.x) / 2.0 * 1.08
    radius_y = (hi.y - lo.y) / 2.0 * 1.08
    height = (hi.z - lo.z) + clearance
    center = Vector(((lo.x + hi.x) / 2.0, (lo.y + hi.y) / 2.0, lo.z))
    print(f"[JAZZ] helmet rx={radius_x:.3f} ry={radius_y:.3f} h={height:.3f} center={tuple(round(v, 3) for v in center)}")

    drop_sample_clothing()
    feet_origin = bpy.data.objects.get("Origin_top")
    if feet_origin:
        feet_origin.hge_obj_settings.ignore = True
    origin = make_head_origin(armature)
    helmet = build_helmet_mesh(center, radius_x, radius_y, height)
    helmet.parent = origin
    helmet.matrix_parent_inverse = origin.matrix_world.inverted()
    build_material(helmet, out_dir)
    apply_hge_settings(helmet)

    blend_path = os.path.join(out_dir, f"{ENTITY}.blend")
    bpy.ops.wm.save_as_mainfile(filepath=blend_path, relative_remap=True)
    print(f"[JAZZ] verts={len(helmet.data.vertices)} polys={len(helmet.data.polygons)}")
    print(f"[JAZZ] saved {blend_path}")


main()
