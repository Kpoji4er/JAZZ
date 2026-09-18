"""Render complete armor silhouettes with lowered arms; never changes export meshes."""
import argparse,sys
from pathlib import Path
import bpy
import numpy as np
from mathutils import Vector
p=argparse.ArgumentParser();p.add_argument('--build-root',type=Path,required=True)
a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
for kind,item in [('chainmail','Chainmail'),('brigantine','TireBrigantine'),('tire','TireArmor')]:
 bpy.ops.wm.open_mainfile(filepath=str(a.build_root/kind/'source'/(kind+'.blend')))
 armor=next(o for o in bpy.data.objects if o.type=='MESH' and o.name.startswith('TEST_'));rig=next(o for o in bpy.data.objects if o.type=='ARMATURE')
 for o in bpy.data.objects:
  if o.type=='MESH':o.hide_render=o!=armor
 for side,sign in [('L',1),('R',-1)]:
  bone=rig.pose.bones['Bip001 '+side+' UpperArm'];direction=Vector((sign*.18,0,-1)).normalized()
  local=bone.bone.matrix_local.to_3x3().inverted()@direction
  bone.rotation_mode='QUATERNION';bone.rotation_quaternion=Vector((0,1,0)).rotation_difference(local)
 bpy.context.view_layer.update();scene=bpy.context.scene;cam=scene.camera
 cam.location=(-1,-3,1.8);cam.rotation_euler=(Vector((0,0,1.25))-cam.location).to_track_quat('-Z','Y').to_euler();bpy.context.view_layer.update()
 ev=armor.evaluated_get(bpy.context.evaluated_depsgraph_get());mesh=ev.to_mesh();inv=cam.matrix_world.inverted()
 points=[inv@(armor.matrix_world@v.co) for v in mesh.vertices]
 lo=[min(v[k] for v in points) for k in (0,1)];hi=[max(v[k] for v in points) for k in (0,1)]
 cam.location+=cam.rotation_euler.to_quaternion()@Vector(((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,0))
 cam.data.ortho_scale=max(hi[k]-lo[k] for k in (0,1))*1.12;ev.to_mesh_clear()
 scene.render.resolution_x=110;scene.render.resolution_y=110;scene.render.resolution_percentage=100
 scene.render.film_transparent=True;scene.render.image_settings.color_mode='RGBA';scene.cycles.device='CPU';scene.cycles.samples=96
 scene.render.filepath=str(a.build_root/kind/'build'/(item+'.png'))
 for attempt in range(4):
  bpy.ops.render.render(write_still=True)
  rendered=bpy.data.images.load(scene.render.filepath,check_existing=False)
  rgba=np.array(rendered.pixels[:]).reshape(110,110,4);ys,xs=np.where(rgba[:,:,3]>0);bpy.data.images.remove(rendered)
  if len(xs) and min(xs)>1 and min(ys)>1 and max(xs)<108 and max(ys)<108:break
  cam.data.ortho_scale*=1.2
 else:raise RuntimeError('Clipped icon silhouette: '+item)
