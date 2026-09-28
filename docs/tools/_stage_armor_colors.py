"""Stage/verify/install existing armor albedo only. Blender performs native shader baking.

Run without --apply to capture the graph and decode source textures; then run
_bake_armor_colors.py in Blender. --apply compiles and installs with rollback.
"""
import argparse
import hashlib
import json
import shutil
import struct
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path
from _audit_armor_color_maps import decode

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    p = argparse.ArgumentParser(description=__doc__)
    for key in ('assets', 'output', 'game-root'):
        p.add_argument('--' + key, type=Path, required=True)
    p.add_argument('--apply', action='store_true')
    p.add_argument('--verify', action='store_true', help='Read-only installed hash, mip and albedo fidelity audit')
    a = p.parse_args()
    root = a.assets.resolve() / 'Entities'
    out = a.output.resolve()
    out.mkdir(parents=True, exist_ok=True)
    planfile = out / 'plan.json'
    if a.verify:
        import numpy as np
        from PIL import Image
        plan = json.loads(planfile.read_text())
        installed = json.loads((out / 'installation.json').read_text())
        assert all(sha(root / f) == h for f, h in installed['files'].items())
        assert all(sha(Path(f)) == h for f, h in plan['protected'].items())
        errors = {}
        for name, row in plan['maps'].items():
            path = root / 'Textures' / name
            actual = decode(path).convert('RGB')
            expected = Image.open(out / 'baked' / (name + '.tga')).convert('RGB')
            assert actual.size == expected.size == tuple(row['size'])
            error = float(np.abs(np.asarray(actual, dtype=np.float32) - np.asarray(expected, dtype=np.float32)).mean())
            assert error < 2, (name, error)
            assert struct.unpack_from('<I', path.read_bytes(), 28)[0] == max(row['size']).bit_length()
            fallback = path.parent / 'Fallbacks' / name
            assert max(decode(fallback).size) <= 64
            assert path.read_bytes()[128:132] == fallback.read_bytes()[128:132]
            errors[name] = error
        (out / 'verification.json').write_text(json.dumps({'status': 'PASS_STATIC', 'albedo_mean_absolute_error_255': errors, 'protected_files': len(plan['protected']), 'runtime': 'NOT_RUN'}, indent=2))
        print('PASS', len(errors), 'albedos;', len(installed['files']), 'installed files;', len(plan['protected']), 'protected; max mean error', max(errors.values()))
        return
    if not a.apply:
        assert not planfile.exists(), 'Use a fresh output directory'
        maps, protected, selected_materials = {}, {}, set()
        names = ['Chainmail'] + [f + v for f in ('Guardian', 'Twaron', 'Zylon') for v in ('Light', 'Medium', 'Full')]
        for name in names:
            ent = root / ('JAZZ_' + name + '_Male.ent')
            protected[str(ent)] = sha(ent)
            tree = ET.parse(ent)
            for ref in tree.findall('.//mesh'):
                f = root / ref.get('file')
                protected[str(f)] = sha(f)
            for ref in tree.findall('.//material'):
                f = root / ref.get('file')
                selected_materials.add(f.resolve())
                protected[str(f)] = sha(f)
                binary = f.with_suffix('.mtlbin')
                if binary.exists():
                    protected[str(binary)] = sha(binary)
                for mat in ET.parse(f).findall('Material'):
                    for node in mat:
                        if not node.tag.endswith('Map') or not node.get('Name'):
                            continue
                        tex = root / 'Textures' / node.get('Name')
                        if node.tag == 'BaseColorMap':
                            family = next(k for k in ('Chainmail', 'Guardian', 'Twaron', 'Zylon') if name.startswith(k))
                            record = {'family': family, 'before': sha(tex), 'size': list(decode(tex).size)}
                            assert maps.setdefault(tex.name, record) == record
                        else:
                            protected[str(tex)] = sha(tex)
                            fallback = tex.parent / 'Fallbacks' / tex.name
                            if fallback.exists():
                                protected[str(fallback)] = sha(fallback)
        # Refuse collateral changes to materials outside these entities.
        for f in (root / 'Materials').glob('*.mtl'):
            if f.resolve() in selected_materials:
                continue
            try:
                refs = {n.get('Name') for n in ET.parse(f).findall('.//BaseColorMap')}
            except ET.ParseError:
                continue
            assert not refs.intersection(maps), ('Albedo shared with unrelated material', f)
        assert len(maps) == 22, len(maps)
        inputs = out / 'inputs'
        inputs.mkdir()
        for name in maps:
            decode(root / 'Textures' / name).save(inputs / (name + '.png'))
        planfile.write_text(json.dumps({'maps': maps, 'protected': protected}, indent=2))
        print('STAGED', len(maps), 'albedo maps;', len(protected), 'protected files')
        return
    plan = json.loads(planfile.read_text())
    converter = a.game_root / 'ModTools/hgimgcvt.exe'
    assert all(sha(Path(f)) == h for f, h in plan['protected'].items()), 'Protected resource changed'
    assert not (out / 'installation.json').exists(), 'Already installed'
    check = subprocess.run(['powershell', '-NoProfile', '-Command',
        'Get-Process JA3,JA3Debug,ged -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Id'], capture_output=True, text=True)
    assert not check.stdout.strip(), 'Close game/editor before installation'
    writes = {}
    for name, row in plan['maps'].items():
        target = root / 'Textures' / name
        assert sha(target) == row['before'], ('Concurrent change', name)
        tga = out / 'baked' / (name + '.tga')
        assert tga.exists(), tga
        full = out / 'compiled' / name
        fallback = out / 'compiled/Fallbacks' / name
        full.parent.mkdir(exist_ok=True)
        fallback.parent.mkdir(exist_ok=True)
        subprocess.run([str(converter), str(tga), str(full), '--compression', 'BC7', '--profile', 'fast', '--mips', '13'], check=True, capture_output=True)
        # Albedo must retain the original sRGB sampling semantics (BC1/3 -> BC7).
        old_header = target.read_bytes()[:148]
        srgb = old_header[84:88] == b'DX10' and struct.unpack_from('<I', old_header, 128)[0] in (72, 75, 78, 99)
        data = bytearray(full.read_bytes())
        assert data[84:88] == b'DX10'
        struct.pack_into('<I', data, 128, 99 if srgb else 98)
        full.write_bytes(data)
        subprocess.run([str(converter), str(full), str(fallback), '--truncate', '64'], check=True, capture_output=True)
        data = bytearray(fallback.read_bytes())
        struct.pack_into('<I', data, 128, 99 if srgb else 98)
        fallback.write_bytes(data)
        assert list(decode(full).size) == row['size']
        assert max(decode(fallback).size) <= 64
        assert struct.unpack_from('<I', full.read_bytes(), 28)[0] == max(row['size']).bit_length()
        writes[target] = full
        writes[target.parent / 'Fallbacks' / name] = fallback
    backup = out / 'backup'
    assert not backup.exists()
    assert all(sha(root / 'Textures' / name) == row['before'] for name, row in plan['maps'].items()), 'Concurrent albedo change during compilation'
    before = {p: p.read_bytes() if p.exists() else None for p in writes}
    for target, data in before.items():
        if data is not None:
            dest = backup / target.relative_to(root)
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(data)
    try:
        assert all(sha(Path(f)) == h for f, h in plan['protected'].items())
        for target, source in writes.items():
            target.parent.mkdir(exist_ok=True)
            shutil.copy2(source, target)
        assert all(sha(p) == sha(s) for p, s in writes.items())
        assert all(sha(Path(f)) == h for f, h in plan['protected'].items())
    except Exception:
        for target, data in before.items():
            if data is None:
                target.unlink(missing_ok=True)
            else:
                target.write_bytes(data)
        raise
    (out / 'installation.json').write_text(json.dumps({'files': {str(p.relative_to(root)): sha(p) for p in writes}, 'protected': len(plan['protected']), 'runtime': 'NOT_RUN'}, indent=2))
    print('INSTALLED', len(writes), 'files; geometry/UV/material/Normal/RM hashes unchanged; runtime NOT_RUN')

if __name__ == '__main__':
    main()
