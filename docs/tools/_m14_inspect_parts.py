"""Blender: render numbered donor parts in native OBJ coordinates, read-only.
--source <mk14 directory> --output <png>; no source/asset writes.
"""
import argparse
import sys
from pathlib import Path
import bpy
from mathutils import Vector

p = argparse.ArgumentParser()
p.add_argument('--source', type=Path, required=True)
p.add_argument('--output', type=Path, required=True)
a = p.parse_args(sys.argv[sys.argv.index('--') + 1:])
bpy.ops.wm.read_factory_settings(use_empty=True)
for i, path in enumerate(sorted(a.source.glob('part_*.obj'))):
    verts, faces = [], []
    for line in path.read_text().splitlines():
        if line.startswith('v '): verts.append(tuple(map(float, line.split()[1:4])))
        elif line.startswith('f '): faces.append([int(t.split('/')[0])-1 for t in line.split()[1:]])
    mesh = bpy.data.meshes.new(path.stem)
    mesh.from_pydata(verts, [], faces)
    obj = bpy.data.objects.new(path.stem, mesh)
    bpy.context.collection.objects.link(obj)
    obj.location = ((i % 2) * 6, 0, -(i // 2) * 1.4)
    font = bpy.data.curves.new('label', 'FONT')
    font.body, font.size = path.stem, .25
    label = bpy.data.objects.new('label', font)
    bpy.context.collection.objects.link(label)
    label.location = ((i % 2)*6-4, -.5, -(i//2)*1.4+.55)
    label.rotation_euler[0] = 1.57079632679
sc = bpy.context.scene
sc.render.engine = 'BLENDER_WORKBENCH'
sc.display.shading.light = 'STUDIO'
sc.display.shading.show_shadows = True
sc.render.resolution_x, sc.render.resolution_y = 1600, 1300
sc.render.resolution_percentage = 100
cam = bpy.data.objects.new('camera', bpy.data.cameras.new('camera'))
bpy.context.collection.objects.link(cam)
cam.data.type, cam.data.ortho_scale = 'ORTHO', 12
cam.location = (2, -20, -3)
cam.rotation_euler = (Vector((2,0,-3))-cam.location).to_track_quat('-Z','Y').to_euler()
sc.camera = cam
sc.render.filepath = str(a.output)
bpy.ops.render.render(write_still=True)
