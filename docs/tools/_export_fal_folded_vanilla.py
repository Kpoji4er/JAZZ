"""JAZZ-WEAPON-FAL-FAMILY-001: fold the vanilla FAL skeleton stock.

The archive Para mesh never sat on Weapon_FNFAL's Stock spot. The unfolded
state therefore stays on vanilla WeaponAttA_StockFNFal_01. This script only
builds the folded sibling, by swinging the vanilla frame about its hinge.

  blender --background --factory-startup --python docs/tools/_export_fal_folded_vanilla.py -- \
      --vanilla <_vanilla_reference/OBJ/WeaponAttA_StockFNFal_01_mesh.obj> \
      --textures <build>/Textures --output <build> --game-root <JA3_ROOT>
"""
import argparse
import importlib.util
import json
import math
import sys
from pathlib import Path

import bpy
from mathutils import Matrix, Vector

# Islands whose furthest Y sits beyond this (metres, vanilla local space) swing.
MOVE_Y = 0.10


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument('--vanilla', type=Path, required=True)
    p.add_argument('--textures', type=Path, required=True)
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


def main():
    args = parse_args()
    rigged = args.output / 'rigged'
    rigged.mkdir(parents=True, exist_ok=True)
    bpy.ops.wm.read_factory_settings(use_empty=True)
    hge = load_hge(args.game_root)

    bpy.ops.wm.obj_import(filepath=str(args.vanilla), forward_axis='Y', up_axis='Z')
    donor = bpy.context.view_layer.objects.active
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.remove_doubles(threshold=1e-5)
    bpy.ops.mesh.separate(type='LOOSE')
    bpy.ops.object.mode_set(mode='OBJECT')
    parts = [o for o in bpy.context.selected_objects if o.type == 'MESH']

    def max_y(o):
        return world_bbox([o])[1].y

    moving = [o for o in parts if max_y(o) > MOVE_Y]
    fixed = [o for o in parts if o not in moving]
    if not moving or not fixed:
        raise SystemExit('vanilla hinge split failed: moving=%d fixed=%d' % (len(moving), len(fixed)))

    hinge_y = world_bbox(fixed)[1].y
    pivot = Vector((0.0, hinge_y, 0.0))
    fold = (Matrix.Translation(pivot)
            @ Matrix.Rotation(math.radians(args.fold_angle), 4, 'Z')
            @ Matrix.Translation(-pivot))
    for o in moving:
        o.data.transform(fold)
        o.data.update()
    bpy.context.view_layer.update()

    bpy.ops.object.select_all(action='DESELECT')
    for o in parts:
        o.select_set(True)
    bpy.context.view_layer.objects.active = parts[0]
    bpy.ops.object.join()
    obj = bpy.context.view_layer.objects.active
    obj.name = 'FNFAL_ParaStk_fld'

    images = {}
    for key, fname in (('Base', 'FNFAL_ParaStk_Base.tga'), ('Normal', 'FNFAL_ParaStk_Normal.tga'),
                       ('RM', 'FNFAL_ParaStk_RM.tga'), ('AO', 'FNFAL_ParaStk_AO.tga')):
        path = args.textures / fname
        if path.exists():
            images[key] = bpy.data.images.load(str(path), check_existing=True)

    material = bpy.data.materials.new('FNFAL_ParaStk')
    hge.add_material_props(material)
    lookup = {'base_color': 'Base', 'normal_map': 'Normal',
              'roughness_metallic_map': 'RM', 'ambient_occlusion_map': 'AO'}
    for prop in hge.MATERIAL_PROPERTIES:
        if not prop.settings_name:
            continue
        key = lookup.get(prop.settings_name)
        if key in images:
            material[prop.id] = images[key].filepath_raw
        elif prop.map:
            material[prop.id] = ''
        else:
            material[prop.id] = getattr(material.hgm_settings, prop.settings_name)

    obj.data.materials.clear()
    obj.data.materials.append(material)
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    tri = obj.modifiers.new('Triangulate', 'TRIANGULATE')
    tri.keep_custom_normals = True
    bpy.ops.object.modifier_apply(modifier=tri.name)

    origin = bpy.data.objects.new('FNFAL_ParaStk_fld_Origin', None)
    bpy.context.collection.objects.link(origin)
    origin.location = Vector()
    obj.parent = origin
    obj.location = Vector()
    st = obj.hge_obj_settings
    st.entity = 'FNFAL_ParaStk_fld'
    st.mesh = 'Mesh'
    st.state = 'idle'
    st.lod = 1
    st.ignore = False
    obj.hge_export = True

    bpy.context.scene.unit_settings.system = 'METRIC'
    bpy.context.scene.unit_settings.scale_length = 1
    bpy.ops.wm.save_as_mainfile(filepath=str(rigged / 'FNFAL_ParaStk_fld.blend'))
    with hge.ObjectNamesExportContext(bpy.context):
        bpy.ops.export_scene.fbx(filepath=str(rigged / 'FNFAL_ParaStk_fld.fbx'),
                                 axis_forward='Y', axis_up='Z',
                                 apply_scale_options='FBX_SCALE_ALL',
                                 object_types={'MESH', 'EMPTY'}, use_custom_props=True,
                                 add_leaf_bones=False, bake_anim=False)

    mn, mx = world_bbox([obj])
    report = {
        'moving': len(moving), 'fixed': len(fixed),
        'pivot': list(pivot), 'min': list(mn), 'max': list(mx),
        'length_y': mx.y - mn.y,
    }
    (args.output / 'fal-folded-vanilla-report.json').write_text(
        json.dumps(report, indent=2), encoding='utf-8')
    print('FAL_FOLDED_VANILLA=' + json.dumps(report))


if __name__ == '__main__':
    main()
