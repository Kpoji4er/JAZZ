"""Blender review of existing weapon meshes with decoded installed material maps.

--blend FILE --entity NAME --maps DIR --output DIR [--no-normal]
Maps are entity_Base/Normal/RM/AO.png produced from installed DDS, not old bake files.
Renders both sides with identical light. Does not change source or installed assets.
"""
import argparse, json, sys
from pathlib import Path
import bpy
from mathutils import Vector

p=argparse.ArgumentParser()
for key in ('blend','entity','maps','output'):p.add_argument('--'+key,required=True)
p.add_argument('--no-normal',action='store_true')
a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
out=Path(a.output);out.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=a.blend,use_scripts=False)
obj=bpy.data.objects[a.entity]
for other in bpy.context.scene.objects:
    if other.type=='MESH':other.hide_render=other!=obj
mat=bpy.data.materials.new('Installed material review');mat.use_nodes=True
nodes=mat.node_tree.nodes;links=mat.node_tree.links;bsdf=nodes.get('Principled BSDF')
for key in ('Base','Normal','RM','AO'):
    path=Path(a.maps)/(a.entity+'_'+key+'.png')
    if not path.exists():continue
    im=bpy.data.images.load(str(path));im.colorspace_settings.name='sRGB' if key=='Base' else 'Non-Color'
    n=nodes.new('ShaderNodeTexImage');n.image=im
    if key=='Base':links.new(n.outputs['Color'],bsdf.inputs['Base Color'])
    elif key=='Normal' and not a.no_normal:
        nm=nodes.new('ShaderNodeNormalMap');links.new(n.outputs['Color'],nm.inputs['Color']);links.new(nm.outputs['Normal'],bsdf.inputs['Normal'])
    elif key=='RM':
        sep=nodes.new('ShaderNodeSeparateColor');links.new(n.outputs['Color'],sep.inputs[0])
        links.new(sep.outputs[0],bsdf.inputs['Roughness']);links.new(sep.outputs[2],bsdf.inputs['Metallic'])
obj.data.materials.clear();obj.data.materials.append(mat)
sc=bpy.context.scene;sc.render.engine='CYCLES';sc.cycles.samples=16
sc.render.resolution_x=1200;sc.render.resolution_y=640;sc.render.resolution_percentage=100
sc.render.film_transparent=False;sc.render.image_settings.file_format='PNG'
sc.view_settings.view_transform='AgX';sc.use_nodes=False
sc.world=bpy.data.worlds.new('Review');sc.world.use_nodes=True
sc.world.node_tree.nodes['Background'].inputs[0].default_value=(.16,.16,.16,1)
sc.world.node_tree.nodes['Background'].inputs[1].default_value=.5
for ob in list(sc.objects):
    if ob.type in ('CAMERA','LIGHT'):bpy.data.objects.remove(ob,do_unlink=True)
pts=[obj.matrix_world@Vector(v) for v in obj.bound_box]
lo=Vector(tuple(min(v[i] for v in pts) for i in range(3)));hi=Vector(tuple(max(v[i] for v in pts) for i in range(3)));center=(lo+hi)/2
span=max(hi-lo)
cam=bpy.data.objects.new('ReviewCamera',bpy.data.cameras.new('ReviewCamera'));sc.collection.objects.link(cam);sc.camera=cam
cam.data.type='ORTHO';cam.data.ortho_scale=span*1.12
for side in (-1,1):
    lights=[]
    for i,(offset,power,size) in enumerate([((side,-.4,1.2),65,.6),((side,.6,.2),25,.8)]):
        light=bpy.data.lights.new('ReviewLight','AREA');light.energy=power;light.size=size
        ob=bpy.data.objects.new(light.name,light);sc.collection.objects.link(ob);ob.location=center+Vector(offset);ob.rotation_euler=(center-ob.location).to_track_quat('-Z','Y').to_euler();lights.append(ob)
    cam.location=center+Vector((side*2,0,.09));cam.rotation_euler=(center-cam.location).to_track_quat('-Z','Y').to_euler()
    sc.render.filepath=str(out/(a.entity+('-neutral' if a.no_normal else '-normal')+str(side)+'.png'))
    bpy.ops.render.render(write_still=True)
    for ob in lights:bpy.data.objects.remove(ob,do_unlink=True)
print('REVIEW_COMPLETE',a.entity,a.no_normal)
