"""Install one validated leather carrier graph and isolated test unit.

--root candidate [--apply]. Dry run prepares complete transaction. Closed game,
source/contact/HGM gates, Lua compilation, backup and concurrency checks required.
"""
import argparse,hashlib,json,re,subprocess
from pathlib import Path
from lupa import LuaRuntime
from _install_soft_legion_armor import validate
from _integrate_sr3m import add_metadata,append_root_item

ROOT=Path(__file__).resolve().parents[2]
ASSETS=ROOT.parent/'jazz_assets';UNITS=ROOT.parent/'jazz-units'
ENTITY='JAZZ_LeatherArmor_Male';UID='JAZZ_Legion_ArmorTest_LeatherArmor'
ARMOR='JazzArmor_LeatherArmor'
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--root',type=Path,required=True)
    p.add_argument('--apply',action='store_true');a=p.parse_args();folder=a.root.resolve()
    assert json.loads((folder/'contacts.json').read_text())['status']=='PASS_SEWN_CONTACT'
    assert json.loads((folder/'qa-report.json').read_text())['status']=='PASS_SOURCE_OFFLINE'
    assert json.loads((folder/'compiled-audit.json').read_text())['pass']
    review=json.loads((folder/'visual-review.json').read_text())
    assert review['status']=='REVIEWED_OFFLINE'
    assert review.get('baked_reviewed'), 'Review the exported atlas on its final mesh before installing'
    assert review['source_sha256']==hashlib.sha256((folder/'source/LeatherArmor.blend').read_bytes()).hexdigest()
    def closed():
        running=subprocess.run(['powershell','-NoProfile','-Command',
            'Get-Process JA3,JA3Debug,ged -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Id'],capture_output=True,text=True)
        assert not running.stdout.strip(),'Game/editor must be closed'
    if a.apply:closed()
    stage=validate(folder/'build',ENTITY,'LeatherArmor')
    protected={path:path.read_bytes() for path in (ROOT/'ArmorIcons/LeatherArmor.png',ROOT/'InventoryItem/JazzArmor_LeatherArmor.lua')}
    paths=[ASSETS/'items.lua',ASSETS/'metadata.lua',UNITS/'items.lua',UNITS/'metadata.lua',
           ROOT/'Code/System_LegionArmorVisuals.lua']
    before={path:path.read_bytes() for path in paths}
    texts={path:data.decode('utf8') for path,data in before.items()}
    assert ENTITY not in texts[ASSETS/'items.lua'] and UID not in texts[UNITS/'items.lua'],'Already registered'
    mapping=ROOT/'Code/System_LegionArmorVisuals.lua'
    marker='local armor_entities = {'
    assert marker in texts[mapping] and not re.search(r'\b'+ARMOR+r'\s*=',texts[mapping])
    texts[mapping]=texts[mapping].replace(marker,marker+'\n\t'+ARMOR+' = { Male = "'+ENTITY+'" },',1)
    template=(UNITS/'UnitData/JAZZ_Legion_ArmorTest.lua').read_text(encoding='utf-8-sig')
    companion=template.replace('JAZZ_Legion_ArmorTest',UID).replace('JazzArmor_ImprovisedCuirass',ARMOR).replace('cuirass + MP40','leather carrier + MP40')
    props=companion[companion.index('    comment ='):companion.rfind('}')]
    props=re.sub(r'^    (\w+) = ',r"    '\1', ",props,flags=re.M)
    unit="PlaceObj('ModItemUnitDataCompositeDef', {\n    'Group', \"JAZZ Tests\",\n    'Id', \""+UID+'",\n'+props+'}),'
    text=texts[UNITS/'items.lua'];pos=text.rfind('}')
    texts[UNITS/'items.lua']=text[:pos]+unit+'\n'+text[pos:]
    texts[UNITS/'metadata.lua']=add_metadata(texts[UNITS/'metadata.lua'],'code',['"UnitData/'+UID+'.lua"'])
    texts[UNITS/'metadata.lua']=add_metadata(texts[UNITS/'metadata.lua'],'affected_resources',[
        "PlaceObj('ModResourcePreset', { 'Class', \"UnitDataCompositeDef\", 'Id', \""+UID+"\", 'ClassDisplayName', \"Unit\" })"])
    entity_item="PlaceObj('ModItemEntity', {\n    'name', \""+ENTITY+"\",\n    'ClassParents', { \"CharacterArmorMale\" },\n    'entity_name', \""+ENTITY+'",\n}),'
    texts[ASSETS/'items.lua']=append_root_item(texts[ASSETS/'items.lua'],entity_item)
    texts[ASSETS/'metadata.lua']=add_metadata(texts[ASSETS/'metadata.lua'],'code',['"Entities/'+ENTITY+'.lua"'])
    texts[ASSETS/'metadata.lua']=add_metadata(texts[ASSETS/'metadata.lua'],'entities',['"'+ENTITY+'"'])
    writes={path:text.encode('utf8') for path,text in texts.items()}
    writes[UNITS/'UnitData'/(UID+'.lua')]=companion.encode('utf8')
    for path in stage.rglob('*'):
        if path.is_file():
            assert path.name.startswith('JAZZ_LeatherArmor'),path
            writes[ASSETS/'Entities'/path.relative_to(stage)]=path.read_bytes()
    writes[ASSETS/'Entities'/(ENTITY+'.lua')]=('EntityData["'+ENTITY+'"] = { editor_artset = "Mods", entity = { class_parent = "CharacterArmorMale" } }\n').encode()
    lua=LuaRuntime()
    for path,data in writes.items():
        if path.suffix=='.lua':lua.compile(data.decode('utf-8-sig'))
    for path,data in before.items():assert path.read_bytes()==data,('Concurrent edit',path)
    for path in writes:
        if path not in before:assert not path.exists(),('Unexpected existing file',path)
    if not a.apply:
        for path,data in writes.items():
            dest=folder/'prepared-install'/path.relative_to(ROOT.parent)
            dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(data)
        print('DRY RUN PASS',len(writes),'files');return
    closed()
    backup=folder/'installation-backup';assert not backup.exists()
    for path,data in before.items():
        dest=backup/path.relative_to(ROOT.parent);dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(data)
    written=[]
    try:
        for path,data in writes.items():
            if path in before:assert path.read_bytes()==before[path],('Concurrent edit',path)
            else:assert not path.exists(),('Concurrent new file',path)
            path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(data);written.append(path)
        for path,data in writes.items():assert path.read_bytes()==data
        for path,data in protected.items():assert path.read_bytes()==data,('Protected item/icon changed',path)
    except Exception:
        for path in written:
            if path in before:path.write_bytes(before[path])
            else:path.unlink()
        raise
    (folder/'installation.json').write_text(json.dumps({'installed':True,'runtime':'NOT_RUN','entity':ENTITY,
        'unit':UID,'icon_preserved':True,'protected_sha256':{str(path.relative_to(ROOT.parent)):hashlib.sha256(data).hexdigest() for path,data in protected.items()},
        'sha256':{str(path.relative_to(ROOT.parent)):hashlib.sha256(data).hexdigest()
        for path,data in writes.items()}},indent=2))
    print('INSTALLED',len(writes),'files',ENTITY,UID)
if __name__=='__main__':main()
