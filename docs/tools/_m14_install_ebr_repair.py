"""Stage/install only repaired EBR resources and its component visual mappings.
--export-root <ExportedEntities> --build <repair build> --game-root <JA3> [--apply]
Dry-run prepares named resources outside mods. Existing files backed up before apply.
"""
import argparse
import hashlib
import json
import re
import shutil
import subprocess
from pathlib import Path
import xml.etree.ElementTree as ET
from _integrate_m14_family import matching, append_root_item, add_metadata, find_item_block

p=argparse.ArgumentParser()
for n in ('export-root','build','game-root'):p.add_argument('--'+n,type=Path,required=True)
p.add_argument('--apply',action='store_true')
p.add_argument('--host',choices=['MK14EBR','JAZZ_M14','JAZZ_M14_MkIII'],default='MK14EBR')
a=p.parse_args()
root=Path(__file__).resolve().parents[2];assets=root.parent/'jazz_assets'
host=a.host
weapons=['M14SAW','M21'] if host=='JAZZ_M14' else [host]
names=[host]+[host+'_Barrel'+n for n in ('Normal','Short','Long')]
if host!='MK14EBR':names += [host+'_Magazine'+n for n in ('Short','Normal')]
stage=a.build/'install-stage';stage.mkdir(exist_ok=True)
suffix={'BaseColorMap':'Base','NormalMap':'Norm','RMMap':'RM','AOMap':'AO'}
plan={};textures={}
for name in names:
    tree=ET.parse(a.export_root/(name+'.ent'));e=tree.getroot();e.set('name',name)
    for lod in e.findall('.//lod'):
        for node in list(lod.findall('src')):lod.remove(node)
    for node in e.findall('.//mesh'):
        rel=node.get('file');plan[assets/'Entities'/rel]=a.export_root/rel
    for node in e.findall('.//material'):
        rel=node.get('file');mtl=ET.parse(a.export_root/rel)
        if host!='MK14EBR':mtl=ET.parse(assets/'Entities/Materials'/(host+'_Mesh.mtl'))
        for tex in mtl.getroot().iter():
            old=tex.get('Name')
            if not old:continue
            if host!='MK14EBR':continue
            new='MK14EBR_'+suffix[tex.tag]+'.dds'
            source=a.export_root/'Textures'/old
            if new in textures:assert textures[new].read_bytes()==source.read_bytes()
            textures[new]=source;tex.set('Name',new)
        out=stage/rel;out.parent.mkdir(parents=True,exist_ok=True)
        mtl.write(out,encoding='utf-8',xml_declaration=True)
        plan[assets/'Entities'/rel]=out
    out=stage/(name+'.ent');tree.write(out,encoding='utf-8',xml_declaration=True)
    plan[assets/'Entities'/(name+'.ent')]=out
    if name!=host:
        out=stage/(name+'.lua');out.write_text('EntityData["'+name+'"] = { editor_artset = "Mods" }\n',encoding='utf-8')
        plan[assets/'Entities'/(name+'.lua')]=out
cvt=a.game_root/'ModTools/hgimgcvt.exe'
for name,source in textures.items():
    out=stage/'Textures'/name;out.parent.mkdir(exist_ok=True)
    shutil.copy2(source,out)
    fallback=stage/'Textures/Fallbacks'/name;fallback.parent.mkdir(exist_ok=True)
    subprocess.run([str(cvt),str(out),str(fallback),'--truncate','64'],check=True,capture_output=True)
    plan[assets/'Entities/Textures'/name]=out
    plan[assets/'Entities/Textures/Fallbacks'/name]=fallback

items=(root/'items.lua').read_text(encoding='utf-8')
changes=[]
pattern=re.compile(r"PlaceObj\('WeaponComponentVisual',\s*\{[^{}]*?ApplyTo = \"(?:"+'|'.join(weapons)+r")\",[^{}]*?\}\)",re.S)
def visual(m):
    block=m.group()
    entity=re.search(r'Entity = "([^"]*)"',block)
    slot=re.search(r'Slot = "([^"]*)"',block)
    if not entity or not slot:return block
    old=entity[1];new=None
    if slot[1]=='Barrel' and old.startswith('WeaponAttA_BarrelM14_'):
        new=host+'_Barrel'+{'Standard':'Normal','Long':'Long','Short':'Short'}[old.rsplit('_',1)[1]]
    elif slot[1]=='Muzzle' and old=='WeaponAttA_MuzzleM14':new=''
    elif slot[1]=='Mount' and old=='WeaponAttA_MountM14':new=''
    elif host=='JAZZ_M14' and slot[1]=='Magazine' and old.startswith('WeaponAttA_MagazineM14_'):
        new=host+'_Magazine'+('Normal' if old.endswith('Extended') else 'Short')
    elif host=='JAZZ_M14_MkIII' and slot[1]=='Magazine' and old=='':
        component=re.search(r'id = "([^"]+)"',items[m.end():])[1]
        new=host+'_Magazine'+('Short' if 'Small' in component else 'Normal')
    if new is None:return block
    changes.append((old,new));return block[:entity.start(1)]+new+block[entity.end(1):]
items=pattern.sub(visual,items)
assert host+'_BarrelNormal' in items
assert all('WeaponAttA_BarrelM14_' not in m.group() for m in pattern.finditer(items))
if host=='JAZZ_M14':
    at=items.index('id = "JAZZ_GrenadeLauncher_M14"')
    start=items.rfind("PlaceObj('ModItemWeaponComponent'",0,at)
    end=matching(items,items.index('(',start));block=items[start:end]
    if 'ApplyTo = "M21"' not in block:
        rx=re.compile(r"PlaceObj\('WeaponComponentVisual',\s*\{[^{}]*?ApplyTo = \"M14SAW\",[^{}]*?\}\)",re.S)
        block,n=rx.subn(lambda m:m.group()+',\n'+m.group().replace('ApplyTo = "M14SAW"','ApplyTo = "M21"'),block)
        assert n==2,n
        items=items[:start]+block+items[end:]
if host=='JAZZ_M14_MkIII':
    start,end=find_item_block(items,host);block=items[start:end]
    block=block.replace("'ModifyRightHandGrip', false,","'ModifyRightHandGrip', true,")
    block=block.replace("'DefaultComponent', \"JAZZ_M14_Default_Muzzle\",","'DefaultComponent', \"JAZZ_Suppressor\",")
    def default_scope(s):
        at=s.index("'SlotType', \"Scope\"")
        opening=s.rfind("PlaceObj('WeaponComponentSlot'",0,at);end=matching(s,s.index('(',opening))
        chunk=s[opening:end]
        if "'DefaultComponent'" not in chunk:
            chunk=chunk.replace("'CanBeEmpty', true,","'CanBeEmpty', true,\n\t\t\t'DefaultComponent', \"JAZZ_Scope_12x\",")
        return s[:opening]+chunk+s[end:]
    block=default_scope(block);items=items[:start]+block+items[end:]
    comp=root/'InventoryItem/JAZZ_M14_MkIII.lua'
    body=comp.read_text(encoding='utf-8').replace('ModifyRightHandGrip = false,','ModifyRightHandGrip = true,')
    body=body.replace("'DefaultComponent', \"JAZZ_M14_Default_Muzzle\",","'DefaultComponent', \"JAZZ_Suppressor\",")
    body=default_scope(body)
    out=stage/'JAZZ_M14_MkIII.lua';out.write_text(body,encoding='utf-8',newline='\n');plan[comp]=out
asset_items=(assets/'items.lua').read_text(encoding='utf-8')
meta=(assets/'metadata.lua').read_text(encoding='utf-8')
for name in names[1:]:
    if '"'+name+'"' not in asset_items:
        asset_items=append_root_item(asset_items,"PlaceObj('ModItemEntity', {\n    'name', \""+name+"\",\n    'ClassParents', {},\n    'entity_name', \""+name+"\",\n}),")
    if '"'+name+'"' not in meta:meta=add_metadata(meta,'entities',['"'+name+'"'])
    if '"Entities/'+name+'.lua"' not in meta:meta=add_metadata(meta,'code',['"Entities/'+name+'.lua"'])
for dest,body,label in [(root/'items.lua',items,'jazz-items.lua'),(assets/'items.lua',asset_items,'assets-items.lua'),(assets/'metadata.lua',meta,'assets-metadata.lua')]:
    out=stage/label;out.write_text(body,encoding='utf-8',newline='\n');plan[dest]=out
report={'mappings':changes,'files':[str(x) for x in plan],'applied':a.apply}
print(json.dumps(report,indent=2))
if a.apply:
    running=subprocess.run(['powershell','-NoProfile','-Command',"@(Get-Process JA3,JA3Debug -ErrorAction SilentlyContinue).Count"],capture_output=True,text=True)
    assert running.stdout.strip()=='0','Close JA3 before install'
    backup=a.build/'install-backup';backup.mkdir(exist_ok=True)
    for dest,source in plan.items():
        if dest.exists():
            key=hashlib.sha256(str(dest).encode()).hexdigest()[:10]+'-'+dest.name
            saved=backup/key
            if not saved.exists():shutil.copy2(dest,saved)
        dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source,dest)
    (a.build/'installation.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
