"""Blender: bounded M14 mount separation or VZ58 grip UV correction.

--mode m14|grip --blend FILE --islands JSON --output DIR --game-root DIR.
No installed writes. Source geometry is preserved; grip changes only shell UVs
that sample grey atlas islands. Upper metal cap and bottom screw stay intact.
"""
import argparse,json,sys
from pathlib import Path
import bpy,bmesh
from mathutils import Matrix
sys.path.insert(0,str(Path(__file__).resolve().parent))
from _export_m14_family_assets import load_hge,export_fbx
from _prepare_weapon_open_surfaces import prepare_export_mesh
p=argparse.ArgumentParser();p.add_argument('--mode',choices=['m14','grip'],required=True)
p.add_argument('--base',type=Path,help='Decoded installed grip albedo for UV classification')
for key in ('blend','islands','output','game-root'):p.add_argument('--'+key,type=Path,required=True)
a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);hge=load_hge(a.game_root)
bpy.ops.wm.open_mainfile(filepath=str(a.blend),use_scripts=False)
name='JAZZ_M14' if a.mode=='m14' else 'JAZZ_VZ58_GripWood';obj=bpy.data.objects[name]
islands=json.loads(a.islands.read_text())[name]['islands'];report={};targets=[obj]
for im in bpy.data.images:
 if im.filepath:im.filepath=bpy.path.abspath(im.filepath)
for mat in obj.data.materials:
 for prop in hge.MATERIAL_PROPERTIES:
  if prop.map and isinstance(mat.get(prop.id),str) and mat[prop.id].startswith('//'):mat[prop.id]=bpy.path.abspath(mat[prop.id])
if a.mode=='m14':
 selected=set(islands[5]['face_indices']+islands[14]['face_indices']);assert len(selected)==742
 mount=obj.copy();mount.data=obj.data.copy();mount.name='JAZZ_M14_OpticsMount';bpy.context.collection.objects.link(mount)
 mount.hge_obj_settings.entity=mount.name
 for target,keep in [(obj,False),(mount,True)]:
  bm=bmesh.new();bm.from_mesh(target.data);bm.faces.ensure_lookup_table()
  bmesh.ops.delete(bm,geom=[f for f in bm.faces if (f.index in selected)!=keep],context='FACES')
  bmesh.ops.delete(bm,geom=[v for v in bm.verts if not v.link_faces],context='VERTS');bm.to_mesh(target.data);bm.free()
 targets.append(mount);report['separated_faces']=len(selected)
else:
 # The broad wood faces are correct. Bevels of the SAME shell used metal UVs.
 assert a.base
 im=bpy.data.images.load(str(a.base))
 im.colorspace_settings.name='Non-Color';pixels=list(im.pixels);w,h=im.size;uv=obj.data.uv_layers.active.data;changed=[]
 def grey(t):
  x=min(w-1,max(0,int(t.x*w)));y=min(h-1,max(0,int(t.y*h)));rgb=pixels[(y*w+x)*4:(y*w+x)*4+3]
  return max(rgb)-min(rgb)<.08 and sum(rgb)/3>.12
 for i in islands[0]['face_indices']:
  f=obj.data.polygons[i];loops=list(f.loop_indices);center=sum((uv[l].uv for l in loops),uv[loops[0]].uv*0)/len(loops)
  probes=[center]+[uv[l].uv for l in loops]+[(uv[l].uv+uv[loops[(j+1)%len(loops)]].uv)/2 for j,l in enumerate(loops)]
  if not any(grey(t) for t in probes):continue
  for li in loops:
   v=obj.data.vertices[obj.data.loops[li].vertex_index].co
   # Existing uninterrupted wood patch, with margin from neighbouring metal.
   uv[li].uv=(.55+(v.y+.041)/.082*.12,.15+(v.z+.050)/.084*.13)
  changed.append(i)
 assert 10<len(changed)<400,changed
 report['remapped_shell_faces']=len(changed);report['upper_cap_and_screw_unchanged']=True
for target in targets:
 out=a.output/target.name;out.mkdir(parents=True,exist_ok=True)
 # Isolate each export in a fresh copy; do not destroy the second candidate.
 keep={target,*target.children}
 if target.parent:keep.add(target.parent)
 for o in bpy.context.scene.objects:o.hide_set(o not in keep);o.select_set(o in keep)
 for o in bpy.context.scene.objects:
  if hasattr(o,'hge_export'):o.hge_export=o in keep
 if target.parent:target.parent.matrix_world=Matrix.Identity(4)
 target.matrix_world=Matrix.Identity(4);bpy.context.view_layer.objects.active=target
 issues=prepare_export_mesh(target);assert not issues and not target.data.has_custom_normals
 bpy.ops.wm.save_as_mainfile(filepath=str(out/(target.name+'.blend')))
 # HGE exports the selection, including only this target's origin/spots.
 filename=str(out/(target.name+'.fbx'))
 with hge.ObjectNamesExportContext(bpy.context):
  bpy.ops.export_scene.fbx(filepath=filename,use_selection=True,axis_forward='Y',axis_up='Z',apply_scale_options='FBX_SCALE_ALL',object_types={'MESH','EMPTY'},use_custom_props=True,add_leaf_bones=False,bake_anim=False)
 (out/'parts-report.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report))
