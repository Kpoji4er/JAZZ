"""Install staged Chainmail Body under its existing ID; dry run unless --apply."""
import argparse,hashlib,json,subprocess
from pathlib import Path
from lupa import LuaRuntime
from _integrate_sr3m import matching
from _install_soft_legion_armor import validate
ROOT=Path(__file__).resolve().parents[2];ASSETS=ROOT.parent/'jazz_assets';ENTITY='JAZZ_Chainmail_Male'
p=argparse.ArgumentParser();p.add_argument('--build-root',required=True,type=Path);p.add_argument('--apply',action='store_true');a=p.parse_args();a.build_root=a.build_root.resolve()
stage=validate(a.build_root/'build',ENTITY,'Chainmail')
assert json.loads((a.build_root/'compiled-audit.json').read_text())['pass']
assert json.loads((a.build_root/'compiled-skin.json').read_text())['pass']
assert json.loads((a.build_root/'poses/pose-check.json').read_text())['status']=='PASS_SKIN_STRUCTURE'
lua=LuaRuntime();writes={}
items=ASSETS/'items.lua';text=items.read_text(encoding='utf-8-sig')
pos=text.index("'entity_name', \""+ENTITY+'"');start=text.rfind("PlaceObj('ModItemEntity'",0,pos);end=matching(text,text.index('(',start))
block=text[start:end];assert 'CharacterArmorMale' in block
block=block.replace("'ClassParents', { \"CharacterArmorMale\" },", "'ClassParents', {},\n    'class_parent', \"CharacterBodyMale\",")
assert 'CharacterArmorMale' not in block and 'CharacterBodyMale' in block
writes[items]=(text[:start]+block+text[end:]).encode('utf-8')
for source in stage.rglob('*'):
    if source.is_file() and source.suffix!='.lua':
        assert source.name.startswith('JAZZ_Chainmail'),source
        writes[ASSETS/'Entities'/source.relative_to(stage)]=source.read_bytes()
writes[ASSETS/'Entities'/(ENTITY+'.lua')]=('EntityData["'+ENTITY+'"] = { editor_artset = "Mods", entity = { class_parent = "CharacterBodyMale" } }\n').encode()
for path,data in writes.items():
    assert path.resolve().is_relative_to(ASSETS.resolve())
    if path.suffix=='.lua':lua.compile(data.decode('utf-8-sig'))
meta=ASSETS/'metadata.lua';meta_before=meta.read_bytes()
assert ('"'+ENTITY+'"') in meta_before.decode('utf-8-sig') and ('"Entities/'+ENTITY+'.lua"') in meta_before.decode('utf-8-sig')
protected=[ROOT/'ArmorIcons/Chainmail.png',ROOT/'InventoryItem/JazzArmor_Chainmail.lua',ROOT.parent/'jazz-units/UnitData/JAZZ_Legion_ArmorTest_Chainmail.lua',meta]
protected_hash={str(f.relative_to(ROOT.parent)):hashlib.sha256(f.read_bytes()).hexdigest() for f in protected}
report=dict(entity=ENTITY,part='Body',class_parent='CharacterBodyMale',files=len(writes),runtime='NOT_RUN',protected=protected_hash)
report['source_sha256']=hashlib.sha256((a.build_root/'source/Chainmail.blend').read_bytes()).hexdigest()
if a.apply:
    running=subprocess.run(['powershell','-NoProfile','-Command','Get-Process JA3,JA3Debug,ged -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Id'],capture_output=True,text=True)
    assert not running.stdout.strip(),'Close game/editor before installing'
    backup=a.build_root/'install-backup';assert not backup.exists(),'Backup exists; do not repeat installation'
    before={f:f.read_bytes() if f.exists() else None for f in writes}
    for path,data in before.items():
        if data is not None:
            dest=backup/path.relative_to(ASSETS);dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(data)
    assert meta.read_bytes()==meta_before,'Concurrent metadata edit'
    try:
        for path,data in writes.items():
            assert (path.read_bytes() if path.exists() else None)==before[path],('Concurrent edit',path)
            path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(data)
        for path,data in writes.items():assert path.read_bytes()==data
        for path,digest in protected_hash.items():assert hashlib.sha256((ROOT.parent/path).read_bytes()).hexdigest()==digest
    except Exception:
        for path,data in before.items():
            if data is not None:path.write_bytes(data)
            elif path.exists() and path.read_bytes()==writes[path]:path.unlink()
        raise
    report.update(installed=True,sha256={str(f.relative_to(ASSETS)):hashlib.sha256(data).hexdigest() for f,data in writes.items()})
    (a.build_root/'installation.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
else:report['installed']=False
print(json.dumps(report,indent=2))
