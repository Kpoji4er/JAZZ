"""Rebind rear/shoulder armor to the actual clothed donor, retaining UV/materials.
Blender --source compiled-source.blend --shirt native.json --entity ID --output DIR
--game-root DIR. Exports a candidate only; never changes installed resources.
"""
import argparse,json,sys,math
from pathlib import Path
import bpy
from mathutils import Vector
from mathutils.bvhtree import BVHTree
from mathutils.geometry import barycentric_transform
sys.path.insert(0,str(Path(__file__).resolve().parent))
from _export_m14_family_assets import load_hge
from _ja3_mesh_prepare import prepare_export_mesh
p=argparse.ArgumentParser()
for k in ('source','shirt','output','game-root'):p.add_argument('--'+k,type=Path,required=True)
p.add_argument('--entity',required=True);a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
hge=load_hge(a.game_root);bpy.ops.wm.open_mainfile(filepath=str(a.source),use_scripts=False);bpy.context.view_layer.update()
armor=bpy.data.objects[a.entity];rig=next(m.object for m in armor.modifiers if m.type=='ARMATURE')
data=json.loads(a.shirt.read_text());shirt=data['meshes'][1];box=shirt.get('bbox') or data['bbox'];c=[(box[i]+box[i+3])/2 for i in range(3)]
vs=[Vector((-(v[1]+c[1]),-(v[0]+c[0]),v[2]+c[2])) for v in shirt['vertices']];faces=[tuple(f) for f in shirt['faces']]
weights=[{data['bones'][i]['name']:w for i,w in zip(ids,ws) if w>0 and data['bones'][i]['name'] in rig.data.bones} for ids,ws in zip(shirt['bone_indices'],shirt['bone_weights'])]
bvh=BVHTree.FromPolygons(vs,faces,all_triangles=True)
def normalize(w):
 w=dict(sorted(((n,x) for n,x in w.items() if x>1e-8),key=lambda pair:-pair[1])[:4]);s=sum(w.values());assert s>0;return {n:x/s for n,x in w.items()}
def native(q):
 co,normal,index,d=bvh.find_nearest(q);ids=faces[index]
 bary=barycentric_transform(co,*[vs[i] for i in ids],Vector((1,0,0)),Vector((0,1,0)),Vector((0,0,1)));w={}
 for i,f in zip(ids,bary):
  for n,x in weights[i].items():w[n]=w.get(n,0)+max(0,f)*x
 return normalize(w),co,normal,d
def fade(v):
 t=max(0,min(1,v));return t*t*(3-2*t)
rows=[];changed=0
for v in armor.data.vertices:
 pos=armor.matrix_world@v.co;old={armor.vertex_groups[g.group].name:g.weight for g in v.groups}
 if a.entity=='JAZZ_6B3_Male':blend=fade((pos.z-1.34)/.08)
 else:blend=fade((pos.y+.015)/.035)*fade((pos.z-1.05)/.08)*(1-fade((abs(pos.x)-.18)/.08))
 if blend<=0:continue
 # All layers sample the same garment point, preserving plate thickness.
 direction=Vector((pos.x,pos.y+.018,0));q=None
 if direction.length and pos.z<1.44:
  q,_,_,_=bvh.ray_cast(Vector((0,-.018,pos.z)),direction.normalized(),.6)
 field,co,normal,d=native(q if q is not None else pos)
 mixed=normalize({n:old.get(n,0)*(1-blend)+field.get(n,0)*blend for n in old.keys()|field.keys()})
 for g in list(v.groups):armor.vertex_groups[g.group].remove([v.index])
 for n,w in mixed.items():
  group=armor.vertex_groups.get(n) or armor.vertex_groups.new(name=n);group.add([v.index],w,'REPLACE')
 changed+=1;rows.append(d)
assert changed>100
# Add the exact shirt for the clothed CPU review, not the game export.
mesh=bpy.data.meshes.new('QA donor');mesh.from_pydata(vs,[],faces);obj=bpy.data.objects.new('QA actual LegionGoon shirt',mesh);bpy.context.collection.objects.link(obj)
groups={}
for v,w in zip(mesh.vertices,weights):
 for n,x in normalize(w).items():
  if n not in groups:groups[n]=obj.vertex_groups.new(name=n)
  groups[n].add([v.index],x,'REPLACE')
obj.modifiers.new('Native shirt skin','ARMATURE').object=rig;obj.hge_export=False
# The existing CPU strain comparator expects the official reference body.
if 'M_BaseMesh Skin_BIP' not in bpy.data.objects:
 sample=a.game_root/'ModTools/Samples/Assets/SampleMaleModel/BlenderScene_Appearance.blend'
 with bpy.data.libraries.load(str(sample),link=False) as (src,dst):dst.objects=['M_BaseMesh Skin_BIP']
 body=dst.objects[0];bpy.context.collection.objects.link(body);body.parent=None
 for modifier in body.modifiers:
  if modifier.type=='ARMATURE':modifier.object=rig
 body.hide_render=True;body.hge_export=False
for im in bpy.data.images:
 if im.filepath:im.filepath=bpy.path.abspath(im.filepath)
for mat in armor.data.materials:
 for prop in hge.MATERIAL_PROPERTIES:
  if prop.map and isinstance(mat.get(prop.id),str) and mat[prop.id].startswith('//'):mat[prop.id]=bpy.path.abspath(mat[prop.id])
assert not prepare_export_mesh(armor)
a.output.mkdir(parents=True,exist_ok=True);bpy.ops.wm.save_as_mainfile(filepath=str(a.output/(a.entity+'.blend')))
bpy.ops.object.select_all(action='DESELECT')
for o in (armor,rig,armor.parent):
 if o:o.hide_set(False);o.select_set(True)
filename=str(a.output/(a.entity+'.fbx'))
with hge.ObjectNamesExportContext(bpy.context):
 bpy.ops.export_scene.fbx(filepath=filename,use_selection=True,axis_forward='Y',axis_up='Z',apply_scale_options='FBX_SCALE_ALL',object_types={'MESH','EMPTY','ARMATURE'},use_custom_props=True,add_leaf_bones=False,bake_anim=False)
(a.output/'skin-report.json').write_text(json.dumps({'entity':a.entity,'changed_vertices':changed,'geometry_uv_materials_preserved':True,'runtime':'NOT_RUN'}))
