"""Execute staged/installed SCAR + actual JAZZ setter/native caliber change in offline Lua.
--build DIR --game-root DIR. Tests ammo conservation, reversals, clones and visuals.
"""
import argparse,json,re
from pathlib import Path
from lupa import LuaRuntime
from _integrate_sr3m import ROOT,matching
from _integrate_scar import VALUES
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
function IsKindOf(x,k) return x and (x.class==k or x.__ancestors and x.__ancestors[k]) end
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
''')
lua.execute((a.game_root/'ModTools/Src/Data/WeaponComponentEffect.lua').read_text(encoding='utf-8-sig'))
items=(stage/'items.lua').read_text(encoding='utf-8-sig')
for kind in ('ModItemWeaponComponentEffect','ModItemWeaponComponent'):
 for m in re.finditer("PlaceObj\\('"+kind+"'",items):
  end=matching(items,items.index('(',m.start()));lua.execute(items[m.start():end])
lua.execute((stage/'InventoryItem/SCAR.lua').read_text(encoding='utf-8'))
lua.execute('SCAR=DefineClass.SCAR;SCAR.__ancestors={Firearm=true,AssaultRifle=true};AssaultRifle={WeaponType="AssaultRifle",ImpactForce=1};Carbine={WeaponType="Carbine",ImpactForce=1};BattleRifle={WeaponType="BattleRifle",ImpactForce=2};setmetatable(SCAR,{__index=FirearmBase})')
lua.execute((ROOT/'Code/System_WeaponComponent_Set.lua').read_text(encoding='utf-8').split('-- MP40 is MagNormal-only')[0])
native=(a.game_root/'ModTools/Src/Lua/Tactical/Weapon.lua').read_text(encoding='utf-8')
lua.execute('function FirearmBase:ChangeCaliber'+native.split('function FirearmBase:ChangeCaliber',1)[1].split('function FirearmBase:GetNumAttachedComponents',1)[0])
lua.execute('function FirearmBase:UpdateVisualObj(vis) end')
lua.execute((ROOT/'Code/Weapon_SCARModular.lua').read_text(encoding='utf-8'))
folding=(ROOT/'Code/Systems_Compontents_FoldingStocks.lua').read_text(encoding='utf-8')
for m in re.finditer("PlaceObj\\('WeaponComponentEffect'",folding):
 end=matching(folding,folding.index('(',m.start()));lua.execute(folding[m.start():end])
for ident in ('JAZZ_SCAR_StockFolded','JAZZ_SCAR_Stock'):
 for effect in lua.globals().WeaponComponents[ident].ModificationEffects.values():
  assert lua.globals().WeaponComponentEffects[effect] is not None,(ident,effect)
lua.execute('''
function new_weapon()
 local w=setmetatable({class='SCAR',id=123,Condition=73,owner='owner',components={},subweapons={},mods={}}, {__index=SCAR})
 for k,v in pairs(SCAR) do if type(v)=='number' or type(v)=='string' then w['base_'..k]=v end end
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
 for _,s in ipairs(SCAR.ComponentSlots) do
  if s.DefaultComponent then w:SetWeaponComponent(s.SlotType,s.DefaultComponent,true) end
 end
 return w
end
local clean=new_weapon()
assert(clean.Damage==24 and clean.Recoil==16 and clean.Caliber=='JAZZ_Caliber_556')
for _,family in ipairs({'L','H'}) do
 for _,barrel in ipairs({'Normal','Short','Long'}) do
  local w=new_weapon()
  w:SetWeaponComponent('Conversion','JAZZ_SCAR_'..family)
  w:SetWeaponComponent('Barrel','JAZZ_SCAR_Barrel'..barrel)
  local h=family=='H';local short=barrel=='Short';local long=barrel=='Long'
  assert(w.Damage==(h and 33 or 24)-(short and 1 or 0))
  assert(w.WeaponRange==(h and 56 or 48)+(short and -8 or long and 8 or 0))
  assert(w.Recoil==(h and 27 or 16)+(short and 2 or 0))
  assert(w.Grouping==(h and 60 or 63)+(short and -3 or long and 3 or 0))
  assert(w.MagazineSize==(h and 20 or 30))
  assert(w.object_class==(short and 'Carbine' or 'AssaultRifle'))
  assert(clean.object_class=='AssaultRifle' and clean.__ancestors.AssaultRifle)
  w:SetWeaponComponent('Stock','JAZZ_SCAR_StockFolded');assert(w.Icon:find('_Folded.png',1,true))
  w:SetWeaponComponent('Stock','JAZZ_SCAR_Stock');assert(not w.Icon:find('_Folded.png',1,true))
 end
end
local w=new_weapon()
for i=1,5 do
 w.ammo={Caliber='JAZZ_Caliber_556',Amount=19};local count=#unloaded
 w:SetWeaponComponent('Conversion','JAZZ_SCAR_H')
 assert(#unloaded==count+1 and unloaded[#unloaded].Amount==19 and not w.ammo)
 assert(w.id==123 and w.Condition==73)
 w:SetWeaponComponent('Conversion','JAZZ_SCAR_SSR')
 assert(w.object_class=='BattleRifle' and w.Caliber=='JAZZ_Caliber_762x51')
 assert(w.Damage==33 and w.WeaponRange==64 and w.Grouping==63 and w.AimAccuracy==14)
 assert(#w.AvailableAttacks==1 and w.AvailableAttacks[1]=='SingleShot')
 w:SetWeaponComponent('Barrel','JAZZ_SCAR_BarrelShort');assert(w.components.Barrel=='JAZZ_SCAR_BarrelLong')
 w:SetWeaponComponent('Stock','JAZZ_SCAR_StockFolded');assert(w.components.Stock=='JAZZ_SCAR_Stock')
 w:SetWeaponComponent('Conversion','JAZZ_SCAR_L');w:SetWeaponComponent('Barrel','JAZZ_SCAR_BarrelNormal')
 assert(w.object_class=='AssaultRifle' and w.Damage==24 and w.MagazineSize==30 and w.Recoil==16)
end
w.owner=false;w.ammo={Amount=23}
assert(w:SetWeaponComponent('Conversion','JAZZ_SCAR_H')==false and w.ammo.Amount==23 and w.Caliber=='JAZZ_Caliber_556')
local c=new_weapon();c.is_clone=true;c.ammo={Amount=17};local count=#unloaded
c:SetWeaponComponent('Conversion','JAZZ_SCAR_H');assert(#unloaded==count and not c.ammo and w.ammo.Amount==23)
function part() return {ChangeEntity=function(self,e) self.entity=e end,SetAttachOffset=function(self,p) self.offset=p end,SetAttachAxis=function() end,SetAttachAngle=function() end} end
for _,family in ipairs({'L','H','SSR'}) do
 local r=new_weapon();r:SetWeaponComponent('Conversion','JAZZ_SCAR_'..family)
 local v={weapon=r,entity='old',parts={Magazine=part(),Stock=part(),Muzzle=part(),Side=part()}}
 function v:GetEntity() return self.entity end
 function v:ChangeEntity(e) self.entity=e end
 r:UpdateVisualObj(v)
 assert(v.entity==r.Entity)
 assert(v.parts.Magazine.entity=='JAZZ_SCAR_'..(family=='L' and 'L' or 'H')..'_Magazine')
 if family=='SSR' then assert(v.parts.Stock.entity=='JAZZ_SCAR_StockSSR') end
 local before={v.parts.Muzzle.offset[1],v.parts.Muzzle.offset[2],v.parts.Muzzle.offset[3]}
 r:UpdateVisualObj(v);assert(before[1]==v.parts.Muzzle.offset[1])
end
for _,s in ipairs(SCAR.ComponentSlots) do
 assert(#s.AvailableComponents>0)
 for _,id in ipairs(s.AvailableComponents) do assert(WeaponComponents[id],id) end
end
''')
m=re.search(r"PlaceObj\('ModItemInventoryItemCompositeDef',\s*\{\s*'Id',\s*\"SCAR\"",items);assert m
end=matching(items,items.index('(',m.start()));item=lua.execute('return '+items[m.start():end]);weapon=lua.globals().SCAR
for key in VALUES:assert item[key]==weapon[key],key
report={'pass':True,'runtime':'NOT_RUN','checks':['6 caliber/barrel configurations','SSR BattleRifle and single fire','SSR dependent slots','15 reversible kit changes','ammo conservation','ownerless guard','clone isolation','identity and condition','fold icons','visual parts and absolute offsets','item companion parity','slot references']}
(a.build/'lua-audit.json').write_text(json.dumps(report,indent=2));print('PASS',len(report['checks']),'SCAR checks')
