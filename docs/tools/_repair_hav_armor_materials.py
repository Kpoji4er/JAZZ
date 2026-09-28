"""Repair imported HAV grayscale RM maps from original split G/B channels.

Stages maps by default; --apply installs only the nine HAV texture graphs.
Never changes meshes, weights, material definitions, base colour or normals.
"""
import argparse
import hashlib
import json
import shutil
import struct
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path

import numpy as np
from PIL import Image


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    p = argparse.ArgumentParser(description=__doc__)
    for arg in ('assets', 'source', 'output', 'game-root'):
        p.add_argument('--' + arg, type=Path, required=True)
    p.add_argument('--apply', action='store_true')
    a = p.parse_args()
    a.output.mkdir(parents=True, exist_ok=True)
    entities = a.assets / 'Entities'
    textures = entities / 'Textures'
    converter = a.game_root / 'ModTools/hgimgcvt.exe'
    sources = {}
    for idx in (0, 4, 8):
        for channel in ('G', 'B'):
            path = a.source / f'gltf_embedded_{idx}@channels={channel}.png'
            sources[idx, channel] = np.asarray(Image.open(path).convert('L').resize((128, 128))).astype(float)
        rough = Image.open(a.source / f'gltf_embedded_{idx}@channels=G.png').convert('L')
        metal = Image.open(a.source / f'gltf_embedded_{idx}@channels=B.png').convert('L')
        tga = a.output / f'RM{idx}.tga'
        Image.merge('RGB', (rough, Image.new('L', rough.size, 0), metal)).save(tga)
        subprocess.run([str(converter), str(tga), str(a.output / f'RM{idx}.dds'),
                        '--compression', 'BC7', '--profile', 'fast', '--mips', '13'], check=True, capture_output=True)
    graph, mapping, protected = set(), {}, {}
    for family in ('Guardian', 'Twaron', 'Zylon'):
        for tier in ('Light', 'Medium', 'Full'):
            ent = entities / f'JAZZ_{family}{tier}_Male.ent'
            protected[str(ent)] = digest(ent)
            tree = ET.parse(ent)
            for node in tree.findall('.//mesh'):
                mesh = entities / node.get('file')
                protected[str(mesh)] = digest(mesh)
            for ref in {n.get('file') for n in tree.findall('.//material')}:
                mtl = entities / ref
                protected[str(mtl)] = digest(mtl)
                for mat in ET.parse(mtl).findall('Material'):
                    for node in mat:
                        if node.tag.endswith('Map') and node.get('Name'):
                            name = node.get('Name')
                            graph.add(name)
                            if node.tag != 'RMMap':
                                protected[str(textures / name)] = digest(textures / name)
                    name = mat.find('RMMap').get('Name')
                    pixels = np.asarray(Image.open(textures / name).convert('RGB').resize((128, 128))).astype(float)
                    assert np.abs(pixels[:, :, 0] - pixels[:, :, 2]).mean() < 2, f'{name}: not original grayscale map; refuse repeat apply'
                    channel = 'B' if family == 'Guardian' else 'G'
                    error, idx = min((float(np.abs(pixels[:, :, 0] - sources[i, channel]).mean()), i) for i in (0, 4, 8))
                    assert error < 2, (name, error)
                    if name in mapping:
                        assert mapping[name]['source'] == idx
                    mapping[name] = {'source': idx, 'match_error_255': error, 'before': digest(textures / name)}
    assert len(mapping) == 21 and len(graph) == 84, (len(mapping), len(graph))
    if a.apply:
        backup = a.output / 'backup'
        backup.mkdir(exist_ok=True)
        for name, info in mapping.items():
            target = textures / name
            if (backup / name).exists():
                assert digest(backup / name) == digest(target), f'Different backup: {name}'
            else:
                shutil.copy2(target, backup / name)
            shutil.copy2(a.output / f'RM{info["source"]}.dds', target)
            info['after'] = digest(target)
        fallback = textures / 'Fallbacks'
        fallback.mkdir(exist_ok=True)
        for name in sorted(graph):
            target = fallback / name
            if target.exists():
                (backup / 'Fallbacks').mkdir(exist_ok=True)
                shutil.copy2(target, backup / 'Fallbacks' / name)
            subprocess.run([str(converter), str(textures / name), str(target), '--truncate', '64'], check=True, capture_output=True)
            header = target.read_bytes()[:128]
            assert header[:4] == b'DDS ', name
            dimensions = struct.unpack_from('<II', header, 12)
            assert max(dimensions) <= 64, (name, dimensions)
        assert all(digest(Path(path)) == sha for path, sha in protected.items())
    report = {'applied': a.apply, 'maps': mapping, 'fallback_count': len(graph),
              'protected_hashes': protected, 'runtime': 'BLOCKED'}
    (a.output / 'repair-report.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(f'RM maps: {len(mapping)}; fallbacks: {len(graph)}; applied: {a.apply}; protected files: {len(protected)}')


if __name__ == '__main__':
    main()
