"""Blender native material revision; bake albedo on unchanged texture coordinates.

--plan folder/plan.json --chainmail source.blend --woodland reference.png
HAV preserves donor fabric shading through material nodes. Chainmail uses its
editable procedural source, with brighter steel rings. No geometry is exported.
"""
import argparse
import json
import sys
from pathlib import Path
import bpy

p = argparse.ArgumentParser(description=__doc__)
for key in ('plan', 'chainmail', 'woodland'):
    p.add_argument('--' + key, type=Path, required=True)
a = p.parse_args(sys.argv[sys.argv.index('--') + 1:])
out = a.plan.resolve().parent
plan = json.loads(a.plan.read_text())
baked = out / 'baked'
baked.mkdir(exist_ok=True)

def settings():
    s = bpy.context.scene
    s.render.engine = 'CYCLES'
    s.cycles.device = 'CPU'
    s.cycles.samples = 1
    s.render.bake.margin = 8
    s.render.bake.use_selected_to_active = False
    return s

def output_image(name, size):
    im = bpy.data.images.new(name, width=size[0], height=size[1], alpha=False)
    im.colorspace_settings.name = 'sRGB'
    return im

def target(mat, im):
    node = mat.node_tree.nodes.new('ShaderNodeTexImage')
    node.image = im
    mat.node_tree.nodes.active = node

def emit(mat, color):
    n, l = mat.node_tree.nodes, mat.node_tree.links
    e = n.new('ShaderNodeEmission')
    l.new(color, e.inputs['Color'])
    output = next(node for node in n if node.type == 'OUTPUT_MATERIAL')
    l.new(e.outputs[0], output.inputs['Surface'])

def save(im, name):
    im.file_format = 'TARGA'
    im.filepath_raw = str(baked / (name + '.tga'))
    im.save()

cache = {}
for name, row in plan['maps'].items():
    if row['family'] == 'Chainmail':
        continue
    key = (row['family'], row['before'])
    if key in cache:
        # Same native material input on multiple configurations: exact same bake.
        import shutil
        shutil.copy2(baked / (cache[key] + '.tga'), baked / (name + '.tga'))
        continue
    bpy.ops.wm.read_factory_settings(use_empty=True)
    settings()
    bpy.ops.mesh.primitive_plane_add(size=2)
    obj = bpy.context.object
    mat = bpy.data.materials.new(row['family'] + ' fabric')
    mat.use_nodes = True
    obj.data.materials.append(mat)
    n, l = mat.node_tree.nodes, mat.node_tree.links
    tex = n.new('ShaderNodeTexImage')
    tex.image = bpy.data.images.load(str(out / 'inputs' / (name + '.png')))
    gray = n.new('ShaderNodeRGBToBW')
    l.new(tex.outputs['Color'], gray.inputs[0])
    if row['family'] == 'Guardian':
        scale = n.new('ShaderNodeMath')
        scale.operation = 'MULTIPLY'
        scale.inputs[1].default_value = .32
        l.new(gray.outputs[0], scale.inputs[0])
        color = scale.outputs[0]
    else:
        detail = n.new('ShaderNodeMapRange')
        detail.inputs['From Min'].default_value = 0
        detail.inputs['From Max'].default_value = .12
        detail.inputs['To Min'].default_value = .35
        detail.inputs['To Max'].default_value = 1.1
        l.new(gray.outputs[0], detail.inputs['Value'])
        mix = n.new('ShaderNodeMixRGB')
        mix.blend_type = 'MULTIPLY'
        mix.inputs[0].default_value = 1
        l.new(detail.outputs[0], mix.inputs[1])
        if row['family'] == 'Twaron':
            mix.inputs[2].default_value = (.055, .115, .035, 1)
        else:
            camo = n.new('ShaderNodeTexImage')
            camo.image = bpy.data.images.load(str(a.woodland.resolve()))
            camo.extension = 'REPEAT'
            uv = n.new('ShaderNodeTexCoord')
            mapping = n.new('ShaderNodeVectorMath')
            mapping.operation = 'MULTIPLY'
            mapping.inputs[1].default_value = (1.2, 1.2 * camo.image.size[0] / camo.image.size[1], 1)
            l.new(uv.outputs['UV'], mapping.inputs[0])
            l.new(mapping.outputs[0], camo.inputs['Vector'])
            l.new(camo.outputs['Color'], mix.inputs[2])
        color = mix.outputs[0]
    emit(mat, color)
    im = output_image(name, row['size'])
    target(mat, im)
    bpy.ops.object.bake(type='EMIT')
    save(im, name)
    bpy.ops.file.pack_all()
    bpy.ops.wm.save_as_mainfile(filepath=str(baked / (name + '.blend')))
    cache[key] = name
    print('BAKED', row['family'], name, flush=True)

bpy.ops.wm.open_mainfile(filepath=str(a.chainmail.resolve()))
settings()
obj = bpy.data.objects['TEST_chainmail_Male']
for other in list(bpy.data.objects):
    if other != obj:
        bpy.data.objects.remove(other, do_unlink=True)
obj.modifiers.clear()
bpy.context.view_layer.objects.active = obj
obj.hide_set(False)
obj.select_set(True)
obj.data.uv_layers.active = obj.data.uv_layers['BakeAtlas']
obj.data.uv_layers['BakeAtlas'].active_render = True
mail = obj.data.materials['Alternating wire mail rings']
mix = mail.node_tree.nodes['Mix (Legacy)']
mix.inputs[1].default_value = (.022, .025, .027, 1)
mix.inputs[2].default_value = (.34, .36, .38, 1)
name, row = next((k, v) for k, v in plan['maps'].items() if v['family'] == 'Chainmail')
im = output_image(name, row['size'])
# Preserve the edited native scene before temporary emission bake wiring.
bpy.ops.wm.save_as_mainfile(filepath=str(baked / 'chainmail-material.blend'))
for mat in obj.data.materials:
    bsdf = mat.node_tree.nodes.get('Principled BSDF')
    if bsdf.inputs['Base Color'].is_linked:
        color = bsdf.inputs['Base Color'].links[0].from_socket
    else:
        rgb = mat.node_tree.nodes.new('ShaderNodeRGB')
        rgb.outputs[0].default_value = bsdf.inputs['Base Color'].default_value
        color = rgb.outputs[0]
    emit(mat, color)
    target(mat, im)
bpy.ops.object.bake(type='EMIT')
save(im, name)
print('BAKED Chainmail', name, flush=True)
