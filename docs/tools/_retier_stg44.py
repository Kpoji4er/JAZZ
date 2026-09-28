"""Stage/apply StG44 T1-2 comment correction; catalog and loot already use T1-2.
--output DIR [--apply]; apply requires closed game/editor and saves originals.
"""
import argparse,json,re,subprocess
from pathlib import Path
from lupa import LuaRuntime
from _integrate_sr3m import ROOT,matching
p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--apply',action='store_true');a=p.parse_args();a.output.mkdir(parents=True,exist_ok=True)
before={};updates={}
def read(path):before[path]=path.read_bytes();return before[path].decode('utf-8-sig')
def put(path,s):
 raw=before[path];nl='\r\n' if b'\r\n' in raw else '\n'
 updates[path]=(b'\xef\xbb\xbf' if raw.startswith(b'\xef\xbb\xbf') else b'')+s.replace('\r\n','\n').replace('\n',nl).encode('utf-8')
path=ROOT/'InventoryItem/STG44.lua';s=read(path);assert 'comment = "Tier 2-1"' in s;put(path,s.replace('comment = "Tier 2-1"','comment = "Tier 1-2"'))
path=ROOT/'items.lua';s=read(path);hit=re.search(r"'Id',\s*\"STG44\"",s);start=s.rfind("PlaceObj('ModItemInventoryItemCompositeDef'",0,hit.start());end=matching(s,s.index('(',start));block=s[start:end];assert block.count('Tier 2-1')==1;put(path,s[:start]+block.replace('Tier 2-1','Tier 1-2')+s[end:])
report={}
lua=LuaRuntime()
for path,data in updates.items():
 if path.suffix=='.lua':lua.compile(data.decode('utf-8-sig'))
 stage=a.output/'staged'/path.relative_to(ROOT.parent);stage.parent.mkdir(parents=True,exist_ok=True);stage.write_bytes(data)
(a.output/'report.json').write_text(json.dumps({'files':[str(p.relative_to(ROOT.parent)) for p in updates],'pools':report,'entries':sum(report.values())},indent=2))
if a.apply:
 proc=subprocess.run(['powershell','-NoProfile','-Command','Get-Process JA3,JA3Debug -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Id'],capture_output=True,text=True)
 assert not proc.stdout.strip(),'Game/editor must be closed for generated-data transaction'
 for path,data in before.items():assert path.read_bytes()==data,'Concurrent edit'
 for path,data in updates.items():
  backup=a.output/'backup'/path.relative_to(ROOT.parent);backup.parent.mkdir(parents=True,exist_ok=True);assert not backup.exists();backup.write_bytes(before[path]);path.write_bytes(data)
print('APPLIED' if a.apply else 'STAGED',len(updates),'files; STG44 comment Tier 2-1 -> Tier 1-2; catalog and loot unchanged')
