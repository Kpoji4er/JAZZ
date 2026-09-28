"""Blender read-only module/island bounds: --blend FILE --output JSON."""
import argparse,json,sys
from pathlib import Path
import bpy,bmesh
p=argparse.ArgumentParser();p.add_argument('--blend');p.add_argument('--output')
a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);bpy.ops.wm.open_mainfile(filepath=a.blend)
result=[]
for o in bpy.data.objects:
 if o.type!='MESH':continue
 bm=bmesh.new();bm.from_mesh(o.data)
 bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=.000001)
 seen=set();parts=[]
 for seed in bm.verts:
  if seed in seen:continue
  todo=[seed];seen.add(seed);verts=[]
  while todo:
   v=todo.pop();verts.append(v)
   for e in v.link_edges:
    q=e.other_vert(v)
    if q not in seen:seen.add(q);todo.append(q)
  pts=[v.co for v in verts]
  parts.append({'n':len(verts),'lo':[round(min(v[i] for v in pts),5) for i in range(3)],'hi':[round(max(v[i] for v in pts),5) for i in range(3)]})
 result.append({'name':o.name,'location':list(o.location),'parent':o.parent.name if o.parent else None,'spots':[(c.name,c.hge_obj_settings.spot_name,list(c.location)) for c in o.children if c.type=='EMPTY'],'parts':parts})
 bm.free()
Path(a.output).write_text(json.dumps(result,indent=2))
