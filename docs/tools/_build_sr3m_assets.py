"""Rebuild SR3M from a preserved source using Blender and the installed JA3 exporter.

Run with Blender --background --factory-startup --python this.py --
  --source <SR_3M.blend> --output <build-directory> --game-root <JA3_ROOT>
Does not edit the source or copy anything into active mods.
"""
import argparse
import importlib.util
import json
import math
import sys
from pathlib import Path

import bpy
import numpy as np
from mathutils import Matrix, Vector

p = argparse.ArgumentParser()
p.add_argument('--source', required=True)
p.add_argument('--output', required=True)
p.add_argument('--game-root', required=True)
p.add_argument('--export', action='store_true')
args = p.parse_args(sys.argv[sys.argv.index('--') + 1:])
out = Path(args.output).resolve()
out.mkdir(parents=True, exist_ok=True)
tex = out / 'Textures'
tex.mkdir(exist_ok=True)
spec = importlib.util.spec_from_file_location('sr3m_hge', Path(args.game_root) / 'ModTools/BlenderExport.py')
hge = importlib.util.module_from_spec(spec)
spec.loader.exec_module(hge)
hge.SETTINGS.update(version='71', game='Zulu', appid='Jagged Alliance 3',
                    mtl_prop_0_visible=True, mtl_prop_0_name='Unit', enable_colliders=True)
hge.register()
bpy.ops.wm.open_mainfile(filepath=str(Path(args.source).resolve()))

# Preserve the original source. Bake its world transforms into a common weapon frame.
# -Y is forward in Blender, as in the existing UMP scene. Grip origin and scale
# are explicit, reproducible and subject to in-hand runtime acceptance.
offset = Vector((0.00445, 0.055, 0.235))
scale = 0.8
transform = Matrix.Scale(scale, 4) @ Matrix.Translation(-offset)
meshes = [o for o in bpy.data.objects if o.type == 'MESH']
for o in meshes:
    bpy.ops.object.select_all(action='DESELECT')
    o.select_set(True)
    bpy.context.view_layer.objects.active = o
    world = o.matrix_world.copy()
    o.parent = None
    o.data.transform(transform @ world)
    o.matrix_world = Matrix.Identity(4)
    o.hide_set(False)
    o.hide_render = False
    # Triangulate in Blender, retaining the artist's split normals. Letting the
    # FBX SDK triangulate these ngons produced two zero-length normals.
    tri = o.modifiers.new('JA3_Triangulate', 'TRIANGULATE')
    tri.keep_custom_normals = True
    bpy.ops.object.modifier_apply(modifier=tri.name)
for o in list(bpy.data.objects):
    if o.type != 'MESH':
        bpy.data.objects.remove(o, do_unlink=True)

images = {}
scene = bpy.context.scene
scene.render.image_settings.file_format = 'TARGA_RAW'
scene.render.image_settings.color_mode = 'RGB'
scene.render.image_settings.color_depth = '8'
# Packed images save their original PNG bytes with Image.save(). Use an explicit
# pixel copy so the exporter receives genuine uncompressed TGA, without view transforms.
def save_tga(im, path):
    width, height = im.size
    pixels = np.empty(width*height*4, np.float32)
    im.pixels.foreach_get(pixels)
    copy = bpy.data.images.new(path.stem, width=width, height=height, alpha=True)
    copy.colorspace_settings.name = im.colorspace_settings.name
    copy.pixels.foreach_set(pixels)
    copy.file_format = 'TARGA_RAW'
    copy.filepath_raw = str(path)
    copy.save()
    assert path.read_bytes()[2] == 2, 'Expected uncompressed RGB TGA'
    return copy
for key, name in [('BaseColor', 'Albedo.png'), ('Normal', 'Normal.png'),
                  ('Roughness', 'Roughness.png'), ('Metallic', 'Metallic.png'), ('AO', 'AO.png')]:
    im = bpy.data.images[name]
    images[key] = save_tga(im, tex / f'SR3M_{key}.tga')
w, h = images['Roughness'].size
r = np.empty(w*h*4, np.float32)
m = np.empty(w*h*4, np.float32)
images['Roughness'].pixels.foreach_get(r)
images['Metallic'].pixels.foreach_get(m)
rm = np.ones((w*h, 4), np.float32)
rm[:, 0] = r.reshape(-1, 4)[:, 0]
rm[:, 1] = 0
rm[:, 2] = m.reshape(-1, 4)[:, 0]
im = bpy.data.images.new('SR3M_RoughnessMetallic', width=w, height=h, alpha=True)
im.colorspace_settings.name = 'Non-Color'
im.pixels.foreach_set(rm.ravel())
im.filepath_raw = str(tex / 'SR3M_RoughnessMetallic.tga')
im.file_format = 'TARGA_RAW'
im.save()
images['RoughnessMetallic'] = im

material = bpy.data.materials['Material_SR_3M']
material.name = 'SR3M'
for node in material.node_tree.nodes:
    if node.type == 'TEX_IMAGE' and node.image:
        key = {'Albedo.png':'BaseColor', 'Normal.png':'Normal', 'Roughness.png':'Roughness',
               'Metallic.png':'Metallic', 'AO.png':'AO'}.get(node.image.name)
        if key:
            node.image = images[key]
hge.add_material_props(material)
# HGE reads material custom properties; preserve artist's shader for Blender previews.
for prop in hge.MATERIAL_PROPERTIES:
    if prop.settings_name:
        image_key = {'base_color':'BaseColor', 'normal_map':'Normal',
                     'roughness_metallic_map':'RoughnessMetallic',
                     'ambient_occlusion_map':'AO'}.get(prop.settings_name)
        if image_key:
            material[prop.id] = str(Path(images[image_key].filepath_raw))
        elif prop.map:
            material[prop.id] = ''
        else:
            material[prop.id] = getattr(material.hgm_settings, prop.settings_name)

barrel = bpy.data.objects['SR_3M_Barrel']
# Artist's isolated barrel lacks its material slot, but retains the source UV layer.
barrel.data.materials.append(material)

groups = {
    'SR3M': ['Base', 'Top', 'Trigger', 'Barrel', 'Sights'],
    'SR3M_Handguard': ['Handle', 'Rail'],
    'SR3M_Magazine': ['Magazine'],
    'SR3M_Muzzle': ['Muzzle'],
    'SR3M_Stock': ['Stock'],
}
source_spots = {
    'Magazine': (0.00445, -0.104, 0.285),
    'Stock': (0.028, 0.120, 0.312),
    'Handguard': (0.00445, -0.15, 0.319),
    'Muzzle': (0.00445, -0.405, 0.319),
    'Barrel': (0.00445, -0.46187, 0.319),
    'Under': (0.00445, -0.284, 0.26865),
    'Hand_l_grip': (0.00445, -0.250, 0.290),
    'Trigger': (0.00445, 0.0, 0.257),
}
spots = {k: transform @ Vector(v) for k, v in source_spots.items()}
entity_objects = {}
for entity, suffixes in groups.items():
    bpy.ops.object.select_all(action='DESELECT')
    objs = [bpy.data.objects['SR_3M_' + s] for s in suffixes]
    for o in objs:
        o.select_set(True)
    bpy.context.view_layer.objects.active = objs[0]
    if len(objs) > 1:
        bpy.ops.object.join()
    obj = bpy.context.object
    obj.name = entity
    origin = bpy.data.objects.new(entity + '_Origin', None)
    bpy.context.collection.objects.link(origin)
    pivot = spots.get(entity.removeprefix('SR3M_'), Vector()) if entity != 'SR3M' else Vector()
    origin.location = pivot
    obj.data.transform(Matrix.Translation(-pivot))
    obj.parent = origin
    obj.location = Vector()
    settings = obj.hge_obj_settings
    settings.entity = entity
    settings.mesh = 'Mesh'
    settings.state = 'idle'
    settings.lod = 1
    settings.ignore = False
    obj.hge_export = True
    entity_objects[entity] = obj

stock = entity_objects['SR3M_Stock']
folded = stock.copy()
folded.data = stock.data.copy()
folded.name = 'SR3M_StockFolded'
bpy.context.collection.objects.link(folded)
folded.data.transform(Matrix.Rotation(math.pi, 4, 'Z'))
folded.hge_obj_settings.entity = folded.name
folded.hide_render = True
entity_objects[folded.name] = folded

for name, point in spots.items():
    obj = bpy.data.objects.new(name, None)
    bpy.context.collection.objects.link(obj)
    obj.parent = entity_objects['SR3M']
    obj.location = point
    obj.hge_obj_settings.spot_name = name

tip = bpy.data.objects.new('MuzzleTip', None)
bpy.context.collection.objects.link(tip)
tip.parent = entity_objects['SR3M_Muzzle']
tip.location = spots['Barrel'] - spots['Muzzle']
tip.hge_obj_settings.spot_name = 'Muzzle'

scene = bpy.context.scene
scene.unit_settings.system = 'METRIC'
scene.unit_settings.scale_length = 1
scene.render.engine = 'CYCLES'
scene.cycles.samples = 24
scene.render.resolution_x = 1200
scene.render.resolution_y = 600
scene.render.resolution_percentage = 100
scene.render.film_transparent = True
scene.render.image_settings.file_format = 'PNG'
scene.render.image_settings.color_mode = 'RGBA'
scene.world.color = (0.3, 0.3, 0.3)
camera_data = bpy.data.cameras.new('ReviewCamera')
camera = bpy.data.objects.new('ReviewCamera', camera_data)
bpy.context.collection.objects.link(camera)
camera.location = (1.6, -0.05, 0.32)
target = Vector((0, -0.045, -0.035))
camera.rotation_euler = (target-camera.location).to_track_quat('-Z','Y').to_euler()
camera_data.type = 'ORTHO'
camera_data.ortho_scale = 0.86
scene.camera = camera
for idx, (loc, energy, size) in enumerate([((1,-0.5,1.5),80,1.5), ((-0.5,0.5,1),65,1), ((1,1,0),35,1)]):
    data = bpy.data.lights.new(f'ReviewLight{idx}', 'AREA')
    data.energy, data.shape, data.size = energy, 'DISK', size
    light = bpy.data.objects.new(data.name, data)
    bpy.context.collection.objects.link(light)
    light.location = loc
    light.rotation_euler = (target-light.location).to_track_quat('-Z','Y').to_euler()

bpy.ops.wm.save_as_mainfile(filepath=str(out / 'SR3M_JAZZ.blend'))
scene.render.filepath = str(out / 'SR3M_preview.png')
bpy.ops.render.render(write_still=True)
stock.hide_render = True
folded.hide_render = False
scene.render.filepath = str(out / 'SR3M_folded_preview.png')
bpy.ops.render.render(write_still=True)
stock.hide_render = False
folded.hide_render = True
report = {'entities': {}, 'spots_blender_m': {k:list(v) for k,v in spots.items()}}
for name, obj in entity_objects.items():
    obj.data.calc_loop_triangles()
    report['entities'][name] = {'triangles':len(obj.data.loop_triangles),
        'vertices':len(obj.data.vertices), 'valid':obj.hge_obj_settings.is_valid(),
        'pivot':list(obj.parent.location)}
(out / 'build-report.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
if args.export:
    # Use the installed exporter's naming context and FBX settings, without its GUI.
    for o in list(bpy.data.objects):
        if o.type in {'CAMERA','LIGHT'}:
            bpy.data.objects.remove(o, do_unlink=True)
    with hge.ObjectNamesExportContext(bpy.context):
        bpy.ops.export_scene.fbx(filepath=str(out / 'SR3M_JAZZ.fbx'), axis_forward='Y', axis_up='Z',
            apply_scale_options='FBX_SCALE_ALL', object_types={'MESH','EMPTY'},
            use_custom_props=True, add_leaf_bones=False, bake_anim=False)
print('SR3M_BUILD=' + json.dumps(report))
