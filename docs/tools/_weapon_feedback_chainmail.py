"""Extend existing baked rear harness straps into the belt; retain atlas UVs.
Blender --editable BLEND --source baked.blend --output DIR --game-root DIR.
"""
import argparse,json,sys
from pathlib import Path
import bpy
from mathutils import Vector
from mathutils.kdtree import KDTree
from mathutils.bvhtree import BVHTree
from mathutils.geometry import barycentric_transform
sys.path.insert(0,str(Path(__file__).resolve().parent))
from _export_m14_family_assets import load_hge
from _ja3_mesh_prepare import prepare_export_mesh
p=argparse.ArgumentParser()
for k in ('editable','source','output','game-root'):p.add_argument('--'+k,type=Path,required=True)
a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);hge=load_hge(a.game_root)
bpy.ops.wm.open_mainfile(filepath=str(a.editable),use_scripts=False);bpy.context.view_layer.update();deps=bpy.context.evaluated_depsgraph_get()
points=[]
for o in bpy.data.objects:
 if o.type=='MESH' and o.name.startswith('Plate carrying leather harness') and min(v.co.y for v in o.data.vertices)>0:
  ev=o.evaluated_get(deps);m=ev.to_mesh();points.extend(o.matrix_world@v.co for v in m.vertices);ev.to_mesh_clear()
assert len(points)>=180
kd=KDTree(len(points))
for i,v in enumerate(points):kd.insert(v,i)
kd.balance();shell=bpy.data.objects['TEST_chainmail_Male'];shell.data.calc_loop_triangles();vs=[v.co.copy() for v in shell.data.vertices];faces=[tuple(t.vertices) for t in shell.data.loop_triangles]
fields=[{shell.vertex_groups[g.group].name:g.weight for g in v.groups} for v in shell.data.vertices];surface=BVHTree.FromPolygons(vs,faces,all_triangles=True)
bpy.ops.wm.open_mainfile(filepath=str(a.source),use_scripts=False);o=bpy.data.objects['JAZZ_Chainmail_Male'];rig=next(m.object for m in o.modifiers if m.type=='ARMATURE');changed=0
for v in o.data.vertices:
 if kd.find(v.co)[2]>.00005:continue
 pos=v.co.copy();direction=Vector((pos.x,pos.y+.018,0)).normalized();co,_,_,_=surface.ray_cast(Vector((0,-.018,pos.z)),direction,.8)
 assert co is not None
 margin=(pos-co).dot(direction);z=1.45-(1.45-pos.z)*(1.45-1.055)/(1.45-1.205)
 q,n,idx,_=surface.ray_cast(Vector((0,-.018,z)),direction,.8);assert q is not None
 t=max(0,min(1,(z-1.10)/.09));v.co=q+direction*(margin*t+.001*(1-t))
 ids=faces[idx];bary=barycentric_transform(q,*[vs[i] for i in ids],Vector((1,0,0)),Vector((0,1,0)),Vector((0,0,1)));w={}
 for i,f in zip(ids,bary):
  for name,value in fields[i].items():w[name]=w.get(name,0)+max(0,f)*value
 w=dict(sorted(w.items(),key=lambda pair:-pair[1])[:4]);total=sum(w.values());assert total>0
 for g in list(v.groups):o.vertex_groups[g.group].remove([v.index])
 for name,value in w.items():
  group=o.vertex_groups.get(name) or o.vertex_groups.new(name=name);group.add([v.index],value/total,'REPLACE')
 changed+=1
assert changed>=100,changed
for im in bpy.data.images:
 if im.filepath:im.filepath=bpy.path.abspath(im.filepath)
for mat in o.data.materials:
 for prop in hge.MATERIAL_PROPERTIES:
  if prop.map and isinstance(mat.get(prop.id),str) and mat[prop.id].startswith('//'):mat[prop.id]=bpy.path.abspath(mat[prop.id])
assert not prepare_export_mesh(o);a.output.mkdir(parents=True,exist_ok=True);bpy.ops.wm.save_as_mainfile(filepath=str(a.output/(o.name+'.blend')))
bpy.ops.object.select_all(action='DESELECT')
for ob in (o,rig,o.parent):
 if ob:ob.hide_set(False);ob.select_set(True)
filename=str(a.output/(o.name+'.fbx'))
with hge.ObjectNamesExportContext(bpy.context):bpy.ops.export_scene.fbx(filepath=filename,use_selection=True,axis_forward='Y',axis_up='Z',apply_scale_options='FBX_SCALE_ALL',object_types={'MESH','EMPTY','ARMATURE'},use_custom_props=True,add_leaf_bones=False,bake_anim=False)
(a.output/'repair.json').write_text(json.dumps({'rear_strap_vertices':changed,'bottom_before':1.205,'bottom_after':1.055,'uv_atlas_preserved':True,'runtime':'NOT_RUN'}))
