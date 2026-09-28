"""JAZZ-WEAPON-FAL-FAMILY-001: build the tactical FAL handguard and stock.

The tactical rifle reuses the vanilla Weapon_FNFAL entity, so only the parts
that change its silhouette are imported. Each donor part is seated against the
matching vanilla attachment mesh, which is authored around the weapon spot, so
the new entities drop into the existing Handguard and Stock spots untouched.

  blender --background --factory-startup --python docs/tools/_export_fal_tactical_assets.py -- \
      --source <FAL Tactical extract> --vanilla <_vanilla_reference/OBJ> \
      --output <build> --game-root <JA3_ROOT> [--only JAZZ_FNFAL_TacHandguard]

Donor objects (verified by island survey, see the spec evidence section):
  model_2 - RIS handguard with full length top and bottom picatinny
  model_5 - polymer butt stock, classic FAL outline

Handguard seats on the receiver collar (max-Y after the Y-forward remaps).
Seating it on min-Y (muzzle) shoved the extra RIS length into the receiver.
"""
import argparse
import importlib.util
import json
import sys
from pathlib import Path

import bpy
import numpy as np
from mathutils import Matrix, Vector

_TOOLS = Path(__file__).resolve().parent
if str(_TOOLS) not in sys.path:
    sys.path.insert(0, str(_TOOLS))
from _ja3_mesh_prepare import prepare_export_mesh

CM_TO_M = 0.01
TEX_SIZE = 2048

PARTS = {
    'JAZZ_FNFAL_TacHandguard': {
        'donor': 'model_2.obj',
        'vanilla': 'WeaponAttA_HandguardFNFal_01_mesh.obj',
        'seat': 'max',
        'textures': {
            'Base': 'FNFALRailHandGuard_BaseColor.png',
            'Normal': 'FNFALRailHandGuard_Normal.png',
            'AO': 'FNFALRailHandGuard_AO.png',
            'Rough': 'FNFALRailHandGuard_Roughness.png',
            'Metal': 'FNFALRailHandGuard_Metallic.png',
        },
    },
    'JAZZ_FNFAL_TacStock': {
        'donor': 'model_5.obj',
        'vanilla': 'WeaponAttA_StockFNFal_02_mesh.obj',
        'seat': 'min',
        'textures': {
            'Base': 'FNFALPolymerStock_BaseColor.png',
            'Normal': 'FNFALPolymerStock_Normal.png',
            'AO': 'FNFALPolymerStock_AO.png',
            'Rough': 'FNFALPolymerStock_Roughness.png',
            'Metal': 'FNFALPolymerStock_Metallic.png',
        },
    },
}


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument('--source', type=Path, required=True)
    p.add_argument('--vanilla', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--game-root', type=Path, required=True)
    p.add_argument('--only', action='append', default=[])
    argv = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
    return p.parse_args(argv)


def load_hge(game_root):
    spec = importlib.util.spec_from_file_location('fal_hge', game_root / 'ModTools/BlenderExport.py')
    hge = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(hge)
    hge.SETTINGS.update(version='71', game='Zulu', appid='Jagged Alliance 3',
                        mtl_prop_0_visible=True, mtl_prop_0_name='Unit', enable_colliders=False)
    hge.register()
    return hge


def world_bbox(objs):
    pts = []
    for o in objs:
        pts += [o.matrix_world @ Vector(c) for c in o.bound_box]
    mn = Vector((min(p.x for p in pts), min(p.y for p in pts), min(p.z for p in pts)))
    mx = Vector((max(p.x for p in pts), max(p.y for p in pts), max(p.z for p in pts)))
    return mn, mx


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


def weld(obj):
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.remove_doubles(threshold=1e-4)
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.context.view_layer.update()


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


def build_material(hge, source, tex_dir, prefix, files):
    tex_dir.mkdir(parents=True, exist_ok=True)

    def pixels(path):
        im = bpy.data.images.load(str(path), check_existing=False)
        im.colorspace_settings.name = 'Non-Color'
        im.scale(TEX_SIZE, TEX_SIZE)
        buf = np.empty(TEX_SIZE * TEX_SIZE * 4, np.float32)
        im.pixels.foreach_get(buf)
        bpy.data.images.remove(im)
        return buf.reshape(-1, 4)

    def save(name, arr, color=False):
        im = bpy.data.images.new(name, width=TEX_SIZE, height=TEX_SIZE, alpha=True)
        im.colorspace_settings.name = 'sRGB' if color else 'Non-Color'
        im.pixels.foreach_set(arr.ravel())
        im.file_format = 'TARGA_RAW'
        im.filepath_raw = str(tex_dir / (name + '.tga'))
        im.save()
        return im

    images = {
        'Base': save(prefix + '_Base', pixels(source / files['Base']), color=True),
        'Normal': save(prefix + '_Normal', pixels(source / files['Normal'])),
        'AO': save(prefix + '_AO', pixels(source / files['AO'])),
    }
    rough = pixels(source / files['Rough'])
    rm = np.ones_like(rough)
    rm[:, 0] = rough[:, 0]
    rm[:, 1] = 0.0
    rm[:, 2] = pixels(source / files['Metal'])[:, 0]
    images['RM'] = save(prefix + '_RM', rm)

    mat = bpy.data.materials.new(prefix)
    hge.add_material_props(mat)
    lookup = {'base_color': 'Base', 'normal_map': 'Normal',
              'roughness_metallic_map': 'RM', 'ambient_occlusion_map': 'AO'}
    for prop in hge.MATERIAL_PROPERTIES:
        if not prop.settings_name:
            continue
        key = lookup.get(prop.settings_name)
        if key in images:
            mat[prop.id] = images[key].filepath_raw
        elif prop.map:
            mat[prop.id] = ''
        else:
            mat[prop.id] = getattr(mat.hgm_settings, prop.settings_name)
    return mat


def finalise(obj, entity_name, material):
    obj.name = entity_name
    obj.data.materials.clear()
    obj.data.materials.append(material)
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    prepare_export_mesh(obj)
    origin = bpy.data.objects.new(entity_name + '_Origin', None)
    bpy.context.collection.objects.link(origin)
    obj.parent = origin
    obj.location = Vector()
    s = obj.hge_obj_settings
    s.entity, s.mesh, s.state, s.lod, s.ignore = entity_name, 'Mesh', 'idle', 1, False
    obj.hge_export = True


def main():
    args = parse_args()
    rigged = args.output / 'rigged'
    rigged.mkdir(parents=True, exist_ok=True)
    bpy.ops.wm.read_factory_settings(use_empty=True)
    hge = load_hge(args.game_root)

    report = {}
    wanted = set(args.only) if args.only else set(PARTS)
    for entity, cfg in PARTS.items():
        if entity not in wanted:
            continue
        vanilla = import_obj(args.vanilla / cfg['vanilla'], entity + '_van', 'Y', 'Z')
        donor = import_obj(args.source / cfg['donor'], entity + '_donor', 'NEGATIVE_Z', 'Y')
        weld(donor)
        donor.data.transform(Matrix.Scale(CM_TO_M, 4))
        donor.data.update()
        bpy.context.view_layer.update()
        seat = cfg.get('seat', 'min')
        if seat == 'max':
            # Receiver Y, barrel-axis XZ from the muzzle tube so the taller
            # wood rear cap does not drag the RIS off the bore.
            van_r, don_r = face_centroid(vanilla, 'max'), face_centroid(donor, 'max')
            van_m, don_m = face_centroid(vanilla, 'min'), face_centroid(donor, 'min')
            delta = Vector((van_m.x - don_m.x, van_r.y - don_r.y, van_m.z - don_m.z))
        else:
            delta = face_centroid(vanilla, seat) - face_centroid(donor, seat)
        donor.data.transform(Matrix.Translation(delta))
        donor.data.update()
        bpy.context.view_layer.update()
        vmn, vmx = world_bbox([vanilla])
        dmn, dmx = world_bbox([donor])
        bpy.data.objects.remove(vanilla, do_unlink=True)
        material = build_material(hge, args.source, args.output / 'Textures', entity, cfg['textures'])
        finalise(donor, entity, material)
        report[entity] = {
            'seat': seat,
            'align_delta_m': list(delta),
            'vanilla_len_y': vmx.y - vmn.y, 'donor_len_y': dmx.y - dmn.y,
            'vanilla_y': [vmn.y, vmx.y], 'donor_y': [dmn.y, dmx.y],
            'min': list(dmn), 'max': list(dmx), 'triangles': len(donor.data.polygons),
        }

    bpy.context.scene.unit_settings.system = 'METRIC'
    bpy.context.scene.unit_settings.scale_length = 1
    bpy.ops.wm.save_as_mainfile(filepath=str(rigged / 'FNFAL_Tactical.blend'))
    with hge.ObjectNamesExportContext(bpy.context):
        bpy.ops.export_scene.fbx(filepath=str(rigged / 'FNFAL_Tactical.fbx'),
                                 axis_forward='Y', axis_up='Z',
                                 apply_scale_options='FBX_SCALE_ALL',
                                 object_types={'MESH', 'EMPTY'}, use_custom_props=True,
                                 add_leaf_bones=False, bake_anim=False)
    (args.output / 'fal-tactical-report.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    print('FAL_TACTICAL_EXPORT=' + json.dumps(report))


if __name__ == '__main__':
    main()
