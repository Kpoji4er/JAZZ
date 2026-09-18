"""Import HGM JSON clothing into the calibrated sample and screen cuirass fit.
CPU-only rest fit: signed nearest-surface samples flag candidates, not runtime PASS.
"""
import bpy,argparse,sys,json,collections
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
p=argparse.ArgumentParser()
for key in ('source','models','roster','output'):p.add_argument('--'+key,type=Path,required=True)
p.add_argument('--skip-renders',action='store_true')
a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);a.output.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(a.source));armor=next(o for o in bpy.data.objects if o.name.startswith('TEST_ImprovisedCuirass'));rig=bpy.data.objects['Bip001']
for o in bpy.data.objects:
 if o.type=='MESH' and o!=armor:o.hide_render=True;o.hide_set(True)
material=bpy.data.materials.new('Vanilla clothing geometry reference');material.use_nodes=True
shader=material.node_tree.nodes.get('Principled BSDF');shader.inputs['Base Color'].default_value=(.08,.17,.20,1);shader.inputs['Roughness'].default_value=.8
roster=json.loads(a.roster.read_text());bodies={};results=[]
roles=[v.value for v in armor.data.attributes['qa_role'].data]
for name in roster['unique_bodies']:
 file=a.models/(name+'_mesh.json')
 if not file.exists():raise RuntimeError('Missing exact mesh '+str(file))
 data=json.loads(file.read_text());objects=[];positions=[];triangles=[];missing=set()
 for k,m in enumerate(data['meshes']):
  box=m['bbox'] or data['bbox'];c=[(box[i]+box[i+3])*.5 for i in range(3)]
  verts=[(-(v[1]+c[1]),-(v[0]+c[0]),v[2]+c[2]) for v in m['vertices']]
  faces=[tuple(reversed(f)) for f in m['faces']]
  mesh=bpy.data.meshes.new(name+str(k));mesh.from_pydata(verts,[],faces);mesh.update()
  obj=bpy.data.objects.new(name+str(k),mesh);bpy.context.collection.objects.link(obj);obj.data.materials.append(material)
  for face in mesh.polygons:face.use_smooth=True
  if data['bones'] and m['bone_indices']:
   groups={}
   for i,(indices,weights) in enumerate(zip(m['bone_indices'],m['bone_weights'])):
    total=sum(weights)
    for idx,w in zip(indices,weights):
     if w<=0:continue
     bone=data['bones'][idx]['name']
     if bone not in rig.data.bones:missing.add(bone)
     if bone not in groups:groups[bone]=obj.vertex_groups.new(name=bone)
     groups[bone].add([i],w/total,'REPLACE')
   if not missing:
    mod=obj.modifiers.new('Original Male weights','ARMATURE');mod.object=rig
   obj['qa_animation_ready']=not bool(missing)
  base=len(positions);positions.extend(verts);triangles.extend(tuple(base+i for i in f) for f in faces)
  obj.hide_render=True;obj.hide_set(True);objects.append(obj)
 bvh=BVHTree.FromPolygons(positions,triangles,all_triangles=True)
 candidates=[];samples=0
 for i,v in enumerate(armor.data.vertices):
  if roles[i] not in (1,2):continue
  if i%4:continue
  co,n,idx,dist=bvh.find_nearest(v.co);samples+=1
  signed=(v.co-co).dot(n)
  if -.06<signed<-.003:candidates.append(i)
 row={'body':name,'vertices':len(positions),'missing_bones':sorted(missing),'sampled_plate_vertices':samples,'penetration_candidates':len(candidates),'status':'REST_SCREEN_ONLY; requires visual review and JA3 poses'}
 results.append(row);bodies[name]=objects
scene=bpy.context.scene;scene.cycles.device='CPU';scene.cycles.samples=12
scene.render.resolution_x=768;scene.render.resolution_y=768;scene.render.resolution_percentage=100
bpy.ops.wm.save_as_mainfile(filepath=str(a.output/'jazz-body-fit.blend'))
selected=['NPCCostumeMale_Shirt_08','Faction_Legion_Top_09','Faction_Legion_Top_08','EquipmentBiff_Top','Faction_Rebels_Top_Heavy']
for name in ([] if a.skip_renders else selected):
 for obj in bodies[name]:obj.hide_render=False;obj.hide_set(False)
 for side,loc in [('front',(-1,-2.6,1.95)),('back',(1,2.6,1.95))]:
  scene.camera.location=loc;scene.camera.rotation_euler=(Vector((0,0,1.25))-scene.camera.location).to_track_quat('-Z','Y').to_euler();scene.camera.data.ortho_scale=.95
  scene.render.filepath=str(a.output/(name+'_'+side+'.png'));bpy.ops.render.render(write_still=True)
 for obj in bodies[name]:obj.hide_render=True;obj.hide_set(True)
(a.output/'fit-report.json').write_text(json.dumps({'bodies':results,'rendered':selected,'runtime':'NOT_RUN','coordinates':'calibrated HGM -> sample; x=-y,y=-x,z=z after bbox center'},indent=2));print('Imported',len(bodies),'bodies')
