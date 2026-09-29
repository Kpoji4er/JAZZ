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
p.add_argument('--ak103-magazines',action='store_true',help='Preserve the scoped AK103 availability and donor drum transaction')
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
if a.ak103_magazines:
 start=old.index("'Id', \"AK103\"")
 end=old.index("PlaceObj('ModItem",start)
 segment=old[start:end]
 segment,count=re.subn(r'(?m)^[ \t]*"JAZZ_MagQuick_AK",\n','',segment)
 assert count==1
 items=old[:start]+segment+old[end:]
 ident=items.index('id = "JAZZ_MagDrum_30_75"')
 start=items.rfind("PlaceObj('ModItemWeaponComponent'",0,ident)
 segment=items[start:ident]
 donor=re.search(r"PlaceObj\('WeaponComponentVisual', \{\s*ApplyTo = \"AKM\",.*?\}\),",segment,re.S)
 assert donor and 'WeaponAttA_MagazineRPK74_03' in donor[0]
 segment=segment[:donor.end()]+'\n'+donor[0].replace('"AKM"','"AK103"')+segment[donor.end():]
 items=items[:start]+segment+items[ident:]
 assert receipt['result']['quick_removed']==1 and receipt['result']['drum_entity']=='WeaponAttA_MagazineRPK74_03'
else:
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
  if a.ak103_magazines and name=='InventoryItem/AK103.lua':
   data=(a.baseline/name).read_bytes()
   data,count=re.subn(rb'(?m)^[ \t]*"JAZZ_MagQuick_AK",\r?\n',b'',data)
   assert count==1 and b'JAZZ_MagQuick_AK' not in (a.repo/name).read_bytes()
   updates[name]=data
  elif (a.repo/name).read_bytes()!=(a.baseline/name).read_bytes():updates[name]=(a.baseline/name).read_bytes()
a.archive.mkdir(parents=True)
for name,data in updates.items():
 archive=a.archive/name;archive.parent.mkdir(parents=True,exist_ok=True)
 shutil.copy2(a.repo/name,archive)
 (a.repo/name).write_bytes(data)
(a.archive/'normalization.json').write_text(json.dumps({'editor_receipt':receipt,'preserved_generated_fields':['version','saved','code_hash','last_changes'],'files':list(updates),'roundtrip':'pending reload from disk'},indent=2),encoding='utf-8')
print(json.dumps({'normalized_files':len(updates),'callbacks':2}))
