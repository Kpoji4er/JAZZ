"""Move prototype configurations onto the existing Mosin item, preserving its economy.

One-time migration, --build <Mosin build>. Backups retain the retired test item.
"""
import argparse,re,shutil
from pathlib import Path
from lupa import LuaRuntime
from _integrate_sr3m import ROOT,matching,write

p=argparse.ArgumentParser();p.add_argument('--build',required=True,type=Path);a=p.parse_args()
backup=a.build/'old-item-merge-backup';backup.mkdir(exist_ok=True)
paths=[ROOT/'items.lua',ROOT/'metadata.lua',ROOT/'InventoryItem/Mosin.lua',
       ROOT/'InventoryItem/JAZZ_MosinModular.lua',ROOT/'Code/Weapon_MosinModular.lua']
before={path:path.read_bytes() for path in paths}
texts={path:raw.decode('utf-8-sig') for path,raw in before.items()}
old=texts[ROOT/'InventoryItem/Mosin.lua'];prototype=texts[ROOT/'InventoryItem/JAZZ_MosinModular.lua']
start=prototype.index('\tComponentSlots = {');end=matching(prototype,prototype.index('{',start),'{','}')
slots=prototype[start:end]
start=old.index('\tComponentSlots = {');end=matching(old,old.index('{',start),'{','}')
merged=old[:start]+slots+old[end:]
merged=merged.replace('Entity = "Mosin"','Entity = "MOSIN_1891"')
texts[ROOT/'InventoryItem/Mosin.lua']=merged
items=texts[ROOT/'items.lua']
def item_bounds(ident):
    m=re.search(r"'Id',\s*\""+ident+'"',items);assert m,ident
    start=items.rfind("PlaceObj('ModItemInventoryItemCompositeDef'",0,m.start())
    return start,matching(items,items.index('(',start))
start,end=item_bounds('JAZZ_MosinModular')
assert items[end]==','
items=items[:start]+items[end+1:]
start,end=item_bounds('Mosin');block=items[start:end]
ss=block.index("'ComponentSlots', {");ee=matching(block,block.index('{',ss),'{','}')
block=block[:ss]+slots.lstrip().replace('ComponentSlots =',"'ComponentSlots',",1)+block[ee:]
block=block.replace("'Entity', \"Mosin\"","'Entity', \"MOSIN_1891\"")
items=items[:start]+block+items[end:]
# Keep the pre-existing long rifle's mass; short configurations keep their own masses.
m=re.search(r'\bid = "JAZZ_Mosin1891"',items)
ss=items.rfind("PlaceObj('ModItemWeaponComponent'",0,m.start());ee=matching(items,items.index('(',ss))
block=items[ss:ee];block,n=re.subn(r"('Name', \"MosinMass\",\s*'Value', )45",r'\g<1>55',block);assert n==1
items=items[:ss]+block+items[ee:];texts[ROOT/'items.lua']=items
meta=texts[ROOT/'metadata.lua']
meta,n=re.subn(r'^\s*"InventoryItem/JAZZ_MosinModular.lua",\s*\n','',meta,flags=re.M);assert n==1
m=re.search(r"'Id',\s*\"JAZZ_MosinModular\"",meta);assert m
ss=meta.rfind("PlaceObj('ModResourcePreset'",0,m.start());ee=matching(meta,meta.index('(',ss));assert meta[ee]==','
meta=meta[:ss]+meta[ee+1:];texts[ROOT/'metadata.lua']=meta
texts[ROOT/'Code/Weapon_MosinModular.lua']=texts[ROOT/'Code/Weapon_MosinModular.lua'].replace('JAZZ_MosinModular','Mosin').replace('Only this new weapon class changes','Only the existing Mosin weapon class changes')
for path,s in texts.items():LuaRuntime().compile(s)
for path,raw in before.items():
    assert path.read_bytes()==raw,'Concurrent change: '+str(path)
    dest=backup/path.relative_to(ROOT);dest.parent.mkdir(parents=True,exist_ok=True)
    assert not dest.exists(),dest
    dest.write_bytes(raw)
for path,s in texts.items():
    if path.name!='JAZZ_MosinModular.lua':write(path,s)
(ROOT/'InventoryItem/JAZZ_MosinModular.lua').unlink()
print('Merged into Mosin; retired prototype definition and resource entry. Existing item names/economy/tier/base stats preserved.')
