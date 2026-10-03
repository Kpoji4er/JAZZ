"""Blender: restore OBJ authored hard boundaries as topology, no custom normals.
--source OBJ --blend FILE --entity NAME --family r4|vz58 --output DIR --game-root DIR
Preserves candidate triangle/UV surface; no installed writes or texture changes.
"""
import argparse,sys,json,math
from pathlib import Path
from collections import Counter,defaultdict
import bpy,bmesh
from mathutils import Matrix,Vector
sys.path.insert(0,str(Path(__file__).resolve().parent))
from _export_m14_family_assets import load_hge,export_fbx
from _prepare_weapon_open_surfaces import prepare_export_mesh
p=argparse.ArgumentParser()
for k in ('source','blend','entity','family','output','game-root'):p.add_argument('--'+k,required=True)
a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);out=Path(a.output);out.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True)
if a.family=='vz58':bpy.ops.wm.obj_import(filepath=a.source,forward_axis='Y',up_axis='Z')
else:bpy.ops.wm.obj_import(filepath=a.source)
src=next(o for o in bpy.context.scene.objects if o.type=='MESH');m=src.data
if a.family=='vz58':
 s=.845/(42.41209411621094+42.3818244934082)
 transform=Matrix(((s,0,0,0),(0,0,-s,-15*s),(0,s,0,7*s),(0,0,0,1)))@Matrix.Translation((0,9.60988998413086,0))
else:
 coords=[src.matrix_world@v.co for v in m.vertices];s=1.005/(max(v.x for v in coords)-min(v.x for v in coords))
 transform=Matrix.Rotation(math.pi/2,4,'Z')@Matrix.Scale(s,4)@Matrix.Translation((-120,-4.5,12))@src.matrix_world
pos=[tuple(round(x,5) for x in transform@v.co) for v in m.vertices]
norm=[n.vector.copy() for n in m.corner_normals];edges=defaultdict(list)
for f in m.polygons:
 ls=list(f.loop_indices)
 for i,l in enumerate(ls):
  other=ls[(i+1)%len(ls)];v1=m.loops[l].vertex_index;v2=m.loops[other].vertex_index
  if pos[v1]==pos[v2]:continue
  key=tuple(sorted((pos[v1],pos[v2])));pair=(norm[l],norm[other]) if pos[v1]==key[0] else (norm[other],norm[l])
  edges[key].append(pair)
sharp=set()
for key,rows in edges.items():
 if any(min(rows[0][0].dot(r[0]),rows[0][1].dot(r[1]))<math.cos(math.radians(1)) for r in rows[1:]):sharp.add(key)
bpy.ops.wm.open_mainfile(filepath=a.blend,use_scripts=False);hge=load_hge(Path(a.game_root));o=bpy.data.objects[a.entity]
keep={o,*o.children}
if o.parent:keep.add(o.parent)
for other in list(bpy.context.scene.objects):
 if other not in keep:bpy.data.objects.remove(other,do_unlink=True)
for im in bpy.data.images:
 if im.filepath:im.filepath=bpy.path.abspath(im.filepath)
for mat in o.data.materials:
 for prop in hge.MATERIAL_PROPERTIES:
  if prop.map and isinstance(mat.get(prop.id),str) and mat[prop.id].startswith('//'):mat[prop.id]=bpy.path.abspath(mat[prop.id])
def surface():
 mesh=o.data;mesh.calc_loop_triangles();uv=mesh.uv_layers.active.data
 return Counter(tuple(sorted(tuple(round(x,7) for x in mesh.vertices[vi].co)+tuple(round(x,7) for x in uv[li].uv) for vi,li in zip(t.vertices,t.loops))) for t in mesh.loop_triangles)
before=surface();bm=bmesh.new();bm.from_mesh(o.data);count=len(bm.faces)
bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-7);assert len(bm.faces)==count
bm.to_mesh(o.data);bm.free();matched=marked=0
for e in o.data.edges:
 key=tuple(sorted(tuple(round(x,5) for x in o.data.vertices[i].co) for i in e.vertices))
 matched+=key in edges;e.use_edge_sharp=key in sharp;marked+=e.use_edge_sharp
bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o
mod=o.modifiers.new('Authored OBJ boundaries','EDGE_SPLIT');mod.use_edge_angle=False;mod.use_edge_sharp=True
bpy.ops.object.modifier_apply(modifier=mod.name);issues=prepare_export_mesh(o)
assert before==surface(),'Surface or UV changed';assert not o.data.has_custom_normals
if o.parent:o.parent.matrix_world=Matrix.Identity(4)
o.matrix_world=Matrix.Identity(4)
bpy.ops.wm.save_as_mainfile(filepath=str(out/(a.entity+'.blend')));export_fbx(hge,out/(a.entity+'.fbx'))
report={'entity':a.entity,'author_edge_matches':matched,'author_hard_edges':marked,'source_hard_edges':len(sharp),'surface_uv_exact':True,'custom_normals':False,'issues':issues}
(out/'authored-edges.json').write_text(json.dumps(report,indent=2));print(json.dumps(report))
