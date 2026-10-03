"""Refresh one existing Legion armor resource graph after QA; --item --root [--apply].
Keeps registrations, icons, loadouts and stats. Closed-game backup/rollback.
"""
import argparse,hashlib,json,subprocess
from pathlib import Path
from _install_soft_legion_armor import validate
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--item',required=True,choices=['Chainmail','TireBrigantine','TireArmor','LeatherArmor'])
p.add_argument('--root',required=True,type=Path);p.add_argument('--apply',action='store_true');a=p.parse_args()
root=a.root.resolve();repo=Path(__file__).resolve().parents[2];assets=repo.parent/'jazz_assets'
entity='JAZZ_'+a.item+'_Male'
assert json.loads((root/'compiled-audit.json').read_text())['pass']
assert json.loads((root/'poses/pose-check.json').read_text())['status']=='PASS_SKIN_STRUCTURE'
if a.item=='Chainmail':assert json.loads((root/'compiled-skin.json').read_text())['pass']
assert json.loads((root/'visual-review.json').read_text())['status']=='REVIEWED_FOR_GAME_TEST'
stage=validate(root/'build',entity,a.item)
writes={assets/'Entities'/f.relative_to(stage):f.read_bytes() for f in stage.rglob('*') if f.is_file() and f.suffix!='.lua'}
assert all(f.resolve().is_relative_to((assets/'Entities').resolve()) and f.name.startswith('JAZZ_'+a.item) for f in writes)
protected=[repo/'ArmorIcons'/(a.item+'.png'),repo/'InventoryItem'/('JazzArmor_'+a.item+'.lua'),assets/'items.lua',assets/'metadata.lua',assets/'Entities'/(entity+'.lua')]
sha=lambda x:hashlib.sha256(x).hexdigest()
report={'item':a.item,'entity':entity,'installed':False,'runtime':'NOT_RUN','files':len(writes),'protected':{str(f.relative_to(repo.parent)):sha(f.read_bytes()) for f in protected},'sha256':{str(f.relative_to(assets)):sha(data) for f,data in writes.items()}}
if a.apply:
 check=subprocess.run(['powershell','-NoProfile','-Command','Get-Process JA3,JA3Debug,ged -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Id'],capture_output=True,text=True)
 assert not check.stdout.strip(),'Game/editor must be closed'
 backup=root/'install-backup';assert not backup.exists(),'Already applied; choose fresh build'
 before={f:f.read_bytes() if f.exists() else None for f in writes}
 for f,data in before.items():
  if data is not None:
   dest=backup/f.relative_to(assets);dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(data)
 try:
  for f,data in writes.items():
   assert (f.read_bytes() if f.exists() else None)==before[f],'Concurrent edit'
   f.parent.mkdir(parents=True,exist_ok=True);f.write_bytes(data)
  assert all(f.read_bytes()==data for f,data in writes.items())
  assert all(sha((repo.parent/f).read_bytes())==h for f,h in report['protected'].items())
 except Exception:
  for f,data in before.items():
   if data is not None:f.write_bytes(data)
   elif f.exists() and f.read_bytes()==writes[f]:f.unlink()
  raise
 report['installed']=True
 (root/'installation.json').write_text(json.dumps(report,indent=2))
else:(root/'installation-plan.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
