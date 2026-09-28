"""Repair disconnected coincident vertices before normals recalculation.
Blender --python this.py -- --source BLEND --output DIR --game-root ROOT.
Exports one selected M14 entity; does not write installed resources or custom normals.
"""
import argparse, json, sys
from collections import Counter
from pathlib import Path
import bpy, bmesh
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _export_m14_family_assets import load_hge, export_fbx
from _ja3_mesh_prepare import prepare_export_mesh

p = argparse.ArgumentParser()
p.add_argument('--entity', default='JAZZ_M14', help='Existing mesh object in the supplied M14 blend')
for name in ('source', 'output', 'game-root'):
    p.add_argument('--' + name, type=Path, required=True)
a = p.parse_args(sys.argv[sys.argv.index('--') + 1:])
a.output.mkdir(parents=True, exist_ok=True)
hge = load_hge(a.game_root)
bpy.ops.wm.open_mainfile(filepath=str(a.source))
obj = bpy.data.objects[a.entity]
keep = {obj, *obj.children}
if obj.parent:
    keep.add(obj.parent)
for other in list(bpy.data.objects):
    if other not in keep:
        bpy.data.objects.remove(other, do_unlink=True)
bm = bmesh.new(); bm.from_mesh(obj.data)
uv_before = Counter(tuple(uv.uv) for uv in obj.data.uv_layers.active.data)
normals_before = [face.normal.copy() for face in obj.data.polygons]
before = {'vertices': len(bm.verts), 'faces': len(bm.faces),
          'boundary_edges': sum(e.is_boundary for e in bm.edges)}
# 1 micrometre: weld coincident UV-split geometry, retain per-corner UVs.
bmesh.ops.remove_doubles(bm, verts=list(bm.verts), dist=1e-6)
after = {'vertices': len(bm.verts), 'faces': len(bm.faces),
         'boundary_edges': sum(e.is_boundary for e in bm.edges)}
assert before['faces'] == after['faces'], 'Weld unexpectedly removed faces'
bm.to_mesh(obj.data); bm.free()
issues = prepare_export_mesh(obj)
assert Counter(tuple(uv.uv) for uv in obj.data.uv_layers.active.data) == uv_before, 'Weld changed loop UVs'
assert len(obj.data.polygons) == before['faces'], 'Preparation changed triangle count'
after['flipped_faces'] = sum(old.dot(face.normal) < 0 for old, face in zip(normals_before, obj.data.polygons))
after['custom_normals'] = obj.data.has_custom_normals
after['loop_uvs_preserved'] = True
bpy.ops.wm.save_as_mainfile(filepath=str(a.output / (a.entity + '.blend')))
export_fbx(hge, a.output / (a.entity + '.fbx'))
(a.output / 'winding-report.json').write_text(json.dumps(
    {'before': before, 'after': after, 'issues': issues}, indent=2))
print(json.dumps({'before': before, 'after': after, 'issues': issues}))
