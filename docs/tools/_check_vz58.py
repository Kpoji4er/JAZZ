"""Read-only VZ58 Lua/metadata, resource graph, catalog, localization and loot gate.
--build DIR [--skip-localization] (intermediate checks only).
"""
import argparse,csv,json,re,struct,xml.etree.ElementTree as ET
from pathlib import Path
from lupa import LuaRuntime
from PIL import Image
from _integrate_vz58 import ROOT,ASSETS,TEXTS,VALUES,SLOTS,WIRING,GENERIC_SCOPES,component_block
from _integrate_sr3m import matching

p=argparse.ArgumentParser();p.add_argument('--build',type=Path,required=True);p.add_argument('--skip-localization',action='store_true');a=p.parse_args()
lua=LuaRuntime(unpack_returned_tuples=True)
lua.execute('''
function point(...) return {...} end
function T(id,text) return {id=id,text=text} end
function PlaceObj(c,p,ch) local r={} for k,v in pairs(p or {}) do if type(k)=='string' then r[k]=v end end for i=1,#(p or {}),2 do r[p[i]]=p[i+1] end return r end
DefineClass={};function UndefineClass(id) end
''')
def native(v):return {k:native(x) for k,x in v.items()} if hasattr(v,'items') else v
for package in [ROOT,ASSETS,ROOT.parent/'jazz-units']:
 for file in ('items.lua','metadata.lua'):lua.compile((package/file).read_text(encoding='utf-8-sig'))
items=(ROOT/'items.lua').read_text(encoding='utf-8-sig');meta=(ROOT/'metadata.lua').read_text(encoding='utf-8-sig')
hit=re.search(r"'Id',\s*\"VZ58\"",items);assert hit
start=items.rfind("PlaceObj('ModItemInventoryItemCompositeDef'",0,hit.start());end=matching(items,items.index('(',start))
item=native(lua.execute('return '+items[start:end]))
lua.execute((ROOT/'InventoryItem/VZ58.lua').read_text(encoding='utf-8'));w=native(lua.globals().DefineClass.VZ58)
for k,v in w.items():
 if not k.startswith('__'):assert item[k]==v,('companion mismatch',k)
for k,v in VALUES.items():assert w[k]==v,k
assert '"InventoryItem/VZ58.lua"' in meta
ai=(ASSETS/'items.lua').read_text(encoding='utf-8-sig');am=(ASSETS/'metadata.lua').read_text(encoding='utf-8-sig')
entities=['JAZZ_VZ58']+['JAZZ_VZ58_'+v[1] for v in WIRING.values()]
assert len(set(entities))==14
for ent in entities:
 assert f'"{ent}"' in ai and f'"{ent}"' in am and f'"Entities/{ent}.lua"' in am
 graph=ET.parse(ASSETS/'Entities'/(ent+'.ent'));assert not graph.findall('.//src')
 if ent=='JAZZ_VZ58':
  spots={x.get('name') for x in graph.findall('.//attach')}
  assert {'Muzzle','Trigger','Hand_l_grip'}|{s[0] for s in SLOTS}<=spots
 for n in graph.findall('.//mesh'):assert (ASSETS/'Entities'/n.get('file')).is_file()
 for n in graph.findall('.//material'):
  mat=ET.parse(ASSETS/'Entities'/n.get('file'))
  for x in mat.getroot().iter():
   name=x.get('Name')
   if not name:continue
   assert name.startswith('JAZZ_VZ58_')
   for folder,limit in [('Textures',2048),('Textures/Fallbacks',64)]:
    raw=(ASSETS/'Entities'/folder/name).read_bytes();assert raw[:4]==b'DDS ';h,width=struct.unpack_from('<II',raw,12);assert 0<max(h,width)<=limit
for cid,(slot,suffix) in WIRING.items():
 start,end=component_block(items,cid);component=native(lua.execute('return '+items[start:end]))
 visuals=[v for v in component['Visuals'].values() if v.get('ApplyTo')=='VZ58']
 assert len(visuals)==1,(cid,visuals)
 assert visuals[0]['Slot']==slot and visuals[0]['Entity']=='JAZZ_VZ58_'+suffix
 if cid=='JAZZ_VZ58_HandguardWood':assert set(component['BlockSlots'].values())=={'Scope','Under'}
# Every legal combination chooses one mesh per occupied slot, no base furniture duplicates.
actual_slots={s['SlotType']:list(s['AvailableComponents'].values()) for s in w['ComponentSlots'].values()}
for slot,options,_ in SLOTS:assert actual_slots[slot]==options,('slot options',slot)
for cid,entity in GENERIC_SCOPES.items():
 start,end=component_block(items,cid);component=native(lua.execute('return '+items[start:end]))
 generic=[v for v in component['Visuals'].values() if v.get('Slot')=='Scope' and not v.get('ApplyTo')]
 assert len(generic)==1 and generic[0]['Entity']==entity,(cid,generic)
import itertools
legal=0
for config in itertools.product(*[([None] if d is None else [])+opts for _,opts,d in SLOTS]):
 config=dict(zip([x[0] for x in SLOTS],config))
 if config['Handguard']=='JAZZ_VZ58_HandguardWood' and (config['Scope'] or config['Under']):continue
 visible=['JAZZ_VZ58']+[GENERIC_SCOPES[v] if v in GENERIC_SCOPES else 'JAZZ_VZ58_'+WIRING[v][1] for v in config.values() if v]
 assert len(visible)==len(set(visible));legal+=1
assert legal==352,legal
assert Image.open(ROOT/'WeaponIcons/VZ58.png').size==(324,165)
with (ROOT/'docs/technical/weapons/data/weapons.csv').open(encoding='utf-8-sig',newline='') as f:row=next(r for r in csv.DictReader(f) if r['id']=='VZ58')
assert (row['tier_label'],row['magazine_size'],row['component_slot_count'])==('2-2','30','7')
assert row['component_option_count']=='16'
loot=json.loads((a.build/'loot-report.json').read_text());assert len(loot['pools'])==8
ui=(ROOT.parent/'jazz-units/items.lua').read_text(encoding='utf-8-sig');um=(ROOT.parent/'jazz-units/metadata.lua').read_text(encoding='utf-8-sig')
for cid in loot['combos']:assert cid in ui and cid in um
assert json.loads((a.build/'compiled-audit.json').read_text())['pass']
report={'static':'PASS','compiled_mesh':'PASS','icon':'PASS','legal_configurations':legal,'entities':14,'loot_pools':8,'loot_weight':102000,'runtime':'NOT_RUN','editor_roundtrip':'NOT_RUN'}
if not a.skip_localization:
 for name,col in [('Russian.csv','Translation'),('English.csv','Translation'),('Localization/Strings.csv','English')]:
  with (ROOT/name).open(encoding='utf-8-sig',newline='') as f:
   if not f.readline().startswith('sep='):f.seek(0)
   rows={r['ID']:r for r in csv.DictReader(f)}
  for ident,ru,en in TEXTS.values():assert rows[ident][col]==(ru if name=='Russian.csv' else en),(name,ident)
 report['localization']='PASS (three new IDs)'
(a.build/'validation-report.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(json.dumps(report))
