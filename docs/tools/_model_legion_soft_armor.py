"""Offline Legion mail/rubber prototypes on the official body skin.
Blender --python this.py -- --sample <blend> --output <folder> --kind chainmail|brigantine|tire
Source-only: no runtime registration, no game interaction. CPU rendering.
"""
import argparse,sys,math,json,random
from pathlib import Path
import bpy,bmesh
from mathutils import Vector
p=argparse.ArgumentParser();p.add_argument('--sample',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--kind',choices=['chainmail','brigantine','tire'],required=True);p.add_argument('--reference-shirt',type=Path);p.add_argument('--physical-rings',action='store_true')
a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);a.output.mkdir(parents=True,exist_ok=True);random.seed(82)
bpy.ops.wm.open_mainfile(filepath=str(a.sample))
rig=bpy.data.objects['Bip001'];body=bpy.data.objects['M_BaseMesh Skin_BIP']
for o in list(bpy.data.objects):
 if o not in (rig,body):bpy.data.objects.remove(o,do_unlink=True)
for c in bpy.data.collections:c.hide_render=False;c.hide_viewport=False
body.hide_render=False;body.hide_set(False)
from mathutils.bvhtree import BVHTree
from mathutils.geometry import barycentric_transform
body.data.calc_loop_triangles()
bind_vertices=[body.matrix_world@v.co for v in body.data.vertices]
bind_faces=[tuple(t.vertices) for t in body.data.loop_triangles]
bind_bvh=BVHTree.FromPolygons(bind_vertices,bind_faces,all_triangles=True)
def skin_weights(pos):
 co,normal,index,distance=bind_bvh.find_nearest(pos);ids=bind_faces[index]
 bary=barycentric_transform(co,*[bind_vertices[i] for i in ids],Vector((1,0,0)),Vector((0,1,0)),Vector((0,0,1)))
 weights={}
 for idx,factor in zip(ids,bary):
  for g in body.data.vertices[idx].groups:
   name=body.vertex_groups[g.group].name
   if name in rig.data.bones and factor>0:weights[name]=weights.get(name,0)+factor*g.weight
 weights=dict(sorted(weights.items(),key=lambda t:t[1],reverse=True)[:4]);total=sum(weights.values())
 return {name:w/total for name,w in weights.items() if w>1e-7}
def torso_weights(pos):
 sample=Vector((max(-.15,min(.15,pos.x)),pos.y,pos.z))
 weights={n:w for n,w in skin_weights(sample).items() if n in ('Bip001 Pelvis','Bip001 Spine','Bip001 Spine1','Bip001 Spine2')}
 if not weights:return {'Bip001 Spine2':1.0}
 total=sum(weights.values());return {n:w/total for n,w in weights.items()}
def mat(name,color,metal=0,rough=.7):
 m=bpy.data.materials.new(name);m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*color,1);p.inputs['Metallic'].default_value=metal;p.inputs['Roughness'].default_value=rough;return m
mail=mat('Alternating wire mail rings',(.13,.13,.12),.78,.46)
n=mail.node_tree.nodes;l=mail.node_tree.links
uv=n.new('ShaderNodeTexCoord');sep=n.new('ShaderNodeSeparateXYZ');l.new(uv.outputs['UV'],sep.inputs[0])
def op(operation,x,y=None):
 t=n.new('ShaderNodeMath');t.operation=operation
 for i,value in enumerate([x,y] if y is not None else [x]):
  if isinstance(value,(int,float)):t.inputs[i].default_value=value
  else:l.new(value,t.inputs[i])
 return t.outputs[0]
x=op('MULTIPLY',sep.outputs['X'],100);y=op('MULTIPLY',sep.outputs['Y'],100)
row=op('FLOOR',y);offset=op('MULTIPLY',op('PINGPONG',row,1),.5)
u=op('SUBTRACT',op('FRACT',op('ADD',x,offset)),.5);v=op('SUBTRACT',op('FRACT',y),.5)
d=op('SQRT',op('ADD',op('MULTIPLY',u,u),op('MULTIPLY',v,v)))
ring=op('MULTIPLY',op('GREATER_THAN',d,.30),op('LESS_THAN',d,.47))
mix=n.new('ShaderNodeMixRGB');mix.inputs[1].default_value=(.008,.009,.008,1);mix.inputs[2].default_value=(.065,.060,.046,1);l.new(ring,mix.inputs[0])
noise=n.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=36;l.new(uv.outputs['Object'],noise.inputs['Vector'])
rust=n.new('ShaderNodeMixRGB');rust.blend_type='MULTIPLY';rust.inputs[0].default_value=.42;l.new(mix.outputs[0],rust.inputs[1]);l.new(noise.outputs['Color'],rust.inputs[2]);l.new(rust.outputs[0],n.get('Principled BSDF').inputs['Base Color'])
bump=n.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.8;bump.inputs['Distance'].default_value=.0016;l.new(ring,bump.inputs['Height']);l.new(bump.outputs[0],n.get('Principled BSDF').inputs['Normal'])
rubber=mat('Weathered truck tire rubber',(.021,.025,.024),0,.86)
leather=mat('Brown repair leather',(.075,.043,.024),0,.8);steel=mat('Rusty fasteners',(.16,.12,.078),.7,.52)
dust=mat('Sun bleached cut rubber',(.055,.047,.033),0,.94)
canvas=mat('Old dark canvas lining',(.025,.019,.011),0,.98)
for material,scale,strength in [(rubber,155,.30),(leather,95,.22),(dust,130,.25),(canvas,230,.20)]:
 nodes=material.node_tree.nodes;links=material.node_tree.links;shader=nodes.get('Principled BSDF')
 noise=nodes.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=scale;noise.inputs['Detail'].default_value=3
 bump=nodes.new('ShaderNodeBump');bump.inputs['Strength'].default_value=strength;bump.inputs['Distance'].default_value=.001
 links.new(noise.outputs['Fac'],bump.inputs['Height']);links.new(bump.outputs[0],shader.inputs['Normal'])
 ramp=nodes.new('ShaderNodeValToRGB');base=shader.inputs['Base Color'].default_value[:3]
 ramp.color_ramp.elements[0].color=(*(c*.55 for c in base),1);ramp.color_ramp.elements[1].color=(*(c*1.65 for c in base),1)
 links.new(noise.outputs['Fac'],ramp.inputs[0]);links.new(ramp.outputs[0],shader.inputs['Base Color'])
body.data.materials.clear();body.data.materials.append(mat('Fitting mannequin',(.045,.064,.070)))
# Retain the exact official weights; crop with planar cuts, not arbitrary face deletion.
shell=body.copy();shell.data=body.data.copy();bpy.context.collection.objects.link(shell);shell.name='TEST_'+a.kind+'_Male';shell.data.materials.clear();shell.data.materials.append(rubber if a.kind=='tire' else mail if a.kind=='chainmail' else canvas)
if a.reference_shirt:
 data=json.loads(a.reference_shirt.read_text());m=data['meshes'][1];box=m['bbox'] or data['bbox'];c=[(box[i]+box[i+3])*.5 for i in range(3)]
 verts=[(-(v[1]+c[1]),-(v[0]+c[0]),v[2]+c[2]) for v in m['vertices']]
 shirt_verts=list(verts);shirt_faces=[tuple(reversed(f)) for f in m['faces']]
 mesh=bpy.data.meshes.new('Actual Legion shirt clearance shell');mesh.from_pydata(verts,[],shirt_faces);mesh.update()
 shell.data=mesh;shell.matrix_world.identity();shell.vertex_groups.clear();shell.data.materials.append(rubber if a.kind=='tire' else mail if a.kind=='chainmail' else canvas)
 from mathutils.kdtree import KDTree
 donor=KDTree(len(body.data.vertices))
 for v in body.data.vertices:donor.insert(body.matrix_world@v.co,v.index)
 donor.balance();groups={}
 for v in shell.data.vertices:
  for name,weight in skin_weights(v.co).items():
   if name not in groups:groups[name]=shell.vertex_groups.new(name=name)
   groups[name].add([v.index],weight,'REPLACE')
bpy.context.view_layer.objects.active=shell;bpy.ops.object.select_all(action='DESELECT');shell.select_set(True)
bpy.ops.object.transform_apply(location=True,rotation=True,scale=True)
bm=bmesh.new();bm.from_mesh(shell.data)
# Offset with the original smooth normals before cutting; cut-edge normals can
# otherwise turn the neck/sleeve opening into spikes that intersect the body.
bm.normal_update()
for v in bm.verts:v.co+=v.normal*(.018 if a.reference_shirt else .024)
sleeve=.28 if a.kind=='brigantine' else .46
cuts=[((0,0,.99),(0,0,-1)),((sleeve,0,0),(1,0,0)),((-sleeve,0,0),(-1,0,0))]
if not a.reference_shirt:cuts.append(((0,0,1.50),(0,0,1)))
for co,normal in cuts:
 bmesh.ops.bisect_plane(bm,geom=list(bm.verts)+list(bm.edges)+list(bm.faces),plane_co=co,plane_no=normal,clear_outer=True,dist=.00001)
bm.normal_update()
bm.to_mesh(shell.data);bm.free();shell.data.update();assert len(shell.data.polygons)>100,'Empty cropped shell'
# Transfer can change nearest donor triangles across folds/armpits. Smooth the
# garment field before attaching panels so both share a continuous deformation.
from mathutils.kdtree import KDTree
smooth_tree=KDTree(len(shell.data.vertices))
for vertex in shell.data.vertices:smooth_tree.insert(vertex.co,vertex.index)
smooth_tree.balance()
neighbours={v.index:smooth_tree.find_n(v.co,16) for v in shell.data.vertices}
fields=[{g.group:g.weight for g in v.groups} for v in shell.data.vertices]
for iteration in range(3):
 updated=[]
 for v in shell.data.vertices:
  weights={};total=0
  for _,idx,distance in neighbours[v.index]:
   if distance>.045:continue
   factor=math.exp(-(distance/.024)**2);total+=factor
   for key,value in fields[idx].items():weights[key]=weights.get(key,0)+value*factor
  updated.append({key:value/total for key,value in weights.items()})
 fields=updated
for vertex,weights in zip(shell.data.vertices,fields):
 for g in list(vertex.groups):shell.vertex_groups[g.group].remove([vertex.index])
 for key,value in weights.items():shell.vertex_groups[key].add([vertex.index],value,'REPLACE')
# Cylindrical UV in metres keeps link size consistent; sleeves map around their axis.
uvlayer=shell.data.uv_layers.active or shell.data.uv_layers.new();uvlayer.name='MailDetail'
detail_uv=n.new('ShaderNodeUVMap');detail_uv.uv_map='MailDetail';l.new(detail_uv.outputs['UV'],sep.inputs[0])
for poly in shell.data.polygons:
 for li in poly.loop_indices:
  v=shell.data.vertices[shell.data.loops[li].vertex_index].co
  if abs(poly.center.x)>.225:
   arm_z=1.455-(abs(v.x)-.205)*.42
   u=math.atan2(v.y-.012,v.z-arm_z)/(2*math.pi)*.42;vv=abs(v.x)
  else:u=math.atan2(v.x,-v.y)/(2*math.pi)*1.12;vv=v.z
  uvlayer.data[li].uv=(u,vv)
 poly.use_smooth=True
sol=shell.modifiers.new('Fabric edge thickness','SOLIDIFY');sol.thickness=.003
# Rubber lamellae use the sample skin via nearest-vertex transfer, normalized to 4.
from mathutils.kdtree import KDTree
kd=KDTree(len(body.data.vertices))
for v in body.data.vertices:kd.insert(body.matrix_world@v.co,v.index)
kd.balance();parts=[shell]
def piece(name,verts,faces,material,thickness=.008,skin='torso'):
 mesh=bpy.data.meshes.new(name);mesh.from_pydata(verts,[],faces);mesh.update();o=bpy.data.objects.new(name,mesh);bpy.context.collection.objects.link(o);o.data.materials.append(material)
 groups={}
 for v in o.data.vertices:
  weights=skin_weights(v.co) if skin=='surface' or any(s in name.lower() for s in ('shoulder','forearm')) else garment_weights(v.co)
  for bone,weight in weights.items():
   if bone not in groups:groups[bone]=o.vertex_groups.new(name=bone)
   groups[bone].add([v.index],weight,'REPLACE')
 for face in mesh.polygons:face.use_smooth=True
 mod=o.modifiers.new('Thickness','SOLIDIFY');mod.thickness=thickness
 mod=o.modifiers.new('Skin','ARMATURE');mod.object=rig;parts.append(o);return o
# Shared garment surface also locates the rubber panels.
from mathutils.bvhtree import BVHTree
shell.data.calc_loop_triangles()
surface=BVHTree.FromPolygons([v.co for v in shell.data.vertices],[tuple(t.vertices) for t in shell.data.loop_triangles],all_triangles=True)
def garment_weights(pos):
 origin=Vector((0,-.018,pos.z));direction=Vector((pos.x,pos.y+.018,0)).normalized()
 co,normal,index,dist=surface.ray_cast(origin,direction,1)
 if co is None:co,normal,index,dist=surface.find_nearest(pos)
 ids=shell.data.loop_triangles[index].vertices
 bary=barycentric_transform(co,*[shell.data.vertices[i].co for i in ids],Vector((1,0,0)),Vector((0,1,0)),Vector((0,0,1)))
 weights={}
 for idx,factor in zip(ids,bary):
  for g in shell.data.vertices[idx].groups:
   name=shell.vertex_groups[g.group].name
   if factor>0:weights[name]=weights.get(name,0)+factor*g.weight
 weights=dict(sorted(weights.items(),key=lambda t:t[1],reverse=True)[:4]);total=sum(weights.values())
 return {name:w/total for name,w in weights.items() if w>1e-7}
# High-detail physical wire rings for baking; not a runtime mesh.
if a.kind=='chainmail' and a.physical_rings:
 centers=[];occupied=set()
 def add_ring(seed,row,origin):
  origin=Vector(origin);direction=(Vector(seed)-origin).normalized()
  co,normal,idx,dist=surface.ray_cast(origin,direction,1.0)
  if co is None:return
  cell=tuple(round(c/.007) for c in co)
  if cell in occupied:return
  occupied.add(cell);centers.append((co+normal*.002,normal,row))
 for row in range(48):
  z=1.003+row*.0102
  for col in range(98):
   theta=(col+.5*(row%2))*math.tau/98
   add_ring((.32*math.sin(theta),-.025-.28*math.cos(theta),z),row,(0,-.025,z))
 for side in (-1,1):
  for row in range(22):
   x=.224+row*.010
   for col in range(48):
    theta=(col+.5*(row%2))*math.tau/48
    add_ring((side*x,.012+.20*math.sin(theta),1.455-(x-.205)*.42+.20*math.cos(theta)),row,(side*x,.012,1.455-(x-.205)*.42))
 for ix in range(-21,22):
  for iy in range(-15,13):
   x=ix*.0105;y=iy*.0105
   co,normal,idx,dist=surface.ray_cast(Vector((x,y,1.7)),Vector((0,0,-1)),.24)
   if co is not None and co.z>1.465:
    cell=tuple(round(c/.007) for c in co)
    if cell not in occupied:occupied.add(cell);centers.append((co+normal*.002,normal,ix))
 verts=[];faces=[]
 for center,normal,row in centers:
  u=normal.cross(Vector((0,0,1)))
  if u.length<.1:u=normal.cross(Vector((0,1,0)))
  u.normalize();v=normal.cross(u).normalized()
  angle=math.radians(28 if row%2 else -28);v=v*math.cos(angle)+normal*math.sin(angle);axis=u.cross(v).normalized()
  start=len(verts)
  for i in range(12):
   q=i*math.tau/12;radial=u*math.cos(q)+v*math.sin(q)
   for j in range(4):
    phi=j*math.tau/4;verts.append(center+radial*(.0054+.00085*math.cos(phi))+axis*(.00085*math.sin(phi)))
  for i in range(12):
   for j in range(4):faces.append((start+i*4+j,start+i*4+(j+1)%4,start+((i+1)%12)*4+(j+1)%4,start+((i+1)%12)*4+j))
 ringmesh=bpy.data.meshes.new('Physical mail bake source');ringmesh.from_pydata(verts,[],faces);ringmesh.update()
 high=bpy.data.objects.new('BAKE_ONLY_Interlinked_wire',ringmesh);bpy.context.collection.objects.link(high);high.data.materials.append(mat('Rusted wire steel',(.105,.100,.085),.8,.43))
 for poly in high.data.polygons:poly.use_smooth=True
 shell.data.materials.clear();shell.data.materials.append(mat('Dark mail backing for bake',(.010,.012,.010),0,.85))
 print('PHYSICAL_RINGS',len(centers),'HIGH_TRIS',len(faces)*2)

# All plates are curved onto the garment, instead of lying in a fixed Y plane.
def torso(theta,z,lift=.012):
 # Local envelope follows actual shirt, smoothing fine cloth folds without a floating barrel.
 origin=Vector((0,-.018,z));direction=Vector((math.sin(theta),-math.cos(theta),0));radii=[]
 for angle,dz in [(0,0),(-.045,0),(.045,0),(0,-.01),(0,.01)]:
  direction2=Vector((math.sin(theta+angle),-math.cos(theta+angle),0));origin2=origin+Vector((0,0,dz))
  co,n,idx,dist=surface.ray_cast(origin2,direction2,1)
  if co is not None:radii.append(dist)
 if not radii:
  # A sleeveless armhole has no radial intersection; bridge to its closest rim.
  co,n,idx,dist=surface.find_nearest(origin+direction*.23)
  assert co is not None and dist<.12,('missing torso surface',theta,z)
  radii.append(max(.12,(co-origin).dot(direction)))
 radius=sum(radii)/len(radii)+.002
 return origin+direction*(radius+lift),direction

def stud_at(co,n,r=.003,skin='torso'):
 u=n.cross(Vector((0,0,1)))
 if u.length<.01:u=n.cross(Vector((0,1,0)))
 u.normalize();v=n.cross(u);verts=[co+r*(u*math.cos(i*math.tau/6)+v*math.sin(i*math.tau/6)) for i in range(6)]+[co+n*.0025]
 piece('Hand peened rusty rivet',verts,[(i,(i+1)%6,6) for i in range(6)],steel,.001,skin)

def strip(name,t0,t1,z0,z1,material,lift=.015,steps=12):
 rows=max(1,math.ceil(abs(z1-z0)/.015));width=steps+1
 verts=[torso(t0+(t1-t0)*i/steps,z0+(z1-z0)*j/rows,lift)[0] for j in range(rows+1) for i in range(width)]
 faces=[(j*width+i,j*width+i+1,(j+1)*width+i+1,(j+1)*width+i) for j in range(rows) for i in range(steps)]
 return piece(name,verts,faces,material,.008)

if a.kind=='chainmail':
 # Icon: broad upper leather harness, uninterrupted mail abdomen, leather hem.
 for back in (0,math.pi):
  strip('Upper salvaged chest harness',back-.93,back+.93,1.32,1.385,leather,.018,18)
  strip('Mail lower leather binding',back-1.15,back+1.15,1.00,1.055,leather,.020,18)
  for col in (-1,1):
   t=back+col*.68
   strip('Harness vertical binding',t-.075,t+.075,1.04,1.38,leather,.024,3)
   for z in (1.07,1.20,1.34):
    co,n=torso(t,z,.031);stud_at(co,n,.004)
else:
 # The brigantine reference is horizontal tyre strips with leather uprights.
 # The full suit uses deep broken tread blocks and larger shoulder/arm sections.
 rows=8 if a.kind=='brigantine' else 9
 for back in (0,math.pi):
  for row in range(rows):
   z=1.005+row*.05
   if a.kind=='brigantine':
    strip('Overlapping horizontal tyre strip',back-1.38,back+1.38,z,z+.047,rubber,.017+(row%2)*.002,24)
    strip('Worn exposed strip lip',back-1.10,back+1.10,z,z+.004,dust,.022,20)
   else:
    for col in range(6):
     t=back+(col-2.5)*.36;shift=.004*math.sin(row*3+col)
     strip('Thick cut truck tread block',t-.162,t+.162,z+shift,z+.052+shift,rubber,.022,4)
     # Chunky chevron lugs, inset grooves between independent rubber blocks.
     for dt in (-.10,.015):
      pts=[]
      for k in range(4):
       zz=z+.007+k*.012;tt=t+dt+k*.023
       pts.extend([torso(tt,zz,.037)[0],torso(tt+.055,zz,.037)[0]])
      piece('Scuffed truck tread lug',pts,[(k*2,k*2+1,k*2+3,k*2+2) for k in range(3)],dust if (row+col)%9==0 else rubber,.005)
  for t in (back-.83,back+.02,back+.83):
   # Irregular reused leather uprights overlap every horizontal plate.
   zs=[1.008+i*.025 for i in range(18)]
   verts=[torso(t+dt,z,.033)[0] for z in zs for dt in (-.038,.038)]
   piece('Salvaged leather rivet upright',verts,[(i*2,i*2+1,i*2+3,i*2+2) for i in range(len(zs)-1)],leather,.004)
   for row in range(rows):
    co,n=torso(t,1.025+row*.05,.034);stud_at(co,n,.0035)
 # A visible rough canvas repair on one flank rather than identical decoration.
 strip('Patch sewn over a split sidewall',.65,.96,1.19,1.26,canvas,.042,5)
 for t in (.67,.94):
  for z in (1.20,1.218,1.236,1.252):
   co,n=torso(t,z,.046);stud_at(co,n,.002)

# Curved shoulders, varied in coverage; no flat rectangular tiles in the air.
body.data.calc_loop_triangles()
shoulder_surface=BVHTree.FromPolygons([body.matrix_world@v.co for v in body.data.vertices],[tuple(t.vertices) for t in body.data.loop_triangles],all_triangles=True)
if a.reference_shirt:
 # Full shirt surface, including sleeves removed from the sleeveless shell.
 shoulder_surface=BVHTree.FromPolygons(shirt_verts,shirt_faces,all_triangles=True)
for side in (-1,1):
 count=(2 if side<0 else 1) if a.kind=='brigantine' else 3
 for row in range(count):
  vs=[]
  for x in (.215+row*.058,.279+row*.058):
   for y in (-.086,-.045,0,.045,.086):
    co,n,idx,dist=shoulder_surface.ray_cast(Vector((side*x,y,1.75)),Vector((0,0,-1)),1)
    if co is None:co,n,idx,dist=shoulder_surface.find_nearest(Vector((side*x,y,1.46)))
    vs.append(co+n*.032)
  piece('Cut tyre shoulder with overlapping lip',vs,[(i,i+1,i+6,i+5) for i in range(4)],rubber,.011)
  for idx in (1,3,6,8):stud_at(vs[idx]+Vector((0,0,.001)),Vector((0,0,1)),.003,'surface')
  # Original transverse tread on the shoulder, following the same curved cap.
  for k in range(4):
   p0=vs[k].lerp(vs[k+5],.27);p1=vs[k+1].lerp(vs[k+6],.27)
   p2=vs[k+1].lerp(vs[k+6],.48);p3=vs[k].lerp(vs[k+5],.48)
   piece('Shoulder tread ridge',[v+Vector((0,0,.007)) for v in (p0,p1,p2,p3)],[(0,1,2,3)],rubber,.004)

if a.kind=='tire':
 for side in (-1,1):
  start=Vector((side*.455,.008,1.285));end=Vector((side*.665,.008,1.125))
  axis=(end-start).normalized();u=Vector((0,-1,0));v=axis.cross(u).normalized()
  for row in range(3):
   for sector in range(6):
    pts=[]
    for height in (row/3+.025,(row+1)/3-.025):
     center=start.lerp(end,height)
     for j in range(4):
      angle=(sector+(j/3)*.92)*math.tau/6
      pts.append(center+(u*math.cos(angle)+v*math.sin(angle))*.075)
    piece('Cut tread forearm guard',pts,[(i,i+1,i+5,i+4) for i in range(3)],rubber,.012)
 # Legs remain the equipped Pants: this is the torso/arms tire item only.
# The waist belt follows the same shell to avoid cutting through the mail.
strip('Old leather waist support',-math.pi,math.pi,1.055,1.080,leather,.043,64)
for theta in (-.13,.13):
 co,n=torso(theta,1.067,.050);stud_at(co,n,.004)
scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=24;scene.cycles.use_denoising=True
scene.render.resolution_x=1000;scene.render.resolution_y=1000;scene.render.resolution_percentage=100
scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs[1].default_value=.35
for name,loc,power in [('Key',(-2,-3,3),180),('Fill',(2,-1,2),90),('Rim',(0,2,3),160)]:
 bpy.ops.object.light_add(type='AREA',location=loc);o=bpy.context.object;o.name=name;o.data.energy=power;o.data.size=2;o.rotation_euler=(Vector((0,0,1.2))-o.location).to_track_quat('-Z','Y').to_euler()
bpy.ops.object.camera_add(location=(-1,-3,1.8));scene.camera=bpy.context.object;scene.camera.data.type='ORTHO';scene.camera.data.ortho_scale=.95;scene.camera.rotation_euler=(Vector((0,0,1.25))-scene.camera.location).to_track_quat('-Z','Y').to_euler()
# Bake atlas is distinct from the mail's metrically mapped detail UV.
for obj in parts:
 bpy.ops.object.select_all(action='DESELECT');obj.select_set(True);bpy.context.view_layer.objects.active=obj
 for mod in list(obj.modifiers):
  if mod.type!='ARMATURE':bpy.ops.object.modifier_apply(modifier=mod.name)
 if not obj.data.uv_layers.get('MailDetail'):obj.data.uv_layers.new(name='MailDetail')
 obj.data.uv_layers.new(name='BakeAtlas');obj.data.uv_layers.active_index=len(obj.data.uv_layers)-1
bpy.ops.object.select_all(action='DESELECT')
for obj in parts:obj.select_set(True)
bpy.context.view_layer.objects.active=shell;bpy.ops.object.join();armor=bpy.context.object
armor.data.uv_layers.active_index=armor.data.uv_layers.find('BakeAtlas');armor.data.uv_layers.active.active_render=True
bpy.ops.object.mode_set(mode='EDIT');bpy.ops.mesh.select_all(action='SELECT');bpy.ops.uv.smart_project(island_margin=.008);bpy.ops.object.mode_set(mode='OBJECT')
for v in armor.data.vertices:
 influences=sorted([(g.group,g.weight) for g in v.groups if g.weight>0],key=lambda g:g[1],reverse=True)[:4];total=sum(w for _,w in influences)
 assert total>0,('unweighted',v.index)
 for g in list(v.groups):armor.vertex_groups[g.group].remove([v.index])
 for index,w in influences:armor.vertex_groups[index].add([v.index],w/total,'REPLACE')
armor.data.calc_loop_triangles()
bpy.ops.wm.save_as_mainfile(filepath=str(a.output/(a.kind+'.blend')))
scene.render.filepath=str(a.output/'front.png');bpy.ops.render.render(write_still=True)
(a.output/'status.json').write_text(json.dumps({'kind':a.kind,'status':'source prototype only; not baked/exported/registered; runtime unverified','reference':'ArmorIcons/'+{'chainmail':'Chainmail','brigantine':'TireBrigantine','tire':'TireArmor'}[a.kind]+'.png','ring_pitch_m':.01,'source_skin':'official sample'} ,indent=2))
