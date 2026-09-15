"""Apply a staged revision of an existing AK entity family; preserve backups.

No new entities, ModItems or resource IDs are registered by this tool.
"""
import argparse,hashlib,xml.etree.ElementTree as ET
from pathlib import Path
from _integrate_sr3m import ROOT,ASSETS

p=argparse.ArgumentParser()
p.add_argument('--build',type=Path,required=True)
p.add_argument('--weapon',choices=['AK74M','AK105'],required=True)
a=p.parse_args()
stage=a.build/a.weapon/'mod-assets-stage/Entities'
files={}
for src in stage.rglob('*'):
    if not src.is_file():continue
    dst=ASSETS/'Entities'/src.relative_to(stage)
    assert dst.exists(),f'Unexpected new resource: {dst}'
    files[dst]=src.read_bytes()
for src in stage.glob('*.ent'):
    tree=ET.parse(src)
    for node in tree.findall('.//mesh')+tree.findall('.//material'):
        assert (stage/node.get('file')).is_file(),node.attrib
for src in (stage/'Materials').glob('*.mtl'):
    for node in ET.parse(src).getroot().iter():
        if node.get('Name'):
            for folder in ('Textures','Textures/Fallbacks'):
                assert (stage/folder/node.get('Name')).is_file(),node.attrib
files[ROOT/f'WeaponIcons/{a.weapon}.png']=(a.build/f'{a.weapon}_icon.png').read_bytes()
files[ROOT/f'WeaponComponents/Magazine/{a.weapon}_Native30.png']=(a.build/f'{a.weapon}_Magazine_icon.png').read_bytes()
before={p:p.read_bytes() for p in files}
for path,raw in before.items():
    if raw==files[path]:continue
    package=ASSETS if path.is_relative_to(ASSETS) else ROOT
    dest=a.build/'visual-revision-backup'/package.name/path.relative_to(package)
    dest=dest.with_name(dest.name+'.'+hashlib.sha256(raw).hexdigest()[:12])
    dest.parent.mkdir(parents=True,exist_ok=True)
    if not dest.exists():dest.write_bytes(raw)
for path,raw in files.items():
    assert path.read_bytes()==before[path],f'Concurrent edit: {path}'
    if raw!=before[path]:path.write_bytes(raw)
print(f'{a.weapon}: updated {sum(files[p]!=before[p] for p in files)} existing resources; reload/visual QA pending.')
