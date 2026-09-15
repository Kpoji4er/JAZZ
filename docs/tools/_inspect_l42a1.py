"""Blender read-only source inspection; outputs a material-restored working copy."""
import argparse
import sys
from pathlib import Path
import bpy
from mathutils import Matrix, Vector

p=argparse.ArgumentParser()
p.add_argument('--source',required=True)
p.add_argument('--output',required=True)
a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
src=Path(a.source).resolve()
out=Path(a.output).resolve();out.mkdir(exist_ok=True,parents=True)
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
for i in range(2):
    bpy.ops.wm.obj_import(filepath=str(src/f'model_{i}.obj'))
    obj=bpy.context.object
    obj.scale=(0.0007,)*3
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    mat=bpy.data.materials.new('L42A1_Body' if i==0 else 'L42A1_Lenses')
    mat.use_nodes=True
    nodes=mat.node_tree.nodes;links=mat.node_tree.links
    bsdf=nodes.get('Principled BSDF')
    img=nodes.new('ShaderNodeTexImage')
    img.image=bpy.data.images.load(str(src/('DefaultMaterial_C.png' if i==0 else 'GAP_2DAE05_Martens_Dries__C.png')))
    links.new(img.outputs['Color'],bsdf.inputs['Base Color'])
    rough=nodes.new('ShaderNodeTexImage')
    rough.image=bpy.data.images.load(str(src/('DefaultMaterial_R.png' if i==0 else 'GAP_2DAE05_Martens_Dries_R.png')))
    rough.image.colorspace_settings.name='Non-Color'
    links.new(rough.outputs['Color'],bsdf.inputs['Roughness'])
    if i==0:
        norm=nodes.new('ShaderNodeTexImage')
        norm.image=bpy.data.images.load(str(src/'GAP_2DAE05_Martens_Dries_N.png'))
        norm.image.colorspace_settings.name='Non-Color'
        normal=nodes.new('ShaderNodeNormalMap')
        links.new(norm.outputs['Color'],normal.inputs['Color'])
        links.new(normal.outputs['Normal'],bsdf.inputs['Normal'])
        metal=nodes.new('ShaderNodeTexImage')
        metal.image=bpy.data.images.load(str(src/'GAP_2DAE05_Martens_Dries_M.png'))
        metal.image.colorspace_settings.name='Non-Color'
        links.new(metal.outputs['Color'],bsdf.inputs['Metallic'])
    obj.data.materials.clear();obj.data.materials.append(mat)
scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=20
scene.render.resolution_x=1500;scene.render.resolution_y=450;scene.render.resolution_percentage=100
scene.render.film_transparent=True;scene.render.image_settings.color_mode='RGBA'
target=Vector((0,0,0))
data=bpy.data.cameras.new('ReviewCamera');cam=bpy.data.objects.new(data.name,data);scene.collection.objects.link(cam)
cam.location=(0,-2,0.3);cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler()
data.type='ORTHO';data.ortho_scale=1.22;scene.camera=cam
for i,loc in enumerate([(0,-1,1),(-1,0,1),(1,-1,0)]):
    data=bpy.data.lights.new('Light'+str(i),'AREA');data.energy=90;data.size=1.5
    light=bpy.data.objects.new(data.name,data);scene.collection.objects.link(light);light.location=loc
    light.rotation_euler=(target-light.location).to_track_quat('-Z','Y').to_euler()
scene.render.filepath=str(out/'L42A1_source_preview.png')
bpy.ops.wm.save_as_mainfile(filepath=str(out/'L42A1_material_review.blend'))
bpy.ops.render.render(write_still=True)
