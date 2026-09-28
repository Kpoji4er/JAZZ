"""JAZZ-WEAPON-M14-FAMILY-001: seat Lego wood, ART, EBR and unique on Weapon_M14.

  blender --background --factory-startup --python docs/tools/_export_m14_family_assets.py -- `
      --source D:/jazz_m14_build/src --vanilla D:/JaWeapons/Weapons/_vanilla_reference/OBJ `
      --output D:/jazz_m14_build --game-root <JA3_ROOT>

Writes one FBX per host plus m14-family-report.json. Does not install into jazz_assets.
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

_TOOLS = Path(__file__).resolve().parent
if str(_TOOLS) not in sys.path:
    sys.path.insert(0, str(_TOOLS))
from _ja3_mesh_prepare import prepare_export_mesh

TEX_SIZE = 2048
CM_TO_M = 0.01
PI2 = math.pi / 2.0


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument('--source', type=Path, required=True)
    p.add_argument('--vanilla', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--game-root', type=Path, required=True)
    argv = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
    return p.parse_args(argv)


def load_hge(game_root):
    spec = importlib.util.spec_from_file_location('m14_hge', game_root / 'ModTools/BlenderExport.py')
    hge = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(hge)
    hge.SETTINGS.update(version='71', game='Zulu', appid='Jagged Alliance 3',
                        mtl_prop_0_visible=True, mtl_prop_0_name='Unit', enable_colliders=False)
    hge.register()
    return hge


def world_bbox(obj):
    pts = [obj.matrix_world @ Vector(c) for c in obj.bound_box]
    mn = Vector((min(p.x for p in pts), min(p.y for p in pts), min(p.z for p in pts)))
    mx = Vector((max(p.x for p in pts), max(p.y for p in pts), max(p.z for p in pts)))
    return mn, mx


def apply_mesh(obj, matrix):
    obj.data.transform(matrix)
    obj.data.update()
    bpy.context.view_layer.update()


def import_obj(path, name, forward='Y', up='Z'):
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


def join_named(names, dest):
    objs = [bpy.data.objects[n] for n in names]
    bpy.ops.object.select_all(action='DESELECT')
    for o in objs:
        o.select_set(True)
    bpy.context.view_layer.objects.active = objs[0]
    if len(objs) > 1:
        bpy.ops.object.join()
    obj = bpy.context.view_layer.objects.active
    obj.name = dest
    return obj


def longest_axis(span):
    return max(range(3), key=lambda i: span[i])


def seat_on_target(donor, target):
    tmn, tmx = world_bbox(target)
    dmn, dmx = world_bbox(donor)
    tspan = tmx - tmn
    dspan = dmx - dmn
    t_axis = longest_axis(tspan)
    d_axis = longest_axis(dspan)
    if t_axis != d_axis:
        unused = ({0, 1, 2} - {t_axis, d_axis}).pop()
        apply_mesh(donor, Matrix.Rotation(PI2, 4, ('X', 'Y', 'Z')[unused]))
        dmn, dmx = world_bbox(donor)
        dspan = dmx - dmn
        d_axis = longest_axis(dspan)
    # Height belongs on Z, thickness on X. After the long-axis match the rifle
    # can still lie on its side (Lego wood did: X=15 cm, Z=4 cm).
    dmn, dmx = world_bbox(donor)
    dspan = dmx - dmn
    if dspan.x > dspan.z:
        apply_mesh(donor, Matrix.Rotation(PI2, 4, 'Y'))
        dmn, dmx = world_bbox(donor)
        dspan = dmx - dmn
    scale = tspan[t_axis] / (dspan[d_axis] or 1.0)
    apply_mesh(donor, Matrix.Scale(scale, 4))
    dmn, dmx = world_bbox(donor)
    delta = ((tmn + tmx) / 2.0) - ((dmn + dmx) / 2.0)
    apply_mesh(donor, Matrix.Translation(delta))
    point_muzzle_neg_y(donor)
    return scale, list(delta), t_axis, d_axis


def point_muzzle_neg_y(obj):
    """Flip 180 around Z if the slimmer end (barrel) sits on +Y."""
    ys = [v.co.y for v in obj.data.vertices]
    lo, hi = min(ys), max(ys)
    span = hi - lo or 1.0
    front, back = [], []
    for v in obj.data.vertices:
        t = (v.co.y - lo) / span
        if t < 0.12:
            front.append(v.co)
        elif t > 0.88:
            back.append(v.co)
    if not front or not back:
        return False

    def xz(pts):
        xs = [p.x for p in pts]
        zs = [p.z for p in pts]
        return (max(xs) - min(xs)) * (max(zs) - min(zs))

    if xz(back) < xz(front):
        apply_mesh(obj, Matrix.Rotation(math.pi, 4, 'Z'))
        return True
    return False


def pixels(path, size=TEX_SIZE):
    im = bpy.data.images.load(str(path), check_existing=False)
    im.colorspace_settings.name = 'Non-Color'
    im.scale(size, size)
    buf = np.empty(size * size * 4, np.float32)
    im.pixels.foreach_get(buf)
    bpy.data.images.remove(im)
    return buf.reshape(size, size, 4)


def save_tga(name, arr, dest, color=False):
    h, w = arr.shape[:2]
    im = bpy.data.images.new(name, width=w, height=h, alpha=True)
    im.colorspace_settings.name = 'sRGB' if color else 'Non-Color'
    im.pixels.foreach_set(arr.ravel())
    im.file_format = 'TARGA_RAW'
    im.filepath_raw = str(dest / (name + '.tga'))
    im.save()
    return im


def assign_hge_maps(hge, mat, images):
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


def build_pbr_material(hge, tex_dir, prefix, maps):
    tex_dir.mkdir(parents=True, exist_ok=True)
    images = {}
    if maps.get('Base'):
        images['Base'] = save_tga(prefix + '_Base', pixels(maps['Base']), tex_dir, True)
    if maps.get('Normal'):
        images['Normal'] = save_tga(prefix + '_Normal', pixels(maps['Normal']), tex_dir)
    if maps.get('AO'):
        images['AO'] = save_tga(prefix + '_AO', pixels(maps['AO']), tex_dir)
    if maps.get('RM'):
        images['RM'] = save_tga(prefix + '_RM', pixels(maps['RM']), tex_dir)
    else:
        rough = pixels(maps['Rough'])[:, :, 0] if maps.get('Rough') else None
        metal = pixels(maps['Metal'])[:, :, 0] if maps.get('Metal') else None
        spec = pixels(maps['Spec'])[:, :, 0] if maps.get('Spec') else None
        rm = np.ones((TEX_SIZE, TEX_SIZE, 4), np.float32)
        if rough is not None:
            rm[:, :, 0] = rough
        elif spec is not None:
            rm[:, :, 0] = 1.0 - spec
        if metal is not None:
            rm[:, :, 2] = metal
        elif spec is not None:
            rm[:, :, 2] = spec * 0.15
        images['RM'] = save_tga(prefix + '_RM', rm, tex_dir)
    mat = bpy.data.materials.new(prefix)
    assign_hge_maps(hge, mat, images)
    return mat


def pack_uv(obj, ox, oy, scale=0.5):
    uv = obj.data.uv_layers.active
    if uv is None:
        return
    for loop in uv.data:
        loop.uv = (loop.uv[0] * scale + ox, loop.uv[1] * scale + oy)


def compose_atlas(tiles):
    """tiles: list of (ox, oy, rgba HxWx4) in a 2x2 2048 atlas."""
    atlas = {key: np.ones((TEX_SIZE, TEX_SIZE, 4), np.float32) for key in ('Base', 'Normal', 'RM', 'AO')}
    for ox, oy, maps in tiles:
        x0 = int(ox * TEX_SIZE)
        y0 = int(oy * TEX_SIZE)
        size = TEX_SIZE // 2
        for key, arr in maps.items():
            if arr is None or key not in atlas:
                continue
            tile = arr
            if tile.shape[0] != size:
                # nearest shrink from 2048
                factor = tile.shape[0] // size
                tile = tile[::factor, ::factor]
            atlas[key][y0:y0 + size, x0:x0 + size] = tile[:size, :size]
    return atlas


def maps_from_set(folder, names, kind='pbr'):
    folder = Path(folder)
    out = {}
    if kind == 'pbr':
        base, normal, rough, metal, ao = names
        out['Base'] = pixels(folder / base) if (folder / base).exists() else None
        out['Normal'] = pixels(folder / normal) if (folder / normal).exists() else None
        out['Rough'] = pixels(folder / rough) if (folder / rough).exists() else None
        out['Metal'] = pixels(folder / metal) if (folder / metal).exists() else None
        out['AO'] = pixels(folder / ao) if (folder / ao).exists() else None
        rm = np.ones((TEX_SIZE, TEX_SIZE, 4), np.float32)
        if out['Rough'] is not None:
            rm[:, :, 0] = out['Rough'][:, :, 0]
        if out['Metal'] is not None:
            rm[:, :, 2] = out['Metal'][:, :, 0]
        out['RM'] = rm
    else:
        base, normal, spec = names
        out['Base'] = pixels(folder / base) if (folder / base).exists() else None
        out['Normal'] = pixels(folder / normal) if (folder / normal).exists() else None
        spec_px = pixels(folder / spec) if (folder / spec).exists() else None
        rm = np.ones((TEX_SIZE, TEX_SIZE, 4), np.float32)
        if spec_px is not None:
            rm[:, :, 0] = 1.0 - spec_px[:, :, 0]
            rm[:, :, 2] = spec_px[:, :, 0] * 0.15
        out['RM'] = rm
    return out


def add_spots(obj):
    mn, mx = world_bbox(obj)
    mid = (mn + mx) / 2.0
    z_mid = (mn.z + mx.z) / 2.0
    y_span = mx.y - mn.y
    spots = {
        'Muzzle': Vector((0.0, mn.y, z_mid + 0.01)),
        'MuzzleTip': Vector((0.0, mn.y - 0.008, z_mid + 0.01)),
        'Barrel': Vector((0.0, mn.y + y_span * 0.22, z_mid + 0.015)),
        'Magazine': Vector((0.0, mid.y + y_span * 0.04, mn.z + 0.018)),
        'Stock': Vector((0.0, mx.y - 0.02, z_mid - 0.01)),
        'Trigger': Vector((0.0, mid.y + y_span * 0.08, mn.z + 0.03)),
        'Hand_l_grip': Vector((0.0, mid.y - y_span * 0.08, mn.z + 0.02)),
        'Scope': Vector((0.0, mid.y + y_span * 0.10, mx.z + 0.008)),
        'General': Vector((0.0, mid.y + y_span * 0.10, mx.z)),
        'Mount': Vector((0.0, mid.y + y_span * 0.10, mx.z)),
        'Side': Vector((0.028, mid.y - y_span * 0.05, z_mid)),
        'Mountside': Vector((0.028, mid.y + y_span * 0.08, z_mid)),
        'Under': Vector((0.0, mid.y - y_span * 0.12, mn.z + 0.008)),
        'Bipod': Vector((0.0, mn.y + y_span * 0.18, mn.z)),
    }
    for name, point in spots.items():
        empty = bpy.data.objects.new(obj.name + '_' + name, None)
        bpy.context.collection.objects.link(empty)
        empty.parent = obj
        empty.location = point
        empty.hge_obj_settings.spot_name = name
    return {n: [round(p.x, 5), round(p.y, 5), round(p.z, 5)] for n, p in spots.items()}


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


def export_fbx(hge, path):
    with hge.ObjectNamesExportContext(bpy.context):
        bpy.ops.export_scene.fbx(
            filepath=str(path), axis_forward='Y', axis_up='Z',
            apply_scale_options='FBX_SCALE_ALL', object_types={'MESH', 'EMPTY'},
            use_custom_props=True, add_leaf_bones=False, bake_anim=False,
        )


def reset(hge_loader, game_root):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    return hge_loader(game_root)


def vanilla_target(vanilla):
    host = import_obj(vanilla / 'Weapon_M14_mesh.obj', 'van_host')
    stock = import_obj(vanilla / 'WeaponAttA_StockM14_Standard_mesh.obj', 'van_stock')
    return join_named(['van_host', 'van_stock'], 'van_m14_full')


def orient_lego(obj):
    apply_mesh(obj, Matrix.Scale(CM_TO_M, 4))
    apply_mesh(obj, Matrix.Rotation(PI2, 4, 'Z'))
    apply_mesh(obj, Matrix.Rotation(PI2, 4, 'Y'))


def place_optic(optic, host):
    hmn, hmx = world_bbox(host)
    omn, omx = world_bbox(optic)
    recv_y = hmn.y + (hmx.y - hmn.y) * 0.62
    target = Vector((0.0, recv_y, hmx.z + 0.002))
    current = Vector(((omn.x + omx.x) / 2.0, (omn.y + omx.y) / 2.0, omn.z))
    apply_mesh(optic, Matrix.Translation(target - current))


def report_obj(obj, extra):
    mn, mx = world_bbox(obj)
    extra = dict(extra)
    extra['span'] = [round(v, 5) for v in (mx - mn)]
    extra['triangles'] = len(obj.data.polygons)
    return extra


def main():
    args = parse_args()
    rigged = args.output / 'rigged'
    tex = args.output / 'Textures'
    rigged.mkdir(parents=True, exist_ok=True)
    tex.mkdir(parents=True, exist_ok=True)
    bpy.ops.wm.read_factory_settings(use_empty=True)
    hge = load_hge(args.game_root)
    report = {}

    target = vanilla_target(args.vanilla)
    wood = import_obj(args.source / 'lego' / 'part_06.obj', 'lego_wood', 'NEGATIVE_Z', 'Y')
    orient_lego(wood)
    scale, delta, t_axis, d_axis = seat_on_target(wood, target)
    tmn, tmx = world_bbox(target)
    vanilla_min, vanilla_max = list(tmn), list(tmx)
    bpy.data.objects.remove(target, do_unlink=True)
    mat = build_pbr_material(hge, tex, 'JAZZ_M14', {
        'Base': args.source / 'lego' / 'T_M14_D.tga.png',
        'Normal': args.source / 'lego' / 'T_M14_N.tga.png',
        'AO': args.source / 'lego' / 'T_M14_AO.tga.png',
        'Spec': args.source / 'lego' / 'T_M14_S.tga.png',
    })
    spots = add_spots(wood)
    finalise(wood, 'JAZZ_M14', mat)
    report['JAZZ_M14'] = report_obj(wood, {
        'scale': scale, 'delta': delta, 'target_axis': t_axis, 'donor_axis': d_axis,
        'vanilla_span': list(tmx - tmn), 'vanilla_min': vanilla_min,
        'vanilla_max': vanilla_max, 'spots': spots,
    })
    bpy.ops.wm.save_as_mainfile(filepath=str(rigged / 'JAZZ_M14.blend'))
    export_fbx(hge, rigged / 'JAZZ_M14.fbx')

    hge = reset(load_hge, args.game_root)
    art = import_obj(args.source / 'lego' / 'part_00.obj', 'lego_art', 'NEGATIVE_Z', 'Y')
    orient_lego(art)
    apply_mesh(art, Matrix.Scale(scale, 4))
    apply_mesh(art, Matrix.Translation(Vector(delta)))
    hmn = Vector(report['JAZZ_M14']['vanilla_min'])
    hmx = Vector(report['JAZZ_M14']['vanilla_max'])
    omn, omx = world_bbox(art)
    recv_y = hmn.y + (hmx.y - hmn.y) * 0.62
    target_pt = Vector((0.0, recv_y, hmx.z + 0.002))
    current = Vector(((omn.x + omx.x) / 2.0, (omn.y + omx.y) / 2.0, omn.z))
    apply_mesh(art, Matrix.Translation(target_pt - current))
    mat_art = build_pbr_material(hge, tex, 'JAZZ_M14_ART', {
        'Base': args.source / 'lego' / 'T_SB_D.tga.png',
        'Normal': args.source / 'lego' / 'T_SB_N.tga.png',
        'AO': args.source / 'lego' / 'T_SB_AO.tga.png',
        'Spec': args.source / 'lego' / 'T_SB_S.tga.png',
    })
    finalise(art, 'JAZZ_M14_ART', mat_art)
    report['JAZZ_M14_ART'] = report_obj(art, {'scale': scale, 'delta': list(delta)})
    bpy.ops.wm.save_as_mainfile(filepath=str(rigged / 'JAZZ_M14_ART.blend'))
    export_fbx(hge, rigged / 'JAZZ_M14_ART.fbx')

    hge = reset(load_hge, args.game_root)
    target = vanilla_target(args.vanilla)
    ebr_parts = [
        ('00', 'recv', ('m14_receiver_BaseColor.png', 'm14_receiver_Normal.png',
                        'm14_receiver_Roughness.png', 'm14_receiver_Metallic.png',
                        'm14_receiver_ambient_occlusion.png')),
        ('01', 'chassis', ('ebr_chassis_01_BaseColor.png', 'ebr_chassis_01_Normal.png',
                           'ebr_chassis_01_Roughness.png', 'ebr_chassis_01_Metallic.png',
                           'ebr_chassis_01_ambient_occlusion.png')),
        ('02', 'barrel', ('m14_barrels_BaseColor.png', 'm14_barrels_Normal.png',
                          'm14_barrels_Roughness.png', 'm14_barrels_Metallic.png',
                          'm14_barrels_ambient_occlusion.png')),
        ('05', 'stock', ('stock_BaseColor.png', 'stock_Normal.png',
                         'stock_Roughness.png', 'stock_Metallic.png',
                         'stock_ambient_occlusion.png')),
    ]
    offsets = [(0.0, 0.0), (0.5, 0.0), (0.0, 0.5), (0.5, 0.5)]
    tiles = []
    names = []
    for (idx, name, maps), (ox, oy) in zip(ebr_parts, offsets):
        obj = import_obj(args.source / 'mk14' / ('part_%s.obj' % idx), 'ebr_' + name, 'NEGATIVE_Z', 'Y')
        pack_uv(obj, ox, oy)
        tiles.append((ox, oy, maps_from_set(args.source / 'mk14', maps, 'pbr')))
        names.append(obj.name)
    ebr = join_named(names, 'ebr_join')
    scale_e, delta_e, ta, da = seat_on_target(ebr, target)
    bpy.data.objects.remove(target, do_unlink=True)
    atlas = compose_atlas(tiles)
    images = {key: save_tga('MK14EBR_' + key, atlas[key], tex, key == 'Base') for key in atlas}
    mat_ebr = bpy.data.materials.new('MK14EBR')
    assign_hge_maps(hge, mat_ebr, images)
    spots_e = add_spots(ebr)
    finalise(ebr, 'MK14EBR', mat_ebr)
    report['MK14EBR'] = report_obj(ebr, {'scale': scale_e, 'delta': delta_e, 'spots': spots_e})
    bpy.ops.wm.save_as_mainfile(filepath=str(rigged / 'MK14EBR.blend'))
    export_fbx(hge, rigged / 'MK14EBR.fbx')

    hge = reset(load_hge, args.game_root)
    target = vanilla_target(args.vanilla)
    uniq_parts = [
        ('04', 'body', ('m14.png', 'm14_normals.png', 'm14_spec.png')),
        ('00', 'scope', ('SCOPE.png', 'scope_normals.png', 'Scope_Spec.png')),
        ('01', 'supp', ('supp_baseTexBaked.png', 'supp_normals.png', 'Supp_Spec.png')),
        ('02', 'acc', ('Laser.png', 'laser_normals.png', 'Laser_spec.png')),
    ]
    tiles = []
    names = []
    for (idx, name, maps), (ox, oy) in zip(uniq_parts, offsets):
        obj = import_obj(args.source / 'uniq' / ('part_%s.obj' % idx), 'uniq_' + name, 'NEGATIVE_Z', 'Y')
        pack_uv(obj, ox, oy)
        tiles.append((ox, oy, maps_from_set(args.source / 'uniq', maps, 'spec')))
        names.append(obj.name)
    extra = import_obj(args.source / 'uniq' / 'part_03.obj', 'uniq_acc2', 'NEGATIVE_Z', 'Y')
    pack_uv(extra, 0.5, 0.5)
    names.append(extra.name)
    uniq = join_named(names, 'uniq_join')
    scale_u, delta_u, ta, da = seat_on_target(uniq, target)
    bpy.data.objects.remove(target, do_unlink=True)
    atlas = compose_atlas(tiles)
    images = {key: save_tga('JAZZ_M14_MkIII_' + key, atlas[key], tex, key == 'Base') for key in atlas}
    mat_u = bpy.data.materials.new('JAZZ_M14_MkIII')
    assign_hge_maps(hge, mat_u, images)
    spots_u = add_spots(uniq)
    finalise(uniq, 'JAZZ_M14_MkIII', mat_u)
    report['JAZZ_M14_MkIII'] = report_obj(uniq, {'scale': scale_u, 'delta': delta_u, 'spots': spots_u})
    bpy.ops.wm.save_as_mainfile(filepath=str(rigged / 'JAZZ_M14_MkIII.blend'))
    export_fbx(hge, rigged / 'JAZZ_M14_MkIII.fbx')

    (args.output / 'm14-family-report.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    print('M14_FAMILY_EXPORT=' + json.dumps(report))


if __name__ == '__main__':
    main()
