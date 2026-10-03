"""Refresh only AEK971/HK416 slots in canonical CSV from installed companions."""
import csv
from pathlib import Path
from lupa import LuaRuntime
ROOT=Path(__file__).resolve().parents[2];data=ROOT/'docs/technical/weapons/data'
def read(name):
 with (data/name).open(encoding='utf-8-sig',newline='') as f:
  r=csv.DictReader(f);return r.fieldnames,list(r)
def write(name,fields,rows):
 with (data/name).open('w',encoding='utf-8',newline='') as f:
  w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
cf,components=read('weapon-components.csv');names={r['component_id']:r['display_name'] for r in components}
of,options=read('weapon-component-options.csv');wf,weapons=read('weapons.csv');ids={'AEK971','HK416'}
old_users={cid:{r['weapon_id'] for r in options if r['component_id']==cid} for cid in names}
options=[r for r in options if r['weapon_id'] not in ids]
lua=LuaRuntime();lua.execute('DefineClass={};function UndefineClass() end;function T(id,t) return t end;function PlaceObj(c,p) local r={};for i=1,#p,2 do r[p[i]]=p[i+1] end;return r end')
for ident in sorted(ids):
 lua.execute((ROOT/f'InventoryItem/{ident}.lua').read_text(encoding='utf-8-sig'));w=lua.globals().DefineClass[ident]
 row=next(r for r in weapons if r['id']==ident);row['display_name']=w.DisplayName;row['component_slot_count']=str(len(w.ComponentSlots));row['component_option_count']=str(sum(len(s.AvailableComponents) for s in w.ComponentSlots.values()))
 for index,s in w.ComponentSlots.items():
  default=s.DefaultComponent or '';available=list(s.AvailableComponents.values())
  for i,cid in enumerate(available,1):
   options.append(dict(weapon_id=ident,slot_index=str(index),slot_type=s.SlotType,modifiable=str(s.Modifiable is not False).lower(),can_be_empty=str(bool(s.CanBeEmpty)).lower(),default_component=default,default_in_options=str(default in available).lower(),option_index=str(i),component_id=cid,component_name=names[cid],component_source='jazz',is_default=str(cid==default).lower(),source_file=f'InventoryItem/{ident}.lua',snapshot_commit='working-tree'))
for row in components:
 cid=row['component_id'];new={r['weapon_id'] for r in options if r['component_id']==cid}
 row['used_by_count']=str(int(row['used_by_count'])+len(new)-len(old_users[cid]))
write('weapons.csv',wf,weapons);write('weapon-component-options.csv',of,options);write('weapon-components.csv',cf,components)
print('Synced 2 installed weapon slot catalogues')
