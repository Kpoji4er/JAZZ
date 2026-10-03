"""Blender: add a native Shirt08 fit reference and neutral lighting to a rigged vest scene."""
import bpy,json,sys,argparse
from pathlib import Path
from mathutils import Vector
p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--shirt',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);a.output=a.output.resolve();a.output.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(a.source.resolve()));rig=bpy.data.objects['Bip001'];armor=next(o for o in bpy.data.objects if o.name.startswith('TEST_'))
for o in bpy.data.objects:
 if o.type=='MESH' and o!=armor:o.hide_render=True
j=json.loads(a.shirt.read_text());m=j['meshes'][1];b=m.get('bbox') or j['bbox'];c=[(b[i]+b[i+3])/2 for i in range(3)];verts=[(-(v[1]+c[1]),-(v[0]+c[0]),v[2]+c[2]) for v in m['vertices']]
me=bpy.data.meshes.new('Reference shirt');me.from_pydata(verts,[],[tuple(reversed(f)) for f in m['faces']]);o=bpy.data.objects.new('QA actual LegionGoon shirt',me);bpy.context.collection.objects.link(o)
mat=bpy.data.materials.new('Neutral shirt');mat.diffuse_color=(.12,.15,.16,1);mat.use_nodes=True;mat.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value=mat.diffuse_color;mat.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value=.85;me.materials.append(mat)
for f in me.polygons:f.use_smooth=True
groups={}
for v,(ids,ws) in enumerate(zip(m['bone_indices'],m['bone_weights'])):
 valid=[(j['bones'][i]['name'],w) for i,w in zip(ids,ws) if w>0 and j['bones'][i]['name'] in rig.data.bones];total=sum(w for n,w in valid)
 for n,w in valid:
  if n not in groups:groups[n]=o.vertex_groups.new(name=n)
  groups[n].add([v],w/total,'REPLACE')
mod=o.modifiers.new('Native shirt skin','ARMATURE');mod.object=rig
s=bpy.context.scene;s.render.engine='CYCLES';s.cycles.samples=12;s.cycles.use_denoising=True;s.world.use_nodes=True;s.world.node_tree.nodes.get('Background').inputs[1].default_value=.5
for loc,power in [((-2,-3,3),250),((2,-1,3),180),((1,2,3),240)]:
 bpy.ops.object.light_add(type='AREA',location=loc);l=bpy.context.object;l.data.energy=power;l.data.size=2;l.rotation_euler=(Vector((0,0,1.3))-l.location).to_track_quat('-Z','Y').to_euler()
s.render.resolution_x=700;s.render.resolution_y=850;s.render.resolution_percentage=100;s.camera.data.type='ORTHO';s.camera.data.ortho_scale=1.02
bpy.ops.wm.save_as_mainfile(filepath=str((a.output/'clothed.blend').resolve()))
for name,loc in [('front',(0,-3,1.5)),('back',(0,3,1.5)),('side',(3,0,1.5)),('oblique',(2,-3,1.8))]:
 s.camera.location=loc;s.camera.rotation_euler=(Vector((0,0,1.3))-s.camera.location).to_track_quat('-Z','Y').to_euler();s.render.filepath=str(a.output/(name+'.png'));bpy.ops.render.render(write_still=True)
