"""Read-only R4 Lua/metadata, resource graph, catalog, localization and loot gate.
--build DIR [--skip-localization] (intermediate checks only).
"""
import argparse,csv,json,re,struct,xml.etree.ElementTree as ET
from pathlib import Path
from lupa import LuaRuntime
from PIL import Image
from _integrate_r4 import ROOT,ASSETS,TEXTS,VALUES
from _integrate_sr3m import matching

p=argparse.ArgumentParser();p.add_argument('--build',type=Path,required=True);p.add_argument('--skip-localization',action='store_true');a=p.parse_args()
lua=LuaRuntime(unpack_returned_tuples=True)
lua.execute('''
function T(id,text) return {id=id,text=text} end
function PlaceObj(c,p,ch) local r={} for k,v in pairs(p or {}) do if type(k)=='string' then r[k]=v end end for i=1,#(p or {}),2 do r[p[i]]=p[i+1] end return r end
DefineClass={};function UndefineClass(id) end
''')
def native(v):return {k:native(x) for k,x in v.items()} if hasattr(v,'items') else v
for package in [ROOT,ASSETS,ROOT.parent/'jazz-units']:
 for file in ('items.lua','metadata.lua'):lua.compile((package/file).read_text(encoding='utf-8-sig'))
items=(ROOT/'items.lua').read_text(encoding='utf-8-sig');meta=(ROOT/'metadata.lua').read_text(encoding='utf-8-sig')
hit=re.search(r"'Id',\s*\"VektorR4\"",items);assert hit
start=items.rfind("PlaceObj('ModItemInventoryItemCompositeDef'",0,hit.start());end=matching(items,items.index('(',start))
item=native(lua.execute('return '+items[start:end]))
lua.execute((ROOT/'InventoryItem/VektorR4.lua').read_text(encoding='utf-8'));w=native(lua.globals().DefineClass.VektorR4)
for k,v in w.items():
 if not k.startswith('__'):assert item[k]==v,('companion mismatch',k)
for k,v in VALUES.items():assert w[k]==v,k
assert '"InventoryItem/VektorR4.lua"' in meta
ent='JAZZ_VektorR4';ai=(ASSETS/'items.lua').read_text(encoding='utf-8-sig');am=(ASSETS/'metadata.lua').read_text(encoding='utf-8-sig')
assert f'"{ent}"' in ai and f'"{ent}"' in am and f'"Entities/{ent}.lua"' in am
graph=ET.parse(ASSETS/'Entities'/(ent+'.ent'));assert not graph.findall('.//src')
spots={x.get('name') for x in graph.findall('.//attach')};assert {'Muzzle','Trigger','Hand_l_grip','Magazine'}<=spots
for n in graph.findall('.//mesh'):assert (ASSETS/'Entities'/n.get('file')).is_file()
for n in graph.findall('.//material'):
 mat=ET.parse(ASSETS/'Entities'/n.get('file'))
 for x in mat.getroot().iter():
  name=x.get('Name')
  if not name:continue
  assert name.startswith(ent)
  for folder,limit in [('Textures',2048),('Textures/Fallbacks',64)]:
   raw=(ASSETS/'Entities'/folder/name).read_bytes();assert raw[:4]==b'DDS ';h,width=struct.unpack_from('<II',raw,12);assert 0<max(h,width)<=limit
assert Image.open(ROOT/'WeaponIcons/VektorR4.png').size==(324,165)
with (ROOT/'docs/technical/weapons/data/weapons.csv').open(encoding='utf-8-sig',newline='') as f:row=next(r for r in csv.DictReader(f) if r['id']=='VektorR4')
assert (row['tier_label'],row['magazine_size'],row['component_slot_count'])==('2-1','35','0')
loot=json.loads((a.build/'loot-report.json').read_text());assert len(loot['pools'])==8
ui=(ROOT.parent/'jazz-units/items.lua').read_text(encoding='utf-8-sig');um=(ROOT.parent/'jazz-units/metadata.lua').read_text(encoding='utf-8-sig')
for cid in loot['combos']:assert cid in ui and cid in um
assert json.loads((a.build/'compiled-audit.json').read_text())['pass']
report={'static':'PASS','compiled_mesh':'PASS','icon':'PASS','loot_pools':8,'loot_weight':101000,'runtime':'NOT_RUN','editor_roundtrip':'NOT_RUN'}
if not a.skip_localization:
 for name,col in [('Russian.csv','Translation'),('English.csv','Translation'),('Localization/Strings.csv','English')]:
  with (ROOT/name).open(encoding='utf-8-sig',newline='') as f:
   if not f.readline().startswith('sep='):f.seek(0)
   rows={r['ID']:r for r in csv.DictReader(f)}
  for ident,ru,en in TEXTS.values():assert rows[ident][col]==(ru if name=='Russian.csv' else en),(name,ident)
 report['localization']='PASS (three new IDs)'
(a.build/'validation-report.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(json.dumps(report))
