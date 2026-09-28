"""Recalculate weapon normals; keep the authored side of open surface islands.

Requires coincident UV seam positions to have been joined by the caller. Closed
shells use Blender outward recalculation. A plane has no inside/outside: select
its side by an area-weighted vote against its source triangle winding. Never
write custom/split normals or move vertices.
"""
from _ja3_mesh_prepare import prepare_export_mesh as _prepare

def prepare_export_mesh(obj, **kwargs):
 import bmesh
 from mathutils.kdtree import KDTree
 from mathutils import Vector
 mesh=obj.data;mesh.calc_loop_triangles();reference=[]
 for f in mesh.loop_triangles:
  a,b,c=(mesh.vertices[i].co.copy() for i in f.vertices)
  reference.append(((a+b+c)/3,(b-a).cross(c-a)))
 tree=KDTree(len(reference))
 for i,(center,_) in enumerate(reference):tree.insert(center,i)
 tree.balance();issues=_prepare(obj,**kwargs)
 bm=bmesh.new();bm.from_mesh(mesh);bm.normal_update();pending=set(bm.faces)
 while pending:
  seed=pending.pop();group={seed};todo=[seed]
  while todo:
   f=todo.pop()
   for e in f.edges:
    for other in e.link_faces:
     if other in pending:pending.remove(other);group.add(other);todo.append(other)
  if not any(e.is_boundary for f in group for e in f.edges):continue
  vote=0
  for f in group:
   _,i,d=tree.find(f.calc_center_median());assert d<1e-6,'Normal preparation moved a face'
   vote+=f.normal.dot(reference[i][1])
  if vote<0:bmesh.ops.reverse_faces(bm,faces=list(group))
 bm.normal_update();bm.to_mesh(mesh);bm.free();mesh.update()
 assert not mesh.has_custom_normals
 return issues
