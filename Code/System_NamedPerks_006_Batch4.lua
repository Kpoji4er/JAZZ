-- JAZZ-UNITS-006 §B Batch4 (JA12 stubs): Flo / Static / Cougar + cheap hooks.
-- Install is called from System_NamedPerks_006.lua (do not overwrite OnMsg here).

g_JAZZ_NamedPerks006Batch4Wrapped = rawget(_G, "g_JAZZ_NamedPerks006Batch4Wrapped") or false
g_JAZZ_FloBuySellBase_BR = rawget(_G, "g_JAZZ_FloBuySellBase_BR") or false
g_JAZZ_FloBuySellBase_Cash = rawget(_G, "g_JAZZ_FloBuySellBase_Cash") or false
g_JAZZ_StaticPartsBase_ModCost = rawget(_G, "g_JAZZ_StaticPartsBase_ModCost") or false
g_JAZZ_StaticPartsBase_ItemsCalc = rawget(_G, "g_JAZZ_StaticPartsBase_ItemsCalc") or false
g_JAZZ_PushUnitAlertBase_B4 = rawget(_G, "g_JAZZ_PushUnitAlertBase_B4") or false
g_JAZZ_RecoilProfileBase_B4 = rawget(_G, "g_JAZZ_RecoilProfileBase_B4") or false

local function lIsPlayerSquadUnit(unit)
	if not unit then
		return false
	end
	local squad_id = unit.Squad
	local squad = squad_id and gv_Squads and gv_Squads[squad_id]
	return squad and (squad.Side == "player1" or squad.Side == "player2")
end

function Jazz_SquadHasFlo(unit_or_nil)
	-- Flo in any player merc squad (active campaign roster).
	for _, squad in pairs(gv_Squads or empty_table) do
		if squad and (squad.Side == "player1" or squad.Side == "player2") then
			for _, uid in ipairs(squad.units or empty_table) do
				local u = gv_UnitData and gv_UnitData[uid]
				if not u and g_Units then
					u = g_Units[uid]
				end
				if u and HasPerk(u, "Jazz_Perk_Flo") and not (u.IsDead and u:IsDead()) then
					return true
				end
			end
		end
	end
	-- Combat map units fallback.
	for _, u in ipairs(g_Units or empty_table) do
		if IsValid(u) and lIsPlayerSquadUnit(u) and HasPerk(u, "Jazz_Perk_Flo") and not u:IsDead() then
			return true
		end
	end
	return false
end

function Jazz_StaticPartsDiscountPercent(unit)
	if not unit or not HasPerk(unit, "Jazz_Perk_Static") then
		return 0
	end
	local lvl = 1
	if unit.GetLevel then
		lvl = unit:GetLevel() or 1
	end
	return Clamp((tonumber(lvl) or 1) * 5, 0, 25)
end

function Jazz_StaticApplyPartsDiscount(unit, parts)
	if type(parts) ~= "number" or parts <= 0 then
		return parts
	end
	local disc = Jazz_StaticPartsDiscountPercent(unit)
	if disc <= 0 then
		return parts
	end
	return Max(0, MulDivRound(parts, 100 - disc, 100))
end

local KULBA_US_AUTOS = {
	M3GreaseGun = true,
	Thompson = true,
	M4A1 = true,
	M4Commando = true,
	CAR15 = true,
	AR15 = true,
	M16A1 = true,
	M16A2 = true,
	M16A4 = true,
	BAR = true,
	M60 = true,
	M60E3 = true,
	M60E4 = true,
	M14SAW = true,
	M1A = true,
	Mini14 = true,
	GoldenGun = true,
}

function Jazz_KulbaIsUSAuto(weapon)
	if not weapon then
		return false
	end
	local class_id = weapon.class or weapon.Id or weapon.id
	return class_id and KULBA_US_AUTOS[class_id] or false
end

function Jazz_ApplyGromSuppression(attacker, suppressionbonus)
	if not attacker or not HasPerk(attacker, "Jazz_Perk_Grom") then
		return suppressionbonus
	end
	local w = attacker.GetActiveWeapons and attacker:GetActiveWeapons()
	if not w then
		return suppressionbonus
	end
	if IsKindOf(w, "GrenadeLauncher")
		or IsKindOf(w, "Mortar")
		or IsKindOf(w, "RocketLauncher")
		or IsKindOf(w, "MissileLauncher")
		or (w.WeaponType == "GrenadeLauncher")
		or (w.WeaponType == "Mortar")
		or (w.WeaponType == "MissileLauncher")
		or (w.WeaponType == "RocketLauncher")
	then
		return (suppressionbonus or 100) * 2
	end
	return suppressionbonus
end

function Jazz_ApplyIggyMortarScatter(attacker, scatter)
	if not attacker or not HasPerk(attacker, "Jazz_Perk_Iggy") then
		return scatter
	end
	if type(scatter) ~= "number" then
		return scatter
	end
	return MulDivRound(scatter, 67, 100)
end

function Jazz_CougarOnStealthKill(attacker)
	if not attacker or not HasPerk(attacker, "Jazz_Perk_Cougar") then
		return
	end
	if attacker:GetEffectValue("Jazz_CougarInspiredUsed") then
		return
	end
	if CharacterEffectDefs and CharacterEffectDefs.Inspired then
		attacker:AddStatusEffect("Inspired")
		attacker:SetEffectValue("Jazz_CougarInspiredUsed", true)
	end
end

function Jazz_InstallNamedPerks006Batch4()
	if rawget(_G, "g_JAZZ_NamedPerks006Batch4Wrapped") then
		return
	end

	-- Flo: Bobby Ray buy −12%.
	local br = rawget(_G, "BobbyRayStoreGetEntryCost")
	if type(br) == "function" and not rawget(_G, "g_JAZZ_FloBuySellBase_BR") then
		rawset(_G, "g_JAZZ_FloBuySellBase_BR", br)
		rawset(_G, "BobbyRayStoreGetEntryCost", function(entry)
			local cost = g_JAZZ_FloBuySellBase_BR(entry)
			if type(cost) == "number" and Jazz_SquadHasFlo() then
				cost = MulDivRound(cost, 88, 100)
			end
			return cost
		end)
	end

	-- Flo: cash-in / sell valuables +12%.
	local cash = rawget(_G, "CashInItem")
	if type(cash) == "function" and not rawget(_G, "g_JAZZ_FloBuySellBase_Cash") then
		rawset(_G, "g_JAZZ_FloBuySellBase_Cash", cash)
		rawset(_G, "CashInItem", function(inventory, slot_name, item, amount, dontLog)
			if Jazz_SquadHasFlo() and item and type(item.Cost) == "number" then
				local old = item.Cost
				item.Cost = MulDivRound(old, 112, 100)
				g_JAZZ_FloBuySellBase_Cash(inventory, slot_name, item, amount, dontLog)
				-- Item may already be DoneObject()'d; only restore if still alive.
				if IsValid(item) then
					item.Cost = old
				end
				return
			end
			return g_JAZZ_FloBuySellBase_Cash(inventory, slot_name, item, amount, dontLog)
		end)
	end

	-- Static: weapon-mod Parts −5%×Level (cap −25%).
	if ModifyWeaponDlg and type(ModifyWeaponDlg.GetChangesCost) == "function" and not rawget(_G, "g_JAZZ_StaticPartsBase_ModCost") then
		rawset(_G, "g_JAZZ_StaticPartsBase_ModCost", ModifyWeaponDlg.GetChangesCost)
		function ModifyWeaponDlg:GetChangesCost(slotFilter, placedComponentOverride)
			local costs, anyChanged, canAfford, canAffordPerCost =
				g_JAZZ_StaticPartsBase_ModCost(self, slotFilter, placedComponentOverride)
			local owner = self.context and self.context.owner
			local unit = owner
			if type(JazzGetOwnerUnit) == "function" then
				unit = JazzGetOwnerUnit(owner) or owner
			elseif type(owner) == "string" and gv_UnitData then
				unit = gv_UnitData[owner] or g_Units and g_Units[owner]
			end
			if costs and costs.Parts then
				costs.Parts = Jazz_StaticApplyPartsDiscount(unit, costs.Parts)
			end
			return costs, anyChanged, canAfford, canAffordPerCost
		end
	end

	-- Static: repair/craft Parts estimate.
	local calc = rawget(_G, "SectorOperation_ItemsCalcRes")
	if type(calc) == "function" and not rawget(_G, "g_JAZZ_StaticPartsBase_ItemsCalc") then
		rawset(_G, "g_JAZZ_StaticPartsBase_ItemsCalc", calc)
		rawset(_G, "SectorOperation_ItemsCalcRes", function(sector_id, operation_id)
			local parts = g_JAZZ_StaticPartsBase_ItemsCalc(sector_id, operation_id)
			if type(parts) ~= "number" or parts <= 0 then
				return parts
			end
			local mercs = GetOperationProfessionals and GetOperationProfessionals(sector_id, operation_id) or empty_table
			local best = 0
			for _, merc in ipairs(mercs) do
				best = Max(best, Jazz_StaticPartsDiscountPercent(merc))
			end
			if best > 0 then
				parts = Max(0, MulDivRound(parts, 100 - best, 100))
			end
			return parts
		end)
	end

	-- Cougar: shot noise −33%.
	local alert = rawget(_G, "PushUnitAlert")
	if type(alert) == "function" and not rawget(_G, "g_JAZZ_PushUnitAlertBase_B4") then
		rawset(_G, "g_JAZZ_PushUnitAlertBase_B4", alert)
		rawset(_G, "PushUnitAlert", function(trigger_type, ...)
			if trigger_type == "noise" then
				local actor, radius, soundName = ...
				if IsKindOf(actor, "Unit") and HasPerk(actor, "Jazz_Perk_Cougar") and type(radius) == "number" then
					radius = MulDivRound(radius, 67, 100)
					return g_JAZZ_PushUnitAlertBase_B4(trigger_type, actor, radius, soundName)
				end
			end
			return g_JAZZ_PushUnitAlertBase_B4(trigger_type, ...)
		end)
	end

	-- Kulba: US autos −50% recoil via JAZZ recoil profile.
	local recoil = rawget(_G, "JAZZ_CTHGetRecoilProfile")
	if type(recoil) == "function" and not rawget(_G, "g_JAZZ_RecoilProfileBase_B4") then
		rawset(_G, "g_JAZZ_RecoilProfileBase_B4", recoil)
		rawset(_G, "JAZZ_CTHGetRecoilProfile", function(weapon, attacker, stance, action, attack_args)
			local profile = g_JAZZ_RecoilProfileBase_B4(weapon, attacker, stance, action, attack_args)
			if profile and attacker and HasPerk(attacker, "Jazz_Perk_Kulba") and Jazz_KulbaIsUSAuto(weapon) then
				profile.effective_recoil = (profile.effective_recoil or 0) * 0.5
				profile.perk_factor = (profile.perk_factor or 1) * 0.5
				if profile.retention and JAZZ_CTH_FACTOR_SCALE then
					local retention = Clamp(1 - profile.effective_recoil * 1.0 / 100, 0.15, 1)
					profile.retention = JAZZ_CTHRound(retention * JAZZ_CTH_FACTOR_SCALE)
				end
			end
			return profile
		end)
	end

	rawset(_G, "g_JAZZ_NamedPerks006Batch4Wrapped", true)
end

function Jazz_NamedPerks006Batch4OnCombatStart()
	for _, u in ipairs(g_Units or empty_table) do
		if IsValid(u) and u.SetEffectValue then
			u:SetEffectValue("Jazz_CougarInspiredUsed", nil)
			u:SetEffectValue("Jazz_GraceKnifeUsed", nil)
		end
	end
end

function Jazz_NamedPerks006Batch4OnTurnStart()
	for _, u in ipairs(g_Units or empty_table) do
		if IsValid(u) and u.SetEffectValue then
			u:SetEffectValue("Jazz_CougarInspiredUsed", nil)
			u:SetEffectValue("Jazz_GraceKnifeUsed", nil)
		end
	end
end
