# -*- coding: utf-8 -*-
"""Apply Unjam + suppressionPinned hotfix patches to items.lua (ACL-safe)."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ITEMS = ROOT / "items.lua"
text = ITEMS.read_text(encoding="utf-8")
orig = text

old_unjam_ui = '''\t\t\t\t\tGetUIState = function (self, units, args)
\t\t\t\t\t\tlocal unit = units[1]
\t\t\t\t\t\tlocal cost = self:GetAPCost(unit, args)
\t\t\t\t\t\tif cost < 0 then return "hidden" end
\t\t\t\t\t\t
\t\t\t\t\t\tlocal weapon = false
\t\t\t\t\t\tif args and args.pos then
\t\t\t\t\t\t\tweapon = unit:GetItemAtPackedPos(args.pos)
\t\t\t\t\t\telseif args and args.weapon then
\t\t\t\t\t\t\tweapon = unit:GetWeaponByDefIdOrDefault("Firearm", args and args.weapon, args and args.pos)
\t\t\t\t\t\tend\t
\t\t\t\t\t\t
\t\t\t\t\t\tif weapon then -- from Inventory
\t\t\t\t\t\t\tlocal jammed = false
\t\t\t\t\t\t\tif IsKindOf(weapon, "Firearm") and weapon.jammed and not weapon:IsCondition("Broken") then
\t\t\t\t\t\t\t\tjammed = true
\t\t\t\t\t\t\tend
\t\t\t\t\t\t\tif not jammed then return "hidden" end
\t\t\t\t\t\telse
\t\t\t\t\t\t\tlocal weapon1, weapon2 = unit:GetActiveWeapons()
\t\t\t\t\t\t\tlocal weaponJammed1, weaponJammed2 = false, false
\t\t\t\t\t\t\tif IsKindOf(weapon1, "Firearm") and weapon1.jammed and not weapon1:IsCondition("Broken") then
\t\t\t\t\t\t\t\tweaponJammed1 = true
\t\t\t\t\t\t\tend
\t\t\t\t\t\t\tif IsKindOf(weapon2, "Firearm") and weapon2.jammed and not weapon2:IsCondition("Broken") then
\t\t\t\t\t\t\t\tweaponJammed2 = true
\t\t\t\t\t\t\tend
\t\t\t\t\t\t\tif not weaponJammed1 and not weaponJammed2 then
\t\t\t\t\t\t\t\treturn "hidden"
\t\t\t\t\t\t\tend
\t\t\t\t\t\tend
\t\t\t\t\t\t
\t\t\t\t\t\tif not unit:UIHasAP(cost) then return "disabled", GetUnitNoApReason(unit) end
\t\t\t\t\t\t
\t\t\t\t\t\treturn "enabled"
\t\t\t\t\tend,'''

new_unjam_ui = '''\t\t\t\t\tGetUIState = function (self, units, args)
\t\t\t\t\t\tlocal unit = units[1]
\t\t\t\t\t\tlocal cost = self:GetAPCost(unit, args)
\t\t\t\t\t\tif cost < 0 then return "hidden" end
\t\t\t\t\t\t-- JAZZ-HOTFIX-003 / WEAPONS-002: durability is WeaponResource.
\t\t\t\t\t\t-- Vanilla IsCondition("Broken") can hide Unjam on a still-repairable jam.
\t\t\t\t\t\tlocal function can_unjam(weapon)
\t\t\t\t\t\t\tif not IsKindOf(weapon, "Firearm") or not weapon.jammed then
\t\t\t\t\t\t\t\treturn false
\t\t\t\t\t\t\tend
\t\t\t\t\t\t\tif weapon.GetWeaponResourceMax then
\t\t\t\t\t\t\t\treturn (weapon:GetWeaponResourceMax() or 0) > 1
\t\t\t\t\t\t\tend
\t\t\t\t\t\t\treturn not weapon:IsCondition("Broken")
\t\t\t\t\t\tend
\t\t\t\t\t\tlocal weapon = false
\t\t\t\t\t\tif args and args.pos then
\t\t\t\t\t\t\tweapon = unit:GetItemAtPackedPos(args.pos)
\t\t\t\t\t\telseif args and args.weapon then
\t\t\t\t\t\t\tweapon = unit:GetWeaponByDefIdOrDefault("Firearm", args and args.weapon, args and args.pos)
\t\t\t\t\t\tend
\t\t\t\t\t\tif weapon then -- from Inventory
\t\t\t\t\t\t\tif not can_unjam(weapon) then return "hidden" end
\t\t\t\t\t\telse
\t\t\t\t\t\t\tlocal weapon1, weapon2 = unit:GetActiveWeapons()
\t\t\t\t\t\t\tif not can_unjam(weapon1) and not can_unjam(weapon2) then
\t\t\t\t\t\t\t\treturn "hidden"
\t\t\t\t\t\t\tend
\t\t\t\t\t\tend
\t\t\t\t\t\tif not unit:UIHasAP(cost) then return "disabled", GetUnitNoApReason(unit) end
\t\t\t\t\t\treturn "enabled"
\t\t\t\t\tend,'''

if old_unjam_ui not in text:
    raise SystemExit("Unjam GetUIState block not found")
text = text.replace(old_unjam_ui, new_unjam_ui, 1)

old_tail = '''\t\t\t\t\tSortKey = 10,
\t\t\t\t\tgroup = "Default",
\t\t\t\t\tid = "Unjam",
\t\t\t\t}),'''
new_tail = '''\t\t\t\t\tShowIn = "CombatActions",
\t\t\t\t\tSortKey = 10,
\t\t\t\t\tgroup = "Default",
\t\t\t\t\tid = "Unjam",
\t\t\t\t}),'''
if old_tail not in text:
    raise SystemExit("Unjam SortKey/group tail not found")
if 'ShowIn = "CombatActions"' in text[text.find('id = "Unjam"') - 200 : text.find('id = "Unjam"')]:
    print("ShowIn already present near Unjam — skip tail")
else:
    text = text.replace(old_tail, new_tail, 1)

old_pinned = '''\t\t\t\t\t'OnAdded', function (self, obj)
\t\t\t\t\t\tobj:InterruptPreparedAttack()
\t\t\t\t\t\tlocal unitStance = obj.stance
\t\t\t\t\t\tif unitStance ~= "Prone" or not (obj:CanTakeCover()) then
\t\t\t\t\t\tobj:SetActionCommand("ChangeStance", nil, nil, "Prone")
\t\t\t\t\t\tend
\t\t\t\t\t\tif obj:CanTakeCover() then
\t\t\t\t\t\tobj:TakeCover();
\t\t\t\t\t\tobj:SetActionCommand("TakeCover", nil, nil, "Prone")
\t\t\t\t\t\tend
\t\t\t\t\t\t
\t\t\t\t\t\tobj.ActionPoints = Clamp(obj.ActionPoints, 0, 4*const.Scale.AP)
\t\t\t\t\t\t
\t\t\t\t\t\tif not obj:IsDead() then
\t\t\t\t\t\t                    if obj:IsMerc() then
\t\t\t\t\t\t                        PlayVoiceResponse(obj, "AIArchetypeScared")
\t\t\t\t\t\t                    else
\t\t\t\t\t\t                        PlayVoiceResponse(obj, "AILoseCover")
\t\t\t\t\t\t                    end
\t\t\t\t\t\t                end
\t\t\t\t\tend,'''

new_pinned = '''\t\t\t\t\t'OnAdded', function (self, obj)
\t\t\t\t\t\tif IsValid(obj) then
\t\t\t\t\t\t\tobj:InterruptPreparedAttack()
\t\t\t\t\t\t\t-- Permanent MG OW can leave StationedMachineGun if Interrupt raced
\t\t\t\t\t\t\t-- with SetActionCommand; strip residual prepared-attack state.
\t\t\t\t\t\t\tif g_Overwatch and g_Overwatch[obj] then
\t\t\t\t\t\t\t\tg_Overwatch[obj] = nil
\t\t\t\t\t\t\t\tMsg("OverwatchChanged")
\t\t\t\t\t\t\tend
\t\t\t\t\t\t\tif obj:HasStatusEffect("StationedMachineGun") then
\t\t\t\t\t\t\t\tobj:RemoveStatusEffect("StationedMachineGun")
\t\t\t\t\t\t\tend
\t\t\t\t\t\t\tobj:RecalcUIActions(true)
\t\t\t\t\t\tend
\t\t\t\t\t\tlocal unitStance = obj.stance
\t\t\t\t\t\tif unitStance ~= "Prone" or not (obj:CanTakeCover()) then
\t\t\t\t\t\t\tobj:SetActionCommand("ChangeStance", nil, nil, "Prone")
\t\t\t\t\t\tend
\t\t\t\t\t\tif obj:CanTakeCover() then
\t\t\t\t\t\t\tobj:TakeCover();
\t\t\t\t\t\t\tobj:SetActionCommand("TakeCover", nil, nil, "Prone")
\t\t\t\t\t\tend
\t\t\t\t\t\tobj.ActionPoints = Clamp(obj.ActionPoints, 0, 4*const.Scale.AP)
\t\t\t\t\t\tif not obj:IsDead() then
\t\t\t\t\t\t\tif obj:IsMerc() then
\t\t\t\t\t\t\t\tPlayVoiceResponse(obj, "AIArchetypeScared")
\t\t\t\t\t\t\telse
\t\t\t\t\t\t\t\tPlayVoiceResponse(obj, "AILoseCover")
\t\t\t\t\t\t\tend
\t\t\t\t\t\tend
\t\t\t\t\tend,'''

if old_pinned not in text:
    raise SystemExit("suppressionPinned OnAdded block not found in items.lua")
text = text.replace(old_pinned, new_pinned, 1)

old_begin = '''\t\t\t\t\t\tPlaceObj('UnitReaction', {
\t\t\t\t\t\t\tEvent = "OnBeginTurn",
\t\t\t\t\t\t\tHandler = function (self, target)
\t\t\t\t\t\t\t\tlocal ap = target.ActionPoints
\t\t\t\t\t\t\t\ttarget.ActionPoints = Clamp(target.ActionPoints, 0, 4*const.Scale.AP)
\t\t\t\t\t\t\t\ttarget:RemoveStatusEffect("FreeMove")
\t\t\t\t\t\t\tend,
\t\t\t\t\t\t\tparam_bindings = false,
\t\t\t\t\t\t}),'''
new_begin = '''\t\t\t\t\t\tPlaceObj('UnitReaction', {
\t\t\t\t\t\t\tEvent = "OnBeginTurn",
\t\t\t\t\t\t\tHandler = function (self, target)
\t\t\t\t\t\t\t\t-- Pinned units cannot keep prepared attacks (incl. permanent MG OW).
\t\t\t\t\t\t\t\ttarget:InterruptPreparedAttack()
\t\t\t\t\t\t\t\tif g_Overwatch and g_Overwatch[target] then
\t\t\t\t\t\t\t\t\tg_Overwatch[target] = nil
\t\t\t\t\t\t\t\t\tMsg("OverwatchChanged")
\t\t\t\t\t\t\t\tend
\t\t\t\t\t\t\t\tif target:HasStatusEffect("StationedMachineGun") then
\t\t\t\t\t\t\t\t\ttarget:RemoveStatusEffect("StationedMachineGun")
\t\t\t\t\t\t\t\tend
\t\t\t\t\t\t\t\ttarget.ActionPoints = Clamp(target.ActionPoints, 0, 4*const.Scale.AP)
\t\t\t\t\t\t\t\ttarget:RemoveStatusEffect("FreeMove")
\t\t\t\t\t\t\tend,
\t\t\t\t\t\t\tparam_bindings = false,
\t\t\t\t\t\t}),'''
# Only replace the pinned OnBeginTurn (first match after suppressionPinned Id).
pinned_id = text.find("'Id', \"suppressionPinned\"")
if pinned_id < 0:
    raise SystemExit("suppressionPinned Id not found")
# next PlaceObj CharacterEffect after pinned ends around Icon; search OnBeginTurn within 2500 chars
window = text[pinned_id : pinned_id + 3500]
if old_begin.strip() not in window and old_begin not in window:
    # try without assuming exact tabs from a narrower unique snippet
    if 'target:InterruptPreparedAttack()' in window and 'OnBeginTurn' in window:
        print("OnBeginTurn already interrupted — skip")
    else:
        raise SystemExit("suppressionPinned OnBeginTurn block not found")
else:
    # replace only inside the pinned window
    new_window = window.replace(old_begin, new_begin, 1)
    if new_window == window:
        raise SystemExit("OnBeginTurn replace failed")
    text = text[:pinned_id] + new_window + text[pinned_id + 3500 :]

if text == orig:
    raise SystemExit("no changes applied")
ITEMS.write_text(text, encoding="utf-8", newline="\n")
print("items.lua patched OK")
