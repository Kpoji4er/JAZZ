"""Read-only installed Chainmail Body graph, class, hash and source QA validation."""
import argparse,hashlib,json,xml.etree.ElementTree as ET
from pathlib import Path
from lupa import LuaRuntime
from _integrate_sr3m import matching
ROOT=Path(__file__).resolve().parents[2];ASSETS=ROOT.parent/'jazz_assets';ENTITY='JAZZ_Chainmail_Male'
p=argparse.ArgumentParser();p.add_argument('--build-root',type=Path,required=True);a=p.parse_args()
receipt=json.loads((a.build_root/'installation.json').read_text())
for rel,digest in receipt['sha256'].items():
    if rel!='items.lua':assert hashlib.sha256((ASSETS/rel).read_bytes()).hexdigest()==digest,rel
for rel,digest in receipt['protected'].items():
    # Shared registries legitimately change for other assets and revision commits.
    # The exact Chainmail registration is checked below, rather than their file hashes.
    if Path(rel).name not in ('items.lua','metadata.lua'):
        assert hashlib.sha256((ROOT.parent/rel).read_bytes()).hexdigest()==digest,rel
lua=LuaRuntime();lua.execute('EntityData={};function PlaceObj(c,p) local t={} for i=1,#p,2 do t[p[i]]=p[i+1] end return t end')
text=(ASSETS/'items.lua').read_text(encoding='utf-8-sig');pos=text.index("'entity_name', \""+ENTITY+'"');start=text.rfind("PlaceObj('ModItemEntity'",0,pos);end=matching(text,text.index('(',start))
item=lua.execute('return '+text[start:end]);assert item.class_parent=='CharacterBodyMale' and len(item.ClassParents)==0
metadata=lua.execute((ASSETS/'metadata.lua').read_text(encoding='utf-8-sig'))
assert ENTITY in list(metadata.entities.values())
assert 'Entities/'+ENTITY+'.lua' in list(metadata.code.values())
lua.execute((ASSETS/'Entities'/(ENTITY+'.lua')).read_text());assert lua.globals().EntityData[ENTITY].entity.class_parent==item.class_parent
tree=ET.parse(ASSETS/'Entities'/(ENTITY+'.ent'));assert tree.find('inherit').get('entity')=='Male';assert not tree.findall('.//src')
for mesh in tree.findall('.//mesh'):assert (ASSETS/'Entities'/mesh.get('file')).is_file()
maps=[]
for material in tree.findall('.//material'):
    for node in ET.parse(ASSETS/'Entities'/material.get('file')).getroot().iter():
        if node.get('Name'):
            maps.append(node.tag)
            for folder in ('Textures','Textures/Fallbacks'):assert (ASSETS/'Entities'/folder/node.get('Name')).read_bytes()[:4]==b'DDS '
assert set(maps)=={'BaseColorMap','NormalMap','RMMap','ColorizationMap'}
for filename in ('compiled-audit.json','compiled-skin.json'):assert json.loads((a.build_root/filename).read_text())['pass']
assert json.loads((a.build_root/'poses/pose-check.json').read_text())['status']=='PASS_SKIN_STRUCTURE'
print('PASS Chainmail Body: installed hashes, class/companion, Male inheritance, four DDS maps/fallbacks, protected item/icon/test unit, pose/compiled geometry/skin')
