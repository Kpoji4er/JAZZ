"""Rebind fitted HAV using cuirass-style torso transitions and sample shoulders.
Run in Blender with --source fitted.blend --output folder. No game mutation.
"""
import argparse,json,sys,math,hashlib
from pathlib import Path
import bpy
from mathutils import Vector
from mathutils.bvhtree import BVHTree
from mathutils.geometry import barycentric_transform
from mathutils.kdtree import KDTree
p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);a.output.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(a.source));bpy.context.view_layer.update()
armor=next(o for o in bpy.data.objects if o.name.startswith('TEST_') and o.type=='MESH');rig=next(o for o in bpy.data.objects if o.type=='ARMATURE');body=bpy.data.objects['M_BaseMesh Skin_BIP']
rigid_limb={v.index:{armor.vertex_groups[g.group].name:g.weight for g in v.groups} for v in armor.data.vertices if v.groups and all('arm' in armor.vertex_groups[g.group].name.lower() for g in v.groups)}
body.data.calc_loop_triangles();vertices=[body.matrix_world@v.co for v in body.data.vertices];faces=[tuple(t.vertices) for t in body.data.loop_triangles];surface=BVHTree.FromPolygons(vertices,faces,all_triangles=True)
def normalize(w):
 w=dict(sorted(((n,x) for n,x in w.items() if x>1e-7),key=lambda t:t[1],reverse=True)[:4]);total=sum(w.values());assert total>0
 return {n:x/total for n,x in w.items()}
def sample(pos):
 q,_,idx,_=surface.find_nearest(pos);ids=faces[idx];b=barycentric_transform(q,*[vertices[i] for i in ids],Vector((1,0,0)),Vector((0,1,0)),Vector((0,0,1)));w={}
 for i,f in zip(ids,b):
  if f<=0:continue
  for g in body.data.vertices[i].groups:
   n=body.vertex_groups[g.group].name
   # Imported twist helpers have independent animation tracks. Use the main
   # limb chains for rigid protective panels, retaining the elbow transition.
   if 'UpArmTwist' in n:n=n.split('UpArmTwist')[0].rstrip()+' UpperArm'
   elif 'ForeTwist' in n:n=n.split('ForeTwist')[0]+'Forearm'
   if n in rig.data.bones:w[n]=w.get(n,0)+f*g.weight
 return normalize(w)
def mix(a,b,t):return normalize({n:a.get(n,0)*(1-t)+b.get(n,0)*t for n in a.keys()|b.keys()})
def clamp(x):return max(0,min(1,x))
def torso_sample(p):
 w={n:x for n,x in sample(p).items() if 'Spine' in n or 'Pelvis' in n}
 return normalize(w) if w else {'Bip001 Spine2':1}
for v in armor.data.vertices:
 p=v.co
 # Local silhouette adjustment, leaving the fitted chest/waist envelope intact.
 if p.z>1.49:p.z=1.49+(p.z-1.49)*.72
 shoulder=clamp((p.z-1.40)/.09)*clamp((abs(p.x)-.14)/.08)
 p.x*=1-.07*shoulder;p.y*=1-.10*shoulder
def binding(p):
 if p.z<1.18:front={'Bip001 Spine':1-clamp((p.z-1.04)/.14),'Bip001 Spine1':clamp((p.z-1.04)/.14)}
 else:front={'Bip001 Spine1':1-clamp((p.z-1.18)/.16),'Bip001 Spine2':clamp((p.z-1.18)/.16)}
 if p.z<=1.15:back={'Bip001 Spine1':1}
 elif p.z<1.24:back=mix({'Bip001 Spine1':1},torso_sample(Vector((p.x,p.y,1.24))),clamp((p.z-1.15)/.09))
 else:back=torso_sample(p)
 torso=mix(front,back,clamp((p.y+.055)/.11))
 # Continuous shoulders/neck; no single-bone island assignment.
 blend=clamp((p.z-1.40)/.12)
 return mix(torso,sample(p),blend)
fields=[binding(v.co) for v in armor.data.vertices]
tree=KDTree(len(fields))
for v in armor.data.vertices:tree.insert(v.co,v.index)
tree.balance()
# Smooth only spatially close samples, preserving continuity across panel seams.
for _ in range(5):
 new=[]
 for v in armor.data.vertices:
  w={}
  for _,index,d in tree.find_range(v.co,.035):
   factor=math.exp(-(d/.022)**2)
   for name,x in fields[index].items():w[name]=w.get(name,0)+factor*x
  new.append(normalize(w))
 fields=new
armor.vertex_groups.clear();groups={}
for v,weights in zip(armor.data.vertices,fields):
 weights=rigid_limb.get(v.index,weights)
 for name,w in weights.items():
  if name not in groups:groups[name]=armor.vertex_groups.new(name=name)
  groups[name].add([v.index],w,'REPLACE')
bpy.ops.wm.save_as_mainfile(filepath=str(a.output/'model.blend'))
skin={'weights':[[[armor.vertex_groups[g.group].name,g.weight] for g in sorted(v.groups,key=lambda g:armor.vertex_groups[g.group].name)] for v in armor.data.vertices],
      'bones':[(b.name,b.parent.name if b.parent else None,list(map(list,b.matrix_local))) for b in rig.data.bones],
      'topology':[list(p.vertices) for p in armor.data.polygons],
      'transforms':[list(map(list,o.matrix_world)) for o in (armor,rig)]}
(a.output/'model.json').write_text(json.dumps({'geometry_sha256':hashlib.sha256(b''.join(float(x).hex().encode() for v in armor.data.vertices for x in v.co)).hexdigest(),'skin_sha256':hashlib.sha256(json.dumps(skin,sort_keys=True).encode()).hexdigest(),'runtime':'NOT_RUN'},indent=2))
fit_path=a.source.parent/'fit.json'
if fit_path.exists():
 import numpy as np
 shirt=bpy.data.objects['QA actual LegionGoon shirt'];shirt.data.calc_loop_triangles();armor.data.calc_loop_triangles()
 ref=BVHTree.FromPolygons([v.co for v in shirt.data.vertices],[tuple(t.vertices) for t in shirt.data.loop_triangles],all_triangles=True)
 fitted=BVHTree.FromPolygons([v.co for v in armor.data.vertices],[tuple(t.vertices) for t in armor.data.loop_triangles],all_triangles=True);gaps=[]
 for z in np.linspace(1.04,1.43,24):
  for theta in np.linspace(-.7,.7,25):
   origin=Vector((0,-.018,z));direction=Vector((math.sin(theta),math.cos(theta),0))
   q,_,_,r=fitted.ray_cast(origin,direction,.5);w,_,_,s=ref.ray_cast(origin,direction,.5)
   if q is not None and w is not None:gaps.append(r-s)
 assert len(gaps)>450 and min(gaps)>-.003 and np.percentile(gaps,95)<.035
 fit=json.loads(fit_path.read_text());fit['rear_inner_gap_after_m']={'min':min(gaps),'median':float(np.median(gaps)),'p95':float(np.percentile(gaps,95))};fit['rechecked_after_rebind']=True
 (a.output/'fit.json').write_text(json.dumps(fit,indent=2))
(a.output/'rebind.json').write_text(json.dumps({'method':'cuirass torso/back field + sample surface shoulders, after morph','vertices':len(fields),'bones':list(groups),'runtime':'NOT_RUN'},indent=2))
