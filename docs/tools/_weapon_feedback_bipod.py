"""Blender offline M14/AK bipod mounting check from decoded vanilla geometry.

--blend assembled-M14.blend --geometry vanilla-bipod.json --output DIR
"""
import argparse,json,sys
from pathlib import Path
import bpy
from mathutils import Vector
p=argparse.ArgumentParser()
for key in ('blend','geometry','output'):p.add_argument('--'+key,type=Path,required=True)
a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);a.output.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(a.blend));sc=bpy.context.scene
d=json.loads(a.geometry.read_text());vertices=[];faces=[]
center=Vector(tuple((d['bbox'][i]+d['bbox'][i+3])/2 for i in range(3)))
for part in d['meshes']:
    offset=len(vertices)
    for v in part['vertices']:
        native=Vector(v)+center+Vector((.56,0,.095));vertices.append((-native.y,-native.x,native.z))
    faces.extend(tuple(offset+i for i in reversed(f)) for f in part['faces'])
mesh=bpy.data.meshes.new('AK bipod');mesh.from_pydata(vertices,[],faces)
obj=bpy.data.objects.new('AK bipod',mesh);sc.collection.objects.link(obj)
mat=bpy.data.materials.new('Bipod');mat.diffuse_color=(.09,.12,.16,1);mesh.materials.append(mat)
sc.render.engine='BLENDER_WORKBENCH';sc.use_nodes=False;sc.render.film_transparent=False
sc.display.shading.color_type='MATERIAL';sc.display.shading.show_cavity=True
sc.render.resolution_x=1200;sc.render.resolution_y=700
cam=sc.camera;target=Vector((0,-.56,.04));cam.data.ortho_scale=.45
for label,view in [('side',(-1,0,.15)),('front',(-.4,-1,.2))]:
    cam.location=target+Vector(view);cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler()
    sc.render.filepath=str(a.output/(label+'.png'));bpy.ops.render.render(write_still=True)
bpy.ops.wm.save_as_mainfile(filepath=str(a.output/'M14-bipod.blend'))
