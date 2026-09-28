"""Recover MkIII donor scope from its packed UV tile, in current host coordinates.
Blender --source original.blend --output DIR --game-root DIR. Reuses installed atlas.
"""
import argparse,sys,json
from pathlib import Path
import bpy,bmesh
from mathutils import Vector,Matrix
sys.path.insert(0,str(Path(__file__).resolve().parent))
from _export_m14_family_assets import load_hge,finalise,export_fbx
from _prepare_weapon_open_surfaces import prepare_export_mesh
p=argparse.ArgumentParser()
for key in ('source','output','game-root'):p.add_argument('--'+key,type=Path,required=True)
a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);hge=load_hge(a.game_root)
bpy.ops.wm.open_mainfile(filepath=str(a.source),use_scripts=False);o=bpy.data.objects['JAZZ_M14_MkIII']
o.parent=None;o.matrix_world=Matrix.Identity(4);mesh=o.data;uv=mesh.uv_layers.active.data
bodyfaces=[];scopefaces=[]
for f in mesh.polygons:
 avg=sum((uv[i].uv for i in f.loop_indices),Vector((0,0)))/len(f.loop_indices)
 if avg.x<.5 and avg.y<.5:bodyfaces.append(f)
 if avg.x>=.5 and avg.y<.5:scopefaces.append(f.index)
vs=[mesh.vertices[i] for f in bodyfaces for i in f.vertices]
midx=(min(v.co.x for v in vs)+max(v.co.x for v in vs))/2
factor=1.12/(max(v.co.y for v in vs)-min(v.co.y for v in vs))
bm=bmesh.new();bm.from_mesh(mesh);bm.faces.ensure_lookup_table();ids=set(scopefaces)
bmesh.ops.delete(bm,geom=[f for f in bm.faces if f.index not in ids],context='FACES')
bmesh.ops.delete(bm,geom=[v for v in bm.verts if not v.link_faces],context='VERTS');bm.to_mesh(mesh);bm.free()
for v in mesh.vertices:v.co=Vector((v.co.x-midx,v.co.y+.070,v.co.z+.010))*factor-Vector((0,-.18,.115))
for other in list(bpy.data.objects):
 if other!=o:bpy.data.objects.remove(other,do_unlink=True)
for im in bpy.data.images:
 if im.filepath:im.filepath=bpy.path.abspath(im.filepath)
mat=mesh.materials[0]
for prop in hge.MATERIAL_PROPERTIES:
 if prop.map and isinstance(mat.get(prop.id),str) and mat[prop.id].startswith('//'):mat[prop.id]=bpy.path.abspath(mat[prop.id])
name='JAZZ_M14_MkIII_Scope';finalise(o,name,mat);assert not prepare_export_mesh(o)
out=a.output/name;out.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=str(out/(name+'.blend')));export_fbx(hge,out/(name+'.fbx'))
(out/'repair.json').write_text(json.dumps({'scope_faces':len(scopefaces),'scale':factor,'shared_material':'JAZZ_M14_MkIII_Mesh.mtl','spot':[.18,0,.115]}))
