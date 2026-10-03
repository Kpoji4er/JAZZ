"""Blender: compare the installed scope build to its authored OBJ, by geometry.

--blend PATH --source OBJ --report JSON. Finds the rigid axis/scale conversion;
reports missing triangles and reversed winding without modifying either input.
"""
import argparse, itertools, json, sys
from pathlib import Path
import bpy
from mathutils import Vector, Matrix
from mathutils.kdtree import KDTree

p=argparse.ArgumentParser()
for key in ('blend','source','report'): p.add_argument('--'+key,type=Path,required=True)
a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
bpy.ops.wm.open_mainfile(filepath=str(a.blend),use_scripts=False)
target=next(o for o in bpy.data.objects if o.type=='MESH')
target.data.calc_loop_triangles()
tv=[v.co.copy() for v in target.data.vertices]
tf=[tuple(t.vertices) for t in target.data.loop_triangles]
def tree(vs):
 t=KDTree(len(vs))
 for i,v in enumerate(vs):t.insert(v,i)
 t.balance();return t
tt=tree(tv)
old=set(bpy.data.objects)
bpy.ops.wm.obj_import(filepath=str(a.source),forward_axis='NEGATIVE_Z',up_axis='Y')
objs=[o for o in bpy.data.objects if o not in old and o.type=='MESH']
assert len(objs)==1
src=objs[0];src.data.calc_loop_triangles()
sv=[src.matrix_world@v.co for v in src.data.vertices]
sf=[tuple(t.vertices) for t in src.data.loop_triangles]
def bounds(vs):
 return Vector([min(v[i] for v in vs) for i in range(3)]),Vector([max(v[i] for v in vs) for i in range(3)])
tmin,tmax=bounds(tv);smin,smax=bounds(sv)
scale=max(tmax-tmin)/max(smax-smin)
best=None
for perm in itertools.permutations(range(3)):
 for signs in itertools.product((-1,1),repeat=3):
  mat=Matrix([[signs[i] if j==perm[i] else 0 for j in range(3)] for i in range(3)])
  pts=[mat@v*scale for v in sv];mn,mx=bounds(pts);delta=(tmin+tmax-mn-mx)/2
  sample=[v+delta for v in pts[::max(1,len(pts)//150)]]
  err=max(tt.find(v)[2] for v in sample)
  if best is None or err<best[0]:best=(err,mat,delta)
err,mat,delta=best;pts=[mat@v*scale+delta for v in sv]
centres=[sum((pts[i] for i in f),Vector())/3 for f in sf];st=tree(centres)
norms=[(pts[f[1]]-pts[f[0]]).cross(pts[f[2]]-pts[f[0]]).normalized()*mat.determinant() for f in sf]
missing=[];reversed_faces=[];matched=set();max_error=0
for i,f in enumerate(tf):
 c=sum((tv[j] for j in f),Vector())/3
 _,idx,d=st.find(c);max_error=max(max_error,d)
 if d>1e-5:missing.append(i);continue
 matched.add(idx)
 n=(tv[f[1]]-tv[f[0]]).cross(tv[f[2]]-tv[f[0]]).normalized()
 if n.dot(norms[idx])<-.9:reversed_faces.append(i)
report={'source_triangles':len(sf),'target_triangles':len(tf),'scale':scale,'matrix':[list(r) for r in mat],
 'delta':list(delta),'vertex_sample_error_m':err,'max_centroid_error_m':max_error,
 'target_unmatched':missing,'source_unmatched':sorted(set(range(len(sf)))-matched),'reversed_faces':reversed_faces}
a.report.parent.mkdir(parents=True,exist_ok=True);a.report.write_text(json.dumps(report,indent=2))
print(json.dumps({k:len(v) if isinstance(v,list) and k.endswith(('faces','unmatched')) else v for k,v in report.items()}))
