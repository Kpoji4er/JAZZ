-- JAZZ named personal perks runtime (spec UNITS-006).
-- Single Code module + ModItem CharacterEffect Parameters/reactions.
-- Loc note: VR 6300-6499 reserved; perk text often 6500+ / 9885+.


--- Read a Named Perk Parameter from unit effect or CharacterEffectDefs (ModItem-tunable).
function Jazz_NamedPerkParam(unit, perk_id, key, default)
	local effect
	if unit and unit.GetStatusEffect then
		effect = unit:GetStatusEffect(perk_id)
	end
	if (not effect or not effect.ResolveValue) and CharacterEffectDefs then
		effect = CharacterEffectDefs[perk_id]
	end
	if effect and effect.ResolveValue then
		local v = effect:ResolveValue(key)
		if v ~= nil then
			return v
		end
	end
	return default
end

g_JAZZ_NamedPerks006Wrapped = rawget(_G, "g_JAZZ_NamedPerks006Wrapped") or false
g_JAZZ_NamedPerks006OpsWrapped = rawget(_G, "g_JAZZ_NamedPerks006OpsWrapped") or false
g_JAZZ_JackOfAllOpsBase = rawget(_G, "g_JAZZ_JackOfAllOpsBase") or false
g_JAZZ_JackOfAllArrivingThreshWrapped = rawget(_G, "g_JAZZ_JackOfAllArrivingThreshWrapped") or false
g_JAZZ_JackOfAllArrivingThreshBase = rawget(_G, "g_JAZZ_JackOfAllArrivingThreshBase") or false
g_JAZZ_SteroidPunchSigHidden = rawget(_G, "g_JAZZ_SteroidPunchSigHidden") or false
g_JAZZ_SteroidPunchUIStateBase = rawget(_G, "g_JAZZ_SteroidPunchUIStateBase") or false

local function lHas(unit, perk)
	return unit and HasPerk(unit, perk)
end

function Jazz_NervousGetBonusShots(unit)
	if not unit then
		return 0
	end
	return Clamp(tonumber(unit:GetEffectValue("Jazz_NervousBonusShots")) or 0, 0, Jazz_NamedPerkParam(unit, "Jazz_Perk_Nervous", "stack_cap", 10))
end

local function Jazz_NervousClearApplyCache(unit)
	if not unit then
		return
	end
	unit:SetEffectValue("Jazz_NervousLastBaseShots", nil)
	unit:SetEffectValue("Jazz_NervousLastOutShots", nil)
end

function Jazz_NervousAddHitStack(unit, hits)
	if not lHas(unit, "Jazz_Perk_Nervous") then
		return
	end
	hits = hits or 1
	local cur = Jazz_NervousGetBonusShots(unit)
	unit:SetEffectValue("Jazz_NervousBonusShots", Clamp(cur + hits, 0, Jazz_NamedPerkParam(unit, "Jazz_Perk_Nervous", "stack_cap", 10)))
	Jazz_NervousClearApplyCache(unit)
end

function Jazz_NervousConsumeBonus(unit)
	if not unit then
		return
	end
	unit:SetEffectValue("Jazz_NervousBonusShots", nil)
	Jazz_NervousClearApplyCache(unit)
end

function Jazz_SquadHasVince(unit)
	if not unit or not unit.team then
		return false
	end
	for _, u in ipairs(unit.team.units or empty_table) do
		if IsValid(u) and not u:IsDead() and HasPerk(u, "Jazz_Perk_Vince") then
			return true
		end
	end
	return false
end

-- Soft lock EV −25% med consume: skip one charge with 25% chance when Vince in squad.
-- (Equivalent expected cost; amount>1 also reduced by MulDivRound 75%.)
function Jazz_VinceShouldSkipMedConsume(healer)
	if not Jazz_SquadHasVince(healer) then
		return false
	end
	return InteractionRand(100, "Jazz_Perk_Vince") < Jazz_NamedPerkParam(healer, "Jazz_Perk_Vince", "med_skip_chance", 25)
end

function Jazz_VinceAdjustMedConsumeAmount(healer, amount)
	if not Jazz_SquadHasVince(healer) then
		return amount
	end
	amount = amount or 1
	if amount <= 1 then
		return amount
	end
	return Max(1, MulDivRound(amount, Jazz_NamedPerkParam(healer, "Jazz_Perk_Vince", "med_amount_mul", 75), 100))
end

function Jazz_MadmanDrainWill(center_unit)
	if not center_unit or not g_Combat then
		return
	end
	local slab = const.SlabSizeX
	for _, u in ipairs(g_Units or empty_table) do
		if IsValid(u) and IsKindOf(u, "Unit") and not u:IsDead() then
			if DivRound(center_unit:GetDist(u), slab) <= Jazz_NamedPerkParam(center_unit, "Jazz_Perk_Madman", "radius", 5) then
				local wp = u.WillPoints or 0
				u.WillPoints = Max(0, wp - Jazz_NamedPerkParam(center_unit, "Jazz_Perk_Madman", "will_drain", 10))
				if u.ApplySuppressionStatus then
					u:ApplySuppressionStatus()
				end
			end
		end
	end
end

local function lInstallNamedPerks006()
	if rawget(_G, "g_JAZZ_NamedPerks006Wrapped") then
		return
	end

	-- Dynamo: skip lock traps when lockpicking / opening.
	if IsKindOf(ItemContainer, "Lockpickable") or true then
		local base_trap = ItemContainer.TriggerTrap
		if type(base_trap) == "function" then
			function ItemContainer:TriggerTrap(unit, ...)
				if unit and HasPerk(unit, "Jazz_Perk_Dynamo") then
					return
				end
				return base_trap(self, unit, ...)
			end
		end
	end

	-- Mike: +2 Overwatch attacks.
	local base_ow = Unit.GetOverwatchAttacksAndAim
	if type(base_ow) == "function" then
		function Unit:GetOverwatchAttacksAndAim(...)
			local attacks, aim = base_ow(self, ...)
			if HasPerk(self, "Jazz_Perk_Mike") and type(attacks) == "number" then
				attacks = attacks + 2
			end
			return attacks, aim
		end
	end

	rawset(_G, "g_JAZZ_NamedPerks006Wrapped", true)
end

local function lInstallJackOfAllArrivingThresh()
	-- Do NOT shorten Arriving: shared arrival_squad + faster Wolf ETA = two timeline events
	-- (Sergej report). Restore vanilla threshold if an older wrap is already installed.
	local arriving = SectorOperations and SectorOperations.Arriving
	if not arriving then
		return
	end
	local base = rawget(_G, "g_JAZZ_JackOfAllArrivingThreshBase")
	if rawget(_G, "g_JAZZ_JackOfAllArrivingThreshWrapped") and type(base) == "function" then
		arriving.ProgressCompleteThreshold = base
		rawset(_G, "g_JAZZ_JackOfAllArrivingThreshWrapped", false)
	end
end

local function lInstallSteroidPunchPassiveOnly()
	-- Hide vanilla Steroid smash signature; perk reactions cover all melee.
	local ca = CombatActions and CombatActions.SteroidPunch
	if not ca or rawget(_G, "g_JAZZ_SteroidPunchSigHidden") then
		return
	end
	if type(ca.GetUIState) == "function" and not rawget(_G, "g_JAZZ_SteroidPunchUIStateBase") then
		rawset(_G, "g_JAZZ_SteroidPunchUIStateBase", ca.GetUIState)
	end
	ca.ShowIn = false
	ca.GetUIState = function(self, units, args)
		return "hidden"
	end
	rawset(_G, "g_JAZZ_SteroidPunchSigHidden", true)
end

local function lInstallNamedPerks006Ops()
	lInstallJackOfAllArrivingThresh()
	lInstallSteroidPunchPassiveOnly()

	if rawget(_G, "g_JAZZ_NamedPerks006OpsWrapped") then
		return
	end

	-- GrizzlyPerk signature: 2× suppression on GetActionResults (shots doubled in GetAutofireShots).
	local ca = CombatActions and CombatActions.GrizzlyPerk
	if ca and type(ca.GetActionResults) == "function" and not rawget(ca, "JazzUnits006GrizzlyWrapped") then
		local base_grizzly = ca.GetActionResults
		ca.GetActionResults = function(self, unit, args)
			args = args and table.copy(args) or {}
			local base_sup = args.suppressionbonus or 100
			args.suppressionbonus = base_sup * 2
			return base_grizzly(self, unit, args)
		end
		rawset(ca, "JazzUnits006GrizzlyWrapped", true)
	end

	-- Wolf JackOfAllTrades: −33% satellite operation time (JAZZ wrap; CE param jazz_ops_bonus is display-only).
	-- Skip Traveling (squad-shared) and Arriving (shared arrival_squad must keep one ETA / timeline).
	local base_ops = rawget(_G, "GetOperationTimeLeft")
	if type(base_ops) == "function" and not rawget(_G, "g_JAZZ_JackOfAllOpsBase") then
		rawset(_G, "g_JAZZ_JackOfAllOpsBase", base_ops)
		rawset(_G, "GetOperationTimeLeft", function(merc, operation_id, ...)
			local t = g_JAZZ_JackOfAllOpsBase(merc, operation_id, ...)
			if type(t) == "number" and merc and HasPerk(merc, "JackOfAllTrades")
				and operation_id ~= "Traveling" and operation_id ~= "Arriving" then
				local perk = merc.GetStatusEffect and merc:GetStatusEffect("JackOfAllTrades")
				local bonus = (perk and perk.ResolveValue and perk:ResolveValue("jazz_ops_bonus")) or 33
				t = MulDivRound(t, 100 - bonus, 100)
			end
			return t
		end)
	end

	rawset(_G, "g_JAZZ_NamedPerks006OpsWrapped", true)
end


g_JAZZ_NamedPerks006SignaturesWrapped = rawget(_G, "g_JAZZ_NamedPerks006SignaturesWrapped") or false
g_JAZZ_BunsDamagedTargets = rawget(_G, "g_JAZZ_BunsDamagedTargets") or {}

function Jazz_TagTeamAllyPinDown(attacker, attack_target)
	if not attacker or not attack_target or not g_Pindown then
		return false
	end
	for _, ally in ipairs(attacker.team and attacker.team.units or empty_table) do
		if ally ~= attacker and IsValid(ally) and not ally:IsDead() then
			local pd = g_Pindown[ally]
			if pd then
				local t = pd.target
				if t == attack_target or (IsValid(t) and t == attack_target) then
					return true
				end
			end
		end
	end
	return false
end

function Jazz_BunsTargetDamagedByAlly(attacker, attack_target)
	if not attacker or not attack_target then
		return false
	end
	local bag = rawget(_G, "g_JAZZ_BunsDamagedTargets")
	if type(bag) ~= "table" then
		return false
	end
	local key = attack_target.handle or tostring(attack_target)
	local entry = bag[key]
	return entry and entry ~= attacker
end

function Jazz_BunsMarkDamaged(attacker, attack_target, results)
	if not attacker or not attack_target or not results or results.miss then
		return
	end
	local dmg = results.total_damage or results.dealt_damage or 0
	if type(dmg) ~= "number" or dmg <= 0 then
		dmg = 0
		for _, hit in ipairs(results.hits or empty_table) do
			if hit and type(hit.damage) == "number" and hit.damage > 0 then
				dmg = dmg + hit.damage
			end
		end
	end
	if dmg <= 0 then
		return
	end
	local bag = rawget(_G, "g_JAZZ_BunsDamagedTargets")
	if type(bag) ~= "table" then
		bag = {}
		rawset(_G, "g_JAZZ_BunsDamagedTargets", bag)
	end
	local key = attack_target.handle or tostring(attack_target)
	if not bag[key] then
		bag[key] = attacker
	end
end

function Jazz_ApplyHawksEyeSuppression(attacker, suppressionbonus)
	if not attacker or not HasPerk(attacker, "HawksEye") then
		return suppressionbonus
	end
	local w = attacker.GetActiveWeapons and attacker:GetActiveWeapons("Firearm")
	if w and IsKindOf(w, "SniperRifle") then
		return (suppressionbonus or 100) * 2
	end
	return suppressionbonus
end

local function lInstallNamedPerks006Signatures()
	if rawget(_G, "g_JAZZ_NamedPerks006SignaturesWrapped") then
		return
	end

	local bh = CombatActions and CombatActions.BulletHell
	if bh then
		local params = bh.Parameters or {}
		local has = false
		for _, p in ipairs(params) do
			if p and p.Name == "recharge_on_kill" then
				p.Value = 1
				has = true
				break
			end
		end
		if not has then
			params[#params + 1] = PlaceObj("PresetParamNumber", {
				"Name", "recharge_on_kill",
				"Value", 1,
				"Tag", "<recharge_on_kill>",
			})
			bh.Parameters = params
		end
	end

	-- Track damage for Buns via Unit.OnAttack reaction-style wrap of ExecAttack results path.
	if type(Unit.OnAttack) == "function" and not rawget(Unit, "JazzUnits006BunsWrapped") then
		local base = Unit.OnAttack
		function Unit:OnAttack(action, target, results, attack_args, ...)
			local ret = base(self, action, target, results, attack_args, ...)
			if type(Jazz_BunsMarkDamaged) == "function" and IsKindOf(target, "Unit") then
				Jazz_BunsMarkDamaged(self, target, results)
			end
			return ret
		end
		rawset(Unit, "JazzUnits006BunsWrapped", true)
	elseif not rawget(Unit, "JazzUnits006BunsWrapped") then
		-- Fallback: wrap FirearmAttack return path is too invasive; Buns CE still works if MapVar filled elsewhere.
		rawset(Unit, "JazzUnits006BunsWrapped", true)
	end

	rawset(_G, "g_JAZZ_NamedPerks006SignaturesWrapped", true)
end

local function lNamedPerks006OnCombatStart_Signatures()
	rawset(_G, "g_JAZZ_BunsDamagedTargets", {})
end

local function lNamedPerks006OnTurnStart_Signatures()
	rawset(_G, "g_JAZZ_BunsDamagedTargets", {})
end

g_JAZZ_NamedPerks006EconomyWrapped = rawget(_G, "g_JAZZ_NamedPerks006EconomyWrapped") or false
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
	return Clamp((tonumber(lvl) or 1) * Jazz_NamedPerkParam(unit, "Jazz_Perk_Static", "parts_per_level", 5), 0, Jazz_NamedPerkParam(unit, "Jazz_Perk_Static", "parts_cap", 25))
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

local function lInstallNamedPerks006Economy()
	if rawget(_G, "g_JAZZ_NamedPerks006EconomyWrapped") then
		return
	end

	-- Flo: Bobby Ray buy −12%.
	local br = rawget(_G, "BobbyRayStoreGetEntryCost")
	if type(br) == "function" and not rawget(_G, "g_JAZZ_FloBuySellBase_BR") then
		rawset(_G, "g_JAZZ_FloBuySellBase_BR", br)
		rawset(_G, "BobbyRayStoreGetEntryCost", function(entry)
			local cost = g_JAZZ_FloBuySellBase_BR(entry)
			if type(cost) == "number" and Jazz_SquadHasFlo() then
				local disc = Jazz_NamedPerkParam(nil, "Jazz_Perk_Flo", "buy_discount", 12)
				cost = MulDivRound(cost, 100 - disc, 100)
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
				local bonus = Jazz_NamedPerkParam(nil, "Jazz_Perk_Flo", "sell_bonus", 12)
				item.Cost = MulDivRound(old, 100 + bonus, 100)
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
					radius = MulDivRound(radius, Jazz_NamedPerkParam(attacker, "Jazz_Perk_Cougar", "noise_mul", 67), 100)
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
				local mul = Jazz_NamedPerkParam(attacker, "Jazz_Perk_Kulba", "recoil_mul", 50)
				profile.effective_recoil = (profile.effective_recoil or 0) * mul / 100
				profile.perk_factor = (profile.perk_factor or 1) * mul / 100
				if profile.retention and JAZZ_CTH_FACTOR_SCALE then
					local retention = Clamp(1 - profile.effective_recoil * 1.0 / 100, 0.15, 1)
					profile.retention = JAZZ_CTHRound(retention * JAZZ_CTH_FACTOR_SCALE)
				end
			end
			return profile
		end)
	end

	rawset(_G, "g_JAZZ_NamedPerks006EconomyWrapped", true)
end

local function lNamedPerks006OnCombatStart_Economy()
	for _, u in ipairs(g_Units or empty_table) do
		if IsValid(u) and u.SetEffectValue then
			u:SetEffectValue("Jazz_CougarInspiredUsed", nil)
			u:SetEffectValue("Jazz_GraceKnifeUsed", nil)
		end
	end
end

local function lNamedPerks006OnTurnStart_Economy()
	for _, u in ipairs(g_Units or empty_table) do
		if IsValid(u) and u.SetEffectValue then
			u:SetEffectValue("Jazz_CougarInspiredUsed", nil)
			u:SetEffectValue("Jazz_GraceKnifeUsed", nil)
		end
	end
end

g_JAZZ_NamedPerks006SatelliteWrapped = rawget(_G, "g_JAZZ_NamedPerks006SatelliteWrapped") or false
g_JAZZ_BarryCraftBase_ItemsCalc = rawget(_G, "g_JAZZ_BarryCraftBase_ItemsCalc") or false
g_JAZZ_CordOpsBase_Time = rawget(_G, "g_JAZZ_CordOpsBase_Time") or false
g_JAZZ_ConradOpsBase_Time = rawget(_G, "g_JAZZ_ConradOpsBase_Time") or false
g_JAZZ_RothmanMineBase = rawget(_G, "g_JAZZ_RothmanMineBase") or false
g_JAZZ_CarlosRemoveHiddenBase = rawget(_G, "g_JAZZ_CarlosRemoveHiddenBase") or false
g_JAZZ_MeatSuppressionBase = rawget(_G, "g_JAZZ_MeatSuppressionBase") or false

local PRIMARY_STATS = {
	"Health",
	"Agility",
	"Dexterity",
	"Strength",
	"Wisdom",
	"Leadership",
	"Marksmanship",
	"Mechanical",
	"Explosives",
	"Medical",
}

local function lIsPlayerSide(side)
	return side == "player1" or side == "player2"
end

function Jazz_SectorHasRothman(sector_id)
	if not sector_id or not gv_Squads then
		return false
	end
	for _, squad in pairs(gv_Squads) do
		if squad and lIsPlayerSide(squad.Side) and squad.CurrentSector == sector_id then
			for _, uid in ipairs(squad.units or empty_table) do
				local u = gv_UnitData and gv_UnitData[uid]
				if not u and g_Units then
					u = g_Units[uid]
				end
				if u and HasPerk(u, "Jazz_Perk_Rothman") and not (u.IsDead and u:IsDead()) then
					return true
				end
			end
		end
	end
	return false
end

-- Loyalty-scaled mine income boost while Rothman garrisons the mine sector.
-- Bonus% = 10 + MulDivRound(Max(0, 100 - loyalty), 30, 100)  → ~10% @100 loyalty, ~40% @0.
function Jazz_RothmanMineBonusPercent(sector_id)
	if not Jazz_SectorHasRothman(sector_id) then
		return 0
	end
	local sector = gv_Sectors and gv_Sectors[sector_id]
	if not sector or not sector.Mine then
		return 0
	end
	local loyalty = GetCityLoyalty and (GetCityLoyalty(sector.City) or 50) or 50
	local base = Jazz_NamedPerkParam(nil, "Jazz_Perk_Rothman", "mine_bonus_base", 10)
	local span = Jazz_NamedPerkParam(nil, "Jazz_Perk_Rothman", "mine_bonus_loyalty_span", 30)
	return base + MulDivRound(Max(0, 100 - loyalty), span, 100)
end

function Jazz_IraApplyMilitiaTrainBonus(unit)
	if not unit or not HasPerk then
		return false
	end
	-- Caller must verify Ira trained this militia; applies +20 to a random primary.
	local stat = PRIMARY_STATS[1 + InteractionRand(#PRIMARY_STATS, "Jazz_Perk_Ira")]
	local cur = unit[stat] or 0
	if type(cur) ~= "number" then
		return false
	end
	unit[stat] = Clamp(cur + Jazz_NamedPerkParam(nil, "Jazz_Perk_Ira", "primary_bonus", 20), 0, 100)
	return true, stat
end

function Jazz_FindMiguel()
	for _, u in ipairs(g_Units or empty_table) do
		if IsValid(u) and HasPerk(u, "Jazz_Perk_Miguel") then
			return u
		end
	end
	return false
end

local function lMiguelIsDowned(u)
	if not u or u:IsDead() then
		return true
	end
	if u.IsDowned and u:IsDowned() then
		return true
	end
	if u.HasStatusEffect and (u:HasStatusEffect("Unconscious") or u:HasStatusEffect("KnockDown")) then
		return true
	end
	return false
end

function Jazz_MiguelRefreshAura()
	local miguel = Jazz_FindMiguel()
	if not miguel then
		return
	end
	local up = not lMiguelIsDowned(miguel)
	local buff = up and "Jazz_MiguelAuraUp" or "Jazz_MiguelAuraDown"
	local other = up and "Jazz_MiguelAuraDown" or "Jazz_MiguelAuraUp"
	local slab = const.SlabSizeX
	for _, u in ipairs(g_Units or empty_table) do
		if IsValid(u) and u ~= miguel and not u:IsDead() and miguel.team and u.team == miguel.team then
			if DivRound(miguel:GetDist(u), slab) <= Jazz_NamedPerkParam(miguel, "Jazz_Perk_Miguel", "aura_radius", 30) then
				if u:HasStatusEffect(other) then
					u:RemoveStatusEffect(other)
				end
				if not u:HasStatusEffect(buff) then
					u:AddStatusEffect(buff)
				end
			else
				u:RemoveStatusEffect("Jazz_MiguelAuraUp")
				u:RemoveStatusEffect("Jazz_MiguelAuraDown")
			end
		end
	end
end

function Jazz_BarryCraftDiscountPercent(unit)
	if unit and HasPerk(unit, "DesignerExplosives") then
		return Jazz_NamedPerkParam(unit, "DesignerExplosives", "craft_discount", 30)
	end
	return 0
end

function Jazz_CordInBarCity(merc)
	if not merc then
		return false
	end
	if not HasPerk(merc, "Jazz_Perk_Cord") then
		return false
	end
	local squad_id = merc.Squad
	local squad = squad_id and gv_Squads and gv_Squads[squad_id]
	local sector_id = squad and squad.CurrentSector
	local sector = sector_id and gv_Sectors and gv_Sectors[sector_id]
	if not sector then
		return false
	end
	-- Soft: any city sector (bar POI gate deferred).
	return sector.City and sector.City ~= "none"
end

function Jazz_ConradEffectiveLeadership(merc)
	local ldr = (merc and merc.Leadership) or 0
	if merc and HasPerk(merc, "Jazz_Perk_Conrad") then
		return Max(ldr, Jazz_NamedPerkParam(merc, "Jazz_Perk_Conrad", "leadership_floor", 90))
	end
	return ldr
end

local TRAIN_OPS = {
	TrainMilitia = true,
	MilitiaTraining = true,
	TrainMercs = true,
	TrainStats = true,
	Teacher = true,
}

local REPAIR_OPS = {
	RepairItems = true,
	Repair = true,
}

local function lInstallNamedPerks006Satellite()
	-- Ira hook may need SectorOperations after first wrap attempt.
	if rawget(_G, "g_JAZZ_NamedPerks006SatelliteWrapped") then
		Jazz_InstallIraMilitiaTrainHook()
		return
	end

	-- Rothman: loyalty-scaled mine income while garrisoned.
	local mine = rawget(_G, "_GetMineIncome")
	if type(mine) == "function" and not rawget(_G, "g_JAZZ_RothmanMineBase") then
		rawset(_G, "g_JAZZ_RothmanMineBase", mine)
		rawset(_G, "_GetMineIncome", function(sector_id, showEvenIfUnowned)
			local income = g_JAZZ_RothmanMineBase(sector_id, showEvenIfUnowned)
			if type(income) ~= "number" or income <= 0 then
				return income
			end
			local bonus = Jazz_RothmanMineBonusPercent(sector_id)
			if bonus > 0 then
				income = MulDivRound(income, 100 + bonus, 100)
			end
			return income
		end)
	end

	-- Barry: CraftAmmo / CraftExplosives Parts −30%.
	local calc = rawget(_G, "SectorOperation_ItemsCalcRes")
	if type(calc) == "function" and not rawget(_G, "g_JAZZ_BarryCraftBase_ItemsCalc") then
		rawset(_G, "g_JAZZ_BarryCraftBase_ItemsCalc", calc)
		rawset(_G, "SectorOperation_ItemsCalcRes", function(sector_id, operation_id)
			local parts = g_JAZZ_BarryCraftBase_ItemsCalc(sector_id, operation_id)
			if type(parts) ~= "number" or parts <= 0 then
				return parts
			end
			local mercs = GetOperationProfessionals and GetOperationProfessionals(sector_id, operation_id) or empty_table
			if operation_id == "CraftAmmo" or operation_id == "CraftExplosives" then
				local best = 0
				for _, merc in ipairs(mercs) do
					best = Max(best, Jazz_BarryCraftDiscountPercent(merc))
				end
				if best > 0 then
					parts = Max(0, MulDivRound(parts, 100 - best, 100))
				end
			elseif REPAIR_OPS[operation_id] then
				for _, merc in ipairs(mercs) do
					if Jazz_CordInBarCity(merc) then
						local disc = Jazz_NamedPerkParam(merc, "Jazz_Perk_Cord", "repair_parts_discount", 10)
						parts = Max(0, MulDivRound(parts, 100 - disc, 100))
						break
					end
				end
			end
			return parts
		end)
	end

	-- Cord / Conrad: satellite op time.
	local base_ops = rawget(_G, "GetOperationTimeLeft")
	if type(base_ops) == "function" and not rawget(_G, "g_JAZZ_CordOpsBase_Time") then
		rawset(_G, "g_JAZZ_CordOpsBase_Time", base_ops)
		rawset(_G, "GetOperationTimeLeft", function(merc, operation_id, ...)
			local t = g_JAZZ_CordOpsBase_Time(merc, operation_id, ...)
			if type(t) ~= "number" then
				return t
			end
			if Jazz_CordInBarCity(merc) and REPAIR_OPS[operation_id] then
				local td = Jazz_NamedPerkParam(merc, "Jazz_Perk_Cord", "repair_time_discount", 15)
				t = MulDivRound(t, 100 - td, 100)
			end
			if merc and HasPerk(merc, "Jazz_Perk_Conrad") and TRAIN_OPS[operation_id] then
				local ldr = merc.Leadership or 0
				local floor = Jazz_NamedPerkParam(merc, "Jazz_Perk_Conrad", "leadership_floor", 90)
				if ldr < floor and ldr > 0 then
					-- Treat Leadership as floor 90 for training pace.
					t = MulDivRound(t, ldr, floor)
				end
			end
			return t
		end)
	end

	-- Meat: Will-point damage → Grit; skip suppression application.
	if type(QueueSuppressionApplication) == "function" and not rawget(_G, "g_JAZZ_MeatSuppressionBase") then
		rawset(_G, "g_JAZZ_MeatSuppressionBase", QueueSuppressionApplication)
		rawset(_G, "QueueSuppressionApplication", function(unit, wp_dmg, effect)
			if IsValid(unit) and HasPerk(unit, "Jazz_Perk_Meat") then
				local dmg = tonumber(wp_dmg) or 0
				if dmg > 0 and unit.ApplyTempHitPoints then
					unit:ApplyTempHitPoints(dmg)
				end
				-- Unsuppressible: drop status_effect from queue path.
				return
			end
			return g_JAZZ_MeatSuppressionBase(unit, wp_dmg, effect)
		end)
	end

	-- Carlos: failed stealth kill may keep Hidden (50%).
	if Unit and type(Unit.RemoveStatusEffect) == "function" and not rawget(_G, "g_JAZZ_CarlosRemoveHiddenBase") then
		rawset(_G, "g_JAZZ_CarlosRemoveHiddenBase", Unit.RemoveStatusEffect)
		function Unit:RemoveStatusEffect(id, ...)
			if id == "Hidden" and HasPerk(self, "Jazz_Perk_Carlos") then
				if self.GetEffectValue and self:GetEffectValue("Jazz_CarlosKeepHidden") then
					self:SetEffectValue("Jazz_CarlosKeepHidden", nil)
					if InteractionRand(100, "Jazz_Perk_Carlos") < Jazz_NamedPerkParam(self, "Jazz_Perk_Carlos", "keep_hidden_chance", 50) then
						return
					end
				end
			end
			return g_JAZZ_CarlosRemoveHiddenBase(self, id, ...)
		end
	end

	if Unit and type(Unit.OnAttack) == "function" and not rawget(Unit, "JazzUnits006CarlosWrapped") then
		local base = Unit.OnAttack
		function Unit:OnAttack(action, target, results, attack_args, ...)
			local ret = base(self, action, target, results, attack_args, ...)
			if HasPerk(self, "Jazz_Perk_Carlos") and results and attack_args then
				local chance = attack_args.stealth_kill_chance or 0
				if chance > 0 and not results.stealth_kill then
					self:SetEffectValue("Jazz_CarlosKeepHidden", true)
				end
			end
			if type(Jazz_DangerCloseOnAttack) == "function" then
				Jazz_DangerCloseOnAttack(self, action, target, results, attack_args)
			end
			if type(Jazz_SimonOnKillCharge) == "function" then
				Jazz_SimonOnKillCharge(self, results, target)
			end
			return ret
		end
		rawset(Unit, "JazzUnits006CarlosWrapped", true)
	end

	-- Ira: militia she trains gains +20 random primary on op Complete.
	Jazz_InstallIraMilitiaTrainHook()

	rawset(_G, "g_JAZZ_NamedPerks006SatelliteWrapped", true)
end

function Jazz_SectorHasIraTrainer(sector)
	local sector_id = type(sector) == "table" and (sector.Id or sector.id) or sector
	if not sector_id then
		return false
	end
	local mercs = GetOperationProfessionals and GetOperationProfessionals(sector_id, "MilitiaTraining") or empty_table
	if not next(mercs) then
		mercs = GetOperationProfessionals and GetOperationProfessionals(sector_id, "TrainMilitia") or empty_table
	end
	for _, merc in ipairs(mercs) do
		if merc and HasPerk(merc, "Jazz_Perk_Ira") and not (merc.IsDead and merc:IsDead()) then
			return true
		end
	end
	-- Garrison fallback: Ira present in sector squads.
	for _, squad in pairs(gv_Squads or empty_table) do
		if squad and lIsPlayerSide(squad.Side) and squad.CurrentSector == sector_id then
			for _, uid in ipairs(squad.units or empty_table) do
				local u = gv_UnitData and gv_UnitData[uid]
				if u and HasPerk(u, "Jazz_Perk_Ira") and not (u.IsDead and u:IsDead()) then
					return true
				end
			end
		end
	end
	return false
end

function Jazz_IraBoostMilitiaInSector(sector)
	if not Jazz_SectorHasIraTrainer(sector) then
		return
	end
	local sector_id = type(sector) == "table" and (sector.Id or sector.id) or sector
	local sector_obj = (type(sector) == "table" and sector) or (gv_Sectors and gv_Sectors[sector_id])
	local squad_id = sector_obj and sector_obj.militia_squad_id
	local squad = squad_id and gv_Squads and gv_Squads[squad_id]
	if not squad then
		return
	end
	for _, uid in ipairs(squad.units or empty_table) do
		local u = gv_UnitData and gv_UnitData[uid]
		if u and not u.Jazz_IraTrainedBonus then
			local ok = Jazz_IraApplyMilitiaTrainBonus(u)
			if ok then
				u.Jazz_IraTrainedBonus = true
			end
		end
	end
end

function Jazz_InstallIraMilitiaTrainHook()
	if rawget(_G, "g_JAZZ_IraMilitiaHook") or not SectorOperations then
		return
	end
	local op = SectorOperations.MilitiaTraining or SectorOperations.TrainMilitia
	if not op then
		return
	end
	rawset(_G, "g_JAZZ_IraMilitiaHook", true)
	local base_complete = op.Complete or op.OnComplete
	if type(base_complete) ~= "function" then
		return
	end
	local key = op.Complete and "Complete" or "OnComplete"
	local prev = op[key]
	op[key] = function(self, sector, ...)
		local ret = prev(self, sector, ...)
		if type(Jazz_IraBoostMilitiaInSector) == "function" then
			Jazz_IraBoostMilitiaInSector(sector)
		end
		return ret
	end
end

function Jazz_DangerCloseOnAttack(attacker, action, target, results, attack_args)
	if not attacker or not HasPerk(attacker, "DangerClose") or not results or results.miss then
		return
	end
	if not IsKindOf(target, "Unit") then
		return
	end
	local dist = DivRound(attacker:GetDist(target), const.SlabSizeX)
	if dist < Jazz_NamedPerkParam(attacker, "DangerClose", "minRange", 8) then
		return
	end
	-- Soft partial: mark bleed stacks if status exists; damage bonus is via CE reaction when present.
	local stacks = Jazz_NamedPerkParam(attacker, "DangerClose", "bleed_stacks", 2)
	if CharacterEffectDefs and CharacterEffectDefs.Bleeding and target.AddStatusEffect then
		for _ = 1, stacks do
			target:AddStatusEffect("Bleeding")
		end
	end
end

local function lNamedPerks006OnCombatStart_Satellite()
	Jazz_MiguelRefreshAura()
end

local function lNamedPerks006OnTurnStart_Satellite()
	Jazz_MiguelRefreshAura()
end

g_JAZZ_NamedPerks006SectionDWrapped = rawget(_G, "g_JAZZ_NamedPerks006SectionDWrapped") or false

function Jazz_BennyDecoyReady(unit)
	return unit and HasPerk(unit, "Jazz_Perk_Benny") and not unit:GetEffectValue("Jazz_BennyDecoyCd")
end

function Jazz_BennyMarkDecoyUsed(unit)
	if unit and unit.SetEffectValue then
		unit:SetEffectValue("Jazz_BennyDecoyCd", true)
	end
end

-- Soft-cut full CombatAction decoy: helper for future CA. Lure prefers lowest-Will enemy ≤8.
function Jazz_BennyPickLureTarget(unit)
	if not Jazz_BennyDecoyReady(unit) then
		return false
	end
	local best, best_will
	local slab = const.SlabSizeX
	for _, enemy in ipairs(g_Units or empty_table) do
		if IsValid(enemy) and not enemy:IsDead() and unit:IsOnEnemySide(enemy) then
			if DivRound(unit:GetDist(enemy), slab) <= Jazz_NamedPerkParam(unit, "Jazz_Perk_Benny", "lure_range", 8) then
				local will = enemy.WillPoints or enemy.Will or 999
				if not best or will < best_will then
					best, best_will = enemy, will
				end
			end
		end
	end
	return best
end

function Jazz_SimonHas4xOptic(unit)
	if not unit then
		return false
	end
	local w = unit.GetActiveWeapons and unit:GetActiveWeapons("Firearm")
	if not w then
		return false
	end
	local components = w.components or w.Components
	if type(components) ~= "table" then
		-- Fallback: Magnification / Scope zoom property if present.
		local zoom = w.ScopeAccuracyBonus or w.Magnification or 0
		return type(zoom) == "number" and zoom >= 4
	end
	for _, comp in pairs(components) do
		if comp then
			local id = type(comp) == "string" and comp or (comp.Id or comp.id or comp.class)
			local def = id and WeaponComponents and WeaponComponents[id]
			local mag = def and (def.Magnification or def.Zoom or def.OpticalZoom)
			if type(mag) == "number" and mag >= 4 then
				return true
			end
			if id and (string.find(tostring(id), "4x", 1, true) or string.find(tostring(id), "Scope", 1, true)) then
				-- Soft: Scope* ids count as eligible until precise mag table wired.
				if string.find(tostring(id), "4x", 1, true) or string.find(tostring(id), "8x", 1, true) or string.find(tostring(id), "10x", 1, true) then
					return true
				end
			end
		end
	end
	return false
end

function Jazz_SimonPerfectShotReady(unit)
	return unit
		and HasPerk(unit, "Jazz_Perk_Simon")
		and not unit:GetEffectValue("Jazz_SimonPerfectCd")
		and Jazz_SimonHas4xOptic(unit)
end

function Jazz_SimonMarkPerfectUsed(unit)
	if unit and unit.SetEffectValue then
		unit:SetEffectValue("Jazz_SimonPerfectCd", true)
	end
end

function Jazz_SimonOnKillCharge(attacker, results, target)
	if not attacker or not HasPerk(attacker, "Jazz_Perk_Simon") then
		return
	end
	local killed = false
	if results and results.killed_units then
		for _, u in ipairs(results.killed_units) do
			if IsValid(u) then
				killed = true
				break
			end
		end
	end
	if not killed and IsKindOf(target, "Unit") and target:IsDead() then
		killed = true
	end
	if killed and attacker.SetEffectValue then
		attacker:SetEffectValue("Jazz_SimonPerfectCd", nil)
	end
end

local function lInstallNamedPerks006SectionD()
	if rawget(_G, "g_JAZZ_NamedPerks006SectionDWrapped") then
		return
	end
	-- Soft-cut: no CombatAction registration yet; CE + StartingPerks + helpers above.
	rawset(_G, "g_JAZZ_NamedPerks006SectionDWrapped", true)
end

local function lNamedPerks006OnCombatStart_SectionD()
	for _, u in ipairs(g_Units or empty_table) do
		if IsValid(u) and u.SetEffectValue then
			u:SetEffectValue("Jazz_BennyDecoyCd", nil)
			-- Simon starts charged (no CD) each combat; CD set after use until kill.
			u:SetEffectValue("Jazz_SimonPerfectCd", nil)
		end
	end
end

local function lInstallAllNamedPerks006()
	lInstallNamedPerks006()
	lInstallNamedPerks006Ops()
	lInstallNamedPerks006Signatures()
	lInstallNamedPerks006Economy()
	lInstallNamedPerks006Satellite()
	lInstallNamedPerks006SectionD()
end

function Jazz_NamedPerks006OnCombatStart()
	lNamedPerks006OnCombatStart_Signatures()
	lNamedPerks006OnCombatStart_Economy()
	lNamedPerks006OnCombatStart_Satellite()
	lNamedPerks006OnCombatStart_SectionD()
end

function Jazz_NamedPerks006OnTurnStart()
	lNamedPerks006OnTurnStart_Signatures()
	lNamedPerks006OnTurnStart_Economy()
	lNamedPerks006OnTurnStart_Satellite()
end

OnMsg.ModsReloaded = function()
	lInstallAllNamedPerks006()
end
OnMsg.DataLoaded = function()
	lInstallAllNamedPerks006()
end
OnMsg.NewGame = function()
	lInstallAllNamedPerks006()
end
OnMsg.LoadGame = function()
	lInstallAllNamedPerks006()
end

OnMsg.CombatStart = function()
	Jazz_NamedPerks006OnCombatStart()
end
OnMsg.TurnStart = function()
	Jazz_NamedPerks006OnTurnStart()
end
