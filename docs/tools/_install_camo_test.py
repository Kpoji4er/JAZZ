"""Install a declared costume resource graph and isolated test appearance/unit."""
import argparse,json,re,hashlib,subprocess
from pathlib import Path
from lupa import LuaRuntime
from _integrate_sr3m import add_metadata,append_root_item
from _install_soft_legion_armor import validate
p=argparse.ArgumentParser();p.add_argument('--config',type=Path,required=True);p.add_argument('--apply',action='store_true');a=p.parse_args()
c=json.loads(a.config.read_text());root=Path(__file__).resolve().parents[2];assets=root.parent/'jazz_assets';units=root.parent/'jazz-units';out=a.config.parent
paths=[assets/'items.lua',assets/'metadata.lua',units/'items.lua',units/'metadata.lua'];before={p:p.read_bytes() for p in paths};texts={p:v.decode('utf-8-sig') for p,v in before.items()};writes={}
uid=c['unit'];assert uid not in texts[units/'items.lua']
for row in c['entities']:
 entity=row['name'];assert entity not in texts[assets/'items.lua'];stage=validate(Path(row['build']),entity,row['icon'])
 item="PlaceObj('ModItemEntity', { 'name', \"%s\", 'entity_name', \"%s\", 'ClassParents', { \"%s\" } }),"%(entity,entity,row['class'])
 texts[assets/'items.lua']=append_root_item(texts[assets/'items.lua'],item)
 texts[assets/'metadata.lua']=add_metadata(texts[assets/'metadata.lua'],'entities',[json.dumps(entity)])
 texts[assets/'metadata.lua']=add_metadata(texts[assets/'metadata.lua'],'code',[json.dumps('Entities/'+entity+'.lua')])
 for f in stage.rglob('*'):
  if f.is_file():writes[assets/'Entities'/f.relative_to(stage)]=f.read_bytes()
 writes[assets/'Entities'/(entity+'.lua')]=('EntityData[%s] = { editor_artset = "Mods", entity = { class_parent = %s } }\n'%(json.dumps(entity),json.dumps(row['class']))).encode()
appearance={key:'' for key in ('Head','Pants','Hat','Hat2','Hair','Armor','Shirt','Chest','Hip')};appearance.update(c['appearance']);appearance.update(group='JAZZ Tests',id=uid)
record="PlaceObj('ModItemAppearancePreset', {\n"+''.join('    '+k+' = '+json.dumps(v)+',\n' for k,v in appearance.items())+'}),'
texts[units/'items.lua']=append_root_item(texts[units/'items.lua'],record)
texts[units/'metadata.lua']=add_metadata(texts[units/'metadata.lua'],'affected_resources',["PlaceObj('ModResourcePreset', { 'Class', \"AppearancePreset\", 'Id', \""+uid+"\", 'ClassDisplayName', \"Appearance preset\" })"])
companion=(units/'UnitData/JAZZ_Legion_ArmorTest_TwaronLight.lua').read_text().replace('JAZZ_Legion_ArmorTest_TwaronLight',uid).replace('TwaronLight + MP40',c['label']+' + MP40').replace('"LegionGoon"',json.dumps(uid))
start=companion.index('    CustomEquipGear =');companion=companion[:start]+'    CustomEquipGear = function(self, items)\n'
for item,slot in c['gear']:
 companion+='        items[#items + 1] = PlaceInventoryItem('+json.dumps(item)+')\n'
 companion+='        self:TryEquip(items, '+json.dumps(slot)+', "Armor")\n'
companion+='''        items[#items + 1] = PlaceInventoryItem("MP40")
        local ammo = PlaceInventoryItem("JAZZ_AMMO_9x19_FMJ")
        ammo.Amount = 120
        items[#items + 1] = ammo
        self:TryEquip(items, "Handheld A", "Firearm")
        self:TryLoadAmmo("Handheld A", "Firearm", "JAZZ_AMMO_9x19_FMJ")
    end,
}
'''
props=companion[companion.index('    comment ='):companion.rfind('}')];props=re.sub(r'^    (\w+) = ',r"    '\1', ",props,flags=re.M)
record="PlaceObj('ModItemUnitDataCompositeDef', {\n    'Group', \"JAZZ Tests\",\n    'Id', "+json.dumps(uid)+',\n'+props+'}),'
texts[units/'items.lua']=append_root_item(texts[units/'items.lua'],record)
texts[units/'metadata.lua']=add_metadata(texts[units/'metadata.lua'],'code',[json.dumps('UnitData/'+uid+'.lua')])
texts[units/'metadata.lua']=add_metadata(texts[units/'metadata.lua'],'affected_resources',["PlaceObj('ModResourcePreset', { 'Class', \"UnitDataCompositeDef\", 'Id', \""+uid+"\", 'ClassDisplayName', \"Unit\" })"])
writes[units/'UnitData'/(uid+'.lua')]=companion.encode()
for path,text in texts.items():writes[path]=text.encode()
lua=LuaRuntime()
for path,data in writes.items():
 if path.suffix=='.lua':lua.compile(data.decode('utf-8-sig'))
for path,data in before.items():assert path.read_bytes()==data,'Concurrent change'
if not a.apply:
 for path,data in writes.items():
  target=out/'prepared-install'/path.relative_to(root.parent);target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
 print('PREPARED',uid);raise SystemExit()
running=subprocess.run(['powershell','-NoProfile','-Command','Get-Process JA3,JA3Debug,ged -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Id'],capture_output=True,text=True)
assert not running.stdout.strip(),'Close game/editor before new registration'
backup=out/'installation-backup';assert not backup.exists()
snapshot={p:p.read_bytes() if p.exists() else None for p in writes}
for path,data in snapshot.items():
 if data is not None:
  q=backup/path.relative_to(root.parent);q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(data)
try:
 for path,data in writes.items():path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(data)
 for path,data in writes.items():assert path.read_bytes()==data
except Exception:
 for path,data in snapshot.items():
  if data is None:path.unlink(missing_ok=True)
  else:path.write_bytes(data)
 raise
(out/'installation.json').write_text(json.dumps({'unit':uid,'runtime':'NOT_RUN','sha256':{str(p.relative_to(root.parent)):hashlib.sha256(data).hexdigest() for p,data in writes.items()}},indent=2))
print('INSTALLED',uid,len(writes),'files; runtime NOT_RUN')
