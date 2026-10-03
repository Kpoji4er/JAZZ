"""Stage compiled Conrad resources at full texture resolution; never installs.

--build DIR --export-root DIR --game-root DIR
Output: BUILD/mod-assets-stage/Entities and stage-manifest.json.
"""
import argparse
import hashlib
import json
import shutil
import struct
import subprocess
from pathlib import Path
import xml.etree.ElementTree as ET

p = argparse.ArgumentParser()
for name in ('build', 'export-root', 'game-root'):
    p.add_argument('--' + name, type=Path, required=True)
a = p.parse_args()
out = a.build / 'mod-assets-stage' / 'Entities'
out.mkdir(parents=True, exist_ok=True)
names = {}
suffixes = {'BaseColorMap': 'Base', 'NormalMap': 'Norm', 'RMMap': 'RM',
            'RoughnessMetallicMap': 'RM'}
for part in ('Body', 'Pants', 'Head'):
    name = 'JAZZ_Conrad' + part
    ent = ET.parse(a.export_root / (name + '.ent'))
    ent.getroot().set('name', name)
    for lod in ent.findall('.//lod'):
        for src in lod.findall('src'):
            lod.remove(src)
    for mesh in ent.findall('.//mesh'):
        rel = Path(mesh.attrib['file'])
        assert (out / rel).resolve().is_relative_to(out.resolve())
        (out / rel).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(a.export_root / rel, out / rel)
    for ref in ent.findall('.//material'):
        rel = Path(ref.attrib['file'])
        assert (out / rel).resolve().is_relative_to(out.resolve())
        mat = ET.parse(a.export_root / rel)
        for node in mat.getroot().iter():
            old = node.get('Name')
            if not old:
                continue
            assert node.tag in suffixes, (node.tag, old)
            source = a.export_root / 'Textures' / old
            digest = hashlib.sha256(source.read_bytes()).hexdigest()
            key = (suffixes[node.tag], digest)
            if key not in names:
                filename = f'JAZZ_Conrad_{len(names)+1}_{suffixes[node.tag]}.dds'
                names[key] = filename
                target = out / 'Textures' / filename
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, target)
                fallback = out / 'Textures' / 'Fallbacks' / filename
                fallback.parent.mkdir(parents=True, exist_ok=True)
                subprocess.run([str(a.game_root / 'ModTools/hgimgcvt.exe'),
                                str(target), str(fallback), '--truncate', '64'],
                               check=True, capture_output=True)
            node.set('Name', names[key])
        (out / rel).parent.mkdir(parents=True, exist_ok=True)
        mat.write(out / rel, encoding='utf-8', xml_declaration=True)
    ent.write(out / (name + '.ent'), encoding='utf-8', xml_declaration=True)
    (out / (name + '.lua')).write_text(
        f'EntityData["{name}"] = {{ editor_artset = "Mods", entity = '
        f'{{ class_parent = "Character{part}Male" }} }}\n', encoding='utf-8')
manifest = []
for path in sorted(out.rglob('*')):
    if not path.is_file():
        continue
    data = path.read_bytes()
    row = {'path': path.relative_to(out).as_posix(),
           'sha256': hashlib.sha256(data).hexdigest()}
    if path.suffix == '.dds':
        assert data[:4] == b'DDS '
        height, width = struct.unpack_from('<II', data, 12)
        row['size'] = [width, height]
    manifest.append(row)
(a.build / 'stage-manifest.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')
print(f'Staged {len(manifest)} files, {len(names)} full-resolution texture pairs: {out}')
