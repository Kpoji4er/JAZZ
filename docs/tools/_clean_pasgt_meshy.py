"""Conservative PASGT cleanup; Blender -- --input GLB --output DIR. Keeps source UVs."""
import argparse
import json
import sys
from pathlib import Path
import bpy
import bmesh
from mathutils import Vector

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _ja3_mesh_prepare import prepare_export_mesh

p = argparse.ArgumentParser(description=__doc__)
p.add_argument('--input', type=Path, required=True)
p.add_argument('--output', type=Path, required=True)
a = p.parse_args(sys.argv[sys.argv.index('--') + 1:])
a.output.mkdir(parents=True, exist_ok=True)
if (a.output / 'PASGT.blend').exists():
    raise RuntimeError('Use a fresh output directory; preserve previous candidates')
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=str(a.input.resolve()))
reports = []
for obj in [o for o in bpy.context.scene.objects if o.type == 'MESH']:
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    if obj.data.has_custom_normals:
        bpy.ops.mesh.customdata_custom_splitnormals_clear()
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    original_triangles = len(bm.faces)
    lo = Vector(tuple(min(v.co[i] for v in bm.verts) for i in range(3)))
    hi = Vector(tuple(max(v.co[i] for v in bm.verts) for i in range(3)))
    height = hi.z - lo.z
    bmesh.ops.remove_doubles(bm, verts=list(bm.verts), dist=height * 1e-7)
    bm.verts.index_update()
    unique = set()
    duplicates = []
    for f in bm.faces:
        key = tuple(sorted(v.index for v in f.verts))
        if key in unique:
            duplicates.append(f)
        unique.add(key)
    bmesh.ops.delete(bm, geom=duplicates, context='FACES_ONLY')
    bmesh.ops.dissolve_degenerate(bm, edges=list(bm.edges), dist=height * 1e-9)
    # Meshy can leave one-triangle fins glued onto otherwise closed surfaces:
    # two exposed edges and a third edge shared with two intact surface faces.
    fins = [f for f in bm.faces if len(f.verts) == 3
            and sum(e.is_boundary for e in f.edges) == 2
            and sum(len(e.link_faces) == 3 for e in f.edges) == 1]
    bmesh.ops.delete(bm, geom=fins, context='FACES_ONLY')
    # Also remove tiny multi-triangle fins. Traverse ordinary two-face edges
    # only: a fin is separated from the main shell by the three-face junction.
    seen = set()
    fin_patches = []
    for seed in list(bm.faces):
        if seed in seen:
            continue
        stack = [seed]
        seen.add(seed)
        patch = []
        while stack:
            f = stack.pop()
            patch.append(f)
            for e in f.edges:
                if len(e.link_faces) == 2:
                    for other in e.link_faces:
                        if other not in seen:
                            seen.add(other)
                            stack.append(other)
        edges = {e for f in patch for e in f.edges}
        if len(patch) <= 4 and any(e.is_boundary for e in edges) and any(len(e.link_faces) > 2 for e in edges):
            fin_patches.extend(patch)
    bmesh.ops.delete(bm, geom=fin_patches, context='FACES_ONLY')
    loose_edges = [e for e in bm.edges if not e.link_faces]
    bmesh.ops.delete(bm, geom=loose_edges, context='EDGES')
    loose_vertices = [v for v in bm.verts if not v.link_faces]
    bmesh.ops.delete(bm, geom=loose_vertices, context='VERTS')
    bm.normal_update()
    original = {v: v.co.copy() for v in bm.verts}
    # Small local relaxation only. Preserve the collar, front pockets, hem,
    # open rims, and sharp creases; never replace an entire panel.
    eligible = []
    for v in bm.verts:
        z = (v.co.z - lo.z) / height
        x = abs((v.co.x - (lo.x + hi.x) / 2) / ((hi.x - lo.x) / 2))
        rear = v.co.y > (lo.y + hi.y) / 2
        patch = (rear and .28 < z < .82) or (x > .68 and .3 < z < .80)
        if patch and v.is_manifold and all(e.calc_face_angle(0) < 1.0 for e in v.link_edges):
            eligible.append(v)
    for step in range(8):
        updates = {}
        for v in eligible:
            neighbors = [e.other_vert(v) for e in v.link_edges]
            avg = sum((n.co for n in neighbors), Vector()) / len(neighbors)
            # Normal-only displacement avoids UV tangential sliding.
            delta = v.normal * (avg - v.co).dot(v.normal) * .28
            target = v.co + delta
            displacement = target - original[v]
            cap = height * .004
            if displacement.length > cap:
                target = original[v] + displacement.normalized() * cap
            updates[v] = target
        for v, co in updates.items():
            v.co = co
        bm.normal_update()
    report = {'original_triangles': original_triangles, 'duplicates_removed': len(duplicates), 'dangling_fins_removed': len(fins), 'fin_patch_faces_removed': len(fin_patches),
              'relaxed_vertices': len(eligible),
              'max_displacement_fraction_height': max((v.co-original[v]).length for v in bm.verts)/height,
              'boundary_edges': sum(e.is_boundary for e in bm.edges),
              'nonmanifold_edges': sum(len(e.link_faces)>2 for e in bm.edges),
              'nonmanifold_details': [{'faces': len(e.link_faces), 'center': list((e.verts[0].co+e.verts[1].co)/2)} for e in bm.edges if len(e.link_faces)>2]}
    bm.to_mesh(obj.data)
    bm.free()
    obj.data.update()
    report['normal_audit'] = prepare_export_mesh(obj)
    obj.data.calc_loop_triangles()
    report['triangles'] = len(obj.data.loop_triangles)
    reports.append(report)
bpy.ops.wm.save_as_mainfile(filepath=str((a.output / 'PASGT.blend').resolve()))
bpy.ops.export_scene.gltf(filepath=str((a.output / 'PASGT.glb').resolve()), export_format='GLB', export_animations=False)
(a.output / 'cleanup.json').write_text(json.dumps(reports, indent=2))
jobs = [{'name': 'clean', 'project': str(a.output.resolve()), 'model': str((a.output/'PASGT.glb').resolve())}]
(a.output / 'render-manifest.json').write_text(json.dumps({'jobs': jobs}, indent=2))
print(json.dumps(reports))
