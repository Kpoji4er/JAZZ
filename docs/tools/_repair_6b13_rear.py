"""Blender: patch the two lower-rear Meshy punctures in the fitted 6B13, preserving UV boundary data."""
import bpy,bmesh,argparse,sys,json
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
bpy.ops.wm.open_mainfile(filepath=str(a.source.resolve()));o=next(o for o in bpy.context.scene.objects if o.type=='MESH')
bm=bmesh.new();bm.from_mesh(o.data)
faces=[f for f in bm.faces if any(-.057<v.co.x<.028 and 1.038<v.co.z<1.062 and v.co.y>.06 for v in f.verts)]
assert 1<len(faces)<250,len(faces)
bmesh.ops.delete(bm,geom=faces,context='FACES')
bound=[e for e in bm.edges if e.is_boundary];assert len(bound)<180,len(bound)
uv=bm.loops.layers.uv.active
known={v:next(l[uv].uv.copy() for f in v.link_faces for l in f.loops if l.vert==v) for e in bound for v in e.verts}
filled=bmesh.ops.holes_fill(bm,edges=bound,sides=180)['faces']
for f in filled:
 for l in f.loops:l[uv].uv=known[l.vert]
 for v in f.verts:
  if v.co.y>.12:v.co.y=max(v.co.y,.144)
bmesh.ops.triangulate(bm,faces=filled)
bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free()
bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o
if o.data.has_custom_normals:bpy.ops.mesh.customdata_custom_splitnormals_clear()
for f in o.data.polygons:f.use_smooth=True
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(a.output.resolve()))
o.data.calc_loop_triangles();print(json.dumps({'removed_faces':len(faces),'filled_patches':len(filled),'triangles':len(o.data.loop_triangles)}))
