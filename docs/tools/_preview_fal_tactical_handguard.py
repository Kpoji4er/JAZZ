"""Overlay vanilla FAL handguard vs reseated RIS. Does not write entities.

  blender --background --factory-startup --python docs/tools/_preview_fal_tactical_handguard.py -- \
      --source <tactical extract> --vanilla <_vanilla_reference/OBJ> --output <png dir>
"""
import argparse
import math
import sys
from pathlib import Path

import bpy
from mathutils import Matrix, Vector

CM_TO_M = 0.01


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument('--source', type=Path, required=True)
    p.add_argument('--vanilla', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    argv = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
    return p.parse_args(argv)


def import_obj(path, name, forward, up):
    before = {o.name for o in bpy.data.objects}
    bpy.ops.wm.obj_import(filepath=str(path), forward_axis=forward, up_axis=up)
    new = [o for o in bpy.data.objects if o.name not in before and o.type == 'MESH']
    new.sort(key=lambda o: -len(o.data.vertices))
    bpy.ops.object.select_all(action='DESELECT')
    for o in new:
        o.select_set(True)
    bpy.context.view_layer.objects.active = new[0]
    if len(new) > 1:
        bpy.ops.object.join()
    obj = bpy.context.view_layer.objects.active
    obj.name = name
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    return obj


def face_centroid(obj, which='min', depth=0.015):
    verts = [obj.matrix_world @ v.co for v in obj.data.vertices]
    if which == 'max':
        y1 = max(v.y for v in verts)
        sel = [v for v in verts if v.y >= y1 - depth]
        y = y1
    else:
        y0 = min(v.y for v in verts)
        sel = [v for v in verts if v.y <= y0 + depth]
        y = y0
    n = float(len(sel))
    return Vector((sum(v.x for v in sel) / n, y, sum(v.z for v in sel) / n))


def paint(obj, color):
    mat = bpy.data.materials.new(obj.name + '_mat')
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes['Principled BSDF']
    bsdf.inputs['Base Color'].default_value = color
    bsdf.inputs['Roughness'].default_value = 0.45
    obj.data.materials.clear()
    obj.data.materials.append(mat)


def bbox(obj):
    pts = [obj.matrix_world @ Vector(c) for c in obj.bound_box]
    mn = Vector((min(p.x for p in pts), min(p.y for p in pts), min(p.z for p in pts)))
    mx = Vector((max(p.x for p in pts), max(p.y for p in pts), max(p.z for p in pts)))
    return mn, mx


def shoot(path, objs, name):
    mn = Vector((min(bbox(o)[0][i] for o in objs) for i in range(3)))
    mx = Vector((max(bbox(o)[1][i] for o in objs) for i in range(3)))
    center = (mn + mx) / 2
    size = (mx - mn).length
    cam = bpy.data.objects.new(name, bpy.data.cameras.new(name))
    bpy.context.collection.objects.link(cam)
    bpy.context.scene.camera = cam
    cam.location = center + Vector((size * 0.15, -size * 1.4, size * 0.35))
    direction = center - cam.location
    cam.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()
    sun = bpy.data.objects.new(name + '_sun', bpy.data.lights.new(name + '_sun', 'SUN'))
    sun.data.energy = 4
    sun.rotation_euler = (math.radians(50), 0, math.radians(30))
    bpy.context.collection.objects.link(sun)
    scene = bpy.context.scene
    scene.render.engine = 'BLENDER_EEVEE_NEXT'
    scene.render.resolution_x = 1280
    scene.render.resolution_y = 720
    scene.render.filepath = str(path)
    scene.render.image_settings.file_format = 'PNG'
    bpy.ops.render.render(write_still=True)
    bpy.data.objects.remove(cam, do_unlink=True)
    bpy.data.objects.remove(sun, do_unlink=True)


def seat_delta(vanilla, donor, which):
    if which == 'max':
        van_r, don_r = face_centroid(vanilla, 'max'), face_centroid(donor, 'max')
        van_m, don_m = face_centroid(vanilla, 'min'), face_centroid(donor, 'min')
        return Vector((van_m.x - don_m.x, van_r.y - don_r.y, van_m.z - don_m.z))
    return face_centroid(vanilla, which) - face_centroid(donor, which)


def seat_copy(donor, vanilla, which):
    copy = donor.copy()
    copy.data = donor.data.copy()
    copy.name = donor.name + '_' + which
    bpy.context.collection.objects.link(copy)
    delta = seat_delta(vanilla, copy, which)
    copy.data.transform(Matrix.Translation(delta))
    copy.data.update()
    return copy, delta


def main():
    args = parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    bpy.ops.wm.read_factory_settings(use_empty=True)
    world = bpy.data.worlds.new('world')
    world.use_nodes = True
    world.node_tree.nodes['Background'].inputs[0].default_value = (0.82, 0.82, 0.80, 1)
    bpy.context.scene.world = world

    vanilla = import_obj(args.vanilla / 'WeaponAttA_HandguardFNFal_01_mesh.obj', 'van', 'Y', 'Z')
    donor = import_obj(args.source / 'model_2.obj', 'donor', 'NEGATIVE_Z', 'Y')
    donor.data.transform(Matrix.Scale(CM_TO_M, 4))
    donor.data.update()

    old, d_old = seat_copy(donor, vanilla, 'min')
    new, d_new = seat_copy(donor, vanilla, 'max')
    bpy.data.objects.remove(donor, do_unlink=True)

    paint(vanilla, (0.55, 0.55, 0.55, 1))
    paint(old, (0.85, 0.25, 0.10, 1))
    paint(new, (0.15, 0.45, 0.85, 1))

    vanilla.hide_render = False
    old.hide_render = False
    new.hide_render = True
    shoot(args.output / 'fal_hg_old_muzzle_seat.png', [vanilla, old], 'old')
    old.hide_render = True
    new.hide_render = False
    shoot(args.output / 'fal_hg_new_receiver_seat.png', [vanilla, new], 'new')

    vmn, vmx = bbox(vanilla)
    omn, omx = bbox(old)
    nmn, nmx = bbox(new)
    print('FAL_HG_PREVIEW=' + repr({
        'old_delta': list(d_old),
        'new_delta': list(d_new),
        'vanilla_y': [vmn.y, vmx.y],
        'old_y': [omn.y, omx.y],
        'new_y': [nmn.y, nmx.y],
        'receiver_gap_old': omn.y - vmn.y if False else omx.y - vmx.y,
        'receiver_gap_new': nmx.y - vmx.y,
        'muzzle_gap_old': omn.y - vmn.y,
        'muzzle_gap_new': nmn.y - vmn.y,
    }))


if __name__ == '__main__':
    main()
