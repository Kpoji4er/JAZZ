"""Validate staged second acceptance transaction against installed source.

--build DIR. Checks semantic weapon preservation, editor folder ancestry,
entity registration, mesh audits and icon bounds/colour before installation.
"""
import argparse,json,re
from pathlib import Path
import numpy as np
from PIL import Image
from lupa import LuaRuntime
from _integrate_m14_family import matching,find_item_block
from _validate_items_quick import check
p=argparse.ArgumentParser();p.add_argument('--build',type=Path,required=True);a=p.parse_args();root=Path(__file__).resolve().parents[2];stage=a.build/'stage';s=(stage/'jazz/items.lua').read_text(encoding='utf-8-sig')
original=a.build/'backup/jazz/items.lua'
old=(original if original.exists() else root/'items.lua').read_text(encoding='utf-8-sig')
def audit_identities(text):
 # Same indentation-sensitive record boundaries as check-generated-sync.ps1.
 pattern=r"(?ms)^(?P<indent>[ \t]*)PlaceObj\('(?P<class>ModItem[^']*)',\s*\{\s*\n(?P<body>.*?)^(?P=indent)\}(?:\)|,\s*\{)"
 rows=[]
 for m in re.finditer(pattern,text):
  keys=[]
  for key in ('Id','id','name','entity_name','CodeFileName'):
   hit=re.search(r"(?m)^[ \t]*'?"+key+r"'?(?:,|\s*=)\s*\"([^\"]+)\"",m['body']);keys.append(hit[1] if hit else None)
  rows.append((m['class'],*keys))
 return sorted(rows,key=str)
assert audit_identities(old)==audit_identities(s),'Auditor must recognize every original ModItem after relocation'
for rel in ('jazz/items.lua','jazz_assets/items.lua','jazz_assets/metadata.lua'):assert not check(stage/rel),check(stage/rel)
for name in ('VZ58','VektorR4','M14SAW','M21','M4A1','M16A4','MK14EBR'):
 start,end=find_item_block(old,name);before=old[start:end];start,end=find_item_block(s,name);after=s[start:end]
 if name=='MK14EBR':before=before.replace('"JAZZ_GrenadeLauncher_M14",','')
 assert [line.lstrip() for line in after.splitlines()]==[line.lstrip() for line in before.splitlines()],('Unexpected weapon change',name)
folders=[]
for m in re.finditer(r"PlaceObj\('ModItemFolder'",s):
 end=matching(s,s.index('(',m.start()));folders.append((m.start(),end))
def ancestry(name):
 start,end=find_item_block(s,name);return [lo for lo,hi in folders if lo<start and end<hi]
assert ancestry('VZ58')==ancestry('VektorR4')==ancestry('AK47') and ancestry('AK47')
lua=LuaRuntime();lua.execute('function T(id,text) return text end; function UndefineClass() end; DefineClass={}; function PlaceObj(c,p) for i=1,#p,2 do if type(p[i])=="string" then p[p[i]]=p[i+1] end end return p end')
start,end=find_item_block(s,'MK14EBR');item=lua.execute('return '+s[start:end]);lua.execute((stage/'jazz/InventoryItem/MK14EBR.lua').read_text(encoding='utf-8-sig'));comp=lua.globals().DefineClass.MK14EBR
def slots(w):return {slot.SlotType:[v for _,v in slot.AvailableComponents.items()] for _,slot in w.ComponentSlots.items()}
assert slots(item)==slots(comp) and 'JAZZ_GrenadeLauncher_M14' not in slots(item)['Under']
name='JAZZ_M14_OpticsMount'
assert (stage/'jazz_assets/Entities'/f'{name}.lua').exists()
meta=(stage/'jazz_assets/metadata.lua').read_text(encoding='utf-8-sig');assert '"Entities/'+name+'.lua"' in meta and '"'+name+'"' in meta
entityitems=(stage/'jazz_assets/items.lua').read_text(encoding='utf-8-sig');assert entityitems.count("'entity_name', \""+name+'"')==1
reports=json.loads((a.build/'compiled-report.json').read_text());assert len(reports)==4 and all(r['pass'] for r in reports)
icons={}
for name in ('AK103','M14','M21','VZ58','JAZZ_M14_MkIII'):
 im=Image.open(a.build/'icons'/(name+'.png'));assert im.size==(324,165) and im.mode=='RGBA'
 data=np.array(im);bbox=im.getchannel('A').getbbox();assert bbox and bbox[0]>0 and bbox[1]>0 and bbox[2]<324 and bbox[3]<165,(name,bbox)
 rgb=data[:,:,:3].astype(int);colour=(rgb.max(2)-rgb.min(2)>15)&(data[:,:,3]>200)
 if name=='JAZZ_M14_MkIII':assert colour.sum()>150,colour.sum()
 icons[name]={'alpha_bbox':bbox,'coloured_pixels':int(colour.sum())}
report={'editor_folder':'same as AK47','weapon_properties':'unchanged except EBR launcher list','EBR_items_companion':'equal','new_entity_registration':'PASS','compiled_meshes':4,'icons':icons,'runtime_verified':False}
(a.build/'validation.json').write_text(json.dumps(report,indent=2));print('PASS:',json.dumps(report))
