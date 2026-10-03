"""Fit a finished SSh60 to the existing Soviet helmet slot and export with HGE.

Blender --python this.py -- --source textured.blend --textures DIR --output DIR
  --game-root JA3_ROOT. Staging only; no active resource changes.
"""
import argparse
import importlib.util
import shutil
import sys
from pathlib import Path
import bpy
from mathutils import Vector

p = argparse.ArgumentParser(description=__doc__)
for name in ('source', 'textures', 'output', 'game-root'):
    p.add_argument('--' + name, type=Path, required=True)
a = p.parse_args(sys.argv[sys.argv.index('--') + 1:])
out = a.output.resolve(); out.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _ja3_mesh_prepare import prepare_export_mesh
spec = importlib.util.spec_from_file_location('ssh60_hge', a.game_root/'ModTools/BlenderExport.py')
hge = importlib.util.module_from_spec(spec); spec.loader.exec_module(hge)
hge.SETTINGS.update(version='71', game='Zulu', appid='Jagged Alliance 3',
                    mtl_prop_0_visible=True, mtl_prop_0_name='Unit', enable_colliders=True)
hge.register()
bpy.ops.wm.open_mainfile(filepath=str(a.source.resolve()))
o = bpy.data.objects['SSh60_finished']
for obj in list(bpy.data.objects):
    if obj != o: bpy.data.objects.remove(obj, do_unlink=True)
bpy.context.view_layer.objects.active = o; o.select_set(True)
# The official sample face and this input brim both point toward -Y.
# Fit the skull with the existing -40 game-unit Hat offset applied in preview.
lo = Vector(tuple(min(v.co[i] for v in o.data.vertices) for i in range(3)))
hi = Vector(tuple(max(v.co[i] for v in o.data.vertices) for i in range(3)))
target_lo = Vector((-.122, -.165, .108))
target_hi = Vector((.122, .143, .270))
for v in o.data.vertices:
    v.co = Vector(tuple(target_lo[i] + (v.co[i]-lo[i])/(hi[i]-lo[i]) *
                        (target_hi[i]-target_lo[i]) for i in range(3)))
prepare_export_mesh(o)
entity = 'JazzHat_SSh68'; o.name = entity
origin = bpy.data.objects.new('Origin_hat', None); bpy.context.collection.objects.link(origin)
o.parent = origin
settings = o.hge_obj_settings
settings.entity = entity; settings.mesh = 'mesh'; settings.state = 'idle'
settings.lod = 1; settings.lod_distance = 0; settings.inherit_animation = 'None'
settings.ignore = False; o.hge_export = True
mat = bpy.data.materials.new(entity); mat.use_nodes = True; hge.add_material_props(mat)
for prop in hge.MATERIAL_PROPERTIES:
    if not prop.settings_name: continue
    key = {'base_color': 'Base', 'normal_map': 'Norm', 'roughness_metallic_map': 'RM'}.get(prop.settings_name)
    if key:
        dest = out/(entity+'_'+key+'.tga')
        shutil.copy2(a.textures/('SSh60_'+key+'.tga'), dest)
        mat[prop.id] = str(dest)
    elif prop.map: mat[prop.id] = ''
    else: mat[prop.id] = getattr(mat.hgm_settings, prop.settings_name)
for prop in hge.MATERIAL_PROPERTIES:
    if prop.settings_name in ('project_specific_0', 'cast_shadows', 'receive_shadows', 'depth_write'):
        mat[prop.id] = True
o.data.materials.clear(); o.data.materials.append(mat)
for face in o.data.polygons: face.material_index = 0
assert len(o.data.uv_layers) == 1 and not o.data.has_custom_normals
bpy.ops.wm.save_as_mainfile(filepath=str(out/(entity+'.blend')))
with hge.ObjectNamesExportContext(bpy.context):
    bpy.ops.export_scene.fbx(filepath=str(out/(entity+'.fbx')), axis_forward='Y', axis_up='Z',
        apply_scale_options='FBX_SCALE_ALL', object_types={'MESH', 'EMPTY'},
        use_custom_props=True, add_leaf_bones=False, bake_anim=False)
print('EXPORT_READY', entity, 'rigid Hat, no animation inheritance')


