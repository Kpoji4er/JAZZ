"""Executable checks of installed soft armor registration and test loadouts."""
from pathlib import Path
import json
from lupa import LuaRuntime
from _integrate_sr3m import matching
from _install_soft_legion_armor import ROWS,ROOT,ASSETS,UNITS,validate
import argparse
p=argparse.ArgumentParser();p.add_argument('--build-root',type=Path,required=True);p.add_argument('--prepared',action='store_true');p.add_argument('--heavy-torso',action='store_true');a=p.parse_args()
if a.heavy_torso:ROWS=[(f+v,f+v) for f in ['Twaron','Guardian','Zylon'] for v in ['Light','Medium','Full']]
if a.prepared:
 ASSETS=a.build_root/'prepared-install/jazz_assets';UNITS=a.build_root/'prepared-install/jazz-units'
lua=LuaRuntime();lua.execute('''
DefineClass={};EntityData={};function UndefineClass(id) DefineClass[id]=nil end
function T(id,text) return text end
function PlaceObj(c,p,ch) local t={};for i=1,#p,2 do t[p[i]]=p[i+1] end;return t end
function PlaceInventoryItem(id) return {class=id} end
function verify(f,armor)
 local unit={slots={}}
 function unit:TryEquip(items,slot,kind)
  local id=kind=='Armor' and armor or 'MP40'
  for i,item in ipairs(items) do if item.class==id then self.slots[slot]=table.remove(items,i);return end end
  error('Missing '..id)
 end
 function unit:TryLoadAmmo(slot,kind,ammo) self.ammo=ammo end
 local items={};f(unit,items)
 assert(unit.slots.Torso.class==armor and unit.slots['Handheld A'].class=='MP40')
 assert(#items==1 and items[1].class=='JAZZ_AMMO_9x19_FMJ' and items[1].Amount==120)
 assert(unit.ammo=='JAZZ_AMMO_9x19_FMJ')
end
''')
def record(text,kind,needle):
 pos=text.index(needle);start=text.rfind("PlaceObj('"+kind+"'",0,pos);end=matching(text,text.index('(',start));return lua.execute('return '+text[start:end])
for package in [ROOT,ASSETS,UNITS]:
 for name in ['items.lua','metadata.lua']:lua.compile((package/name).read_text(encoding='utf-8-sig'))
manifest_path=a.build_root/('planned-install.json' if a.prepared else 'installation.json')
if not a.prepared and not manifest_path.exists() and (a.build_root/'fit-installation.json').exists():
 manifest=json.loads((a.build_root/'fit-installation.json').read_text());manifest['sha256']={'jazz_assets/'+p:d for p,d in manifest['sha256'].items()}
else:manifest=json.loads(manifest_path.read_text())
import hashlib
for path,digest in manifest.get('sha256',{}).items():
 # Shared metadata may evolve after installation: checked structurally below.
 if Path(path).name not in ['items.lua','metadata.lua']:assert hashlib.sha256((ROOT.parent/path).read_bytes()).hexdigest()==digest,path
for kind,item in ROWS:
 uid='JAZZ_Legion_ArmorTest_'+item;entity='JAZZ_'+item+'_Male';armor='JazzArmor_'+item
 validate(a.build_root/kind/'build',entity,item)
 pose=json.loads((a.build_root/kind/'poses/pose-check.json').read_text());assert pose['status']=='PASS_SKIN_STRUCTURE'
 unit=record((UNITS/'items.lua').read_text(encoding='utf-8-sig'),'ModItemUnitDataCompositeDef',"'Id', \""+uid+'"')
 lua.execute((UNITS/'UnitData'/(uid+'.lua')).read_text(encoding='utf-8-sig'));definition=lua.globals().DefineClass[uid]
 assert unit.Group=='JAZZ Tests' and definition.gender=='Male'
 assert unit.AppearancesList[1].Preset=='LegionGoon' and definition.AppearancesList[1].Preset=='LegionGoon'
 lua.globals().verify(unit.CustomEquipGear,armor);lua.globals().verify(definition.CustomEquipGear,armor)
 for key,value in definition.items():
  if key not in ['__parents','__generated_by_class','CustomEquipGear','AppearancesList','Equipment']:assert unit[key]==value,(uid,key)
 ent=record((ASSETS/'items.lua').read_text(encoding='utf-8-sig'),'ModItemEntity',"'entity_name', \""+entity+'"')
 assert ent.ClassParents[1]=='CharacterArmorMale';lua.execute((ASSETS/'Entities'/(entity+'.lua')).read_text())
 assert lua.globals().EntityData[entity].entity.class_parent=='CharacterArmorMale'
 assert '"UnitData/'+uid+'.lua"' in (UNITS/'metadata.lua').read_text()
 assert '"Entities/'+entity+'.lua"' in (ASSETS/'metadata.lua').read_text()
 assert '"'+entity+'"' in (ASSETS/'metadata.lua').read_text()
 print('PASS',item,'resources/registration/skin/loadouts; runtime NOT_RUN')
(a.build_root/('prepared-check.json' if a.prepared else 'installed-check.json')).write_text(json.dumps({'status':'PASS','prepared':a.prepared,'runtime':'NOT_RUN','items':[item for _,item in ROWS]},indent=2))
