"""Blender read-only connected-surface bounds for attachment/embedded-part QA.

--blend FILE --entity NAME (repeatable) --output JSON. Coincident positions
are joined in an analysis graph only; source geometry and UVs are not changed.
"""
import argparse,json,sys
from pathlib import Path
import bpy
p=argparse.ArgumentParser()
p.add_argument('--blend',required=True);p.add_argument('--entity',action='append',required=True);p.add_argument('--output',required=True)
a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
bpy.ops.wm.open_mainfile(filepath=a.blend,use_scripts=False)
report={}
for name in a.entity:
 o=bpy.data.objects[name];m=o.data;parent=list(range(len(m.vertices)));positions={}
 def root(i):
  while parent[i]!=i:parent[i]=parent[parent[i]];i=parent[i]
  return i
 for v in m.vertices:
  key=tuple(round(x,5) for x in v.co)
  if key in positions:parent[root(v.index)]=root(positions[key])
  else:positions[key]=v.index
 for f in m.polygons:
  for i in f.vertices[1:]:parent[root(i)]=root(f.vertices[0])
 groups={}
 for v in m.vertices:groups.setdefault(root(v.index),[]).append(v)
 rows=[]
 for vs in groups.values():
  ids={v.index for v in vs};fs=[f for f in m.polygons if f.vertices[0] in ids]
  rows.append(dict(vertices=len(vs),faces=len(fs),face_indices=[f.index for f in fs],
   min=[min(v.co[i] for v in vs) for i in range(3)],max=[max(v.co[i] for v in vs) for i in range(3)]))
 report[name]=dict(location=list(o.location),materials=[x.name for x in m.materials],islands=sorted(rows,key=lambda x:-x['faces']))
Path(a.output).write_text(json.dumps(report,indent=2))
