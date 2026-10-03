"""Blender: --blend FILE --output DIR. Both sides of assembled magazine well."""
import argparse,sys
from pathlib import Path
import bpy
from mathutils import Vector
p=argparse.ArgumentParser();p.add_argument('--blend',required=True);p.add_argument('--output',type=Path,required=True)
a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);a.output.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=a.blend,use_scripts=False)
for o in bpy.context.scene.objects:
 if o.type=='MESH':o.hide_render=o.name not in ('JAZZ_HK416_Standard','JAZZ_HK416_Magazine')
s=bpy.context.scene;s.use_nodes=False;s.render.engine='CYCLES';s.cycles.samples=24
s.render.resolution_x=1000;s.render.resolution_y=800;s.render.resolution_percentage=100
s.render.film_transparent=True;s.view_settings.view_transform='Standard'
cam=s.camera;cam.data.type='ORTHO';cam.data.ortho_scale=.26
target=Vector((0,-.07,.015))
for side in (-1,1):
 cam.location=target+Vector((side*2,0,-.1));cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler()
 s.render.filepath=str(a.output/f'magwell-{side}.png');bpy.ops.render.render(write_still=True)
