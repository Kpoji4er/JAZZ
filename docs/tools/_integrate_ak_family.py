"""Install staged AK remasters and AK74M/AK105 prototypes once (--build).

Uses existing shared magazine IDs. Original files are backed up; no publication.
"""
import argparse,json,re,shutil,xml.etree.ElementTree as ET
from pathlib import Path
from lupa import LuaRuntime
from _integrate_sr3m import ROOT,ASSETS,matching,write,add_metadata,append_root_item

p=argparse.ArgumentParser();p.add_argument('--build',type=Path,required=True);a=p.parse_args();build=a.build
before={path:path.read_bytes() for path in [ROOT/'items.lua',ROOT/'metadata.lua',ASSETS/'items.lua',ASSETS/'metadata.lua',ROOT/'InventoryItem/AK74.lua',ROOT/'InventoryItem/AKM.lua']}
texts={path:raw.decode('utf-8-sig') for path,raw in before.items()};items=texts[ROOT/'items.lua']
assert not re.search(r"'Id',\s*\"AK74M\"",items),'Already installed'
def bounds(s,kind,key,ident):
    pat=(r"'"+key+r"',\s*" if key=='Id' else r'\b'+key+r'\s*=\s*')+'"'+ident+'"'
    m=re.search(pat,s);assert m,ident
    start=s.rfind("PlaceObj('"+kind+"'",0,m.start());return start,matching(s,s.index('(',start))
def replace_slot(s,slot,transform):
    m=re.search(r"'SlotType',\s*\""+slot+'"',s);assert m,slot
    start=s.rfind("PlaceObj('WeaponComponentSlot'",0,m.start());end=matching(s,s.index('(',start))
    return s[:start]+transform(s[start:end])+s[end:]
def muzzle_default(block):
    if '"JAZZ_DefMuzzle"' not in block:block=block.replace("'AvailableComponents', {","'AvailableComponents', { \"JAZZ_DefMuzzle\",",1)
    if "'DefaultComponent'" not in block:block=block[:-2]+"'DefaultComponent', \"JAZZ_DefMuzzle\",\n})"
    return block
companions={}
for weapon in ('AK74','AKM'):
    text=texts[ROOT/f'InventoryItem/{weapon}.lua']
    text=text.replace(f'Entity = "{weapon}"',f'Entity = "AKR_{weapon}"')
    text=replace_slot(text,'Muzzle',muzzle_default);companions[weapon]=text
    start,end=bounds(items,'ModItemInventoryItemCompositeDef','Id',weapon);block=items[start:end]
    block=block.replace(f"'Entity', \"{weapon}\"",f"'Entity', \"AKR_{weapon}\"")
    block=replace_slot(block,'Muzzle',muzzle_default);items=items[:start]+block+items[end:]

translations={}
for weapon,index in [('AK74M',0),('AK105',1)]:
    text=texts[ROOT/'InventoryItem/AK74.lua'].replace("UndefineClass('AK74')",f"UndefineClass('{weapon}')").replace('DefineClass.AK74 =',f'DefineClass.{weapon} =')
    values={'comment':'"Tier 3-1"','CanAppearInShop':'false','RestockWeight':'0','Cost':'16000',
            'Entity':f'"AKR_{weapon}"','Icon':f'"Mod/e6L4ECj/WeaponIcons/{weapon}.png"','WeaponResource':'10000'}
    if weapon=='AK74M':values.update(WeaponMass='36',WeaponRange='50',Grouping='58')
    else:
        text=text.replace('"AssaultRifle"','"Carbine"')
        values.update(Damage='27',WeaponRange='40',AimAccuracy='11',WeaponMass='32',CyclicRPM='600',ShootAP='4000',Recoil='17',Grouping='55',BulletDropRange='14',CloseRange='6',CloseRangeFactor='90',WeaponSizeClass='"Carbine"',CategoryPair='"SubmachineGuns"',Noise='50')
        aa=text.index('\tAvailableAttacks = {');ae=matching(text,text.index('{',aa),'{','}')
        text=text[:aa]+'''\tAvailableAttacks = { "BurstFire", "AutoFire", "SingleShot", "RunAndGun_Carbine", "JAZZ_TargetSweep" }'''+text[ae:]
    for key,val in values.items():
        text,n=re.subn(r'^\t'+key+r' = [^\n]+',f'\t{key} = {val},',text,flags=re.M);assert n==1,key
    text=re.sub(r'^\tAdditionalHint = .*\n','',text,flags=re.M)
    ru='АК-74М' if weapon=='AK74M' else 'АК-105';en='AK-74M' if weapon=='AK74M' else 'AK-105'
    desc=('Автомат под патрон 5,45x39 мм с полимерным складным прикладом и общими магазинами семейства АК на 30 и 45 патронов.' if weapon=='AK74M' else 'Укороченный автомат под патрон 5,45x39 мм. Использует общие магазины семейства АК на 30 и 45 патронов.')
    eng=('A 5.45x39 mm rifle with a folding polymer stock and shared 30- and 45-round AK magazines.' if weapon=='AK74M' else 'A compact 5.45x39 mm carbine using shared 30- and 45-round AK magazines.')
    for offset,(key,russian,english) in enumerate([('DisplayName',ru,en),('DisplayNamePlural',ru,en),('Description',desc,eng)]):
        ident=761915303101+index*10+offset;assert str(ident) not in items
        translations[weapon+'_'+key]=[ident,russian,english]
        text,n=re.subn(r'^\t'+key+r' = .*$',f'\t{key} = T({ident}, "{russian}"),',text,flags=re.M);assert n==1
    text=text.replace(f'\tEntity = "AKR_{weapon}",',f'\tEntity = "AKR_{weapon}",\n\tfxClass = "AK74",')
    text=replace_slot(text,'Stock',lambda b:b.replace('"JAZZ_StockNormal",','').replace("'DefaultComponent', \n", "'DefaultComponent', \"JAZZ_StockLightUnFolded\",\n"))
    # Rebuild the stock slot explicitly to retain a valid default after removal.
    text=replace_slot(text,'Stock',lambda _:'''PlaceObj('WeaponComponentSlot', { 'SlotType', "Stock", 'AvailableComponents', { "JAZZ_StockLightUnFolded", "JAZZ_StockLightFolded" }, 'DefaultComponent', "JAZZ_StockLightUnFolded" })''')
    text=replace_slot(text,'Muzzle',lambda _:'''PlaceObj('WeaponComponentSlot', { 'SlotType', "Muzzle", 'AvailableComponents', { "JAZZ_DefMuzzle", "JAZZ_Compensator", "JAZZ_Suppressor" }, 'DefaultComponent', "JAZZ_DefMuzzle" })''')
    companions[weapon]=text
    props=text[text.index('\tcomment ='):text.rfind('}')]
    props=re.sub(r'^\t([A-Za-z_][A-Za-z_0-9]*) = ',r"\t'\1', ",props,flags=re.M)
    group='JAZZ - Firearm - Rifles-AR' if weapon=='AK74M' else 'JAZZ - Firearm - Rifles-Carbines'
    item=f"PlaceObj('ModItemInventoryItemCompositeDef', {{ 'Group', \"{group}\", 'Id', \"{weapon}\",\n"+props+'})'
    start,_=bounds(items,'ModItemInventoryItemCompositeDef','Id','AK74' if weapon=='AK74M' else 'AKSU')
    items=items[:start]+item+',\n'+items[start:]

# Existing AK74-specific optics/mounts/magazines are suitable donors for the new
# 5.45 rifles. Override their stock, standard magazine, handguard and muzzle.
for m in reversed(list(re.finditer(r"PlaceObj\('ModItemWeaponComponent'",items))):
    start=m.start();end=matching(items,items.index('(',start));block=items[start:end]
    ident=re.search(r'\bid\s*=\s*"([^"]+)"',block)[1]
    inserts=[]
    for v in list(re.finditer(r"PlaceObj\('WeaponComponentVisual'",block)):
        stop=matching(block,block.index('(',v.start()));visual=block[v.start():stop]
        if re.search(r'ApplyTo\s*=\s*"AK74"',visual):
            for weapon in ('AK74M','AK105'):inserts.append(visual.replace('"AK74"',f'"{weapon}"'))
    if inserts:block,n=re.subn(r'Visuals\s*=\s*\{','Visuals = {\n'+',\n'.join(inserts)+',\n',block,count=1);assert n==1
    for weapon in ('AK74','AKM','AK74M','AK105'):
        own={'JAZZ_Handguard':'Handguard','JAZZ_MagNormal':'Magazine','JAZZ_DefMuzzle':'Muzzle'}
        if weapon in ('AK74','AKM'):own['JAZZ_StockNormal']='Stock'
        else:own.update(JAZZ_StockLightUnFolded='Stock',JAZZ_StockLightFolded='StockFolded',JAZZ_UnfoldStocks='Stock')
        if weapon!='AKM':own['JAZZ_Compensator']='Muzzle'
        if ident not in own:continue
        suffix=own[ident];slot='Stock' if suffix=='StockFolded' else suffix
        replacement=f'PlaceObj(\'WeaponComponentVisual\', {{ ApplyTo = "{weapon}", Entity = "AKR_{weapon}_{suffix}", Slot = "{slot}", param_bindings = false'
        if slot=='Magazine':replacement+=f', Icon = "Mod/e6L4ECj/WeaponComponents/Magazine/{weapon}_Native30.png"'
        replacement+=' })'
        hits=[]
        for v in re.finditer(r"PlaceObj\('WeaponComponentVisual'",block):
            stop=matching(block,block.index('(',v.start()));visual=block[v.start():stop]
            if re.search(r'ApplyTo\s*=\s*"'+weapon+'"',visual) and re.search(r'Slot\s*=\s*"'+slot+'"',visual):hits.append((v.start(),stop))
        if hits:
            for vs,ve in reversed(hits):block=block[:vs]+replacement+block[ve:]
        else:
            block,n=re.subn(r'Visuals\s*=\s*\{','Visuals = {\n'+replacement+',\n',block,count=1);assert n==1,ident
    items=items[:start]+block+items[end:]
texts[ROOT/'items.lua']=items
meta=add_metadata(texts[ROOT/'metadata.lua'],'code',[f'"InventoryItem/{w}.lua"' for w in ('AK74M','AK105')])
texts[ROOT/'metadata.lua']=add_metadata(meta,'affected_resources',[f'PlaceObj(\'ModResourcePreset\', {{ \'Class\', "InventoryItemCompositeDef", \'Id\', "{w}", \'ClassDisplayName\', "Inventory item" }})' for w in ('AK74M','AK105')])

entities=[];copies={}
reference=ET.parse(ASSETS/'Entities/AK74.ent');refspots={n.get('name'):n for n in reference.findall('.//attach')}
for weapon in companions:
    stage=build/weapon/'mod-assets-stage/Entities'
    tree=ET.parse(stage/f'AKR_{weapon}.ent');mesh=tree.find('.//mesh_description')
    if weapon in ('AK74','AKM'):
        oldspots={n.get('name'):n for n in ET.parse(ASSETS/f'Entities/{weapon}.ent').findall('.//attach')}
        for node in mesh.findall('attach'):
            if node.get('name') in oldspots:node.set('spot_rot',oldspots[node.get('name')].get('spot_rot','0,0,1,0'))
    else:
        scope=next(n for n in mesh.findall('attach') if n.get('name')=='Scope')
        position=list(map(float,scope.get('spot_pos').split(',')));old_scope=list(map(float,refspots['Scope'].get('spot_pos').split(',')))
        for spot in ('General','Mount'):
            node=next((n for n in mesh.findall('attach') if n.get('name')==spot),None)
            if node is None:node=ET.SubElement(mesh,'attach',name=spot)
            offset=list(map(float,refspots[spot].get('spot_pos').split(',')))
            node.set('spot_pos',','.join(f'{position[i]+offset[i]-old_scope[i]:.3f}' for i in range(3)));node.set('spot_rot','0,0,1,0')
    tree.write(stage/f'AKR_{weapon}.ent',encoding='utf-8',xml_declaration=True)
    for src in stage.rglob('*'):
        if not src.is_file() or (weapon in ('AK74','AKM') and '_StockFolded' in src.name):continue
        copies[ASSETS/'Entities'/src.relative_to(stage)]=src
        if src.suffix=='.ent':entities.append(src.stem)
    copies[ROOT/f'WeaponIcons/{weapon}.png']=build/f'{weapon}_icon.png'
    copies[ROOT/f'WeaponComponents/Magazine/{weapon}_Native30.png']=build/f'{weapon}_Magazine_icon.png'
folder='PlaceObj(\'ModItemFolder\', { \'name\', "AK remasters" }, {\n'+''.join(f'PlaceObj(\'ModItemEntity\', {{ \'name\', "{e}", \'ClassParents\', {{}}, \'entity_name\', "{e}" }}),\n' for e in entities)+'}),'
texts[ASSETS/'items.lua']=append_root_item(texts[ASSETS/'items.lua'],folder)
meta=add_metadata(texts[ASSETS/'metadata.lua'],'entities',[f'"{e}"' for e in entities])
texts[ASSETS/'metadata.lua']=add_metadata(meta,'code',[f'"Entities/{e}.lua"' for e in entities])
for weapon,text in companions.items():texts[ROOT/f'InventoryItem/{weapon}.lua']=text
for text in texts.values():LuaRuntime().compile(text)
for dest,src in copies.items():
    assert src.is_file(),src
    if dest.exists():assert dest.parent==ROOT/'WeaponIcons',dest
backup=build/'integration-backup'
assert not backup.exists(),backup
for dest in copies:
    if dest.exists():before[dest]=dest.read_bytes()
for path,raw in before.items():
    assert path.read_bytes()==raw,'Concurrent modification: '+str(path)
    package=ROOT if path.is_relative_to(ROOT) else ASSETS
    dest=backup/package.name/path.relative_to(package);dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(raw)
for dest,src in copies.items():dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,dest)
for path,text in texts.items():write(path,text)
data=build/'mod-data-stage';data.mkdir(exist_ok=True)
(data/'texts.json').write_text(json.dumps(translations,ensure_ascii=False,indent=2),encoding='utf-8')
print(f'Installed 4 AKs, {len(entities)} entities; shared 5.45 magazine IDs retained; 7.62 magazine slots unchanged. Localization/runtime QA pending.')
