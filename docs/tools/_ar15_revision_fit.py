"""Blender: scale existing AR15 furniture, seat unchanged magazines, repair short tube.

--weapon M16A4|M4A1 --blend assembled.blend --output DIR --game-root ROOT
Stages only. Existing IDs/materials/UVs survive; no ModItem writes.
"""
import argparse
import json
import sys
from pathlib import Path

import bpy
import bmesh
from mathutils import Matrix, Vector

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _export_m14_family_assets import load_hge, export_fbx
from _prepare_weapon_open_surfaces import prepare_export_mesh

p = argparse.ArgumentParser()
p.add_argument('--weapon', choices=('M16A4', 'M4A1'), required=True)
for key in ('blend', 'output', 'game-root'):
    p.add_argument('--' + key, type=Path, required=True)
a = p.parse_args(sys.argv[sys.argv.index('--') + 1:])
a.output.mkdir(parents=True, exist_ok=True)
hge = load_hge(a.game_root)
bpy.ops.wm.open_mainfile(filepath=str(a.blend))
prefix = 'M16R_M16A4' if a.weapon == 'M16A4' else 'M4R_M4A1'
host = bpy.data.objects[prefix]
scale = 1.10
scope_forward = .035 if a.weapon == 'M4A1' else 0
magazine_back = .008 if a.weapon == 'M4A1' else .006
meshes = [o for o in bpy.data.objects if o.type == 'MESH' and o.name.startswith(prefix)]
# RearSight is shared between both weapons. Magazines keep their existing size,
# but the curved donor uses a different seating offset from the vanilla straight one.
affected = [o for o in meshes if not any(s in o.name for s in ('RearSight', 'HandguardRifle'))]
short = bpy.data.objects[prefix + '_BarrelShort']
normal = bpy.data.objects[prefix + '_Barrel']
if a.weapon == 'M16A4':
    # The old island classifier mistook the shortened tube for a sight island.
    # Copy the already separated NORMAL barrel, then shorten its end ring only.
    short.data = normal.data.copy()
    front = min(v.co.y for v in short.data.vertices)
    for v in short.data.vertices:
        if v.co.y < front + .0001:
            v.co.y += .10
    for child in short.children:
        if child.hge_obj_settings.spot_name == 'Muzzle':
            child.location.y = front + .10

for obj in meshes:
    if obj.parent:
        obj.parent.location *= scale
    if obj not in affected:
        continue
    obj.data = obj.data.copy()
    if 'Magazine' in obj.name:
        obj.data.transform(Matrix.Translation((0, -(magazine_back - .002), 0)))
    else:
        obj.data.transform(Matrix.Scale(scale, 4))
    for child in obj.children:
        if child.type == 'EMPTY':
            child.location *= scale

spots = {c.hge_obj_settings.spot_name: c for c in host.children if c.type == 'EMPTY'}
spots['Magazine'].location.y += magazine_back
spots['Scope'].location.y -= scope_forward
for obj in meshes:
    if 'Magazine' in obj.name:
        obj.parent.location.y += magazine_back
    if obj.name.endswith('_RearSight'):
        obj.parent.location.y -= scope_forward
carry = bpy.data.objects[prefix + '_CarryHandle']
carry.parent.location.y -= scope_forward
carry.data.transform(Matrix.Translation((0, scope_forward, 0)))

reports = {}
for obj in affected:
    # Long, thin authored A2 handguard strips trip the weld-spike gate.
    # Split edges in place (including interpolated loop UV), without moving surfaces.
    if obj.name == 'M16R_M16A4_Handguard':
        bm = bmesh.new()
        bm.from_mesh(obj.data)
        bmesh.ops.triangulate(bm, faces=list(bm.faces))
        edges = [e for e in bm.edges if e.calc_length() > .15]
        bmesh.ops.subdivide_edges(bm, edges=edges, cuts=3, use_grid_fill=False)
        bmesh.ops.triangulate(bm, faces=list(bm.faces))
        bm.to_mesh(obj.data)
        bm.free()
    reports[obj.name] = prepare_export_mesh(obj)
    assert not reports[obj.name], (obj.name, reports[obj.name])
    assert not obj.data.has_custom_normals
barrels = {}
for obj in affected:
    if '_Barrel' not in obj.name:
        continue
    tip = min(v.co.y for v in obj.data.vertices)
    muzzle = next(c for c in obj.children if c.hge_obj_settings.spot_name == 'Muzzle')
    assert abs(tip - muzzle.location.y) < .0001, (obj.name, tip, muzzle.location.y)
    barrels[obj.name] = {'tip_m': tip, 'triangles': len(obj.data.polygons)}
assert barrels[prefix + '_BarrelShort']['tip_m'] > barrels[prefix + '_Barrel']['tip_m'] + .09

# Canonical assembly retains all options; export is a separate, local-origin scene.
bpy.ops.wm.save_as_mainfile(filepath=str(a.output / (a.weapon + '-assembled.blend')))
keep = set(affected)
for obj in affected:
    keep.update(obj.children)
    if obj.parent:
        keep.add(obj.parent)
        obj.parent.location = Vector()
for obj in list(bpy.data.objects):
    if obj not in keep:
        bpy.data.objects.remove(obj, do_unlink=True)
bpy.ops.wm.save_as_mainfile(filepath=str(a.output / (a.weapon + '.blend')))
export_fbx(hge, a.output / (a.weapon + '.fbx'))
report = dict(weapon=a.weapon, scale=scale, magazine_back_m=magazine_back,
              scope_forward_m=scope_forward, barrels=barrels, mesh_checks=reports)
(a.output / 'fit-report.json').write_text(json.dumps(report, indent=2))
print(json.dumps(report))
