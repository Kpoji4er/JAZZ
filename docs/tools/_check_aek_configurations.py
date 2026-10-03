"""Execute staged AEK + actual JAZZ setter/native caliber change in offline Lua.
--build DIR --game-root DIR. Tests ammo conservation, reversals, clones and visuals.
"""
import argparse,json,re
from pathlib import Path
from lupa import LuaRuntime
from _integrate_sr3m import ROOT,matching
from _integrate_aek import VALUES
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
''')
lua.execute((a.game_root/'ModTools/Src/Data/WeaponComponentEffect.lua').read_text(encoding='utf-8-sig'))
items=(stage/'items.lua').read_text(encoding='utf-8-sig')
for kind in ('ModItemWeaponComponentEffect','ModItemWeaponComponent'):
 for m in re.finditer("PlaceObj\\('"+kind+"'",items):
  end=matching(items,items.index('(',m.start()));lua.execute(items[m.start():end])
lua.execute((stage/'InventoryItem/AEK971.lua').read_text(encoding='utf-8'))
lua.execute('AEK971=DefineClass.AEK971;setmetatable(AEK971,{__index=FirearmBase})')
lua.execute((ROOT/'Code/System_WeaponComponent_Set.lua').read_text(encoding='utf-8').split('-- MP40 is MagNormal-only')[0])
native=(a.game_root/'ModTools/Src/Lua/Tactical/Weapon.lua').read_text(encoding='utf-8')
lua.execute('function FirearmBase:ChangeCaliber'+native.split('function FirearmBase:ChangeCaliber',1)[1].split('function FirearmBase:GetNumAttachedComponents',1)[0])
lua.execute('function FirearmBase:UpdateVisualObj(vis) end')
lua.execute((ROOT/'Code/Weapon_AEKModular.lua').read_text(encoding='utf-8'))
folding=(ROOT/'Code/Systems_Compontents_FoldingStocks.lua').read_text(encoding='utf-8')
for m in re.finditer("PlaceObj\\('WeaponComponentEffect'",folding):
 end=matching(folding,folding.index('(',m.start()));lua.execute(folding[m.start():end])
for ident in ('JAZZ_StockLightFolded','JAZZ_StockLightUnFolded'):
 for effect in lua.globals().WeaponComponents[ident].ModificationEffects.values():
  assert lua.globals().WeaponComponentEffects[effect] is not None,(ident,effect)
lua.execute('''
function new_weapon()
 local w=setmetatable({class='AEK971',id=123,Condition=73,owner='owner',components={},subweapons={},mods={}}, {__index=AEK971})
 for k,v in pairs(AEK971) do if type(v)=='number' or type(v)=='string' then w['base_'..k]=v end end
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
 w:SetWeaponComponent('Barrel','JAZZ_AEK_545',true)
 return w
end
w=new_weapon()
assert(w.Caliber=='JAZZ_Caliber_545' and w.Damage==26 and w.Recoil==13)
for i=1,5 do
 w.ammo={Caliber='JAZZ_Caliber_545',Amount=19};local count=#unloaded
 w:SetWeaponComponent('Barrel','JAZZ_AEK_762')
 assert(#unloaded==count+1 and unloaded[#unloaded].Amount==19 and not w.ammo)
 assert(w.Caliber=='JAZZ_Caliber_762x39' and w.Damage==30 and w.WeaponRange==42 and w.Recoil==17 and w.AimAccuracy==11)
 assert(w.Entity=='JAZZ_AEK973S' and w.id==123 and w.Condition==73)
 w.ammo={Caliber='JAZZ_Caliber_762x39',Amount=11};count=#unloaded
 w:SetWeaponComponent('Barrel','JAZZ_AEK_762');assert(#unloaded==count and w.ammo.Amount==11)
 w:SetWeaponComponent('Barrel','JAZZ_AEK_545')
 assert(#unloaded==count+1 and not w.ammo and w.Caliber=='JAZZ_Caliber_545')
 assert(w.Damage==26 and w.WeaponRange==50 and w.Recoil==13 and w.AimAccuracy==12)
end
w.owner=false;w.ammo={Amount=23};assert(w:SetWeaponComponent('Barrel','JAZZ_AEK_762')==false)
assert(w.components.Barrel=='JAZZ_AEK_545' and w.Caliber=='JAZZ_Caliber_545' and w.ammo.Amount==23)
w.owner='owner';bag_available=false;assert(w:SetWeaponComponent('Barrel','JAZZ_AEK_762')==false);assert(w.ammo.Amount==23);bag_available=true
local c=new_weapon();c.is_clone=true;c.ammo={Amount=17};local count=#unloaded
c:SetWeaponComponent('Barrel','JAZZ_AEK_762');assert(#unloaded==count and not c.ammo and w.ammo.Amount==23)
local r=new_weapon();r:Setcomponents({Barrel='JAZZ_AEK_762',Stock='JAZZ_StockLightFolded'})
assert(r.Entity=='JAZZ_AEK973S' and r.Icon:find('AEK973S_Folded.png',1,true))
function part() return {ChangeEntity=function(self,e) self.entity=e end} end
local v={weapon=r,entity='old',parts={Magazine=part(),Stock=part()}}
function v:GetEntity() return self.entity end
function v:ChangeEntity(e) self.entity=e end
r:UpdateVisualObj(v)
assert(v.entity=='JAZZ_AEK973S' and v.parts.Magazine.entity=='JAZZ_AEK973S_Magazine' and v.parts.Stock.entity=='JAZZ_AEK973S_StockFolded')
r:SetWeaponComponent('Stock','JAZZ_StockLightUnFolded');assert(r.Icon:find('AEK973S.png',1,true))
local scope_slot=table.find_value(AEK971.ComponentSlots,'SlotType','Scope');assert(scope_slot and scope_slot.CanBeEmpty)
for _,scope in ipairs(scope_slot.AvailableComponents) do
 local q=new_weapon();q:SetWeaponComponent('Scope',scope)
 assert(q.components.Scope==scope)
 q:SetWeaponComponent('Barrel','JAZZ_AEK_762');assert(q.components.Scope==scope and q.Damage==30)
 q:SetWeaponComponent('Barrel','JAZZ_AEK_545');assert(q.components.Scope==scope and q.Damage==26)
 q:SetWeaponComponent('Scope','');assert(q.components.Scope=='')
end
''')
m=re.search(r"PlaceObj\('ModItemInventoryItemCompositeDef',\s*\{\s*'Id',\s*\"AEK971\"",items);assert m
end=matching(items,items.index('(',m.start()));item=lua.execute('return '+items[m.start():end]);weapon=lua.globals().AEK971
for key in VALUES:assert item[key]==weapon[key],key
for obj in (item,weapon):
 scopes=[s for s in obj.ComponentSlots.values() if s.SlotType=='Scope'];assert len(scopes)==1 and len(scopes[0].AvailableComponents)==5
report={'pass':True,'installed_files':a.installed,'checks':['native caliber change','10 reversible conversions','ammo conservation','same-kit no-op','ownerless and missing bag reject','clone isolation','Condition/id preservation','component presentation restore','magazine/stock variant visuals','fold icon','item/companion fields'],'runtime':'NOT_RUN'}
(a.build/'lua-audit.json').write_text(json.dumps(report,indent=2));print('PASS',len(report['checks']),'AEK checks')
