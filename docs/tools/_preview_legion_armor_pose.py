"""Blender CPU-only pose preview and skin validation; --source <blend> --output <folder>."""
import argparse,sys,json,math
from pathlib import Path
import bpy
from mathutils import Vector
p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);a.output.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(a.source))
armor=next(o for o in bpy.data.objects if o.name.startswith('TEST_ImprovisedCuirass'))
rig=next(o for o in bpy.data.objects if o.type=='ARMATURE')
errors=[]
for v in armor.data.vertices:
    weights=[g.weight for g in v.groups if g.weight>1e-6]
    if not weights or len(weights)>4 or abs(sum(weights)-1)>.0001:errors.append(v.index)
assert not errors,errors[:20]
scene=bpy.context.scene;scene.cycles.device='CPU';scene.cycles.samples=16
scene.render.resolution_x=768;scene.render.resolution_y=768
# Synthetic stress poses are reproducible, but do not substitute JA3 animation.
from mathutils.bvhtree import BVHTree
roles=[v.value for v in armor.data.attributes['qa_role'].data]
anchors=json.loads(armor['qa_anchors'])
assert len(anchors)==12
rest=[v.co.copy() for v in armor.data.vertices]
assert all(math.isfinite(c) for v in rest for c in v)
for v in armor.data.vertices:
 for g in v.groups:
  assert armor.vertex_groups[g.group].name in rig.data.bones
poses={
 'rest':[],
 'lean':[('Bip001 Spine1',(12,0,0)),('Bip001 Spine2',(23,0,12)),('Bip001 R Clavicle',(0,0,-15)),('Bip001 R UpperArm',(0,35,-25))],
 'deep_lean':[('Bip001 Spine1',(28,0,0)),('Bip001 Spine2',(35,0,-18)),('Bip001 R Clavicle',(0,0,-22))],
 'twist':[('Bip001 Spine1',(0,0,25)),('Bip001 Spine2',(0,0,25)),('Bip001 L Clavicle',(0,0,20))],
}
results=[]
for pose,rotations in poses.items():
 for bone in rig.pose.bones:bone.rotation_mode='XYZ';bone.rotation_euler=(0,0,0)
 for name,angles in rotations:rig.pose.bones[name].rotation_euler=[math.radians(v) for v in angles]
 bpy.context.view_layer.update()
 evaluated=armor.evaluated_get(bpy.context.evaluated_depsgraph_get());mesh=evaluated.to_mesh()
 current=[v.co.copy() for v in mesh.vertices];assert len(current)==len(rest)
 plates={side:BVHTree.FromPolygons(current,[tuple(p.vertices) for p in mesh.polygons if all(roles[i]==role for i in p.vertices)]) for side,role in ((-1,1),(1,2))}
 gaps=[];signed_gaps=[]
 for anchor in anchors:
  point=Vector((0,0,0))
  for name,w in anchor['weights'].items():
   transform=rig.pose.bones[name].matrix@rig.data.bones[name].matrix_local.inverted()
   point+=(transform@Vector(anchor['position']))*w
  co,n,_,gap=plates[anchor['side']].find_nearest(point);gaps.append(gap)
  signed=(point-co).dot(n);signed_gaps.append(signed)
  assert signed>0,(pose,'anchor inside plate',signed)
  assert gap<.018,(pose,'detached strap anchor',gap)
 # The actual bottom-edge mesh must stay rigid locally; spikes require strain.
 stretches=[]
 for edge in armor.data.edges:
  i,j=edge.vertices
  if roles[i] in (2,3) and roles[j] in (2,3) and max(rest[i].z,rest[j].z)<1.11:
   length=(rest[i]-rest[j]).length
   if length>1e-6:stretches.append((current[i]-current[j]).length/length)
 assert stretches and max(stretches)<1.02 and min(stretches)>.98,(pose,'lower rim strain',min(stretches),max(stretches))
 # Bind each declared anchor to the actual strap vertices as well.
 strap=BVHTree.FromPolygons(current,[tuple(p.vertices) for p in mesh.polygons if all(roles[i]==4 for i in p.vertices)])
 for anchor in anchors:
  point=sum((((rig.pose.bones[name].matrix@rig.data.bones[name].matrix_local.inverted())@Vector(anchor['position']))*w for name,w in anchor['weights'].items()),Vector((0,0,0)))
  assert strap.find_nearest(point)[3]<.012,(pose,'missing leather at anchor')
 results.append({'pose':pose,'anchor_max_gap_m':max(gaps),'anchor_min_signed_gap_m':min(signed_gaps),'lower_rim_min_stretch':min(stretches),'lower_rim_max_stretch':max(stretches)})
 evaluated.to_mesh_clear()
 for side,loc in [('front',(-1,-2.6,1.95)),('back',(1,2.6,1.95))]:
  scene.camera.location=loc;scene.camera.rotation_euler=(Vector((0,0,1.25))-scene.camera.location).to_track_quat('-Z','Y').to_euler()
  scene.camera.data.ortho_scale=.9;scene.render.filepath=str(a.output/(pose+'_'+side+'.png'));bpy.ops.render.render(write_still=True)
report={'skin_validation':'PASS','vertices':len(armor.data.vertices),'max_influences':max(sum(g.weight>1e-6 for g in v.groups) for v in armor.data.vertices),'poses':results,'runtime':'NOT_RUN; synthetic poses do not prove collision-free JA3 animations','device':'CPU'}
(a.output/'pose-check.json').write_text(json.dumps(report,indent=2));print(report)
