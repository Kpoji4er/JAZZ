"""Blender --blend FILE --entity ID --output DIR --game-root DIR.
Narrow 0.5 mm mechanical edge bevels; retain authored planar shading without
custom normals. Candidate only; UVs inherited, installed DDS never modified.
"""
import argparse,json,sys,math
from pathlib import Path
import bpy,bmesh
sys.path.insert(0,str(Path(__file__).resolve().parent))
from _export_m14_family_assets import load_hge,export_fbx
from _prepare_weapon_open_surfaces import prepare_export_mesh
p=argparse.ArgumentParser()
for key in ('blend','entity','output','game-root'):p.add_argument('--'+key,required=True)
a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);out=Path(a.output);out.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=a.blend,use_scripts=False);hge=load_hge(Path(a.game_root));o=bpy.data.objects[a.entity];m=o.data
flat=[all(m.corner_normals[i].vector.dot(f.normal)>.9999 for i in f.loop_indices) for f in m.polygons]
bm=bmesh.new();bm.from_mesh(m);bm.faces.ensure_lookup_table();layer=bm.faces.layers.int.new('author_planar')
bevel_tag=bm.faces.layers.int.new('generated_bevel')
for f,flag in zip(bm.faces,flat):f[layer]=int(flag)
before=len(bm.faces);bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-7);bm.normal_update()
edges=[e for e in bm.edges if len(e.link_faces)==2 and .52<e.calc_face_angle()<2.6 and max(f.calc_area() for f in e.link_faces)>5e-5 and e.calc_length()>.003]
result=bmesh.ops.bevel(bm,geom=edges,offset=.0005,segments=2,affect='EDGES',clamp_overlap=True,profile=.5)
for f in result['faces']:f[layer]=0;f[bevel_tag]=1
bmesh.ops.triangulate(bm,faces=list(bm.faces))
slivers=[f for f in bm.faces if f.calc_area()<1e-9 or (f.calc_area()<1e-8 and f.calc_area()/max(max(e.calc_length() for e in f.edges)**2,1e-20)<1e-4)]
print('Submicron bevel slivers:',len(slivers),'area',sum(f.calc_area() for f in slivers))
assert len(slivers)<200 and sum(f.calc_area() for f in slivers)<1e-7
bmesh.ops.delete(bm,geom=slivers,context='FACES')
bm.to_mesh(m);bm.free();issues=prepare_export_mesh(o,strict=False)
bad={i['triangle'] for i in issues if i['kind'] in ('degenerate','zero_normal')}
assert len(bad)<100,issues
if bad:
 bm=bmesh.new();bm.from_mesh(m);bm.faces.ensure_lookup_table();faces=[bm.faces[i] for i in bad]
 assert all(f.calc_area()<1e-8 for f in faces)
 assert sum(f.calc_area() for f in faces)<1e-7
 bmesh.ops.delete(bm,geom=faces,context='FACES');bm.to_mesh(m);bm.free()
issues=prepare_export_mesh(o)
bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o
split=o.modifiers.new('Remaining hard and opposing joins','EDGE_SPLIT');split.split_angle=math.radians(60);split.use_edge_angle=True;split.use_edge_sharp=False
bpy.ops.object.modifier_apply(modifier=split.name)
# The preparation helper intentionally smooths all polygons; restore only
# proven planar source faces. New narrow bevel strips remain smooth.
bm=bmesh.new();bm.from_mesh(m);layer=bm.faces.layers.int.get('author_planar');assert layer
boundaries=[e for e in bm.edges if len(e.link_faces)==2 and bool(e.link_faces[0][layer])!=bool(e.link_faces[1][layer])]
bmesh.ops.split_edges(bm,edges=boundaries);bm.to_mesh(m);bm.free()
for f in m.polygons:f.use_smooth=True
# Collapsed UVs on a newly generated strip produce undefined tangent vectors in
# the native importer. Project only those new strips around inherited UV centre.
uv=m.uv_layers.active.data;generated=m.attributes['generated_bevel'];fixed_uv=0
for f,flag in zip(m.polygons,generated.data):
 loops=list(f.loop_indices);u,v,w=(uv[i].uv.copy() for i in loops)
 area=abs((v.x-u.x)*(w.y-u.y)-(v.y-u.y)*(w.x-u.x))
 if area>=1e-10:continue
 points=[m.vertices[i].co.copy() for i in f.vertices];origin=sum(points,points[0]*0)/3
 axis=(points[1]-points[0]).normalized();other=f.normal.cross(axis).normalized();center=(u+v+w)/3
 for index,point in zip(loops,points):uv[index].uv=center+type(center)(((point-origin).dot(axis)*5,(point-origin).dot(other)*5))
 fixed_uv+=1
print('Reprojected generated bevel UV triangles:',fixed_uv)
assert not m.has_custom_normals
for im in bpy.data.images:
 if im.filepath:im.filepath=bpy.path.abspath(im.filepath)
for mat in m.materials:
 for prop in hge.MATERIAL_PROPERTIES:
  if prop.map and isinstance(mat.get(prop.id),str) and mat[prop.id].startswith('//'):mat[prop.id]=bpy.path.abspath(mat[prop.id])
bpy.ops.wm.save_as_mainfile(filepath=str(out/(a.entity+'.blend')));export_fbx(hge,out/(a.entity+'.fbx'))
(out/'bevel-report.json').write_text(json.dumps({'entity':a.entity,'selected_edges':len(edges),'bevel_width_m':.0005,'source_faces':before,'final_triangles':len(m.polygons),'custom_normals':False,'issues':issues},indent=2))
