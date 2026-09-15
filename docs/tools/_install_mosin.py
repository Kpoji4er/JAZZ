"""Install the prepared JAZZ_MosinModular transaction once, with game/editor closed.

python docs/tools/_install_mosin.py --build <JAZZ_MosinModular build directory>
Run canonical localization export and graph checks immediately afterwards.
"""
import argparse,re,shutil
from pathlib import Path
from lupa import LuaRuntime
from _integrate_sr3m import ROOT,ASSETS,matching,write,append_root_item,add_metadata

p=argparse.ArgumentParser();p.add_argument('--build',required=True,type=Path);a=p.parse_args();build=a.build
data=build/'mod-data-stage'
paths=[ROOT/'items.lua',ROOT/'metadata.lua',ASSETS/'items.lua',ASSETS/'metadata.lua']
before={p:p.read_bytes() for p in paths};texts={p:b.decode('utf-8-sig') for p,b in before.items()}
assert 'JAZZ_Mosin1891' not in (ROOT/'InventoryItem/Mosin.lua').read_text(encoding='utf-8'), 'Prototype installer retired: existing Mosin already modular'
items=texts[ROOT/'items.lua'];assert "'Id', \"JAZZ_MosinModular\"" not in items
def before_item(s,marker,kind,block):
    at=s.index(marker);start=s.rfind("PlaceObj('"+kind+"'",0,at);line=s.rfind('\n',0,start)+1
    indent=s[line:start];return s[:line]+indent+block+',\n'+s[line:]
item=(data/'weapon-item.lua').read_text(encoding='utf-8')
items=before_item(items,"'Id', \"Mosin\"",'ModItemInventoryItemCompositeDef',item)
blocks=(data/'components.lua').read_text(encoding='utf-8')
resources=[]
for m in re.finditer(r"PlaceObj\('ModItemWeaponComponent(?:Effect)?'",blocks):
    end=matching(blocks,blocks.index('(',m.start()));block=blocks[m.start():end]
    effect=block.startswith("PlaceObj('ModItemWeaponComponentEffect'")
    kind='ModItemWeaponComponentEffect' if effect else 'ModItemWeaponComponent'
    marker='id = "IncreaseShotAP"' if effect else 'id = "JAZZ_BarrelsDefs"'
    items=before_item(items,marker,kind,block)
    ident=re.search(r'\bid = "([^"]+)"',block)[1]
    resources.append("PlaceObj('ModResourcePreset', { 'Class', \""+kind.removeprefix('ModItem')+"\", 'Id', \""+ident+"\" })")
items=append_root_item(items,"PlaceObj('ModItemCode', { 'name', \"Weapon_MosinModular\", 'CodeFileName', \"Code/Weapon_MosinModular.lua\" }),")
texts[ROOT/'items.lua']=items
meta=add_metadata(texts[ROOT/'metadata.lua'],'code',['"InventoryItem/JAZZ_MosinModular.lua"'])
meta=add_metadata(meta,'affected_resources',["PlaceObj('ModResourcePreset', { 'Class', \"InventoryItemCompositeDef\", 'Id', \"JAZZ_MosinModular\", 'ClassDisplayName', \"Inventory item\" })"]+resources)
m=re.search(r"'code',\s*\{",meta);end=matching(meta,m.end()-1,'{','}')-1
meta=meta[:end]+'\n\t\t"Code/Weapon_MosinModular.lua",\n\t'+meta[end:]
texts[ROOT/'metadata.lua']=meta
entities=['MOSIN_1891','MOSIN_M38','MOSIN_Obrez']
folder="PlaceObj('ModItemFolder', { 'name', \"JAZZ_MosinModular\" }, {\n"+''.join(f"PlaceObj('ModItemEntity', {{ 'name', \"{e}\", 'ClassParents', {{}}, 'entity_name', \"{e}\" }}),\n" for e in entities)+'})'
texts[ASSETS/'items.lua']=append_root_item(texts[ASSETS/'items.lua'],folder+',')
meta=add_metadata(texts[ASSETS/'metadata.lua'],'entities',['"'+e+'"' for e in entities])
texts[ASSETS/'metadata.lua']=add_metadata(meta,'code',['"Entities/'+e+'.lua"' for e in entities])
lua=LuaRuntime()
for s in texts.values():lua.compile(s)
lua.compile((data/'JAZZ_MosinModular.lua').read_text(encoding='utf-8'))
copies={ROOT/'InventoryItem/JAZZ_MosinModular.lua':data/'JAZZ_MosinModular.lua',ROOT/'Code/Weapon_MosinModular.lua':data/'Weapon_MosinModular.lua'}
for name in entities:copies[ROOT/'WeaponIcons'/(name+'.png')]=build/(name+'_icon.png')
stage=build/'mod-assets-stage'/'Entities'
for src in stage.rglob('*'):
    if src.is_file():copies[ASSETS/'Entities'/src.relative_to(stage)]=src
for dest,src in copies.items():assert src.is_file() and not dest.exists(),(src,dest)
for path,raw in before.items():
    assert path.read_bytes()==raw,'Concurrent modification: '+str(path)
    target=build/'integration-backup'/path.parent.name/path.name;target.parent.mkdir(parents=True,exist_ok=True)
    assert not target.exists(),target
    target.write_bytes(raw)
for dest,src in copies.items():dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,dest)
for path,s in texts.items():write(path,s)
print('Installed modular Mosin, three configurations and resource graph. Localization and runtime verification still required.')
