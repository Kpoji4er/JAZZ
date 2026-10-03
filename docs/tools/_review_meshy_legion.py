"""Blender clothed reference review: --source BLEND --shirt decoded JSON --output DIR.
Native Shirt08 geometry/weights, neutral material, rest and synthetic lean only.
"""
import argparse,json,math,sys
from pathlib import Path
import bpy
from mathutils import Vector
p=argparse.ArgumentParser()
for k in ('source','shirt','output'):p.add_argument('--'+k,type=Path,required=True)
a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);a.output=a.output.resolve();a.source=a.source.resolve();a.output.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(a.source));rig=bpy.data.objects['Bip001']
armor=next(o for o in bpy.data.objects if o.name.startswith('TEST_'))
for o in bpy.data.objects:
 if o.type=='MESH':o.hide_render=o!=armor
s=json.loads(a.shirt.read_text());m=s['meshes'][1];bb=m.get('bbox') or s['bbox'];c=[(bb[i]+bb[i+3])/2 for i in range(3)]
vs=[(-(v[1]+c[1]),-(v[0]+c[0]),v[2]+c[2]) for v in m['vertices']]
me=bpy.data.meshes.new('Native Shirt08');me.from_pydata(vs,[],[tuple(reversed(f)) for f in m['faces']]);me.update()
shirt=bpy.data.objects.new('Native Shirt08',me);bpy.context.collection.objects.link(shirt)
mat=bpy.data.materials.new('Clothing reference');mat.diffuse_color=(.12,.23,.28,1);mat.use_nodes=True;mat.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value=mat.diffuse_color;me.materials.append(mat)
for i,(ids,ws) in enumerate(zip(m['bone_indices'],m['bone_weights'])):
 pairs=[(s['bones'][n]['name'],w) for n,w in zip(ids,ws) if w>0 and s['bones'][n]['name'] in rig.data.bones];total=sum(w for _,w in pairs)
 for n,w in pairs:(shirt.vertex_groups.get(n) or shirt.vertex_groups.new(name=n)).add([i],w/total,'REPLACE')
shirt.modifiers.new('Native skeleton','ARMATURE').object=rig
scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=12;scene.render.resolution_x=700;scene.render.resolution_y=700;scene.render.resolution_percentage=100
scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs[0].default_value=(.25,.28,.32,1);scene.world.node_tree.nodes['Background'].inputs[1].default_value=.7
focus=Vector((0,0,1.30))
for pos in [(2,-3,4),(-2,-1,3),(0,3,3)]:
 bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.data.energy=300;o.data.size=3;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
scene.camera.data.type='ORTHO';scene.camera.data.ortho_scale=1.05
for pose in ['rest','lean']:
 for b in rig.pose.bones:b.rotation_mode='XYZ';b.rotation_euler=(0,0,0)
 if pose=='lean':
  rig.pose.bones['Bip001 Spine1'].rotation_euler=(.21,0,0);rig.pose.bones['Bip001 Spine2'].rotation_euler=(.40,0,.2)
 bpy.context.view_layer.update()
 for side,loc in [('front',(0,-3,1.5)),('back',(0,3,1.5)),('side',(3,0,1.5))]:
  scene.camera.location=loc;scene.camera.rotation_euler=(focus-scene.camera.location).to_track_quat('-Z','Y').to_euler();scene.render.filepath=str(a.output/(pose+'_'+side+'.png'));bpy.ops.render.render(write_still=True)
