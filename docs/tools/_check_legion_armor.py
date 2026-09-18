"""Executable mocked lifecycle and isolated generated-graph checks for APPEAR-001."""
from pathlib import Path
import struct, xml.etree.ElementTree as ET
from lupa import LuaRuntime
from _integrate_sr3m import matching
ROOT=Path(__file__).resolve().parents[2];ASSETS=ROOT.parent/'jazz_assets';UNITS=ROOT.parent/'jazz-units'
import argparse
parser=argparse.ArgumentParser()
parser.add_argument('--resources',type=Path,default=ASSETS/'Entities')
parser.add_argument('--icon',type=Path,default=ROOT/'ArmorIcons/ImprovisedCuirass.png')
options=parser.parse_args()
lua=LuaRuntime(unpack_returned_tuples=True)
lua.execute('''
OnMsg={}; const={efCollision=1,efWalkable=2,efApplyToGrids=4,gofRealTimeAnim=8}
valid_entities={JAZZ_ImprovisedCuirass_Male=true,OriginalArmor=true,OtherArmor=true}
AppearancePresets={Test={Armor='OriginalArmor'}}
function IsValid(o) return type(o)=='table' and not o.dead end
function IsKindOf(o,c) return o.kind==c end
function IsValidEntity(e) return valid_entities[e] or false end
function DoneObject(o) assert(not o.dead);o.dead=true end
Part={}
function Part:ChangeEntity(e) self.entity=e end
function Part:GetEntity() return self.entity end
function Part:ClearEnumFlags(f) self.cleared=f end
function Part:SetGameFlags(f) self.flags=f end
function PlaceObject(c) assert(c=='AppearanceObjectPart');return setmetatable({}, {__index=Part}) end
Unit={}
function Unit:GetItemInSlot(slot,kind) assert(kind=='Armor');if slot=='Torso' then return self.torso elseif slot=='Head' then return self.head end end
function Unit:GetGameFlags(flag) return 8 end
function Unit:ApplyPartSpotAttachments(p) assert(p=='Armor' or p=='Hat');self.parts[p].parent=self end
function Unit:ColorizePart(p) self.parts[p].colorized=true end
function RGB(r,g,b) return r*65536+g*256+b end
function Part:SetColorizationMaterial(i,color,r,m) self.colors=self.colors or {};self.colors[i]=color end
function Part:SetVisible(v) self.visible=v end
base_calls=0
function Unit:UpdateItemAppearance() base_calls=base_calls+1;return 'base',nil,17 end
function UpdateItemAppearanceDelayed(u) u:UpdateItemAppearance() end
function makeunit(id,gender,baseline)
 local u=setmetatable({kind='Unit',unitdatadef_id=id,gender=gender,parts={},Appearance='Test'}, {__index=Unit})
 if baseline then local p=PlaceObject('AppearanceObjectPart');p:ChangeEntity(baseline);u.parts.Armor=p end
 local hat=PlaceObject('AppearanceObjectPart');hat:ChangeEntity('UnchangedHat');u.parts.Hat=hat
 local hair=PlaceObject('AppearanceObjectPart');hair:ChangeEntity('Hair');hair.visible=true;u.parts.Hair=hair
 return u
end
''')
source=(ROOT/'Code/System_LegionArmorVisuals.lua').read_text(encoding='utf8');lua.execute(source)
lua.execute('''
u=makeunit('JAZZ_Legion_ArmorTest','Male','OriginalArmor');old=u.parts.Armor;hat=u.parts.Hat
u.torso={class='JazzArmor_ImprovisedCuirass'}
local a,b,c=u:UpdateItemAppearance();assert(a=='base' and b==nil and c==17)
assert(old.dead and u.parts.Armor.entity=='JAZZ_ImprovisedCuirass_Male');assert(u.parts.Armor.cleared==7 and u.parts.Armor.flags==8)
assert(u.parts.Hat==hat);own=u.parts.Armor;u:UpdateItemAppearance();assert(u.parts.Armor==own)
u.torso=nil;OnMsg.ItemRemoved(u,{},'Torso');assert(own.dead and u.parts.Armor.entity=='OriginalArmor' and u.parts.Armor.colorized)
u.inventory={class='JazzArmor_ImprovisedCuirass'};u:UpdateItemAppearance();assert(u.parts.Armor.entity=='OriginalArmor')
for _,id in ipairs({'JAZZ_AME_01','Igor','LegionRaider','jazz_legion_test','JAZZ_LegionX'}) do
 local v=makeunit(id,'Male','OriginalArmor');v.torso={class='JazzArmor_ImprovisedCuirass'};local p=v.parts.Armor;v:UpdateItemAppearance();assert(v.parts.Armor==p)
end
local f=makeunit('JAZZ_Legion_Female','Female','OriginalArmor');f.torso={class='JazzArmor_ImprovisedCuirass'};local p=f.parts.Armor;f:UpdateItemAppearance();assert(f.parts.Armor==p)
u.torso={class='JazzArmor_ImprovisedCuirass'};valid_entities.JAZZ_ImprovisedCuirass_Male=nil;u:UpdateItemAppearance();assert(u.parts.Armor.entity=='OriginalArmor')
valid_entities.JAZZ_ImprovisedCuirass_Male=true;u:UpdateItemAppearance();local gone=u.parts.Armor;DoneObject(gone)
local replacement=PlaceObject('AppearanceObjectPart');replacement:ChangeEntity('OtherArmor');u.parts.Armor=replacement;u:UpdateItemAppearance();assert(replacement.dead)
u.torso=nil;u:UpdateItemAppearance();assert(u.parts.Armor.entity=='OtherArmor')
local n=makeunit('JAZZ_Legion_Empty','Male',nil);n.torso={class='JazzArmor_ImprovisedCuirass'};n:UpdateItemAppearance();n.torso=nil;n:UpdateItemAppearance();assert(n.parts.Armor==nil)
u.torso={class='JazzArmor_ImprovisedCuirass'};u:UpdateItemAppearance();g_JAZZ_LegionArmorParts=setmetatable({}, {__mode='k'});u.torso=nil;u:UpdateItemAppearance();assert(u.parts.Armor.entity=='OriginalArmor')
u.torso={class='JazzArmor_ImprovisedCuirass'};u:UpdateItemAppearance();u.torso={class='UnmappedArmor'};u:UpdateItemAppearance();assert(u.parts.Armor.entity=='OriginalArmor')
before_fn=Unit.UpdateItemAppearance;before_calls=base_calls;OnMsg.ClassesBuilt();OnMsg.ModsReloaded();u:UpdateItemAppearance();assert(base_calls==before_calls+1 and Unit.UpdateItemAppearance==before_fn)
''')
lua.execute(source);lua.execute("OnMsg.ModsReloaded();assert(Unit.UpdateItemAppearance==before_fn);u:UpdateItemAppearance()")
lua.execute('''
for _,name in ipairs({'EquipmentMale_FlackVest','EquipmentMale_InterceptorVest_01','EquipmentMale_InterceptorVest_02','FactionMale_Hat_05','Construction_Helmet_01','JungleCamp_GraveyardHelmet_02','FactionMale_Hat_09','EquipmentMale_WW2Helmet','FactionMale_Hat_08','FactionMale_Hat_10','FactionMale_Hat_11'}) do
 valid_entities[name]=true
end
local flak=makeunit('JAZZ_Legion_ArmorTest_FlakM1955','Male','OriginalArmor')
flak.torso={class='JazzArmor_FlakM1955'};flak:UpdateItemAppearance()
assert(flak.parts.Armor.entity=='EquipmentMale_FlackVest' and flak.parts.Armor.colors[1]==RGB(61,74,46))
flak.torso={class='JazzArmor_FlakM69'};flak:UpdateItemAppearance()
assert(flak.parts.Armor.entity=='EquipmentMale_FlackVest' and flak.parts.Armor.colors[1]==RGB(78,88,52))
local iba=makeunit('JAZZ_Legion_ArmorTest_IBA','Male','OriginalArmor')
iba.torso={class='JazzArmor_IBA'};iba:UpdateItemAppearance()
assert(iba.parts.Armor.entity=='EquipmentMale_InterceptorVest_02' and iba.parts.Armor.colors[2]==RGB(40,52,28))
iba.torso={class='JazzArmor_IBAFull'};iba:UpdateItemAppearance()
assert(iba.parts.Armor.entity=='EquipmentMale_InterceptorVest_02' and iba.parts.Armor.colors[1]==RGB(42,54,30))
local helm=makeunit('JAZZ_Legion_ArmorTest_PASGTHelm','Male','OriginalArmor');local oldhat=helm.parts.Hat
helm.head={class='JazzArmor_PASGTHelm'};helm:UpdateItemAppearance()
assert(oldhat.dead and helm.parts.Hat.entity=='FactionMale_Hat_08' and helm.parts.Hair.visible==false)
assert(helm.parts.Hat.colors[1]==RGB(61,74,46) and helm.parts.Armor.entity=='OriginalArmor')
local same=helm.parts.Hat;helm.head={class='JazzArmor_6b7Helm'};helm:UpdateItemAppearance()
assert(helm.parts.Hat.entity=='FactionMale_Hat_10' and same.dead and helm.parts.Hair.visible==false)
helm.head=nil;OnMsg.ItemRemoved(helm,{},'Head')
assert(helm.parts.Hat==nil and helm.parts.Hair.visible==true)
local merc=makeunit('Igor','Male','OriginalArmor');merc.torso={class='JazzArmor_FlakM1955'};merc.head={class='JazzArmor_PASGTHelm'}
local parmor,phat,phair=merc.parts.Armor,merc.parts.Hat,merc.parts.Hair.visible
merc:UpdateItemAppearance();assert(merc.parts.Armor==parmor and merc.parts.Hat==phat and merc.parts.Hair.visible==phair)
''')
lua.execute('''
for _,suffix in ipairs({'Chainmail','TireBrigantine','TireArmor','TwaronLight','TwaronMedium','TwaronFull','GuardianLight','GuardianMedium','GuardianFull','ZylonLight','ZylonMedium','ZylonFull'}) do
 local entity='JAZZ_'..suffix..'_Male';valid_entities[entity]=true
 local v=makeunit('JAZZ_Legion_ArmorTest_'..suffix,'Male','OriginalArmor')
 v.torso={class='JazzArmor_'..suffix};v:UpdateItemAppearance();assert(v.parts.Armor.entity==entity)
 local original=v.parts.Armor;v:UpdateItemAppearance();assert(v.parts.Armor==original)
 v.torso={class='JazzArmor_ImprovisedCuirass'};v:UpdateItemAppearance();assert(original.dead)
 v.torso=nil;v:UpdateItemAppearance();assert(v.parts.Armor.entity=='OriginalArmor')
 v.torso={class='JazzArmor_'..suffix};v:UpdateItemAppearance();g_JAZZ_LegionArmorParts=setmetatable({}, {__mode='k'})
 v.torso=nil;v:UpdateItemAppearance();assert(v.parts.Armor.entity=='OriginalArmor')
 local merc=makeunit('Igor','Male','OriginalArmor');merc.torso={class='JazzArmor_'..suffix}
 merc:UpdateItemAppearance();assert(merc.parts.Armor.entity=='OriginalArmor')
end
''')
# A new compiled Unit class can install a fresh CL method without rebasing a live wrapper.
lua.execute("Unit={UpdateItemAppearance=function() return 'newbase' end};OnMsg.ClassesBuilt();assert(g_JAZZ_LegionArmorHook.owner==Unit)")
print('PASS: mocked gating, equip/unequip, baseline, appearance rebuild, saved parts, idempotent reload, base return values')

lua.execute('''
DefineClass={};EntityData={}
function UndefineClass(id) DefineClass[id]=nil end
function T(id,text) return {id=id,text=text} end
function PlaceObj(c,p,ch)
 if c=='ModItemUnitDataCompositeDef' then assert(p[1], 'Composite ModItem requires property/value array') end
 local t={__class=c};for k,v in pairs(p or {}) do if type(k)=='string' then t[k]=v end end
 for i=1,#(p or {}),2 do t[p[i]]=p[i+1] end
 t.children=ch;return t
end
''')
def block(text,kind,needle):
    pos=text.index(needle);start=text.rfind("PlaceObj('"+kind+"'",0,pos);end=matching(text,text.index('(',start));return lua.execute('return '+text[start:end])
def native(v):
    if hasattr(v,'items'):return {k:native(x) for k,x in v.items()}
    return v
for package in (ROOT,ASSETS,UNITS):
    for f in ('items.lua','metadata.lua'):lua.compile((package/f).read_text(encoding='utf-8-sig'))
unit_id='JAZZ_Legion_ArmorTest';entity='JAZZ_ImprovisedCuirass_Male'
item=block((UNITS/'items.lua').read_text(encoding='utf8'),'ModItemUnitDataCompositeDef',"'Id', \""+unit_id+'"')
assert item.Group=='JAZZ Tests'
lua.execute((UNITS/f'UnitData/{unit_id}.lua').read_text(encoding='utf8'));definition=lua.globals().DefineClass[unit_id]
for k,v in definition.items():
    if not k.startswith('__') and k!='CustomEquipGear':assert native(item[k])==native(v),k
# Compare actual behavior of both serialized functions, including slot and ammo.
lua.execute('''
function PlaceInventoryItem(id) return {class=id} end
function gear_result(func)
 local u={slots={}}
 function u:TryEquip(items,slot,kind)
  local id=kind=='Armor' and 'JazzArmor_ImprovisedCuirass' or 'MP40'
  for i,v in ipairs(items) do if v.class==id then self.slots[slot]=v;table.remove(items,i);return true end end
 end
 function u:TryLoadAmmo(slot,kind,ammo) self.loaded=ammo end
 local items={};func(u,items)
 assert(u.slots.Torso.class=='JazzArmor_ImprovisedCuirass' and u.slots['Handheld A'].class=='MP40')
 assert(u.loaded=='JAZZ_AMMO_9x19_FMJ' and #items==1 and items[1].class==u.loaded and items[1].Amount==120)
end
''')
lua.globals().gear_result(item.CustomEquipGear);lua.globals().gear_result(definition.CustomEquipGear)
assert f'"UnitData/{unit_id}.lua"' in (UNITS/'metadata.lua').read_text(encoding='utf8')
asset_item=block((ASSETS/'items.lua').read_text(encoding='utf8'),'ModItemEntity',"'entity_name', \""+entity+'"')
assert asset_item.ClassParents[1]=='CharacterArmorMale'
lua.execute((ASSETS/f'Entities/{entity}.lua').read_text(encoding='utf8'));assert lua.globals().EntityData[entity].entity.class_parent=='CharacterArmorMale'
meta=(ASSETS/'metadata.lua').read_text(encoding='utf8');assert '"'+entity+'"' in meta and f'"Entities/{entity}.lua"' in meta
tree=ET.parse(options.resources/f'{entity}.ent');assert tree.find('inherit').get('entity')=='Male';assert not tree.findall('.//src')
for mesh in tree.findall('.//mesh'):assert (options.resources/mesh.get('file')).stat().st_size>0
for node in tree.findall('.//material'):
    mt=ET.parse(options.resources/node.get('file'))
    for tag in mt.getroot().iter():
        name=tag.get('Name')
        if name:
            assert name.startswith('JAZZ_ImprovisedCuirass_')
            for sub in ('Textures','Textures/Fallbacks'):
                path=options.resources/sub/name;assert path.read_bytes()[:4]==b'DDS '
    for prop in ('CastShadow','ReceiveShadow','DepthWrite'):assert mt.find(f'.//Property[@{prop}]').get(prop)=='1'
png=options.icon.read_bytes();assert png[:8]==b'\x89PNG\r\n\x1a\n';assert struct.unpack('>II',png[16:24])==(110,110);assert png[25]==6
rootmeta=(ROOT/'metadata.lua').read_text(encoding='utf8');assert rootmeta.index('Code/System_UnitAppearance.lua')<rootmeta.index('Code/System_LegionArmorVisuals.lua')
assert 'Code/System_LegionArmorVisuals.lua' in (ROOT/'items.lua').read_text(encoding='utf8')
print('PASS: isolated item/metadata/companion graph, loadout execution, HGM/material/DDS/fallbacks, Male inheritance, render icon RGBA 110x110')

from _install_vanilla_armor_visuals import rows
lua.execute('''
function gear_slot_result(func, armor, slot)
 local u={slots={}}
 function u:TryEquip(items,slot_name,kind)
  local id=kind=='Armor' and armor or 'MP40'
  for i,v in ipairs(items) do if v.class==id then self.slots[slot_name]=v;table.remove(items,i);return true end end
 end
 function u:TryLoadAmmo(slot,kind,ammo) self.loaded=ammo end
 local items={};func(u,items)
 assert(u.slots[slot].class==armor and u.slots['Handheld A'].class=='MP40')
 assert(u.loaded=='JAZZ_AMMO_9x19_FMJ' and #items==1 and items[1].class==u.loaded and items[1].Amount==120)
end
''')
units_items=(UNITS/'items.lua').read_text(encoding='utf8')
units_meta=(UNITS/'metadata.lua').read_text(encoding='utf8')
for item,slot in rows():
    uid='JAZZ_Legion_ArmorTest_'+item;armor='JazzArmor_'+item
    rec=block(units_items,'ModItemUnitDataCompositeDef',"'Id', \""+uid+'"')
    assert rec.Group=='JAZZ Tests'
    lua.execute((UNITS/f'UnitData/{uid}.lua').read_text(encoding='utf8'));definition=lua.globals().DefineClass[uid]
    for k,v in definition.items():
        if not k.startswith('__') and k not in ('CustomEquipGear','AppearancesList','Equipment'):
            assert native(rec[k])==native(v),(uid,k)
    lua.globals().gear_slot_result(rec.CustomEquipGear,armor,slot)
    lua.globals().gear_slot_result(definition.CustomEquipGear,armor,slot)
    assert f'"UnitData/{uid}.lua"' in units_meta
print('PASS: vanilla Torso/Head test-unit graph and Head/Torso loadouts')
