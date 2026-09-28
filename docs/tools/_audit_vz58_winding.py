"""Blender: compare prepared VZ58 face winding to authored donor normals.
--build DIR --output report.json; reads source OBJ and prepared blend, no writes to assets.
"""
import argparse,json,sys
from pathlib import Path
import bpy
from mathutils import Vector,Matrix
from mathutils.kdtree import KDTree
p=argparse.ArgumentParser();p.add_argument('--build',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--r4-source',type=Path);p.add_argument('--require-outward',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
S=.845/(42.41209411621094+42.3818244934082)
M=Matrix(((S,0,0,0),(0,0,-S,-15*S),(0,S,0,7*S),(0,0,0,1)))
if a.r4_source:
 import math
 raw=[float(l.split()[1]) for l in (a.r4_source/'model_0.obj').read_text().splitlines() if l.startswith('v ')]
 scale=1.005/(max(raw)-min(raw))
 M=Matrix.Rotation(math.pi/2,4,'Z')@Matrix.Scale(scale,4)@Matrix.Translation(Vector((-120,-4.5,12)))@Matrix.Rotation(math.pi/2,4,'X')
bpy.ops.wm.open_mainfile(filepath=str(a.build/('rigged/VektorR4_JA3.blend' if a.r4_source else 'rigged/VZ58_JA3.blend')))
result={}
parts=[('JAZZ_VZ58','classic',2,9.60988998413086),('JAZZ_VZ58_HandguardWood','classic',3,9.60988998413086),('JAZZ_VZ58_GripWood','classic',3,9.60988998413086),('JAZZ_VZ58_Magazine','modern',0,0),('JAZZ_VZ58_StockWood','classic',5,9.60988998413086),('JAZZ_VZ58_StockWire','classic',0,-20.50680923461914),('JAZZ_VZ58_StockModern','modern',5,0),('JAZZ_VZ58_GripModern','modern',5,0),('JAZZ_VZ58_Foregrip','modern',6,0),('JAZZ_VZ58_Reflex','modern',6,0),('JAZZ_VZ58_Suppressor','modern',7,0)]
if a.r4_source:parts=[('JAZZ_VektorR4','',0,0)]
for entity,family,index,shift in parts:
 vertices=[];normals=[];centres=[];expected=[]
 for line in ((a.r4_source if a.r4_source else a.build/'source'/family)/f'model_{index}.obj').read_text().splitlines():
  q=line.split()
  if not q:continue
  if q[0]=='v':
   v=Vector(tuple(map(float,q[1:4])));v.y+=shift;vertices.append(M@v)
  elif q[0]=='vn':normals.append((M.to_3x3()@Vector(tuple(map(float,q[1:4])))).normalized())
  elif q[0]=='f':
   ids=[list(map(int,t.split('/'))) for t in q[1:]];vs=[vertices[x[0]-1] for x in ids]
   if (vs[1]-vs[0]).cross(vs[2]-vs[0]).length<1e-12:continue
   centres.append(sum(vs,Vector())/3);expected.append(sum((normals[x[2]-1] for x in ids),Vector()).normalized())
 tree=KDTree(len(centres))
 for i,c in enumerate(centres):tree.insert(c,i)
 tree.balance();o=bpy.data.objects[entity];o.data.calc_loop_triangles();bad=0;area_bad=area_total=0
 for f in o.data.loop_triangles:
  vs=[o.matrix_world@o.data.vertices[i].co for i in f.vertices];center=sum(vs,Vector())/3;_,i,d=tree.find(center);assert d<1e-5,(entity,d)
  normal=(vs[1]-vs[0]).cross(vs[2]-vs[0]);area_total+=normal.length
  if normal.normalized().dot(expected[i])<-.2:bad+=1;area_bad+=normal.length
 result[entity]={'triangles':len(o.data.loop_triangles),'inverted':bad,'inverted_area_fraction':area_bad/area_total}
a.output.write_text(json.dumps(result,indent=2));print(json.dumps(result))

if a.require_outward:assert all(v['inverted_area_fraction']<.001 for v in result.values()),'Surface winding differs substantially from donor'
