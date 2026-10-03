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
valid_entities={JAZZ_ImprovisedCuirass_Male=true,OriginalArmor=true,OtherArmor=true,OriginalBody=true,OtherBody=true}
AppearancePresets={Test={Armor='OriginalArmor',Body='OriginalBody'}}
function IsValid(o) return type(o)=='table' and not o.dead end
function IsKindOf(o,c) return o.kind==c end
function IsValidEntity(e) return valid_entities[e] or false end
function DoneObject(o) assert(not o.dead);o.dead=true end
Part={}
local point_meta={__add=function(a,b) return point(a.x+b.x,a.y+b.y,a.z+b.z) end}
function point(x,y,z) return setmetatable({x=x,y=y,z=z},point_meta) end
function Part:GetAttachOffset() return self.offset or point(0,0,0) end
function Part:SetAttachOffset(offset) self.offset=offset end
function Part:GetAttachSpot() return self.spot end
function Part:ChangeEntity(e) self.entity=e end
function Part:GetEntity() return self.entity end
function Part:ClearEnumFlags(f) self.cleared=f end
function Part:SetGameFlags(f) self.flags=f end
function PlaceObject(c) assert(c=='AppearanceObjectPart');return setmetatable({}, {__index=Part}) end
Unit={}
function Unit:GetItemInSlot(slot,kind) assert(kind=='Armor');if slot=='Torso' then return self.torso elseif slot=='Head' then return self.head end end
function Unit:GetGameFlags(flag) return 8 end
function Unit:GetSpotBeginIndex(spot) return spot=='Head' and 7 or 0 end
function Unit:Attach(part,spot) part.parent=self;part.spot=spot end
function Unit:GetEntity() return self.entity end
function Unit:GetStateText() return self.anim or 'idle' end
function Unit:GetAnimPhase() return self.phase or 0 end
function Unit:SetAnimPhase(c,p) self.phase=p end
function Unit:ChangeEntity(e,a) self.entity=e;self.anim=a end
function Unit:SetColorization(c) self.bodycolor=c end
function Unit:ApplyPartSpotAttachments(p)
 assert(p=='Armor' or p=='Hat' or p=='Body')
 local appearance=AppearancePresets[self.Appearance]
 self:Attach(self.parts[p],self:GetSpotBeginIndex(appearance[p..'Spot'] or 'Origin'))
end
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
 u.entity='OriginalBody'
 return u
end
''')
source=(ROOT/'Code/System_LegionArmorVisuals.lua').read_text(encoding='utf8');lua.execute(source)
import re
lua.globals().source_6b7_entity=re.search(r'JazzArmor_6b7Helm\s*=\s*\{\s*Male\s*=\s*"([^"]+)"',source).group(1)
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
valid_entities.JazzHat_SSh68=true
-- Resolve the current 6b7 asset independently of this torso regression suite.
local six=source_6b7_entity
valid_entities[six]=true
helm.head={class='JazzArmor_SovietHelm'};helm:UpdateItemAppearance()
assert(helm.parts.Hat.entity=='JazzHat_SSh68' and helm.parts.Hair.visible==false and not helm.parts.Hat.colors)
assert(helm.parts.Hat:GetAttachOffset().z==-40)
helm:UpdateItemAppearance();helm:UpdateItemAppearance()
assert(helm.parts.Hat:GetAttachOffset().z==-40, 'helmet offset must not accumulate')
local same=helm.parts.Hat;helm.head={class='JazzArmor_6b7Helm'};helm:UpdateItemAppearance()
assert(helm.parts.Hat.entity==six and same.dead and helm.parts.Hair.visible==false)
assert(helm.parts.Hat:GetAttachOffset().z==0, 'SSh68 fit must not leak to other hats')
assert(helm.parts.Hat:GetAttachSpot()==7, '6b7 must attach to Head despite baseline Origin')
assert(helm.parts.Armor:GetAttachSpot()==nil, 'unchanged armor must remain untouched')
local retained=helm.parts.Hat;helm:Attach(retained,0);helm:UpdateItemAppearance()
assert(helm.parts.Hat==retained and retained:GetAttachSpot()==7, 'repair cached helmet at Origin')
helm:Attach(retained,0);g_JAZZ_LegionHatParts=setmetatable({}, {__mode='k'});helm:UpdateItemAppearance()
assert(helm.parts.Hat==retained and retained:GetAttachSpot()==7, 'repair saved helmet at Origin')
helm.head=nil;OnMsg.ItemRemoved(helm,{},'Head')
assert(helm.parts.Hat==nil and helm.parts.Hair.visible==true)
valid_entities.BaselineHat=true;AppearancePresets.Test.Hat='BaselineHat'
local restored=makeunit('JAZZ_Legion_ArmorTest_6b7Helm','Male',nil)
restored.parts.Hat:ChangeEntity('BaselineHat');restored.head={class='JazzArmor_6b7Helm'};restored:UpdateItemAppearance()
restored.head=nil;restored:UpdateItemAppearance()
assert(restored.parts.Hat.entity=='BaselineHat' and restored.parts.Hat:GetAttachSpot()==0, 'restore original hat at preset Origin')
AppearancePresets.Test.Hat=nil
local merc=makeunit('Igor','Male','OriginalArmor');merc.torso={class='JazzArmor_FlakM1955'};merc.head={class='JazzArmor_PASGTHelm'}
local parmor,phat,phair=merc.parts.Armor,merc.parts.Hat,merc.parts.Hair.visible
merc:UpdateItemAppearance();assert(merc.parts.Armor==parmor and merc.parts.Hat==phat and merc.parts.Hair.visible==phair)
''')
lua.execute('''
for _,suffix in ipairs({'TireBrigantine','TireArmor','TwaronLight','TwaronMedium','TwaronFull','GuardianLight','GuardianMedium','GuardianFull','ZylonLight','ZylonMedium','ZylonFull','6B3','LeatherArmor'}) do
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
lua.execute('''
valid_entities.JAZZ_Chainmail_Male=true
local v=makeunit('JAZZ_Legion_ArmorTest_Chainmail','Male','OriginalArmor')
local hat=v.parts.Hat
v.torso={class='JazzArmor_Chainmail'};v:UpdateItemAppearance()
assert(v.entity=='JAZZ_Chainmail_Male' and not v.parts.Body)
assert(v.parts.Armor==nil and v.parts.Hat==hat)
v:UpdateItemAppearance();assert(v.entity=='JAZZ_Chainmail_Male')
v.torso={class='JazzArmor_ImprovisedCuirass'};v:UpdateItemAppearance()
assert(v.entity=='OriginalBody' and v.parts.Armor.entity=='JAZZ_ImprovisedCuirass_Male')
v.torso={class='JazzArmor_Chainmail'};v:UpdateItemAppearance()
assert(v.parts.Armor==nil)
v:ChangeEntity('OtherBody');v:UpdateItemAppearance();v.torso=nil;v:UpdateItemAppearance();assert(v.entity=='OtherBody')
v.torso={class='JazzArmor_Chainmail'};v:UpdateItemAppearance();g_JAZZ_LegionBodyParts=setmetatable({}, {__mode='k'})
v.torso=nil;v:UpdateItemAppearance();assert(v.entity=='OriginalBody')
-- Migration of the old Armor-slot entity on a saved unit.
local old=v.parts.Armor;old:ChangeEntity('JAZZ_Chainmail_Male');g_JAZZ_LegionArmorParts=setmetatable({}, {__mode='k'})
v.torso={class='JazzArmor_Chainmail'};v:UpdateItemAppearance()
assert(old.dead and v.parts.Armor==nil and v.entity=='JAZZ_Chainmail_Male')
valid_entities.JAZZ_Chainmail_Male=nil;v:UpdateItemAppearance();assert(v.entity=='OriginalBody')
valid_entities.JAZZ_Chainmail_Male=true
-- A preset flak vest must disappear beneath Chainmail, then return on removal.
local grenadier=makeunit('JAZZ_Legion_HeavyT2_Grenadier','Male','OriginalArmor')
grenadier.torso={class='JazzArmor_Chainmail'};grenadier:UpdateItemAppearance()
assert(grenadier.parts.Armor==nil)
g_JAZZ_LegionArmorParts=setmetatable({}, {__mode='k'})
grenadier:UpdateItemAppearance();assert(grenadier.parts.Armor==nil)
grenadier.torso=nil;grenadier:UpdateItemAppearance()
assert(grenadier.parts.Armor.entity=='OriginalArmor' and grenadier.entity=='OriginalBody')
grenadier.torso={class='JazzArmor_Chainmail'};grenadier:UpdateItemAppearance()
grenadier.parts.Armor=PlaceObject('AppearanceObjectPart');grenadier.parts.Armor:ChangeEntity('OriginalArmor')
grenadier:UpdateItemAppearance();assert(grenadier.parts.Armor==nil)
grenadier.torso={class='JazzArmor_ImprovisedCuirass'};grenadier:UpdateItemAppearance()
assert(grenadier.parts.Armor.entity=='JAZZ_ImprovisedCuirass_Male')
grenadier.torso=nil;grenadier:UpdateItemAppearance();assert(grenadier.parts.Armor.entity=='OriginalArmor')
for _,row in ipairs({{'Igor','Male'},{'JAZZ_Legion_Female','Female'}}) do
 local other=makeunit(row[1],row[2],'OriginalArmor');local original=other.entity
 other.torso={class='JazzArmor_Chainmail'};other:UpdateItemAppearance();assert(other.entity==original)
end
''')
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
    for f in ('items.lua','metadata.lua'):
        try:
            lua.compile((package/f).read_text(encoding='utf-8-sig'))
        except Exception:
            if package==ROOT and f=='items.lua':
                print('WARN: jazz/items.lua does not compile (pre-existing dirty state); 6B3 did not edit it')
            else:
                raise
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
function gear_slot_result(func, armor, slot, head)
 local u={slots={}}
 function u:TryEquip(items,slot_name,kind)
  local id=kind=='Armor' and (slot_name=='Head' and head or armor) or 'MP40'
  for i,v in ipairs(items) do if v.class==id then self.slots[slot_name]=v;table.remove(items,i);return true end end
 end
 function u:TryLoadAmmo(slot,kind,ammo) self.loaded=ammo end
 local items={};func(u,items)
 assert(u.slots[slot].class==armor and u.slots['Handheld A'].class=='MP40')
 if head then assert(u.slots.Head.class==head) end
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

six = 'JAZZ_6B3_Male'
six_item = block((ASSETS/'items.lua').read_text(encoding='utf8'),'ModItemEntity',"'entity_name', \""+six+'"')
assert six_item.ClassParents[1]=='CharacterArmorMale'
lua.execute((ASSETS/f'Entities/{six}.lua').read_text(encoding='utf8'))
assert lua.globals().EntityData[six].entity.class_parent=='CharacterArmorMale'
six_meta=(ASSETS/'metadata.lua').read_text(encoding='utf8')
assert '"'+six+'"' in six_meta and f'"Entities/{six}.lua"' in six_meta
six_tree=ET.parse(options.resources/f'{six}.ent')
assert six_tree.find('inherit').get('entity')=='Male' and not six_tree.findall('.//src')
for mesh in six_tree.findall('.//mesh'):
    assert (options.resources/mesh.get('file')).stat().st_size>0
for node in six_tree.findall('.//material'):
    mt=ET.parse(options.resources/node.get('file'))
    for tag in mt.getroot().iter():
        name=tag.get('Name')
        if name:
            assert name.startswith('JAZZ_6B3_')
            for sub in ('Textures','Textures/Fallbacks'):
                path=options.resources/sub/name;assert path.read_bytes()[:4]==b'DDS '
six_uid='JAZZ_Legion_ArmorTest_6B3'
six_rec=block((UNITS/'items.lua').read_text(encoding='utf8'),'ModItemUnitDataCompositeDef',"'Id', \""+six_uid+'"')
assert six_rec.Group=='JAZZ Tests'
lua.execute((UNITS/f'UnitData/{six_uid}.lua').read_text(encoding='utf8'))
six_def=lua.globals().DefineClass[six_uid]
lua.globals().gear_slot_result(six_rec.CustomEquipGear,'JazzArmor_6B3','Torso','JazzArmor_SovietHelm')
lua.globals().gear_slot_result(six_def.CustomEquipGear,'JazzArmor_6B3','Torso','JazzArmor_SovietHelm')
assert f'"UnitData/{six_uid}.lua"' in (UNITS/'metadata.lua').read_text(encoding='utf8')
assert (ROOT/'ArmorIcons'/'6b3.png').is_file()
print('PASS: 6B3 entity graph, Male inheritance, test-unit loadout, preserved icon')

# Leather carrier: both serialized and runtime definitions execute the same loadout.
leather = 'JAZZ_LeatherArmor_Male'
leather_uid = 'JAZZ_Legion_ArmorTest_LeatherArmor'
leather_item = block((ASSETS/'items.lua').read_text(encoding='utf8'), 'ModItemEntity', "'entity_name', \""+leather+'"')
assert leather_item.ClassParents[1] == 'CharacterArmorMale'
lua.execute((ASSETS/f'Entities/{leather}.lua').read_text(encoding='utf8'))
assert lua.globals().EntityData[leather].entity.class_parent == 'CharacterArmorMale'
leather_meta = (ASSETS/'metadata.lua').read_text(encoding='utf8')
assert f'"{leather}"' in leather_meta and f'"Entities/{leather}.lua"' in leather_meta
leather_tree = ET.parse(options.resources/f'{leather}.ent')
assert leather_tree.find('inherit').get('entity') == 'Male' and not leather_tree.findall('.//src')
for node in leather_tree.findall('.//mesh') + leather_tree.findall('.//material'):
    resource = options.resources/node.get('file')
    assert resource.is_file()
    if node.tag == 'material':
        for tag in ET.parse(resource).getroot().iter():
            name = tag.get('Name')
            if name:
                assert name.startswith('JAZZ_LeatherArmor_')
                for directory in ('Textures', 'Textures/Fallbacks'):
                    assert (options.resources/directory/name).read_bytes()[:4] == b'DDS '
leather_unit = block((UNITS/'items.lua').read_text(encoding='utf8'), 'ModItemUnitDataCompositeDef', "'Id', \""+leather_uid+'"')
assert leather_unit.Group == 'JAZZ Tests'
lua.execute((UNITS/f'UnitData/{leather_uid}.lua').read_text(encoding='utf8'))
for obj in (leather_unit, lua.globals().DefineClass[leather_uid]):
    assert obj.AppearancesList[1].Preset == 'LegionGoon' and obj.gender == 'Male'
    lua.globals().gear_slot_result(obj.CustomEquipGear, 'JazzArmor_LeatherArmor', 'Torso')
assert f'"UnitData/{leather_uid}.lua"' in (UNITS/'metadata.lua').read_text(encoding='utf8')
print('PASS: leather entity graph, native Male, serialized/runtime MP40+120 FMJ loadout')
