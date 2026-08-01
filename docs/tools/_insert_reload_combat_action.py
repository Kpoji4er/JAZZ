# -*- coding: utf-8 -*-
"""Insert full ModItemCombatAction Reload into items.lua CombatActions folder."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ITEMS = ROOT / "items.lua"
META = ROOT / "metadata.lua"

RELOAD_ITEM = r'''
			PlaceObj('ModItemCombatAction', {
				ActivePauseBehavior = "queue",
				Description = T(646737101780, --[[ModItemCombatAction Reload Description]] "<em>Reload</em> or <em>change</em> ammo."),
				DisplayName = T(642187794904, --[[ModItemCombatAction Reload DisplayName]] "Reload"),
				GetAPCost = function (self, unit, args)
					if unit:HasStatusEffect("ManningEmplacement") then return -1 end
					local weapon = JazzResolveReloadWeapon(unit, args)
					if weapon and weapon:IsPerRoundReload() then
						return weapon.jammed and -1 or weapon:GetReloadUnitAP()
					end
					if not weapon then
						if args and args.item_id then
							local alt_set = (unit.current_weapon == "Handheld A") and "Handheld B" or "Handheld A"
							weapon =
								unit:FindWeaponInSlotById(unit.current_weapon, args.item_id) or
								unit:FindWeaponInSlotById(alt_set, args.item_id) or
								unit:FindWeaponInSlotById("Inventory", args.item_id)
						end
						if not weapon then
							if args and args.pos then
								weapon = unit:GetItemAtPackedPos(args.pos)
							else
								weapon = unit:GetWeaponByDefIdOrDefault("Firearm", args and args.weapon)
							end
						end
					end
					return (weapon and not weapon.jammed) and weapon.ReloadAP or -1
				end,
				GetActionDisplayName = function (self, units)
					local unit = units[1]
					if not IsKindOf(unit, "Unit") then return end

					local weapon = unit:GetActiveWeapons("Firearm")
					if weapon and weapon:IsPerRoundReload() then
						return T(990002013, "Top up")
					end

					local w1, w2, weaponList = unit:GetActiveWeapons("Firearm")
					local canChange = false
					for i, w in ipairs(weaponList) do
						local ammoForWeapon = unit:GetAvailableAmmos(w, nil, "unique")
						local onlyAmmoIsCurrent = w.ammo and #ammoForWeapon == 1 and ammoForWeapon[1].class == w.ammo.class
						local fullMag = not w.ammo or w.ammo.Amount == w.MagazineSize
						canChange = canChange or (onlyAmmoIsCurrent and fullMag)
					end

					if canChange then
						return T(817996274899, "Change Ammo")
					else
						return self.DisplayName
					end
				end,
				GetTargets = function (self, units)
					local unit = units[1]
					local weapon = unit:GetActiveWeapons()
					return unit:GetAvailableAmmos(weapon)
				end,
				GetUIState = function (self, units, args)
					if not g_Combat and #units ~= 1 then return "hidden" end

					local unit = units[1]
					local cost = self:GetAPCost(unit, args)
					if cost < 0 then return "hidden" end
					if not unit:UIHasAP(cost) then return "disabled", GetUnitNoApReason(unit) end
					local availableWeaponsToReload = 0

					local errorReason
					local weapon
					if args and args.pos then
						weapon = unit:GetItemAtPackedPos(args.pos)
					elseif args and args.weapon then
						weapon = unit:GetWeaponByDefIdOrDefault("Firearm", args and args.weapon, args and args.pos)
					end
					if weapon then
						local weaponReloadOptions = GetReloadOptionsForWeapon(weapon, unit)
						if #weaponReloadOptions > 0 then
							availableWeaponsToReload = availableWeaponsToReload + 1
						end
					else
						local w1, w2, weaponList = unit:GetActiveWeapons()
						if not weaponList then return "enabled" end
						for i, w in ipairs(weaponList) do
							local canReload, err = IsWeaponAvailableForReload(w, unit:GetAvailableAmmos(w, nil, "unique"))
							errorReason = err
							if canReload then
								availableWeaponsToReload = availableWeaponsToReload + 1
							end
						end
					end
					if availableWeaponsToReload == 0 then return "disabled", errorReason end
					return "enabled"
				end,
				Icon = "UI/Icons/Hud/reload",
				IdDefault = "Reloaddefault",
				IsAimableAttack = false,
				QueuedBadgeText = T(871510388525, --[[ModItemCombatAction Reload QueuedBadgeText]] "RELOAD"),
				RequireState = "any",
				RequireWeapon = true,
				Run = function (self, unit, ap, ...)
					unit:SetActionCommand("ReloadAction", self.id, ap, ...)
				end,
				ShowIn = false,
				SortKey = 8,
				UIBegin = function (self, units, args)
					local unit = units[1]
					local mode_dlg = GetInGameInterfaceModeDlg()
					if IsKindOf(mode_dlg, "IModeCommonUnitControl") then
						local w1, w2, weaponList = unit:GetActiveWeapons("Firearm")
						local processedList = {}
						for i, w in ipairs(weaponList) do
							local text = T{535301054415, "<weaponName>", weaponName = w.DisplayName}
							local ammoForWeapon = unit:GetAvailableAmmos(w, nil, "unique")
							local noAmmo = #ammoForWeapon == 0
							if w.ammo == 0 then
								text = text .. T(642941753004, " (Empty)")
							end

							local onlyAmmoIsCurrent = w.ammo and #ammoForWeapon == 1 and ammoForWeapon[1].class == w.ammo.class
							local fullMag = not w.ammo or w.ammo.Amount == w.MagazineSize

							local processedAmmo = {}

							for _, a in ipairs(ammoForWeapon) do
								local isCurrent = w.ammo and a.class == w.ammo.class
								local ammoEntry = {
									DisplayName = isCurrent and T{541680584484, "Current: <DisplayName>", a} or a.DisplayName,
									ammo = a,
									disabled = w.ammo and isCurrent and fullMag,
									icon = a.Icon,
									uiCtx = a,
									rolloverTemplate = "RolloverInventory"
								}
								if isCurrent then table.insert(processedAmmo, 1, ammoEntry) else table.insert(processedAmmo, ammoEntry) end
							end

							processedList[#processedList + 1] = {
								DisplayName = text,
								weaponIdx = i,
								ammo = processedAmmo,
								disabled = noAmmo or (onlyAmmoIsCurrent and fullMag),
								icon = w.Icon,
								uiCtx = w,
								rolloverTemplate = "RolloverInventory"
							}
						end

						local weaponChoiceCallback = function(u, weaponWrapped)
							local ammoChoiceCallback = function(u, ammoWrapped)
								self:Execute({u}, { weapon = weaponWrapped.weaponIdx, target = ammoWrapped.ammo.class })
							end
							mode_dlg:ShowCombatActionTargetChoice(self, {u}, weaponWrapped.ammo, ammoChoiceCallback, "suppress_toggle")
						end

						mode_dlg:ShowCombatActionTargetChoice(self, units, processedList, weaponChoiceCallback)
					else
						self:Execute(units)
					end
				end,
				group = "Hidden",
				id = "Reload",
			}),
'''

ANCHOR = """\t\t\tPlaceObj('ModItemCode', {
\t\t\t\t'name', \"CombatActions\",
\t\t\t\t'CodeFileName', \"Code/CombatActions.lua\",
\t\t\t}),"""

META_ANCHOR = """\t\tPlaceObj('ModResourcePreset', {
\t\t\t'Class', \"CombatAction\",
\t\t\t'Id', \"Bandage\",
\t\t\t'ClassDisplayName', \"Combat Actions\",
\t\t}),"""

META_INSERT = """\t\tPlaceObj('ModResourcePreset', {
\t\t\t'Class', \"CombatAction\",
\t\t\t'Id', \"Bandage\",
\t\t\t'ClassDisplayName', \"Combat Actions\",
\t\t}),
\t\tPlaceObj('ModResourcePreset', {
\t\t\t'Class', \"CombatAction\",
\t\t\t'Id', \"Reload\",
\t\t\t'ClassDisplayName', \"Combat Actions\",
\t\t}),"""


def main() -> None:
    items = ITEMS.read_text(encoding="utf-8")
    if 'id = "Reload"' in items and "ModItemCombatAction Reload" in items:
        print("items.lua already has ModItemCombatAction Reload")
    else:
        if ANCHOR not in items:
            raise SystemExit("anchor ModItemCode CombatActions not found")
        # strip leading newline from RELOAD_ITEM for clean join
        block = RELOAD_ITEM.lstrip("\n")
        items = items.replace(ANCHOR, block + ANCHOR, 1)
        ITEMS.write_text(items, encoding="utf-8", newline="\n")
        print("inserted Reload ModItemCombatAction")

    meta = META.read_text(encoding="utf-8")
    if "'Id', \"Reload\"" in meta and "CombatAction" in meta[meta.find("'Id', \"Reload\"") - 80 : meta.find("'Id', \"Reload\"") + 40]:
        # check it's CombatAction Reload specifically
        if "Class', \"CombatAction\",\n\t\t\t'Id', \"Reload\"" in meta or "Class', \"CombatAction\",\r\n\t\t\t'Id', \"Reload\"" in meta:
            print("metadata already has CombatAction Reload resource")
        else:
            pass
    if 'Class\', "CombatAction",\n\t\t\t\'Id\', "Reload"' not in meta and "Class', \"CombatAction\",\n\t\t\t'Id', \"Reload\"" not in meta:
        if META_ANCHOR not in meta:
            raise SystemExit("metadata Bandage anchor not found")
        meta = meta.replace(META_ANCHOR, META_INSERT, 1)
        META.write_text(meta, encoding="utf-8", newline="\n")
        print("inserted metadata ModResourcePreset Reload")
    else:
        print("metadata Reload resource ok")


if __name__ == "__main__":
    main()
