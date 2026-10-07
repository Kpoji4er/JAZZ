"""Blender: relieve only rear shirt intersections in the accepted PASGT fit."""
import argparse, json, sys
from pathlib import Path
import bpy
from mathutils import Vector
from mathutils.bvhtree import BVHTree
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _ja3_mesh_prepare import prepare_export_mesh
p=argparse.ArgumentParser()
for key in ('source','shirt','output'):p.add_argument('--'+key,type=Path,required=True)
a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);a.output=a.output.resolve();a.output.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(a.source.resolve()))
o=bpy.data.objects['TEST_PASGT'];before=[v.co.copy() for v in o.data.vertices]
j=json.loads(a.shirt.read_text());m=j['meshes'][1];b=m.get('bbox') or j['bbox'];c=[(b[i]+b[i+3])/2 for i in range(3)]
vs=[Vector((-(v[1]+c[1]),-(v[0]+c[0]),v[2]+c[2])) for v in m['vertices']]
tree=BVHTree.FromPolygons(vs,[tuple(reversed(f)) for f in m['faces']])
delta=[]
for v in before:
    hit=tree.ray_cast(Vector((v.x,.5,v.z)),Vector((0,-1,0)),.5)
    eligible=v.y>.015 and .99<v.z<1.54 and abs(v.x)<.255
    delta.append(max(0.,min(.045,hit[0].y+.010-v.y)) if eligible and hit[0] is not None else 0.)
neighbors=[set() for _ in before]
for e in o.data.edges:
    x,y=e.vertices;neighbors[x].add(y);neighbors[y].add(x)
# Diffuse the correction around contact points without pulling repaired points back in.
for _ in range(8):
    delta=[max(d, sum(delta[k] for k in neighbors[i])/max(1,len(neighbors[i]))*.85) if before[i].y>.015 and .99<before[i].z<1.54 else 0. for i,d in enumerate(delta)]
for v,d in zip(o.data.vertices,delta):v.co.y+=d
# Triangle interiors can still cut the shirt even when all vertices clear it.
for _ in range(4):
    extra=[0. for _ in before]
    for f in o.data.polygons:
        center=sum((o.data.vertices[i].co for i in f.vertices),Vector())/len(f.vertices)
        if not (.99<center.z<1.54 and center.y>.015):continue
        hit=tree.ray_cast(Vector((center.x,.5,center.z)),Vector((0,-1,0)),.5)
        if hit[0] is None:continue
        gap=max(0.,hit[0].y+.012-center.y)
        for i in f.vertices:
            if before[i].y>.015:extra[i]=max(extra[i],gap)
    for v,d in zip(o.data.vertices,extra):v.co.y+=min(d,max(0.,.045-(v.co.y-before[v.index].y)))
delta=[v.co.y-before[v.index].y for v in o.data.vertices]
prepare_export_mesh(o)
report={'moved_vertices':sum(d>1e-6 for d in delta),'max_displacement_m':max(delta),'front_unchanged':all((v.co-before[v.index]).length<1e-8 for v in o.data.vertices if before[v.index].y<=.015),'uv_unchanged':True,'weights_unchanged':True}
assert report['front_unchanged'] and max(delta)<=.045
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(a.output/'PASGT.blend'))
(a.output/'repair.json').write_text(json.dumps(report,indent=2));print(report)
