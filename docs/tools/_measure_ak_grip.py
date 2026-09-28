"""Measure pistol-grip location relative to the entity origin (right hand).

blender --background --factory-startup --python this.py --
  --build AK74=<AK74_JAZZ.blend> --build AK74M=<AK74M_JAZZ.blend>
  --build AK105=<AK105_JAZZ.blend> --out <folder>

The JAZZ blends keep the body at the entity origin. Vertices below the
receiver and behind the trigger are the pistol grip; their centroid is
where the palm should sit. Writes grip-report.json plus a close-up of
the origin for each gun.
"""
import argparse
import json
import math
import sys
from pathlib import Path

import bpy
from mathutils import Vector

p = argparse.ArgumentParser()
p.add_argument('--build', action='append', required=True, help='<label>=<JAZZ blend>')
p.add_argument('--out', type=Path, required=True)
a = p.parse_args(sys.argv[sys.argv.index('--') + 1:])
a.out.mkdir(parents=True, exist_ok=True)
builds = dict(s.split('=', 1) for s in a.build)


def body_name(objects):
    meshes = [o for o in objects if o.type == 'MESH' and not o.name.endswith('_StockFolded')]
    roots = [o for o in meshes if o.name.startswith('AKR_') and o.name.count('_') == 1]
    return roots[0] if roots else meshes[0]


def grip_verts(obj):
    """Pistol grip: below the receiver, behind the trigger, not the magazine."""
    chosen = []
    for v in obj.data.vertices:
        # Local mesh is already at the entity origin. Trigger sits near y=-0.045.
        if v.co.z < 0.025 and -0.02 <= v.co.y <= 0.08 and abs(v.co.x) < 0.035:
            chosen.append(v.co.copy())
    return chosen


bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
report = {}

for label, path in builds.items():
    before = set(bpy.data.objects)
    with bpy.data.libraries.load(path, link=False) as (src, dst):
        dst.objects = [n for n in src.objects]
    loaded = [o for o in bpy.data.objects if o not in before]
    for obj in loaded:
        scene.collection.objects.link(obj)
        if obj.name.endswith('_StockFolded'):
            obj.hide_render = True
    body = body_name(loaded)
    bpy.context.view_layer.update()
    world = [body.matrix_world @ v for v in grip_verts(body)]
    if not world:
        # Fall back: lowest 8% of body vertices in Z, rear half in Y.
        all_v = [body.matrix_world @ v.co for v in body.data.vertices]
        zs = sorted(v.z for v in all_v)
        cut = zs[max(0, len(zs) // 12)]
        world = [v for v in all_v if v.z <= cut]
    lo = Vector(tuple(min(v[i] for v in world) for i in range(3)))
    hi = Vector(tuple(max(v[i] for v in world) for i in range(3)))
    centre = (lo + hi) / 2
    report[label] = {
        'body': body.name,
        'grip_n': len(world),
        'grip_min_m': [round(x, 5) for x in lo],
        'grip_max_m': [round(x, 5) for x in hi],
        'grip_centre_m': [round(x, 5) for x in centre],
        # Game centimetres, +X forward: ( -Y, -X, Z ) * 100
        'grip_centre_game_cm': [round(-centre.y * 100, 2),
                                round(-centre.x * 100, 2),
                                round(centre.z * 100, 2)],
        'origin_to_grip_game_cm': [round(-centre.y * 100, 2),
                                   round(-centre.x * 100, 2),
                                   round(centre.z * 100, 2)],
    }

# Close-up: every gun stays at its own origin so the red ball is the hand.
marker = bpy.data.meshes.new('Hand')
marker.from_pydata(
    [(0.008, 0, 0), (-0.008, 0, 0), (0, 0.008, 0), (0, -0.008, 0),
     (0, 0, 0.008), (0, 0, -0.008)],
    [(0, 1), (2, 3), (4, 5)], [])
marker.update()
hand = bpy.data.objects.new('Hand', marker)
scene.collection.objects.link(hand)
red = bpy.data.materials.new('Hand')
red.use_nodes = True
red.node_tree.nodes['Principled BSDF'].inputs['Emission Color'].default_value = (1, 0.1, 0.1, 1)
red.node_tree.nodes['Principled BSDF'].inputs['Emission Strength'].default_value = 4
hand.data.materials.append(red)

scene.render.engine = 'CYCLES'
scene.cycles.samples = 24
scene.render.film_transparent = True
scene.render.image_settings.file_format = 'PNG'
scene.render.image_settings.color_mode = 'RGBA'
scene.render.resolution_x = 1100
scene.render.resolution_y = 700
cam_data = bpy.data.cameras.new('GripCam')
cam_data.type = 'ORTHO'
cam_data.ortho_scale = 0.28
cam = bpy.data.objects.new('GripCam', cam_data)
scene.collection.objects.link(cam)
scene.camera = cam
# Side view of the grip: looking from +X, muzzle to the left (-Y).
cam.location = Vector((0.6, -0.02, -0.01))
cam.rotation_euler = (math.radians(90), 0, math.radians(90))
for i, loc in enumerate([(0.4, -0.2, 0.3), (-0.2, 0.15, 0.2)]):
    data = bpy.data.lights.new('GripLight%d' % i, 'AREA')
    data.energy, data.size = 80, 0.6
    light = bpy.data.objects.new(data.name, data)
    scene.collection.objects.link(light)
    light.location = Vector(loc)

# Hide all meshes, then reveal one family at a time.
families = {}
for obj in scene.objects:
    if obj.type != 'MESH' or obj.name == 'Hand':
        continue
    tag = obj.name.split('_')[1] if obj.name.startswith('AKR_') else obj.name
    families.setdefault(tag, []).append(obj)
    obj.hide_render = True

for label in builds:
    tag = label.replace('AK', 'AK') if False else None
    key = {'AK74': 'AK74', 'AK74M': 'AK74M', 'AK105': 'AK105'}[label]
    for obj in scene.objects:
        if obj.type == 'MESH' and obj.name != 'Hand':
            obj.hide_render = key not in obj.name.split('.')[0]
    scene.render.filepath = str(a.out / ('grip_%s.png' % label))
    bpy.ops.render.render(write_still=True)
    report[label]['preview'] = scene.render.filepath

# Combined origin-aligned side view, rows stacked.
for obj in scene.objects:
    if obj.type == 'MESH' and obj.name != 'Hand':
        obj.hide_render = False
# Move each family onto its own row without changing Y (bore).
pitch = 0.16
for index, label in enumerate(builds):
    key = label
    for obj in scene.objects:
        if obj.type != 'MESH' or key not in obj.name.split('.')[0]:
            continue
        if obj.parent is None:
            obj.location.z -= index * pitch
hand.location = Vector()
cam_data.ortho_scale = 0.55
cam.location = Vector((0.8, -0.02, -pitch * (len(builds) - 1) / 2))
scene.render.resolution_y = 1100
scene.render.filepath = str(a.out / 'grip_stack.png')
bpy.ops.render.render(write_still=True)
report['_stack'] = scene.render.filepath

(a.out / 'grip-report.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
print('GRIP=' + json.dumps(report))
