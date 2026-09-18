"""Inspect and prepare supplied woodland uniform on the JA3 Male skeleton."""
import argparse,json,sys,math
from pathlib import Path
import bpy
from mathutils import Vector
p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);a.output.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True)
verts=[];uv=[];faces=[];faceuv=[]
for line in (a.source/'model_0.obj').read_text().splitlines():
 s=line.split()
 if not s:continue
 if s[0]=='v':verts.append(tuple(map(float,s[1:4])))
 elif s[0]=='vt':uv.append(tuple(map(float,s[1:3])))
 elif s[0]=='f':
  f=[x.split('/') for x in s[1:]];faces.append([int(x[0])-1 for x in f]);faceuv.append([int(x[1])-1 for x in f])
mesh=bpy.data.meshes.new('Original uniform mesh');mesh.from_pydata(verts,[],faces);mesh.update();obj=bpy.data.objects.new('DONOR_Complete',mesh);bpy.context.collection.objects.link(obj)
layer=mesh.uv_layers.new(name='SourceUV')
for face,ids in zip(mesh.polygons,faceuv):
 for loop,idx in zip(face.loop_indices,ids):layer.data[loop].uv=uv[idx]
 face.use_smooth=True
mat=bpy.data.materials.new('Original woodland');mat.use_nodes=True;n=mat.node_tree.nodes;l=mat.node_tree.links;bs=n.get('Principled BSDF');bs.inputs['Roughness'].default_value=.85
for suffix,socket in [('_D.png','Base Color'),('_NRM.png',None)]:
 image=bpy.data.images.load(str(next(a.source.glob('*'+suffix))));image.pack();tex=n.new('ShaderNodeTexImage');tex.image=image
 if socket:l.new(tex.outputs['Color'],bs.inputs[socket])
 else:
  image.colorspace_settings.name='Non-Color';normal=n.new('ShaderNodeNormalMap');l.new(tex.outputs['Color'],normal.inputs['Color']);l.new(normal.outputs[0],bs.inputs['Normal'])
mesh.materials.append(mat)
scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=16;scene.cycles.use_denoising=True;scene.render.resolution_x=800;scene.render.resolution_y=1050;scene.render.resolution_percentage=100
scene.world=bpy.data.worlds.new('Studio');scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs[0].default_value=(.12,.12,.12,1)
for name,loc,power in [('Key',(-2,-3,3),350),('Fill',(2,-1,1),150),('Rim',(0,3,2),250)]:
 bpy.ops.object.light_add(type='AREA',location=loc);o=bpy.context.object;o.name=name;o.data.energy=power;o.data.size=2;o.rotation_euler=(-o.location).to_track_quat('-Z','Y').to_euler()
bpy.ops.object.camera_add(location=(0,-3,.3));scene.camera=bpy.context.object;scene.camera.data.type='ORTHO';scene.camera.data.ortho_scale=2.25;scene.camera.rotation_euler=(-scene.camera.location).to_track_quat('-Z','Y').to_euler()
bpy.ops.wm.save_as_mainfile(filepath=str(a.output/'donor.blend'))
scene.render.filepath=str(a.output/'donor_front.png');bpy.ops.render.render(write_still=True)
