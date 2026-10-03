"""Transfer the accepted cuirass torso/strap skin field to a Meshy vest.
Blender -- --source BLEND --reference BLEND --output DIR --item NAME.
Preserves topology, UVs and materials. Stages a candidate, never installs it.
"""
import argparse,json,sys,math
from pathlib import Path
import bpy
from mathutils import Vector
from mathutils.bvhtree import BVHTree
from mathutils.geometry import barycentric_transform
sys.path.insert(0,str(Path(__file__).resolve().parent))
from _ja3_mesh_prepare import prepare_export_mesh
p=argparse.ArgumentParser()
for n in ('source','reference','output'):p.add_argument('--'+n,required=True,type=Path)
p.add_argument('--item',required=True,choices=['TireBrigantine','LeatherArmor','6B3'])
p.add_argument('--shirt',required=True,type=Path,help='Decoded native Shirt08 for shoulder clearance')
a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);a.output.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(a.source.resolve()))
obj=next(o for o in bpy.data.objects if o.name.startswith('TEST_'));rig=next(o for o in bpy.data.objects if o.type=='ARMATURE')
with bpy.data.libraries.load(str(a.reference.resolve()),link=False) as (src,dst):dst.objects=['TEST_ImprovisedCuirass_Male_v7']
ref=dst.objects[0];assert ref
ref.data.calc_loop_triangles();vs=[ref.matrix_world@v.co for v in ref.data.vertices];fs=[tuple(t.vertices) for t in ref.data.loop_triangles]
bvh=BVHTree.FromPolygons(vs,fs,all_triangles=True)
def field(q):
 hit,_,i,_=bvh.find_nearest(q);ids=fs[i]
 bary=barycentric_transform(hit,*[vs[k] for k in ids],Vector((1,0,0)),Vector((0,1,0)),Vector((0,0,1)))
 w={}
 for k,t in zip(ids,bary):
  for g in ref.data.vertices[k].groups:
   n=ref.vertex_groups[g.group].name
   if t>0:w[n]=w.get(n,0)+t*g.weight
 return w
# Evaluate a continuous spatial field, avoiding jumps between nearby rivets.
cache={}
def spatial_bind(q):
 cell=.035;s=[v/cell for v in q];lo=[math.floor(v) for v in s];fraction=[s[i]-lo[i] for i in range(3)];w={}
 for x in (0,1):
  for y in (0,1):
   for z in (0,1):
    corner=(x,y,z);key=tuple(lo[i]+corner[i] for i in range(3))
    if key not in cache:cache[key]=field(Vector(tuple(k*cell for k in key)))
    factor=math.prod(fraction[i] if corner[i] else 1-fraction[i] for i in range(3))
    for n,value in cache[key].items():w[n]=w.get(n,0)+factor*value
 w=dict(sorted(w.items(),key=lambda row:-row[1])[:4]);total=sum(w.values())
 return {n:v/total for n,v in w.items() if v>1e-7}
def bind(q):
 # Plate centres exclude shoulder hardware when sampling the torso. Blend into
 # actual strap weights only at the shoulder, as the source cuirass does.
 front=spatial_bind(Vector((0,-.20,q.z)));back=spatial_bind(Vector((0,.20,q.z)))
 side=max(0,min(1,(q.y+.10)/.20));side=side*side*(3-2*side)
 torso={n:front.get(n,0)*(1-side)+back.get(n,0)*side for n in front.keys()|back.keys()}
 shoulder=spatial_bind(q);t=max(0,min(1,(q.z-1.34)/.12));t=t*t*(3-2*t)
 w={n:torso.get(n,0)*(1-t)+shoulder.get(n,0)*t for n in torso.keys()|shoulder.keys()}
 w=dict(sorted(w.items(),key=lambda row:-row[1])[:4]);total=sum(w.values())
 return {n:v/total for n,v in w.items() if v>1e-7}
native=json.loads(a.shirt.read_text());part=native['meshes'][1];box=part.get('bbox') or native['bbox'];center=[(box[i]+box[i+3])/2 for i in range(3)]
cloth=[Vector((-(v[1]+center[1]),-(v[0]+center[0]),v[2]+center[2])) for v in part['vertices']]
cloth_bvh=BVHTree.FromPolygons(cloth,[tuple(reversed(f)) for f in part['faces']],all_triangles=True)
before=[v.co.copy() for v in obj.data.vertices]
for v in obj.data.vertices:
 q=v.co;hit,normal,_,distance=cloth_bvh.find_nearest(q)
 clearance=(q-hit).dot(normal)
 if q.z>1.33 and clearance<.012:
  t=max(0,min(1,(q.z-1.33)/.04));t=t*t*(3-2*t)
  q+=normal*min(.055,.012-clearance)*t
 if a.item=='6B3' and q.y>.08 and q.z<1.44 and clearance>.045:
  q.y-=min(.025,clearance-.045)
 if a.item=='TireBrigantine' and q.y>.04 and q.z<1.16:
  # Native Shirt08's loose lower back protrudes through the short vest in a
  # forward lean. Add smooth clearance to the existing back panel, not bones.
  t=max(0,min(1,(1.16-q.z)/.10));t=t*t*(3-2*t)
  q.y+=.018*t
while obj.vertex_groups:obj.vertex_groups.remove(obj.vertex_groups[0])
for v in obj.data.vertices:
 for name,weight in bind(v.co).items():
  assert name in rig.data.bones
  (obj.vertex_groups.get(name) or obj.vertex_groups.new(name=name)).add([v.index],weight,'REPLACE')
max_shift=max((v.co-q).length for v,q in zip(obj.data.vertices,before))
prepare_export_mesh(obj)
bpy.data.objects.remove(ref,do_unlink=True)
bpy.ops.wm.save_as_mainfile(filepath=str((a.output/(a.item+'.blend')).resolve()))
(a.output/'rebind-report.json').write_text(json.dumps({'reference':'accepted cuirass v7','max_clearance_correction_m':max_shift,'uv_unchanged':True,'vertices':len(before),'max_influences':4,'runtime':'NOT_RUN'},indent=2),encoding='utf-8')
