"""Stage/apply HK416 and six compiled assets; --build DIR [--apply]. Closed game only.
Backups and hash guards protect existing files. Localize with canonical scoped exporter.
"""
import argparse,csv,io,json,re,hashlib,subprocess
from pathlib import Path
from lupa import LuaRuntime
from _integrate_sr3m import ROOT,ASSETS,matching,append_root_item,add_metadata
from _integrate_vz58 import component_block
from _apply_sr3m_slots import slot
VALUES={'comment':'Tier 3-1','Reliability':90,'Cost':18000,'RestockWeight':30,'MaxStock':1,'Tier':4,'Entity':'JAZZ_HK416_Standard','Icon':'Mod/e6L4ECj/WeaponIcons/HK416_Standard.png','Damage':23,'WeaponRange':46,'AimAccuracy':12,'Recoil':17,'MagazineSize':30,'CyclicRPM':850,'AutoShots':9,'BurstShots':4,'WeaponMass':35,'WeaponResource':8000,'BaseJamChance':-40}
TEXTS=[('890000000033101','HK416','HK416'),('890000000033103','Современный карабин под патрон 5,56×45 мм. Сменные стволы, приклады и прицелы; магазин STANAG на 30 патронов.','A modern 5.56x45 mm carbine with interchangeable barrels, stocks and optics. Uses a 30-round STANAG magazine.'),('890000000033104','Приклад Magpul CTR','Magpul CTR stock')]
SLOTS=[('Barrel',['JAZZ_HK416_BarrelNormal','JAZZ_HK416_BarrelShort','JAZZ_HK416_BarrelLong'],'JAZZ_HK416_BarrelNormal'),('Stock',['JAZZ_HK416_Stock','JAZZ_HK416_StockCTR'],'JAZZ_HK416_Stock'),('Magazine',['JAZZ_MagNormal'],'JAZZ_MagNormal'),('Scope',['JAZZ_Reflex_Closed','JAZZ_Reflex_Eotech','JAZZ_Reflex_M68','JAZZ_CombatScope_2x','JAZZ_CombatScope_ACOG'],None)]
def main():
 p=argparse.ArgumentParser();p.add_argument('--build',type=Path,required=True);p.add_argument('--apply',action='store_true');a=p.parse_args()
 before={};updates={}
 def read(path):before[path]=path.read_bytes();return before[path].decode('utf-8-sig')
 def put(path,s):
  raw=before.get(path,b'');nl='\r\n' if b'\r\n' in raw else '\n';updates[path]=(b'\xef\xbb\xbf' if raw.startswith(b'\xef\xbb\xbf') else b'')+s.replace('\r\n','\n').replace('\n',nl).encode('utf-8')
 items=read(ROOT/'items.lua');meta=read(ROOT/'metadata.lua');assert not (ROOT/'InventoryItem/HK416.lua').exists(),'Already installed'
 s=(ROOT/'InventoryItem/M4A1.lua').read_text(encoding='utf-8-sig').replace('M4A1','HK416')
 for field,value in VALUES.items():
  line='\t'+field+' = '+json.dumps(value,ensure_ascii=False)+','
  s,n=re.subn(r'^\t'+field+r' = .*$',lambda _:line,s,flags=re.M)
  if not n:s=s.replace('\tcomment =',line+'\n\tcomment =',1)
 for field,entry in [('DisplayName',TEXTS[0]),('DisplayNamePlural',TEXTS[0]),('Description',TEXTS[1])]:
  s=re.sub(r'^\t'+field+r' = .*$',lambda _:f'\t{field} = T({entry[0]}, {json.dumps(entry[1],ensure_ascii=False)}),',s,flags=re.M)
 s=re.sub(r'^\tAdditionalHint = .*\n','',s,flags=re.M)
 start=s.index('\tComponentSlots = {');end=matching(s,s.index('{',start),'{','}')
 body=''.join(slot('\t\t',name,options,default,can_be_empty=default is None,modifiable=name!='Magazine') for name,options,default in SLOTS)
 s=s[:start]+'\tComponentSlots = {\n'+body+'\t}'+s[end:];put(ROOT/'InventoryItem/HK416.lua',s)
 props=s[s.index('\t',s.index('__generated_by_class')):s.rfind('}')];props=re.sub(r'^\t__generated_by_class = .*\n','',props,flags=re.M);props=re.sub(r'^\t([A-Za-z_][A-Za-z_0-9]*) = ',r"\t'\1', ",props,flags=re.M)
 items=append_root_item(items,"PlaceObj('ModItemInventoryItemCompositeDef', {\n'Id',\"HK416\",\n'Group',\"JAZZ - Firearm - Rifles-AR\",\n"+props+'}),')
 resources=[('InventoryItemCompositeDef','HK416')]
 for old,new,entity in [('JAZZ_BarrelNormal','JAZZ_HK416_BarrelNormal',None),('JAZZ_BarrelShort','JAZZ_HK416_BarrelShort',None),('JAZZ_BarrelLong','JAZZ_HK416_BarrelLong',None),('JAZZ_StockNormal','JAZZ_HK416_Stock','JAZZ_HK416_Stock'),('JAZZ_StockHeavy','JAZZ_HK416_StockCTR','JAZZ_HK416_StockCTR')]:
  lo,hi=component_block(items,old);block=items[lo:hi];block=re.sub(r'\bid\s*=\s*"'+old+'"','id="'+new+'"',block)
  hit=re.search(r'Visuals\s*=\s*\{',block);assert hit,old;end=matching(block,block.index('{',hit.start()),'{','}')
  visuals="{PlaceObj('WeaponComponentVisual', {ApplyTo=\"HK416\",Slot=\"Stock\",Entity="+json.dumps(entity)+',param_bindings=false})}' if entity else '{}'
  block=block[:hit.start()]+'Visuals = '+visuals+block[end:]
  if new.endswith('StockCTR'):block=re.sub(r'DisplayName\s*=\s*T\([^\n]+',lambda _:f'DisplayName=T({TEXTS[2][0]}, {json.dumps(TEXTS[2][1],ensure_ascii=False)}),',block)
  items=append_root_item(items,block+',');resources.append(('WeaponComponent',new))
 lo,hi=component_block(items,'JAZZ_MagNormal');block=items[lo:hi];visual="PlaceObj('WeaponComponentVisual', {ApplyTo=\"HK416\",Entity=\"JAZZ_HK416_Magazine\",Slot=\"Magazine\",param_bindings=false}),"
 block,n=re.subn(r'Visuals\s*=\s*\{',lambda m:m[0]+visual,block,count=1);assert n==1;items=items[:lo]+block+items[hi:]
 items=append_root_item(items,"PlaceObj('ModItemCode', {'name',\"Weapon_HK416Modular\",'CodeFileName',\"Code/Weapon_HK416Modular.lua\"}),");put(ROOT/'items.lua',items)
 meta=add_metadata(meta,'code',['"InventoryItem/HK416.lua"']);marker='"Code/Weapon_AEKModular.lua",';assert marker in meta;meta=meta.replace(marker,marker+'\n\t\t"Code/Weapon_HK416Modular.lua",',1)
 meta=add_metadata(meta,'affected_resources',[f"PlaceObj('ModResourcePreset', {{'Class',\"{c}\",'Id',\"{i}\"}})" for c,i in resources]);put(ROOT/'metadata.lua',meta)
 stage=a.build/'mod-assets-stage/Entities';entities=sorted(f.stem for f in stage.glob('JAZZ_HK416*.ent'));assert len(entities)==6
 ai=read(ASSETS/'items.lua');am=read(ASSETS/'metadata.lua')
 for name in entities:
  assert name not in ai;ai=append_root_item(ai,f"PlaceObj('ModItemEntity', {{'name',\"{name}\",'ClassParents',{{}},'entity_name',\"{name}\"}}),")
 put(ASSETS/'items.lua',ai);am=add_metadata(am,'entities',[json.dumps(e) for e in entities]);am=add_metadata(am,'code',[json.dumps('Entities/'+e+'.lua') for e in entities]);put(ASSETS/'metadata.lua',am)
 for src in stage.rglob('*'):
  if src.is_file():
   target=ASSETS/'Entities'/src.relative_to(stage);assert not target.exists();updates[target]=src.read_bytes()
 for variant in ('Short','Standard','Long'):
  for suffix in ('','_CTR'):
   name='HK416_'+variant+suffix;updates[ROOT/'WeaponIcons'/(name+'.png')]=(a.build/'previews'/(name+'_icon.png')).read_bytes()
 parser=LuaRuntime(unpack_returned_tuples=True).eval('function(s) local f,e=load(s);assert(f,e);return true end')
 report={'files':[],'entities':entities,'applied':False}
 for target,data in updates.items():
  if target.suffix=='.lua':parser(data.decode('utf-8-sig'))
  rel=target.relative_to(ROOT.parent);dest=a.build/'mod-data-stage'/rel;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(data);report['files'].append({'path':str(rel),'sha256':hashlib.sha256(data).hexdigest()})
 (a.build/'integration-plan.json').write_text(json.dumps(report,indent=2))
 (a.build/'texts.json').write_text(json.dumps(TEXTS,ensure_ascii=False),encoding='utf-8')
 if a.apply:
  running=subprocess.run(['powershell','-NoProfile','-Command','Get-Process JA3,JA3Debug -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Id'],capture_output=True,text=True).stdout.strip();assert not running,'Close game/editor before installation'
  assert json.loads((a.build/'lua-audit.json').read_text())['pass'];assert all(r['pass'] for r in json.loads((a.build/'compiled-audit.json').read_text()))
  for target,raw in before.items():assert target.read_bytes()==raw,'Concurrent change'
  for target,data in updates.items():
   if target.exists():
    backup=a.build/'integration-backup'/target.relative_to(ROOT.parent);backup.parent.mkdir(parents=True,exist_ok=True);assert not backup.exists();backup.write_bytes(target.read_bytes())
   target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
  report['applied']=True;(a.build/'integration-receipt.json').write_text(json.dumps(report,indent=2))
 print('APPLIED' if a.apply else 'STAGED',len(updates),'files')
if __name__=='__main__':main()
