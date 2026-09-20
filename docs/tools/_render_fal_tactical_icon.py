"""JAZZ-WEAPON-FAL-FAMILY-001: render the inventory icon for the tactical FAL.

The FAL Tactical archive ships its parts already assembled, so the icon can be
rendered straight from the donor scene without the engine attachment spots.
Only the default loadout is shown - receiver, RIS handguard, polymer stock and
the standard magazine - so the icon matches what the item looks like with no
attachments fitted. The top rail, muzzle brake and red dot are left out.

  blender --background --factory-startup --python docs/tools/_render_fal_tactical_icon.py -- \
      --source <FAL Tactical extract> --output <jazz>/WeaponIcons/JAZZ_FNFAL_Tactical.png

Matches the existing WeaponIcons series: 324x165 RGBA, transparent background,
muzzle pointing right, black outline in the alpha fringe.

Blender ships without Pillow, so the run is two steps:

  blender ... --python _render_fal_tactical_icon.py -- --source <x> --output <y>
  python docs/tools/_render_fal_tactical_icon.py --post <y>_raw.png --output <y>
"""
import argparse
import math
import os
import sys
from pathlib import Path

import numpy as np

try:
    import bpy
    from mathutils import Vector
except ModuleNotFoundError:          # post-processing runs under system python
    bpy = None
    Vector = None

WIDTH, HEIGHT = 324, 165
SUPERSAMPLE = 4
CONTENT_WIDTH = 300          # matches the 12 px side margin of the shipped icons
CONTOUR_RAMP = (0.01, 0.13, 0.38)   # luma multiplier per shell, outermost first

# donor object -> texture stem in the archive
PARTS = {
    'model_3': 'FNFAL',                 # receiver, barrel, grip
    'model_2': 'FNFALRailHandGuard',    # RIS forend
    'model_5': 'FNFALPolymerStock',     # polymer butt stock
    'model_4': 'FNFALMag',              # 20 round magazine
}
MAPS = {'BaseColor': 'Base Color', 'Roughness': 'Roughness', 'Metallic': 'Metallic'}


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument('--source', type=Path)
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--post', type=Path, help='post-process this raw render and exit')
    p.add_argument('--light', type=float, default=350.0)
    # under Blender the real arguments sit after '--'; under system python they
    # are the ordinary argv tail
    argv = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:]
    return p.parse_args(argv)


def build_material(source, stem):
    mat = bpy.data.materials.new(stem)
    mat.use_nodes = True
    nt = mat.node_tree
    bsdf = nt.nodes['Principled BSDF']
    for suffix, socket in MAPS.items():
        path = source / ('%s_%s.png' % (stem, suffix))
        if not path.exists():
            continue
        tex = nt.nodes.new('ShaderNodeTexImage')
        tex.image = bpy.data.images.load(str(path), check_existing=True)
        if suffix != 'BaseColor':
            tex.image.colorspace_settings.name = 'Non-Color'
        nt.links.new(tex.outputs['Color'], bsdf.inputs[socket])
    normal_path = source / ('%s_Normal.png' % stem)
    if normal_path.exists():
        tex = nt.nodes.new('ShaderNodeTexImage')
        tex.image = bpy.data.images.load(str(normal_path), check_existing=True)
        tex.image.colorspace_settings.name = 'Non-Color'
        nmap = nt.nodes.new('ShaderNodeNormalMap')
        nt.links.new(tex.outputs['Color'], nmap.inputs['Color'])
        nt.links.new(nmap.outputs['Normal'], bsdf.inputs['Normal'])
    return mat


def world_bbox(objs):
    pts = []
    for o in objs:
        pts += [o.matrix_world @ Vector(c) for c in o.bound_box]
    mn = Vector((min(p.x for p in pts), min(p.y for p in pts), min(p.z for p in pts)))
    mx = Vector((max(p.x for p in pts), max(p.y for p in pts), max(p.z for p in pts)))
    return mn, mx


def postprocess(raw_path, out_path):
    from PIL import Image
    im = Image.open(raw_path).convert('RGBA')
    a = np.array(im).astype(np.float32)
    alpha = a[..., 3]
    ys, xs = np.nonzero(alpha > 4)
    if len(xs) == 0:
        raise SystemExit('render is empty')
    crop = im.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))

    scale = CONTENT_WIDTH / crop.width
    new_h = max(1, int(round(crop.height * scale)))
    if new_h > HEIGHT - 8:
        scale = (HEIGHT - 8) / crop.height
        new_h = HEIGHT - 8
    new_w = max(1, int(round(crop.width * scale)))
    crop = crop.resize((new_w, new_h), Image.LANCZOS)

    canvas = Image.new('RGBA', (WIDTH, HEIGHT), (0, 0, 0, 0))
    canvas.paste(crop, ((WIDTH - new_w) // 2, (HEIGHT - new_h) // 2))

    # The shipped icons carry a dark contour that runs inward rather than a ring
    # drawn outside the silhouette: the outer shells measure roughly 0, 8 and 29
    # luma before reaching the body. Reproduce that ramp so the new icon sits in
    # the same series.
    arr = np.array(canvas).astype(np.float32)
    solid = arr[..., 3] > 153
    shade = np.ones(solid.shape, dtype=np.float32)
    cur = solid.copy()
    for factor in CONTOUR_RAMP:
        padded = np.pad(cur, 1, constant_values=False)
        eroded = (padded[:-2, 1:-1] & padded[2:, 1:-1] & padded[1:-1, :-2] &
                  padded[1:-1, 2:] & padded[:-2, :-2] & padded[:-2, 2:] &
                  padded[2:, :-2] & padded[2:, 2:] & cur)
        shade[cur & ~eroded] = factor
        cur = eroded
    # pixels outside the solid mask are the antialiased fringe; keep them dark
    shade[~solid] = CONTOUR_RAMP[0]

    out = arr.copy()
    out[..., :3] = np.clip(arr[..., :3] * shade[..., None], 0, 255)
    Image.fromarray(out.astype(np.uint8), 'RGBA').save(out_path)
    print('ICON_WRITTEN=%s size=%dx%d content=%dx%d' % (out_path, WIDTH, HEIGHT, new_w, new_h))


def main():
    args = parse_args()
    if args.post is not None:
        postprocess(args.post, args.output)
        return
    bpy.ops.wm.read_factory_settings(use_empty=True)

    objs = []
    for name, stem in PARTS.items():
        before = {o.name for o in bpy.data.objects}
        bpy.ops.wm.obj_import(filepath=str(args.source / (name + '.obj')),
                              forward_axis='NEGATIVE_Z', up_axis='Y')
        new = [o for o in bpy.data.objects if o.name not in before and o.type == 'MESH']
        new.sort(key=lambda o: -len(o.data.vertices))
        obj = new[0]
        obj.name = name
        obj.data.materials.clear()
        obj.data.materials.append(build_material(args.source, stem))
        objs.append(obj)

    mn, mx = world_bbox(objs)
    ctr = (mn + mx) / 2
    span = max((mx - mn).y, (mx - mn).z)

    sc = bpy.context.scene
    sc.render.engine = 'BLENDER_EEVEE_NEXT'
    sc.render.film_transparent = True
    sc.render.resolution_x = WIDTH * SUPERSAMPLE
    sc.render.resolution_y = HEIGHT * SUPERSAMPLE
    sc.render.image_settings.file_format = 'PNG'
    sc.render.image_settings.color_mode = 'RGBA'
    sc.view_settings.view_transform = 'Standard'

    cam_data = bpy.data.cameras.new('cam')
    cam_data.type = 'ORTHO'
    cam_data.ortho_scale = span * 1.06
    cam = bpy.data.objects.new('cam', cam_data)
    sc.collection.objects.link(cam)
    sc.camera = cam
    # muzzle to the right, matching the shipped icon series
    cam.location = (ctr.x - span * 4, ctr.y, ctr.z)
    cam.rotation_euler = (math.radians(90), 0, math.radians(-90))

    # The donor archive is authored in centimetres, so point lights would sit
    # metres away and wash out to nothing. Sun lamps are distance independent.
    world = bpy.data.worlds.new('icon')
    world.use_nodes = True
    world.node_tree.nodes['Background'].inputs['Color'].default_value = (0.05, 0.05, 0.06, 1)
    world.node_tree.nodes['Background'].inputs['Strength'].default_value = 0.6
    sc.world = world

    scale = args.light / 25.0
    for direction, energy in (
        (Vector((-1.0, 0.45, -1.0)), 3.2 * scale),
        (Vector((-1.0, -0.8, -0.35)), 1.4 * scale),
        (Vector((0.6, 0.1, 0.9)), 0.8 * scale),
    ):
        ld = bpy.data.lights.new('sun', type='SUN')
        ld.energy = energy
        ld.angle = math.radians(25)
        lamp = bpy.data.objects.new('sun', ld)
        sc.collection.objects.link(lamp)
        lamp.rotation_euler = direction.normalized().to_track_quat('-Z', 'Y').to_euler()

    raw = args.output.with_name(args.output.stem + '_raw.png')
    sc.render.filepath = str(raw)
    bpy.ops.render.render(write_still=True)
    print('RAW_WRITTEN=%s' % raw)


if __name__ == '__main__':
    main()

