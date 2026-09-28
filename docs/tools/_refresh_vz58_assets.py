"""Refresh only installed VZ58 binary resources from the checked stage; --build DIR [--apply]."""
import argparse,subprocess,shutil,json,xml.etree.ElementTree as ET
from pathlib import Path
from _integrate_vz58 import ROOT,ASSETS
p=argparse.ArgumentParser();p.add_argument('--build',type=Path,required=True);p.add_argument('--apply',action='store_true');a=p.parse_args()
assert json.loads((a.build/'compiled-audit.json').read_text())['pass']
assert not subprocess.run(['powershell','-NoProfile','-Command','Get-Process JA3,JA3Debug -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Id'],capture_output=True,text=True).stdout.strip()
stage=a.build/'mod-assets-stage/Entities';changed=[];needed=set()
for ent in stage.glob('JAZZ_VZ58*.ent'):
 needed.update([ent.relative_to(stage),ent.with_suffix('.lua').relative_to(stage)])
 for node in ET.parse(ent).findall('.//mesh')+ET.parse(ent).findall('.//material'):
  rel=Path(node.get('file'));needed.add(rel)
  if node.tag=='material':
   for tag in ET.parse(stage/rel).getroot().iter():
    name=tag.get('Name')
    if name:needed.update([Path('Textures')/name,Path('Textures/Fallbacks')/name])
for rel in sorted(needed):
 src=stage/rel
 if not src.is_file():continue
 rel=src.relative_to(stage);assert src.name.startswith('JAZZ_VZ58')
 target=ASSETS/'Entities'/rel
 if target.is_file() and src.read_bytes()==target.read_bytes():continue
 changed.append(str(rel))
 if a.apply:
  backup=a.build/'refresh-backup'/rel;backup.parent.mkdir(parents=True,exist_ok=True)
  if target.exists() and not backup.exists():shutil.copy2(target,backup)
  target.parent.mkdir(parents=True,exist_ok=True)
  shutil.copy2(src,target)
# Retire only this task's unreferenced texture names, after installing the complete graph.
for folder in ['Textures','Textures/Fallbacks']:
 for target in (ASSETS/'Entities'/folder).glob('JAZZ_VZ58_*.dds'):
  rel=target.relative_to(ASSETS/'Entities')
  if rel in needed:continue
  assert target.resolve().is_relative_to((ASSETS/'Entities').resolve())
  if a.apply:
   backup=a.build/'refresh-backup'/rel;backup.parent.mkdir(parents=True,exist_ok=True)
   if not backup.exists():shutil.copy2(target,backup)
   target.unlink()
print('REFRESHED' if a.apply else 'STAGED',changed)
