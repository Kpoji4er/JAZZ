"""Blender close-up QA of an assembled scene, using its actual materials.

--blend FILE --target X,Y,Z --scale METRES --output DIR. Three fixed views.
"""
import argparse,sys
from pathlib import Path
import bpy
from mathutils import Vector
p=argparse.ArgumentParser();p.add_argument('--blend',required=True);p.add_argument('--target',required=True);p.add_argument('--scale',type=float,required=True);p.add_argument('--output',type=Path,required=True)
a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);a.output.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=a.blend,use_scripts=False);s=bpy.context.scene;s.use_nodes=False;s.cycles.samples=16
s.view_settings.view_transform='AgX';s.view_settings.exposure=0;s.render.resolution_x=1000;s.render.resolution_y=800;s.render.film_transparent=False
target=Vector(tuple(map(float,a.target.split(','))));cam=s.camera;cam.data.ortho_scale=a.scale
for name,vec in [('front',(.08,-1,.12)),('reverse',(1,.15,.05)),('under',(-.4,.4,-.8))]:
 cam.location=target+Vector(vec);cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();s.render.filepath=str(a.output/(name+'.png'));bpy.ops.render.render(write_still=True)
