"""Scaled side/top overlay of two built weapons against a metre ruler.

Blender: blender --background --factory-startup --python this.py --
  --build <name>=<JAZZ blend> [--build ...] --assets <jazz_assets> --out <folder>

Lengths come from the built geometry; anchors come from the installed `.ent`
attach spots, so the overlay shows the same proportions the runtime loads.
Renders are clay-shaded on purpose: this answers "how long", not "how it looks".
"""
import argparse
import json
import math
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

import bpy
from mathutils import Vector

p = argparse.ArgumentParser()
p.add_argument('--build', action='append', required=True, help='<label>=<blend path>')
p.add_argument('--entity', action='append', default=[], help='<label>=<entity name>')
# A rebuilt weapon is not installed yet, so its anchors must come from the build report.
p.add_argument('--spots', action='append', default=[], help='<label>=<report json with spots_m>')
p.add_argument('--assets', type=Path, required=True)
p.add_argument('--out', type=Path, required=True)
p.add_argument('--anchor', default='Hand_l_grip')
# Trial scale about the entity origin, for comparing candidate sizes without rebuilding.
p.add_argument('--scale', action='append', default=[], help='<label>=<factor>')
a = p.parse_args(sys.argv[sys.argv.index('--') + 1:])
a.out.mkdir(parents=True, exist_ok=True)
builds = dict(s.split('=', 1) for s in a.build)
entities = dict(s.split('=', 1) for s in a.entity)
overrides = dict(s.split('=', 1) for s in a.spots)
factors = {k: float(v) for k, v in (s.split('=', 1) for s in a.scale)}

COLOURS = [(0.30, 0.36, 0.42), (0.52, 0.40, 0.24), (0.28, 0.44, 0.32), (0.45, 0.30, 0.38)]


def spots(label):
    """Attach spots in Blender metres, from a build report if given, else the installed .ent."""
    if label in overrides:
        data = json.loads(Path(overrides[label]).read_text(encoding='utf-8'))
        return {k: Vector(v) for k, v in data['spots_m'].items()}
    tree = ET.parse(a.assets / 'Entities' / (entities.get(label, label) + '.ent'))
    out = {}
    for node in tree.findall('.//attach'):
        x, y, z = (float(v) / 100 for v in node.get('spot_pos').split(','))
        out[node.get('name')] = Vector((-y, -x, z))
    return out


bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
report = {}
rows = []
for index, (label, path) in enumerate(builds.items()):
    with bpy.data.libraries.load(path, link=False) as (src, dst):
        dst.objects = [n for n in src.objects]
    clay = bpy.data.materials.new('Clay ' + label)
    clay.use_nodes = True
    bsdf = clay.node_tree.nodes['Principled BSDF']
    bsdf.inputs['Base Color'].default_value = (*COLOURS[index % len(COLOURS)], 1)
    bsdf.inputs['Roughness'].default_value = 0.55
    # Part pivots live on parent empties, so the whole hierarchy has to come across
    # or modules land at their local origin instead of their attach spot.
    loaded = [o for o in dst.objects if o is not None and o.type in {'MESH', 'EMPTY'}]
    group = []
    for obj in loaded:
        scene.collection.objects.link(obj)
        if obj.type != 'MESH':
            continue
        if obj.name.endswith('_StockFolded'):
            obj.hide_render = True
            continue
        obj.hide_render = False
        obj.data.materials.clear()
        obj.data.materials.append(clay)
        group.append(obj)
    control = bpy.data.objects.new('Overlay ' + label, None)
    scene.collection.objects.link(control)
    for obj in loaded:
        if obj.parent is None and obj is not control:
            obj.parent = control
    factor = factors.get(label, 1.0)
    control.scale = (factor, factor, factor)
    bpy.context.view_layer.update()
    points = [obj.matrix_world @ Vector(v) for obj in group for v in obj.bound_box]
    lo = Vector(tuple(min(v[i] for v in points) for i in range(3)))
    hi = Vector(tuple(max(v[i] for v in points) for i in range(3)))
    anchor = spots(label).get(a.anchor, (lo + hi) / 2) * factor
    report[label] = {'length_m': hi.y - lo.y, 'height_m': hi.z - lo.z, 'width_m': hi.x - lo.x,
                     'muzzle_y': lo.y, 'butt_y': hi.y, 'anchor_y': anchor.y, 'scale': factor,
                     'parts': sorted(o.name for o in group)}
    rows.append((label, group, lo, hi, anchor, control))

# One shared metre frame for every row, so pixels compare directly across guns.
depth = max(hi.z - lo.z for _, _, lo, hi, _, _ in rows)
breadth = max(hi.x - lo.x for _, _, lo, hi, _, _ in rows)
for mode in ('muzzle', 'grip'):
    # Grip alignment needs room for whichever gun reaches furthest ahead of the hand,
    # otherwise the longer barrel falls outside the frame and the ruler lies.
    lead = max(anchor.y - lo.y for _, _, lo, _, anchor, _ in rows) if mode == 'grip' else 0.0
    shifts = [(-lo.y if mode == 'muzzle' else lead - anchor.y)
              for _, _, lo, _, anchor, _ in rows]
    frame = max(hi.y + shift for (_, _, _, hi, _, _), shift in zip(rows, shifts))
    for view in ('side', 'top'):
        pitch = depth * 1.45 if view == 'side' else breadth * 2.2
        for index, (row, shift) in enumerate(zip(rows, shifts)):
            control = row[5]
            control.location = Vector((0, shift, 0))
            # Screen-up is +Z in the side view but -X from above; both must run downwards.
            if view == 'side':
                control.location.z = -index * pitch
            else:
                control.location.x = index * pitch
        bpy.context.view_layer.update()
        ortho = frame * 1.06
        width = 1500
        stack = (len(rows) - 1) * pitch + (depth if view == 'side' else breadth) * 1.25
        height = max(200, round(width * stack / ortho))
        scene.render.resolution_x, scene.render.resolution_y = width, height
        scene.render.resolution_percentage = 100
        scene.render.engine = 'CYCLES'
        scene.cycles.samples = 24
        scene.render.film_transparent = True
        scene.render.image_settings.file_format = 'PNG'
        scene.render.image_settings.color_mode = 'RGBA'
        points = [o.matrix_world @ Vector(v) for row in rows for o in row[1] for v in o.bound_box]
        lo = Vector(tuple(min(v[i] for v in points) for i in range(3)))
        hi = Vector(tuple(max(v[i] for v in points) for i in range(3)))
        centre = (lo + hi) / 2
        # Pin the frame's left edge to y=0 so the annotated ruler reads absolute metres.
        centre.y = ortho / 2
        camera_data = bpy.data.cameras.new('OverlayCamera ' + view + mode)
        camera_data.type = 'ORTHO'
        # Blender maps ortho_scale to the longer image side. With many stacked rows the
        # frame is taller than wide, so pin the fit horizontally or the guns get cropped.
        camera_data.sensor_fit = 'HORIZONTAL'
        camera_data.ortho_scale = ortho
        camera = bpy.data.objects.new(camera_data.name, camera_data)
        scene.collection.objects.link(camera)
        scene.camera = camera
        if view == 'side':
            camera.location = centre + Vector((4, 0, 0))
            camera.rotation_euler = (centre - camera.location).to_track_quat('-Z', 'Y').to_euler()
        else:
            # Yaw the top-down camera so screen-right stays +Y, matching the side view.
            camera.location = centre + Vector((0, 0, 4))
            camera.rotation_euler = (0, 0, math.radians(90))
        for i, loc in enumerate([(3, -1.2, 2.4), (-2, 1.0, 1.6), (0.5, 0.5, 3)]):
            data = bpy.data.lights.new('OverlayLight%d%s%s' % (i, view, mode), 'AREA')
            data.energy, data.size = 400, 2.5
            light = bpy.data.objects.new(data.name, data)
            scene.collection.objects.link(light)
            light.location = Vector(loc) + centre
            light.rotation_euler = (centre - light.location).to_track_quat('-Z', 'Y').to_euler()
        scene.render.filepath = str(a.out / ('overlay_%s_%s.png' % (mode, view)))
        bpy.ops.render.render(write_still=True)
        # Hand the annotator each row's real screen position instead of letting it assume
        # the rows are evenly spread over the image height.
        ppm = width / ortho
        cover = ortho * height / width
        bands = []
        for index, row in enumerate(rows):
            if view == 'side':
                pixel = (centre.z + cover / 2 - row[5].location.z) * ppm
            else:
                pixel = (row[5].location.x - (centre.x - cover / 2)) * ppm
            bands.append({'label': row[0], 'centre_px': pixel})
        report.setdefault('_frames', {})['%s_%s' % (mode, view)] = {
            'file': scene.render.filepath, 'ortho_scale_m': ortho,
            'pixels_per_metre': ppm, 'resolution': [width, height], 'rows': bands}

(a.out / 'overlay-report.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
print('OVERLAY=' + json.dumps(report))
