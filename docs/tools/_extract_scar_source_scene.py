"""Extract owner-approved SCAR-H assembly without moving its components.

Blender --background SOURCE.blend --python SCRIPT -- --output DIR
This is source preparation, not an HGE exporter or installer. Requires the
owner's all-OBJ scene; original world coordinates and loop UV are preserved.
"""
import argparse
import hashlib
import json
import math
import sys
from pathlib import Path

import bmesh
import bpy

p = argparse.ArgumentParser()
p.add_argument('--output', type=Path, required=True)
a = p.parse_args(sys.argv[sys.argv.index('--') + 1:])
a.output.mkdir(parents=True, exist_ok=True)
source = Path(bpy.data.filepath)
parts = {
    'model_0': 'Upper_H', 'model_1': 'Stock',
    'model_3': 'RearSight', 'model_4': 'Common',
    'model_7': 'Lower_H', 'model_8': 'Magazine_H',
    'model_11': 'Muzzle',
}
missing = set(parts) - set(bpy.data.objects.keys())
if missing:
    raise RuntimeError(f'Missing source objects: {sorted(missing)}')
report = []
for obj in list(bpy.context.scene.objects):
    if obj.type != 'MESH' or obj.name not in parts:
        bpy.data.objects.remove(obj, do_unlink=True)
        continue
    source_name = obj.name
    bm = bmesh.new()
    bm.from_mesh(obj.data)

    def inside(v):
        q = obj.matrix_world @ v.co
        return 48 < q.x < 80 and 0 < q.y < 110 and -2 < q.z < 10

    keep = {f for f in bm.faces if all(inside(v) for v in f.verts)}
    crossing = [f for f in bm.faces
                if any(inside(v) for v in f.verts)
                and not all(inside(v) for v in f.verts)]
    if crossing or not keep:
        raise RuntimeError(f'{source_name}: empty selection or cut faces')
    bmesh.ops.delete(bm, geom=[f for f in bm.faces if f not in keep],
                     context='FACES_ONLY')
    bmesh.ops.delete(bm, geom=[v for v in bm.verts if not v.link_faces],
                     context='VERTS')
    bm.to_mesh(obj.data)
    bm.free()
    obj.name = parts[source_name]
    obj['scar_source_object'] = source_name
    obj['scar_preparation_status'] = 'source-preserved; not export-ready'
    report.append({'source': source_name, 'part': obj.name,
                   'faces': len(obj.data.polygons), 'cut_faces': 0,
                   'uv_layers': len(obj.data.uv_layers)})

scene = bpy.context.scene
scene.render.engine = 'BLENDER_WORKBENCH'
scene.render.resolution_x = 1600
scene.render.resolution_y = 650
scene.render.resolution_percentage = 100
scene.display.shading.color_type = 'SINGLE'
scene.display.shading.single_color = (.6, .65, .7)
scene.display.shading.show_cavity = True
scene.display.shading.show_shadows = False
cam_data = bpy.data.cameras.new('SourceReview')
cam_data.type = 'ORTHO'
cam_data.ortho_scale = 115
cam = bpy.data.objects.new('SourceReview', cam_data)
scene.collection.objects.link(cam)
scene.camera = cam
cam.location = (64, 55, -200)
cam.rotation_euler = (math.pi, 0, -math.pi / 2)
scene.render.filepath = str(a.output / 'SCAR-H-source.png')
bpy.ops.wm.save_as_mainfile(filepath=str(a.output / 'SCAR-H-source.blend'))
bpy.ops.render.render(write_still=True)
(a.output / 'source-manifest.json').write_text(json.dumps({
    'source_file': source.name,
    'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
    'status': 'source geometry only; materials/export/runtime pending',
    'parts': report,
}, indent=2), encoding='utf-8')
