"""JAZZ-WEAPON-FAL-FAMILY-001: build the folding FAL Para stock entities.

Run through Blender, not plain Python:

  blender --background --factory-startup --python docs/tools/_export_fal_assets.py -- \
      --source <FAL archive folder with model_9.obj and FNFALParaStock_*.png> \
      --vanilla <_vanilla_reference/OBJ> \
      --output <build folder> \
      --game-root <JA3_ROOT>

Produces <build>/rigged/FNFAL_ParaStk.fbx holding two entities:
  FNFAL_ParaStk_unfld  - the 50.63 Para skeleton stock, deployed
  FNFAL_ParaStk_fld    - the same stock swung about its hinge, folded

The donor archive is authored in centimetres while JA3 attachment meshes are in
metres, hence the flat 0.01 factor. The donor is then seated so its hinge collar
coincides with the collar of vanilla WeaponAttA_StockFNFal_01, which is authored
around the weapon's Stock spot; that is what lets the new entities drop into the
existing spot without touching it.
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

CM_TO_M = 0.01
# Islands whose centre sits beyond this line (donor centimetres) swing on the hinge.
HINGE_CUT_Y = 31.4
TEX_SIZE = 2048


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument('--source', type=Path, required=True)
    p.add_argument('--vanilla', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--game-root', type=Path, required=True)
    p.add_argument('--fold-angle', type=float, default=180.0)
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


def split_islands(obj):
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.remove_doubles(threshold=1e-4)
    bpy.ops.mesh.separate(type='LOOSE')
    bpy.ops.object.mode_set(mode='OBJECT')
    parts = [o for o in bpy.context.selected_objects if o.type == 'MESH']
    bpy.context.view_layer.update()
    return parts


def face_centroid(objs, depth=0.015):
    verts = []
    for o in objs:
        verts += [o.matrix_world @ v.co for v in o.data.vertices]
    y0 = min(v.y for v in verts)
    sel = [v for v in verts if v.y <= y0 + depth]
    n = float(len(sel))
    return Vector((sum(v.x for v in sel) / n, y0, sum(v.z for v in sel) / n))


def build_textures(hge, source, out_dir, prefix):
    out_dir.mkdir(parents=True, exist_ok=True)

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
        im.filepath_raw = str(out_dir / (name + '.tga'))
        im.save()
        return im

    images = {
        'Base': save(prefix + '_Base', pixels(source / 'FNFALParaStock_Albedo.png'), color=True),
        'Normal': save(prefix + '_Normal', pixels(source / 'FNFALParaStock_Normal.png')),
        'AO': save(prefix + '_AO', pixels(source / 'FNFALParaStock_AO.png')),
    }
    rough = pixels(source / 'FNFALParaStock_Roughness.png')
    metal = pixels(source / 'FNFALParaStock_Metallic.png')
    rm = np.ones_like(rough)
    rm[:, 0] = rough[:, 0]
    rm[:, 1] = 0.0
    rm[:, 2] = metal[:, 0]
    images['RM'] = save(prefix + '_RM', rm)
    return images


def apply_material(hge, mat, images):
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


def finalise(obj, entity_name, material):
    obj.name = entity_name
    obj.data.materials.clear()
    obj.data.materials.append(material)
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    tri = obj.modifiers.new('Triangulate', 'TRIANGULATE')
    tri.keep_custom_normals = True
    bpy.ops.object.modifier_apply(modifier=tri.name)
    origin = bpy.data.objects.new(entity_name + '_Origin', None)
    bpy.context.collection.objects.link(origin)
    origin.location = Vector()
    obj.parent = origin
    obj.location = Vector()
    settings = obj.hge_obj_settings
    settings.entity = entity_name
    settings.mesh = 'Mesh'
    settings.state = 'idle'
    settings.lod = 1
    settings.ignore = False
    obj.hge_export = True
    return obj


def main():
    args = parse_args()
    out = args.output
    rigged = out / 'rigged'
    rigged.mkdir(parents=True, exist_ok=True)

    bpy.ops.wm.read_factory_settings(use_empty=True)
    hge = load_hge(args.game_root)

    vstock = import_obj(args.vanilla / 'WeaponAttA_StockFNFal_01_mesh.obj', 'van_stock', 'Y', 'Z')
    donor = import_obj(args.source / 'model_9.obj', 'donor', 'NEGATIVE_Z', 'Y')
    parts = split_islands(donor)

    scale = Matrix.Scale(CM_TO_M, 4)
    for p in parts:
        p.data.transform(scale)
        p.data.update()
    bpy.context.view_layer.update()

    def centre_y(p):
        mn, mx = world_bbox([p])
        return (mn.y + mx.y) / 2

    cut = HINGE_CUT_Y * CM_TO_M
    # the cut line is expressed in donor centimetres measured from the donor origin,
    # so rescale it the same way before comparing
    moving = [p for p in parts if centre_y(p) > cut]
    fixed = [p for p in parts if centre_y(p) <= cut]
    if not moving or not fixed:
        raise SystemExit('hinge split failed: moving=%d fixed=%d' % (len(moving), len(fixed)))

    delta = face_centroid([vstock]) - face_centroid(fixed)
    for p in parts:
        p.data.transform(Matrix.Translation(delta))
        p.data.update()
    bpy.context.view_layer.update()

    fixed_max_y = world_bbox(fixed)[1].y
    all_max_x = world_bbox(parts)[1].x
    pivot = Vector((all_max_x, fixed_max_y, 0.0))
    fold = (Matrix.Translation(pivot) @ Matrix.Rotation(math.radians(args.fold_angle), 4, 'Z')
            @ Matrix.Translation(-pivot))

    folded_parts = []
    for p in parts:
        dup = p.copy()
        dup.data = p.data.copy()
        dup.name = p.name + '_folded'
        bpy.context.collection.objects.link(dup)
        if p in moving:
            dup.data.transform(fold)
            dup.data.update()
        folded_parts.append(dup)
    bpy.context.view_layer.update()

    def join(objs, name):
        bpy.ops.object.select_all(action='DESELECT')
        for o in objs:
            o.select_set(True)
        bpy.context.view_layer.objects.active = objs[0]
        if len(objs) > 1:
            bpy.ops.object.join()
        obj = bpy.context.view_layer.objects.active
        obj.name = name
        return obj

    unfolded = join(parts, 'FNFAL_ParaStk_unfld')
    folded = join(folded_parts, 'FNFAL_ParaStk_fld')

    images = build_textures(hge, args.source, out / 'Textures', 'FNFAL_ParaStk')
    material = bpy.data.materials.new('FNFAL_ParaStk')
    apply_material(hge, material, images)

    bpy.data.objects.remove(vstock, do_unlink=True)
    for name, obj in (('FNFAL_ParaStk_unfld', unfolded), ('FNFAL_ParaStk_fld', folded)):
        finalise(obj, name, material)

    bpy.context.scene.unit_settings.system = 'METRIC'
    bpy.context.scene.unit_settings.scale_length = 1
    bpy.ops.wm.save_as_mainfile(filepath=str(rigged / 'FNFAL_ParaStk.blend'))

    with hge.ObjectNamesExportContext(bpy.context):
        bpy.ops.export_scene.fbx(filepath=str(rigged / 'FNFAL_ParaStk.fbx'),
                                 axis_forward='Y', axis_up='Z',
                                 apply_scale_options='FBX_SCALE_ALL',
                                 object_types={'MESH', 'EMPTY'}, use_custom_props=True,
                                 add_leaf_bones=False, bake_anim=False)

    report = {'fold_angle': args.fold_angle, 'align_delta_m': list(delta),
              'pivot_m': list(pivot), 'entities': {}}
    for obj in (unfolded, folded):
        mn, mx = world_bbox([obj])
        report['entities'][obj.name] = {
            'min': list(mn), 'max': list(mx),
            'length_y': mx.y - mn.y, 'triangles': len(obj.data.polygons),
        }
    (out / 'fal-stock-report.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    print('FAL_STOCK_EXPORT=' + json.dumps(report))


if __name__ == '__main__':
    main()
