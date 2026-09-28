"""Validate/replace only the three existing improvised armor graphs, with rollback.

Input: --build-root containing kind/build and kind/poses. Default is validation;
--apply installs closed-game resources and icons, without touching registration.
"""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path

from _install_soft_legion_armor import ASSETS, ROOT, ROWS, validate


def digest(data):
    return hashlib.sha256(data).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--build-root', required=True, type=Path)
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    build_root = args.build_root.resolve()
    writes = {}
    for kind, item in ROWS:
        folder = build_root / kind
        pose = json.loads((folder / 'poses/pose-check.json').read_text())
        assert pose['status'] == 'PASS_SKIN_STRUCTURE', kind
        compiled = json.loads((folder / 'compiled-audit.json').read_text())
        assert compiled['pass'], (kind, 'Compiled topology mismatch')
        visual = json.loads((folder / 'visual-review.json').read_text())
        assert visual['status'] == 'REVIEWED_FOR_GAME_TEST', (kind, 'Missing visual review')
        assert visual['source_sha256'] == digest((folder / (kind+'.blend')).read_bytes()), (kind, 'Review is stale')
        report = json.loads((folder / 'build/report.json').read_text())
        entity = 'JAZZ_' + item + '_Male'
        assert report['entity'] == entity and report['inherit'] == 'Male'
        assert report['baked_maps'] == ['Base', 'Norm', 'RM']
        stage = validate(folder / 'build', entity, item)
        for source in stage.rglob('*'):
            if not source.is_file() or source.suffix == '.lua':
                continue
            target = ASSETS / 'Entities' / source.relative_to(stage)
            assert target.resolve().is_relative_to((ASSETS / 'Entities').resolve())
            assert source.name.startswith('JAZZ_' + item), source
            assert target.is_file(), ('Unexpected new resource', target)
            writes[target] = source.read_bytes()
        icon = ROOT / 'ArmorIcons' / (item + '.png')
        assert icon.is_file()
        writes[icon] = (folder / 'build' / (item + '.png')).read_bytes()

    # Run the existing exact item/entity/test-loadout checks before mutation.
    manifest = build_root / 'installation.json'
    assert not manifest.exists(), 'Already installed; choose a fresh build root'
    manifest.write_text(json.dumps({'installed': False, 'sha256': {}}))
    try:
        subprocess.run([
            'python', str(ROOT / 'docs/tools/_check_soft_legion_armor.py'),
            '--build-root', str(build_root),
        ], check=True)
    finally:
        manifest.unlink()
    before = {path: path.read_bytes() for path in writes}
    plan = {
        'runtime': 'NOT_RUN', 'human': 'PENDING', 'files': len(writes),
        'before': {str(p.relative_to(ROOT.parent)): digest(v) for p, v in before.items()},
        'sha256': {str(p.relative_to(ROOT.parent)): digest(v) for p, v in writes.items()},
    }
    (build_root / 'resource-refresh-plan.json').write_text(json.dumps(plan, indent=2))
    print('PASS targeted registration, resource graphs, poses, icons;', len(writes), 'files')
    if not args.apply:
        return
    processes = subprocess.run([
        'powershell', '-NoProfile', '-Command',
        'Get-Process JA3,JA3Debug,ged -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Id',
    ], capture_output=True, text=True)
    assert not processes.stdout.strip(), 'Game/editor must be closed for installation'
    backup = build_root / 'resource-backup'
    assert not backup.exists(), 'Backup exists; refusing overwrite'
    for path, data in before.items():
        dest = backup / path.relative_to(ROOT.parent)
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(data)
    # Check every destination before the first write.
    assert all(path.read_bytes() == data for path, data in before.items()), 'Concurrent edit'
    try:
        for path, data in writes.items():
            path.write_bytes(data)
        assert all(path.read_bytes() == data for path, data in writes.items())
        manifest.write_text(json.dumps(dict(plan, installed=True), indent=2))
        subprocess.run([
            'python', str(ROOT / 'docs/tools/_check_soft_legion_armor.py'),
            '--build-root', str(build_root),
        ], check=True)
    except Exception:
        for path, data in before.items():
            path.write_bytes(data)
        if manifest.exists():
            manifest.unlink()
        raise
    print('INSTALLED experimental armor resources; native animation/human acceptance pending')


if __name__ == '__main__':
    main()
