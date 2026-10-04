"""Exercise real JA3 visual construction with staged/installed attachment fit.

--root DIR --game-root DIR. Mocks only engine objects, not visual selection.
"""
import argparse
import re
from pathlib import Path
from lupa import LuaRuntime
from _integrate_sr3m import ROOT, matching

p = argparse.ArgumentParser(description=__doc__)
p.add_argument('--root', type=Path, default=ROOT)
p.add_argument('--game-root', type=Path, required=True)
a = p.parse_args()
lua = LuaRuntime(unpack_returned_tuples=True)
lua.execute('''
FirearmBase={};DefineClass={};WeaponComponents={};empty_table={}
function T(id,text) return text end
function UndefineClass() end
function point(x,y,z) return {x=x,y=y,z=z} end
function IsValid(o) return type(o)=='table' and not o.dead end
function DoneObject(o) o.dead=true end
function sorted_pairs(t) return pairs(t) end
function table.copy(t) local r={};for k,v in pairs(t) do r[k]=v end;return r end
function table.find(t,k,v) for i,row in ipairs(t) do if row[k]==v then return i end end end
function PlaceObj(cls,p)
 local t={};for k,v in pairs(p or {}) do if type(k)=='string' then t[k]=v end end
 for i=1,#(p or {}),2 do t[p[i]]=p[i+1] end
 function t:IsGeneric() return not self.ApplyTo or self.ApplyTo=='' end
 function t:Match(id) return self:IsGeneric() or self.ApplyTo==id end
 if cls=='ModItemWeaponComponent' then t.Visuals=t.Visuals or {};WeaponComponents[t.id]=t end
 return t
end
function PlaceObject()
 local t={}
 function t:GetEntity() return self.entity end
 function t:ChangeEntity(e) self.entity=e end
 function t:GetSpotBeginIndex(s) return 1 end
 function t:Attach(o,s) o.parent=self;o.spot=s end
 function t:SetAttachOffset(v) self.offset=v end
 function t:SetAttachAxis(v) self.axis=v end
 function t:SetAttachAngle(v) self.angle=v end
 return t
end
function FirearmBase:UpdateColorMod() end
function new_weapon(cls)
 local w=setmetatable({class=cls,components={},subweapons={}}, {__index=_G[cls]})
 local vis=PlaceObject();vis.weapon=w;vis.parts={};vis.components={};w.visual_obj=vis
 return w,vis
end
''')
items = (a.root / 'items.lua').read_text(encoding='utf-8-sig')
for m in re.finditer(r"PlaceObj\('ModItemWeaponComponent'", items):
    end = matching(items, items.index('(', m.start()))
    lua.execute(items[m.start():end])
native = (a.game_root / 'ModTools/Src/Lua/Tactical/Weapon.lua').read_text(encoding='utf-8-sig')
lua.execute(native[native.index('SlotDependencies = {'):native.index('function FirearmBase:GetJamChance')])
for name, cls in [('HK416', 'HK416'), ('AEK', 'AEK971')]:
    lua.execute((ROOT / 'InventoryItem' / (cls + '.lua')).read_text(encoding='utf-8-sig'))
    lua.execute(cls + '=DefineClass.' + cls + ';setmetatable(' + cls + ',{__index=FirearmBase})')
    lua.execute((a.root / 'Code' / ('Weapon_' + name + 'Modular.lua')).read_text(encoding='utf-8-sig'))
lua.execute('''
local scopes={'JAZZ_Reflex_Closed','JAZZ_Reflex_Eotech','JAZZ_Reflex_M68','JAZZ_CombatScope_2x','JAZZ_CombatScope_ACOG'}
local w,v=new_weapon('AEK971')
for _,barrel in ipairs({'JAZZ_AEK_545','JAZZ_AEK_762','JAZZ_AEK_545'}) do
 w.components.Barrel=barrel
 local lift=barrel=='JAZZ_AEK_762' and 28 or 0
 for _,scope in ipairs(scopes) do
  w.components.Scope=scope
  for i=1,3 do
   w:UpdateVisualObj(v)
   assert(v.parts.Mount:GetEntity()=='WeaponAttA_MountAK47')
   assert(v.parts.Mount.offset.x==13 and v.parts.Mount.offset.z==-40+lift)
   assert(v.parts.Scope.offset.z==26+lift)
  end
  local old=v.parts.Mount;w.components.Scope='';w:UpdateVisualObj(v)
  assert(old.dead and not v.parts.Mount and not v.parts.Scope)
 end
end
local h,vis=new_weapon('HK416')
for _,barrel in ipairs({'JAZZ_HK416_BarrelNormal','JAZZ_HK416_BarrelShort','JAZZ_HK416_BarrelLong'}) do
 h.components.Barrel=barrel
 for _,id in ipairs({'JAZZ_GrenadeLauncher','JAZZ_VerticalGrip','JAZZ_TacGrip'}) do
  h.components.Under=id
  for i=1,3 do
   h:UpdateVisualObj(vis);assert(vis.parts.Under)
   if id=='JAZZ_GrenadeLauncher' then assert(vis.parts.Under.offset.x==60)
   else assert(not vis.parts.Under.offset) end
  end
 end
 for _,id in ipairs({'JAZZ_Flashlight','JAZZ_FlashlightOff','JAZZ_FlashlightDot','JAZZ_LaserDot','JAZZ_UVDot'}) do
  h.components.Side=id
  for i=1,3 do
   h:UpdateVisualObj(vis);assert(vis.parts.Side)
   assert(vis.parts.Side.axis.x==4096 and vis.parts.Side.angle==-5400)
  end
 end
 h.components.Side='';h.components.Under='';h:UpdateVisualObj(vis)
 assert(not vis.parts.Side and not vis.parts.Under)
end
-- AKM keeps its original adapter and receives no AEK placement code.
AKM={ComponentSlots={{SlotType='Scope'}}};setmetatable(AKM,{__index=FirearmBase})
local ak,akvis=new_weapon('AKM');ak.components.Scope='JAZZ_CombatScope_ACOG';ak:UpdateVisualObj(akvis)
assert(akvis.parts.Mount and not akvis.parts.Mount.offset and not akvis.parts.Scope.offset)
''')
print('PASS native visual selection, 5 AEK optics across caliber reversals, removal,')
print('     3 HK barrels, M203/grip isolation, 5 side devices, repeated updates, AKM unchanged')
