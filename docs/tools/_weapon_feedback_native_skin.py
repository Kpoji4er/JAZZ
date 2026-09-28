"""Blender BVH: compute rear torso weights for installed HAV geometry (JSON).
--armor decoded.json --shirt native.json --output weights.json. No HGM writes.
"""
import argparse,json,sys
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
from mathutils.geometry import barycentric_transform
p=argparse.ArgumentParser()
for k in ('armor','shirt','output'):p.add_argument('--'+k,type=Path,required=True)
a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);d=json.loads(a.armor.read_text());s=json.loads(a.shirt.read_text());m=s['meshes'][1]
def coords(data,mesh):
 b=mesh.get('bbox') or data['bbox'];c=[(b[i]+b[i+3])/2 for i in range(3)]
 return [Vector((-(v[1]+c[1]),-(v[0]+c[0]),v[2]+c[2])) for v in mesh['vertices']]
vs=coords(s,m);faces=m['faces'];tree=BVHTree.FromPolygons(vs,faces,all_triangles=True);available={b['name'] for b in d['bones']}
native=[{s['bones'][i]['name']:w for i,w in zip(ids,ws) if w>0 and s['bones'][i]['name'] in available and s['bones'][i]['name']!='Bip001'} for ids,ws in zip(m['bone_indices'],m['bone_weights'])]
def fade(x):
 t=max(0,min(1,x));return t*t*(3-2*t)
out=[]
for mesh in d['meshes']:
 rows=[]
 for pos,ids,ws in zip(coords(d,mesh),mesh['bone_indices'],mesh['bone_weights']):
  blend=fade((pos.y+.015)/.035)*fade((pos.z-1.04)/.07)*(1-fade((abs(pos.x)-.18)/.08))
  if blend<=0:rows.append(None);continue
  old={d['bones'][i]['name']:w for i,w in zip(ids,ws) if w>0};direction=Vector((pos.x,pos.y+.018,0))
  q,_,_,_=tree.ray_cast(Vector((0,-.018,pos.z)),direction.normalized(),.6)
  if q is None:q=pos
  co,_,index,_=tree.find_nearest(q);vertices=faces[index]
  bary=barycentric_transform(co,*[vs[i] for i in vertices],Vector((1,0,0)),Vector((0,1,0)),Vector((0,0,1)));new={}
  for i,f in zip(vertices,bary):
   for n,w in native[i].items():new[n]=new.get(n,0)+max(0,f)*w
  total=sum(new.values());assert total>0;new={n:w/total for n,w in new.items()}
  mixed={n:old.get(n,0)*(1-blend)+new.get(n,0)*blend for n in old.keys()|new.keys()};mixed=dict(sorted(mixed.items(),key=lambda pair:-pair[1])[:4]);total=sum(mixed.values())
  rows.append({n:w/total for n,w in mixed.items() if w>1e-8})
 out.append(rows)
a.output.write_text(json.dumps(out))
