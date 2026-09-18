"""Validate and replace existing nine HAV resource graphs; no metadata edits."""
import argparse,json,hashlib,subprocess
from pathlib import Path
from _install_soft_legion_armor import validate,ASSETS
p=argparse.ArgumentParser();p.add_argument('--build-root',type=Path,required=True);p.add_argument('--apply',action='store_true');p.add_argument('--live',action='store_true',help='Explicitly authorized replacement while game is running; reload is separate');a=p.parse_args()
writes={};hashes={}
for family in ['Twaron','Guardian','Zylon']:
 for variant in ['Light','Medium','Full']:
  item=family+variant;folder=a.build_root/item;entity='JAZZ_'+item+'_Male'
  fit=json.loads((folder/'source/fit.json').read_text());pose=json.loads((folder/'poses/pose-check.json').read_text())
  assert fit['rear_inner_gap_after_m']['min']>-.003 and fit['rear_inner_gap_after_m']['p95']<.035
  assert pose['status']=='PASS_SKIN_STRUCTURE'
  manifest=json.loads((folder/'source/model.json').read_text());hashes.setdefault(variant,set()).add(manifest['geometry_sha256'])
  stage=validate(folder/'build',entity,item)
  for src in stage.rglob('*'):
   if not src.is_file() or src.suffix=='.lua':continue
   target=ASSETS/'Entities'/src.relative_to(stage)
   assert target.is_file() and src.name.startswith('JAZZ_'+item),target
   writes[target]=src.read_bytes()
assert all(len(v)==1 for v in hashes.values()),'Material families must share fitted geometry'
print('PASS nine fitted resource graphs, skin and shared geometry')
if not a.apply:raise SystemExit(0)
process=subprocess.run(['powershell','-NoProfile','-Command','Get-Process JA3,JA3Debug,ged -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Id'],capture_output=True,text=True)
assert a.live or not process.stdout.strip(),'Game/editor open: resource installation postponed; explicit live authorization requires --live'
backup=a.build_root/'fit-install-backup';assert not backup.exists()
before={p:p.read_bytes() for p in writes}
for path,data in before.items():
 dest=backup/path.relative_to(ASSETS);dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(data)
try:
 for path,data in writes.items():
  assert path.read_bytes()==before[path],'Concurrent resource edit'
  path.write_bytes(data)
 for path,data in writes.items():assert path.read_bytes()==data
except Exception:
 for path,data in before.items():path.write_bytes(data)
 raise
(a.build_root/'fit-installation.json').write_text(json.dumps({'installed':True,'runtime':'NOT_RUN','sha256':{str(p.relative_to(ASSETS)):hashlib.sha256(v).hexdigest() for p,v in writes.items()}},indent=2))
print('INSTALLED',len(writes),'resources; existing registration and unit IDs preserved')
