"""Blender: restore audited author winding, weld UV seams, prepare/export scope.
--blend PATH --audit JSON --output DIR --game-root DIR. Never installs assets.
"""
import argparse,json,sys
from pathlib import Path
import bpy,bmesh
sys.path.insert(0,str(Path(__file__).resolve().parent))
from _export_m14_family_assets import load_hge,export_fbx
from _prepare_weapon_open_surfaces import prepare_export_mesh
p=argparse.ArgumentParser()
for k in ('blend','audit','output','game-root'):p.add_argument('--'+k,type=Path,required=True)
a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
r=json.loads(a.audit.read_text());assert not r['source_unmatched'] and not r['target_unmatched']
assert r['max_centroid_error_m']<1e-6
hge=load_hge(a.game_root);bpy.ops.wm.open_mainfile(filepath=str(a.blend),use_scripts=False)
o=bpy.data.objects['JAZZ_M14_MkIII_Scope'];me=o.data
assert len(me.polygons)==r['target_triangles'] and all(len(f.vertices)==3 for f in me.polygons)
def uv_signature():
 uv=me.uv_layers.active.data
 return sorted(tuple(sorted(tuple(round(x,7) for x in (*me.vertices[me.loops[i].vertex_index].co,*uv[i].uv)) for i in f.loop_indices)) for f in me.polygons)
before=uv_signature()
bm=bmesh.new();bm.from_mesh(me);bm.faces.ensure_lookup_table()
bmesh.ops.reverse_faces(bm,faces=[bm.faces[i] for i in r['reversed_faces']])
bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-7)
bm.to_mesh(me);bm.free();me.update()
assert not prepare_export_mesh(o)
assert uv_signature()==before,'Position/UV/triangle change'
for im in bpy.data.images:
 if im.filepath:im.filepath=bpy.path.abspath(im.filepath)
for mat in me.materials:
 for prop in hge.MATERIAL_PROPERTIES:
  if prop.map and isinstance(mat.get(prop.id),str) and mat[prop.id].startswith('//'):mat[prop.id]=bpy.path.abspath(mat[prop.id])
a.output.mkdir(parents=True,exist_ok=False)
bpy.ops.wm.save_as_mainfile(filepath=str(a.output/(o.name+'.blend')))
export_fbx(hge,a.output/(o.name+'.fbx'))
print('PASS: source winding restored, UV/positions/triangles unchanged, no custom normals')
