"""Blender -- --blend FILE --references DIR --output JSON.
Read-only comparison to P3DM authored normals. Never creates custom normal layers.
Checks the current export mesh against source directions, not against itself.
"""
import argparse, itertools, json, sys
from pathlib import Path
import bpy
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent))
from _read_hk416_mlod import read
p=argparse.ArgumentParser()
for k in ('blend','references','output'):p.add_argument('--'+k,type=Path,required=True)
a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
bpy.ops.wm.open_mainfile(filepath=str(a.blend),use_scripts=False)
def key(points):return tuple(sorted(tuple(round(float(c),5) for c in v) for v in points))
result=[]
for suffix,source in [('Short','416D10'),('Standard','416D145'),('Long','416D20'),('Stock','416D145'),('StockCTR','416D10_ST6')]:
 r=read(a.references/(source+'.p3d'),audit_normals=True);expected={}
 for f in r['faces']:
  pts=[Vector((-r['vertices'][i][2],r['vertices'][i][0]-.06,r['vertices'][i][1]+.04)) for i in f['vertices']]
  normal=sum((Vector((-v[2],v[0],v[1])) for v in f['audit_normals']),Vector()).normalized()
  for ids in itertools.combinations(range(len(pts)),3):expected[key([pts[i] for i in ids])]=normal
 obj=bpy.data.objects['JAZZ_HK416_'+suffix];mesh=obj.data;mesh.calc_loop_triangles()
 row={'entity':obj.name,'matched':0,'unmatched':0,'opposed':0,'examples':[]}
 for face in mesh.loop_triangles:
  pts=[obj.matrix_world@mesh.vertices[i].co for i in face.vertices];ref=expected.get(key(pts))
  if ref is None:row['unmatched']+=1;continue
  row['matched']+=1;dot=face.normal.dot(ref)
  if dot<-.1:
   row['opposed']+=1
   if len(row['examples'])<12:row['examples'].append({'triangle':face.polygon_index,'dot':dot,'center':list(sum(pts,Vector())/3)})
 result.append(row)
a.output.write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
