"""Blender M4 QA repair: detach FSB for iron-sight components, keep carbine furniture.
--blend FILE --output DIR --game-root ROOT. Stages only, one weapon per pass.
"""
import argparse,json,sys
from pathlib import Path
import bpy,bmesh
from mathutils import Matrix,Vector
sys.path.insert(0,str(Path(__file__).resolve().parent))
from _ja3_mesh_prepare import prepare_export_mesh
from _export_m14_family_assets import load_hge,export_fbx
p=argparse.ArgumentParser()
p.add_argument('--weapon',choices=('M4A1','M16A4'),default='M4A1')
for k in ('blend','output','game-root'):p.add_argument('--'+k,type=Path,required=True)
a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);a.output.mkdir(parents=True,exist_ok=True)
hge=load_hge(a.game_root);bpy.ops.wm.open_mainfile(filepath=str(a.blend))
prefix='M4R_M4A1' if a.weapon=='M4A1' else 'M16R_M16A4';host=bpy.data.objects[prefix]
spots={c.hge_obj_settings.spot_name:c.location.copy() for c in host.children if c.type=='EMPTY'}
normal=bpy.data.objects[prefix+'_Barrel']
def split(obj,keep_sight):
 bm=bmesh.new();bm.from_mesh(obj.data)
 bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=.000001)
 seen=set();remove=[];count=0
 for seed in bm.verts:
  if seed in seen:continue
  todo=[seed];seen.add(seed);part=[]
  while todo:
   v=todo.pop();part.append(v)
   for e in v.link_edges:
    q=e.other_vert(v)
    if q not in seen:seen.add(q);todo.append(q)
  lo=min(v.co.y for v in part);hi=max(v.co.y for v in part)
  cutoff=-.183 if a.weapon=='M4A1' else -.3241
  is_sight=lo<cutoff and hi-lo<.10
  if is_sight:count+=len(part)
  if is_sight!=keep_sight:remove.extend(part)
 assert count>200,(obj.name,count)
 bmesh.ops.delete(bm,geom=remove,context='VERTS');bm.to_mesh(obj.data);bm.free()
front=normal.copy();front.data=normal.data.copy();bpy.context.collection.objects.link(front)
front.name=prefix+'_FrontSight';front.hge_obj_settings.entity=front.name
origin=normal.parent.copy();origin.name=front.name+'_Origin';bpy.context.collection.objects.link(origin)
front.parent=origin
split(front,True)
affected=[]
for suffix in ('Barrel','BarrelShort'):
 obj=bpy.data.objects[prefix+'_'+suffix];split(obj,False);affected.append(obj)
extension=0
if a.weapon=='M4A1':
 long=bpy.data.objects[prefix+'_BarrelLong'];old_front=min(v.co.y for v in long.data.vertices)
 long.data=normal.data.copy()
 front_y=min(v.co.y for v in long.data.vertices)
 extension=front_y-old_front
 for v in long.data.vertices:
  if v.co.y<-.23:v.co.y-=extension*((-.23-v.co.y)/(-.23-front_y))
 affected.append(long)
reports={}
if a.weapon=='M4A1':
 rear=bpy.data.objects[prefix+'_RearSight']
 assert min(v.co.y for v in rear.data.vertices)>3.9,'Expected known source-layout offset'
 rear.data.transform(Matrix.Translation((0,-4,0)))
 affected.append(rear)
spot=next(c for c in host.children if c.type=='EMPTY' and c.hge_obj_settings.spot_name=='Barrel').copy()
spot.name='Gassblock';spot.hge_obj_settings.spot_name='Gassblock';bpy.context.collection.objects.link(spot)
affected.extend([front,host])
for obj in affected:reports[obj.name]=prepare_export_mesh(obj)
bpy.ops.wm.save_as_mainfile(filepath=str(a.output/(a.weapon+'-assembled.blend')))
keep=set(affected)
for obj in affected:
 keep.update(obj.children)
 if obj.parent:keep.add(obj.parent);obj.parent.location=Vector()
for obj in list(bpy.data.objects):
 if obj not in keep:bpy.data.objects.remove(obj,do_unlink=True)
bpy.ops.wm.save_as_mainfile(filepath=str(a.output/(a.weapon+'.blend')))
export_fbx(hge,a.output/(a.weapon+'.fbx'))
(a.output/'report.json').write_text(json.dumps({'barrel_extension_m':extension,'mesh_checks':reports},indent=2))
print('STAGED',list(reports))
