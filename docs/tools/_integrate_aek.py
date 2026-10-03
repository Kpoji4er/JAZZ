"""Bounded AEK971/973S installation. --build DIR [--apply]; requires closed JA3.
Creates all data layers and preserves originals in integration-backup.
Localization is seeded through EnglishManual; run the canonical catalog exporter.
"""
import argparse,csv,hashlib,io,json,re,subprocess
from pathlib import Path
from _integrate_sr3m import ROOT,ASSETS,matching,append_root_item,add_metadata
from _integrate_vz58 import component_block
from _apply_sr3m_slots import slot

TEXTS={
 'name':('890000000032101','АЕК-971','AEK-971'),
 'plural':('890000000032102','АЕК-971','AEK-971'),
 'description':('890000000032103','Автомат со сбалансированной автоматикой. Комплект АЕК-973С меняет калибр с 5,45×39 на 7,62×39 мм. Штатный магазин на 30 патронов, складной приклад.','A balanced-action assault rifle. The AEK-973S conversion changes its caliber from 5.45x39 to 7.62x39 mm. Standard 30-round magazine and folding stock.'),
 '762':('890000000032104','АЕК-973С','AEK-973S'),
 'caliber':('890000000032105','Калибр 7,62×39 мм','7.62x39 mm caliber'),
 'Damage':('890000000032106','Урон +4','Damage +4'),
 'WeaponRange':('890000000032107','Дальность −8','Range -8'),
 'Recoil':('890000000032108','Отдача +4','Recoil +4'),
 'AimAccuracy':('890000000032109','Точность прицеливания −1','Aim accuracy -1'),
}
def t(key):
 ident,ru,en=TEXTS[key];return f'T({ident}, {json.dumps(ru,ensure_ascii=False)})'
VALUES={'comment':'Tier 3-2','Reliability':90,'Cost':22000,'RestockWeight':25,'MaxStock':1,'Tier':4,
 'Entity':'JAZZ_AEK971','Icon':'Mod/e6L4ECj/WeaponIcons/AEK971.png','Damage':26,'WeaponRange':50,'Recoil':13,
 'AimAccuracy':12,'MagazineSize':30,'CyclicRPM':900,'AutoShots':9,'BurstShots':5,'WeaponMass':33,'WeaponResource':8000}

def weapon():
 s=(ROOT/'InventoryItem/AK74M.lua').read_text(encoding='utf-8-sig').replace('AK74M','AEK971')
 for field,key in [('DisplayName','name'),('DisplayNamePlural','plural'),('Description','description')]:
  s=re.sub(r'^\t'+field+r' = .*$',lambda _:f'\t{field} = {t(key)},',s,flags=re.M)
 for field,value in VALUES.items():
  line='\t'+field+' = '+json.dumps(value,ensure_ascii=False)+','
  s,n=re.subn(r'^\t'+field+r' = .*$',lambda _:line,s,flags=re.M)
  if not n:s=s.replace('\tcomment =',line+'\n\tcomment =',1)
 start=s.index('\tComponentSlots = {');end=matching(s,s.index('{',start),'{','}')
 slots=[('Barrel',['JAZZ_AEK_545','JAZZ_AEK_762'],'JAZZ_AEK_545'),('Magazine',['JAZZ_MagNormal'],'JAZZ_MagNormal'),('Stock',['JAZZ_StockLightUnFolded','JAZZ_StockLightFolded'],'JAZZ_StockLightUnFolded')]
 body=''.join(slot('\t\t',name,options,default,can_be_empty=False) for name,options,default in slots)
 s=s[:start]+'\tComponentSlots = {\n'+body+'\t}'+s[end:]
 props=s[s.index('\t',s.index('__generated_by_class')):s.rfind('}')]
 props=re.sub(r'^\t__generated_by_class = .*\n','',props,flags=re.M)
 props=re.sub(r'^\t([A-Za-z_][A-Za-z_0-9]*) = ',r"\t'\1', ",props,flags=re.M)
 item="\tPlaceObj('ModItemInventoryItemCompositeDef', {\n\t'Id', \"AEK971\",\n\t'Group', \"JAZZ - Firearm - Rifles-AR\",\n"+props+'\t}),'
 return s,item

def main():
 p=argparse.ArgumentParser();p.add_argument('--build',type=Path,required=True);p.add_argument('--apply',action='store_true');a=p.parse_args()
 proc=subprocess.run(['powershell','-NoProfile','-Command','Get-Process JA3,JA3Debug -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Id'],capture_output=True,text=True)
 assert not proc.stdout.strip(),'Close JA3/editor before installation'
 assert not (a.build/'integration-receipt.json').exists(),'Already applied'
 audits=json.loads((a.build/'compiled-audit.json').read_text());assert len(audits)==8 and all(r['pass'] and r['winding_positive_area_fraction']==0 for r in audits)
 before={};updates={}
 def read(path):before[path]=path.read_bytes();return before[path].decode('utf-8-sig')
 def put(path,s):
  raw=before.get(path,b'');nl='\r\n' if b'\r\n' in raw else '\n';updates[path]=(b'\xef\xbb\xbf' if raw.startswith(b'\xef\xbb\xbf') else b'')+s.replace('\r\n','\n').replace('\n',nl).encode()
 items=read(ROOT/'items.lua');meta=read(ROOT/'metadata.lua');assert '"AEK971"' not in items
 for ident,_,_ in TEXTS.values():assert ident not in items and ident not in (ROOT/'Localization/Strings.csv').read_text(encoding='utf-8-sig'),ident
 companion,item=weapon();put(ROOT/'InventoryItem/AEK971.lua',companion);items=append_root_item(items,item)
 effects=['JAZZ_AEK_762Caliber'];newresources=[('InventoryItemCompositeDef','AEK971')]
 items=append_root_item(items,f'PlaceObj(\'ModItemWeaponComponentEffect\', {{ id="JAZZ_AEK_762Caliber", group="Caliber", CaliberChange="JAZZ_Caliber_762x39", Description={t("caliber")} }}),')
 for stat,value in [('Damage',4),('WeaponRange',-8),('Recoil',4),('AimAccuracy',-1)]:
  ident='JAZZ_AEK_'+stat;effects.append(ident)
  items=append_root_item(items,f'PlaceObj(\'ModItemWeaponComponentEffect\', {{ id="{ident}", group="Stats", StatToModify="{stat}", ModificationType="Add", Description={t(stat)}, Parameters={{PlaceObj(\'PresetParamNumber\', {{\'Name\',"AEKDelta",\'Value\',{value},\'Tag\',"<AEKDelta>"}})}} }}),')
 for ident,key,eff in [('JAZZ_AEK_545','name',[]),('JAZZ_AEK_762','762',effects)]:
  effects_literal='{'+','.join(json.dumps(e) for e in eff)+'}'
  items=append_root_item(items,f'PlaceObj(\'ModItemWeaponComponent\', {{id="{ident}",group="Barrel",Slot="Barrel",Cost=100,ModificationDifficulty=25,Icon="UI/Icons/Upgrades/default_barrel",DisplayName={t(key)},ModificationEffects={effects_literal},Visuals={{}} }}),')
  newresources.append(('WeaponComponent',ident))
 newresources += [('WeaponComponentEffect',ident) for ident in effects]
 for ident,part in [('JAZZ_MagNormal','Magazine'),('JAZZ_StockLightUnFolded','Stock'),('JAZZ_StockLightFolded','StockFolded')]:
  start,end=component_block(items,ident);block=items[start:end];spot='Magazine' if part=='Magazine' else 'Stock'
  visual=f'PlaceObj(\'WeaponComponentVisual\', {{ApplyTo="AEK971",Entity="JAZZ_AEK971_{part}",Slot="{spot}",param_bindings=false}}),'
  block,n=re.subn(r'Visuals\s*=\s*\{',lambda m:m[0]+visual,block,count=1);assert n==1
  items=items[:start]+block+items[end:]
 items=append_root_item(items,'PlaceObj(\'ModItemCode\', {\'name\',"Weapon_AEKModular",\'CodeFileName\',"Code/Weapon_AEKModular.lua"}),')
 put(ROOT/'items.lua',items)
 meta=add_metadata(meta,'code',['"InventoryItem/AEK971.lua"'])
 # Class methods load after the shared setter and generated definitions.
 marker='"Code/Weapon_MosinModular.lua",';assert marker in meta;meta=meta.replace(marker,marker+'\n\t\t"Code/Weapon_AEKModular.lua",',1)
 meta=add_metadata(meta,'affected_resources',[f'PlaceObj(\'ModResourcePreset\', {{\'Class\',"{cls}",\'Id\',"{ident}"}})' for cls,ident in newresources]);put(ROOT/'metadata.lua',meta)
 ai=read(ASSETS/'items.lua');am=read(ASSETS/'metadata.lua');stage=a.build/'mod-assets-stage/Entities';entities=sorted(f.stem for f in stage.glob('JAZZ_AEK*.ent'));assert len(entities)==8
 for ent in entities:
  assert ent not in ai
  ai=append_root_item(ai,f'PlaceObj(\'ModItemEntity\', {{\'name\',"{ent}",\'ClassParents\',{{}},\'entity_name\',"{ent}"}}),')
 put(ASSETS/'items.lua',ai);am=add_metadata(am,'entities',[json.dumps(e) for e in entities]);am=add_metadata(am,'code',[json.dumps('Entities/'+e+'.lua') for e in entities]);put(ASSETS/'metadata.lua',am)
 for src in stage.rglob('*'):
  if src.is_file():
   target=ASSETS/'Entities'/src.relative_to(stage);assert not target.exists(),target;updates[target]=src.read_bytes()
 for variant in ('971','973S'):
  for folded in ('','_Folded'):
   target=ROOT/'WeaponIcons'/('AEK'+variant+folded+'.png');assert not target.exists();updates[target]=(a.build/'previews'/('AEK'+variant+folded+'_icon.png')).read_bytes()
 manual=ROOT/'Localization/EnglishManual.csv';raw=read(manual);reader=csv.DictReader(io.StringIO(raw));fields=reader.fieldnames;rows=list(reader);n=max(int(r['N']) for r in rows)
 additions=[]
 for i,(ident,ru,en) in enumerate(dict((v[1],v) for v in TEXTS.values()).values(),1):
  assert not any(r['SourceText']==ru and r['English']!=en for r in rows)
  if not any(r['SourceText']==ru for r in rows):additions.append(dict(N=str(n+i),AnchorID=ident,SourceText=ru,English=en,Notes='AEK manual translation'))
 out=io.StringIO(newline='');writer=csv.DictWriter(out,fieldnames=fields);writer.writerows(additions);put(manual,raw.rstrip('\r\n')+'\n'+out.getvalue())
 report={'files':[],'entities':entities,'runtime':'NOT_RUN'}
 from lupa import LuaRuntime
 parser=LuaRuntime(unpack_returned_tuples=True).eval('function(s) local f,e=load(s);assert(f,e);return true end')
 for path,data in updates.items():
  if path.suffix=='.lua':parser(data.decode('utf-8-sig'))
 for path,data in updates.items():
  relative=path.relative_to(ROOT.parent);dest=a.build/'mod-data-stage'/relative;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(data);report['files'].append({'path':str(relative),'sha256':hashlib.sha256(data).hexdigest()})
 (a.build/'integration-plan.json').write_text(json.dumps(report,indent=2))
 if a.apply:
  assert json.loads((a.build/'lua-audit.json').read_text())['pass'],'Run executable AEK checks first'
  for path,raw in before.items():assert path.read_bytes()==raw,'Concurrent change: '+str(path)
  for path,data in updates.items():
   if path.exists():
    backup=a.build/'integration-backup'/path.relative_to(ROOT.parent);backup.parent.mkdir(parents=True,exist_ok=True);assert not backup.exists();backup.write_bytes(path.read_bytes())
   path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(data)
  (a.build/'integration-receipt.json').write_text(json.dumps(report,indent=2))
 print('APPLIED' if a.apply else 'STAGED',len(updates),'files')
if __name__=='__main__':main()
