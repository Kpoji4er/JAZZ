"""Add the installed AEK candidate to canonical weapon CSVs; run docs build next."""
import csv,io,re
from pathlib import Path
from lupa import LuaRuntime
from _integrate_aek import ROOT,TEXTS
data=ROOT/'docs/technical/weapons/data'
def read(name):
 with (data/name).open(encoding='utf-8-sig',newline='') as f:
  r=csv.DictReader(f);return r.fieldnames,list(r)
def write(name,fields,rows):
 with (data/name).open('w',encoding='utf-8',newline='') as f:
  w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
lua=LuaRuntime(unpack_returned_tuples=True);lua.execute('DefineClass={};function UndefineClass() end;function T(id,t) return t end;function PlaceObj(c,p) return p end')
lua.execute((ROOT/'InventoryItem/AEK971.lua').read_text(encoding='utf-8'));w=lua.globals().DefineClass.AEK971
fields,rows=read('weapons.csv');assert not any(r['id']=='AEK971' for r in rows)
row=dict(next(r for r in rows if r['id']=='AK74M'))
aliases={'shoot_ap':'ShootAP','reload_ap':'ReloadAP','cyclic_rpm':'CyclicRPM','caliber':'Caliber'}
for col in fields:
 value=w[aliases.get(col,''.join(s.title() for s in col.split('_')))]
 if isinstance(value,(str,int,float,bool)):row[col]=str(value).lower() if isinstance(value,bool) else str(value)
row.update(id='AEK971',display_name='АЕК-971',balance_tier='3',balance_subtier='2',tier_label='3-2',code_tier_label='3-2',tier_source='JAZZ-WEAPON-AEK-001',engine_tier='4',source_file='InventoryItem/AEK971.lua',snapshot_commit='working-tree',component_slot_count='3',component_option_count='5',available_attacks=';'.join(w.AvailableAttacks.values()))
row['defaulted_fields']=';'.join(k for k in row['defaulted_fields'].split(';') if w[k] is None)
rows.append(row);write('weapons.csv',fields,rows)
fields,rows=read('weapon-component-options.csv');assert not any(r['weapon_id']=='AEK971' for r in rows)
for index,(slot,options,default) in enumerate([('Barrel',['JAZZ_AEK_545','JAZZ_AEK_762'],'JAZZ_AEK_545'),('Magazine',['JAZZ_MagNormal'],'JAZZ_MagNormal'),('Stock',['JAZZ_StockLightUnFolded','JAZZ_StockLightFolded'],'JAZZ_StockLightUnFolded')],1):
 for option,id in enumerate(options,1):
  rows.append(dict(weapon_id='AEK971',slot_index=str(index),slot_type=slot,modifiable='true',can_be_empty='false',default_component=default,default_in_options='true',option_index=str(option),component_id=id,component_name={'JAZZ_AEK_545':'АЕК-971','JAZZ_AEK_762':'АЕК-973С'}.get(id,next((r['component_name'] for r in rows if r['component_id']==id),id)),component_source='jazz',is_default=str(id==default).lower(),source_file='InventoryItem/AEK971.lua',snapshot_commit='working-tree'))
write('weapon-component-options.csv',fields,rows)
fields,rows=read('weapon-components.csv')
for r in rows:
 if r['component_id'] in ('JAZZ_MagNormal','JAZZ_StockLightUnFolded','JAZZ_StockLightFolded'):r['used_by_count']=str(int(r['used_by_count'])+1)
effects=['JAZZ_AEK_762Caliber']+['JAZZ_AEK_'+s for s in ('Damage','WeaponRange','Recoil','AimAccuracy')]
for id,name in [('JAZZ_AEK_545','АЕК-971'),('JAZZ_AEK_762','АЕК-973С')]:
 rows.append(dict(component_id=id,display_name=name,slot='Barrel',cost='100',modification_difficulty='25',effects=';'.join(effects) if id.endswith('762') else '',parameters='',additional_costs='',group='Barrel',used_by_count='1',source='jazz',snapshot_commit='working-tree'))
write('weapon-components.csv',fields,rows)
fields,rows=read('weapon-component-effects.csv')
for id,key,value in [('JAZZ_AEK_762Caliber','caliber',None)]+[('JAZZ_AEK_'+s,s,v) for s,v in [('Damage',1),('WeaponRange',-8),('Recoil',4),('AimAccuracy',-1)]]:
 rows.append(dict(effect_id=id,display_name=id,description=TEXTS[key][1],parameters='' if value is None else 'AEKDelta='+str(value),source='jazz',snapshot_commit='working-tree'))
write('weapon-component-effects.csv',fields,rows)
print('Added AEK to four canonical CSVs')
