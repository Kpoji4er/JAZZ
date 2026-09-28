"""Offline Hatchet source preparation; run with Blender --background --python.

Arguments after --: --archive <zip> --out <new build directory>.
Never launches JA3 or writes generated mod data. Existing build output is refused.
"""
import argparse
import hashlib
import json
from pathlib import Path
import sys
import zipfile

import bpy

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _ja3_mesh_prepare import prepare_export_mesh, mesh_has_custom_normals
from _inspect_weapon_source import world_bbox, setup_render, render_views, describe


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--archive', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args(sys.argv[sys.argv.index('--') + 1:])
    archive = args.archive.resolve()
    out = args.out.resolve()
    if out.exists():
        raise RuntimeError(f'Refusing existing output directory: {out}')
    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    with zipfile.ZipFile(archive) as source:
        entries = source.infolist()
        if {e.filename for e in entries} != {'model_0.obj', 'model_1.obj'}:
            raise RuntimeError('Archive contents changed; inspect before preparing')
        raw = out / 'source'
        raw.mkdir(parents=True)
        for entry in entries:
            target = raw / entry.filename
            target.write_bytes(source.read(entry))
        manifest = [{'name': e.filename, 'bytes': e.file_size} for e in entries]
    bpy.ops.wm.read_factory_settings(use_empty=True)
    issues = {}
    for path in sorted(raw.glob('*.obj')):
        before = set(bpy.data.objects)
        bpy.ops.wm.obj_import(filepath=str(path))
        imported = sorted(set(bpy.data.objects) - before, key=lambda o: o.name)
        for index, obj in enumerate(imported):
            if obj.type != 'MESH':
                continue
            obj.name = f'Hatchet_{path.stem}_{index}'
            obj['source_file'] = path.name
            obj['material_status'] = 'Missing original textures and MTL'
            issues[obj.name] = prepare_export_mesh(obj, strict=False)
    meshes = [o for o in bpy.context.scene.objects if o.type == 'MESH']
    if not meshes:
        raise RuntimeError('No meshes imported')
    lo, hi = world_bbox(meshes)
    clean = out / 'clean'
    clean.mkdir()
    blend = clean / 'Hatchet.blend'
    bpy.ops.wm.save_as_mainfile(filepath=str(blend))
    bpy.ops.wm.open_mainfile(filepath=str(blend))
    meshes = [o for o in bpy.context.scene.objects if o.type == 'MESH']
    assert not any(mesh_has_custom_normals(o.data) for o in meshes)
    views = out / 'review'
    views.mkdir()
    setup_render(1200, 'SINGLE')
    previews = render_views(views, 'Hatchet', lo, hi)
    assert hashlib.sha256(archive.read_bytes()).hexdigest() == digest
    report = {
        'stage': 'source-preparation-only',
        'archive': str(archive), 'archive_sha256': digest,
        'archive_unchanged': True, 'entries': manifest,
        'clean_blend': str(blend), 'reopen_verified': True,
        'source_units': 'unknown; coordinates preserved, not game scale',
        'source_bbox_size': list(hi - lo),
        'objects': describe(meshes), 'mesh_audit': issues,
        'uv_layers': {o.name: len(o.data.uv_layers) for o in meshes},
        'custom_normals': {o.name: mesh_has_custom_normals(o.data) for o in meshes},
        'previews': previews,
        'integration_ready': False,
        'remaining': ['original textures/MTL absent', 'confirm scale and orientation',
                      'grip/animation and entity export', 'item/balance/localization/icon',
                      'editor and game acceptance deferred by owner'],
    }
    (out / 'prepare-report.json').write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({'report': str(out / 'prepare-report.json'),
                      'mesh_count': len(meshes),
                      'issues': {k: len(v) for k, v in issues.items()},
                      'previews': previews}, indent=2))


if __name__ == '__main__':
    main()
