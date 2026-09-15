"""Install the prepared L42A1 transaction once, with game/editor closed.

python docs/tools/_install_l42a1.py --build <L42A1 build directory>
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
items=texts[ROOT/'items.lua'];assert "'Id', \"L42A1\"" not in items
def before_item(s,marker,kind,block):
    at=s.index(marker);start=s.rfind("PlaceObj('"+kind+"'",0,at);line=s.rfind('\n',0,start)+1
    indent=s[line:start];return s[:line]+indent+block+',\n'+s[line:]
item=(data/'weapon-item.lua').read_text(encoding='utf-8').replace('JAZZ - Firearm - Sniper Rifle','JAZZ - Firearm - Rifles-Bolt')
items=before_item(items,"'Id', \"M24Sniper\"",'ModItemInventoryItemCompositeDef',item)
items=before_item(items,'id = "JAZZ_Scope_PU"','ModItemWeaponComponent',(data/'scope-item.lua').read_text(encoding='utf-8'))
texts[ROOT/'items.lua']=items
meta=add_metadata(texts[ROOT/'metadata.lua'],'code',['"InventoryItem/L42A1.lua"'])
meta=add_metadata(meta,'affected_resources',["PlaceObj('ModResourcePreset', { 'Class', \"InventoryItemCompositeDef\", 'Id', \"L42A1\", 'ClassDisplayName', \"Inventory item\" })","PlaceObj('ModResourcePreset', { 'Class', \"WeaponComponent\", 'Id', \"JAZZ_L42A1_Scope\" })"])
texts[ROOT/'metadata.lua']=meta
entities=['L42A1','L42A1_Scope']
folder="PlaceObj('ModItemFolder', { 'name', \"L42A1\" }, {\n"+''.join(f"PlaceObj('ModItemEntity', {{ 'name', \"{e}\", 'ClassParents', {{}}, 'entity_name', \"{e}\" }}),\n" for e in entities)+'})'
texts[ASSETS/'items.lua']=append_root_item(texts[ASSETS/'items.lua'],folder+',')
meta=add_metadata(texts[ASSETS/'metadata.lua'],'entities',['"'+e+'"' for e in entities])
texts[ASSETS/'metadata.lua']=add_metadata(meta,'code',['"Entities/'+e+'.lua"' for e in entities])
lua=LuaRuntime()
for s in texts.values():lua.compile(s)
lua.compile((data/'L42A1.lua').read_text(encoding='utf-8'))
copies={ROOT/'InventoryItem/L42A1.lua':data/'L42A1.lua',ROOT/'WeaponIcons/L42A1.png':build/'L42A1_icon.png',ROOT/'WeaponComponents/Optics/JAZZ_L42A1_Scope.png':build/'JAZZ_L42A1_Scope.png'}
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
print('Installed L42A1, its native scope, icon and resource graph. Localization and runtime verification still required.')
