"""Offline author-PBR inspection and inventory icons for both AEK configurations.
Blender --python THIS -- --build DIR. Does not install or change source meshes.
"""
import argparse,json,sys
from pathlib import Path
import bpy
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent))
from _render_ak103_icon import build_compositor
p=argparse.ArgumentParser();p.add_argument('--build',type=Path,required=True)
a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
bpy.ops.wm.open_mainfile(filepath=str(a.build/'rigged/AEK_JA3.blend'),use_scripts=False)
scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=32
scene.render.film_transparent=True;scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA';scene.render.resolution_percentage=100
scene.view_settings.view_transform='Standard';scene.view_settings.look='None'
scene.world=bpy.data.worlds.new('InspectionWorld');scene.world.use_nodes=True
scene.world.node_tree.nodes.get('Background').inputs['Strength'].default_value=.25
cam=bpy.data.cameras.new('InspectionCamera');cam.type='ORTHO';camera=bpy.data.objects.new(cam.name,cam);scene.collection.objects.link(camera);scene.camera=camera
lights=[]
for i,offset in enumerate([(-1,-.5,1.5),(-.5,.5,1),(1,1,0)]):
 data=bpy.data.lights.new('InspectionLight'+str(i),'AREA');data.energy=25;data.size=1.5
 ob=bpy.data.objects.new(data.name,data);scene.collection.objects.link(ob);lights.append((ob,Vector(offset)))
nodes=build_compositor(scene);report={};meshes=[o for o in scene.objects if o.type=='MESH']
for variant in ('971','973S'):
 for folded in (False,True):
  names={'JAZZ_AEK'+variant,'JAZZ_AEK'+variant+'_Magazine','JAZZ_AEK'+variant+('_StockFolded' if folded else '_Stock')}
  for o in meshes:o.hide_render=o.name not in names
  bpy.context.view_layer.update()
  pts=[o.matrix_world@Vector(v) for o in meshes if not o.hide_render for v in o.bound_box]
  lo=Vector([min(v[i] for v in pts) for i in range(3)]);hi=Vector([max(v[i] for v in pts) for i in range(3)]);target=(lo+hi)/2
  for icon in (False,True):
   w,h=(324,165) if icon else (1400,650);scene.render.resolution_x=w;scene.render.resolution_y=h;scene.use_nodes=icon
   cam.ortho_scale=max(hi.y-lo.y,(hi.z-lo.z)*w/h)*(1.25 if icon else 1.12)
   camera.location=target+Vector((-2,0,.20 if icon else .4));camera.rotation_euler=(target-camera.location).to_track_quat('-Z','Y').to_euler()
   for light,offset in lights:light.location=target+offset;light.rotation_euler=(target-light.location).to_track_quat('-Z','Y').to_euler()
   name='AEK'+variant+('_Folded' if folded else '')+('_icon' if icon else '_pbr')
   scene.render.filepath=str(a.build/'previews'/(name+'.png'));bpy.ops.render.render(write_still=True)
   report[name]={'path':scene.render.filepath,'size':[w,h],'engine':'Cycles CPU','source_materials':True}
(a.build/'render-report.json').write_text(json.dumps(report,indent=2))
