"""Compare installed/candidate skinned geometry against native clothed donor.
Blender --before JSON --after JSON --shirt JSON --sample BLEND --output DIR.
Synthetic clothed poses are not runtime acceptance.
"""
import argparse,json,sys,math
from pathlib import Path
import bpy
from mathutils import Vector
from mathutils.bvhtree import BVHTree
p=argparse.ArgumentParser()
for k in ('before','after','shirt','sample','output'):p.add_argument('--'+k,type=Path,required=True)
a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);a.output.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(a.sample),use_scripts=False);rig=bpy.data.objects['Bip001']
for o in list(bpy.data.objects):
 if o!=rig:bpy.data.objects.remove(o,do_unlink=True)
bpy.context.view_layer.update()
def build(path,label,color,part=None):
 d=json.loads(path.read_text());vs=[];fs=[];ws=[]
 for mi,m in enumerate(d['meshes']):
  if part is not None and mi!=part:continue
  box=m.get('bbox') or d['bbox'];c=[(box[i]+box[i+3])/2 for i in range(3)];offset=len(vs)
  vs.extend((-(v[1]+c[1]),-(v[0]+c[0]),v[2]+c[2]) for v in m['vertices']);fs.extend(tuple(offset+i for i in reversed(f)) for f in m['faces'])
  ws.extend({d['bones'][i]['name']:w for i,w in zip(ids,weights) if w>0 and d['bones'][i]['name'] in rig.data.bones} for ids,weights in zip(m['bone_indices'],m['bone_weights']))
 mesh=bpy.data.meshes.new(label);mesh.from_pydata(vs,[],fs);o=bpy.data.objects.new(label,mesh);bpy.context.collection.objects.link(o);groups={}
 for v,weights in zip(mesh.vertices,ws):
  total=sum(weights.values());assert total>0
  for n,w in weights.items():
   if n not in groups:groups[n]=o.vertex_groups.new(name=n)
   groups[n].add([v.index],w/total,'REPLACE')
 o.modifiers.new('Native skin','ARMATURE').object=rig
 mat=bpy.data.materials.new(label);mat.use_nodes=True;bs=mat.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=(*color,1);bs.inputs['Roughness'].default_value=.75;mesh.materials.append(mat)
 return o
shirt=build(a.shirt,'Shirt',(.28,.04,.025),1);before=build(a.before,'Before',(.22,.27,.20));after=build(a.after,'After',(.22,.27,.20))
scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=16;scene.render.resolution_x=700;scene.render.resolution_y=700;scene.render.resolution_percentage=100;scene.render.film_transparent=False
scene.world=bpy.data.worlds.new('World');scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs[0].default_value=(.09,.09,.09,1);scene.world.node_tree.nodes['Background'].inputs[1].default_value=.7
bpy.ops.object.camera_add(location=(1,2.6,1.95));scene.camera=bpy.context.object;scene.camera.data.type='ORTHO';scene.camera.data.ortho_scale=.86;scene.camera.rotation_euler=(Vector((0,0,1.3))-scene.camera.location).to_track_quat('-Z','Y').to_euler()
for loc in [(1,2,3),(-2,-1,2)]:
 light=bpy.data.lights.new('Key','AREA');light.energy=180;light.size=2;ob=bpy.data.objects.new('Key',light);scene.collection.objects.link(ob);ob.location=loc;ob.rotation_euler=(Vector((0,0,1.3))-ob.location).to_track_quat('-Z','Y').to_euler()
poses={'rest':[], 'lean':[('Bip001 Spine1',(12,0,0)),('Bip001 Spine2',(23,0,12))], 'deep_lean':[('Bip001 Spine1',(28,0,0)),('Bip001 Spine2',(35,0,-18))], 'twist':[('Bip001 Spine1',(0,0,25)),('Bip001 Spine2',(0,0,25))]}
report={}
for pose,rotations in poses.items():
 for bone in rig.pose.bones:bone.rotation_mode='XYZ';bone.rotation_euler=(0,0,0)
 for n,angles in rotations:rig.pose.bones[n].rotation_euler=[math.radians(x) for x in angles]
 bpy.context.view_layer.update();deps=bpy.context.evaluated_depsgraph_get();ev=shirt.evaluated_get(deps);sm=ev.to_mesh();sm.calc_loop_triangles();tree=BVHTree.FromPolygons([v.co for v in sm.vertices],[tuple(t.vertices) for t in sm.loop_triangles],all_triangles=True);report[pose]={}
 for name,o,other in [('before',before,after),('after',after,before)]:
  o.hide_render=False;other.hide_render=True;ae=o.evaluated_get(deps);am=ae.to_mesh();dist=[]
  for base,v in zip(o.data.vertices,am.vertices):
   if base.co.y>.035 and abs(base.co.x)<.17 and 1.08<base.co.z<1.44:
    co,n,_,d=tree.find_nearest(v.co);dist.append((v.co-co).dot(n))
  report[pose][name]={'samples':len(dist),'penetrating_beyond_3mm':sum(x<-.003 for x in dist),'min_signed_m':min(dist) if dist else None}
  ae.to_mesh_clear();scene.render.filepath=str(a.output/(pose+'-'+name+'.png'));bpy.ops.render.render(write_still=True)
 ev.to_mesh_clear()
(a.output/'clearance.json').write_text(json.dumps(report,indent=2));bpy.ops.wm.save_as_mainfile(filepath=str(a.output/'comparison.blend'))
