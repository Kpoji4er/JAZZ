"""Blender --before BLEND --after BLEND --report JSON: surface/UV preservation.
Ignores vertex indexing and triangle winding, compares triangle corner position
and UV pairs. Position tolerance 10 micrometres, UV tolerance 1e-6.
"""
import argparse,json,sys
from collections import Counter
from pathlib import Path
import bpy
p=argparse.ArgumentParser()
for k in ['before','after','report']:p.add_argument('--'+k,type=Path,required=True)
p.add_argument('--allow-submicron-slivers',action='store_true',help='Allow <10 removed faces only when area<1e-8 m2 and area/longest-edge^2<1e-4')
a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
def snapshot(path):
 bpy.ops.wm.open_mainfile(filepath=str(path));result={}
 for o in bpy.data.objects:
  if o.type!='MESH' or not o.name.startswith(('JAZZ_VZ58','JAZZ_VektorR4')):continue
  m=o.data;m.calc_loop_triangles();uv=m.uv_layers.active.data;triangles=[];slivers=[]
  for t in m.loop_triangles:
   corners=[]
   for vi,li in zip(t.vertices,t.loops):
    co=m.vertices[vi].co;corners.append(tuple(round(x,5) for x in co)+tuple(round(x,6) for x in uv[li].uv))
   key=tuple(sorted(corners));triangles.append(key)
   points=[m.vertices[i].co for i in t.vertices]
   area=(points[1]-points[0]).cross(points[2]-points[0]).length/2
   longest=max((points[i]-points[(i+1)%3]).length for i in range(3))
   if longest and area<1e-8 and area/longest**2<1e-4:slivers.append(key)
  result[o.name]=(Counter(triangles),Counter(slivers))
 return result
before=snapshot(a.before);after=snapshot(a.after);report={}
for name,(triangles,slivers) in before.items():
 assert name in after,name
 missing_counter=triangles-after[name][0]
 missing=sum(missing_counter.values());added=sum((after[name][0]-triangles).values())
 allowed=missing if a.allow_submicron_slivers and missing<10 and not missing_counter-slivers else 0
 report[name]={'before':sum(triangles.values()),'after':sum(after[name][0].values()),'missing':missing,'added':added,'allowed_submicron_slivers':allowed}
a.report.write_text(json.dumps(report,indent=2));print(json.dumps(report))
assert all(v['missing']==v['allowed_submicron_slivers'] and v['added']==0 for v in report.values()),'Surface/UV changed'
