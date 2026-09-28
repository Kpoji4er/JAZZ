"""Install VZ58 folding pair + one native entity, preserving other changes. --build DIR --base-build DIR [--apply]."""
import argparse,json,re,csv,io,subprocess,xml.etree.ElementTree as ET
from pathlib import Path
from lupa import LuaRuntime
from _integrate_vz58 import ROOT,ASSETS,SLOTS,component_block
from _integrate_sr3m import matching,append_root_item,add_metadata
from _apply_sr3m_slots import slot
p=argparse.ArgumentParser();p.add_argument('--build',type=Path,required=True);p.add_argument('--base-build',type=Path,required=True);p.add_argument('--apply',action='store_true');a=p.parse_args()
assert not subprocess.run(['powershell','-NoProfile','-Command','Get-Process JA3,JA3Debug -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Id'],capture_output=True,text=True).stdout.strip()
assert json.loads((a.build/'compiled-audit.json').read_text())['pass']
before={};updates={}
def read(path):before[path]=path.read_bytes();return before[path].decode('utf-8-sig')
def put(path,text):
 raw=before.get(path,b'');nl='\r\n' if b'\r\n' in raw else '\n';updates[path]=(b'\xef\xbb\xbf' if raw.startswith(b'\xef\xbb\xbf') else b'')+text.replace('\r\n','\n').replace('\n',nl).encode('utf-8')
items=read(ROOT/'items.lua');weapon=read(ROOT/'InventoryItem/VZ58.lua')
assert 'JAZZ_StockLightFolded' not in weapon,'Already installed'
# Change only the Stock slot, with identical nested records in both representations.
stock=next(x for x in SLOTS if x[0]=='Stock');replacement=slot('\t\t',*stock).strip().rstrip(',')
def replace_stock(text,start):
 pos=text.index("'SlotType', \"Stock\"",start);at=text.rfind("PlaceObj('WeaponComponentSlot'",0,pos);end=matching(text,text.index('(',at));return text[:at]+replacement+text[end:]
weapon=replace_stock(weapon,0);items=replace_stock(items,items.index("'Id', \"VZ58\""))
for cid,suffix in [('JAZZ_StockLightUnFolded','StockWire'),('JAZZ_StockLightFolded','StockWireFolded')]:
 start,end=component_block(items,cid);block=items[start:end];assert 'ApplyTo = "VZ58"' not in block
 visual=f'\n\tPlaceObj(\'WeaponComponentVisual\', {{ ApplyTo = "VZ58", Entity = "JAZZ_VZ58_{suffix}", Slot = "Stock", param_bindings = false }}),'
 block,n=re.subn(r'Visuals\s*=\s*\{',lambda m:m[0]+visual,block,count=1);assert n==1;items=items[:start]+block+items[end:]
put(ROOT/'items.lua',items);put(ROOT/'InventoryItem/VZ58.lua',weapon)
ent='JAZZ_VZ58_StockWireFolded';ai=read(ASSETS/'items.lua');am=read(ASSETS/'metadata.lua');assert ent not in ai
ai=append_root_item(ai,f'\tPlaceObj(\'ModItemEntity\', {{\n\t\t\'name\', "{ent}",\n\t\t\'ClassParents\', {{}},\n\t\t\'entity_name\', "{ent}",\n\t}}),');am=add_metadata(am,'entities',[f'"{ent}"']);am=add_metadata(am,'code',[f'"Entities/{ent}.lua"']);put(ASSETS/'items.lua',ai);put(ASSETS/'metadata.lua',am)
export=a.build.parent/'ExportedEntities';tree=ET.parse(export/(ent+'.ent'));tree.getroot().set('name',ent)
for lod in tree.findall('.//lod'):
 for src in list(lod.findall('src')):lod.remove(src)
updates[ASSETS/'Entities'/(ent+'.ent')]=ET.tostring(tree.getroot(),encoding='utf-8',xml_declaration=True)
put(ASSETS/'Entities'/(ent+'.lua'),f'EntityData["{ent}"] = {{ editor_artset = "Mods" }}\n')
for n in tree.findall('.//mesh'):updates[ASSETS/'Entities'/n.get('file')]=(export/n.get('file')).read_bytes()
for n in tree.findall('.//material'):
 # Identical stock UV and material: reuse installed named maps, without duplicate DDS.
 updates[ASSETS/'Entities'/n.get('file')]=(ASSETS/'Entities/Materials/JAZZ_VZ58_StockWire_Mesh.mtl').read_bytes()
path=ROOT/'docs/technical/weapons/data/weapons.csv';r=csv.DictReader(io.StringIO(read(path)));fields=r.fieldnames;rows=list(r)
for row in rows:
 if row['id']=='VZ58':row['component_option_count']=str(sum(len(v[1]) for v in SLOTS))
out=io.StringIO(newline='');w=csv.DictWriter(out,fieldnames=fields);w.writeheader();w.writerows(rows);put(path,out.getvalue())
lua=LuaRuntime()
for path,raw in updates.items():
 if path.suffix=='.lua':lua.compile(raw.decode('utf-8-sig'))
if a.apply:
 for path,raw in before.items():assert path.read_bytes()==raw,'Concurrent edit'
 for path,raw in updates.items():
  if path.exists():
   backup=a.build/'integration-backup'/path.relative_to(ROOT.parent);backup.parent.mkdir(parents=True,exist_ok=True);assert not backup.exists();backup.write_bytes(path.read_bytes())
  path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(raw)
 report=json.loads((a.base_build/'compiled-audit.json').read_text());fold=json.loads((a.build/'compiled-audit.json').read_text());report['entities'].append(fold);(a.base_build/'compiled-audit.json').write_text(json.dumps(report,indent=2))
print('APPLIED' if a.apply else 'STAGED',len(updates),'files')
