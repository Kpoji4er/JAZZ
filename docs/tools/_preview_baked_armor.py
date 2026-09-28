"""Render the baked armor atlas on its export mesh, independently of source shaders.

Blender -b --factory-startup --python this.py -- --build DIR --entity ID --output DIR
Reads the prepared blend and Base/Norm/RM TGA. Writes front/back PNG and UV audit.
This preview does not test JA3 materials, animation or collision.
"""
import argparse
import json
import sys
from pathlib import Path

import bpy
from mathutils import Vector

p = argparse.ArgumentParser()
p.add_argument('--build', type=Path, required=True)
p.add_argument('--entity', required=True)
p.add_argument('--output', type=Path, required=True)
a = p.parse_args(sys.argv[sys.argv.index('--') + 1:])
a.build = a.build.resolve()
a.output = a.output.resolve()
a.output.mkdir(parents=True, exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(a.build / (a.entity + '.blend')))
obj = bpy.data.objects[a.entity]
assert len(obj.data.uv_layers) == 1, 'Export must contain exactly one atlas UV'
mat = bpy.data.materials.new('Baked atlas preview')
mat.use_nodes = True
nodes, links = mat.node_tree.nodes, mat.node_tree.links
bsdf = nodes['Principled BSDF']
for suffix in ('Base', 'Norm', 'RM'):
    tex = nodes.new('ShaderNodeTexImage')
    tex.image = bpy.data.images.load(str(a.build / (a.entity + '_' + suffix + '.tga')))
    tex.image.colorspace_settings.name = 'sRGB' if suffix == 'Base' else 'Non-Color'
    if suffix == 'Base':
        links.new(tex.outputs['Color'], bsdf.inputs['Base Color'])
    elif suffix == 'Norm':
        normal = nodes.new('ShaderNodeNormalMap')
        links.new(tex.outputs['Color'], normal.inputs['Color'])
        links.new(normal.outputs['Normal'], bsdf.inputs['Normal'])
    else:
        split = nodes.new('ShaderNodeSeparateColor')
        links.new(tex.outputs['Color'], split.inputs['Color'])
        links.new(split.outputs['Red'], bsdf.inputs['Roughness'])
        links.new(split.outputs['Blue'], bsdf.inputs['Metallic'])
obj.data.materials.clear()
obj.data.materials.append(mat)
for face in obj.data.polygons:
    face.material_index = 0
scene = bpy.context.scene
scene.render.engine = 'CYCLES'
scene.cycles.device = 'CPU'
scene.cycles.samples = 32
scene.cycles.use_denoising = True
scene.render.resolution_x, scene.render.resolution_y = 900, 1000
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = 'PNG'
scene.render.film_transparent = False
scene.world.use_nodes = True
background = scene.world.node_tree.nodes.get('Background')
background.inputs[0].default_value = (.9, .9, .88, 1)
background.inputs[1].default_value = 1.05
points = [obj.matrix_world @ v.co for v in obj.data.vertices]
lo = Vector(tuple(min(v[i] for v in points) for i in range(3)))
hi = Vector(tuple(max(v[i] for v in points) for i in range(3)))
focus = (lo + hi) / 2

def aim(target):
    target.rotation_euler = (focus - target.location).to_track_quat('-Z', 'Y').to_euler()

for pos, energy, size in [((-1.2, -1.8, 2.4), 170, 2),
                          ((1.5, -1, 1.6), 80, 2), ((0, 1.6, 2), 100, 2)]:
    bpy.ops.object.light_add(type='AREA', location=pos)
    lamp = bpy.context.object
    lamp.data.energy, lamp.data.size = energy, size
    aim(lamp)
bpy.ops.object.camera_add()
cam = bpy.context.object
cam.data.type = 'ORTHO'
cam.data.ortho_scale = max(hi.x - lo.x, hi.z - lo.z) * 1.12
scene.camera = cam
for name, y in [('front', -2.6), ('back', 2.6)]:
    cam.location = (0, y, focus.z)
    aim(cam)
    scene.render.filepath = str(a.output / ('baked_' + name + '.png'))
    bpy.ops.render.render(write_still=True)
(a.output / 'baked-preview.json').write_text(json.dumps({
    'entity': a.entity, 'uv_layers': [u.name for u in obj.data.uv_layers],
    'maps': ['Base', 'Norm', 'RM'], 'runtime': 'NOT_RUN',
}, indent=2), encoding='utf-8')
