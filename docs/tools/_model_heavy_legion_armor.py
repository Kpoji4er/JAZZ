"""Shared HAV geometry, three material families, fitted Male source and CPU preview."""
import argparse,json,sys,math,hashlib
from pathlib import Path
import bpy
from mathutils import Vector
from mathutils.bvhtree import BVHTree
from mathutils.geometry import barycentric_transform
p=argparse.ArgumentParser()
for name in ('source','sample','output'):p.add_argument('--'+name,type=Path,required=True)
p.add_argument('--family',choices=['Twaron','Guardian','Zylon'],required=True)
p.add_argument('--variant',choices=['Light','Medium','Full','Legs','HeavyLegs'],required=True)
p.add_argument('--woodland',type=Path,help='User supplied woodland image; required for Zylon')
a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);a.output.mkdir(parents=True,exist_ok=True)
if a.family=='Zylon' and (not a.woodland or not a.woodland.is_file()):p.error('Zylon requires --woodland image')
bpy.ops.wm.open_mainfile(filepath=str(a.source))
roles={'Light':['vest'],'Medium':['vest','belt','collar','groin'],'Full':['vest','belt','collar','groin','arms'], 'Legs':['thighs'],'HeavyLegs':['thighs','shins']}[a.variant]
parts=[bpy.data.objects['HAV_'+r] for r in roles]
for obj in list(bpy.data.objects):
 if obj.type=='MESH' and obj not in parts:bpy.data.objects.remove(obj,do_unlink=True)
with bpy.data.libraries.load(str(a.sample),link=False) as (src,dst):dst.objects=['Bip001','M_BaseMesh Skin_BIP']
for obj in dst.objects:
 if obj and obj.name not in bpy.context.scene.objects:bpy.context.collection.objects.link(obj)
rig=bpy.data.objects['Bip001'];body=bpy.data.objects['M_BaseMesh Skin_BIP'];body.hide_render=True;body.hide_set(True)
bpy.context.view_layer.update()
body.data.calc_loop_triangles();bv=[body.matrix_world@v.co for v in body.data.vertices];bt=[tuple(t.vertices) for t in body.data.loop_triangles]
bvh=BVHTree.FromPolygons(bv,bt,all_triangles=True)
def weights(pos):
 co,n,idx,d=bvh.find_nearest(pos);ids=bt[idx]
 bary=barycentric_transform(co,*[bv[i] for i in ids],Vector((1,0,0)),Vector((0,1,0)),Vector((0,0,1)));result={}
 for index,f in zip(ids,bary):
  if f<=0:continue
  for g in body.data.vertices[index].groups:
   name=body.vertex_groups[g.group].name
   if name in rig.data.bones:result[name]=result.get(name,0)+f*g.weight
 result=dict(sorted(result.items(),key=lambda t:t[1],reverse=True)[:4]);total=sum(result.values())
 return {n:w/total for n,w in result.items() if w>1e-7}
materials=set()
for obj in parts:
 obj.hide_render=False;obj.hide_set(False)
 bpy.ops.object.select_all(action='DESELECT');obj.select_set(True);bpy.context.view_layer.objects.active=obj
 bpy.ops.object.transform_apply(location=True,rotation=True,scale=True)
 role=obj['armor_part'];obj.vertex_groups.clear();groups={}
 for v in obj.data.vertices:
  co=v.co
  if role in ['vest','collar','arms']:
   upper=max(0,min(1,(co.z-1.2)/.15));shoulder=max(0,min(1,(co.z-1.45)/.1))
   co.x*=1.03;co.y*=1.16
   if co.y<0:co.y-=.055*upper
   co.z-=.075-.025*shoulder
  elif role in ['belt','groin']:co.x*=1.03;co.y*=1.12;co.z-=.055
  else:co.y*=1.12
  skin=weights(co)
  if role in ['vest','collar','belt','groin']:
   # Keep thick torso panels away from nearby arm/leg bone influences.
   # Broad, continuous transitions avoid sharp folds between plate rows.
   centers=[('Bip001 Pelvis',.85),('Bip001 Spine',1.05),('Bip001 Spine1',1.28),('Bip001 Spine2',1.55)]
   skin={name:math.exp(-((co.z-z)/.22)**2) for name,z in centers}
   total=sum(skin.values());skin={name:w/total for name,w in skin.items()}
  elif role=='arms':
   skin={'Bip001 '+('L' if co.x>0 else 'R')+' UpperArm':1.0}
  for name,w in skin.items():
   if name not in groups:groups[name]=obj.vertex_groups.new(name=name)
   groups[name].add([v.index],w,'REPLACE')
 if role=='arms':
  # Each disconnected arm protection follows its nearest arm bone rigidly.
  # Forearm plates must follow elbows rather than remain on the upper arm.
  neighbors={v.index:[] for v in obj.data.vertices}
  for e in obj.data.edges:
   i,j=e.vertices;neighbors[i].append(j);neighbors[j].append(i)
  remaining=set(neighbors)
  while remaining:
   stack=[remaining.pop()];island=[]
   while stack:
    index=stack.pop();island.append(index)
    for other in neighbors[index]:
     if other in remaining:remaining.remove(other);stack.append(other)
   center=sum((obj.data.vertices[i].co for i in island),Vector())/len(island)
   influences={n:w for n,w in weights(center).items() if 'arm' in n.lower()}
   bone=max(influences,key=influences.get) if influences else 'Bip001 '+('L' if center.x>0 else 'R')+' UpperArm'
   for group in obj.vertex_groups:group.remove(island)
   group=obj.vertex_groups.get(bone) or obj.vertex_groups.new(name=bone);group.add(island,1,'REPLACE')
 obj.modifiers.new('Male skin','ARMATURE').object=rig
 obj.data.uv_layers.active.name='SourceUV'
 for mat in obj.data.materials:materials.add(mat)
for mat in materials:
 nodes=mat.node_tree.nodes;links=mat.node_tree.links;bsdf=nodes.get('Principled BSDF')
 source_uv=nodes.new('ShaderNodeUVMap');source_uv.uv_map='SourceUV'
 for node in list(nodes):
  if node.type=='TEX_IMAGE':links.new(source_uv.outputs['UV'],node.inputs['Vector'])
 old=bsdf.inputs['Base Color'].links[0].from_socket
 if a.family=='Guardian':
  hue=nodes.new('ShaderNodeHueSaturation');hue.inputs['Saturation'].default_value=0;hue.inputs['Value'].default_value=.28
  links.new(old,hue.inputs['Color']);links.new(hue.outputs['Color'],bsdf.inputs['Base Color'])
 elif a.family=='Zylon':
  # Apply the supplied pattern unchanged, projected in physical metres.
  # Its wide aspect ratio is preserved: 1.8 m across and ~0.5 m vertically.
  tex=nodes.new('ShaderNodeTexImage');tex.image=bpy.data.images.load(str(a.woodland),check_existing=True);tex.image.pack();tex.extension='REPEAT'
  coords=nodes.new('ShaderNodeTexCoord');split=nodes.new('ShaderNodeSeparateXYZ');links.new(coords.outputs['Object'],split.inputs[0])
  combine=nodes.new('ShaderNodeCombineXYZ')
  for axis,output,scale in [('X','X',1/1.8),('Y','Z',tex.image.size[0]/tex.image.size[1]/1.8)]:
   mul=nodes.new('ShaderNodeMath');mul.operation='MULTIPLY';mul.inputs[1].default_value=scale;links.new(split.outputs[output],mul.inputs[0]);links.new(mul.outputs[0],combine.inputs[axis])
  links.new(combine.outputs[0],tex.inputs['Vector'])
  gray=nodes.new('ShaderNodeRGBToBW');links.new(old,gray.inputs[0])
  detail=nodes.new('ShaderNodeMapRange');detail.inputs['From Min'].default_value=0;detail.inputs['From Max'].default_value=.5;detail.inputs['To Min'].default_value=.45;detail.inputs['To Max'].default_value=1;links.new(gray.outputs[0],detail.inputs['Value'])
  mix=nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1
  links.new(detail.outputs[0],mix.inputs[1]);links.new(tex.outputs['Color'],mix.inputs[2]);links.new(mix.outputs[0],bsdf.inputs['Base Color'])
bpy.ops.object.select_all(action='DESELECT')
for obj in parts:obj.select_set(True)
bpy.context.view_layer.objects.active=parts[0];bpy.ops.object.join();armor=bpy.context.object;armor.name='TEST_'+a.family+a.variant
armor.data.uv_layers.new(name='BakeAtlas');armor.data.uv_layers.active_index=len(armor.data.uv_layers)-1;armor.data.uv_layers.active.active_render=True
bpy.ops.object.mode_set(mode='EDIT');bpy.ops.mesh.select_all(action='SELECT');bpy.ops.uv.smart_project(island_margin=.008);bpy.ops.object.mode_set(mode='OBJECT')
scene=bpy.context.scene;scene.cycles.device='CPU';scene.cycles.samples=32;scene.render.resolution_x=800;scene.render.resolution_y=900
scene.render.film_transparent=False;scene.camera.location=(-1,-3,1.9)
target=Vector((0,0,1.22 if 'Legs' not in a.variant else .6));scene.camera.rotation_euler=(target-scene.camera.location).to_track_quat('-Z','Y').to_euler()
scene.camera.data.ortho_scale=1.12 if a.variant!='Full' else 1.75
geometry=hashlib.sha256(b''.join(float(v).hex().encode() for vertex in armor.data.vertices for v in vertex.co)).hexdigest()
armor.data.calc_loop_triangles();(a.output/'model.json').write_text(json.dumps({'family':a.family,'variant':a.variant,'geometry_sha256':geometry,'triangles':len(armor.data.loop_triangles),'runtime':'NOT_RUN'},indent=2))
bpy.ops.wm.save_as_mainfile(filepath=str(a.output/'model.blend'))
scene.render.filepath=str(a.output/'front.png');bpy.ops.render.render(write_still=True)
