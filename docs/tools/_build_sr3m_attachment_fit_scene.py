"""Offline fit check for the SR3M receiver rail and handguard Side pad.

Blender: blender --background --factory-startup --python this.py --
  --rigged <rigged/SR3M_JA3.blend> --report <rigged/build-report.json>
  --reference <_vanilla_reference> --assets <jazz_assets> --out <attach_renders>

Real decoded HGM geometry is used wherever it exists; optics that only ship as mod
entities are drawn as labelled wireframe bounding boxes from their `.ent`, never as
invented meshes. Writes clearance numbers to fit-report.json. No active mod writes.
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
p.add_argument('--rigged', type=Path, required=True)
p.add_argument('--report', type=Path, required=True)
p.add_argument('--reference', type=Path, required=True)
p.add_argument('--assets', type=Path, required=True)
p.add_argument('--out', type=Path, required=True)
p.add_argument('--config', action='append')
a = p.parse_args(sys.argv[sys.argv.index('--') + 1:])
a.out.mkdir(parents=True, exist_ok=True)
build = json.loads(a.report.read_text(encoding='utf-8'))
spots = {k: Vector(v) for k, v in build['spots_blender_m'].items()}
rotations = {k: tuple(v) for k, v in build.get('spot_rotations_euler', {}).items()}
RAIL = build['rail']

# Each optic: JAZZ component id -> entity that its default visual mounts at Scope.
SCOPE_SET = [
    ('JAZZ_Reflex_Eotech', 'WeaponAttA_ScopeReflex'),
    ('JAZZ_CombatScope_2x', 'WeaponAttA_ScopeCOG'),
    ('JAZZ_NightScope', 'WeaponAttA_ScopeThermal'),
    ('JAZZ_Reflex_Aimpoint5000', 'Aimpoint5000'),
    ('JAZZ_Reflex_Closed', 'PKM_Scope'),
    ('JAZZ_Reflex_M68', 'Ithaca_AimPoint'),
    ('JAZZ_CombatScope_ACOG', 'ACOGV2'),
    ('JAZZ_Scope_Scout', 'SteyrS_Scope'),
]
SIDE_SET = [('JAZZ_Flashlight', 'WeaponAttA_SideLight'), ('JAZZ_LaserDot', 'WeaponAttA_SideLaser')]


def material(name, colour, wire=False):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes['Principled BSDF']
    bsdf.inputs['Base Color'].default_value = (*colour, 1)
    bsdf.inputs['Roughness'].default_value = 0.6
    if wire:
        bsdf.inputs['Emission Color'].default_value = (*colour, 1)
        bsdf.inputs['Emission Strength'].default_value = 1.5
    return m


def decoded(entity):
    path = a.reference / 'Geometry' / (entity + '_mesh.json')
    return path if path.is_file() else None


def ent_box(entity):
    path = a.assets / 'Entities' / (entity + '.ent')
    if not path.is_file():
        return None
    node = ET.parse(path).find('.//box')
    lo = [float(v) / 100 for v in node.get('min').split(',')]
    hi = [float(v) / 100 for v in node.get('max').split(',')]
    # .ent axes are centimetres with +X forward; convert to the Blender weapon frame.
    return (Vector((-hi[1], -hi[0], lo[2])), Vector((-lo[1], -lo[0], hi[2])))


def load_decoded(path, name, mat):
    """Rebuild a decoded HGM, seating every submesh inside its own declared bbox.

    Submesh vertices are not all stored symmetric about their bbox centre, so adding
    that centre blindly throws skinned parts metres away (visible as stray spikes).
    Re-centring on each submesh's own extents reproduces the declared bbox exactly.
    """
    data = json.loads(path.read_text())
    verts, faces = [], []
    for mesh in data['meshes']:
        if not mesh['vertices']:
            print('PARTIAL REFERENCE: empty submesh in', path.name)
            continue
        b = mesh['bbox'] or data['bbox']
        target = [(b[i] + b[i + 3]) * .5 for i in range(3)]
        local = [(min(v[i] for v in mesh['vertices']) + max(v[i] for v in mesh['vertices'])) * .5
                 for i in range(3)]
        offset = len(verts)
        for v in mesh['vertices']:
            x, y, z = [v[i] - local[i] + target[i] for i in range(3)]
            verts.append((-y, -x, z))
        faces.extend(tuple(i + offset for i in reversed(f)) for f in mesh['faces'])
    me = bpy.data.meshes.new(name)
    me.from_pydata(verts, [], faces)
    me.update()
    me.materials.append(mat)
    o = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(o)
    return o


def load_box(bounds, name, mat):
    """Wireframe cage for an optic whose mesh is not decoded: honest volume, no fake shape."""
    lo, hi = bounds
    verts = [(lo.x, lo.y, lo.z), (hi.x, lo.y, lo.z), (hi.x, hi.y, lo.z), (lo.x, hi.y, lo.z),
             (lo.x, lo.y, hi.z), (hi.x, lo.y, hi.z), (hi.x, hi.y, hi.z), (lo.x, hi.y, hi.z)]
    edges = [(0, 1), (1, 2), (2, 3), (3, 0), (4, 5), (5, 6), (6, 7), (7, 4),
             (0, 4), (1, 5), (2, 6), (3, 7)]
    me = bpy.data.meshes.new(name)
    me.from_pydata(verts, edges, [])
    me.update()
    o = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(o)
    skin = o.modifiers.new('Cage', 'SKIN')
    for v in o.data.skin_vertices[0].data:
        v.radius = (0.0013, 0.0013)
    o.data.materials.append(mat)
    return o


bpy.ops.wm.open_mainfile(filepath=str(a.rigged))
scene = bpy.context.scene
gun = material('Gun', (0.26, 0.29, 0.33))
optic = material('Optic real', (0.20, 0.52, 0.18))
cage = material('Optic bbox', (0.95, 0.55, 0.10), wire=True)
side_mat = material('Side device', (0.20, 0.42, 0.78))

for o in list(scene.objects):
    if o.type == 'MESH':
        o.hide_render = o.name.endswith('_StockFolded')
        o.data.materials.clear()
        o.data.materials.append(gun)
    elif o.type in {'LIGHT', 'CAMERA'}:
        bpy.data.objects.remove(o, do_unlink=True)
bpy.context.view_layer.update()

fit = {'rail_blender_y': [RAIL['y_front'], RAIL['y_rear']],
       'rail_z_plate': RAIL['z_plate'], 'rail_z_top': RAIL['z_top'],
       'scope_spot': list(spots['Scope']), 'side_spot': list(spots['Side']), 'optics': {}}
attachments = {}
for ident, entity in SCOPE_SET + SIDE_SET:
    slot = 'Scope' if (ident, entity) in SCOPE_SET else 'Side'
    path = decoded(entity)
    real = path is not None
    if real:
        obj = load_decoded(path, ident, optic if slot == 'Scope' else side_mat)
    else:
        bounds = ent_box(entity)
        if bounds is None:
            fit['optics'][ident] = {'entity': entity, 'status': 'entity not found'}
            continue
        obj = load_box(bounds, ident, cage)
    obj.location = spots[slot]
    obj.rotation_euler = rotations.get(slot, (0, 0, 0))
    obj.hide_render = True
    bpy.context.view_layer.update()
    points = [obj.matrix_world @ Vector(v) for v in obj.bound_box]
    lo = Vector(tuple(min(v[i] for v in points) for i in range(3)))
    hi = Vector(tuple(max(v[i] for v in points) for i in range(3)))
    record = {'entity': entity, 'slot': slot, 'geometry': 'decoded HGM' if real else 'ent bbox',
              'length_cm': (hi.y - lo.y) * 100}
    if slot == 'Scope':
        # Bite = how far the clamp reaches below the rail's base-plate top. It must land
        # inside the tooth band to read as clamped rather than hovering or buried.
        bite = (RAIL['z_plate'] - lo.z) * 100
        tooth = (RAIL['z_top'] - RAIL['z_plate']) * 100
        record.update({
            'height_cm': (hi.z - lo.z) * 100,
            'front_overhang_cm': max(0.0, (RAIL['y_front'] - lo.y)) * 100,
            'rear_overhang_cm': max(0.0, (hi.y - RAIL['y_rear'])) * 100,
            'clamp_bite_cm': bite,
            'top_above_rail_cm': (hi.z - RAIL['z_top']) * 100,
            'seating': 'floating' if bite < -0.25 else 'buried' if bite > tooth + 0.25 else 'seated'})
    else:
        record.update({'width_cm': (hi.z - lo.z) * 100, 'outboard_x_cm': min(lo.x, hi.x) * 100})
    fit['optics'][ident] = record
    attachments[ident] = obj

VIEWS = {'left': Vector((2.0, 0.02, 0.12)), 'right': Vector((-2.0, 0.02, 0.12)),
         'top': Vector((0.0, 0.0, 2.0))}
scene.render.engine = 'CYCLES'
scene.cycles.samples = 40
scene.render.resolution_percentage = 100
# The build scene renders on alpha for icons; a fit check needs a readable dark backdrop.
scene.render.film_transparent = False
scene.render.image_settings.file_format = 'PNG'
scene.world = bpy.data.worlds.new('Fit')
scene.world.use_nodes = True
scene.world.node_tree.nodes['Background'].inputs[0].default_value = (0.055, 0.055, 0.06, 1)
scene.world.node_tree.nodes['Background'].inputs[1].default_value = 0.35
camera_data = bpy.data.cameras.new('FitCamera')
camera_data.type = 'ORTHO'
camera = bpy.data.objects.new('FitCamera', camera_data)
scene.collection.objects.link(camera)
scene.camera = camera
lights = []
for i, loc in enumerate([(1.2, -0.7, 1.4), (-1.0, 0.5, 1.0), (0.3, 0.3, 1.5)]):
    data = bpy.data.lights.new('FitLight%d' % i, 'AREA')
    data.energy, data.size = 600, 2.0
    light = bpy.data.objects.new(data.name, data)
    scene.collection.objects.link(light)
    lights.append((light, Vector(loc)))

configs = a.config or ['bare', 'JAZZ_Reflex_Eotech', 'JAZZ_CombatScope_2x', 'JAZZ_Flashlight', 'muzzle']
for config in configs:
    for obj in attachments.values():
        obj.hide_render = True
    if config in attachments:
        attachments[config].hide_render = False
    views = ('left', 'right') if config in {'JAZZ_Flashlight', 'JAZZ_LaserDot'} else \
            ('left', 'right', 'top') if config in attachments else ('left', 'top')
    if config in attachments:
        views = views + ('detail',)
    for view in views:
        points = [o.matrix_world @ Vector(v) for o in scene.objects
                  if o.type == 'MESH' and not o.hide_render for v in o.bound_box]
        lo = Vector(tuple(min(v[i] for v in points) for i in range(3)))
        hi = Vector(tuple(max(v[i] for v in points) for i in range(3)))
        if config == 'muzzle':
            focus = spots['Muzzle'].copy()
            extent, across = 0.16, 0.16 * 0.46
        elif view == 'detail' or (view == 'top' and config in attachments):
            # Tight on the mounting interface, so a millimetre gap is actually visible.
            # From above, whole-gun framing collapses the receiver into a useless sliver.
            obj = attachments[config]
            pts = [obj.matrix_world @ Vector(v) for v in obj.bound_box]
            alo = Vector(tuple(min(v[i] for v in pts) for i in range(3)))
            ahi = Vector(tuple(max(v[i] for v in pts) for i in range(3)))
            focus = (alo + ahi) / 2
            focus.x = 0.0
            extent = max(ahi.y - alo.y, 0.10) * 1.5
            across = extent * 0.55
        else:
            focus = (lo + hi) / 2
            extent = (hi.y - lo.y) * 1.08
            # Screen-vertical is Z from the side and X from above; size the frame to the
            # taller of the two so a mounted optic is never cropped.
            across = ((hi.z - lo.z) if view != 'top' else (hi.x - lo.x)) * 1.14
        wide = 1600
        scene.render.resolution_x = wide
        scene.render.resolution_y = max(240, int(wide * across / extent))
        camera_data.ortho_scale = extent
        # A detail shot must look from the side the attachment is actually on.
        side = view
        if view == 'detail':
            side = 'right' if attachments[config].location.x < -0.005 else 'left'
        camera.location = focus + VIEWS[side]
        if view == 'top':
            camera.rotation_euler = (0, 0, math.radians(90))
        else:
            camera.rotation_euler = (focus - camera.location).to_track_quat('-Z', 'Y').to_euler()
        for light, offset in lights:
            light.location = focus + offset
            light.rotation_euler = (focus - light.location).to_track_quat('-Z', 'Y').to_euler()
        scene.render.filepath = str(a.out / ('sr3m_%s_%s.png' % (config, view)))
        bpy.ops.render.render(write_still=True)

(a.out / 'fit-report.json').write_text(json.dumps(fit, indent=2), encoding='utf-8')
print('SR3M_FIT=' + json.dumps(fit))
