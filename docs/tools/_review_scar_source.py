"""Blender source inventory; no edits to source files. -- --source DIR --output DIR.

Render original OBJ geometry in three orthographic projections. Labels and
geometry share a Blender scene, so no image processing or guessed assembly.
"""
import argparse
import sys
from pathlib import Path
import bpy
from mathutils import Vector

p = argparse.ArgumentParser()
p.add_argument('--source', type=Path, required=True)
p.add_argument('--output', type=Path, required=True)
p.add_argument('--models', default='5,13,24,41,19,18,15,67')
p.add_argument('--bounds', type=float, nargs=6)
a = p.parse_args(sys.argv[sys.argv.index('--') + 1:])
a.output.mkdir(parents=True, exist_ok=True)
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
scene = bpy.context.scene
scene.render.engine = 'BLENDER_WORKBENCH'
scene.render.resolution_x = 1800
scene.render.resolution_y = 1800
scene.render.resolution_percentage = 100
scene.display.shading.light = 'STUDIO'
scene.display.shading.studio_light = 'paint.sl'
scene.display.shading.color_type = 'OBJECT'
scene.display.shading.show_shadows = False
scene.display.shading.show_cavity = True
scene.display.shading.background_type = 'WORLD'
scene.world.color = (0.12, 0.12, 0.12)
scene.view_settings.view_transform = 'Standard'
camdata = bpy.data.cameras.new('audit')
camdata.type = 'ORTHO'
camdata.ortho_scale = 3.2
cam = bpy.data.objects.new('audit', camdata)
scene.collection.objects.link(cam)
cam.location = (0, 0, 10)
scene.camera = cam
for row, number in enumerate(map(int, a.models.split(','))):
    path = a.source / f'model_{number}.obj'
    verts, faces = [], []
    for line in path.read_text().splitlines():
        bits = line.split()
        if not bits:
            continue
        if bits[0] == 'v':
            verts.append(tuple(map(float, bits[1:4])))
        elif bits[0] == 'f':
            faces.append([int(token.split('/')[0]) - 1 for token in bits[1:]])
    if a.bounds:
        faces=[f for f in faces if all(all(a.bounds[i]<=verts[v][i]<=a.bounds[i+3] for i in range(3)) for v in f)]
        used=sorted({v for f in faces for v in f}); remap={v:i for i,v in enumerate(used)}
        verts=[verts[v] for v in used];faces=[[remap[v] for v in f] for f in faces]
    lo = Vector(tuple(min(v[i] for v in verts) for i in range(3)))
    hi = Vector(tuple(max(v[i] for v in verts) for i in range(3)))
    centre = (lo + hi) / 2
    for col, axes in enumerate(((0,1,2),(0,2,1),(2,1,0))):
        scale = min(0.9/(hi[axes[0]]-lo[axes[0]]), 0.28/(hi[axes[1]]-lo[axes[1]]))
        offset = Vector((col - 1, 1.3 - row * 0.38, 0))
        points = [Vector(tuple((v[ax] - centre[ax]) * scale for ax in axes)) + offset for v in verts]
        mesh = bpy.data.meshes.new(f'{number}_{col}')
        mesh.from_pydata(points, [], faces)
        obj = bpy.data.objects.new(mesh.name, mesh)
        scene.collection.objects.link(obj)
        obj.color = (0.6, 0.63, 0.68, 1)
        font = bpy.data.curves.new('label', 'FONT')
        font.body = f'{number}: {"XYZ"[axes[0]]}/{"XYZ"[axes[1]]}'
        font.size = 0.047
        label = bpy.data.objects.new('label', font)
        scene.collection.objects.link(label)
        label.location = offset + Vector((-0.45, 0.13, 1))
        label.color = (1, 1, 1, 1)
scene.render.filepath = str(a.output / ('source-' + a.models.replace(',', '-') + '.png'))
bpy.ops.render.render(write_still=True)
