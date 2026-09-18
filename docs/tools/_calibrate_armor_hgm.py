"""Calibrate extracted HGM against the same compiled cuirass's Blender source."""
import bpy,json,argparse,sys,itertools
from mathutils import Vector
from mathutils.kdtree import KDTree
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--hgm-json',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);bpy.ops.wm.open_mainfile(filepath=str(a.source))
o=next(o for o in bpy.data.objects if o.name.startswith('TEST_ImprovisedCuirass'));kd=KDTree(len(o.data.vertices))
for v in o.data.vertices:kd.insert(o.matrix_world@v.co,v.index)
kd.balance();data=json.loads(a.hgm_json.read_text());results=[]
for flip in (1,-1):
 points=[]
 for mesh in data['meshes']:
  b=mesh['bbox'] or data['bbox'];center=Vector([(b[i]+b[i+3])*.5 for i in range(3)])
  points.extend(Vector((v[0],v[1]*flip,v[2]))+center for v in mesh['vertices'][::7])
 for perm in itertools.permutations(range(3)):
  for signs in itertools.product((-1,1),repeat=3):
   distances=[kd.find(Vector([pt[perm[i]]*signs[i] for i in range(3)]))[2] for pt in points]
   results.append({'pre_y_sign':flip,'permutation':perm,'signs':signs,'mean_m':sum(distances)/len(distances),'max_m':max(distances)})
results.sort(key=lambda x:x['mean_m']);best=results[0]
assert best['max_m']<.003,best
a.output.write_text(json.dumps({'best':best,'source_vertices':len(o.data.vertices),'sample_count':len(points)},indent=2));print(best)
