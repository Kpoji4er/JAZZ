"""Restore US Soldier 2 original mesh parts and packed woodland materials."""
import argparse,sys
from pathlib import Path
import bpy
from mathutils import Vector
p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);a.output.mkdir(parents=True,exist_ok=True);bpy.ops.wm.read_factory_settings(use_empty=True)
materials={}
for kind,base,norm in [('Clothing','HHR_CH3D_US-Soldier-2_DIFF.png','HHR_CH3D_US-Soldier-#2_NRM.png'),('Skin','HHR_CH3D_US-Soldier-#2_Skin_DIFF.png','HHR_CH3D_US-Soldier-#2_Skin_NRM.png'),('Eyes','HHR_CH3D_US-Soldier-#2_Eyes_DIFF.png',None)]:
 mat=bpy.data.materials.new(kind);mat.use_nodes=True;n=mat.node_tree.nodes;l=mat.node_tree.links;bs=n.get('Principled BSDF');bs.inputs['Roughness'].default_value=.85 if kind=='Clothing' else .65
 im=bpy.data.images.load(str(a.source/base));im.pack();tex=n.new('ShaderNodeTexImage');tex.image=im;l.new(tex.outputs['Color'],bs.inputs['Base Color'])
 if norm:
  im=bpy.data.images.load(str(a.source/norm));im.colorspace_settings.name='Non-Color';im.pack();tex=n.new('ShaderNodeTexImage');tex.image=im;normal=n.new('ShaderNodeNormalMap');l.new(tex.outputs['Color'],normal.inputs['Color']);l.new(normal.outputs[0],bs.inputs['Normal'])
 materials[kind]=mat
for idx in range(5):
 verts=[];uv=[];faces=[];faceuv=[]
 for line in (a.source/('model_'+str(idx)+'.obj')).read_text().splitlines():
  s=line.split()
  if not s:continue
  if s[0]=='v':
   x,y,z=map(float,s[1:4]);verts.append((x*.01,-z*.01,y*.01))
  elif s[0]=='vt':uv.append(tuple(map(float,s[1:3])))
  elif s[0]=='f':
   f=[x.split('/') for x in s[1:]];faces.append([int(x[0])-1 for x in f]);faceuv.append([int(x[1])-1 if len(x)>1 and x[1] else None for x in f])
 mesh=bpy.data.meshes.new('Source '+str(idx));mesh.from_pydata(verts,[],faces);mesh.update();obj=bpy.data.objects.new('US_Source_'+str(idx),mesh);bpy.context.collection.objects.link(obj);layer=mesh.uv_layers.new(name='SourceUV')
 for face,ids in zip(mesh.polygons,faceuv):
  for loop,uvindex in zip(face.loop_indices,ids):
   if uvindex is not None:layer.data[loop].uv=uv[uvindex]
  face.use_smooth=True
 mesh.materials.append(materials['Clothing' if idx==2 else 'Skin' if idx==3 else 'Eyes'])
 if not uv:obj.hide_render=True;obj.hide_set(True)
scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=16;scene.cycles.use_denoising=True;scene.render.resolution_x=800;scene.render.resolution_y=1050;scene.render.resolution_percentage=100
scene.world=bpy.data.worlds.new('Studio');scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs[0].default_value=(.12,.12,.12,1)
target=Vector((0,0,1))
for name,loc,power in [('Key',(-2,-3,3),350),('Fill',(2,-1,2),150),('Rim',(0,3,3),250)]:
 bpy.ops.object.light_add(type='AREA',location=loc);o=bpy.context.object;o.name=name;o.data.energy=power;o.data.size=2;o.rotation_euler=(target-o.location).to_track_quat('-Z','Y').to_euler()
bpy.ops.object.camera_add(location=(0,-3,1.3));scene.camera=bpy.context.object;scene.camera.data.type='ORTHO';scene.camera.data.ortho_scale=2.15;scene.camera.rotation_euler=(target-scene.camera.location).to_track_quat('-Z','Y').to_euler()
bpy.ops.wm.save_as_mainfile(filepath=str(a.output/'donor.blend'));scene.render.filepath=str(a.output/'donor_front.png');bpy.ops.render.render(write_still=True)
