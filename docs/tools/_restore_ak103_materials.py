"""Reconstruct the missing AK103 cover material without changing geometry.

Run with Blender --background --factory-startup --python this.py --
--source-build PATH --out PATH --components AUDIT.json --game-root PATH [--render].
The cover uses a plain painted receiver patch, not the unverified receiver UV
layout. This is a reconstruction, not a recovery of the absent original MTL.
"""
import argparse
import hashlib
import json
import shutil
import sys
from pathlib import Path

import bpy
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _export_ak103_assets import load_hge
from _export_m14_family_assets import assign_hge_maps, export_fbx, save_tga
from _optimize_ak103_mesh import render_pairs


def pixels(image):
    w, h = image.size
    arr = np.empty(w * h * 4, dtype=np.float32)
    image.pixels.foreach_get(arr)
    return arr.reshape(h, w, 4)


def geometry_digest(mesh):
    mesh.calc_loop_triangles()
    values = {
        'vertices': [list(v.co) for v in mesh.vertices],
        'faces': [list(p.vertices) for p in mesh.polygons],
        'normals': [list(n.vector) for n in mesh.corner_normals],
    }
    return hashlib.sha256(json.dumps(values).encode()).hexdigest()


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--source-build', type=Path, required=True)
    p.add_argument('--out', type=Path, required=True)
    p.add_argument('--components', type=Path, required=True)
    p.add_argument('--game-root', type=Path, required=True)
    p.add_argument('--render', action='store_true')
    a = p.parse_args(sys.argv[sys.argv.index('--') + 1:])
    assert a.out.resolve() != a.source_build.resolve()
    tex = a.out / 'Textures'
    rig = a.out / 'rigged'
    tex.mkdir(parents=True, exist_ok=True)
    rig.mkdir(parents=True, exist_ok=True)
    hge = load_hge(a.game_root)
    bpy.ops.wm.open_mainfile(filepath=str(a.source_build / 'rigged/AK103_JA3.blend'), use_scripts=False)
    for im in bpy.data.images:
        if im.filepath:
            im.filepath = bpy.path.abspath(im.filepath)
    objects = [o for o in bpy.context.scene.objects if o.type == 'MESH' and o.name.startswith('AKR_AK103')]
    assert len(objects) == 6
    before = {o.name: o.data.copy() for o in objects}
    hashes = {o.name: geometry_digest(o.data) for o in objects}
    body = bpy.data.objects['AKR_AK103']
    assert len(body.data.polygons) == 19000
    component = next(c for c in json.loads(a.components.read_text())['entities']['AKR_AK103']['components'] if c['id'] == 11)
    faces = component['face_indices']
    assert len(faces) == 416
    points = np.array([body.data.vertices[v].co for i in faces for v in body.data.polygons[i].vertices]) * 1000
    assert np.allclose([points.min(axis=0), points.max(axis=0)], component['bbox_mm'], atol=.001)
    uv = body.data.uv_layers.active
    cover_loops = [i for f in faces for i in body.data.polygons[f].loop_indices]
    old_uv = np.array([uv.data[i].uv[:] for i in cover_loops])
    # Cover shares source slot zero with the receiver. Slot six must be unused.
    assert old_uv.min() >= -.00025 and old_uv.max() <= .25025
    assert not any(2 <= l.uv.x * 4 < 3 and 1 <= l.uv.y * 4 < 2 for l in uv.data)
    inset = 8 / 1024
    for i, v in zip(cover_loops, old_uv):
        local = np.clip(v * 4, 0, 1)
        uv.data[i].uv = ((2 + inset + local[0] * (1 - 2 * inset)) / 4,
                         (1 + inset + local[1] * (1 - 2 * inset)) / 4)

    mats = {}
    changes = {}
    for obj in objects:
        for slot, original in enumerate(list(obj.data.materials)):
            if original.name in mats:
                obj.data.materials[slot] = mats[original.name]
                continue
            mat = original.copy()
            mats[original.name] = mat
            obj.data.materials[slot] = mat
            images = {}
            for node in mat.node_tree.nodes:
                if node.type != 'TEX_IMAGE':
                    continue
                key = node.label
                original_image = node.image
                dest = tex / Path(original_image.filepath).name
                modified = key == 'RM' or obj == body
                if not modified:
                    shutil.copy2(original_image.filepath, dest)
                    im = bpy.data.images.load(str(dest), check_existing=False)
                    im.colorspace_settings.name = original_image.colorspace_settings.name
                else:
                    arr = pixels(original_image)
                    if key == 'RM':
                        old = arr[:, :, 0].copy()
                        # A floor retains native variation above the threshold.
                        floor = .52 if obj.name in {'AKR_AK103_Stock', 'AKR_AK103_Magazine'} else .44
                        arr[:, :, 0] = np.maximum(arr[:, :, 0], floor)
                        changes[obj.name] = {'roughness_floor': floor, 'changed_fraction': float(np.mean(old < floor))}
                    if obj == body:
                        assert arr.shape == (4096, 4096, 4)
                        patch_image = bpy.data.images.load(str(a.source_build / 'Textures' / ('AKR_AK103_Weapon_AK-103_' + key + '.tga')), check_existing=False)
                        patch_image.colorspace_settings.name = 'sRGB' if key == 'Base' else 'Non-Color'
                        source = pixels(patch_image)
                        h, w = source.shape[:2]
                        # Coordinates measured on a 1024px top-origin preview:
                        # plain black paint inside the receiver side panel.
                        patch = source[round(h*(1-482/1024)):round(h*(1-443/1024)),
                                       round(w*225/1024):round(w*405/1024)].copy()
                        temp = bpy.data.images.new('CoverPatch', width=patch.shape[1], height=patch.shape[0], alpha=True)
                        temp.colorspace_settings.name = patch_image.colorspace_settings.name
                        temp.pixels.foreach_set(patch.ravel())
                        temp.scale(1024, 1024)
                        patch = pixels(temp)
                        # This source strip was not authored for the cover UVs.
                        # Retain its paint colour with only faint grain, avoiding
                        # stretched source streaks that resemble woven fabric.
                        median = np.median(patch[:, :, :3], axis=(0, 1))
                        patch[:, :, :3] = median + (patch[:, :, :3] - median) * .06
                        if key == 'RM':
                            patch[:, :, 0] = np.maximum(patch[:, :, 0], .56)
                        elif key == 'Normal':
                            # Missing original bake: neutral tangent normal avoids
                            # inventing receiver bolts/ridges on the smooth cover.
                            patch[:] = (.5, .5, 1, 1)
                        arr[1024:2048, 2048:3072] = patch
                        bpy.data.images.remove(temp)
                        bpy.data.images.remove(patch_image)
                    im = save_tga(dest.stem, arr, tex, key == 'Base')
                node.image = im
                images[key] = im
            assign_hge_maps(hge, mat, images)
    report = {'cover_faces': len(faces), 'cover_tile': [2, 1], 'cover_patch_preview_pixels': [225,443,405,482],
              'cover_normal': 'neutral tangent normal; original bake absent', 'roughness': changes, 'geometry': {}}
    for obj in objects:
        digest = geometry_digest(obj.data)
        assert digest == hashes[obj.name], obj.name
        assert not obj.data.has_custom_normals
        report['geometry'][obj.name] = {'triangles': len(obj.data.loop_triangles), 'unchanged_geometry_and_normals_sha256': digest}
        if obj != body:
            assert all(tuple(a.uv) == tuple(b.uv) for a,b in zip(obj.data.uv_layers.active.data, before[obj.name].uv_layers.active.data))
    assert sum(v['triangles'] for k,v in report['geometry'].items() if not k.endswith('StockFolded')) == 33514
    (a.out / 'restoration-report.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    bpy.ops.wm.save_as_mainfile(filepath=str(rig / 'AK103_JA3.blend'))
    export_fbx(hge, rig / 'AK103_JA3.fbx')
    if a.render:
        render_pairs(a.out / 'review', objects, before)


if __name__ == '__main__':
    main()
