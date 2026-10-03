"""Add the installed AEK candidate to canonical weapon CSVs; run docs build next."""
import csv,io,re
from pathlib import Path
from lupa import LuaRuntime
from _integrate_hk416 import ROOT,TEXTS,SLOTS
data=ROOT/'docs/technical/weapons/data'
def read(name):
 with (data/name).open(encoding='utf-8-sig',newline='') as f:
  r=csv.DictReader(f);return r.fieldnames,list(r)
def write(name,fields,rows):
 with (data/name).open('w',encoding='utf-8',newline='') as f:
  w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
lua=LuaRuntime(unpack_returned_tuples=True);lua.execute('DefineClass={};function UndefineClass() end;function T(id,t) return t end;function PlaceObj(c,p) return p end')
lua.execute((ROOT/'InventoryItem/HK416.lua').read_text(encoding='utf-8'));w=lua.globals().DefineClass.HK416
fields,rows=read('weapons.csv');assert not any(r['id']=='HK416' for r in rows)
row=dict(next(r for r in rows if r['id']=='M4A1'))
aliases={'shoot_ap':'ShootAP','reload_ap':'ReloadAP','cyclic_rpm':'CyclicRPM','caliber':'Caliber'}
for col in fields:
 value=w[aliases.get(col,''.join(s.title() for s in col.split('_')))]
 if isinstance(value,(str,int,float,bool)):row[col]=str(value).lower() if isinstance(value,bool) else str(value)
row.update(id='HK416',display_name='РђР•Рљ-971',balance_tier='3',balance_subtier='1',tier_label='3-1',code_tier_label='3-1',tier_source='JAZZ-WEAPON-HK416-001',engine_tier='4',source_file='InventoryItem/HK416.lua',snapshot_commit='working-tree',component_slot_count='4',component_option_count='11',available_attacks=';'.join(w.AvailableAttacks.values()))
row['defaulted_fields']=';'.join(k for k in row['defaulted_fields'].split(';') if w[k] is None)
rows.append(row);write('weapons.csv',fields,rows)
fields,rows=read('weapon-components.csv')
clones={'JAZZ_HK416_BarrelNormal':'JAZZ_BarrelNormal','JAZZ_HK416_BarrelShort':'JAZZ_BarrelShort','JAZZ_HK416_BarrelLong':'JAZZ_BarrelLong','JAZZ_HK416_Stock':'JAZZ_StockNormal','JAZZ_HK416_StockCTR':'JAZZ_StockHeavy'}
used={id for _,options,_ in SLOTS for id in options}
for r in rows:
 if r['component_id'] in used:r['used_by_count']=str(int(r['used_by_count'])+1)
for id,old in clones.items():
 r=dict(next(r for r in rows if r['component_id']==old));r.update(component_id=id,used_by_count='1',snapshot_commit='working-tree')
 if id.endswith('CTR'):r['display_name']='Приклад Magpul CTR'
 rows.append(r)
names={r['component_id']:r['display_name'] for r in rows}
write('weapon-components.csv',fields,rows)
fields,rows=read('weapon-component-options.csv')
assert not any(r['weapon_id']=='HK416' for r in rows)
for index,(slot,options,default) in enumerate(SLOTS,1):
 for option,id in enumerate(options,1):
  rows.append(dict(weapon_id='HK416',slot_index=str(index),slot_type=slot,modifiable=str(slot!='Magazine').lower(),can_be_empty=str(default is None).lower(),default_component=default or '',default_in_options=str(default in options).lower(),option_index=str(option),component_id=id,component_name=names[id],component_source='jazz',is_default=str(id==default).lower(),source_file='InventoryItem/HK416.lua',snapshot_commit='working-tree'))
write('weapon-component-options.csv',fields,rows)
print('Added HK416 to three canonical CSVs')
