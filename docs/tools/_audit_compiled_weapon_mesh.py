"""Blender compare source entity-local geometry to decoded compiled HGM JSON.
--blend <blend> --entity <id> --decoded <json> --report <json>.
Checks face count, vertex/triangle-centroid displacement; catches index corruption
missed by a successful AssetsProcessor run. Does not test materials or runtime.
"""
import argparse,json,sys
from pathlib import Path
import bpy
from mathutils import Vector
from mathutils.kdtree import KDTree
p=argparse.ArgumentParser()
for n in ('blend','decoded','report'):p.add_argument('--'+n,type=Path,required=True)
p.add_argument('--entity',required=True)
p.add_argument('--check-winding',action='store_true',help='Require orientation consistency after JA3 coordinate conversion')
a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
bpy.ops.wm.open_mainfile(filepath=str(a.blend));mesh=bpy.data.objects[a.entity].data
mesh.calc_loop_triangles()
expected=[Vector(v.co) for v in mesh.vertices]
centres=[sum((expected[i] for i in f.vertices),Vector())/3 for f in mesh.loop_triangles]
normals=[(expected[f.vertices[1]]-expected[f.vertices[0]]).cross(expected[f.vertices[2]]-expected[f.vertices[0]]).normalized() for f in mesh.loop_triangles]
def tree(points):
    t=KDTree(len(points))
    for i,pt in enumerate(points):t.insert(pt,i)
    t.balance();return t
vt,ft=tree(expected),tree(centres)
d=json.loads(a.decoded.read_text());max_vertex=max_face=0;count=0;actual_centres=[];positive_area=negative_area=0
for sub in d['meshes']:
    b=sub.get('bbox') or d['bbox'];c=[(b[i]+b[i+3])/2 for i in range(3)]
    points=[Vector((-(v[1]+c[1]),-(v[0]+c[0]),v[2]+c[2])) for v in sub['vertices']]
    max_vertex=max(max_vertex,max(vt.find(v)[2] for v in points))
    cs=[sum((points[i] for i in f),Vector())/3 for f in sub['faces']]
    for f,center in zip(sub['faces'],cs):
        cross=(points[f[1]]-points[f[0]]).cross(points[f[2]]-points[f[0]])
        dot=cross.dot(normals[ft.find(center)[1]])
        if dot>=0:positive_area+=cross.length
        else:negative_area+=cross.length
    max_face=max(max_face,max(ft.find(v)[2] for v in cs));count+=len(cs);actual_centres+=cs
reverse=tree(actual_centres)
max_missing=max(reverse.find(v)[2] for v in centres)
report={'entity':a.entity,'source_triangles':len(centres),'compiled_triangles':count,
 'vertex_max_m':max_vertex,'triangle_max_m':max_face,'missing_triangle_max_m':max_missing,
 'pass':count==len(centres) and max(max_vertex,max_face,max_missing)<.0001}
report['winding_positive_area_fraction']=positive_area/max(positive_area+negative_area,1e-20)
if a.check_winding:
    # The position mapping above has determinant -1; native index winding is
    # opposite to Blender after that reflection (JA3 clockwise front faces).
    report['pass']=report['pass'] and report['winding_positive_area_fraction']<.001
a.report.write_text(json.dumps(report,indent=2));print(json.dumps(report))
assert report['pass'],'Compiled geometry differs from the prepared source'
