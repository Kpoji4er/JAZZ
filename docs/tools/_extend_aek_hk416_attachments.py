"""Stage/apply AEK Scope and HK416 Under/Side in both serialized item layers.
--build DIR [--apply]. Existing components; closed-game, backup and SHA guards.
"""
import argparse,hashlib,json,re,subprocess
from pathlib import Path
from _integrate_sr3m import ROOT,matching
from _integrate_vz58 import component_block
from _apply_sr3m_slots import slot,SCOPE,SIDE
p=argparse.ArgumentParser();p.add_argument('--build',type=Path,required=True);p.add_argument('--apply',action='store_true');a=p.parse_args()
a.build.mkdir(parents=True,exist_ok=True);manifest=a.build/'attachments-install.json'
sha=lambda data:hashlib.sha256(data).hexdigest()
if a.apply:
 r=json.loads(manifest.read_text());assert not r['applied']
 assert not subprocess.run(['powershell','-NoProfile','-Command','Get-Process JA3,JA3Debug -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Id'],capture_output=True,text=True).stdout.strip(),'Close game/editor before apply'
 for rel,h in r['files'].items():assert sha((ROOT/rel).read_bytes())==h['before'] and sha((a.build/'mod-data-stage/jazz'/rel).read_bytes())==h['after'],rel
 for rel in r['files']:
  dst=a.build/'backup'/rel;assert not dst.exists();dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes((ROOT/rel).read_bytes())
 try:
  for rel,h in r['files'].items():(ROOT/rel).write_bytes((a.build/'mod-data-stage/jazz'/rel).read_bytes());assert sha((ROOT/rel).read_bytes())==h['after']
 except Exception:
  for rel in r['files']:(ROOT/rel).write_bytes((a.build/'backup'/rel).read_bytes())
  raise
 r['applied']=True;manifest.write_text(json.dumps(r,indent=2));print('APPLIED',len(r['files']),'files');raise SystemExit
items=(ROOT/'items.lua').read_text(encoding='utf-8-sig');updates={}
def append_slots(block,extra):
 hit=re.search(r"(?:ComponentSlots\s*=|'ComponentSlots',)\s*\{",block);assert hit
 end=matching(block,block.index('{',hit.start()),'{','}')
 return block[:end-1]+extra+block[end-1:]
for name,extra in [('AEK971',slot('\t\t','Scope',SCOPE,can_be_empty=True)),('HK416',slot('\t\t','Under',['JAZZ_GrenadeLauncher','JAZZ_VerticalGrip','JAZZ_TacGrip'],can_be_empty=True)+slot('\t\t','Side',SIDE,can_be_empty=True))]:
 source=(ROOT/f'InventoryItem/{name}.lua').read_text(encoding='utf-8-sig');assert "'SlotType', \""+('Scope' if name=='AEK971' else 'Under')+'"' not in source
 updates[f'InventoryItem/{name}.lua']=append_slots(source,extra)
 hit=re.search(r"PlaceObj\('ModItemInventoryItemCompositeDef',\s*\{\s*'Id',\s*\""+name+r'"',items);assert hit
 end=matching(items,items.index('(',hit.start()));items=items[:hit.start()]+append_slots(items[hit.start():end],extra)+items[end:]
# M203 has no default visual. Use the same established entity as M4A1.
for ident,entity in [('JAZZ_GrenadeLauncher','WeaponAttA_GrenadeLauncherM14'),('JAZZ_VerticalGrip','WeaponAttA_VerticalGripCAR15')]:
 lo,hi=component_block(items,ident);block=items[lo:hi];assert 'ApplyTo = "HK416"' not in block
 visual=f'PlaceObj(\'WeaponComponentVisual\', {{ApplyTo = "HK416", Entity = "{entity}", Slot = "Under", param_bindings = false}}),'
 block,n=re.subn(r'Visuals\s*=\s*\{',lambda m:m[0]+'\n'+visual,block,count=1);assert n==1
 items=items[:lo]+block+items[hi:]
updates['items.lua']=items;records={}
for rel,text in updates.items():
 old=(ROOT/rel).read_bytes();newline='\r\n' if b'\r\n' in old else '\n'
 raw=(b'\xef\xbb\xbf' if old.startswith(b'\xef\xbb\xbf') else b'')+text.replace('\r\n','\n').replace('\n',newline).encode('utf-8')
 dest=a.build/'mod-data-stage/jazz'/rel;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(raw)
 records[rel]={'before':sha(old),'after':sha(raw)}
manifest.write_text(json.dumps({'files':records,'applied':False},indent=2));print('STAGED',len(records),'files')
