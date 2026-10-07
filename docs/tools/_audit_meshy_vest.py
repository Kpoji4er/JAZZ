"""Blender: read-only topology/UV/material audit for a Meshy GLB or fitted blend."""
import bpy,bmesh,json,argparse,sys
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--input',type=Path,required=True);p.add_argument('--report',type=Path,required=True);a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
if a.input.suffix=='.blend':bpy.ops.wm.open_mainfile(filepath=str(a.input.resolve()))
else:
 bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(a.input.resolve()))
rows=[]
for o in [o for o in bpy.context.scene.objects if o.type=='MESH']:
 me=o.data;me.calc_loop_triangles();bm=bmesh.new();bm.from_mesh(me);bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-6);bm.verts.ensure_lookup_table();seen=set();components=[]
 for v in bm.verts:
  if v in seen:continue
  todo=[v];seen.add(v);vs=[];fs=set()
  while todo:
   x=todo.pop();vs.append(x);fs.update(x.link_faces)
   for e in x.link_edges:
    y=e.other_vert(x)
    if y not in seen:seen.add(y);todo.append(y)
  components.append({'vertices':len(vs),'faces':len(fs)})
 rows.append({'name':o.name,'vertices':len(me.vertices),'triangles':len(me.loop_triangles),'welded_vertices':len(bm.verts),'components':sorted(components,key=lambda x:-x['faces']),'boundary_edges':sum(e.is_boundary for e in bm.edges),'nonmanifold_nonboundary':sum(not e.is_manifold and not e.is_boundary for e in bm.edges),'degenerate_faces':sum(f.calc_area()<1e-12 for f in bm.faces),'uv_layers':len(me.uv_layers),'custom_normals':me.has_custom_normals,'dimensions':list(o.dimensions),'materials':[m.name for m in me.materials]});bm.free()
a.report.parent.mkdir(parents=True,exist_ok=True);a.report.write_text(json.dumps(rows,indent=2));print(json.dumps(rows))
