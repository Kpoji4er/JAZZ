"""Read-only installed rifle/AK graph and ModItem/companion checks.

Also runs the SR3M checker. Does not claim game-renderer validation.
"""
import re,struct,xml.etree.ElementTree as ET
from PIL import Image
from _check_sr3m import ROOT,ASSETS,lua,native,matching,csv_ids
lua.execute('function point(...) return {...} end; function RGB(...) return {...} end; function RGBA(...) return {...} end')
items=(ROOT/'items.lua').read_text(encoding='utf-8');meta=(ROOT/'metadata.lua').read_text(encoding='utf-8')
asset_items=(ASSETS/'items.lua').read_text(encoding='utf-8');asset_meta=(ASSETS/'metadata.lua').read_text(encoding='utf-8')
def preset(kind,ident,key='Id'):
    pattern=(r"'Id',\s*" if key=='Id' else r'\bid\s*=\s*')+'"'+ident+'"'
    m=re.search(pattern,items);assert m,ident
    start=items.rfind("PlaceObj('"+kind+"'",0,m.start());end=matching(items,items.index('(',start))
    return native(lua.execute('return '+items[start:end]))
def weapon(ident):
    lua.execute((ROOT/f'InventoryItem/{ident}.lua').read_text(encoding='utf-8'))
    result=native(lua.globals().DefineClass[ident]);item=preset('ModItemInventoryItemCompositeDef',ident)
    keys=[k for k in result if not k.startswith('__')] if ident in ('AK74M','AK105','L42A1') else ['Entity','ComponentSlots']
    for key in keys:assert item.get(key)==result[key],(ident,key,item.get(key),result[key])
    assert f'"InventoryItem/{ident}.lua"' in meta
    return result,item
weapons={}
for ident in ('L42A1','Mosin','AK74','AKM','AK74M','AK105','AKSU','AK47'):
    if ident in ('AKSU','AK47'):
        lua.execute((ROOT/f'InventoryItem/{ident}.lua').read_text(encoding='utf-8'));weapons[ident]=native(lua.globals().DefineClass[ident]);continue
    weapons[ident],item=weapon(ident)
    assert item.get('Group','').endswith('Rifles-Bolt' if ident in ('Mosin','L42A1') else 'Rifles-Carbines' if ident=='AK105' else 'Rifles-AR'),(ident,item.get('Group'))
    if ident in ('AK74M','AK105','L42A1'):assert weapons[ident]['CanAppearInShop'] is True and weapons[ident]['RestockWeight']>0
assert not re.search(r"'Id',\s*\"JAZZ_MosinModular\"",items)
assert 'InventoryItem/JAZZ_MosinModular.lua' not in meta
assert not (ROOT/'InventoryItem/JAZZ_MosinModular.lua').exists()
assert 'Code/Weapon_MosinModular.lua' in meta
assert 'function Mosin:SetWeaponComponent' in (ROOT/'Code/Weapon_MosinModular.lua').read_text()

def slots(weapon):return {s['SlotType']:s for s in weapon['ComponentSlots'].values()}
for ident in ('AK74','AK74M','AK105','AKSU'):
    available=set(slots(weapons[ident])['Magazine']['AvailableComponents'].values())
    assert 'JAZZ_MagLarge_30_45' in available and not available&{'JAZZ_MagLarge_30_40','JAZZ_MagDrum_30_75'},(ident,available)
for ident in ('AKM','AK47'):
    available=set(slots(weapons[ident])['Magazine']['AvailableComponents'].values())
    assert {'JAZZ_MagLarge_30_40','JAZZ_MagDrum_30_75'}<=available and 'JAZZ_MagLarge_30_45' not in available
assert slots(weapons['Mosin'])['Scope']['AvailableComponents'][1]=='JAZZ_Scope_PU'
assert weapons['Mosin']['CanAppearInShop'] and weapons['Mosin']['RestockWeight']==110 and weapons['Mosin']['Tier']==1

entities=['L42A1','L42A1_Scope','MOSIN_1891','MOSIN_M38','MOSIN_Obrez']
entities += [p.stem for p in (ASSETS/'Entities').glob('AKR_*.ent')]
textures=set();spots={}
for ident in entities:
    assert f'"Entities/{ident}.lua"' in asset_meta
    assert re.search(r"'entity_name',\s*\""+ident+'"',asset_items),ident
    tree=ET.parse(ASSETS/f'Entities/{ident}.ent');assert not tree.findall('.//src')
    spots[ident]={node.get('name') for node in tree.findall('.//attach')}
    for node in tree.findall('.//mesh')+tree.findall('.//material'):assert (ASSETS/'Entities'/node.get('file')).is_file(),(ident,node.attrib)
    for node in tree.findall('.//material'):
        material=ET.parse(ASSETS/'Entities'/node.get('file'))
        for tag in material.getroot().iter():
            if tag.get('Name'):textures.add(tag.get('Name'))
for texture in textures:
    for directory,maximum in [('Textures',2048),('Textures/Fallbacks',64)]:
        path=ASSETS/'Entities'/directory/texture;data=path.read_bytes();assert data[:4]==b'DDS '
        height,width=struct.unpack_from('<II',data,12);assert max(width,height)<=maximum,(path,width,height)
for ident in ('MOSIN_1891','MOSIN_M38','MOSIN_Obrez'):assert {'Scope','Hand_l_grip'}<=spots[ident]
for ident in ('AK74','AKM','AK74M','AK105'):
    assert {'Stock','Magazine','Handguard','Muzzle','Scope','General'}<=spots['AKR_'+ident]
    for slot in slots(weapons[ident]).values():
        for comp in slot['AvailableComponents'].values():
            component=preset('ModItemWeaponComponent',comp,'id')
            assert component.get('Slot')==slot['SlotType'],(ident,comp,slot['SlotType'],component.get('Slot'))
    expected_size=(324,165) if ident in ('AK74','AKM') else (512,256)
    image=Image.open(ROOT/f'WeaponIcons/{ident}.png');assert image.size==expected_size and image.mode=='RGBA'
    if ident in ('AK74','AKM'):
        assert weapons[ident]['Entity']==ident
        for slot in slots(weapons[ident]).values():
            for comp in slot['AvailableComponents'].values():
                component=preset('ModItemWeaponComponent',comp,'id')
                for visual in component.get('Visuals',{}).values():
                    if visual.get('ApplyTo')==ident:
                        assert not visual.get('Entity','').startswith('AKR_'),(ident,comp,visual)
    image=Image.open(ROOT/f'WeaponComponents/Magazine/{ident}_Native30.png');assert image.size==(100,100) and image.mode=='RGBA'
long=ET.parse(ASSETS/'Entities/MOSIN_1891.ent')
assert long.find('.//material').get('file')=='Materials/Mosin_Mosin.mtl'
assert long.find('.//mesh').get('file')=='Meshes/Mosin_Mosin.m.hgm'
for language in ('Russian.csv','English.csv'):
    rows=csv_ids(ROOT/language)
    for ident in [761915301101,761915301103,761915302104,761915302105,761915302106,761915303101,761915303111]:assert str(ident) in rows,(language,ident)
print(f'PASS: installed ModItem/companion sync; {len(entities)} entity graphs; {len(textures)} DDS/fallback pairs; AK magazine families; legacy Mosin+PU; native icons and localization.')
