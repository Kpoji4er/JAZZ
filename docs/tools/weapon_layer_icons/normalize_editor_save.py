"""Retain the verified two-callback editor delta without unrelated regeneration.

Requires a successful official save receipt and immutable pre-save baseline.
Archives every replaced post-save file before preserving original formatting,
companion sources, and load order. Generated revision/time/hash are copied from
the editor output, never calculated or invented here. Reload validation follows.
"""
import argparse,hashlib,json,re,shutil
from pathlib import Path

p=argparse.ArgumentParser(__doc__)
p.add_argument('--repo',type=Path,required=True)
p.add_argument('--baseline',type=Path,required=True)
p.add_argument('--archive',type=Path,required=True)
a=p.parse_args()
receipt=json.loads((a.baseline/'editor-result.json').read_text(encoding='utf-8'))
assert receipt['ok'] and receipt['result']['status']=='PASS'
assert not a.archive.exists(),'Use an immutable new archive'
manifest=json.loads((a.baseline/'manifest.json').read_text(encoding='utf-8'))
for name,digest in manifest.items():
 assert hashlib.sha256((a.baseline/name).read_bytes()).hexdigest()==digest,name
old=(a.baseline/'items.lua').read_text(encoding='utf-8-sig')
current=(a.repo/'items.lua').read_text(encoding='utf-8-sig')
assert current.count('JazzWeaponIcon_BindItemImage(itemIcon, item)')==2
anchor='itemIcon:SetImage(item.Icon)'
assert old.count(anchor)==2
items=re.sub(r'([ \t]*)itemIcon:SetImage\(item.Icon\)',lambda m:m[0]+'\n'+m[1]+'if JazzWeaponIcon_BindItemImage then\n'+m[1]+'\tJazzWeaponIcon_BindItemImage(itemIcon, item)\n'+m[1]+'end',old)
metadata=(a.baseline/'metadata.lua').read_text(encoding='utf-8-sig')
saved=(a.repo/'metadata.lua').read_text(encoding='utf-8-sig')
for key in ('version','saved','code_hash','last_changes'):
 pattern=r"(?m)^\s*'"+key+r"',[^\n]*$"
 replacement=re.findall(pattern,saved)
 assert len(replacement)==1,key
 metadata,count=re.subn(pattern,lambda m:replacement[0],metadata)
 assert count==1,key
updates={'items.lua':items.encode('utf-8'),'metadata.lua':metadata.encode('utf-8')}
for name in updates:
 if b'\r\n' in (a.baseline/name).read_bytes():updates[name]=updates[name].replace(b'\n',b'\r\n')
for name in manifest:
 if name.startswith(('InventoryItem/','CharacterEffect/','Entities/','UnitData/')):
  if (a.repo/name).read_bytes()!=(a.baseline/name).read_bytes():updates[name]=(a.baseline/name).read_bytes()
a.archive.mkdir(parents=True)
for name,data in updates.items():
 archive=a.archive/name;archive.parent.mkdir(parents=True,exist_ok=True)
 shutil.copy2(a.repo/name,archive)
 (a.repo/name).write_bytes(data)
(a.archive/'normalization.json').write_text(json.dumps({'editor_receipt':receipt,'preserved_generated_fields':['version','saved','code_hash','last_changes'],'files':list(updates),'roundtrip':'pending reload from disk'},indent=2),encoding='utf-8')
print(json.dumps({'normalized_files':len(updates),'callbacks':2}))
