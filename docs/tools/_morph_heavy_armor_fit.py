"""Morph HAV torso depth to actual Legion shirt; preserve shell thickness and UVs.
Blender --python this.py -- --source model.blend --reference-armor Light.blend
 --shirt calibrated.json --output folder. Produces fitted model and body views.
"""
import argparse,json,sys,math,hashlib
from pathlib import Path
import bpy
import numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree
from mathutils.geometry import barycentric_transform
p=argparse.ArgumentParser()
for key in ('source','reference-armor','shirt','output'):p.add_argument('--'+key,type=Path,required=True)
a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);a.output.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(a.source))
armor=next(o for o in bpy.data.objects if o.type=='MESH' and o.name.startswith('TEST_'))
with bpy.data.libraries.load(str(a.reference_armor),link=False) as (src,dst):dst.objects=[n for n in src.objects if n.startswith('TEST_')]
donor=dst.objects[0];bpy.context.collection.objects.link(donor);bpy.context.view_layer.update()
donor.data.calc_loop_triangles()
source=BVHTree.FromPolygons([donor.matrix_world@v.co for v in donor.data.vertices],[tuple(t.vertices) for t in donor.data.loop_triangles],all_triangles=True)
data=json.loads(a.shirt.read_text(encoding='utf-8'));m=data['meshes'][1];box=m['bbox'] or data['bbox'];c=[(box[i]+box[i+3])*.5 for i in range(3)]
verts=[(-(v[1]+c[1]),-(v[0]+c[0]),v[2]+c[2]) for v in m['vertices']];faces=[tuple(reversed(f)) for f in m['faces']]
target=BVHTree.FromPolygons(verts,faces)
# Radial inner surfaces, sampled independently of pouches/outer MOLLE details.
NZ,NT=45,96;zs=np.linspace(.99,1.48,NZ);delta=np.full((NZ,NT),np.nan);before=[]
for iz,z in enumerate(zs):
 for it in range(NT):
  theta=2*math.pi*it/NT;direction=Vector((math.sin(theta),math.cos(theta),0));origin=Vector((0,-.018,z))
  v,_,_,r=source.ray_cast(origin,direction,.5);w,_,_,s=target.ray_cast(origin,direction,.5)
  if v is not None and w is not None:
   delta[iz,it]=s+.024-r
   if direction.y>.7:before.append(r-s)
assert np.isfinite(delta).sum()>NZ*NT*.5,'Insufficient shirt/vest ray overlap'
valid=np.argwhere(np.isfinite(delta))
for iz,it in np.argwhere(~np.isfinite(delta)):
 dtheta=np.minimum(abs(valid[:,1]-it),NT-abs(valid[:,1]-it));dist=(valid[:,0]-iz)**2+(dtheta*.5)**2
 j,k=valid[np.argmin(dist)];delta[iz,it]=delta[j,k]
for _ in range(3):
 padded=np.pad(delta,((1,1),(0,0)),mode='edge');delta=(delta*4+np.roll(delta,1,1)+np.roll(delta,-1,1)+padded[:-2]+padded[2:])/8
def displacement(co):
 radial=Vector((co.x,co.y+.018,0));r=radial.length
 if r<.02:return Vector()
 theta=math.atan2(radial.x,radial.y)%(2*math.pi);t=theta/(2*math.pi)*NT;it=int(t)%NT;ft=t-int(t)
 z=max(0,min(NZ-1.00001,(co.z-zs[0])/(zs[-1]-zs[0])*(NZ-1)));iz=int(z);fz=z-iz
 d=(delta[iz,it]*(1-ft)+delta[iz,(it+1)%NT]*ft)*(1-fz)+(delta[iz+1,it]*(1-ft)+delta[iz+1,(it+1)%NT]*ft)*fz
 # Neck opening and isolated arm guards stay outside the torso morph cage.
 fade=max(0,min(1,(1.61-co.z)/.13))*max(0,min(1,(.34-abs(co.x))/.1))
 return radial.normalized()*float(d)*fade
movements=[]
for v in armor.data.vertices:
 d=displacement(v.co);v.co+=d;movements.append(d.length)
armor.data.update();bpy.data.objects.remove(donor,do_unlink=True)
armor.data.calc_loop_triangles();fitted=BVHTree.FromPolygons([v.co for v in armor.data.vertices],[tuple(t.vertices) for t in armor.data.loop_triangles],all_triangles=True)
after=[]
for z in np.linspace(1.04,1.43,24):
 for theta in np.linspace(-.7,.7,25):
  origin=Vector((0,-.018,z));direction=Vector((math.sin(theta),math.cos(theta),0))
  v,_,_,r=fitted.ray_cast(origin,direction,.5);w,_,_,s=target.ray_cast(origin,direction,.5)
  if v is not None and w is not None:after.append(r-s)
assert len(after)>450
assert min(after)>-.003 and np.percentile(after,95)<.035,('Rear fitting gate',min(after),np.percentile(after,95))
mesh=bpy.data.meshes.new('LegionGoon shirt reference');mesh.from_pydata(verts,[],faces);mesh.update()
shirt=bpy.data.objects.new('QA actual LegionGoon shirt',mesh);bpy.context.collection.objects.link(shirt)
rig=next(o for o in bpy.data.objects if o.type=='ARMATURE');body=bpy.data.objects['M_BaseMesh Skin_BIP'];bpy.context.view_layer.update();body.data.calc_loop_triangles()
bverts=[body.matrix_world@v.co for v in body.data.vertices];bfaces=[tuple(t.vertices) for t in body.data.loop_triangles];body_bvh=BVHTree.FromPolygons(bverts,bfaces,all_triangles=True)
for v in mesh.vertices:
 point,_,index,_=body_bvh.find_nearest(v.co);ids=bfaces[index]
 bary=barycentric_transform(point,*[bverts[i] for i in ids],Vector((1,0,0)),Vector((0,1,0)),Vector((0,0,1)));weights={}
 for i,factor in zip(ids,bary):
  for g in body.data.vertices[i].groups:
   name=body.vertex_groups[g.group].name
   if name in rig.data.bones and factor>0:weights[name]=weights.get(name,0)+factor*g.weight
 weights=dict(sorted(weights.items(),key=lambda t:t[1],reverse=True)[:4]);total=sum(weights.values())
 for name,w in weights.items():
  group=shirt.vertex_groups.get(name) or shirt.vertex_groups.new(name=name);group.add([v.index],w/total,'REPLACE')
shirt.modifiers.new('QA approximate shirt weights from official body','ARMATURE').object=rig
mat=bpy.data.materials.new('QA red shirt');mat.use_nodes=True;mat.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value=(.3,.018,.012,1);mesh.materials.append(mat)
for poly in mesh.polygons:poly.use_smooth=True
scene=bpy.context.scene;scene.cycles.device='CPU';scene.cycles.samples=16;scene.render.resolution_x=720;scene.render.resolution_y=800
scene.camera.data.ortho_scale=1.25
for side,loc in [('front',(0,-3,1.5)),('back',(0,3,1.5)),('side',(3,0,1.5)),('back_oblique',(1.6,3,1.7))]:
 scene.camera.location=loc;scene.camera.rotation_euler=(Vector((0,0,1.27))-scene.camera.location).to_track_quat('-Z','Y').to_euler()
 scene.render.filepath=str(a.output/(side+'.png'));bpy.ops.render.render(write_still=True)
for bone,angles in [('Bip001 Spine1',(12,0,0)),('Bip001 Spine2',(23,0,12))]:
 rig.pose.bones[bone].rotation_mode='XYZ';rig.pose.bones[bone].rotation_euler=[math.radians(x) for x in angles]
bpy.context.view_layer.update()
for side,loc in [('lean_back',(1.6,3,1.7)),('lean_side',(3,0,1.5))]:
 scene.camera.location=loc;scene.camera.rotation_euler=(Vector((0,0,1.27))-scene.camera.location).to_track_quat('-Z','Y').to_euler()
 scene.render.filepath=str(a.output/(side+'.png'));bpy.ops.render.render(write_still=True)
for bone in rig.pose.bones:bone.rotation_mode='XYZ';bone.rotation_euler=(0,0,0)
bpy.context.view_layer.update()
shirt.hide_render=True
bpy.ops.wm.save_as_mainfile(filepath=str(a.output/'model.blend'))
manifest_path=a.output/'model.json'
if manifest_path.exists():
 manifest=json.loads(manifest_path.read_text());manifest['geometry_sha256']=hashlib.sha256(b''.join(float(v).hex().encode() for vertex in armor.data.vertices for v in vertex.co)).hexdigest();manifest['fitted_to']=a.shirt.name;manifest_path.write_text(json.dumps(manifest,indent=2))
(a.output/'fit.json').write_text(json.dumps({'reference':a.shirt.name,'rear_inner_gap_before_m':{'median':float(np.median(before)),'p95':float(np.percentile(before,95))},'rear_inner_gap_after_m':{'min':min(after),'median':float(np.median(after)),'p95':float(np.percentile(after,95))},'max_vertex_morph_m':max(movements),'runtime':'NOT_RUN'},indent=2))
