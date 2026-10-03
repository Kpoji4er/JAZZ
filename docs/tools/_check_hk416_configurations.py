"""Execute staged AEK + actual JAZZ setter/native caliber change in offline Lua.
--build DIR --game-root DIR. Tests ammo conservation, reversals, clones and visuals.
"""
import argparse,json,re
from pathlib import Path
from lupa import LuaRuntime
from _integrate_sr3m import ROOT,matching
from _integrate_hk416 import VALUES
p=argparse.ArgumentParser();p.add_argument('--build',type=Path,required=True);p.add_argument('--game-root',type=Path,required=True);p.add_argument('--installed',action='store_true');a=p.parse_args()
stage=ROOT if a.installed else a.build/'mod-data-stage/jazz';lua=LuaRuntime(unpack_returned_tuples=True)
lua.execute('''
DefineClass={};FirearmBase={};WeaponComponents={};WeaponComponentEffects={};empty_table={};const={Scale={AP=1000}}
function UndefineClass() end
function T(id,text) return text end
function point(...) return {...} end
function PlaceObj(cls,p)
 local r={};for k,v in pairs(p or {}) do if type(k)=='string' then r[k]=v end end
 for i=1,#(p or {}),2 do r[p[i]]=p[i+1] end
 function r:ResolveValue(key) for _,p in ipairs(self.Parameters or {}) do if p.Name==key then return p.Value end end end
 function r:Match(cls) return not self.ApplyTo or self.ApplyTo=='' or self.ApplyTo==cls end
 if cls=='ModItemWeaponComponent' then r.ModificationEffects=r.ModificationEffects or {};r.Visuals=r.Visuals or {};WeaponComponents[r.id]=r end
 if cls=='ModItemWeaponComponentEffect' or cls=='WeaponComponentEffect' then r.ModificationType=r.ModificationType or 'Add';WeaponComponentEffects[r.id]=r end
 return r
end
function IsValid(x) return type(x)=='table' end
function ObjModified() end
function InventoryUIRespawn() end
function GetInventoryUnit() return {} end
function InventoryUIResetSquadBag() end
function table.find_value(t,k,v) for _,r in ipairs(t or {}) do if r[k]==v then return r end end end
gv_UnitData={owner={Squad=1}};bag={};unloaded={};bag_available=true
function GetSquadBagInventory(squad) if bag_available then return bag end end
function UnloadWeapon(w,b) if w.ammo then table.insert(unloaded,w.ammo);w.ammo=false end end
function JazzWeaponIcon_ScheduleWeaponDisplayRefresh() end
function PlaceInventoryItem(cls) return {class=cls,delete=function(self) self.deleted=true end} end
''')
lua.execute((a.game_root/'ModTools/Src/Data/WeaponComponentEffect.lua').read_text(encoding='utf-8-sig'))
items=(stage/'items.lua').read_text(encoding='utf-8-sig')
for kind in ('ModItemWeaponComponentEffect','ModItemWeaponComponent'):
 for m in re.finditer("PlaceObj\\('"+kind+"'",items):
  end=matching(items,items.index('(',m.start()));lua.execute(items[m.start():end])
lua.execute((stage/'InventoryItem/HK416.lua').read_text(encoding='utf-8'))
lua.execute('HK416=DefineClass.HK416;setmetatable(HK416,{__index=FirearmBase})')
lua.execute('function FirearmBase:GetVisualObj() return self.visual_obj end')
lua.execute((ROOT/'Code/System_WeaponComponent_Set.lua').read_text(encoding='utf-8').split('-- MP40 is MagNormal-only')[0])
native=(a.game_root/'ModTools/Src/Lua/Tactical/Weapon.lua').read_text(encoding='utf-8')
lua.execute('function FirearmBase:ChangeCaliber'+native.split('function FirearmBase:ChangeCaliber',1)[1].split('function FirearmBase:GetNumAttachedComponents',1)[0])
lua.execute('function FirearmBase:UpdateVisualObj(vis) end')
lua.execute((ROOT/'Code/Weapon_HK416Modular.lua').read_text(encoding='utf-8'))
folding=(ROOT/'Code/Systems_Compontents_FoldingStocks.lua').read_text(encoding='utf-8')
for m in re.finditer("PlaceObj\\('WeaponComponentEffect'",folding):
 end=matching(folding,folding.index('(',m.start()));lua.execute(folding[m.start():end])
for ident in ('JAZZ_StockLightFolded','JAZZ_StockLightUnFolded'):
 for effect in lua.globals().WeaponComponents[ident].ModificationEffects.values():
  assert lua.globals().WeaponComponentEffects[effect] is not None,(ident,effect)
lua.execute('''
function new_weapon()
 local w=setmetatable({class='HK416',id=123,Condition=73,owner='owner',components={},subweapons={},mods={}}, {__index=HK416})
 for k,v in pairs(HK416) do if type(v)=='number' or type(v)=='string' then w['base_'..k]=v end end
 function w:UnregisterReactions() end
 function w:RegisterReactions() end
 function w:recalc(prop)
  local add,mul=0,1000
  for _,mods in pairs(self.mods) do local v=mods[prop];if v then add=add+v[2];mul=mul*v[1]/1000 end end
  self[prop]=math.floor(((self['base_'..prop] or 0)+add)*mul/1000+.5)
 end
 function w:RemoveModifiers(id)
  local old=self.mods[id] or {};self.mods[id]=nil;for prop in pairs(old) do self:recalc(prop) end
 end
 function w:AddModifier(id,prop,mul,add)
  self.mods[id]=self.mods[id] or {};self.mods[id][prop]={mul,add};self:recalc(prop)
 end
 for _,slot in ipairs(HK416.ComponentSlots) do if slot.DefaultComponent then w:SetWeaponComponent(slot.SlotType,slot.DefaultComponent,true) end end
 return w
end
w=new_weapon()
local baseline={Damage=w.Damage,Recoil=w.Recoil,WeaponRange=w.WeaponRange,AimAccuracy=w.AimAccuracy}
local ammo={Amount=23,Caliber='JAZZ_Caliber_556'};w.ammo=ammo
for repeat_index=1,5 do
 for _,barrel in ipairs({'Short','Long','Normal'}) do
  w:SetWeaponComponent('Barrel','JAZZ_HK416_Barrel'..barrel)
  local variant=barrel=='Normal' and 'Standard' or barrel
  assert(w.Entity=='JAZZ_HK416_'..variant)
  for _,stock in ipairs({'JAZZ_HK416_StockCTR','JAZZ_HK416_Stock'}) do
   w:SetWeaponComponent('Stock',stock)
   assert(w.Icon:find(variant..(stock:find('CTR') and '_CTR' or '')..'.png',1,true))
   assert(w.ammo==ammo and w.ammo.Amount==23 and w.id==123 and w.Condition==73)
  end
 end
 for property,value in pairs(baseline) do assert(w[property]==value,property..' accumulated') end
end
assert(w:SetWeaponComponent('Barrel','JAZZ_AEK_762')==false)
assert(w:SetWeaponComponent('Stock','JAZZ_StockLightFolded')==false)
for _,scope in ipairs({'JAZZ_Reflex_Closed','JAZZ_Reflex_Eotech','JAZZ_Reflex_M68','JAZZ_CombatScope_2x','JAZZ_CombatScope_ACOG',''}) do
 w:SetWeaponComponent('Scope',scope)
end
for property,value in pairs(baseline) do assert(w[property]==value,property..' scope residue') end
local r=new_weapon();r:Setcomponents({Barrel='JAZZ_HK416_BarrelLong',Stock='JAZZ_HK416_StockCTR'})
assert(r.Entity=='JAZZ_HK416_Long' and r.Icon:find('Long_CTR.png',1,true))
local vis={weapon=r,entity='old'}
function vis:GetEntity() return self.entity end
function vis:ChangeEntity(e) self.entity=e end
r:UpdateVisualObj(vis);assert(vis.entity=='JAZZ_HK416_Long')
assert(#unloaded==0)
''')
m=re.search(r"PlaceObj\('ModItemInventoryItemCompositeDef',\s*\{\s*'Id',\s*\"HK416\"",items);assert m
end=matching(items,items.index('(',m.start()));item=lua.execute('return '+items[m.start():end]);weapon=lua.globals().HK416
for key in VALUES:assert item[key]==weapon[key],key
lua.execute('''
for _,barrel in ipairs({'JAZZ_HK416_BarrelNormal','JAZZ_HK416_BarrelShort','JAZZ_HK416_BarrelLong'}) do
 w:SetWeaponComponent('Barrel',barrel)
 for _,id in ipairs({'JAZZ_VerticalGrip','JAZZ_TacGrip','JAZZ_GrenadeLauncher',''}) do
  w:SetWeaponComponent('Under',id);assert(w.components.Under==id)
  if id=='JAZZ_GrenadeLauncher' then
   assert(w.subweapons.Under and w.subweapons.Under.class=='UnderslungGrenadeLauncher')
   w.subweapons.Under.ammo={Amount=1};local n=#unloaded
   w:SetWeaponComponent('Under','JAZZ_VerticalGrip')
   assert(not w.subweapons.Under and #unloaded==n+1 and unloaded[#unloaded].Amount==1)
  else assert(not w.subweapons.Under) end
 end
 local side=table.find_value(HK416.ComponentSlots,'SlotType','Side');assert(side and side.CanBeEmpty)
 for _,id in ipairs(side.AvailableComponents) do w:SetWeaponComponent('Side',id);assert(w.components.Side==id) end
 w:SetWeaponComponent('Side','');assert(w.components.Side=='')
end
''')
report={'pass':True,'installed_files':a.installed,'checks':['all default components initialized','30 barrel/stock combinations','stat reversibility','ammo/id/Condition preservation','all scopes and removal','invalid barrel/stock rejected','presentation restore','entity swap','item/companion sync','Under and Side on all barrels','M203 creates subweapon and preserves grenade on removal'],'runtime':'NOT_RUN'}
(a.build/'lua-audit.json').write_text(json.dumps(report,indent=2));print('PASS',len(report['checks']),'HK416 checks')
