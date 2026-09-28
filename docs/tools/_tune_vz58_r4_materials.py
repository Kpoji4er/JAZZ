"""Blender: rebuild bounded VZ58/R4 material candidates from pre-fix blends.

--blend FILE --family vz58|r4 --build DIR --game-root DIR [--wood DIR]
Keeps mesh/UV/spot data; reduces exaggerated tangent-space perturbations,
sets a matte metal roughness floor, consumes ImageGen wood albedo atlases.
Only exports to build; installed resources are handled separately.
"""
import argparse,json,sys
from pathlib import Path
import bpy,numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parent))
from _export_m14_family_assets import load_hge,save_tga,assign_hge_maps
from _weapon_material_finish import finish_material,separate_hard_edges
from _prepare_weapon_open_surfaces import prepare_export_mesh

p=argparse.ArgumentParser()
for key in ('blend','build','game-root'):p.add_argument('--'+key,type=Path,required=True)
p.add_argument('--family',choices=['vz58','r4'],required=True);p.add_argument('--wood',type=Path)
a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
a.build=a.build.resolve();a.game_root=a.game_root.resolve()
if a.wood:a.wood=a.wood.resolve()
for sub in ('Textures','rigged'):(a.build/sub).mkdir(parents=True,exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(a.blend));hge=load_hge(a.game_root)
for im in bpy.data.images:
 if im.filepath:im.filepath_raw=bpy.path.abspath(im.filepath)
for mat in bpy.data.materials:
 for prop in hge.MATERIAL_PROPERTIES:
  if prop.map and isinstance(mat.get(prop.id),str) and mat[prop.id].startswith('//'):
   mat[prop.id]=bpy.path.abspath(mat[prop.id])
report={};changed=set();mesh_repairs={}
for mat in bpy.data.materials:
 key=mat.name.removeprefix('JAZZ_VZ58_')
 if a.family=='vz58' and key not in ('Steel','Mag','Wood','StockWood'):continue
 if a.family=='r4' and mat.name!='JAZZ_VektorR4':continue
 nodes=mat.node_tree.nodes
 images={}
 for n in nodes:
  if n.type!='TEX_IMAGE' or not n.image:continue
  kind=next((k for k in ('Base','Normal','RM','AO') if n.image.name.endswith('_'+k)),None)
  if kind:images[kind]=(n,n.image)
 assert {'Base','Normal','RM'}<=images.keys(),(mat.name,images)
 def read(im):
  im.colorspace_settings.name='Non-Color'
  arr=np.empty(im.size[0]*im.size[1]*4,np.float32);im.pixels.foreach_get(arr)
  return arr.reshape(im.size[1],im.size[0],4)
 normal,rm,finish_report=finish_material(read(images['Normal'][1]),read(images['RM'][1]),a.family,key)
 replacements={'Normal':save_tga(mat.name+'_Normal',normal,a.build/'Textures'),
               'RM':save_tga(mat.name+'_RM',rm,a.build/'Textures')}
 if a.wood and key in ('Wood','StockWood'):
  im=bpy.data.images.load(str(a.wood/(key+'_Base.png')));im.colorspace_settings.name='sRGB';im.scale(2048,2048)
  im.file_format='TARGA_RAW';im.filepath_raw=str(a.build/'Textures'/(mat.name+'_Base.tga'));im.save()
  replacements['Base']=im
 for kind,im in replacements.items():images[kind][0].image=im
 all_maps={kind:replacements.get(kind,im) for kind,(_,im) in images.items()}
 assign_hge_maps(hge,mat,all_maps);changed.add(mat.name)
 report[mat.name]=finish_report
# Mixed-material variants share the same DDS with these single-material parts.
# Export each changed texture source once, without rebuilding unrelated geometry.
objects=[o for o in bpy.context.scene.objects if o.type=='MESH' and o.data.materials and all(m and m.name in changed for m in o.data.materials)]
assert objects
for o in objects:
 if a.family=='r4':mesh_repairs[o.name]=separate_hard_edges(o)
 prepare_export_mesh(o)
 assert not o.data.has_custom_normals
 original=o.location.copy();o.location=(0,0,0)
 bpy.ops.object.select_all(action='DESELECT');o.select_set(True)
 if o.parent:o.parent.select_set(True)
 for child in o.children:child.select_set(True)
 bpy.context.view_layer.objects.active=o
 filename=a.build/'rigged'/(o.name+'.fbx')
 with hge.ObjectNamesExportContext(bpy.context):
  bpy.ops.export_scene.fbx(filepath=str(filename),use_selection=True,axis_forward='Y',axis_up='Z',apply_scale_options='FBX_SCALE_ALL',object_types={'MESH','EMPTY'},use_custom_props=True,add_leaf_bones=False,bake_anim=False)
 o.location=original
bpy.ops.wm.save_as_mainfile(filepath=str(a.build/'rigged'/(a.family+'_material.blend')))
(a.build/'material-report.json').write_text(json.dumps({'materials':report,'entities':[o.name for o in objects],'mesh_repairs':mesh_repairs},indent=2))
print(json.dumps(report))
