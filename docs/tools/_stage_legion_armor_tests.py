"""Prepare (do not install) a test UnitData + ModItem per Torso armour.
python docs/tools/_stage_legion_armor_tests.py --output <folder>
Uses existing approved test unit and existing localization. Executes staged gear functions.
"""
import argparse,re,json
from pathlib import Path
from lupa import LuaRuntime
ROOT=Path(__file__).resolve().parents[2]
p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args();a.output.mkdir(parents=True,exist_ok=True)
template=(ROOT.parent/'jazz-units/UnitData/JAZZ_Legion_ArmorTest.lua').read_text(encoding='utf-8-sig')
lua=LuaRuntime();lua.execute('''DefineClass={};function UndefineClass() end;function T(id,s) return s end
function PlaceObj(c,p) return p end
function PlaceInventoryItem(id) return {class=id} end
function verify(f,armor)
 local u={slots={}};function u:TryEquip(items,slot,kind)
 local expected=kind=='Armor' and armor or 'MP40'
 for i,v in ipairs(items) do if v.class==expected then self.slots[slot]=v;table.remove(items,i);return end end
 error('missing '..expected) end
 function u:TryLoadAmmo(slot,kind,ammo) self.ammo=ammo end
 local items={};f(u,items)
 assert(u.slots.Torso.class==armor and u.slots['Handheld A'].class=='MP40')
 assert(#items==1 and items[1].Amount==120 and u.ammo=='JAZZ_AMMO_9x19_FMJ')
end''')
manifest=[]
for source in sorted((ROOT/'InventoryItem').glob('JazzArmor_*.lua')):
 text=source.read_text(encoding='utf-8-sig')
 if not re.search(r'ProtectedBodyParts\s*=\s*set\([^\n]*"Torso"',text):continue
 armor=source.stem
 if armor=='JazzArmor_ImprovisedCuirass':
  manifest.append({'armor':armor,'unit':'JAZZ_Legion_ArmorTest','state':'already installed'});continue
 uid='JAZZ_Legion_ArmorTest_'+armor.removeprefix('JazzArmor_')
 companion=template.replace('JAZZ_Legion_ArmorTest',uid).replace('JazzArmor_ImprovisedCuirass',armor).replace('cuirass + MP40',armor+' + MP40; visual readiness tracked separately')
 lua.execute(companion);definition=lua.globals().DefineClass[uid];lua.globals().verify(definition.CustomEquipGear,armor)
 props=companion[companion.index('    comment ='):companion.rfind('}')]
 serialized=re.sub(r'^    (\w+) = ',r"    '\1', ",props,flags=re.M)
 record="PlaceObj('ModItemUnitDataCompositeDef', {\n    'Group', \"JAZZ Tests\",\n    'Id', \""+uid+'",\n'+serialized+'})'
 lua.compile('return '+record)
 (a.output/(uid+'.lua')).write_text(companion,encoding='utf-8')
 (a.output/(uid+'.moditem.lua')).write_text('return '+record+'\n',encoding='utf-8')
 manifest.append({'armor':armor,'unit':uid,'state':'staged only; not installed'})
(a.output/'manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
print('PASS:',len(manifest),'Torso items;',len(manifest)-1,'new staged test definitions with executed loadouts; active mods untouched')
