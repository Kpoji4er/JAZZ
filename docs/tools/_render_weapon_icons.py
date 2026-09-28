"""Render inventory icons with a hand-drawn-style outline, muzzle to the right.

Blender: blender --background --factory-startup --python this.py --
  --icon <label>=<JAZZ blend> [--icon ...] --out <folder> [--ring 8] [--halo 20]

Renders at 2x and leaves downscaling to _finalize_weapon_icons.py, so the ring keeps
clean edges at the 324x165 target. `--ring`/`--halo` are 2x pixels: ring 8 lands a
~4 px contour on the final icon, matching hand-made WeaponIcons/AK74.png.
"""
import argparse
import json
import sys
from pathlib import Path

import bpy
from mathutils import Vector

p = argparse.ArgumentParser()
p.add_argument('--icon', action='append', required=True, help='<label>=<blend path>')
p.add_argument('--out', type=Path, required=True)
p.add_argument('--width', type=int, default=324)
p.add_argument('--height', type=int, default=165)
p.add_argument('--supersample', type=int, default=2)
p.add_argument('--ring', type=int, default=7)
p.add_argument('--halo', type=int, default=12)
p.add_argument('--samples', type=int, default=64)
a = p.parse_args(sys.argv[sys.argv.index('--') + 1:])
a.out.mkdir(parents=True, exist_ok=True)
icons = dict(s.split('=', 1) for s in a.icon)

OUTLINE = (0.006, 0.005, 0.004, 1.0)
report = {'target': [a.width, a.height], 'ring_final_px': a.ring / a.supersample,
          'halo_final_px': a.halo / a.supersample, 'icons': {}}

for label, path in icons.items():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.wm.open_mainfile(filepath=path)
    scene = bpy.context.scene
    scene.render.engine = 'CYCLES'
    scene.cycles.samples = a.samples
    scene.render.resolution_x = a.width * a.supersample
    scene.render.resolution_y = a.height * a.supersample
    scene.render.resolution_percentage = 100
    scene.render.film_transparent = True
    scene.render.image_settings.file_format = 'PNG'
    scene.render.image_settings.color_mode = 'RGBA'

    for o in list(scene.objects):
        if o.type == 'MESH':
            # Folded-stock variants are alternate modules, never both at once.
            o.hide_render = o.name.endswith('_StockFolded')
        elif o.type in {'CAMERA', 'LIGHT'}:
            bpy.data.objects.remove(o, do_unlink=True)
    bpy.context.view_layer.update()

    camera_data = bpy.data.cameras.new('IconCamera')
    camera_data.type = 'ORTHO'
    camera = bpy.data.objects.new('IconCamera', camera_data)
    scene.collection.objects.link(camera)
    scene.camera = camera
    lights = []
    for i, offset in enumerate([(-1, -.5, 1.5), (-.5, .5, 1), (1, 1, 0)]):
        data = bpy.data.lights.new('IconLight%d' % i, 'AREA')
        data.energy, data.size = 25, 1.5
        light = bpy.data.objects.new(data.name, data)
        scene.collection.objects.link(light)
        lights.append((light, Vector(offset)))

    # Outline: dilate the alpha, tint it near-black, and lay the beauty pass on top so the
    # dark band only survives outside the silhouette. A wider blurred copy adds the halo.
    scene.use_nodes = True
    tree = scene.node_tree
    tree.nodes.clear()
    link = tree.links.new
    layers = tree.nodes.new('CompositorNodeRLayers')
    ring = tree.nodes.new('CompositorNodeDilateErode')
    ring.mode, ring.distance = 'DISTANCE', a.ring
    link(layers.outputs['Alpha'], ring.inputs[0])
    ring_rgba = tree.nodes.new('CompositorNodeSetAlpha')
    ring_rgba.inputs['Image'].default_value = OUTLINE
    link(ring.outputs[0], ring_rgba.inputs['Alpha'])

    halo = tree.nodes.new('CompositorNodeDilateErode')
    halo.mode, halo.distance = 'DISTANCE', a.halo
    link(layers.outputs['Alpha'], halo.inputs[0])
    soften = tree.nodes.new('CompositorNodeBlur')
    soften.filter_type, soften.size_x, soften.size_y = 'GAUSS', a.halo, a.halo
    link(halo.outputs[0], soften.inputs[0])
    fade = tree.nodes.new('CompositorNodeMath')
    fade.operation = 'MULTIPLY'
    fade.inputs[1].default_value = 0.32
    link(soften.outputs[0], fade.inputs[0])
    halo_rgba = tree.nodes.new('CompositorNodeSetAlpha')
    halo_rgba.inputs['Image'].default_value = OUTLINE
    link(fade.outputs[0], halo_rgba.inputs['Alpha'])

    contour = tree.nodes.new('CompositorNodeAlphaOver')
    contour.inputs[0].default_value = 1
    link(halo_rgba.outputs[0], contour.inputs[1])
    link(ring_rgba.outputs[0], contour.inputs[2])
    final = tree.nodes.new('CompositorNodeAlphaOver')
    final.inputs[0].default_value = 1
    link(contour.outputs[0], final.inputs[1])
    link(layers.outputs['Image'], final.inputs[2])
    link(final.outputs[0], tree.nodes.new('CompositorNodeComposite').inputs[0])

    meshes = [o for o in scene.objects if o.type == 'MESH' and not o.hide_render]
    points = [o.matrix_world @ Vector(v) for o in meshes for v in o.bound_box]
    lo = Vector(tuple(min(v[i] for v in points) for i in range(3)))
    hi = Vector(tuple(max(v[i] for v in points) for i in range(3)))
    target = (lo + hi) / 2
    aspect = a.width / a.height
    # The hand-made icons leave ~10 px clear on each side. Reserve that here too, or the
    # dilated ring and halo get clipped flat against the frame edge.
    margin = 1.0 + 2.2 * (a.ring + a.halo) / (a.width * a.supersample)
    camera_data.ortho_scale = max(hi.y - lo.y, (hi.z - lo.z) * aspect) * margin
    # Camera on -X puts +Y (the butt) on screen-left, so the muzzle points right.
    camera.location = target + Vector((-2, .04, .25))
    camera.rotation_euler = (target - camera.location).to_track_quat('-Z', 'Y').to_euler()
    for light, offset in lights:
        light.location = target + offset
        light.rotation_euler = (target - light.location).to_track_quat('-Z', 'Y').to_euler()

    scene.render.filepath = str(a.out / (label + '_icon_2x.png'))
    bpy.ops.render.render(write_still=True)
    report['icons'][label] = {'source': path, 'ortho_scale_m': camera_data.ortho_scale,
                              'length_m': hi.y - lo.y, 'height_m': hi.z - lo.z,
                              'rendered': scene.render.filepath,
                              'parts': sorted(o.name for o in meshes)}

(a.out / 'icons-report.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
print('ICONS=' + json.dumps(report))
