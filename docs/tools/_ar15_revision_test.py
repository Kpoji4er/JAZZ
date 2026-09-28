"""Offline behavioral regression for AR15 rail gating and fixed M14/AR15 parts.
Runs the real Lua setter/dialog guard in a minimal engine harness (not runtime QA).
"""
from pathlib import Path
import argparse
from lupa import LuaRuntime
root=Path(__file__).resolve().parents[2]
parser=argparse.ArgumentParser()
parser.add_argument('--setter',type=Path,default=root/'Code/System_WeaponComponent_Set.lua')
args=parser.parse_args()
lua=LuaRuntime(unpack_returned_tuples=True)
lua.execute('''
empty_table={}; FirearmBase={}; OnMsg={}; WeaponComponentEffects={}
WeaponComponents=setmetatable({}, {__index=function(t,k)
  if not k or k=="" then return nil end
  local v={ModificationEffects={},Visuals={}};rawset(t,k,v);return v
end})
function ObjModified() end
function IsKindOf() return true end
function sorted_pairs(t) return pairs(t) end
function FirearmBase:UnregisterReactions() end
function FirearmBase:RegisterReactions() end
function FirearmBase:RemoveModifiers(id) self.removed=id end
function FirearmBase:UpdateVisualObj() self.updated=true end
function FirearmBase:GetVisualObj() return nil end
ModifyWeaponDlg={CanModifySlot=function() return true end}
function JAZZ_IsHiddenModifyWeaponCraftOption() return false end
function JAZZ_FilterModifyWeaponCraftOptions(t) return t end
''')
lua.execute(args.setter.read_text(encoding='utf-8'))
text=(root/'Code/System_WeaponRemovableModify.lua').read_text(encoding='utf-8')
lua.execute(text[text.index('local VanillaCanModifySlot ='):text.index('-- CloseRange*')])
lua.execute('''
function weapon(class, hg, under, side)
 return setmetatable({class=class,components={Handguard=hg,Under=under,Side=side},
  subweapons={},applied_modifiers={}}, {__index=FirearmBase})
end
function allowed(w,slot,part)
 return ModifyWeaponDlg.CanModifySlot({context={weapon=w}},
  {SlotType=slot,AvailableComponents={part}},part)
end
for _,class in ipairs({"M4A1","M16A4"}) do
 local w=weapon(class,"JAZZ_Handguard","","")
 for _,slot in ipairs({"Side","Under"}) do
  assert(not allowed(w,slot,"attachment"))
  assert(w:SetWeaponComponent(slot,"attachment")==false)
  assert(w.components[slot]=="")
  assert(allowed(w,slot,""))
 end
 assert(allowed(w,"Scope","optic"))
 w:SetWeaponComponent("Handguard","JAZZ_Handguard_RIS","init")
 assert(w.components.Handguard=="JAZZ_Handguard_RIS")
 for _,slot in ipairs({"Side","Under"}) do
  assert(allowed(w,slot,"attachment"))
  w:SetWeaponComponent(slot,"attachment","init")
  assert(w.components[slot]=="attachment")
  assert(not allowed(w,"Handguard","JAZZ_Handguard"))
  assert(w:SetWeaponComponent("Handguard","JAZZ_Handguard")==false)
  w:SetWeaponComponent(slot,false,"init")
 end
 assert(allowed(w,"Handguard","JAZZ_Handguard"))
 w:SetWeaponComponent("Handgrip","JAZZ_Handgrip_Ergo","init")
 assert(w.components.Handgrip=="JAZZ_Handgrip_Default")
end
for _,class in ipairs({"M14SAW","M21","MK14EBR","JAZZ_M14_MkIII"}) do
 local w=weapon(class)
 w.components.Barrel="JAZZ_BarrelLong"
 w:SetWeaponComponent("Barrel","JAZZ_BarrelShort","init")
 assert(w.components.Barrel=="JAZZ_BarrelNormal")
 assert(w.removed=="JAZZ_BarrelLong")
end
local w=weapon("M16A4");w:SetWeaponComponent("Stock","JAZZ_StockLight","init")
assert(w.components.Stock=="JAZZ_StockNormal")
for _,class in ipairs({"M1A","GoldenGun","AK74"}) do
 local w=weapon(class,"JAZZ_Handguard")
 assert(allowed(w,"Under","attachment"))
 w:SetWeaponComponent("Barrel","JAZZ_BarrelShort","init")
 assert(w.components.Barrel=="JAZZ_BarrelShort")
end
for _,old in ipairs({"JAZZ_GrenadeLauncher_M14","JAZZ_TacGrip_M14","JAZZ_VerticalGrip_M14"}) do
 local w=weapon("M14SAW",nil,old)
 w:SetWeaponComponent("Under",old,"init")
 assert(w.components.Under=="" and w.removed==old)
 w:SetWeaponComponent("Under","JAZZ_Bipod_Under","init")
 assert(w.components.Under=="JAZZ_Bipod_Under")
 w:SetWeaponComponent("Under","","init")
 assert(w.components.Under=="" and w.removed=="JAZZ_Bipod_Under")
end
local legacy=weapon("M14SAW",nil,"JAZZ_TacGrip_M14")
local bipod=weapon("M14SAW",nil,"JAZZ_Bipod_Under")
local other=weapon("M21",nil,"JAZZ_TacGrip_M14")
local ebr=weapon("MK14EBR",nil,"JAZZ_GrenadeLauncher_M14")
local ebrGrip=weapon("MK14EBR",nil,"JAZZ_VerticalGrip_M14")
g_Units={{ForEachItem=function(self,kind,fn) fn(legacy);fn(bipod);fn(other);fn(ebr);fn(ebrGrip) end}}
OnMsg.LoadGame()
assert(legacy.components.Under=="" and legacy.removed=="JAZZ_TacGrip_M14")
assert(bipod.components.Under=="JAZZ_Bipod_Under")
assert(other.components.Under=="JAZZ_TacGrip_M14")
assert(ebr.components.Under=="" and ebr.removed=="JAZZ_GrenadeLauncher_M14")
assert(ebrGrip.components.Under=="JAZZ_VerticalGrip_M14")
ebr:SetWeaponComponent("Under","JAZZ_GrenadeLauncher_M14","init")
assert(ebr.components.Under=="")
''')
print('PASS: both installation orders, removals, receiver optics, fixed parts, unrelated weapons')
