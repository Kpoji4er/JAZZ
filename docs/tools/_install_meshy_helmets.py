"""Install the reviewed 2026-10-03 6B7 and SSh60 fit candidates, with backups.
Run from jazz; requires closed JA3 and the documented Sources build directories.
"""
from pathlib import Path
import re,json,shutil,hashlib,subprocess,xml.etree.ElementTree as ET
root=Path(__file__).resolve().parents[2];assets=root.parent/'jazz_assets'
check=subprocess.run(['powershell','-NoProfile','-Command','Get-Process JA3,JA3Debug,ged -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Id'],capture_output=True,text=True)
assert not check.stdout.strip(),'Close game/editor first'
src=assets/'Sources/Character/JazzHat_6B7/meshy-20261003';stage=src/'build/mod-assets-stage/Entities'
mtl=stage/'Materials/JazzHat_6B7_mesh.mtl';text=mtl.read_text()
for suffix,n in [('Norm',1),('Base',2),('RM',3)]:
 old=f'JazzHat_6B7_{n}_{suffix}.dds';new=f'JazzHat_6B7_{suffix}.dds'
 for folder in ['Textures','Textures/Fallbacks']:
  if (stage/folder/old).exists():(stage/folder/old).rename(stage/folder/new)
 text=text.replace(old,new)
mtl.write_text(text)
(stage/'JazzHat_6B7.lua').write_text('EntityData["JazzHat_6B7"] = {\n\teditor_artset = "Mods",\n\tentity = { class_parent = "CharacterHat" },\n}\n')
fit=assets/'Sources/Character/JazzHat_SSh68/ssh60-fit-20261003';export=fit.parent/'ExportedEntities';fitstage=fit/'stage/Entities';fitstage.mkdir(parents=True,exist_ok=True)
tree=ET.parse(export/'JazzHat_SSh68.ent');tree.getroot().set('name','JazzHat_SSh68')
for lod in tree.findall('.//lod'):
 for node in list(lod.findall('src')):lod.remove(node)
tree.write(fitstage/'JazzHat_SSh68.ent',encoding='utf-8',xml_declaration=True)
(fitstage/'Meshes').mkdir(exist_ok=True);shutil.copy2(export/'Meshes/JazzHat_SSh68_mesh.m.hgm',fitstage/'Meshes/JazzHat_SSh68_mesh.m.hgm')
changes={}
for staged in [stage,fitstage]:
 for f in staged.rglob('*'):
  if f.is_file():changes[assets/'Entities'/f.relative_to(staged)]=f.read_bytes()
items=assets/'items.lua';data=items.read_bytes();anchor=b"PlaceObj('ModItemEntity', {\n    'name', \"JazzHat_SSh68\",\n    'class_parent', \"CharacterHat\",\n    'ClassParents', { \"CharacterHat\" },\n    'entity_name', \"JazzHat_SSh68\",\n}),"
assert data.count(anchor)==1 and b'"JazzHat_6B7"' not in data
changes[items]=data.replace(anchor,anchor+b'\n'+anchor.replace(b'JazzHat_SSh68',b'JazzHat_6B7'))
meta=assets/'metadata.lua';data=meta.read_bytes()
for old,new in [(b'"JazzHat_SSh68",',b'"JazzHat_6B7",'),(b'"Entities/JazzHat_SSh68.lua",',b'"Entities/JazzHat_6B7.lua",')]:
 assert data.count(old)==1 and new not in data;data=data.replace(old,old+b'\r\n\t\t'+new)
changes[meta]=data
code=root/'Code/System_LegionArmorVisuals.lua';data=code.read_bytes()
pat=rb'(\tJazzArmor_6b7Helm = \{\r?\n).*?(\t\},)'
data,n=re.subn(pat,lambda m:m[1]+b'\t\tMale = "JazzHat_6B7", hide_hair = true,\r\n'+m[2],data,flags=re.S);assert n==1
# Remove obsolete bbox comment for the previous Soviet shell.
data=data.replace(b'\t\t-- The imported shell starts 4.24 cm above its local origin.\n\t\t-- Seat it 4 cm lower relative to the appearance\'s existing Hat offset.\n',b'\t\t-- Head-local SSh60 mesh is fitted with this 4 cm downward offset.\n')
changes[code]=data
backup=src/'installation-backup';assert not (src/'installation.json').exists(),'Already installed; inspect receipt instead of replaying'
receipt=[]
for dest,data in changes.items():
 rel=dest.relative_to(root.parent);previous=None
 if dest.exists():
  previous=hashlib.sha256(dest.read_bytes()).hexdigest();b=backup/rel;b.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(dest,b)
 receipt.append({'path':str(rel),'old_sha256':previous,'sha256':hashlib.sha256(data).hexdigest()})
for dest,data in changes.items():dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(data)
for row in receipt:assert hashlib.sha256((root.parent/row['path']).read_bytes()).hexdigest()==row['sha256']
(src/'installation.json').write_text(json.dumps({'files':receipt,'runtime':'NOT_RUN','editor_roundtrip':'NOT_RUN'},indent=2))
print('Installed and verified',len(changes),'files; backups:',backup)
