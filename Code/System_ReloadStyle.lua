-- JAZZ-WEAPONS-004: per-round reloads for tube, break-action, and revolver firearms.
-- CombatAction.Reload UI/AP is a full ModItem replace in items.lua; this file owns helpers + Unit.ReloadAction.
g_JAZZ_ReloadFlareHudWrapped = rawget(_G, "g_JAZZ_ReloadFlareHudWrapped") or false
-- Top-up must cap transfer at 1 round: vanilla Firearm:Reload fills MagSize in one call;
-- breaking UnitInventory:ReloadWeapon's stack loop alone does not limit rounds transferred.

local JazzPerRoundStyles = {
	Tube = true,
	Break = true,
	Revolver = true,
}

-- Optional 4th arg max_add: temporarily clamp the source stack so vanilla Reload
-- cannot pull more than that many rounds (used by WEAPONS-004 Top up).
local VanillaFirearmReload = Firearm.Reload
function Firearm:Reload(ammo, suspend_fx, delayed_fx, max_add)
	if not ammo or (ammo.Amount or 0) <= 0 then
		return false, false, false
	end
	local reserved = 0
	if max_add and max_add > 0 and ammo and ammo.Amount and ammo.Amount > max_add then
		reserved = ammo.Amount - max_add
		ammo.Amount = max_add
	end
	local prev_ammo, played_fx, change = VanillaFirearmReload(self, ammo, suspend_fx, delayed_fx)
	if reserved > 0 and ammo then
		ammo.Amount = (ammo.Amount or 0) + reserved
	end
	return prev_ammo, played_fx, change
end

local JazzReloadStyleByWeaponId = {
	Auto5 = "Tube",
	Auto5_quest = "Tube",
	DoubleBarrelShotgun = "Break",
	Ithaca = "Tube",
	M1897 = "Tube",
	R870 = "Tube",
	SPAS12 = "Tube",
	Stoeger = "Break",
	Winchester1894 = "Tube",
	Winchester_Quest = "Tube",
	Colt38Special = "Revolver",
	ColtAnaconda = "Revolver",
	ColtM1917 = "Revolver",
	ColtPeacemaker = "Revolver",
	Korth = "Revolver",
	MR73 = "Revolver",
	RSH12 = "Revolver",
	SWModel10 = "Revolver",
	SWModel19 = "Revolver",
	SWModel29 = "Revolver",
	TexRevolver = "Revolver",
	Webley = "Revolver",
}

function OnMsg.ClassesBuilt()
	for weapon_id, reload_style in pairs(JazzReloadStyleByWeaponId) do
		local weapon_class = g_Classes[weapon_id]
		if weapon_class then
			weapon_class.ReloadStyle = reload_style
		end
	end
end

function JazzHudReloadWeapons(unit)
	local list = {}
	if not unit or not unit.GetActiveWeapons then
		return list
	end
	local _, _, weapons = unit:GetActiveWeapons()
	for _, weapon in ipairs(weapons or empty_table) do
		if IsKindOf(weapon, "Firearm") and not IsKindOf(weapon, "HeavyWeapon") then
			list[#list + 1] = weapon
		end
	end
	return list
end

function JazzResolveReloadWeapon(unit, args)
	if not unit then
		return false
	end
	local weapon
	if args and args.item_id then
		local alternate_slot = unit.current_weapon == "Handheld A" and "Handheld B" or "Handheld A"
		weapon = unit:FindWeaponInSlotById(unit.current_weapon, args.item_id)
			or unit:FindWeaponInSlotById(alternate_slot, args.item_id)
			or unit:FindWeaponInSlotById("Inventory", args.item_id)
	end
	if not IsKindOf(weapon, "Firearm") and args and args.pos and unit.GetItemAtPackedPos then
		weapon = unit:GetItemAtPackedPos(args.pos)
	end
	if not IsKindOf(weapon, "Firearm") then
		-- Inventory drag reload passes weapon class + packed pos; pos can point at the
		-- wrong container/unit (UnitData vs Unit) and yield ammo or another item.
		weapon = unit.GetWeaponByDefIdOrDefault
			and unit:GetWeaponByDefIdOrDefault("Firearm", args and args.weapon, args and args.pos, args and args.item_id)
	end
	if not IsKindOf(weapon, "Firearm") then
		weapon = unit.GetWeaponByDefIdOrDefault
			and unit:GetWeaponByDefIdOrDefault("FlareGun", args and args.weapon, args and args.pos, args and args.item_id)
	end
	if not IsKindOf(weapon, "Firearm") then
		weapon = unit:GetActiveWeapons()
	end
	return IsKindOf(weapon, "Firearm") and weapon or false
end

function Firearm:GetReloadUnitAP()
	local magazine_size = Max(1, self.MagazineSize or 1)
	return Max(const.Scale.AP, DivCeil(self.ReloadAP, magazine_size))
end

function Firearm:IsPerRoundReload()
	local bullets = self.ammo and self.ammo.Amount or 0
	return JazzPerRoundStyles[self.ReloadStyle] and bullets > 0 and bullets < self.MagazineSize
end

local VanillaReloadAction = Unit.ReloadAction
function Unit:ReloadAction(action_id, cost_ap, args)
	local weapon = JazzResolveReloadWeapon(self, args)
	if not IsKindOf(weapon, "Firearm") or not weapon:IsPerRoundReload() then
		return VanillaReloadAction(self, action_id, cost_ap, args)
	end

	local ammo
	if args and args.target then
		ammo = self:GetItem(args.target)
		if not ammo then
			local bag = self.Squad and GetSquadBagInventory(self.Squad)
			ammo = bag and bag:GetItem(args.target)
		end
	end
	self:ReloadWeapon(weapon, ammo, args and args.delayed_fx, nil, "one_round")
end

local function Jazz_InstallReloadFlareHudWrap()
	local action = CombatActions and CombatActions.Reload
	if not action or rawget(action, "JazzFlareReloadWrapped") then
		return
	end
	local base_name = action.GetActionDisplayName
	action.GetActionDisplayName = function(self, units)
		local unit = units and units[1]
		if IsKindOf(unit, "Unit") then
			local weapons = JazzHudReloadWeapons(unit)
			local weapon = weapons[1]
			if IsKindOf(weapon, "Firearm") and weapon.IsPerRoundReload and weapon:IsPerRoundReload() then
				return T(990002013, "Top up")
			end
			local canChange = false
			for _, w in ipairs(weapons) do
				local ammoForWeapon = unit:GetAvailableAmmos(w, nil, "unique")
				local onlyAmmoIsCurrent = w.ammo and #ammoForWeapon == 1 and ammoForWeapon[1].class == w.ammo.class
				local fullMag = not w.ammo or w.ammo.Amount == w.MagazineSize
				canChange = canChange or (onlyAmmoIsCurrent and fullMag)
			end
			if canChange then
				return T(817996274899, "Change Ammo")
			end
			return self.DisplayName
		end
		return base_name and base_name(self, units)
	end
	action.UIBegin = function(self, units, args)
		local unit = units[1]
		local mode_dlg = GetInGameInterfaceModeDlg()
		if IsKindOf(mode_dlg, "IModeCommonUnitControl") then
			local weaponList = JazzHudReloadWeapons(unit)
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
					if isCurrent then
						table.insert(processedAmmo, 1, ammoEntry)
					else
						table.insert(processedAmmo, ammoEntry)
					end
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
				local ammoChoiceCallback = function(u2, ammoWrapped)
					self:Execute({ u2 }, { weapon = weaponWrapped.weaponIdx, target = ammoWrapped.ammo.class })
				end
				mode_dlg:ShowCombatActionTargetChoice(self, { u }, weaponWrapped.ammo, ammoChoiceCallback, "suppress_toggle")
			end
			mode_dlg:ShowCombatActionTargetChoice(self, units, processedList, weaponChoiceCallback)
		else
			self:Execute(units)
		end
	end
	rawset(action, "JazzFlareReloadWrapped", true)
	rawset(_G, "g_JAZZ_ReloadFlareHudWrapped", true)
end

function OnMsg.ModsReloaded()
	Jazz_InstallReloadFlareHudWrap()
end
function OnMsg.DataLoaded()
	Jazz_InstallReloadFlareHudWrap()
end
Jazz_InstallReloadFlareHudWrap()
