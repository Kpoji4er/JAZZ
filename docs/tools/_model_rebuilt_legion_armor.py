"""2026-09-26 rebuilt improvised armor; shared sample fitting utilities from the legacy builder.
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
body.hide_render=False;body.hide_set(False);bpy.context.view_layer.update()
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
x=op('MULTIPLY',sep.outputs['X'],85);y=op('MULTIPLY',sep.outputs['Y'],85)
row=op('FLOOR',y);offset=op('MULTIPLY',op('PINGPONG',row,1),.5)
u=op('SUBTRACT',op('FRACT',op('ADD',x,offset)),.5);v=op('SUBTRACT',op('FRACT',y),.5)
d=op('SQRT',op('ADD',op('MULTIPLY',u,u),op('MULTIPLY',v,v)))
ring=op('MULTIPLY',op('GREATER_THAN',d,.30),op('LESS_THAN',d,.47))
mix=n.new('ShaderNodeMixRGB');mix.inputs[1].default_value=(.022,.025,.027,1);mix.inputs[2].default_value=(.34,.36,.38,1);l.new(ring,mix.inputs[0])
noise=n.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=36;l.new(uv.outputs['Object'],noise.inputs['Vector'])
rust=n.new('ShaderNodeMixRGB');rust.blend_type='MULTIPLY';rust.inputs[0].default_value=.42;l.new(mix.outputs[0],rust.inputs[1]);l.new(noise.outputs['Color'],rust.inputs[2]);l.new(rust.outputs[0],n.get('Principled BSDF').inputs['Base Color'])
bump=n.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.8;bump.inputs['Distance'].default_value=.004;l.new(op('SQRT',op('MAXIMUM',op('SUBTRACT',.009,op('MULTIPLY',op('SUBTRACT',d,.38),op('SUBTRACT',d,.38))),0)),bump.inputs['Height']);l.new(bump.outputs[0],n.get('Principled BSDF').inputs['Normal'])
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
  native={data['bones'][i]['name']:w for i,w in zip(m['bone_indices'][v.index],m['bone_weights'][v.index]) if w>0 and data['bones'][i]['name'] in rig.data.bones}
  total=sum(native.values())
  for name,weight in native.items():
   if name not in groups:groups[name]=shell.vertex_groups.new(name=name)
   groups[name].add([v.index],weight/total,'REPLACE')
bpy.context.view_layer.objects.active=shell;bpy.ops.object.select_all(action='DESELECT');shell.select_set(True)
bpy.ops.object.transform_apply(location=True,rotation=True,scale=True)
bm=bmesh.new();bm.from_mesh(shell.data)
# Imported UV/normal seams are coincident boundaries, not garment openings.
# Weld before offsetting or smoothing so sleeves and collar stay sewn together.
bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-6)
bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces))
shirt_clearance_surface=BVHTree.FromBMesh(bm)
# Offset with the original smooth normals before cutting; cut-edge normals can
# otherwise turn the neck/sleeve opening into spikes that intersect the body.
bm.normal_update()
for v in bm.verts:
 radial=Vector((v.co.x,v.co.y+.018,0)).normalized()
 torso_blend=max(0,min(1,(.27-abs(v.co.x))/.07))*max(0,min(1,(1.40-v.co.z)/.10))
 direction=v.normal.lerp(radial,torso_blend).normalized()
 if a.kind!='chainmail':direction=radial if v.co.z<1.38 and abs(v.co.x)<.235 else v.normal
 clearance=.026 if a.kind=='chainmail' else .018 if a.reference_shirt else .024
 v.co+=direction*clearance
sleeve=.39 if a.kind=='chainmail' else .235
cuts=[((0,0,.99),(0,0,-1)),((sleeve,0,0),(1,0,0)),((-sleeve,0,0),(-1,0,0))]
if not a.reference_shirt:cuts.append(((0,0,1.50),(0,0,1)))
for co,normal in cuts:
 bmesh.ops.bisect_plane(bm,geom=list(bm.verts)+list(bm.edges)+list(bm.faces),plane_co=co,plane_no=normal,clear_outer=True,dist=.00001)
boundary=[v for v in bm.verts if v.is_boundary and v.co.z>1.3]
for iteration in range(8):
 positions={v: v.co.lerp(sum((edge.other_vert(v).co for edge in v.link_edges if edge.is_boundary),Vector())/max(1,sum(edge.is_boundary for edge in v.link_edges)),.4) for v in boundary}
 for v,co in positions.items():v.co=co
bm.normal_update()
if a.reference_shirt:
 # Cover the donor's protruding hip-pocket folds with a continuous mail hem.
 for v in bm.verts:
  if v.co.z>=1.16:continue
  direction=Vector((v.co.x,v.co.y+.018,0)).normalized()
  radii=[]
  for x,y,z in shirt_verts:
   radial=Vector((x,y+.018,0))
   if abs(z-v.co.z)<.035 and radial.length and radial.normalized().dot(direction)>.985:radii.append(radial.length)
  if radii:
   radius=max(Vector((v.co.x,v.co.y+.018,0)).length,max(radii)+.020)
   v.co.x=direction.x*radius;v.co.y=-.018+direction.y*radius
if a.kind=='chainmail':
 # Correct concave armpit folds against actual shirt triangles, not just averaged
 # vertex normals. Face-centre samples catch penetration between clear vertices.
 for iteration in range(6):
  corrections={v:Vector() for v in bm.verts};counts={v:0 for v in bm.verts}
  samples=[(v.co,[v]) for v in bm.verts]+[(f.calc_center_median(),list(f.verts)) for f in bm.faces]
  for point,vertices in samples:
   co,normal,index,distance=shirt_clearance_surface.find_nearest(point)
   if distance>.045:continue
   signed=(point-co).dot(normal)
   if signed>=.010:continue
   move=normal*min(.016,.012-signed)
   for vertex in vertices:corrections[vertex]+=move;counts[vertex]+=1
  for vertex in bm.verts:
   if counts[vertex]:vertex.co+=corrections[vertex]/counts[vertex]
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
for iteration in range(0 if a.kind=='chainmail' else 3):
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
  if poly.center.z>1.30 and abs(poly.center.x)>.225:
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
if a.reference_shirt:
 native_tree=KDTree(len(shirt_verts))
 native_fields=[]
 for index,co in enumerate(shirt_verts):
  native_tree.insert(Vector(co),index)
  native_fields.append({data['bones'][i]['name']:w for i,w in zip(m['bone_indices'][index],m['bone_weights'][index]) if w>0})
 native_tree.balance()
_torso_cache={}
def stable_torso_weights(pos):
 # Gaussian integration of the official torso skin, continuous through side seams.
 key=tuple(round(float(c),3) for c in pos)
 if key in _torso_cache:return _torso_cache[key]
 q=Vector(pos);result={}
 # Depth of an applied strap/bolt must not change its animation relative to
 # the supporting band. All torso layers sample the same radial garment point.
 direction=Vector((pos.x,pos.y+.018,0))
 if direction.length and pos.z<1.46:
  hit,_,_,_=surface.ray_cast(Vector((0,-.018,pos.z)),direction.normalized(),1)
  if hit is not None:q=hit
 tree=native_tree if a.reference_shirt else kd
 nearby=tree.find_range(q,.14) or tree.find_n(q,12)
 for _,index,distance in nearby:
  factor=math.exp(-(distance/.045)**2)
  field=native_fields[index] if a.reference_shirt else {body.vertex_groups[g.group].name:g.weight for g in body.data.vertices[index].groups}
  for bone,weight in field.items():
   if bone in ('Bip001 Pelvis','Bip001 Spine','Bip001 Spine1','Bip001 Spine2'):
    result[bone]=result.get(bone,0)+weight*factor
 total=sum(result.values());assert total>0
 weights={bone:w/total for bone,w in result.items() if w>1e-7}
 _torso_cache[key]=weights;return weights


def piece(name,verts,faces,material,thickness=.008,skin='torso'):
 mesh=bpy.data.meshes.new(name);mesh.from_pydata(verts,[],faces);mesh.update();o=bpy.data.objects.new(name,mesh);bpy.context.collection.objects.link(o);o.data.materials.append(material)
 o['detail_wire']=thickness==0
 groups={}
 for v in o.data.vertices:
  weights=skin_weights(v.co) if 'forearm' in name.lower() else garment_weights(v.co) if skin=='surface' else attachment_weights(v.co)
  for bone,weight in weights.items():
   if bone not in groups:groups[bone]=o.vertex_groups.new(name=bone)
   groups[bone].add([v.index],weight,'REPLACE')
 for face in mesh.polygons:face.use_smooth=True
 if thickness:
  mod=o.modifiers.new('Thickness','SOLIDIFY');mod.thickness=thickness
 mod=o.modifiers.new('Skin','ARMATURE');mod.object=rig;parts.append(o);return o
# Shared garment surface also locates the rubber panels.
from mathutils.bvhtree import BVHTree
shell.data.calc_loop_triangles()
surface=BVHTree.FromPolygons([v.co for v in shell.data.vertices],[tuple(t.vertices) for t in shell.data.loop_triangles],all_triangles=True)
garment_fields=[{shell.vertex_groups[g.group].name:g.weight for g in v.groups} for v in shell.data.vertices]
def garment_weights(pos):
 co,normal,index,dist=surface.find_nearest(pos)
 ids=shell.data.loop_triangles[index].vertices
 bary=barycentric_transform(co,*[shell.data.vertices[i].co for i in ids],Vector((1,0,0)),Vector((0,1,0)),Vector((0,0,1)))
 weights={}
 for idx,factor in zip(ids,bary):
  for name,weight in garment_fields[idx].items():
   if factor>0:weights[name]=weights.get(name,0)+factor*weight
 weights=dict(sorted(weights.items(),key=lambda t:t[1],reverse=True)[:4]);total=sum(weights.values())
 return {name:w/total for name,w in weights.items() if w>1e-7}

def attachment_weights(pos):
 # A torso fitting must never jump to an adjacent sleeve at the armpit.
 # Share the same continuous transition with the mail itself and all attachments.
 t=max(0,min(1,(pos.z-1.35)/.13));t=t*t*(3-2*t)
 lo=stable_torso_weights(pos)
 if t==0:return lo
 hi=garment_weights(pos)
 values={name:lo.get(name,0)*(1-t)+hi.get(name,0)*t for name in lo.keys()|hi.keys()}
 return values

for vertex in shell.data.vertices:
 follow_sleeve=abs(vertex.co.x)>.225 and vertex.co.z>1.2
 follow_shoulder=a.kind=='chainmail' and vertex.co.z>1.38
 weights=garment_weights(vertex.co) if follow_sleeve or follow_shoulder else attachment_weights(vertex.co)
 for group in list(vertex.groups):shell.vertex_groups[group.group].remove([vertex.index])
 for name,value in weights.items():
  group=shell.vertex_groups.get(name) or shell.vertex_groups.new(name=name)
  group.add([vertex.index],value,'REPLACE')
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
 # Every panel, belt and fastener shares the same fitted radial surface.
 # Clamp below the hem for the hanging shield; retain its requested height.
 # Lower the upper flank around the armhole, retaining the full chest height.
 if a.kind!='chainmail':z-=.075*abs(math.sin(theta))**6*max(0,min(1,(z-1.27)/.17))
 direction=Vector((math.sin(theta),-math.cos(theta),0))
 origin=Vector((0,-.018,max(1.015,min(1.445,z))))
 co,normal,index,dist=surface.ray_cast(origin,direction,1)
 if co is None:co,normal,index,dist=surface.find_nearest(origin+direction*.20)
 # A local outer envelope bridges small cloth creases without cutting through them.
 radius=(Vector((co.x,co.y+.018,0))).length
 for dt,dz in ((-.045,0),(.045,0),(0,-.012),(0,.012)):
  ray=Vector((math.sin(theta+dt),-math.cos(theta+dt),0))
  hit,_,_,_=surface.ray_cast(origin+Vector((0,0,dz)),ray,1)
  if hit is not None:radius=max(radius,Vector((hit.x,hit.y+.018,0)).length)
 co=Vector((0,-.018,z))+direction*radius
 return co+direction*lift,direction

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

# Broad, constructed components replace the rejected uniform tiled overlay.
# All coordinates are metres in the official sample frame.
def material(name,col,metal=0,rough=.65,texture=False):
    m=bpy.data.materials.new(name); m.diffuse_color=(*col,1); m.use_nodes=True
    n=m.node_tree.nodes; l=m.node_tree.links; p=n.get('Principled BSDF')
    p.inputs['Base Color'].default_value=(*col,1); p.inputs['Metallic'].default_value=metal; p.inputs['Roughness'].default_value=rough
    if texture:
        tex=n.new('ShaderNodeTexNoise'); tex.inputs['Scale'].default_value=180; tex.inputs['Detail'].default_value=3
        coords=n.new('ShaderNodeTexCoord'); l.new(coords.outputs['Object'],tex.inputs['Vector'])
        ramp=n.new('ShaderNodeValToRGB'); ramp.color_ramp.elements[0].position=.27; ramp.color_ramp.elements[0].color=(*(c*.78 for c in col),1); ramp.color_ramp.elements[1].position=.74; ramp.color_ramp.elements[1].color=(*(c*1.12 for c in col),1)
        l.new(tex.outputs['Fac'],ramp.inputs[0]); l.new(ramp.outputs[0],p.inputs['Base Color'])
        b=n.new('ShaderNodeBump'); b.inputs['Strength'].default_value=.13; b.inputs['Distance'].default_value=.0009; l.new(tex.outputs['Fac'],b.inputs['Height']); l.new(b.outputs[0],p.inputs['Normal'])
    if metal>.4 and texture:
        # Layer oxidation and fine directional scratches in physical shader inputs.
        ox=n.new('ShaderNodeTexNoise');ox.inputs['Scale'].default_value=31;ox.inputs['Detail'].default_value=4
        l.new(coords.outputs['Object'],ox.inputs['Vector'])
        mask=n.new('ShaderNodeValToRGB');mask.color_ramp.elements[0].position=.55;mask.color_ramp.elements[0].color=(0,0,0,1)
        mask.color_ramp.elements[1].position=.76;mask.color_ramp.elements[1].color=(.8,.8,.8,1);l.new(ox.outputs['Fac'],mask.inputs[0])
        mix=n.new('ShaderNodeMixRGB');mix.inputs[2].default_value=(.12,.047,.017,1)
        l.new(mask.outputs[0],mix.inputs[0]);l.new(ramp.outputs[0],mix.inputs[1])
        direction=n.new('ShaderNodeVectorMath');direction.operation='MULTIPLY';direction.inputs[1].default_value=(700,700,26)
        l.new(coords.outputs['Object'],direction.inputs[0])
        scratch=n.new('ShaderNodeTexNoise');scratch.inputs['Scale'].default_value=1;scratch.inputs['Detail'].default_value=2
        l.new(direction.outputs[0],scratch.inputs['Vector'])
        scratchmask=n.new('ShaderNodeValToRGB');scratchmask.color_ramp.elements[0].position=.72;scratchmask.color_ramp.elements[0].color=(0,0,0,1)
        scratchmask.color_ramp.elements[1].position=.79;scratchmask.color_ramp.elements[1].color=(.65,.65,.65,1);l.new(scratch.outputs['Fac'],scratchmask.inputs[0])
        scratchmix=n.new('ShaderNodeMixRGB');scratchmix.inputs[2].default_value=(.27,.27,.25,1)
        l.new(scratchmask.outputs[0],scratchmix.inputs[0]);l.new(mix.outputs[0],scratchmix.inputs[1]);l.new(scratchmix.outputs[0],p.inputs['Base Color'])
        roughmix=n.new('ShaderNodeMapRange');roughmix.inputs['To Min'].default_value=.38;roughmix.inputs['To Max'].default_value=.88
        l.new(mask.outputs[0],roughmix.inputs[0]);l.new(roughmix.outputs[0],p.inputs['Roughness'])
        bevelnode=n.new('ShaderNodeBevel');bevelnode.inputs['Radius'].default_value=.001;bevelnode.samples=4
        l.new(bevelnode.outputs[0],b.inputs['Normal'])
    return m
iron=material('Oxidised salvaged steel',(.105,.099,.087),.6,.68,True)
iron2=material('Faded olive painted steel',(.071,.087,.056),.48,.66,True)
rubber=material('Weathered black truck rubber',(.018,.019,.017),0,.91,True)
rubber2=material('Worn tread surfaces',(.025,.024,.020),0,.88,True)
strapmat=material('Dark repaired leather',(.073,.039,.023),0,.84,True)
cutedge=material('Worn cut steel edge',(.24,.25,.23),.8,.42,True)

def panel(name,t0,t1,z0,z1,material,lift=.02,slant=0,thickness=.006):
 cols=max(4,min(14,math.ceil((t1-t0)*.24/.022)));rows=max(2,math.ceil((z1-z0)/.018));vs=[]
 for j in range(rows+1):
  v=j/rows
  for i in range(cols+1):
   u=i/cols;bevel=.055*(abs(2*v-1)**8)
   t=t0+(t1-t0)*(bevel+(1-2*bevel)*u)
   z=z0+(z1-z0)*v+slant*(u-.5)+.0006*math.sin(u*13+v*5)
   vs.append(torso(t,z,lift)[0])
 fs=[(j*(cols+1)+i,j*(cols+1)+i+1,(j+1)*(cols+1)+i+1,(j+1)*(cols+1)+i) for j in range(rows) for i in range(cols)]
 return piece(name,vs,fs,material,thickness)

_part_surfaces={}
def outer_attachment(t,z,lift):
 co,norm=torso(t,z,lift)
 origin=co+norm*.15;hits=[]
 for obj in parts:
  if obj==shell or obj.get('detail_wire') or 'rivet' in obj.name.lower():continue
  if obj.name not in _part_surfaces:
   obj.data.calc_loop_triangles()
   _part_surfaces[obj.name]=BVHTree.FromPolygons([v.co for v in obj.data.vertices],[tuple(f.vertices) for f in obj.data.loop_triangles],all_triangles=True)
  hit,normal,index,distance=_part_surfaces[obj.name].ray_cast(origin,-norm,.30)
  if hit is not None:hits.append((distance,hit))
 if hits:co=min(hits,key=lambda h:h[0])[1]+norm*.0008
 return co,norm

def fastening(t,z,lift=.03):
 co,norm=outer_attachment(t,z,lift);stud_at(co,norm,.0035)

def tube(name,path,radius,material,skin='torso',sides=6):
 vs=[];fs=[]
 for i,co in enumerate(path):
  tangent=(path[min(i+1,len(path)-1)]-path[max(0,i-1)]).normalized()
  normal=tangent.cross(Vector((0,0,1)))
  if normal.length<.1:normal=tangent.cross(Vector((0,1,0)))
  normal.normalize();binormal=tangent.cross(normal).normalized()
  for j in range(sides):vs.append(co+radius*(normal*math.cos(j*math.tau/sides)+binormal*math.sin(j*math.tau/sides)))
 for i in range(len(path)-1):
  for j in range(sides):fs.append((i*sides+j,i*sides+(j+1)%sides,(i+1)*sides+(j+1)%sides,(i+1)*sides+j))
 fs.extend([tuple(reversed(range(sides))),tuple((len(path)-1)*sides+j for j in range(sides))])
 return piece(name,vs,fs,material,0,skin)

def buckle(theta,z,lift=.05,skin='torso'):
 pts=[outer_attachment(theta+dt,z+dz,lift)[0] for dt,dz in [(-.060,-.015),(.060,-.015),(.060,.015),(-.060,.015),(-.060,-.015)]]
 tube('Forged rectangular buckle',pts,.0023,steel,skin)
 tube('Buckle tongue',[outer_attachment(theta,z-.015,lift)[0],outer_attachment(theta,z+.01,lift)[0]],.0015,steel,skin)

def stitch_line(theta,z0,z1,lift):
 for i in range(int((z1-z0)/.012)):
  z=z0+i*.012
  tube('Waxed leather stitch',[outer_attachment(theta-.010,z,lift)[0],outer_attachment(theta+.010,z+.003,lift)[0]],.00065,dust)

def side_lacing():
 for side in (-1,1):
  t=side*math.pi/2
  for row in range(5):
   z=1.05+.066*row
   for direction in (-1,1):
    points=[outer_attachment(t-.19+.38*u/8,z+(.050*u/8 if direction>0 else .050*(1-u/8)),.026)[0] for u in range(9)]
    tube('Crossed repair cord at flank',points,.002,strapmat)
   for dt in (-.19,.19):fastening(t+dt,z,.029)

def belt(t0,t1,z,width=.025,lift=.035):
 return strip('Leather support strap',t0,t1,z,z+width,strapmat,lift,32)

def tread(t0,t1,z0,z1,lift,rows=5):
 # One truck tread sheet with a central channel and large diagonal lugs.
 for row in range(rows):
  z=z0+(z1-z0)*(row+.12)/rows
  for side in (-1,1):
   mid=(t0+t1)/2;lo=mid+.03 if side>0 else t0+.025;hi=t1-.025 if side>0 else mid-.03
   panel('Worn chevron tread',lo,hi,z,z+(z1-z0)*.52/rows,rubber2,lift,.020*side,.009)

def shoulder(side,large):
 # Deliberately arched tyre casing with uniform thickness and no collapsed rays.
 nx=12;ny=16;vs=[]
 for i in range(nx+1):
  u=i/nx;x=side*(.19+(.225 if large else .15)*u)
  z=1.519-.075*u-.030*u*u
  for j in range(ny+1):
   angle=-1.12+2.24*j/ny
   y=-.009+.119*math.sin(angle)
   co,normal,_,_=surface.ray_cast(Vector((x,y,1.8)),Vector((0,0,-1)),.6)
   if co is None:co,normal,_,_=bind_bvh.ray_cast(Vector((x,y,1.8)),Vector((0,0,-1)),.6)
   fitted=max(z-.095*(1-math.cos(angle)),co.z+.015 if co else 0)
   vs.append(Vector((x,y,fitted)))
 fs=[(i*(ny+1)+j,(i+1)*(ny+1)+j,(i+1)*(ny+1)+j+1,i*(ny+1)+j+1) for i in range(nx) for j in range(ny)]
 if side<0:fs=[tuple(reversed(f)) for f in fs]
 piece('Shoulder cut from truck tyre',vs,fs,rubber,.012,'surface')
 for i in (2,5,8):
  if not large and i==8:continue
  pts=[vs[i*(ny+1)+j]+Vector((0,0,.010)) for j in range(ny+1)]
  pts2=[vs[(i+1)*(ny+1)+j]+Vector((0,0,.010)) for j in range(ny+1)]
  ridge_faces=[(j,j+1,ny+2+j,ny+1+j) for j in range(ny)]
  if side>0:ridge_faces=[tuple(reversed(f)) for f in ridge_faces]
  piece('Shoulder tread ridge',pts+pts2,ridge_faces,rubber2,.006,'surface')
 for index in (ny+3,len(vs)-ny-4):stud_at(vs[index]+Vector((0,0,.003)),Vector((0,0,1)),.004,'surface')

 # Two leather ties across the shoulder root join it to the harness.
 for y in (-.055,.055):
  points=[]
  for i in range(7):
   x=side*(.145+.075*i/6)
   for dy in (-.011,.011):
    co,_,_,_=surface.ray_cast(Vector((x,y+dy,1.8)),Vector((0,0,-1)),.6)
    points.append(Vector((x,y+dy,co.z+(.017 if abs(x)>.19 else .013) if co else 1.515)))
  piece('Shoulder anchor tie',points,[(2*i,2*i+1,2*i+3,2*i+2) for i in range(6)],strapmat,.004,'surface')

def over_shoulder(side):
 # Front and rear hangers visibly connect the torso armor across the shoulder.
 vs=[];steps=24
 for i in range(steps+1):
  t=i/steps
  angle=.65 if a.kind=='chainmail' else 1.0 if a.kind=='brigantine' else .75
  height=1.432 if a.kind=='chainmail' else 1.408 if a.kind=='brigantine' else 1.365
  front=torso(side*angle,height,.018)[0]
  back=torso(math.pi-side*angle,height,.018)[0]
  point=front.lerp(back,t)
  for dx in (-.016,.016):
   x=point.x*(1-math.sin(math.pi*t))+side*.145*math.sin(math.pi*t)+dx
   origin=Vector((x,-.018,point.z))
   direction=Vector((0,-math.cos(math.pi*t),math.sin(math.pi*t)))
   co,_,_,_=surface.ray_cast(origin,direction,.6)
   if co is None:co=point
   fitted=co+direction*.009
   endpoint=front if t<.5 else back
   blend=min(1,min(t,1-t)/.14)
   anchor=Vector((x,endpoint.y,endpoint.z))
   vs.append(anchor.lerp(fitted,blend))
 for iteration in range(3):
  smooth=list(vs)
  for i in range(1,steps):
   for edge in (0,1):smooth[2*i+edge]=vs[2*i+edge]*.5+(vs[2*(i-1)+edge]+vs[2*(i+1)+edge])*.25
  vs=smooth
 piece('Continuous leather shoulder hanger',vs,[(2*i,2*i+1,2*i+3,2*i+2) for i in range(steps)],strapmat,.004,'hanger')

if a.kind=='chainmail':
 # Two independent battered chest plates, free mail between and below them.
 panel('Left scavenged chest plate',-.83,-.065,1.265,1.437,iron,.018,-.016,.004)
 panel('Right scavenged chest plate',.07,.79,1.28,1.435,iron2,.019,.009,.004)
 for t in (-.70,-.17,.18,.67):
  for z in (1.30,1.41):fastening(t,z,.027)
 # Soft belt follows the actual mail surface, not the rigid torso envelope.
 belt_verts=[];belt_steps=96
 for i in range(belt_steps+1):
  theta=-math.pi+i*math.tau/belt_steps
  for z in (1.075,1.10):
   origin=Vector((0,-.018,z));direction=Vector((math.sin(theta),-math.cos(theta),0))
   co,norm,_,_=surface.ray_cast(origin,direction,1)
   if co is None:co,norm,_,_=surface.find_nearest(origin+direction*.22)
   assert co is not None
   belt_verts.append(co+direction*.004)
 piece('Close fitting soft leather belt',belt_verts,[(2*i,2*i+1,2*i+3,2*i+2) for i in range(belt_steps)],strapmat,.003,'mail')
 # Paired load-bearing straps run behind the steel plates and over both shoulders.
 over_shoulder(-1);over_shoulder(1)
 for back in (0,math.pi):
  for t in (back-.65,back+.65):
   strip('Plate carrying leather harness',t-.058,t+.058,1.205,1.45,strapmat,.016,4)
   buckle(t,1.239,.024)
   for z in (1.27,1.42):fastening(t,z,.030)
   for edge in (-.043,.043):stitch_line(t+edge,1.21,1.265 if back==0 else 1.45,.021)
 # An articulated lower shield with narrow hangers; no rectangular chest frame.
 for t in (-.24,.24):strip('Shield leather suspension',t-.036,t+.036,.993,1.11,strapmat,.009,3)
 panel('Hanging front groin shield',-.49,.49,.987,1.065,iron,.014,-.006,.004)
 panel('Lower shield overlap',-.42,.42,.927,.997,iron2,.019,.004,.004)
 for t in (-.24,.24):fastening(t,1.039,.015)
 shoulder(-1,False)
elif a.kind=='brigantine':
 # Five broad overlapping sidewall bands, individually cut and stitched.
 shell.data.materials.clear();shell.data.materials.append(canvas)
 for back in (0,math.pi):
  for row in range(5):
   z=1.012+row*.079
   panel('Broad overlapping tyre band',back-1.42,back+1.42,z,z+.093,rubber if row%2 else rubber2,.013+row*.001,.005*(-1)**row,.012)
   for t in (back-.99,back+.91):fastening(t,z+.060,.030)
  # Uprights are on the flanks, leaving broad rubber faces readable.
  for t in (back-1.03,back+.96):
   strip('Narrow flank suspension',t-.040,t+.040,1.035,1.433,strapmat,.032,3)
   for row in range(5):fastening(t,1.045+row*.079,.041)
 belt(-math.pi,math.pi,1.105,.029,.035)
 shoulder(-1,False)
 # Unequal shoulder coverage is supported by a visible repair strap.
 panel('Repaired right upper band',.35,.88,1.345,1.422,iron2,.037,-.014,.003)
 for t in (.43,.79):fastening(t,1.38,.045)
 side_lacing()
 for t in (-1.03,.96):
  buckle(t,1.21,.044)
  for edge in (-.026,.026):stitch_line(t+edge,1.045,1.425,.039)
 # Tyre sidewall moulding and cut lips, interrupted by the carrying straps.
 for back in (0,math.pi):
  for row in range(5):
   z=1.026+row*.079
   for delta in (0,.007):
    tube('Moulded sidewall bead',[torso(back-1.32+2.64*i/32,z+delta,.019+row*.001)[0] for i in range(33)],.0013,rubber2)
else:
 shell.data.materials.clear();shell.data.materials.append(canvas)
 # Large longitudinal tread sections, not a checkerboard of small plates.
 for back in (0,math.pi):
  for col,(t0,t1) in enumerate(((-1.34,-.49),(-.45,.45),(.49,1.34))):
   lo=back+t0;hi=back+t1;z0=1.015+(.022 if col==1 else 0);z1=1.439-(.04 if col!=1 else 0)
   panel('Whole salvaged truck tread segment',lo,hi,z0,z1,rubber,.022,.007*(col-1),.016)
   tread(lo,hi,z0+.025,z1-.02,.043,6)
   for t in (lo+.11,hi-.11):
    fastening(t,z0+.03,.052);fastening(t,z1-.025,.052)
 for z in (1.08,1.29):belt(-math.pi,math.pi,z,.029,.047)
 shoulder(-1,True);shoulder(1,True)
 for side in (-1,1):
  forearm=rig.data.bones['Bip001 '+('L' if side>0 else 'R')+' Forearm'];hand=rig.data.bones['Bip001 '+('L' if side>0 else 'R')+' Hand']
  elbow=rig.matrix_world@forearm.head_local;wrist=rig.matrix_world@hand.head_local
  start=elbow.lerp(wrist,.12);end=elbow.lerp(wrist,.82)
  axis=(end-start).normalized();u=Vector((0,-1,0));v=axis.cross(u).normalized();vs=[];nr=10;nc=12
  for row in range(nr+1):
   for col in range(nc+1):
    angle=-1.9+3.8*col/nc;r=.052+.004*math.sin(math.pi*row/nr)
    vs.append(start.lerp(end,row/nr)+(u*math.cos(angle)+v*math.sin(angle))*r)
  fs=[(r*(nc+1)+c,(r+1)*(nc+1)+c,(r+1)*(nc+1)+c+1,r*(nc+1)+c+1) for r in range(nr) for c in range(nc)]
  piece('Forearm single curved tyre guard',vs,[tuple(reversed(f)) for f in fs],rubber,.012,'surface')
  for row in (2,7):
   pts=[vs[row*(nc+1)+c]*1 for c in range(nc+1)]+[vs[(row+1)*(nc+1)+c]*1 for c in range(nc+1)]
   piece('Forearm leather retaining strap',pts,[(c,c+1,nc+2+c,nc+1+c) for c in range(nc)],strapmat,.006,'surface')
  # Ribbing on the curved guard follows the arm rather than forming square tiles.
  for row in (2,4,6,8):
   path=[]
   for col in range(2,nc-1):
    co=vs[row*(nc+1)+col];center=start.lerp(end,row/nr)
    path.append(co+(co-center).normalized()*.007)
   tube('Forearm casing rib',path,.0035,rubber2,'surface')
 side_lacing()
 for z in (1.094,1.304):
  buckle(-.74,z,.066)
  for t in (-.54,-.40,-.26):fastening(t,z,.066)
 # Metal washers around bolts show how thick rubber is clamped to backing.
 for back in (0,math.pi):
  for t in (-1.18,-.30,.30,1.18):
   for z in (1.068,1.37):
    co,norm=outer_attachment(back+t,z,.054);u=Vector((math.cos(t+back),math.sin(t+back),0));v=Vector((0,0,1))
    tube('Rusty load spreading washer',[co+.006*(u*math.cos(i*math.tau/12)+v*math.sin(i*math.tau/12)) for i in range(13)],.0015,steel)

if a.kind!='chainmail':
 over_shoulder(-1);over_shoulder(1)
 shell.hide_render=True;parts.remove(shell)
 binding_shell=shell;binding_shell.name='Binding surface only';shell=parts[0];shell.name='TEST_'+a.kind+'_Male'
else:binding_shell=None

if a.reference_shirt:
 mesh=bpy.data.meshes.new('LegionGoon reference shirt');mesh.from_pydata(shirt_verts,[],shirt_faces);mesh.update()
 shirt=bpy.data.objects.new('QA actual LegionGoon shirt',mesh);bpy.context.collection.objects.link(shirt)
 shirt.data.materials.append(mat('Reference shirt only',(.12,.135,.105),0,.96));groups={}
 for vertex in mesh.vertices:
  native={data['bones'][i]['name']:w for i,w in zip(m['bone_indices'][vertex.index],m['bone_weights'][vertex.index]) if w>0 and data['bones'][i]['name'] in rig.data.bones}
  total=sum(native.values())
  for bone,weight in native.items():
   if bone not in groups:groups[bone]=shirt.vertex_groups.new(name=bone)
   groups[bone].add([vertex.index],weight/total,'REPLACE')
 mod=shirt.modifiers.new('Native reference skin','ARMATURE');mod.object=rig
 shirt.hide_render=True

# Preserve editable construction in a separate source; export receives one mesh.
scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=24;scene.cycles.use_denoising=True
scene.render.resolution_x=900;scene.render.resolution_y=900;scene.render.resolution_percentage=100
scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs[0].default_value=(.075,.085,.10,1);scene.world.node_tree.nodes['Background'].inputs[1].default_value=.5
for name,loc,power in [('Key',(-2,-3,3),240),('Fill',(2,-1,2),120),('Rim',(0,2,3),210)]:
 bpy.ops.object.light_add(type='AREA',location=loc);o=bpy.context.object;o.name=name;o.data.energy=power;o.data.size=2;o.rotation_euler=(Vector((0,0,1.2))-o.location).to_track_quat('-Z','Y').to_euler()
bpy.ops.object.camera_add(location=(-1,-3,1.8));scene.camera=bpy.context.object;scene.camera.data.type='ORTHO';scene.camera.data.ortho_scale=1.58 if a.kind=='tire' else 1.05
bpy.ops.wm.save_as_mainfile(filepath=str(a.output/(a.kind+'_editable.blend')))
sys.path.insert(0,str(Path(__file__).resolve().parent))
from _ja3_mesh_prepare import prepare_export_mesh
for obj in parts:
 bpy.ops.object.select_all(action='DESELECT');obj.select_set(True);bpy.context.view_layer.objects.active=obj
 # Projection onto the shirt rim can produce identical adjacent samples.
 # Weld only inside this component, at sub-micron tolerance, before thickness.
 bm=bmesh.new();bm.from_mesh(obj.data)
 bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-7)
 bmesh.ops.dissolve_degenerate(bm,edges=list(bm.edges),dist=1e-7)
 bm.normal_update();bm.to_mesh(obj.data);bm.free();obj.data.update()
 for mod in list(obj.modifiers):
  if mod.type!='ARMATURE':bpy.ops.object.modifier_apply(modifier=mod.name)
 if (obj!=shell or a.kind!='chainmail') and len(obj.data.polygons)>30 and not obj.get('detail_wire') and 'rivet' not in obj.name.lower():
  if any(m in (iron,iron2) for m in obj.data.materials):
   obj.data.materials.append(cutedge)
  bev=obj.modifiers.new('Supported cut edge','BEVEL');bev.width=.0008;bev.segments=2;bev.limit_method='ANGLE';bev.angle_limit=.55
  if any(m in (iron,iron2) for m in obj.data.materials):bev.material=len(obj.data.materials)-1
  bpy.ops.object.modifier_apply(modifier=bev.name)
  bm=bmesh.new();bm.from_mesh(obj.data)
  bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-6)
  bmesh.ops.dissolve_degenerate(bm,edges=list(bm.edges),dist=1e-6)
  bm.normal_update();bm.to_mesh(obj.data);bm.free();obj.data.update()
 if not obj.data.uv_layers.get('MailDetail'):obj.data.uv_layers.new(name='MailDetail')
 obj.data.uv_layers.new(name='BakeAtlas');obj.data.uv_layers.active_index=len(obj.data.uv_layers)-1
bpy.ops.object.select_all(action='DESELECT')
for obj in parts:obj.select_set(True)
bpy.context.view_layer.objects.active=shell;bpy.ops.object.join();armor=bpy.context.object
armor.data.uv_layers.active_index=armor.data.uv_layers.find('BakeAtlas');armor.data.uv_layers.active.active_render=True
bpy.ops.object.mode_set(mode='EDIT');bpy.ops.mesh.select_all(action='SELECT');bpy.ops.uv.smart_project(island_margin=.008);bpy.ops.object.mode_set(mode='OBJECT')
for vertex in armor.data.vertices:
 influences=sorted([(g.group,g.weight) for g in vertex.groups if g.weight>0],key=lambda g:g[1],reverse=True)[:4];total=sum(w for _,w in influences)
 assert total>0,('unweighted',vertex.index)
 for g in list(vertex.groups):armor.vertex_groups[g.group].remove([vertex.index])
 for index,w in influences:armor.vertex_groups[index].add([vertex.index],w/total,'REPLACE')
prepare_export_mesh(armor)
body.hide_render=True
if binding_shell is not None:bpy.data.objects.remove(binding_shell,do_unlink=True)
bpy.ops.wm.save_as_mainfile(filepath=str(a.output/(a.kind+'.blend')))
for view,loc in [('front',(0,-3,1.40)),('back',(0,3,1.40)),('side',(3,0,1.40)),('oblique',(-1.8,-3,1.70))]:
 body.hide_render=False
 if a.reference_shirt:shirt.hide_render=False
 scene.camera.location=loc;scene.camera.rotation_euler=(Vector((0,0,1.24))-scene.camera.location).to_track_quat('-Z','Y').to_euler()
 scene.render.filepath=str(a.output/(view+'.png'));bpy.ops.render.render(write_still=True)
(a.output/'status.json').write_text(json.dumps({'kind':a.kind,'status':'REVIEW CANDIDATE; no runtime installation or human acceptance','vertices':len(armor.data.vertices),'triangles':len(armor.data.loop_triangles),'runtime':'NOT_RUN'},indent=2))

