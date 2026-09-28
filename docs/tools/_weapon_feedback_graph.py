"""Run vanilla visual traversal with all actual default slots and components.

--game-root DIR --output JSON [--items FILE]. Offline graph, not game rendering.
"""
import argparse,json,re
from pathlib import Path
import xml.etree.ElementTree as ET
from lupa import LuaRuntime
from _integrate_m14_family import matching
p=argparse.ArgumentParser();p.add_argument('--game-root',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--items',type=Path)
p.add_argument('--assets',type=Path);p.add_argument('--setter',type=Path);p.add_argument('--mosin',type=Path)
a=p.parse_args();root=Path(__file__).resolve().parents[2];lua=LuaRuntime(unpack_returned_tuples=True)
source=(root/'docs/tools/_weapon_feedback_components.py').read_text()
setup=source.split("lua.execute('''",1)[1].split("''')",1)[0];lua.execute(setup)
lua.execute('function point(...) return {...} end; function RGBA(...) return {...} end; function RGB(...) return {...} end')
staged=(a.items or root/'items.lua').read_text(encoding='utf-8-sig')
for m in re.finditer(r"PlaceObj\('ModItemWeaponComponent'",staged):
 end=matching(staged,staged.index('(',m.start()));v=lua.execute('return '+staged[m.start():end]);lua.globals().WeaponComponents[v.id]=v
for path in (root.parent/'jazz_assets/Entities').glob('*.ent'):
 spots={n.get('name'):True for n in ET.parse(path).findall('.//attach')}
 lua.globals().EntitySpots[path.stem]=lua.table_from(spots)
if a.assets:
 for path in (a.assets/'Entities').glob('*.ent'):
  lua.globals().EntitySpots[path.stem]=lua.table_from({n.get('name'):True for n in ET.parse(path).findall('.//attach')})
engine=(a.game_root/'ModTools/Src/Lua/Tactical/Weapon.lua').read_text(encoding='utf-8');start=engine.index('function FirearmBase:UpdateVisualObj(vis)');end=engine.index('\nfunction ',start+10);lua.execute(engine[start:end])
lua.execute('''
 OnMsg={}; WeaponComponentEffects={}
 function ObjModified() end
 function table.find_value(t,key,value) for _,v in ipairs(t or {}) do if v[key]==value then return v end end end
 function FirearmBase:UnregisterReactions() end
 function FirearmBase:RegisterReactions() end
 function FirearmBase:RemoveModifiers() end
 for _,c in pairs(WeaponComponents) do c.ModificationEffects={} end
''')
lua.execute((a.setter or root/'Code/System_WeaponComponent_Set.lua').read_text(encoding='utf-8'))
report={}
for name in ('M4A1','M16A4'):
 lua.execute((root/'InventoryItem'/(name+'.lua')).read_text(encoding='utf-8'))
 lua.globals().name=name
 lua.execute('''
 local def=DefineClass[name]
 w=setmetatable({class=name,components={},subweapons={},ComponentSlots=def.ComponentSlots},{__index=FirearmBase})
 for _,s in ipairs(w.ComponentSlots) do w.components[s.SlotType]=s.DefaultComponent or "" end
 vis=PlaceObject();vis:ChangeEntity(def.Entity);vis.weapon=w;vis.parts={};vis.components={};w.visual_obj=vis
 results={}
 for _,id in ipairs({"JAZZ_BarrelNormal","JAZZ_BarrelShort","JAZZ_BarrelNormal","JAZZ_BarrelShort"}) do
  w:SetWeaponComponent('Barrel',id);w:UpdateVisualObj(vis)
  local row={id=id,parts={}}
  for spot,obj in pairs(vis.parts) do row.parts[spot]={entity=obj.entity,parent=obj.parent.entity,valid=IsValid(obj)} end
  results[#results+1]=row
 end
 ''')
 report[name]=[{'id':v.id,'parts':{k:dict(o.items()) for k,o in v.parts.items()}} for _,v in lua.globals().results.items()]
 for v in report[name]:
  assert v['parts']['Barrel']['entity'].endswith('_BarrelShort' if v['id'].endswith('Short') else '_Barrel')
  assert v['parts']['Muzzle']['parent']==v['parts']['Barrel']['entity'],v
if a.assets:
 for name in ('M14SAW','M21'):
  lua.execute((root/'InventoryItem'/(name+'.lua')).read_text(encoding='utf-8'));lua.globals().name=name
  lua.execute('''
   local def=DefineClass[name]
   local w=setmetatable({class=name,components={},subweapons={},ComponentSlots=def.ComponentSlots},{__index=FirearmBase})
   for _,s in ipairs(w.ComponentSlots) do w.components[s.SlotType]=s.DefaultComponent or "" end
   local vis=PlaceObject();vis:ChangeEntity(def.Entity);vis.weapon=w;vis.parts={};vis.components={};w.visual_obj=vis
   w:UpdateVisualObj(vis)
   if name=="M21" then assert(vis.parts.Opticsmount) else assert(not vis.parts.Opticsmount) end
   for _,scope in ipairs({"JAZZ_Reflex_Closed","JAZZ_Scope_12x","","JAZZ_Reflex_Closed",""}) do
    w:SetWeaponComponent('Scope',scope)
    if scope=="" then assert(not vis.parts.Opticsmount) else
     assert(vis.parts.Opticsmount.entity=="JAZZ_M14_OpticsMount" and IsValid(vis.parts.Opticsmount))
    end
   end
  ''')
 report['M14_mount_lifecycle']='PASS: empty, default ART, reflex, scope, remove, reinstall'
if a.mosin:
 lua.execute((root/'InventoryItem/Mosin.lua').read_text(encoding='utf-8'));lua.execute('Mosin=DefineClass.Mosin;setmetatable(Mosin,{__index=FirearmBase})')
 lua.execute(a.mosin.read_text(encoding='utf-8'))
 lua.execute('''
 local w=setmetatable({class="Mosin",components={},subweapons={},ComponentSlots=Mosin.ComponentSlots,Condition=73,ammo={Amount=3}},{__index=Mosin})
 local ammo=w.ammo
 for _,s in ipairs(w.ComponentSlots) do w.components[s.SlotType]=s.DefaultComponent or "" end
 for _,id in ipairs({"JAZZ_MosinObrez","JAZZ_MosinM38","JAZZ_Mosin1891"}) do
  w:SetWeaponComponent("Barrel",id)
  assert(w.Condition==73 and w.ammo==ammo and w.ammo.Amount==3)
  assert(w.DisplayName==(id=="JAZZ_Mosin1891" and Mosin.DisplayName or WeaponComponents[id].DisplayName))
 end
 ''')
 report['Mosin_name']='PASS: same instance, condition/ammo retained, reversible names'
# Names read from the live native host, not guessed from component slot IDs.
lua.globals().EntitySpots['Weapon_FNFAL']=lua.table_from({n:True for n in 'Barrel Bipod Center Hand_l_grip Handguard Launcher Magazine Mount1 Mount2 Mount3 Scope Side Stock Under Origin'.split()})
fal=(a.items.parent if a.items else root)/'InventoryItem/JAZZ_FNFAL_Tactical.lua'
lua.execute((fal if fal.exists() else root/'InventoryItem/JAZZ_FNFAL_Tactical.lua').read_text(encoding='utf-8-sig'))
for m in re.finditer(r"PlaceObj\('ModItemInventoryItemCompositeDef'",staged):
 end=matching(staged,staged.index('(',m.start()));block=staged[m.start():end]
 if re.search(r"'Id',\s*\"JAZZ_FNFAL_Tactical\"",block):
  serialized=lua.execute('return '+block)
  assert [v.SlotType for _,v in serialized.ComponentSlots.items()]==[v.SlotType for _,v in lua.globals().DefineClass.JAZZ_FNFAL_Tactical.ComponentSlots.items()]
  break
else:raise AssertionError('Serialized tactical FAL missing')
lua.execute('''
 local def=DefineClass.JAZZ_FNFAL_Tactical
 local w=setmetatable({class="JAZZ_FNFAL_Tactical",components={},subweapons={},ComponentSlots=def.ComponentSlots},{__index=FirearmBase})
 for _,s in ipairs(w.ComponentSlots) do w.components[s.SlotType]=s.DefaultComponent or "" end
 local vis=PlaceObject();vis:ChangeEntity(def.Entity);vis.weapon=w;vis.parts={};vis.components={};w.visual_obj=vis
 w:UpdateVisualObj(vis)
 assert(vis.parts.Mount1 and vis.parts.Mount1.entity=="WeaponAttA_MountFNFal_01")
 for _,scope in ipairs({"JAZZ_Reflex_Closed","JAZZ_Scope_12x","","JAZZ_CombatScope_ACOG",""}) do
  w:SetWeaponComponent("Scope",scope)
  assert(vis.parts.Mount1 and IsValid(vis.parts.Mount1))
 end
 assert(WeaponComponents.JAZZ_CarryHandle_AR15.Icon=="Mod/e6L4ECj/WeaponComponents/Optics/JAZZ_CarryHandle_AR15.png")
''')
report['FAL_rail']='PASS: permanent mount survives all scope switches/removal'
a.output.write_text(json.dumps(report,indent=2));print('PASS: complete component traversal',', '.join(report))
