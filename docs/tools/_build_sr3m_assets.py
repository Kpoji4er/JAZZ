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

import bmesh
import bpy
import numpy as np
from mathutils import Matrix, Vector
from mathutils.bvhtree import BVHTree
from mathutils.interpolate import poly_3d_calc

_TOOLS = Path(__file__).resolve().parent
if str(_TOOLS) not in sys.path:
    sys.path.insert(0, str(_TOOLS))
from _ja3_mesh_prepare import prepare_export_mesh

p = argparse.ArgumentParser()
p.add_argument('--source', required=True)
p.add_argument('--output', required=True)
p.add_argument('--game-root', required=True)
p.add_argument('--export', action='store_true')
# JAZZ-WEAPON-SR3M-001: the stock receiver cover is a smooth ribbed AK-type dome with
# no rail, so top-mounted optics need one generated. Off by default.
p.add_argument('--top-rail', action='store_true')
p.add_argument('--rail-uv', choices=['project', 'flat'], default='project',
               help='project: nearest-surface UV from the cover; flat: one frozen texel')
args = p.parse_args(sys.argv[sys.argv.index('--') + 1:])
out = Path(args.output).resolve()
out.mkdir(parents=True, exist_ok=True)
clean_dir = out / 'clean'
rigged_dir = out / 'rigged'
for folder in (clean_dir, rigged_dir):
    folder.mkdir(parents=True, exist_ok=True)
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
    # Recalc only. Custom/split normals are never kept; the validator rejects
    # leftover zero-area tris instead of papering over them.
    prepare_export_mesh(o)

# MIL-STD-1913 profile in final weapon metres, measured against the baked cover crests
# (z=0.1015) and kept clear of the rear sight block at y<=-0.180.
RAIL = {'y_front': -0.168, 'y_rear': 0.030, 'z_base': 0.1000, 'z_plate': 0.1040,
        'z_top': 0.1095, 'half_base': 0.0106, 'half_top': 0.0078,
        'pitch': 0.0099, 'slot': 0.00535}


def cover_uv():
    """A UV on the receiver cover's crest, reused flat across the rail.

    Cheap and safe, but a single texel gives the rail no normal or roughness variation,
    so it reads flatter and lighter than the cover it sits on.
    """
    cover = bpy.data.objects['SR_3M_Top']
    layer = cover.data.uv_layers.active
    best = None
    for poly in cover.data.polygons:
        if poly.normal.z < 0.7:
            continue
        centre = sum((cover.data.vertices[i].co for i in poly.vertices), Vector()) / len(poly.vertices)
        if best is None or centre.z > best[0]:
            best = (centre.z, [layer.data[i].uv.copy() for i in poly.loop_indices])
    return sum(best[1], Vector((0, 0))) / len(best[1])


def cover_uv_sampler():
    """Nearest-surface UV lookup on the receiver cover.

    The rail sits directly on the cover, so taking the UV of the closest cover point
    makes it sample the same neighbourhood of the atlas and inherit real normal,
    roughness and AO detail instead of one frozen texel.
    """
    cover = bpy.data.objects['SR_3M_Top']
    mesh = cover.data
    layer = mesh.uv_layers.active
    coords = [v.co.copy() for v in mesh.vertices]
    tree = BVHTree.FromPolygons(coords, [list(p.vertices) for p in mesh.polygons],
                                all_triangles=False)

    def sample(point):
        location, _, index, _ = tree.find_nearest(point)
        if index is None:
            return None
        poly = mesh.polygons[index]
        weights = poly_3d_calc([coords[i] for i in poly.vertices], location)
        uv = Vector((0.0, 0.0))
        for weight, loop in zip(weights, poly.loop_indices):
            uv += weight * layer.data[loop].uv
        return uv

    return sample


def build_top_rail(material):
    """Low-poly Picatinny: one base plate plus a row of trapezoidal teeth."""
    r = RAIL
    verts, faces = [], []

    def box(y0, y1, z0, z1, hx0, hx1):
        base = len(verts)
        verts.extend([(-hx0, y0, z0), (hx0, y0, z0), (hx0, y1, z0), (-hx0, y1, z0),
                      (-hx1, y0, z1), (hx1, y0, z1), (hx1, y1, z1), (-hx1, y1, z1)])
        faces.extend([(base+0, base+1, base+2, base+3), (base+7, base+6, base+5, base+4),
                      (base+0, base+4, base+5, base+1), (base+2, base+6, base+7, base+3),
                      (base+1, base+5, base+6, base+2), (base+3, base+7, base+4, base+0)])

    box(r['y_front'], r['y_rear'], r['z_base'], r['z_plate'], r['half_base'], r['half_base'])
    tooth = r['pitch'] - r['slot']
    teeth = 0
    y = r['y_front']
    while y + tooth <= r['y_rear'] + 1e-9:
        box(y, y + tooth, r['z_plate'], r['z_top'], r['half_base'], r['half_top'])
        teeth += 1
        y += r['pitch']
    mesh = bpy.data.meshes.new('SR_3M_TopRail')
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    # Hand-written winding is easy to get backwards, and inverted normals only show up
    # in the game renderer. Let bmesh settle it, then assert every face points outward.
    bm = bmesh.new()
    bm.from_mesh(mesh)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(mesh)
    bm.free()
    mesh.update()
    # Signed volume is positive only when a closed surface is wound outward, and unlike a
    # centroid test it stays valid for a row of separate teeth.
    volume = 0.0
    for poly in mesh.polygons:
        corner = [mesh.vertices[i].co for i in poly.vertices]
        for k in range(1, len(corner) - 1):
            volume += corner[0].dot(corner[k].cross(corner[k + 1])) / 6.0
    assert volume > 0, 'Rail normals point inward: signed volume %.9f' % volume
    layer = mesh.uv_layers.new(name='UVMap')
    if args.rail_uv == 'project':
        sample = cover_uv_sampler()
        fallback = cover_uv()
        for loop in mesh.loops:
            uv = sample(mesh.vertices[loop.vertex_index].co)
            layer.data[loop.index].uv = uv if uv is not None else fallback
    else:
        uv = cover_uv()
        for loop in mesh.loops:
            layer.data[loop.index].uv = uv
    mesh.materials.append(material)
    obj = bpy.data.objects.new('SR_3M_TopRail', mesh)
    bpy.context.collection.objects.link(obj)
    obj.hge_export = False
    return obj, teeth


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

rail_teeth = 0
if args.top_rail:
    _, rail_teeth = build_top_rail(material)

groups = {
    'SR3M': ['Base', 'Top', 'Trigger', 'Barrel', 'Sights'] + (['TopRail'] if args.top_rail else []),
    'SR3M_Handguard': ['Handle', 'Rail'],
    'SR3M_Magazine': ['Magazine'],
    'SR3M_Muzzle': ['Muzzle'],
    'SR3M_Stock': ['Stock'],
}
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.scale_length = 1
bpy.ops.wm.save_as_mainfile(filepath=str(clean_dir / 'SR3M.blend'))
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
spot_rotations = {}
if args.top_rail:
    # Scope sits on the rail's top flat; most optic clamps reach 4-7 mm below their origin
    # and so bite onto the teeth rather than floating.
    spots['Scope'] = Vector((0.0, -0.060, RAIL['z_top']))
    # Side rides the handguard's own lateral Picatinny pad, rolled a quarter turn about the
    # bore so the device stands off the flank instead of the receiver.
    spots['Side'] = Vector((-0.03736, -0.256, 0.0761))
    spot_rotations['Side'] = (0.0, -math.pi / 2, 0.0)
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
    obj.rotation_euler = spot_rotations.get(name, (0.0, 0.0, 0.0))
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

# Keep the pre-rail build products intact: they describe what is currently installed.
stage = rigged_dir if args.top_rail else out
bpy.ops.wm.save_as_mainfile(filepath=str(rigged_dir / 'SR3M_JA3.blend'))
if not args.top_rail:
    bpy.ops.wm.save_as_mainfile(filepath=str(out / 'SR3M_JAZZ.blend'))
scene.render.filepath = str(stage / 'SR3M_preview.png')
bpy.ops.render.render(write_still=True)
stock.hide_render = True
folded.hide_render = False
scene.render.filepath = str(stage / 'SR3M_folded_preview.png')
bpy.ops.render.render(write_still=True)
stock.hide_render = False
folded.hide_render = True
report = {'entities': {}, 'rail_teeth': rail_teeth, 'rail': RAIL if args.top_rail else None,
          'spots_blender_m': {k:list(v) for k,v in spots.items()},
          'spot_rotations_euler': {k:list(v) for k,v in spot_rotations.items()}}
for name, obj in entity_objects.items():
    obj.data.calc_loop_triangles()
    report['entities'][name] = {'triangles':len(obj.data.loop_triangles),
        'vertices':len(obj.data.vertices), 'valid':obj.hge_obj_settings.is_valid(),
        'pivot':list(obj.parent.location)}
(stage / 'build-report.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
if args.export:
    for obj in entity_objects.values():
        prepare_export_mesh(obj)
    # Use the installed exporter's naming context and FBX settings, without its GUI.
    for o in list(bpy.data.objects):
        if o.type in {'CAMERA','LIGHT'}:
            bpy.data.objects.remove(o, do_unlink=True)
    fbx = rigged_dir / 'SR3M_JA3.fbx' if args.top_rail else out / 'SR3M_JAZZ.fbx'
    with hge.ObjectNamesExportContext(bpy.context):
        bpy.ops.export_scene.fbx(filepath=str(fbx), axis_forward='Y', axis_up='Z',
            apply_scale_options='FBX_SCALE_ALL', object_types={'MESH','EMPTY'},
            use_custom_props=True, add_leaf_bones=False, bake_anim=False)
print('SR3M_BUILD=' + json.dumps(report))
