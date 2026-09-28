"""Verify the reviewed feedback manifest; --apply installs only with JA3 closed.
--build DIR. Dry run is default. Hash checks, immutable backup, rollback on error.
Does not launch/close the game, regenerate packages, or install armor experiments.
"""
import argparse, hashlib, json, os, subprocess
from pathlib import Path
from datetime import datetime, timezone
from lupa import LuaRuntime

p=argparse.ArgumentParser()
p.add_argument('--build',type=Path,required=True)
p.add_argument('--apply',action='store_true')
a=p.parse_args();suite=Path(__file__).resolve().parents[3]
manifest=json.loads((a.build/'data-manifest.json').read_text())
lua=LuaRuntime(unpack_returned_tuples=True)
check=lua.eval('function(s) local f,e=load(s); return f~=nil,e end')
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest() if path.exists() else None
def paths(rel):
 assert rel.startswith(('jazz/','jazz_assets/')),rel
 dest=(suite/rel).resolve();assert dest.is_relative_to(suite.resolve()),rel
 staged=(a.build/'stage'/rel).resolve();assert staged.is_relative_to((a.build/'stage').resolve()),rel
 return staged,dest
for rel,h in manifest.items():
 staged,dest=paths(rel)
 assert digest(staged)==h['after'],('staged content changed',rel)
 assert digest(dest)==h['before'],('installed content changed; restage first',rel)
 if rel.endswith('.lua'):
  ok,error=check(staged.read_text(encoding='utf-8-sig'));assert ok,(rel,error)
assert json.loads((a.build/'graph-check.json').read_text())['FAL_rail'].startswith('PASS')
for r in json.loads((a.build/'compiled-report.json').read_text()):assert r['pass'],r
report={'status':'VERIFIED_STAGED','files':len(manifest),'installed':False,'runtime':'NOT_RUN'}
if a.apply:
 result=subprocess.run(['powershell','-NoProfile','-Command',"@(Get-Process -Name JA3,JA3Debug,Ged -ErrorAction SilentlyContinue).Count"],capture_output=True,text=True,check=True)
 assert result.stdout.strip()=='0','Close JA3 and its editor before applying; no files written'
 backup=a.build/('backup-'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ'))
 backup.mkdir(exist_ok=False)
 for rel in manifest:
  _,dest=paths(rel)
  if dest.exists():
   saved=backup/rel;saved.parent.mkdir(parents=True,exist_ok=True);saved.write_bytes(dest.read_bytes())
 (backup/'manifest.json').write_text(json.dumps(manifest,indent=2))
 written=[]
 try:
  for rel,h in manifest.items():
   staged,dest=paths(rel);assert digest(dest)==h['before'],('concurrent change',rel)
   dest.parent.mkdir(parents=True,exist_ok=True)
   temp=dest.with_name(dest.name+'.feedback029.tmp');assert not temp.exists(),temp
   temp.write_bytes(staged.read_bytes());os.replace(temp,dest);written.append(rel)
   assert digest(dest)==h['after'],rel
 except Exception:
  for rel in reversed(written):
   _,dest=paths(rel);saved=backup/rel
   if saved.exists():dest.write_bytes(saved.read_bytes())
   else:dest.unlink()
  raise
 report.update(status='INSTALLED_PENDING_RUNTIME',installed=True,backup=str(backup))
(a.build/'transaction-status.json').write_text(json.dumps(report,indent=2));print(json.dumps(report))
