"""Withdrawn prototype helper: bind LDW soldier to the official JA3 Male rest skeleton.

JAZZ-APPEAR-001-REQ-023: do not install JAZZ_SpecOpsBody_Male / JAZZ_Legion_SpecOpsTest.
The in-game entity was removed; this script stays as source-only tooling.
"""
import argparse,sys,json
from pathlib import Path
import bpy
from mathutils import Vector
from mathutils.bvhtree import BVHTree
from mathutils.geometry import barycentric_transform
p=argparse.ArgumentParser()
for k in ('source','sample','output'):p.add_argument('--'+k,type=Path,required=True)
a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);a.output.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(a.source));armor=bpy.data.objects['DONOR_Complete'];armor.name='TEST_SpecOps'
with bpy.data.libraries.load(str(a.sample),link=False) as (src,dst):dst.objects=['Bip001','M_BaseMesh Skin_BIP']
for obj in dst.objects:bpy.context.collection.objects.link(obj)
rig,body=dst.objects;body.hide_render=True;body.hide_set(True);bpy.context.view_layer.update()
body.data.calc_loop_triangles();bv=[body.matrix_world@v.co for v in body.data.vertices];bt=[tuple(t.vertices) for t in body.data.loop_triangles];surface=BVHTree.FromPolygons(bv,bt,all_triangles=True)
z0=min(v.co.z for v in armor.data.vertices);z1=max(v.co.z for v in armor.data.vertices)
floor=min(v.z for v in bv);top=max(v.z for v in bv);scale=(top-floor)/(z1-z0)
groups={}
for v in armor.data.vertices:
 v.co=Vector((v.co.x*scale,v.co.y*scale,(v.co.z-z0)*scale+floor))
 q,_,idx,_=surface.find_nearest(v.co);ids=bt[idx];b=barycentric_transform(q,*[bv[i] for i in ids],Vector((1,0,0)),Vector((0,1,0)),Vector((0,0,1)));weights={}
 for i,f in zip(ids,b):
  for g in body.data.vertices[i].groups:
   n=body.vertex_groups[g.group].name
   if f>0 and n in rig.data.bones:weights[n]=weights.get(n,0)+f*g.weight
 weights=dict(sorted(weights.items(),key=lambda t:t[1],reverse=True)[:4]);s=sum(weights.values());assert s>0
 for n,w in weights.items():
  if n not in groups:groups[n]=armor.vertex_groups.new(name=n)
  groups[n].add([v.index],w/s,'REPLACE')
armor.modifiers.new('JA3 Male skin','ARMATURE').object=rig
scene=bpy.context.scene
for obj in scene.objects:
 if obj.type=='LIGHT':obj.location.z+=.9
target=Vector((0,0,.92));scene.camera.location=(-.8,-3,1.5);scene.camera.rotation_euler=(target-scene.camera.location).to_track_quat('-Z','Y').to_euler();scene.camera.data.ortho_scale=2.05
bpy.context.view_layer.update();bpy.ops.wm.save_as_mainfile(filepath=str(a.output/'model.blend'))
scene.render.filepath=str(a.output/'rest_front.png');bpy.ops.render.render(write_still=True)
scene.camera.location=(.8,3,1.5);scene.camera.rotation_euler=(target-scene.camera.location).to_track_quat('-Z','Y').to_euler();scene.render.filepath=str(a.output/'rest_back.png');bpy.ops.render.render(write_still=True)
(a.output/'source-report.json').write_text(json.dumps({'scale':scale,'vertices':len(armor.data.vertices),'bones':len(groups),'method':'uniform scale only; barycentric official sample skin top4','runtime':'NOT_RUN'},indent=2))
