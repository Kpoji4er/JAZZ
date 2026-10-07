"""Audit staged PASGT/RBA resources; --apply installs after closed-game and QA gates."""
import argparse
import hashlib
import io
import json
from pathlib import Path
import shutil
import struct
import subprocess
import xml.etree.ElementTree as ET
import numpy as np
from PIL import Image

p = argparse.ArgumentParser(description=__doc__)
p.add_argument('--apply', action='store_true')
a = p.parse_args()
root = Path(__file__).resolve().parents[2]
assets = root.parent / 'jazz_assets'
changes = {}
reports = []
for item in ('PASGT', 'RBA'):
    entity = 'JAZZ_' + item + '_Male'
    src = assets / 'Sources/Character' / entity / 'import-20261007'
    for audit in ('compiled-audit.json', 'skin-audit.json'):
        assert json.loads((src / audit).read_text())['pass'], audit
    assert json.loads((src / 'poses/pose-check.json').read_text())['status'] == 'PASS_SKIN_STRUCTURE'
    stage = src / 'build/mod-assets-stage/Entities'
    mtl = stage / 'Materials' / (entity + '_mesh.mtl')
    tree = ET.parse(mtl)
    for tag in tree.getroot().iter():
        old = tag.get('Name')
        if not old:
            continue
        suffix = {'NormalMap': 'Norm', 'BaseColorMap': 'Base', 'RMMap': 'RM'}[tag.tag]
        name = entity + '_' + suffix + '.dds'
        for folder in ('Textures', 'Textures/Fallbacks'):
            if old != name:
                shutil.copy2(stage / folder / old, stage / folder / name)
        tag.set('Name', name)
    tree.write(mtl, encoding='utf-8', xml_declaration=True)
    rm = np.asarray(Image.open(src / 'build' / (entity + '_RM.tga')).convert('RGB')).astype(int)
    assert np.array_equal(rm[:, :, 0], rm[:, :, 1])
    rows = []
    for folder, size, mips in [('Textures', 2048, 12), ('Textures/Fallbacks', 64, 7)]:
        for suffix in ('Base', 'Norm', 'RM'):
            f = stage / folder / (entity + '_' + suffix + '.dds')
            buf = bytearray(f.read_bytes())
            assert struct.unpack_from('<I', buf, 28)[0] == mips
            if buf[84:88] == b'DX10':
                fmt = struct.unpack_from('<I', buf, 128)[0]
                if fmt in (72, 75, 78, 99):
                    struct.pack_into('<I', buf, 128, fmt - 1)
            im = Image.open(io.BytesIO(buf))
            assert im.size == (size, size)
            row = {'path': str(f.relative_to(stage)), 'size': size, 'mips': mips}
            if suffix == 'RM':
                pixels = np.asarray(im.convert('RGB')).astype(int)
                row['rg_delta'] = int(abs(pixels[:, :, 0] - pixels[:, :, 1]).max())
                assert row['rg_delta'] <= 8
            rows.append(row)
    ent = ET.parse(stage / (entity + '.ent'))
    assert ent.find('.//inherit').get('entity') == 'Male'
    assert not ent.findall('.//src')
    for tag in ent.findall('.//mesh') + ent.findall('.//material'):
        assert (stage / tag.get('file')).exists()
    report = {'pass': True, 'source_rm_rg_exact': True, 'dds': rows}
    (src / 'texture-audit.json').write_text(json.dumps(report, indent=2))
    files = [Path(entity + '.ent'), Path('Meshes') / (entity + '_mesh.m.hgm'), Path('Materials') / (entity + '_mesh.mtl')]
    files += [Path(folder) / (entity + '_' + s + '.dds') for folder in ('Textures', 'Textures/Fallbacks') for s in ('Base', 'Norm', 'RM')]
    for file in files:
        changes[assets / 'Entities' / file] = (stage / file).read_bytes()
    changes[assets / 'Entities' / (entity + '.lua')] = ('EntityData["' + entity + '"] = { editor_artset = "Mods", entity = { class_parent = "CharacterArmorMale" } }\n').encode()
    reports.append(src)

items = assets / 'items.lua'
data = items.read_bytes()
meta = assets / 'metadata.lua'
metadata = meta.read_bytes()
code = root / 'Code/System_LegionArmorVisuals.lua'
mapping = code.read_bytes()
for item in ('PASGT', 'RBA'):
    entity = 'JAZZ_' + item + '_Male'
    assert entity.encode() not in data, 'Already registered: inspect receipt before rerunning installation'
    record = ("PlaceObj('ModItemEntity', {\n    'name', \"" + entity + "\",\n    'class_parent', \"CharacterArmorMale\",\n    'ClassParents', { \"CharacterArmorMale\" },\n    'entity_name', \"" + entity + "\",\n}),\n").encode()
    pos = data.rfind(b'}')
    data = data[:pos] + record + data[pos:]
    for old, new in [('"JAZZ_6B13_Male",', '"' + entity + '",'), ('"Entities/JAZZ_6B13_Male.lua",', '"Entities/' + entity + '.lua",')]:
        assert metadata.count(old.encode()) == 1
        metadata = metadata.replace(old.encode(), old.encode() + b'\n\t\t' + new.encode())
    anchor = b'\tJazzArmor_6B13 = { Male = "JAZZ_6B13_Male" },'
    assert mapping.count(anchor) == 1
    assert ('JazzArmor_' + item + ' =').encode() not in mapping
    mapping = mapping.replace(anchor, anchor + ('\n\tJazzArmor_' + item + ' = { Male = "' + entity + '" },').encode())
changes.update({items: data, meta: metadata, code: mapping})
print('PASS staged resource/texture/pose/compiled gates; planned files:', len(changes))
if not a.apply:
    raise SystemExit(0)
state = subprocess.run(['powershell', '-NoProfile', '-Command', 'Get-Process JA3,JA3Debug,ged -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Id'], capture_output=True, text=True)
assert not state.stdout.strip(), 'Close game/editor before install'
backup = reports[0] / 'installation-backup'
receipt = reports[0] / 'installation.json'
assert not receipt.exists()
rows = []
for dest, content in changes.items():
    rel = dest.relative_to(root.parent)
    if dest.exists():
        saved = backup / rel
        saved.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(dest, saved)
    rows.append({'path': rel.as_posix(), 'sha256': hashlib.sha256(content).hexdigest()})
for dest, content in changes.items():
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(content)
for row in rows:
    assert hashlib.sha256((root.parent / row['path']).read_bytes()).hexdigest() == row['sha256']
result = {'files': rows, 'runtime': 'NOT_RUN', 'editor': 'NOT_RUN', 'source_preserved': True}
for folder in reports:
    (folder / 'installation.json').write_text(json.dumps(result, indent=2))
print('Installed; backup and SHA256 verified')
