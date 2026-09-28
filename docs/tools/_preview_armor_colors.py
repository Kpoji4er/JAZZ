"""Blender offline review of baked albedo on HAV donor and unchanged mail source."""
import argparse
import json
import sys
from pathlib import Path
import bpy
from mathutils import Vector

p = argparse.ArgumentParser(description=__doc__)
for key in ('plan', 'hav', 'chainmail'):
    p.add_argument('--' + key, type=Path, required=True)
a = p.parse_args(sys.argv[sys.argv.index('--') + 1:])
out = a.plan.resolve().parent
plan = json.loads(a.plan.read_text())

for family in ('Guardian', 'Twaron', 'Zylon', 'Chainmail'):
    bpy.ops.wm.open_mainfile(filepath=str((a.chainmail if family == 'Chainmail' else a.hav).resolve()))
    obj = bpy.data.objects['TEST_chainmail_Male' if family == 'Chainmail' else 'HAV_vest']
    for o in list(bpy.data.objects):
        if o.type in ('LIGHT', 'CAMERA') or (o.type == 'MESH' and o != obj):
            bpy.data.objects.remove(o, do_unlink=True)
    obj.hide_render = False
    name = next(k for k, v in plan['maps'].items() if v['family'] == family)
    im = bpy.data.images.load(str(out / 'baked' / (name + '.tga')))
    for mat in obj.data.materials:
        n, l = mat.node_tree.nodes, mat.node_tree.links
        bsdf = n.get('Principled BSDF')
        tex = n.new('ShaderNodeTexImage')
        tex.image = im
        uv = n.new('ShaderNodeUVMap')
        uv.uv_map = 'BakeAtlas' if family == 'Chainmail' else obj.data.uv_layers[0].name
        l.new(uv.outputs[0], tex.inputs['Vector'])
        l.new(tex.outputs['Color'], bsdf.inputs['Base Color'])
    scene = bpy.context.scene
    scene.render.engine = 'CYCLES'
    scene.cycles.device = 'CPU'
    scene.cycles.samples = 16
    scene.cycles.use_denoising = True
    scene.render.resolution_x = 600
    scene.render.resolution_y = 720
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = 'PNG'
    scene.render.film_transparent = False
    scene.world = bpy.data.worlds.new('Neutral studio')
    scene.world.use_nodes = True
    scene.world.node_tree.nodes['Background'].inputs[0].default_value = (.32, .32, .32, 1)
    scene.world.node_tree.nodes['Background'].inputs[1].default_value = .8
    points = [obj.matrix_world @ v.co for v in obj.data.vertices]
    lo = Vector(tuple(min(v[i] for v in points) for i in range(3)))
    hi = Vector(tuple(max(v[i] for v in points) for i in range(3)))
    focus = (lo + hi) / 2
    for loc, power in [((-2, -3, 3), 220), ((2, -1, 3), 140), ((1, 2, 3), 180)]:
        bpy.ops.object.light_add(type='AREA', location=focus + Vector(loc))
        lamp = bpy.context.object
        lamp.data.energy = power
        lamp.data.size = 2
        lamp.rotation_euler = (focus - lamp.location).to_track_quat('-Z', 'Y').to_euler()
    bpy.ops.object.camera_add(location=focus + Vector((-.35, -3, .18)))
    cam = bpy.context.object
    cam.rotation_euler = (focus - cam.location).to_track_quat('-Z', 'Y').to_euler()
    cam.data.type = 'ORTHO'
    cam.data.ortho_scale = max(hi - lo) * 1.35
    scene.camera = cam
    scene.render.filepath = str(out / (family + '-preview.png'))
    bpy.ops.render.render(write_still=True)
