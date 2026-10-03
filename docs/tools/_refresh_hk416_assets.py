"""Install compiled HK416 correction after initial registration; --build DIR.
Requires closed game, successful mesh audits and unchanged initial install hashes.
"""
import argparse,hashlib,json,subprocess
from pathlib import Path
from _integrate_hk416 import ROOT,ASSETS
p=argparse.ArgumentParser();p.add_argument('--build',type=Path,required=True);a=p.parse_args()
assert not subprocess.run(['powershell','-NoProfile','-Command','Get-Process JA3,JA3Debug -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Id'],capture_output=True,text=True).stdout.strip(),'Game/editor must be closed'
assert all(x['pass'] for x in json.loads((a.build/'compiled-audit.json').read_text()))
receipt=json.loads((a.build/'integration-receipt.json').read_text());assert receipt['applied']
prior={x['path']:x['sha256'] for x in receipt['files']}
refresh=a.build/'sharp-edge-refresh-receipt.json'
if refresh.exists():prior.update({x['path']:x['after'] for x in json.loads(refresh.read_text())['files']})
updates={ASSETS/'Entities'/x.relative_to(a.build/'mod-assets-stage/Entities'):x.read_bytes() for x in (a.build/'mod-assets-stage/Entities').rglob('*') if x.is_file()}
for x in (a.build/'previews').glob('HK416_*_icon.png'):updates[ROOT/'WeaponIcons'/x.name.replace('_icon','')]=x.read_bytes()
sha=lambda data:hashlib.sha256(data).hexdigest()
before={}
for target,data in updates.items():
 rel=target.relative_to(ROOT.parent);raw=target.read_bytes();assert sha(raw)==prior[str(rel)],f'Concurrent edit: {rel}'
 before[target]=raw
index=1
while (a.build/f'asset-refresh-backup-{index}').exists():index+=1
backup=a.build/f'asset-refresh-backup-{index}'
for target,raw in before.items():
 dest=backup/target.relative_to(ROOT.parent);dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(raw)
for target,data in updates.items():
 assert target.read_bytes()==before[target]
 target.write_bytes(data)
report={'backup':backup.name,'files':[{'path':str(target.relative_to(ROOT.parent)),'before':sha(before[target]),'after':sha(data)} for target,data in updates.items()],'runtime_verified':False}
(backup/'receipt.json').write_text(json.dumps(report,indent=2))
(a.build/'sharp-edge-refresh-receipt.json').write_text(json.dumps(report,indent=2));print('REFRESHED',len(updates),'files; game not launched')
