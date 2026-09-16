"""Exercise real component setter against installed Mosin variants and reversals.

python docs/tools/_check_mosin_configurations.py --build <mosin build>
This checks data/method behavior in Lua; it is not a game renderer test.
"""
import argparse,re
from pathlib import Path
from lupa import LuaRuntime
from _integrate_sr3m import ROOT,matching
p=argparse.ArgumentParser();p.add_argument('--build',required=True,type=Path);p.add_argument('--game-root',type=Path);a=p.parse_args();stage=a.build/'mod-data-stage'
lua=LuaRuntime(unpack_returned_tuples=True)
lua.execute('''
WeaponComponents={};WeaponComponentEffects={};FirearmBase={};DefineClass={};const={Scale={AP=1000}};empty_table={}
function UndefineClass() end
function T(id,text) return text end
function IsValid(obj) return obj~=nil and obj~=false end
function ObjModified() end
function PlaceObj(class,props)
 local t={}
 for k,v in pairs(props or {}) do if type(k)=='string' then t[k]=v end end
 for i=1,#(props or {}),2 do t[props[i]]=props[i+1] end
 function t:ResolveValue(key)
  for _,p in ipairs(self.Parameters or {}) do if p.Name==key then return p.Value or 0 end end
 end
 if class=='ModItemWeaponComponent' then WeaponComponents[t.id]=t end
 if class=='ModItemWeaponComponentEffect' then
  t.ModificationType=t.ModificationType or 'Add';WeaponComponentEffects[t.id]=t
 end
 return t
end
''')
items=(ROOT/'items.lua').read_text(encoding='utf-8')
for m in re.finditer(r"PlaceObj\('ModItemWeaponComponentEffect'",items):
    end=matching(items,items.index('(',m.start()));lua.execute(items[m.start():end])
for m in re.finditer(r"PlaceObj\('ModItemWeaponComponent'",items):
    end=matching(items,items.index('(',m.start()));block=items[m.start():end]
    if re.search(r'id\s*=\s*"JAZZ_Mosin(?:1891|M38|Obrez)"',block):lua.execute(block)
lua.execute((ROOT/'InventoryItem/Mosin.lua').read_text(encoding='utf-8'))
lua.execute('Mosin=DefineClass.Mosin; Mosin.MaxAimActions=Mosin.MaxAimActions or 3')
setter=(ROOT/'Code/System_WeaponComponent_Set.lua').read_text(encoding='utf-8').split('-- MP40 is MagNormal-only')[0]
lua.execute(setter)
lua.execute('function FirearmBase:UpdateVisualObj(vis) end')
lua.execute((ROOT/'Code/Weapon_MosinModular.lua').read_text(encoding='utf-8'))
lua.execute('''
w=setmetatable({components={},subweapons={},mods={}}, {__index=Mosin})
for k,v in pairs(Mosin) do if type(v)=='number' then w['base_'..k]=v end end
function w:UnregisterReactions() end
function w:RegisterReactions() end
function w:RemoveModifiers(id)
 for prop,_ in pairs(self.mods[id] or {}) do self[prop]=self['base_'..prop] end
 self.mods[id]=nil
end
function w:AddModifier(id,prop,mul,add)
 self.mods[id]=self.mods[id] or {};self.mods[id][prop]=true
 self[prop]=math.floor(((self['base_'..prop] or 0)+add)*mul/1000+.5)
end
w.visual_obj={weapon=w,entity='MOSIN_1891'}
function w.visual_obj:GetEntity() return self.entity end
function w.visual_obj:ChangeEntity(entity) self.entity=entity end
''')
expected={
 'JAZZ_Mosin1891':(8000,40,50,66,13,3,55,'Long','MOSIN_1891'),
 'JAZZ_MosinM38':(7000,38,50,52,11,3,34,'Carbine','MOSIN_M38'),
 'JAZZ_MosinObrez':(5000,32,35,24,4,1,18,'Compact','MOSIN_Obrez'),
}
for id in ['JAZZ_Mosin1891','JAZZ_MosinM38','JAZZ_MosinObrez','JAZZ_Mosin1891','JAZZ_MosinObrez','JAZZ_MosinM38','JAZZ_Mosin1891']:
    lua.globals().w.SetWeaponComponent(lua.globals().w,'Barrel',id,False)
    w=lua.globals().w
    actual=tuple(w[k] for k in ['ShootAP','Damage','CritChanceScaled','WeaponRange','AimAccuracy','MaxAimActions','WeaponMass','WeaponSizeClass','Entity'])
    assert actual==expected[id],(id,actual,expected[id])
    assert w.visual_obj.entity==w.Entity
    assert w.Icon.endswith(w.Entity+'.png')
print('PASS: real JAZZ component setter, 7 transitions, AP/damage/crit/aim/range/mass/size/entity/icon; no accumulated modifiers.')

if a.game_root:
    src=a.game_root/'ModTools/Src/Lua'
    ui=(src/'UI/ModifyWeaponDlg.lua').read_text(encoding='utf-8')
    start=ui.index('function GetComponentBlocksAnyOfAttachedSlots(')
    lua.execute(ui[start:ui.index('\nfunction ',start+1)])
    weapon=(src/'Tactical/Weapon.lua').read_text(encoding='utf-8')
    start=weapon.index('function FirearmBase:GetNumModifySlotOptions(')
    lua.execute(weapon[start:weapon.index('\nfunction ',start+1)])
    lua.execute('''
    function table.find(t,v) for i,x in ipairs(t) do if x==v then return i end end end
    function table.find_value(t,k,v) for _,x in ipairs(t) do if x[k]==v then return x end end end
    -- A neutral scope isolates slot compatibility from optical stat modifiers.
    WeaponComponents.JAZZ_Scope_PU={Slot="Scope",ModificationEffects={},Visuals={}}
    local scope=table.find_value(w.ComponentSlots,"SlotType","Scope")
    assert(not WeaponComponents.JAZZ_Mosin1891.BlockSlots)
    for _,short in ipairs({"JAZZ_MosinM38","JAZZ_MosinObrez"}) do
      w:SetWeaponComponent("Barrel","JAZZ_Mosin1891")
      w:SetWeaponComponent("Scope","JAZZ_Scope_PU")
      local blocked,id=GetComponentBlocksAnyOfAttachedSlots(w,WeaponComponents[short])
      assert(blocked and id=="JAZZ_Scope_PU","UI must require scope removal before shortening")
      w:SetWeaponComponent("Barrel",short)
      assert(w.components.Scope=="","real setter must clear blocked scope")
      assert(FirearmBase.GetNumModifySlotOptions(w,scope)==0,"short variant offers scope")
      w:SetWeaponComponent("Barrel","JAZZ_Mosin1891")
      assert(FirearmBase.GetNumModifySlotOptions(w,scope)==1,"long variant lost scope option")
    end
    ''')
    print('PASS: native UI block check requires PU removal; M38/Obrez have zero Scope options; real setter clears blocked slot; long rifle restores scope option.')
