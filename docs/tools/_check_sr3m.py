"""Read-only SR3M graph, Lua serialization, texture and attachment checks."""
import csv
import re
import struct
import xml.etree.ElementTree as ET
from pathlib import Path
from lupa import LuaRuntime
from _integrate_sr3m import ROOT, ASSETS, ENTITIES, TEXTS, matching

lua = LuaRuntime(unpack_returned_tuples=True)
lua.execute('''
function T(id, text) return {id=id,text=text} end
function PlaceObj(class, props, children)
  local result = {__class=class}
  for k,v in pairs(props or {}) do if type(k)=='string' then result[k]=v end end
  for i=1,#(props or {}),2 do result[props[i]]=props[i+1] end
  if children then result.__children=children end
  return result
end
DefineClass={}
function UndefineClass(id) DefineClass[id]=nil end
''')

def native(value):
    if hasattr(value,'items'):
        return {k:native(v) for k,v in value.items()}
    return value

def csv_ids(path):
    with path.open(encoding='utf-8-sig',newline='') as f:
        if not f.readline().startswith('sep='): f.seek(0)
        return {r['ID']:r for r in csv.DictReader(f)}

items=(ROOT/'items.lua').read_text(encoding='utf-8')
for package in [ROOT,ASSETS]:
    for name in ['items.lua','metadata.lua']:
        lua.compile((package/name).read_text(encoding='utf-8-sig'))
lua.execute((ROOT/'InventoryItem/SR3M.lua').read_text(encoding='utf-8'))
weapon=native(lua.globals().DefineClass.SR3M)
where=items.index("'Id', \"SR3M\"")
start=items.rfind("PlaceObj('ModItemInventoryItemCompositeDef'",0,where)
end=matching(items,items.index('(',start))
item=native(lua.execute('return '+items[start:end]))
for key,value in weapon.items():
    if not key.startswith('__'):
        assert item[key]==value, ('ModItem/companion mismatch',key)
# WEAPON-ROLLOUT-001: approved campaign/shop introduction.
assert weapon.get('CanAppearInShop') is True
assert (weapon['Tier'], weapon['RestockWeight'], weapon['Cost']) == (4,20,22000)
assert item['Group']=='JAZZ - Firearm - SMG'
assert weapon['Caliber']=='JAZZ_Caliber_9x39'
assert weapon['MagazineSize']==30
assert weapon['object_class']=='SubmachineGun'
assert weapon['comment']=='Tier 3-2'
assert weapon['Noise']>5
assert weapon['fxClass']=='AK74'
assert '"InventoryItem/SR3M.lua"' in (ROOT/'metadata.lua').read_text(encoding='utf-8')

entity_spots={}
asset_items=(ASSETS/'items.lua').read_text(encoding='utf-8')
asset_meta=(ASSETS/'metadata.lua').read_text(encoding='utf-8')
textures=set()
for name in ENTITIES:
    assert f'"Entities/{name}.lua"' in asset_meta
    assert f"'entity_name', \"{name}\"" in asset_items
    assert f'EntityData["{name}"]' in (ASSETS/f'Entities/{name}.lua').read_text()
    tree=ET.parse(ASSETS/f'Entities/{name}.ent')
    assert tree.getroot().get('name')==name
    assert tree.find("state[@id='idle']") is not None
    assert not tree.findall('.//src'), 'Absolute source path leaked'
    entity_spots[name]={n.get('name'):n for n in tree.findall('.//attach')}
    for node in tree.findall('.//mesh'):
        assert (ASSETS/'Entities'/node.get('file')).stat().st_size>0
    for node in tree.findall('.//material'):
        mtl=ET.parse(ASSETS/'Entities'/node.get('file'))
        for tag in mtl.getroot().iter():
            texture=tag.get('Name')
            if texture:
                assert texture.startswith('SR3M_') and texture.endswith('.dds')
                textures.add(texture)
for texture in textures:
    for folder,maximum in [('Textures',2048),('Textures/Fallbacks',64)]:
        path=ASSETS/'Entities'/folder/texture
        data=path.read_bytes()
        assert data[:4]==b'DDS '
        height,width=struct.unpack_from('<II',data,12)
        assert 0<width<=maximum and 0<height<=maximum,(texture,width,height)

count=0
for slot in weapon['ComponentSlots'].values():
    for ident in slot['AvailableComponents'].values():
        m=re.search(r'\bid\s*=\s*"'+ident+'"',items)
        start=items.rfind("PlaceObj('ModItemWeaponComponent'",0,m.start())
        end=matching(items,items.index('(',start))
        comp=native(lua.execute('return '+items[start:end]))
        visuals=[v for v in comp['Visuals'].values() if v.get('ApplyTo')=='SR3M']
        assert len(visuals)==1, (ident,visuals)
        visual=visuals[0]
        assert visual['Entity'] in ENTITIES
        assert visual['Slot'] in entity_spots['SR3M']
        count+=1
assert count==5
assert {'Hand_l_grip','Trigger','Muzzle'} <= entity_spots['SR3M'].keys()
assert 'Muzzle' in entity_spots['SR3M_Muzzle']
for filename,language_index in [('Russian.csv',1),('English.csv',2)]:
    rows=csv_ids(ROOT/filename)
    for ident,ru,en in TEXTS.values():
        row=rows[str(ident)]
        assert row['Translation']==(ru if language_index==1 else en), (filename,ident,row)
print(f'PASS: SR3M Lua/ModItem equality, 6 entities, 5 visual bindings, {len(textures)} DDS/fallback pairs, RU/EN.')
