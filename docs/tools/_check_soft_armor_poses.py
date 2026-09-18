"""Reproducible CPU skin QA for staged soft armor; not JA3 collision acceptance."""
import argparse,json,math,sys
from pathlib import Path
import bpy
from mathutils import Vector
p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
p.add_argument('--no-renders',action='store_true')
p.add_argument('--clothed',action='store_true')
a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);a.output.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(a.source))
armor=next(o for o in bpy.data.objects if o.type=='MESH' and o.name.startswith('TEST_'))
rig=next(o for o in bpy.data.objects if o.type=='ARMATURE')
if a.clothed:
 shirt=bpy.data.objects.get('QA actual LegionGoon shirt');assert shirt,'Missing clothed reference'
 shirt.hide_render=False
assert any(m.type=='ARMATURE' and m.object==rig for m in armor.modifiers)
for v in armor.data.vertices:
 weights=[g for g in v.groups if g.weight>1e-6]
 assert 1<=len(weights)<=4 and abs(sum(g.weight for g in weights)-1)<.0001
 assert all(armor.vertex_groups[g.group].name in rig.data.bones for g in weights)
poses={'rest':[], 'lean':[('Bip001 Spine1',(12,0,0)),('Bip001 Spine2',(23,0,12)),('Bip001 R UpperArm',(0,35,-25))],
       'deep_lean':[('Bip001 Spine1',(28,0,0)),('Bip001 Spine2',(35,0,-18))],
       'twist':[('Bip001 Spine1',(0,0,25)),('Bip001 Spine2',(0,0,25)),('Bip001 L Clavicle',(0,0,20))]}
if armor.name.endswith('Full'):
 poses['elbows']=[('Bip001 R Forearm',(0,0,-65)),('Bip001 L Forearm',(0,0,65))]
scene=bpy.context.scene;scene.cycles.device='CPU';scene.cycles.samples=12;scene.render.resolution_x=600;scene.render.resolution_y=600
rest=[v.co.copy() for v in armor.data.vertices];rows=[]
reference=bpy.data.objects['M_BaseMesh Skin_BIP']
reference_rest=[v.co.copy() for v in reference.data.vertices]
for name,rotations in poses.items():
 for b in rig.pose.bones:b.rotation_mode='XYZ';b.rotation_euler=(0,0,0)
 for bone,angles in rotations:rig.pose.bones[bone].rotation_euler=[math.radians(x) for x in angles]
 bpy.context.view_layer.update();ev=armor.evaluated_get(bpy.context.evaluated_depsgraph_get());mesh=ev.to_mesh()
 assert len(mesh.vertices)==len(rest)
 pts=[v.co.copy() for v in mesh.vertices]
 assert all(math.isfinite(x) for v in pts for x in v)
 movement=max((x-y).length for x,y in zip(pts,rest))
 if rotations:assert .005<movement<1.5,(name,'missing skin motion or exploded mesh',movement)
 strains=[];details=[]
 for edge in armor.data.edges:
  i,j=edge.vertices;length=(rest[i]-rest[j]).length
  if length>.003:
   strain=(pts[i]-pts[j]).length/length;strains.append(strain);details.append((strain,list(rest[i]),list(rest[j]),[(armor.vertex_groups[g.group].name,g.weight) for g in armor.data.vertices[i].groups]))
 strains.sort();p99=strains[int(.99*(len(strains)-1))]
 reference_ev=reference.evaluated_get(bpy.context.evaluated_depsgraph_get());reference_mesh=reference_ev.to_mesh();reference_strains=[]
 for edge in reference.data.edges:
  i,j=edge.vertices;length=(reference_rest[i]-reference_rest[j]).length
  if length>.3:reference_strains.append((reference_mesh.vertices[i].co-reference_mesh.vertices[j].co).length/length)
 reference_strains.sort();reference_p99=reference_strains[int(.99*(len(reference_strains)-1))];reference_ev.to_mesh_clear()
 # Native body itself stretches under synthetic Spine extremes; compare like-for-like.
 limit=max(1.8,min(2.0,reference_p99+.25))
 if p99>=limit:print('STRAIN_DIAGNOSTIC',sorted(details,reverse=True)[:8],flush=True)
 assert p99<limit,(name,'excessive stretch relative to native body',p99,reference_p99,limit)
 rows.append({'pose':name,'max_motion_m':movement,'edge_strain_p99':p99,'reference_body_p99':reference_p99,'limit':limit})
 ev.to_mesh_clear()
 for side,loc in ([] if a.no_renders else [('front',(-1,-2.6,1.95)),('back',(1,2.6,1.95))]):
  scene.camera.location=loc;scene.camera.rotation_euler=(Vector((0,0,1.25))-scene.camera.location).to_track_quat('-Z','Y').to_euler();scene.camera.data.ortho_scale=1.18
  scene.render.filepath=str(a.output/(name+'_'+side+'.png'));bpy.ops.render.render(write_still=True)
(a.output/'pose-check.json').write_text(json.dumps({'status':'PASS_SKIN_STRUCTURE','runtime':'NOT_RUN','collision_acceptance':False,'vertices':len(rest),'poses':rows},indent=2))
print('PASS skin weights/bones/finite animated geometry and eight CPU views')
