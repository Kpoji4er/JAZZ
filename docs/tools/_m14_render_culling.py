"""Blender offline two-sided culling inspection; --blend FILE --output DIR.
Uses EEVEE material backface culling, unlike the double-sided icon renderer.
Does not modify the source blend or installed assets.
"""
import argparse, sys
from pathlib import Path
import bpy
from mathutils import Vector
p=argparse.ArgumentParser()
p.add_argument('--blend',type=Path,required=True)
p.add_argument('--output',type=Path,required=True)
p.add_argument('--only',help='Comma-separated mesh names for an assembled review')
a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
a.output.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(a.blend))
if a.only:
    names=set(a.only.split(','))
    for obj in list(bpy.data.objects):
        if obj.type=='MESH' and obj.name not in names:
            bpy.data.objects.remove(obj,do_unlink=True)
meshes=[o for o in bpy.data.objects if o.type=='MESH']
points=[o.matrix_world@Vector(v) for o in meshes for v in o.bound_box]
lo=Vector(tuple(min(v[i] for v in points) for i in range(3)))
hi=Vector(tuple(max(v[i] for v in points) for i in range(3)))
center=(lo+hi)/2; span=max(hi-lo)
for mat in bpy.data.materials:
    mat.use_backface_culling=True
    mat.use_nodes=True
    bs=mat.node_tree.nodes.get('Principled BSDF')
    if bs:
        bs.inputs['Base Color'].default_value=(.30,.22,.13,1)
        bs.inputs['Roughness'].default_value=.65
scene=bpy.context.scene
scene.render.engine='BLENDER_EEVEE_NEXT'
scene.render.resolution_x=1400;scene.render.resolution_y=500
scene.render.resolution_percentage=100
if scene.world is None: scene.world=bpy.data.worlds.new('QA world')
scene.world.color=(.3,.3,.3)
scene.render.image_settings.file_format='PNG'
for side in (-1,1):
    bpy.ops.object.light_add(type='AREA',location=center+Vector((side*span*2,0,span)))
    bpy.context.object.data.energy=180;bpy.context.object.data.shape='DISK';bpy.context.object.data.size=span*2
    bpy.context.object.rotation_euler=(center-bpy.context.object.location).to_track_quat('-Z','Y').to_euler()
    bpy.ops.object.camera_add(location=center+Vector((side*span*3,0,span*.18)))
    cam=bpy.context.object;cam.data.type='ORTHO';cam.data.ortho_scale=span*1.12
    cam.rotation_euler=(center-cam.location).to_track_quat('-Z','Y').to_euler();scene.camera=cam
    scene.render.filepath=str(a.output/('side'+str(side)+'.png'))
    bpy.ops.render.render(write_still=True)
