"""Blender offline normal-map comparison; --blend FILE --output DIR --family vz58|r4.

Produces matching original / no-normal / flipped-green renders without touching
installed assets. Optional --wood DIR consumes approved Wood/StockWood_Base.png.
"""
import argparse, sys
from pathlib import Path
import bpy
from mathutils import Vector

p=argparse.ArgumentParser()
p.add_argument('--blend',type=Path,required=True)
p.add_argument('--output',type=Path,required=True)
p.add_argument('--family',choices=['vz58','r4'],required=True)
p.add_argument('--wood',type=Path)
p.add_argument('--final',action='store_true',help='One material render and VZ58 side icon')
a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
a.output=a.output.resolve()
if a.wood:a.wood=a.wood.resolve()
a.output.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(a.blend))
active={'JAZZ_VZ58','JAZZ_VZ58_StockWood','JAZZ_VZ58_HandguardWood','JAZZ_VZ58_GripWood','JAZZ_VZ58_Magazine'}
objects=[o for o in bpy.context.scene.objects if o.type=='MESH']
for o in objects:o.hide_render=a.family=='vz58' and o.name not in active
visible=[o for o in objects if not o.hide_render]
if a.wood:
 for mat in bpy.data.materials:
  if not mat.use_nodes:continue
  for n in mat.node_tree.nodes:
   if n.type=='TEX_IMAGE' and n.image:
    for key in ('Wood','StockWood'):
     if n.image.name=='JAZZ_VZ58_'+key+'_Base':
      n.image=bpy.data.images.load(str(a.wood/(key+'_Base.png')))
scene=bpy.context.scene
scene.render.engine='CYCLES';scene.cycles.samples=16
scene.render.resolution_x=1200;scene.render.resolution_y=460;scene.render.resolution_percentage=100
scene.render.film_transparent=True;scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA'
scene.view_settings.view_transform='Standard';scene.view_settings.look='None'
scene.world=bpy.data.worlds.new('ReviewWorld');scene.world.use_nodes=True
scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.3
pts=[o.matrix_world@Vector(v) for o in visible for v in o.bound_box]
target=Vector(tuple((min(v[i] for v in pts)+max(v[i] for v in pts))/2 for i in range(3)))
cam=bpy.data.cameras.new('ReviewCamera');cam.type='ORTHO';cam.ortho_scale=1.12 if a.family=='r4' else .94
camera=bpy.data.objects.new('ReviewCamera',cam);scene.collection.objects.link(camera);scene.camera=camera
camera.location=target+Vector((-2,0,0));camera.rotation_euler=(target-camera.location).to_track_quat('-Z','Y').to_euler()
for i,offset in enumerate([(-1,-.5,1.5),(-.5,.5,1),(1,1,0)]):
 light=bpy.data.lights.new('ReviewLight'+str(i),'AREA');light.energy=25;light.size=1.5
 o=bpy.data.objects.new(light.name,light);scene.collection.objects.link(o);o.location=target+Vector(offset);o.rotation_euler=(target-o.location).to_track_quat('-Z','Y').to_euler()
normals=[n for mat in bpy.data.materials if mat.use_nodes for n in mat.node_tree.nodes if n.type=='NORMAL_MAP']
for mode in (('original',) if a.final else ('original','no-normal','flip-green')):
 for n in normals:n.inputs['Strength'].default_value=0 if mode=='no-normal' else 1
 if mode=='flip-green':
  for mat in bpy.data.materials:
   if not mat.use_nodes:continue
   for n in list(mat.node_tree.nodes):
    if n.type!='NORMAL_MAP' or not n.inputs['Color'].is_linked:continue
    socket=n.inputs['Color'].links[0].from_socket
    curve=mat.node_tree.nodes.new('ShaderNodeRGBCurve');curve.mapping.curves[1].points[0].location=(0,1);curve.mapping.curves[1].points[1].location=(1,0);curve.mapping.update()
    mat.node_tree.links.new(socket,curve.inputs['Color']);mat.node_tree.links.new(curve.outputs['Color'],n.inputs['Color'])
 scene.render.filepath=str(a.output/(a.family+'-'+mode+'.png'));bpy.ops.render.render(write_still=True)
if a.final and a.family=='vz58':
 sys.path.insert(0,str(Path(__file__).resolve().parent))
 from _render_ak103_icon import build_compositor
 build_compositor(scene)
 scene.cycles.samples=64;scene.render.resolution_x=324;scene.render.resolution_y=165;cam.ortho_scale=.94
 scene.render.filepath=str(a.output/'VZ58_icon.png');bpy.ops.render.render(write_still=True)
