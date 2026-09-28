"""Blender offline render of M4 source snapshot into registered transparent layers.

blender -b --factory-startup --python render.py -- --blend FILE --assets DIR --output DIR
No source saves or active mod writes. Input must be an assembled M4A1 scene.
"""
import argparse
import hashlib
import json
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
import bpy
from mathutils import Vector

p = argparse.ArgumentParser(__doc__)
p.add_argument('--blend', type=Path, required=True)
p.add_argument('--assets', type=Path, required=True)
p.add_argument('--output', type=Path, required=True)
args = p.parse_args(sys.argv[sys.argv.index('--') + 1:])
args.output = args.output.resolve()
args.blend = args.blend.resolve()
args.assets = args.assets.resolve()
args.output.mkdir(parents=True, exist_ok=True)
(args.output / 'layers').mkdir(exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(args.blend), use_scripts=False)
scene = bpy.context.scene
scene.use_nodes = False
scene.render.engine = 'CYCLES'
scene.cycles.samples = 24
scene.cycles.use_denoising = True
scene.cycles.max_bounces = 1
scene.render.resolution_x, scene.render.resolution_y = 648, 330
scene.render.resolution_percentage = 100
scene.render.film_transparent = True
scene.render.image_settings.file_format = 'PNG'
scene.render.image_settings.color_mode = 'RGBA'
scene.view_settings.view_transform = 'Standard'
scene.view_settings.look = 'None'
scene.view_settings.exposure = 1.0
scene.world = bpy.data.worlds.new('LayerWorld')
scene.world.use_nodes = True
scene.world.node_tree.nodes['Background'].inputs[1].default_value = .3
for obj in list(scene.objects):
    if obj.type in {'CAMERA', 'LIGHT'}:
        bpy.data.objects.remove(obj, do_unlink=True)
center = Vector((0, -.16, .04))
camera = bpy.data.objects.new('LayerCamera', bpy.data.cameras.new('LayerCamera'))
scene.collection.objects.link(camera)
scene.camera = camera
camera.data.type = 'ORTHO'
camera.data.ortho_scale = 1.2
camera.location = center + Vector((-2, 0, 0))
camera.rotation_euler = (center - camera.location).to_track_quat('-Z', 'Y').to_euler()
for index, (offset, energy) in enumerate([((-1, -.5, 1.5), 35), ((-.5, .5, 1), 25), ((1, 1, 0), 25)]):
    data = bpy.data.lights.new('LayerLight' + str(index), 'AREA')
    data.energy, data.size = energy, 1.5
    obj = bpy.data.objects.new(data.name, data)
    scene.collection.objects.link(obj)
    obj.location = center + Vector(offset)
    obj.rotation_euler = (center - obj.location).to_track_quat('-Z', 'Y').to_euler()
meshes = [o for o in scene.objects if o.type == 'MESH']
prefix = 'M4R_M4A1'
# Back-to-front for the strict side camera. Other hosts require their own order.
parts = {'stock': ('Stock', 10), 'stock_collapsed': ('StockFolded', 10),
         'barrel': ('Barrel', 20), 'barrel_short': ('BarrelShort', 20),
         'barrel_long': ('BarrelLong', 20), 'magazine': ('Magazine', 30),
         'grip': ('Handgrip', 35),
         'body': ('', 40), 'frontsight': ('FrontSight', 45),
         'handguard': ('Handguard', 50), 'ris': ('HandguardRIS', 50),
         'carry': ('CarryHandle', 60), 'rear': ('RearSight', 60),
         'muzzle': ('DefMuzzle', 70), 'muzzle_short': ('DefMuzzle', 70),
         'muzzle_long': ('DefMuzzle', 70)}


def muzzle_spot(entity):
    path = args.assets / 'Entities' / (entity + '.ent')
    root = ET.parse(path)
    node = next(n for n in root.findall('.//attach') if n.get('name') == 'Muzzle')
    x, y, z = [float(v) / 100 for v in node.get('spot_pos').split(',')]
    return Vector((-y, -x, z))


normal = muzzle_spot(prefix + '_Barrel')
offsets = {name: muzzle_spot(prefix + '_Barrel' + suffix) - normal
           for name, suffix in [('muzzle_short', 'Short'), ('muzzle_long', 'Long')]}
layers = {}
for name, (suffix, order) in parts.items():
    entity = prefix + ('_' + suffix if suffix else '')
    obj = bpy.data.objects[entity]
    for other in meshes:
        other.hide_render = other != obj
    before = obj.location.copy()
    obj.location += offsets.get(name, Vector((0, 0, 0)))
    scene.render.filepath = str(args.output / 'layers' / (name + '.png'))
    bpy.ops.render.render(write_still=True)
    obj.location = before
    layers[name] = {'image': 'layers/' + name + '.png', 'z': order, 'entity': entity,
                    'delta_m': list(offsets.get(name, Vector((0, 0, 0))))}
    print('LAYER_READY', name, flush=True)

# Full-scene reference quantifies occlusion/shadow differences against compositing.
default_ids = ['stock', 'barrel', 'magazine', 'grip', 'body', 'frontsight', 'handguard', 'carry', 'muzzle']
visible = {layers[k]['entity'] for k in default_ids}
for obj in meshes:
    obj.hide_render = obj.name not in visible
scene.render.filepath = str(args.output / 'reference.png')
bpy.ops.render.render(write_still=True)


def bundle(*names):
    return {'layers': list(names)}


slots = {
    'Barrel': {'JAZZ_BarrelNormal': bundle('barrel'), 'JAZZ_BarrelShort': bundle('barrel_short'),
               'JAZZ_BarrelLong': bundle('barrel_long')},
    'Handguard': {'JAZZ_Handguard': bundle('handguard'), 'JAZZ_Handguard_RIS': bundle('ris')},
    'Handgrip': {'JAZZ_Handgrip_Default': bundle('grip')},
    'Magazine': {'JAZZ_MagNormal': bundle('magazine')},
    'Stock': {'JAZZ_StockLightUnFolded': bundle('stock'), 'JAZZ_StockLightFolded': bundle('stock_collapsed')},
    'Scope': {'JAZZ_CarryHandle_AR15': bundle('carry'), 'JAZZ_IronSight': bundle('rear')},
    'Under': {'': bundle()}, 'Side': {'': bundle()},
    'Muzzle': {'': bundle(), 'JAZZ_DefMuzzle': {'variants': [
        {'when': {'Barrel': 'JAZZ_BarrelNormal'}, 'layers': ['muzzle']},
        {'when': {'Barrel': 'JAZZ_BarrelShort'}, 'layers': ['muzzle_short']},
        {'when': {'Barrel': 'JAZZ_BarrelLong'}, 'layers': ['muzzle_long']}]}},
}
defaults = {'Barrel': 'JAZZ_BarrelNormal', 'Handguard': 'JAZZ_Handguard',
            'Handgrip': 'JAZZ_Handgrip_Default', 'Magazine': 'JAZZ_MagNormal',
            'Stock': 'JAZZ_StockLightUnFolded', 'Scope': 'JAZZ_CarryHandle_AR15',
            'Muzzle': 'JAZZ_DefMuzzle', 'Under': '', 'Side': ''}
registry = {'revision': 'prototype-m4-snapshot-v1', 'weapons': {'M4A1': {
    'host': prefix, 'slots': {s: {'default': defaults[s], 'options': {k: True for k in opts}}
                            for s, opts in slots.items()},
    'hosts': {prefix: {'width': 648, 'height': 330, 'layers': layers, 'fixed': ['body', 'frontsight'], 'slots': slots}}}},
    'provenance': {'blend_name': args.blend.name, 'blend_sha256': hashlib.sha256(args.blend.read_bytes()).hexdigest(),
                   'camera': {'direction': [-1, 0, 0], 'target_m': list(center), 'ortho_width_m': 1.2},
                   'light': '3 fixed area lights, Standard +1 exposure, no per-layer auto fit',
                   'limitations': 'Snapshot art only. Real 20-round magazine is WeaponAttA_MagazineCAR15_02, not snapshot Magazine20; intentionally unsupported until game capture. Side/Under external attachments unsupported. Long barrel keeps snapshot fore-end/sight; not a production legal-configuration preview.'}}
registry['weapons']['M4A1']['slots']['Magazine']['options']['JAZZ_MagSmall30_20'] = True
(args.output / 'registry.json').write_text(json.dumps(registry, indent=2), encoding='utf-8')
print('REGISTRY_READY', flush=True)
