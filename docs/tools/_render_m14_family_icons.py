"""JAZZ-WEAPON-M14-FAMILY-001: 324x165 icons from seated blends.

  blender --background --factory-startup --python docs/tools/_render_m14_family_icons.py -- `
      --build D:/jazz_m14_build --output <jazz>/WeaponIcons
  python docs/tools/_render_m14_family_icons.py --post --output <jazz>/WeaponIcons
"""
import argparse
import math
import sys
from pathlib import Path

import numpy as np

try:
    import bpy
    from mathutils import Vector
except ModuleNotFoundError:
    bpy = None
    Vector = None

WIDTH, HEIGHT = 324, 165
SUPERSAMPLE = 4
CONTENT_WIDTH = 300
CONTOUR_RAMP = (0.01, 0.13, 0.38)
ICONS = ('JAZZ_M14', 'MK14EBR', 'JAZZ_M14_MkIII')
NAME_MAP = {'JAZZ_M14': 'M14', 'MK14EBR': 'MK14EBR', 'JAZZ_M14_MkIII': 'JAZZ_M14_MkIII'}


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument('--build', type=Path)
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--post', action='store_true')
    argv = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:]
    return p.parse_args(argv)


def postprocess(raw_path, out_path):
    from PIL import Image
    im = Image.open(raw_path).convert('RGBA')
    a = np.array(im).astype(np.float32)
    alpha = a[..., 3]
    ys, xs = np.nonzero(alpha > 4)
    if len(xs) == 0:
        raise SystemExit('empty render %s' % raw_path)
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
    shade[~solid] = CONTOUR_RAMP[0]
    out = arr.copy()
    out[..., :3] = np.clip(arr[..., :3] * shade[..., None], 0, 255)
    Image.fromarray(out.astype(np.uint8), 'RGBA').save(out_path)
    print('ICON_WRITTEN', out_path)


def render_one(blend, raw):
    bpy.ops.wm.open_mainfile(filepath=str(blend))
    meshes = [o for o in bpy.data.objects if o.type == 'MESH']
    pts = []
    for o in meshes:
        pts += [o.matrix_world @ Vector(c) for c in o.bound_box]
    mn = Vector((min(p.x for p in pts), min(p.y for p in pts), min(p.z for p in pts)))
    mx = Vector((max(p.x for p in pts), max(p.y for p in pts), max(p.z for p in pts)))
    ctr = (mn + mx) / 2
    span = max((mx - mn).y, (mx - mn).z)
    sc = bpy.context.scene
    sc.render.engine = 'BLENDER_WORKBENCH'
    sc.render.film_transparent = True
    sc.render.resolution_x = WIDTH * SUPERSAMPLE
    sc.render.resolution_y = HEIGHT * SUPERSAMPLE
    sc.render.image_settings.file_format = 'PNG'
    sc.render.image_settings.color_mode = 'RGBA'
    cam_data = bpy.data.cameras.new('cam')
    cam_data.type = 'ORTHO'
    cam_data.ortho_scale = span * 1.08
    cam = bpy.data.objects.new('cam', cam_data)
    sc.collection.objects.link(cam)
    sc.camera = cam
    cam.location = (ctr.x - span * 4, ctr.y, ctr.z)
    cam.rotation_euler = (math.radians(90), 0, math.radians(-90))
    sc.render.filepath = str(raw)
    bpy.ops.render.render(write_still=True)
    print('RAW_WRITTEN', raw)


def main():
    args = parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    if args.post:
        for ent, name in NAME_MAP.items():
            raw = args.output / (name + '_raw.png')
            if raw.exists():
                postprocess(raw, args.output / (name + '.png'))
        return
    for ent in ICONS:
        render_one(args.build / 'rigged' / (ent + '.blend'), args.output / (NAME_MAP[ent] + '_raw.png'))


if __name__ == '__main__':
    main()
