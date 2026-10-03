"""Blender: -- --source clean.glb --project DIR. Audit texture-only geometry and pack a blend."""
import argparse
import json
import sys
from pathlib import Path
import bpy
import bmesh
import numpy as np
from mathutils import Vector
from mathutils.kdtree import KDTree

p = argparse.ArgumentParser(description=__doc__)
p.add_argument('--source', type=Path, required=True)
p.add_argument('--project', type=Path, required=True)
a = p.parse_args(sys.argv[sys.argv.index('--') + 1:])
a.source = a.source.resolve(); a.project = a.project.resolve()

def geometry(path):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=str(path))
    triangles = []
    for obj in [o for o in bpy.context.scene.objects if o.type == 'MESH']:
        obj.data.calc_loop_triangles()
        for tri in obj.data.loop_triangles:
            # Ignore UV seams, face order and winding; compare actual triangle positions.
            triangles.append(sorted(tuple(round(c, 5) for c in obj.matrix_world @ obj.data.vertices[v].co) for v in tri.vertices))
    return sorted(triangles)

before = geometry(a.source)
after = geometry(a.project / 'model.glb')
report = dict(triangles=len(after), geometry_unchanged=before == after, textures={}, meshes=[])
# Meshy normalizes input bounds and may collapse tiny edges while unwrapping.
# Restore the input coordinate system, then measure deviation both ways.
src = np.unique(np.array(before).reshape(-1,3), axis=0)
dst = np.unique(np.array(after).reshape(-1,3), axis=0)
sc = (src.max(axis=0)+src.min(axis=0))/2
dc = (dst.max(axis=0)+dst.min(axis=0))/2
scale = float(np.ptp(src,axis=0).max()/np.ptp(dst,axis=0).max())
restored = (dst-dc)*scale+sc
def distance(points, target):
    tree = KDTree(len(target))
    for i, point in enumerate(target): tree.insert(point, i)
    tree.balance()
    return max(tree.find(point)[2] for point in points)
report.update(source_triangles=len(before), restored_scale=scale, max_vertex_deviation=max(distance(src,restored),distance(restored,src)))
assert report['max_vertex_deviation'] < .001*np.ptp(src,axis=0).max(), report
for obj in [o for o in bpy.context.scene.objects if o.type == 'MESH']:
    inv = obj.matrix_world.inverted()
    for v in obj.data.vertices:
        v.co = inv @ Vector((np.array(obj.matrix_world @ v.co)-dc)*scale+sc)
for obj in [o for o in bpy.context.scene.objects if o.type == 'MESH']:
    bm = bmesh.new(); bm.from_mesh(obj.data)
    bmesh.ops.remove_doubles(bm, verts=list(bm.verts), dist=1e-6)
    report['meshes'].append(dict(boundary_edges=sum(e.is_boundary for e in bm.edges), nonmanifold_edges=sum(not e.is_manifold for e in bm.edges), uv_layers=len(obj.data.uv_layers)))
    assert not any(not e.is_manifold for e in bm.edges), report
    bm.free()

# Use original PNG maps instead of the JPEG copies embedded by the service.
mat = bpy.data.materials.new('Chainmail_PBR_4K'); mat.use_nodes = True
nodes = mat.node_tree.nodes; links = mat.node_tree.links
shader = nodes.get('Principled BSDF')
for i, (kind, socket) in enumerate([('base_color', 'Base Color'), ('metallic', 'Metallic'), ('roughness', 'Roughness'), ('normal', None)]):
    im = bpy.data.images.load(str(a.project / ('texture_0_' + kind + '.png')))
    im.colorspace_settings.name = 'sRGB' if kind == 'base_color' else 'Non-Color'
    report['textures'][kind] = list(im.size)
    tex = nodes.new('ShaderNodeTexImage'); tex.image = im; tex.label = kind; tex.location = (-600, 300-i*260)
    if socket:
        links.new(tex.outputs['Color'], shader.inputs[socket])
    else:
        normal = nodes.new('ShaderNodeNormalMap'); normal.location = (-260, -480)
        links.new(tex.outputs['Color'], normal.inputs['Color']); links.new(normal.outputs['Normal'], shader.inputs['Normal'])
    im.pack()
for obj in [o for o in bpy.context.scene.objects if o.type == 'MESH']:
    obj.data.materials.clear(); obj.data.materials.append(mat)
    for face in obj.data.polygons: face.material_index = 0
bpy.ops.wm.save_as_mainfile(filepath=str(a.project / 'Chainmail_textured.blend'))
bpy.ops.export_scene.gltf(filepath=str(a.project / 'Chainmail_textured.glb'), export_format='GLB', export_animations=False)
(a.project / 'verification.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
(a.project / 'render-manifest.json').write_text(json.dumps({'jobs':[{'name':'Chainmail_textured', 'project':str(a.project.resolve()), 'model':str((a.project / 'Chainmail_textured.glb').resolve())}]}, indent=2), encoding='utf-8')
print(json.dumps(report))
