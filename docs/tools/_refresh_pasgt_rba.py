"""Refresh existing PASGT or RBA only; preserve registration; backups and geometry/texture gates."""
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
p.add_argument('--source', type=Path, required=True)
p.add_argument('--item', choices=('PASGT','RBA'), required=True)
a = p.parse_args()
root = Path(__file__).resolve().parents[2]
assets = root.parent / 'jazz_assets'
changes = {}
reports = []
for item in (a.item,):
    entity = 'JAZZ_' + item + '_Male'
    src = a.source.resolve()
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

assert entity in (assets / 'items.lua').read_text(encoding='utf-8')
assert entity in (assets / 'metadata.lua').read_text(encoding='utf-8')
for dest in changes:
    assert dest.is_file(), ('Expected existing file', dest)
print('PASS pose/compiled/skin/RM/mips/resource gates;', len(changes), 'existing files')
if not a.apply:
    raise SystemExit(0)
state = subprocess.run(['powershell','-NoProfile','-Command','Get-Process JA3,JA3Debug,ged -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Id'],capture_output=True,text=True)
assert not state.stdout.strip(), 'Close game/editor'
backup = src / 'refresh-backup'
assert not backup.exists(), 'Backup exists; inspect receipt before rerun'
before = {dest: dest.read_bytes() for dest in changes}
for dest,content in before.items():
    saved=backup/dest.relative_to(assets);saved.parent.mkdir(parents=True,exist_ok=True);saved.write_bytes(content)
try:
    for dest,content in changes.items():
        assert dest.read_bytes()==before[dest], 'Concurrent edit'
        dest.write_bytes(content)
    for dest,content in changes.items():
        assert dest.read_bytes()==content
except Exception:
    for dest,content in before.items():dest.write_bytes(content)
    raise
(src/'refresh-installation.json').write_text(json.dumps({'installed':True,'entity':entity,'runtime':'NOT_RUN','sha256':{str(dest.relative_to(assets)):hashlib.sha256(content).hexdigest() for dest,content in changes.items()}},indent=2))
print('Installed with backup and hash verification')
