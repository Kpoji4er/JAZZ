"""Stage/apply SCAR in core and assets with hash guards and backups.
--build DIR [--apply]. Compilation and executable Lua checks required to apply.
"""
import argparse,csv,hashlib,io,json,re,subprocess
from pathlib import Path
from lupa import LuaRuntime
from _integrate_sr3m import ROOT,ASSETS,matching,append_root_item,add_metadata
from _integrate_vz58 import component_block
from _apply_sr3m_slots import slot
VALUES={'comment':'Tier 3-2','object_class':'AssaultRifle','Entity':'JAZZ_SCAR_L_Standard',
 'Icon':'Mod/e6L4ECj/WeaponIcons/SCAR_L_Standard.png','Damage':24,'WeaponRange':48,
 'Recoil':16,'Grouping':63,'AimAccuracy':13,'CyclicRPM':650,'MagazineSize':30,
 'ShootAP':5000,'ReloadAP':6000,'Reliability':90,'WeaponResource':10000,
 'Cost':22000,'Tier':4,'RestockWeight':25,'MaxStock':1,'WeaponMass':35,'WeaponSizeClass':'Long'}
SLOTS=[('Conversion',['JAZZ_SCAR_L','JAZZ_SCAR_H','JAZZ_SCAR_SSR'],'JAZZ_SCAR_L'),
 ('Barrel',['JAZZ_SCAR_BarrelNormal','JAZZ_SCAR_BarrelShort','JAZZ_SCAR_BarrelLong'],'JAZZ_SCAR_BarrelNormal'),
 ('Stock',['JAZZ_SCAR_Stock','JAZZ_SCAR_StockFolded'],'JAZZ_SCAR_Stock'),
 ('Magazine',['JAZZ_MagNormal'],'JAZZ_MagNormal'),
 ('Muzzle',['JAZZ_SCAR_Muzzle','JAZZ_Compensator','JAZZ_Suppressor'],'JAZZ_SCAR_Muzzle'),
 ('Scope',['JAZZ_Reflex_Closed','JAZZ_Reflex_Eotech','JAZZ_Reflex_M68','JAZZ_CombatScope_2x','JAZZ_CombatScope_ACOG','JAZZ_Scope_6x','JAZZ_NightScope'],None),
 ('Under',['JAZZ_VerticalGrip','JAZZ_TacGrip','JAZZ_Bipod_Under'],None),
 ('Side',['JAZZ_Flashlight','JAZZ_FlashlightOff','JAZZ_FlashlightDot','JAZZ_LaserDot','JAZZ_UVDot'],None)]

def main():
 p=argparse.ArgumentParser();p.add_argument('--build',type=Path,required=True);p.add_argument('--apply',action='store_true');a=p.parse_args()
 before={};updates={};texts=[];resources=[]
 def read(path):before[path]=path.read_bytes();return before[path].decode('utf-8-sig')
 def put(path,s):
  old=before.get(path,b'');nl='\r\n' if b'\r\n' in old else '\n'
  updates[path]=(b'\xef\xbb\xbf' if old.startswith(b'\xef\xbb\xbf') else b'')+s.replace('\r\n','\n').replace('\n',nl).encode()
 items=read(ROOT/'items.lua');meta=read(ROOT/'metadata.lua')
 assert not (ROOT/'InventoryItem/SCAR.lua').exists(),'Already installed'
 def t(ru,en):
  for ident,r,e in texts:
   if r==ru:assert e==en;return f'T({ident}, {json.dumps(ru,ensure_ascii=False)})'
  ident=str(890000000034101+len(texts));assert ident not in items
  texts.append((ident,ru,en));return f'T({ident}, {json.dumps(ru,ensure_ascii=False)})'
 def append(block,cls,ident):
  nonlocal items
  items=append_root_item(items,block+',');resources.append((cls,ident))
 def effect(ident,stat,value,mode='Add'):
  desc=t(f'SCAR: {stat} {value:+}',f'SCAR: {stat} {value:+}')
  append(f"PlaceObj('ModItemWeaponComponentEffect', {{id=\"{ident}\",group=\"Stats\",StatToModify=\"{stat}\",ModificationType=\"{mode}\",Description={desc},Parameters={{PlaceObj('PresetParamNumber', {{'Name',\"SCARValue\",'Value',{value},'Tag',\"<SCARValue>\"}})}}}})",'WeaponComponentEffect',ident)
  return ident
 def component(ident,group,title,english,effects,extra=''):
  append(f"PlaceObj('ModItemWeaponComponent', {{id=\"{ident}\",group=\"{group}\",Slot=\"{group}\",Cost=100,ModificationDifficulty=25,Icon=\"UI/Icons/Upgrades/default_barrel\",DisplayName={t(title,english)},ModificationEffects={{{','.join(json.dumps(e) for e in effects)}}},Visuals={{}},{extra}}})",'WeaponComponent',ident)
 cal='JAZZ_SCAR_Caliber762'
 append(f"PlaceObj('ModItemWeaponComponentEffect', {{id=\"{cal}\",group=\"Caliber\",CaliberChange=\"JAZZ_Caliber_762x51\",Description={t('Калибр 7,62×51 мм','7.62x51 mm caliber')}}})",'WeaponComponentEffect',cal)
 heffects=[cal]+[effect('JAZZ_SCAR_H_'+stat,stat,value,mode) for stat,value,mode in [('Damage',9,'Add'),('WeaponRange',8,'Add'),('Recoil',11,'Add'),('Grouping',-3,'Add'),('CyclicRPM',-50,'Add'),('MagazineSize',20,'Set'),('ShootAP',1000,'Add')]]
 component('JAZZ_SCAR_L','Conversion','SCAR-L','SCAR-L',[])
 component('JAZZ_SCAR_H','Conversion','SCAR-H','SCAR-H',heffects)
 component('JAZZ_SCAR_SSR','Conversion','SCAR SSR','SCAR SSR',heffects,'BlockSlots={"Barrel","Stock"},')
 for kind,title,en,deltas in [('Normal','Штатный ствол SCAR','Standard SCAR barrel',{}),('Short','Короткий ствол SCAR','Short SCAR barrel',{'Damage':-1,'WeaponRange':-8,'Recoil':2,'Grouping':-3}),('Long','Длинный ствол SCAR','Long SCAR barrel',{'WeaponRange':8,'Grouping':3,'AimAccuracy':1})]:
  effects=[effect('JAZZ_SCAR_'+kind+'_'+k,k,v) for k,v in deltas.items()]
  component('JAZZ_SCAR_Barrel'+kind,'Barrel',title,en,effects)
 component('JAZZ_SCAR_Muzzle','Muzzle','Штатный пламегаситель SCAR','Standard SCAR flash hider',[])
 # Dedicated folding pair: unfolded is the baseline, without generic +2 recoil.
 for old,new,partner in [('JAZZ_StockLightUnFolded','JAZZ_SCAR_Stock','JAZZ_SCAR_StockFolded'),('JAZZ_StockLightFolded','JAZZ_SCAR_StockFolded','JAZZ_SCAR_Stock')]:
  lo,hi=component_block(items,old);block=items[lo:hi]
  block=re.sub(r'\bid\s*=\s*"'+old+'"','id="'+new+'"',block)
  for field,literal in [('Visuals','{}'),('zzFoldingPair','{'+json.dumps(partner)+'}')]:
   hit=re.search(field+r'\s*=\s*\{',block);assert hit
   end=matching(block,block.index('{',hit.start()),'{','}')
   block=block[:hit.start()]+field+' = '+literal+block[end:]
  if new=='JAZZ_SCAR_Stock':block=block.replace('"RecoilIncrease",','')
  append(block,'WeaponComponent',new)
 # Add only SCAR-scoped visuals to shared components.
 for ident,part in [('JAZZ_MagNormal','L_Magazine'),('JAZZ_SCAR_Stock','Stock'),('JAZZ_SCAR_StockFolded','StockFolded'),('JAZZ_SCAR_Muzzle','L_Muzzle')]:
  lo,hi=component_block(items,ident);block=items[lo:hi];vslot='Magazine' if part.endswith('Magazine') else 'Muzzle' if part.endswith('Muzzle') else 'Stock'
  visual=f"PlaceObj('WeaponComponentVisual', {{ApplyTo=\"SCAR\",Slot=\"{vslot}\",Entity=\"JAZZ_SCAR_{part}\",param_bindings=false}}),"
  block,n=re.subn(r'Visuals\s*=\s*\{',lambda m:m[0]+visual,block,count=1);assert n==1;items=items[:lo]+block+items[hi:]
 s=(ROOT/'InventoryItem/HK416.lua').read_text(encoding='utf-8-sig').replace('HK416','SCAR').replace('__parents = { "Carbine" }','__parents = { "AssaultRifle" }')
 for key,val in VALUES.items():
  line='\t'+key+' = '+json.dumps(val,ensure_ascii=False)+','
  s,n=re.subn(r'^\t'+key+r' = .*$',lambda _:line,s,flags=re.M)
  if not n:s=s.replace('\tcomment =',line+'\n\tcomment =',1)
 for key,text in [('DisplayName',t('SCAR-L','SCAR-L')),('DisplayNamePlural',t('SCAR-L','SCAR-L')),('Description',t('Модульная винтовка FN SCAR. Комплекты L/H меняют калибр, стволы — длину и характеристики. SSR — боевая винтовка под 7,62×51 мм с одиночным огнём.','A modular FN SCAR rifle. L/H kits change caliber; barrels change length and handling. SSR is a semi-automatic 7.62x51 mm battle-rifle configuration.'))]:
  s=re.sub(r'^\t'+key+r' = .*$',lambda _:f'\t{key} = {text},',s,flags=re.M)
 start=s.index('\tComponentSlots = {');end=matching(s,s.index('{',start),'{','}')
 s=s[:start]+'\tComponentSlots = {\n'+''.join(slot('\t\t',name,options,default,can_be_empty=default is None,modifiable=name!='Magazine') for name,options,default in SLOTS)+'\t}'+s[end:]
 start=s.index('\tAvailableAttacks = {');end=matching(s,s.index('{',start),'{','}')
 s=s[:start]+'\tAvailableAttacks = {"SingleShot","BurstFire","AutoFire","JAZZ_TargetSweep"}'+s[end:]
 put(ROOT/'InventoryItem/SCAR.lua',s)
 props=s[s.index('\t',s.index('__generated_by_class')):s.rfind('}')]
 props=re.sub(r'^\t__generated_by_class = .*\n','',props,flags=re.M);props=re.sub(r'^\t([A-Za-z_][A-Za-z_0-9]*) = ',r"\t'\1', ",props,flags=re.M)
 append("PlaceObj('ModItemInventoryItemCompositeDef', {'Id',\"SCAR\",'Group',\"JAZZ - Firearm - Rifles-AR\",\n"+props+'})','InventoryItemCompositeDef','SCAR')
 items=append_root_item(items,"PlaceObj('ModItemCode', {'name',\"Weapon_SCARModular\",'CodeFileName',\"Code/Weapon_SCARModular.lua\"}),");put(ROOT/'items.lua',items)
 meta=add_metadata(meta,'code',['"InventoryItem/SCAR.lua"']);marker='"Code/Weapon_HK416Modular.lua",';assert marker in meta;meta=meta.replace(marker,marker+'\n\t\t"Code/Weapon_SCARModular.lua",',1)
 meta=add_metadata(meta,'affected_resources',[f"PlaceObj('ModResourcePreset', {{'Class',\"{c}\",'Id',\"{i}\"}})" for c,i in resources]);put(ROOT/'metadata.lua',meta)
 stage=a.build/'mod-assets-stage/Entities';entities=sorted(f.stem for f in stage.glob('JAZZ_SCAR*.ent'));assert len(entities)==14
 ai=read(ASSETS/'items.lua');am=read(ASSETS/'metadata.lua')
 for name in entities:
  assert name not in ai;ai=append_root_item(ai,f"PlaceObj('ModItemEntity', {{'name',\"{name}\",'ClassParents',{{}},'entity_name',\"{name}\"}}),")
 put(ASSETS/'items.lua',ai);am=add_metadata(am,'entities',[json.dumps(e) for e in entities]);am=add_metadata(am,'code',[json.dumps('Entities/'+e+'.lua') for e in entities]);put(ASSETS/'metadata.lua',am)
 for src in stage.rglob('*'):
  if src.is_file():
   target=ASSETS/'Entities'/src.relative_to(stage);assert not target.exists();updates[target]=src.read_bytes()
 for src in (a.build/'previews').glob('SCAR*.png'):updates[ROOT/'WeaponIcons'/src.name]=src.read_bytes()
 manual=ROOT/'Localization/EnglishManual.csv';raw=read(manual);reader=csv.DictReader(io.StringIO(raw));fields=reader.fieldnames;rows=list(reader);n=max(int(r['N']) for r in rows)
 additions=[]
 for ident,ru,en in texts:
  existing=[r for r in rows if r['SourceText']==ru];assert not existing or all(r['English']==en for r in existing)
  if not existing:
   n+=1;additions.append(dict(N=n,AnchorID=ident,SourceText=ru,English=en,Notes='technical-copy' if ru==en else 'SCAR manual translation'))
 out=io.StringIO(newline='');csv.DictWriter(out,fieldnames=fields).writerows(additions);put(manual,raw.rstrip('\r\n')+'\n'+out.getvalue())
 parser=LuaRuntime().eval('function(s) local f,e=load(s);assert(f,e) end')
 report={'entities':entities,'files':[],'applied':False}
 for target,data in updates.items():
  if target.suffix=='.lua':parser(data.decode('utf-8-sig'))
  rel=target.relative_to(ROOT.parent);dest=a.build/'mod-data-stage'/rel;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(data);report['files'].append({'path':str(rel),'sha256':hashlib.sha256(data).hexdigest()})
 (a.build/'integration-plan.json').write_text(json.dumps(report,indent=2));(a.build/'texts.json').write_text(json.dumps(texts,ensure_ascii=False),encoding='utf-8')
 if a.apply:
  running=subprocess.run(['powershell','-NoProfile','-Command','Get-Process JA3,JA3Debug -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Id'],capture_output=True,text=True).stdout.strip();assert not running,'Game/editor must be closed'
  audits=json.loads((a.build/'compiled-audit.json').read_text());assert len(audits)==14 and all(r['pass'] for r in audits)
  assert json.loads((a.build/'lua-audit.json').read_text())['pass']
  for target,raw in before.items():assert target.read_bytes()==raw,'Concurrent edit'
  for target,data in updates.items():
   if target.exists():
    backup=a.build/'integration-backup'/target.relative_to(ROOT.parent);backup.parent.mkdir(parents=True,exist_ok=True);assert not backup.exists();backup.write_bytes(target.read_bytes())
   target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
  report['applied']=True;(a.build/'integration-receipt.json').write_text(json.dumps(report,indent=2))
 print('APPLIED' if a.apply else 'STAGED',len(updates))
if __name__=='__main__':main()
