"""Inspect and trial-fit the existing AK74M dust cover on AK103, offline.

Blender --background --factory-startup --python this.py --
--donor AK74M_JAZZ.blend --out trial [--inspect].
"""
import argparse
from collections import defaultdict
import json
from pathlib import Path
import shutil
import sys

import bmesh
import bpy
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _ja3_mesh_prepare import prepare_export_mesh
from _export_ak103_assets import load_hge
from _export_m14_family_assets import assign_hge_maps, export_fbx, save_tga
from _restore_ak103_materials import geometry_digest, pixels
from _optimize_ak103_mesh import render_pairs


def components(mesh):
    parent = list(range(len(mesh.vertices)))
    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i
    # OBJ seams may duplicate indices: group coincident positions for inspection
    # only, without welding or changing the actual donor geometry/UV.
    positions = {}
    for v in mesh.vertices:
        key = tuple(round(c, 7) for c in v.co)
        if key in positions:
            parent[find(v.index)] = find(positions[key])
        positions[key] = v.index
    for p in mesh.polygons:
        for v in p.vertices[1:]:
            parent[find(v)] = find(p.vertices[0])
    groups = defaultdict(list)
    for p in mesh.polygons:
        groups[find(p.vertices[0])].append(p.index)
    rows = []
    for idx, faces in enumerate(sorted(groups.values(), key=len, reverse=True)):
        vertices = {v for f in faces for v in mesh.polygons[f].vertices}
        xyz = np.array([mesh.vertices[v].co[:] for v in vertices])
        rows.append({'id': idx, 'faces': faces, 'triangles': sum(len(mesh.polygons[f].vertices)-2 for f in faces),
                     'bbox_mm': [list(xyz.min(axis=0)*1000), list(xyz.max(axis=0)*1000)],
                     'materials': sorted({mesh.polygons[f].material_index for f in faces})})
    return rows


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--donor', type=Path, required=True)
    p.add_argument('--out', type=Path, required=True)
    p.add_argument('--inspect', action='store_true')
    p.add_argument('--source-build', type=Path)
    p.add_argument('--game-root', type=Path)
    p.add_argument('--render', action='store_true')
    a = p.parse_args(sys.argv[sys.argv.index('--') + 1:])
    a.out.mkdir(parents=True, exist_ok=True)
    bpy.ops.wm.open_mainfile(filepath=str(a.donor), use_scripts=False)
    donor = bpy.data.objects['AKR_AK74M']
    rows = components(donor.data)
    (a.out/'donor-components.json').write_text(json.dumps(rows, indent=2), encoding='utf-8')
    for row in rows:
        if row['triangles'] >= 50:
            print(json.dumps({k:v for k,v in row.items() if k != 'faces'}), flush=True)
    if a.inspect:
        return
    assert a.source_build and a.game_root
    assert a.out.resolve() != a.source_build.resolve()
    cover = rows[1]
    assert cover['triangles'] == 827 and cover['materials'] == [0]
    # Capture the donor before opening the host scene. UVs remain per corner.
    donor_faces = [donor.data.polygons[f] for f in cover['faces']]
    used = sorted({v for face in donor_faces for v in face.vertices})
    remap = {v:i for i,v in enumerate(used)}
    coords = [tuple(donor.data.vertices[v].co) for v in used]
    polys = [tuple(remap[v] for v in f.vertices) for f in donor_faces]
    donor_uv = [tuple(donor.data.uv_layers.active.data[l].uv) for f in donor_faces for l in f.loop_indices]
    bsdf = donor.data.materials[0].node_tree.nodes.get('Principled BSDF')
    paths = {}
    for key, socket in [('Base','Base Color'),('Rough','Roughness'),('Metal','Metallic'),('Normal','Normal')]:
        node = bsdf.inputs[socket].links[0].from_node
        if key == 'Normal':
            node = node.inputs['Color'].links[0].from_node
        assert node.type == 'TEX_IMAGE'
        paths[key] = Path(bpy.path.abspath(node.image.filepath))
        if not paths[key].is_file():
            paths[key] = a.donor.parent/'AK74M/source'/paths[key].name
        assert paths[key].is_file()
    hge = load_hge(a.game_root)
    bpy.ops.wm.open_mainfile(filepath=str(a.source_build/'rigged/AK103_JA3.blend'), use_scripts=False)
    for image in bpy.data.images:
        if image.filepath:
            image.filepath = bpy.path.abspath(image.filepath)
    objects = [o for o in bpy.context.scene.objects if o.type == 'MESH' and o.name.startswith('AKR_AK103')]
    before = {o.name:o.data.copy() for o in objects}
    hashes = {o.name:geometry_digest(o.data) for o in objects}
    body = bpy.data.objects['AKR_AK103']
    assert len(body.data.polygons) == 19000
    target_faces = list(range(18584,19000))
    xyz = np.array([body.data.vertices[v].co[:] for f in target_faces for v in body.data.polygons[f].vertices])
    lo, hi = xyz.min(axis=0), xyz.max(axis=0)
    assert np.allclose([lo*1000,hi*1000],[[-11.469,-212.174,60.015],[27.628,25.623,94.912]],atol=.001)
    donor_mesh = bpy.data.meshes.new('AK74M_CoverTrial')
    donor_mesh.from_pydata(coords, [], polys)
    layer = donor_mesh.uv_layers.new(name=body.data.uv_layers.active.name)
    for l, uv in zip(layer.data, donor_uv):
        l.uv = uv
    cap = bpy.data.objects.new('AK74M_CoverTrial', donor_mesh)
    bpy.context.scene.collection.objects.link(cap)
    # Both prepared entity meshes use Z-up and muzzle toward local -Y.
    pts = np.array([v.co[:] for v in donor_mesh.vertices])
    d_lo, d_hi = pts.min(axis=0), pts.max(axis=0)
    scale = (hi-lo)/(d_hi-d_lo)
    assert np.all((scale > .9) & (scale < 1.1)), scale
    for v in donor_mesh.vertices:
        v.co = (np.array(v.co[:])-d_lo)*scale+lo
        # The AK74M receiver supports a stepped left-front skirt. AK103's
        # receiver lip is lower here: extend only that rim, up to 8mm, easing
        # into the existing low rim. Keep the roof and ejection side intact.
        if v.co.x > .020:
            longitudinal = np.clip((-.136-v.co.y)/.007,0,1)
            height_weight = np.clip((.0784-v.co.z)/.0104,0,1)
            v.co.z -= .008 * longitudinal * height_weight
    cap.matrix_world = body.matrix_world.copy()
    # Weld only coincident donor seam vertices, preserving corner UVs. Never
    # weld to the host receiver or modify unrelated original AK103 geometry.
    bm = bmesh.new(); bm.from_mesh(donor_mesh)
    bmesh.ops.remove_doubles(bm, verts=list(bm.verts), dist=1e-7)
    bm.to_mesh(donor_mesh); bm.free()
    prepare_export_mesh(cap)
    assert len(donor_mesh.polygons) == 827
    tex = a.out/'Textures'; tex.mkdir(exist_ok=True)
    mat = body.data.materials[0].copy()
    body.data.materials[0] = mat
    cap.data.materials.append(mat)
    uv_points = np.array([l.uv[:] for l in cap.data.uv_layers.active.data])
    uv_lo, uv_hi = uv_points.min(axis=0), uv_points.max(axis=0)
    assert uv_lo.min() >= 0 and uv_hi.max() <= 1
    maps = {}
    crop_bounds = None
    for key, path in paths.items():
        im = bpy.data.images.load(str(path), check_existing=False)
        im.colorspace_settings.name = 'sRGB' if key == 'Base' else 'Non-Color'
        arr = pixels(im); h,w = arr.shape[:2]
        lower = np.maximum(0, np.floor(uv_lo*[w,h]).astype(int)-8)
        upper = np.minimum([w,h], np.ceil(uv_hi*[w,h]).astype(int)+8)
        bounds = (lower/np.array([w,h]), upper/np.array([w,h]))
        if crop_bounds is None:
            crop_bounds = bounds
        assert np.allclose(crop_bounds, bounds)
        arr = arr[lower[1]:upper[1],lower[0]:upper[0]].copy()
        patch = bpy.data.images.new('DonorCoverPatch',width=arr.shape[1],height=arr.shape[0],alpha=True)
        patch.colorspace_settings.name = im.colorspace_settings.name
        patch.pixels.foreach_set(arr.ravel()); patch.scale(2048,2048)
        maps[key] = pixels(patch)
        bpy.data.images.remove(patch); bpy.data.images.remove(im)
    rm = np.ones_like(maps['Rough']); rm[:,:,0] = np.maximum(maps['Rough'][:,:,0],.44)
    rm[:,:,1] = 0; rm[:,:,2] = maps['Metal'][:,:,0]; maps['RM'] = rm
    # Match the darker AK103 finish while retaining donor wear and normal map.
    maps['Base'][:,:,:3] *= .65
    # One body material: the donor crop occupies four previously unused cells.
    for l in cap.data.uv_layers.active.data:
        local = (np.array(l.uv[:])-crop_bounds[0])/(crop_bounds[1]-crop_bounds[0])
        l.uv = local*.5+np.array([.5,.5])
    images = {}
    for node in mat.node_tree.nodes:
        if node.type != 'TEX_IMAGE':
            continue
        arr = pixels(node.image)
        assert arr.shape == (4096,4096,4)
        arr[2048:4096,2048:4096] = maps[node.label]
        im = save_tga('AKR_AK103_DonorCover_'+node.label,arr,tex,node.label=='Base')
        node.image = im; images[node.label] = im
    assign_hge_maps(hge,mat,images)
    # Detach only the identified original cover, retaining every other face.
    bm = bmesh.new(); bm.from_mesh(body.data); bm.faces.ensure_lookup_table()
    bmesh.ops.delete(bm,geom=[bm.faces[i] for i in target_faces],context='FACES')
    bm.to_mesh(body.data); bm.free()
    bpy.ops.object.select_all(action='DESELECT')
    body.hide_set(False); body.select_set(True); cap.select_set(True)
    bpy.context.view_layer.objects.active = body
    bpy.ops.object.join()
    issues = prepare_export_mesh(body, strict=False)
    # Existing tiny host face is recorded separately; donor was strict-clean.
    assert all(i['kind'] == 'zero_normal' for i in issues), issues
    assert len(body.data.polygons) == 19411
    def surface(mesh, count):
        uv = mesh.uv_layers.active.data
        return sorted(tuple(sorted(tuple(round(x,8) for x in (*mesh.vertices[mesh.loops[l].vertex_index].co,*uv[l].uv))
                                   for l in p.loop_indices)) for p in list(mesh.polygons)[:count])
    assert surface(body.data,18584) == surface(before[body.name],18584)
    # Copy untouched part textures to keep the candidate independent.
    copied = set()
    for obj in objects:
        if obj == body:
            continue
        assert geometry_digest(obj.data) == hashes[obj.name]
        for original in obj.data.materials:
            if original.name in copied:
                continue
            copied.add(original.name)
            part_images = {}
            for node in original.node_tree.nodes:
                if node.type == 'TEX_IMAGE':
                    dest = tex/Path(node.image.filepath).name
                    shutil.copy2(node.image.filepath,dest)
                    im = bpy.data.images.load(str(dest),check_existing=False)
                    im.colorspace_settings.name = node.image.colorspace_settings.name
                    node.image = im; part_images[node.label] = im
            assign_hge_maps(hge,original,part_images)
    report = {'donor_component':1,'donor_triangles':827,'removed_triangles':416,'body_triangles':19411,
              'assembled_triangles':33925,'fit_scale_xyz':list(scale),'target_bbox_m':[list(lo),list(hi)],
              'donor_uv_crop':[list(x) for x in crop_bounds],'host_mesh_issues':issues,
              'other_parts_geometry_unchanged':True,'runtime':'NOT_RUN'}
    report.update(host_noncover_surface_uv_unchanged=True, left_front_skirt_max_extension_mm=8, donor_base_gain=.65)
    (a.out/'fit-report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    rig = a.out/'rigged'; rig.mkdir(exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(rig/'AK103_JA3.blend'))
    export_fbx(hge,rig/'AK103_JA3.fbx')
    if a.render:
        render_pairs(a.out/'review',objects,before)


if __name__ == '__main__':
    main()
