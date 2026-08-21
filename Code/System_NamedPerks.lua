-- JAZZ named personal perks runtime (spec UNITS-006).
-- Single Code module + ModItem CharacterEffect Parameters/reactions.
-- Loc note: VR 6300-6499 reserved; perk text often 6500+ / 9885+.

-- Defined in System_OR_Unit.lua (CombatAction/Perk id fallback).
JazzUnitHasPerk = rawget(_G, "JazzUnitHasPerk") or false


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

-- Pre-declare so ModsReloaded / mid-session rawset can overwrite without "new global" assert.
Jazz_KillingWindCountEnemies = rawget(_G, "Jazz_KillingWindCountEnemies") or false
Jazz_KillingWindTryGrit = rawget(_G, "Jazz_KillingWindTryGrit") or false
g_JAZZ_WeGotThisSquadGuardWrapped = rawget(_G, "g_JAZZ_WeGotThisSquadGuardWrapped") or false

--- Fauda KillingWind: count distinct enemies damaged/hit in one attack results table.
local function lKillingWindCountEnemies(attacker, results)
	if not attacker or not results then
		return 0
	end
	local enemiesHit = 0
	local seen = {}
	local function consider(obj)
		if not obj or seen[obj] then
			return
		end
		-- Vanilla sometimes stores hit records { obj = Unit, damage = n } in hit_objs.
		if not IsKindOf(obj, "Unit") and type(obj) == "table" and obj.obj then
			obj = obj.obj
		end
		if not obj or seen[obj] or not IsKindOf(obj, "Unit") then
			return
		end
		if attacker.IsOnEnemySide then
			if not attacker:IsOnEnemySide(obj) then
				return
			end
		elseif obj.IsOnEnemySide then
			if not obj:IsOnEnemySide(attacker) then
				return
			end
		else
			return
		end
		seen[obj] = true
		enemiesHit = enemiesHit + 1
	end
	if type(results.unit_damage) == "table" then
		for obj, dmg in pairs(results.unit_damage) do
			if type(dmg) == "number" and dmg > 0 then
				consider(obj)
			end
		end
	end
	for _, obj in ipairs(results.hit_objs or empty_table) do
		consider(obj)
	end
	for _, hit in ipairs(results.area_hits or empty_table) do
		if hit and (hit.damage or 0) > 0 then
			consider(hit.obj)
		end
	end
	for _, obj in ipairs(results.killed_units or empty_table) do
		consider(obj)
	end
	-- Dual/burst nested attacks: fold child tables (shared `seen`).
	for _, nested in ipairs(results.attacks or empty_table) do
		if nested and nested ~= results then
			if type(nested.unit_damage) == "table" then
				for obj, dmg in pairs(nested.unit_damage) do
					if type(dmg) == "number" and dmg > 0 then
						consider(obj)
					end
				end
			end
			for _, obj in ipairs(nested.hit_objs or empty_table) do
				consider(obj)
			end
			for _, hit in ipairs(nested.area_hits or empty_table) do
				if hit and (hit.damage or 0) > 0 then
					consider(hit.obj)
				end
			end
			for _, obj in ipairs(nested.killed_units or empty_table) do
				consider(obj)
			end
		end
	end
	return enemiesHit
end

--- Fauda KillingWind: ≥2 enemies → +gritPerEnemyHit Grit each (ApplyTempHitPoints).
--- Do NOT bail on results.miss — primary miss still allows multi-target hits in the same volley.
--- Prefer aggregate `results` (ExecFirearmAttacks); CE OnUnitAttack may see per-hand/per-shot tables.
local function lKillingWindTryGrit(attacker, results)
	if not attacker then
		return
	end
	local has_kw = type(JazzUnitHasPerk) == "function" and JazzUnitHasPerk(attacker, "KillingWind")
		or HasPerk(attacker, "KillingWind")
	if not has_kw then
		return
	end
	if not results then
		return
	end
	-- One grant per aggregate results table (nested OnAttack / dual calls).
	if results.jazz_kw_grit_done then
		return
	end
	local n = lKillingWindCountEnemies(attacker, results)
	if n < 2 then
		return
	end
	results.jazz_kw_grit_done = true
	local per = Jazz_NamedPerkParam(attacker, "KillingWind", "gritPerEnemyHit", 8)
	if type(per) ~= "number" or per < 1 then
		per = 8
	end
	attacker:ApplyTempHitPoints(per * n)
end

rawset(_G, "Jazz_KillingWindCountEnemies", lKillingWindCountEnemies)
rawset(_G, "Jazz_KillingWindTryGrit", lKillingWindTryGrit)

g_JAZZ_NamedPerks006Wrapped = rawget(_G, "g_JAZZ_NamedPerks006Wrapped") or false
g_JAZZ_NamedPerks006OpsWrapped = rawget(_G, "g_JAZZ_NamedPerks006OpsWrapped") or false
g_JAZZ_JackOfAllArrivingThreshWrapped = rawget(_G, "g_JAZZ_JackOfAllArrivingThreshWrapped") or false
g_JAZZ_JackOfAllArrivingThreshBase = rawget(_G, "g_JAZZ_JackOfAllArrivingThreshBase") or false
g_JAZZ_SteroidPunchSigHidden = rawget(_G, "g_JAZZ_SteroidPunchSigHidden") or false
g_JAZZ_SteroidPunchUIStateBase = rawget(_G, "g_JAZZ_SteroidPunchUIStateBase") or false
g_JAZZ_SteroidBurningTickWrapped = rawget(_G, "g_JAZZ_SteroidBurningTickWrapped") or false
g_JAZZ_EnvEffectBurningTickBase = rawget(_G, "g_JAZZ_EnvEffectBurningTickBase") or false
g_JAZZ_ExplodingPalmSigConfigured = rawget(_G, "g_JAZZ_ExplodingPalmSigConfigured") or false
g_JAZZ_ExplodingPalmMeleeWrapped = rawget(_G, "g_JAZZ_ExplodingPalmMeleeWrapped") or false
g_JAZZ_ExplodingPalmMeleeBase = rawget(_G, "g_JAZZ_ExplodingPalmMeleeBase") or false
g_JAZZ_BuildingConfidenceHealWrapped = rawget(_G, "g_JAZZ_BuildingConfidenceHealWrapped") or false
g_JAZZ_BuildingConfidenceHealBase = rawget(_G, "g_JAZZ_BuildingConfidenceHealBase") or false
g_JAZZ_DangerCloseExplosionWrapped = rawget(_G, "g_JAZZ_DangerCloseExplosionWrapped") or false
g_JAZZ_TheGrimRechargeWrapped = rawget(_G, "g_JAZZ_TheGrimRechargeWrapped") or false
g_JAZZ_AddSignatureRechargeTimeBase = rawget(_G, "g_JAZZ_AddSignatureRechargeTimeBase") or false
g_JAZZ_UpdateSignatureRechargesBase = rawget(_G, "g_JAZZ_UpdateSignatureRechargesBase") or false
g_JAZZ_TheGrimGetActionDescriptionBase = rawget(_G, "g_JAZZ_TheGrimGetActionDescriptionBase") or false
g_JAZZ_PendingSigKillCount = rawget(_G, "g_JAZZ_PendingSigKillCount") or 0

-- Legacy flag from earlier hide-only install; keep so ModsReloaded does not break.
g_JAZZ_ExplodingPalmSigHidden = rawget(_G, "g_JAZZ_ExplodingPalmSigHidden") or false

-- Reaper TheGrim: kills required to clear recharge_on_kill CD (UNITS-006).
Jazz_TheGrimKillsToRecharge = rawget(_G, "Jazz_TheGrimKillsToRecharge") or 5
if Jazz_TheGrimKillsToRecharge < 2 then
	Jazz_TheGrimKillsToRecharge = 5
end

--- Merc/unit level for MD BuildingConfidence (±heal by level delta).
function Jazz_BuildingConfidenceUnitLevel(unit)
	if not unit then
		return 1
	end
	if type(unit.GetLevel) == "function" then
		local ok, lvl = pcall(unit.GetLevel, unit)
		if ok and lvl ~= nil then
			return tonumber(lvl) or 1
		end
	end
	local sid = unit.session_id
	local ud = sid and gv_UnitData and gv_UnitData[sid]
	if ud and type(ud.GetLevel) == "function" then
		local ok, lvl = pcall(ud.GetLevel, ud)
		if ok and lvl ~= nil then
			return tonumber(lvl) or 1
		end
	end
	return 1
end

--- Apply ±10%/level-diff heal_modifier (cap ±50%). Sets data.jazz_buildingconfidence to avoid double apply.
function Jazz_BuildingConfidenceApplyHealMod(medic, patient, data)
	if not data or data.jazz_buildingconfidence then
		return
	end
	if not medic or not patient or not HasPerk(medic, "BuildingConfidence") then
		return
	end
	local per = Jazz_NamedPerkParam(medic, "BuildingConfidence", "percentPerLevel", 10)
	local cap = Jazz_NamedPerkParam(medic, "BuildingConfidence", "percentCap", 50)
	local delta = Jazz_BuildingConfidenceUnitLevel(medic) - Jazz_BuildingConfidenceUnitLevel(patient)
	local bonus = Clamp(delta * per, -cap, cap)
	data.jazz_buildingconfidence = true
	if bonus == 0 then
		return
	end
	data.heal_modifier = MulDivRound(data.heal_modifier or 100, 100 + bonus, 100)
end

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

--- Thor NaturalHealing: same sat squad (or self) has the perk.
function Jazz_SquadHasNaturalHealing(unit)
	if not unit then
		return false
	end
	if HasPerk(unit, "NaturalHealing") then
		return true
	end
	local squad_id = unit.Squad
	local squad = squad_id and gv_Squads and gv_Squads[squad_id]
	if not squad then
		return false
	end
	for _, uid in ipairs(squad.units or empty_table) do
		local u = gv_UnitData and gv_UnitData[uid]
		if not u and g_Units then
			u = g_Units[uid]
		end
		if u and HasPerk(u, "NaturalHealing") and not (u.IsDead and u:IsDead()) then
			return true
		end
	end
	return false
end

--- Interval mul for trauma/burn checks: 15% faster → 85. Infection timers must not use this.
function Jazz_NaturalHealingDebtHoursMul(unit)
	if not Jazz_SquadHasNaturalHealing(unit) then
		return 100
	end
	local pct = Jazz_NamedPerkParam(unit, "NaturalHealing", "sat_debt_speed_percent", 15)
	return Max(1, 100 - (tonumber(pct) or 15))
end

--- HP / TreatWounds progress mul: +15% when Thor in squad.
function Jazz_NaturalHealingDebtSpeedMul(unit)
	if not Jazz_SquadHasNaturalHealing(unit) then
		return 100
	end
	local pct = Jazz_NamedPerkParam(unit, "NaturalHealing", "sat_debt_speed_percent", 15)
	return 100 + (tonumber(pct) or 15)
end

--- Bandage by Thor: restore patient WillPoints in [willRestoreMin, willRestoreMax].
function Jazz_NaturalHealingRestoreWill(healer, patient)
	if not patient then
		return false
	end
	if not healer or not HasPerk(healer, "NaturalHealing") then
		return false
	end
	local lo = Jazz_NamedPerkParam(healer, "NaturalHealing", "willRestoreMin", 20)
	local hi = Jazz_NamedPerkParam(healer, "NaturalHealing", "willRestoreMax", 25)
	lo = tonumber(lo) or 20
	hi = tonumber(hi) or 25
	if hi < lo then
		hi = lo
	end
	local amount = lo + InteractionRand(hi - lo + 1, "NaturalHealingWill")
	local cur = patient.WillPoints or 0
	local max_wp = patient.MaxWillPoints or cur
	patient.WillPoints = Min(max_wp, cur + amount)
	local sid = patient.session_id
	if sid and gv_UnitData and gv_UnitData[sid] and gv_UnitData[sid] ~= patient then
		gv_UnitData[sid].WillPoints = patient.WillPoints
	end
	ObjModified(patient)
	return amount
end

--- DrQ ExplodingPalm: same sat squad (or self) has the perk.
function Jazz_SquadHasExplodingPalm(unit)
	if not unit then
		return false
	end
	if HasPerk(unit, "ExplodingPalm") then
		return true
	end
	local squad_id = unit.Squad
	local squad = squad_id and gv_Squads and gv_Squads[squad_id]
	if not squad then
		return false
	end
	for _, uid in ipairs(squad.units or empty_table) do
		local u = gv_UnitData and gv_UnitData[uid]
		if not u and g_Units then
			u = g_Units[uid]
		end
		if u and HasPerk(u, "ExplodingPalm") and not (u.IsDead and u:IsDead()) then
			return true
		end
	end
	return false
end

function Jazz_ExplodingPalmDebtHoursMul(unit)
	if not Jazz_SquadHasExplodingPalm(unit) then
		return 100
	end
	local pct = Jazz_NamedPerkParam(unit, "ExplodingPalm", "sat_debt_speed_percent", 30)
	return Max(1, 100 - (tonumber(pct) or 30))
end

function Jazz_ExplodingPalmDebtSpeedMul(unit)
	if not Jazz_SquadHasExplodingPalm(unit) then
		return 100
	end
	local pct = Jazz_NamedPerkParam(unit, "ExplodingPalm", "sat_debt_speed_percent", 30)
	return 100 + (tonumber(pct) or 30)
end

--- Combined sat debt mul: Thor NaturalHealing + DrQ ExplodingPalm (stack).
function Jazz_SatDebtHoursMul(unit)
	local mul = 100
	if type(Jazz_NaturalHealingDebtHoursMul) == "function" then
		mul = MulDivRound(mul, Jazz_NaturalHealingDebtHoursMul(unit), 100)
	end
	if type(Jazz_ExplodingPalmDebtHoursMul) == "function" then
		mul = MulDivRound(mul, Jazz_ExplodingPalmDebtHoursMul(unit), 100)
	end
	return Max(1, mul)
end

function Jazz_SatDebtSpeedMul(unit)
	local mul = 100
	if type(Jazz_NaturalHealingDebtSpeedMul) == "function" then
		mul = MulDivRound(mul, Jazz_NaturalHealingDebtSpeedMul(unit), 100)
	end
	if type(Jazz_ExplodingPalmDebtSpeedMul) == "function" then
		mul = MulDivRound(mul, Jazz_ExplodingPalmDebtSpeedMul(unit), 100)
	end
	return mul
end

function Jazz_SquadBlocksWoundInfected(unit)
	return Jazz_SquadHasExplodingPalm(unit)
end

local function lExplodingPalmIsUnarmedWeapon(weapon)
	if not weapon then
		return false
	end
	if weapon.IsUnarmed then
		return true
	end
	return IsKindOf(weapon, "UnarmedWeapon")
end

local function lExplodingPalmResolveWeapon(attacker, action, results, attack_args)
	local weapon = attack_args and attack_args.weapon
	if not weapon and results then
		weapon = results.weapon
	end
	if not weapon and action and action.GetAttackWeapons and attacker then
		weapon = action:GetAttackWeapons(attacker, attack_args)
	end
	if not weapon and attacker and attacker.GetActiveWeapons then
		weapon = attacker:GetActiveWeapons("UnarmedWeapon") or attacker:GetActiveWeapons()
	end
	return weapon
end

--- Successful bare-hand hit → status by target HP% (pre-hit when damage known).
function Jazz_ExplodingPalmOnUnarmedHit(attacker, action, attack_target, results, attack_args)
	if not attacker or not HasPerk(attacker, "ExplodingPalm") then
		return false
	end
	if not IsKindOf(attack_target, "Unit") then
		return false
	end
	if results and results.miss then
		return false
	end
	if results and results.jazz_ep_done then
		return false
	end
	local aid = action and (action.id or action)
	if type(aid) == "table" then
		aid = aid.id
	end
	local weapon = lExplodingPalmResolveWeapon(attacker, action, results, attack_args)
	local unarmed = lExplodingPalmIsUnarmedWeapon(weapon)
		or aid == "UnarmedAttack"
		or aid == "ExplodingPalm"
	if not unarmed then
		return false
	end
	if action and action.ActionType and action.ActionType ~= "Melee Attack" and aid ~= "UnarmedAttack" and aid ~= "ExplodingPalm" then
		return false
	end

	local max_hp = Max(1, attack_target.MaxHitPoints or 1)
	local hp = attack_target.HitPoints or 0
	local dmg = 0
	if results then
		if type(results.unit_damage) == "table" and type(results.unit_damage[attack_target]) == "number" then
			dmg = results.unit_damage[attack_target]
		elseif type(results.total_damage) == "number" then
			dmg = results.total_damage
		end
	end
	if dmg > 0 then
		hp = Min(max_hp, hp + dmg)
	end
	local pct = MulDivRound(hp, 100, max_hp)
	if results then
		results.jazz_ep_done = true
	end
	if attack_target.IsDead and attack_target:IsDead() and pct > 20 then
		return false
	end
	if pct <= 20 then
		if not (attack_target.IsDead and attack_target:IsDead()) then
			attack_target:AddStatusEffect("KnockDown")
			attack_target:AddStatusEffect("Unconscious")
		end
		return "ko"
	elseif pct <= 35 then
		if CharacterEffectDefs and CharacterEffectDefs.Concussion then
			attack_target:AddStatusEffect("Concussion")
		end
		return "concussion"
	elseif pct <= 50 then
		if type(JazzApplyTrauma) == "function" then
			JazzApplyTrauma(attack_target, "Ribs", "Medium")
		end
		return "ribs"
	elseif pct <= 65 then
		if type(JazzApplyTrauma) == "function" then
			JazzApplyTrauma(attack_target, "Arms", "Medium")
		end
		return "arms"
	elseif pct <= 80 then
		if type(JazzApplyTrauma) == "function" then
			JazzApplyTrauma(attack_target, "Legs", "Medium")
		end
		return "legs"
	else
		if type(JazzApplyTrauma) == "function" then
			JazzApplyTrauma(attack_target, "Ribs", "Light")
		end
		attack_target:AddStatusEffect("Pain")
		return "groin"
	end
end

--- Refresh CE reactions on live units (saves hired under vanilla empty-reaction ExplodingPalm).
function Jazz_ExplodingPalmRefreshUnitPerk(unit)
	if not unit or not unit.AddStatusEffect then
		return false
	end
	if not HasPerk(unit, "ExplodingPalm") then
		return false
	end
	if unit.RemoveStatusEffect then
		unit:RemoveStatusEffect("ExplodingPalm", "all")
	end
	unit:AddStatusEffect("ExplodingPalm")
	return true
end

--- Flay MakeThemBleed: count distinct visible enemies with any bleeding tier.
function Jazz_MakeThemBleedCountVisible(unit)
	if not unit or not unit.GetVisibleEnemies then
		return 0
	end
	local n = 0
	for _, u in ipairs(unit:GetVisibleEnemies() or empty_table) do
		if IsValid(u) and not (u.IsDead and u:IsDead()) then
			if u:HasStatusEffect("Bleeding")
				or u:HasStatusEffect("BleedingMedium")
				or u:HasStatusEffect("BleedingHeavy")
			then
				n = n + 1
			end
		end
	end
	return n
end

--- HUD stacks = min(5, visible bleeders); remove buff when 0.
function Jazz_MakeThemBleedSyncBuff(unit)
	if not unit or not HasPerk(unit, "MakeThemBleed") then
		return false
	end
	if not g_Combat then
		if unit.HasStatusEffect and unit:HasStatusEffect("Jazz_MakeThemBleedBuff") then
			unit:RemoveStatusEffect("Jazz_MakeThemBleedBuff", "all")
		end
		return false
	end
	local n = Min(5, Jazz_MakeThemBleedCountVisible(unit) or 0)
	if unit.HasStatusEffect and unit:HasStatusEffect("Jazz_MakeThemBleedBuff") then
		unit:RemoveStatusEffect("Jazz_MakeThemBleedBuff", "all")
	end
	if n <= 0 then
		return false
	end
	unit:AddStatusEffect("Jazz_MakeThemBleedBuff", n)
	return true
end

function Jazz_MakeThemBleedSyncAll()
	local units = g_Units or empty_table
	for _, u in pairs(units) do
		if IsValid(u) and HasPerk(u, "MakeThemBleed") then
			Jazz_MakeThemBleedSyncBuff(u)
		end
	end
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

g_JAZZ_ExplodingPalmSigHidden = rawget(_G, "g_JAZZ_ExplodingPalmSigHidden") or false

local function lInstallExplodingPalmPassiveOnly()
	-- Always configure Passive CA (ModItem may leave vanilla Execute/UIBegin + 108 dual icon).
	local ca = CombatActions and CombatActions.ExplodingPalm
	if not ca then
		return
	end
	local def = CharacterEffectDefs and CharacterEffectDefs.ExplodingPalm
	local cls = g_Classes and g_Classes.ExplodingPalm
	if def and cls then
		if not def.DisplayName and cls.DisplayName then
			def.DisplayName = cls.DisplayName
		end
		if (not def.Description or def.Description == "") and cls.Description then
			def.Description = cls.Description
		end
		if cls.unit_reactions and (not def.unit_reactions or #def.unit_reactions == 0) then
			def.unit_reactions = cls.unit_reactions
		end
	end
	ca.ShowIn = "SignatureAbilities"
	ca.ActionType = "Passive"
	ca.AimType = "none"
	ca.ActionPoints = 0
	ca.CostBasedOnWeapon = false
	ca.IsTargetableAttack = false
	ca.Icon = "Mod/e6L4ECj/Perks/SignatureAbilities/ExplodingPalm.png"
	ca.GetActionDisplayName = function(self, units)
		return GetSignatureActionDisplayName(self)
	end
	ca.GetActionDescription = function(self, units)
		return GetSignatureActionDescription(self)
	end
	ca.GetAPCost = function(self, unit, args)
		return 0
	end
	ca.GetUIState = function(self, units, args)
		local unit = units and units[1]
		if not unit or not HasPerk(unit, "ExplodingPalm") then
			return "hidden"
		end
		return "enabled"
	end
	ca.GetActionResults = function(self, unit, args)
		return {}
	end
	ca.Run = function(self, unit, ap, ...)
		return false
	end
	ca.Execute = function(self, units, args)
	end
	ca.UIBegin = function(self, units, args)
	end
	rawset(_G, "g_JAZZ_ExplodingPalmSigConfigured", true)
	rawset(_G, "g_JAZZ_ExplodingPalmSigHidden", true)
end

local function lInstallExplodingPalmMeleeWrap()
	-- After vanilla OnAttack reactions (may be stale CE); idempotent via results.jazz_ep_done.
	if rawget(_G, "g_JAZZ_ExplodingPalmMeleeWrapped") then
		return
	end
	if type(Unit) ~= "table" or type(Unit.OnAttack) ~= "function" then
		return
	end
	rawset(_G, "g_JAZZ_ExplodingPalmMeleeBase", Unit.OnAttack)
	rawset(_G, "g_JAZZ_ExplodingPalmMeleeWrapped", true)
	function Unit:OnAttack(action, target, results, attack_args, ...)
		local ret = g_JAZZ_ExplodingPalmMeleeBase(self, action, target, results, attack_args, ...)
		if HasPerk(self, "ExplodingPalm") and type(Jazz_ExplodingPalmOnUnarmedHit) == "function" then
			Jazz_ExplodingPalmOnUnarmedHit(self, action, target, results, attack_args)
		end
		return ret
	end
end

local function lInstallSteroidPunchPassiveOnly()
	-- Convert vanilla smash CA into Passive hotbar icon (knockback is on all unarmed hits).
	-- Passive hotbar uses SetColumns(1) → Icon must be 54×54 single tile, NOT 108×54 dual.
	-- AimType must be "none" — leftover AimType="melee" makes CombatActionRollover append
	-- "<error>No enemies in melee range</error>" / RU «Цели вне досягаемости…».
	local ca = CombatActions and CombatActions.SteroidPunch
	if not ca then
		return
	end
	if type(ca.GetUIState) == "function" and not rawget(_G, "g_JAZZ_SteroidPunchUIStateBase") then
		rawset(_G, "g_JAZZ_SteroidPunchUIStateBase", ca.GetUIState)
	end
	-- ModItem CharacterEffectDefs entry can miss DisplayName; class/companion has the T().
	local def = CharacterEffectDefs and CharacterEffectDefs.SteroidPunch
	local cls = g_Classes and g_Classes.SteroidPunch
	if def and cls then
		if not def.DisplayName and cls.DisplayName then
			def.DisplayName = cls.DisplayName
		end
		if (not def.Description or def.Description == "") and cls.Description then
			def.Description = cls.Description
		end
	end
	ca.ShowIn = "SignatureAbilities"
	ca.ActionType = "Passive"
	ca.AimType = "none"
	ca.ActionPoints = 0
	ca.CostBasedOnWeapon = false
	ca.IsAimableAttack = false
	ca.IsTargetableAttack = false
	ca.Icon = "Mod/e6L4ECj/Perks/SignatureAbilities/SteroidPunch.png"
	ca.GetActionDisplayName = function(self, units)
		return GetSignatureActionDisplayName(self)
	end
	ca.GetActionDescription = function(self, units)
		return GetSignatureActionDescription(self)
	end
	ca.GetAPCost = function(self, unit, args)
		return 0
	end
	ca.GetUIState = function(self, units, args)
		local unit = units and units[1]
		if not unit or not HasPerk(unit, "SteroidPunch") then
			return "hidden"
		end
		return "enabled"
	end
	ca.GetActionResults = function(self, unit, args)
		return {}
	end
	ca.GetAnyTarget = function(self, units)
		return false
	end
	ca.GetTargets = function(self, units)
		return {}
	end
	ca.Run = function(self, unit, ap, ...)
		return false
	end
	ca.Execute = function(self, units, args)
	end
	ca.UIBegin = function(self, units, args)
	end
	rawset(_G, "g_JAZZ_SteroidPunchSigHidden", true) -- configured as Passive display
end

local function lInstallSteroidBurningDotReduce()
	-- Burning DoT uses EnvEffectBurningTick → TakeDirectDamage (not OnCalcDamageAndEffects).
	if rawget(_G, "g_JAZZ_SteroidBurningTickWrapped") then
		return
	end
	local base = rawget(_G, "EnvEffectBurningTick")
	if type(base) ~= "function" then
		return
	end
	rawset(_G, "g_JAZZ_EnvEffectBurningTickBase", base)
	rawset(_G, "EnvEffectBurningTick", function(unit, voxels, combat_moment)
		if not (unit and HasPerk(unit, "SteroidPunch") and unit.TakeDirectDamage) then
			return g_JAZZ_EnvEffectBurningTickBase(unit, voxels, combat_moment)
		end
		local take = unit.TakeDirectDamage
		unit.TakeDirectDamage = function(self, damage, ...)
			if type(damage) == "number" then
				damage = MulDivRound(damage, 70, 100)
			end
			return take(self, damage, ...)
		end
		local ok, err = pcall(g_JAZZ_EnvEffectBurningTickBase, unit, voxels, combat_moment)
		unit.TakeDirectDamage = take
		if not ok then
			error(err)
		end
	end)
	rawset(_G, "g_JAZZ_SteroidBurningTickWrapped", true)
end

local function lInstallNamedPerks006Ops()
	lInstallJackOfAllArrivingThresh()
	lInstallSteroidPunchPassiveOnly()
	lInstallExplodingPalmPassiveOnly()
	lInstallExplodingPalmMeleeWrap()
	lInstallSteroidBurningDotReduce()

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

	-- Wolf JackOfAllTrades: vanilla SectorOperation.ProgressPerTick already applies
	-- CharacterEffectDefs.JackOfAllTrades activityDurationMod (+33% progress). Do NOT
	-- wrap GetOperationTimeLeft — that double-dipped and renaming the param to
	-- jazz_ops_bonus made ResolveValue("activityDurationMod") nil → MulDivRound assert
	-- on every Wolf op assign (GetOperationTimeLeftAssign → ProgressPerTick).
	-- Arriving hire co-group stays in SatelliteSquad.LocalSetArrivingMercSector.

	rawset(_G, "g_JAZZ_NamedPerks006OpsWrapped", true)
end


g_JAZZ_NamedPerks006SignaturesWrapped = rawget(_G, "g_JAZZ_NamedPerks006SignaturesWrapped") or false

local function lEnsureTheGrimRechargeParam()
	-- ResolveValue reads g_PresetParamCache — Parameters alone is not enough (same as BulletHell).
	local ca = CombatActions and CombatActions.TheGrim
	if not ca then
		return false
	end
	local need = tonumber(rawget(_G, "Jazz_TheGrimKillsToRecharge")) or 5
	if need < 2 then
		need = 5
		rawset(_G, "Jazz_TheGrimKillsToRecharge", need)
	end
	local params = ca.Parameters or {}
	local has = false
	for _, p in ipairs(params) do
		if p and p.Name == "recharge_on_kill" then
			p.Value = need
			has = true
			break
		end
	end
	if not has then
		params[#params + 1] = PlaceObj("PresetParamNumber", {
			"Name", "recharge_on_kill",
			"Value", need,
			"Tag", "<recharge_on_kill>",
		})
		ca.Parameters = params
	end
	if type(rawget(_G, "g_PresetParamCache")) ~= "table" then
		return false
	end
	local cache = g_PresetParamCache[ca]
	if not cache then
		cache = {}
		g_PresetParamCache[ca] = cache
	end
	cache.recharge_on_kill = need

	if type(ca.GetActionDescription) == "function" and not rawget(_G, "g_JAZZ_TheGrimGetActionDescriptionBase") then
		rawset(_G, "g_JAZZ_TheGrimGetActionDescriptionBase", ca.GetActionDescription)
		ca.GetActionDescription = function(self, units)
			local desc = g_JAZZ_TheGrimGetActionDescriptionBase(self, units)
			local unit = units and units[1]
			local rec = unit and unit.GetSignatureRecharge and unit:GetSignatureRecharge("TheGrim")
			local need_desc = self:ResolveValue("recharge_on_kill") or (rawget(_G, "Jazz_TheGrimKillsToRecharge") or 5)
			if rec and rec.on_kill and (rec.kills_needed or need_desc) > 1 then
				local done = rec.kills_done or 0
				local req = rec.kills_needed or need_desc
				return desc
					.. T({
						890000000009941,
						"<newline><newline>Перезарядка: <em><done>/<need></em> убийств.",
						done = done,
						need = req,
					})
			end
			return desc
				.. T({
					890000000009940,
					"<newline><newline>Перезаряжается после <em><need></em> убийств (другой атакой).",
					need = need_desc,
				})
		end
	end
	return true
end

--- Public ensure (ModsReloaded / DAP): TheGrim recharge_on_kill cache = Jazz_TheGrimKillsToRecharge.
function Jazz_EnsureTheGrimRechargeOnKill()
	return lEnsureTheGrimRechargeParam()
end

local function lInstallTheGrimMultiKillRecharge()
	lEnsureTheGrimRechargeParam()
	if not Unit or type(Unit.AddSignatureRechargeTime) ~= "function" then
		return
	end
	-- ModsReloaded can restore vanilla Unit methods while leave wrap flags set — reinstall if lost.
	local baseAdd = rawget(_G, "g_JAZZ_AddSignatureRechargeTimeBase")
	if rawget(_G, "g_JAZZ_TheGrimRechargeWrapped")
		and type(baseAdd) == "function"
		and Unit.AddSignatureRechargeTime ~= baseAdd
	then
		return
	end
	rawset(_G, "g_JAZZ_AddSignatureRechargeTimeBase", Unit.AddSignatureRechargeTime)
	rawset(_G, "g_JAZZ_UpdateSignatureRechargesBase", Unit.UpdateSignatureRecharges)
	rawset(_G, "g_JAZZ_TheGrimRechargeWrapped", true)

	function Unit:AddSignatureRechargeTime(id, duration, recharge_on_kill)
		g_JAZZ_AddSignatureRechargeTimeBase(self, id, duration, recharge_on_kill and true or false)
		if id ~= "TheGrim" then
			return
		end
		local rec = self:GetSignatureRecharge("TheGrim")
		if not (rec and rec.on_kill) then
			return
		end
		local ca = CombatActions and CombatActions.TheGrim
		local need = (ca and ca.ResolveValue and ca:ResolveValue("recharge_on_kill"))
			or (rawget(_G, "Jazz_TheGrimKillsToRecharge") or 5)
		need = tonumber(need) or 5
		if need > 1 then
			rec.kills_needed = need
			rec.kills_done = 0
		end
	end

	function Unit:UpdateSignatureRecharges(trigger)
		local n = 1
		if trigger == "kill" then
			n = tonumber(rawget(_G, "g_JAZZ_PendingSigKillCount")) or 1
			if n < 1 then
				n = 1
			end
			local recharges = self.signature_recharge or empty_table
			for i = #recharges, 1, -1 do
				local recharge = recharges[i]
				local need = recharge and recharge.kills_needed or 1
				if recharge and recharge.on_kill and need > 1 then
					recharge.kills_done = (recharge.kills_done or 0) + n
					if recharge.kills_done < need then
						-- Keep CD; block vanilla one-kill clear for this entry.
						recharge.on_kill = false
						recharge._jazz_multikill_hold = true
					end
					ObjModified(self)
				end
			end
		end
		g_JAZZ_UpdateSignatureRechargesBase(self, trigger)
		if trigger == "kill" then
			local recharges = self.signature_recharge or empty_table
			for i = 1, #recharges do
				local recharge = recharges[i]
				if recharge and recharge._jazz_multikill_hold then
					recharge.on_kill = true
					recharge._jazz_multikill_hold = nil
				end
			end
		end
		rawset(_G, "g_JAZZ_PendingSigKillCount", 0)
	end
end

function OnMsg.OnKill(attacker, killed_units)
	local n = #(killed_units or empty_table)
	if n < 1 then
		n = 1
	end
	rawset(_G, "g_JAZZ_PendingSigKillCount", n)
end

local function lEnsureBulletHellRechargeOnKill()
	-- Spike BulletHell: CD clears on kill (UNITS-006). Vanilla CA has no recharge_on_kill param;
	-- injecting into Parameters alone is not enough — ResolveValue reads g_PresetParamCache.
	local bh = CombatActions and CombatActions.BulletHell
	if not bh then
		return
	end
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
	if type(rawget(_G, "g_PresetParamCache")) ~= "table" then
		return
	end
	local cache = g_PresetParamCache[bh]
	if not cache then
		cache = {}
		g_PresetParamCache[bh] = cache
	end
	cache.recharge_on_kill = 1
end

local function lEnsureKillingWindGritParam()
	-- Fauda: ResolveValue("gritPerEnemyHit") can be nil if cache miss → arithmetic error, no Grit.
	local def = CharacterEffectDefs and CharacterEffectDefs.KillingWind
	if not def then
		return
	end
	if type(rawget(_G, "g_PresetParamCache")) ~= "table" then
		return
	end
	local cache = g_PresetParamCache[def]
	if not cache then
		cache = {}
		g_PresetParamCache[def] = cache
	end
	if cache.gritPerEnemyHit == nil then
		cache.gritPerEnemyHit = 8
	end
end

local lInstallHawksEyeOverwatchCost

local function lInstallNamedPerks006Signatures()
	-- Always refresh BulletHell cache (wrapped flag must not skip it).
	lEnsureBulletHellRechargeOnKill()
	lEnsureKillingWindGritParam()
	lInstallHawksEyeOverwatchCost()

	if rawget(_G, "g_JAZZ_NamedPerks006SignaturesWrapped") then
		lInstallTheGrimMultiKillRecharge()
		return
	end

	lInstallTheGrimMultiKillRecharge()
	rawset(_G, "g_JAZZ_NamedPerks006SignaturesWrapped", true)
end

local function lNamedPerks006OnCombatStart_Signatures()
end

local function lNamedPerks006OnTurnStart_Signatures()
end

g_JAZZ_NamedPerks006EconomyWrapped = rawget(_G, "g_JAZZ_NamedPerks006EconomyWrapped") or false
g_JAZZ_FloBuySellBase_BR = rawget(_G, "g_JAZZ_FloBuySellBase_BR") or false
g_JAZZ_FloBuySellBase_Cash = rawget(_G, "g_JAZZ_FloBuySellBase_Cash") or false
g_JAZZ_StaticPartsBase_ModCost = rawget(_G, "g_JAZZ_StaticPartsBase_ModCost") or false
g_JAZZ_StaticPartsBase_ItemsCalc = rawget(_G, "g_JAZZ_StaticPartsBase_ItemsCalc") or false
g_JAZZ_CraftPartsDiscountWrapped = rawget(_G, "g_JAZZ_CraftPartsDiscountWrapped") or false
g_JAZZ_CraftPartsDiscountFn = rawget(_G, "g_JAZZ_CraftPartsDiscountFn") or false
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

g_JAZZ_HawksEyeOverwatchWrapped = rawget(_G, "g_JAZZ_HawksEyeOverwatchWrapped") or false
g_JAZZ_HawksEyeOverwatchBase = rawget(_G, "g_JAZZ_HawksEyeOverwatchBase") or false

local function lHawksEyeIsSniper(weapon)
	if not weapon then
		return false
	end
	return IsKindOf(weapon, "SniperRifle") or weapon.WeaponType == "Sniper"
end

function Jazz_ApplyHawksEyeSuppression(attacker, suppressionbonus)
	if not attacker or not HasPerk(attacker, "HawksEye") then
		return suppressionbonus
	end
	local w = attacker.GetActiveWeapons and attacker:GetActiveWeapons("Firearm")
	if lHawksEyeIsSniper(w) then
		return (suppressionbonus or 100) * 2
	end
	return suppressionbonus
end

function Jazz_HawksEyeSniperOverwatchAP(unit, weapon)
	if not unit or not HasPerk(unit, "HawksEye") then
		return
	end
	weapon = weapon or (unit.GetActiveWeapons and unit:GetActiveWeapons("Firearm"))
	if not lHawksEyeIsSniper(weapon) then
		return
	end
	if weapon.PreparedAttackType ~= "Overwatch" and weapon.PreparedAttackType ~= "Both" then
		return
	end
	local n = Jazz_NamedPerkParam(unit, "HawksEye", "overwatchCostOverwrite", 1)
	return n * const.Scale.AP
end

lInstallHawksEyeOverwatchCost = function()
	if rawget(_G, "g_JAZZ_HawksEyeOverwatchWrapped") then
		return
	end
	local ow = CombatActions and CombatActions.Overwatch
	if not ow or type(ow.GetAPCost) ~= "function" then
		return
	end
	rawset(_G, "g_JAZZ_HawksEyeOverwatchBase", ow.GetAPCost)
	rawset(_G, "g_JAZZ_HawksEyeOverwatchWrapped", true)
	function ow.GetAPCost(self, unit, args)
		if not (args and args.action_cost_only) then
			local weapon = self:GetAttackWeapons(unit, args)
			local ap = Jazz_HawksEyeSniperOverwatchAP(unit, weapon)
			if ap then
				return ap, ap
			end
		end
		return g_JAZZ_HawksEyeOverwatchBase(self, unit, args)
	end
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
	Jazz_InstallCraftPartsDiscountWrap()
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

	-- Static repair/craft Parts + Barry CraftAmmo/CraftExplosives −craft_discount%.
	Jazz_InstallCraftPartsDiscountWrap()

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
	if not unit then
		return 0
	end
	if not HasPerk(unit, "DesignerExplosives") then
		-- UnitData / live Unit may lag HasPerk; StatusEffect is enough.
		if not (unit.HasStatusEffect and unit:HasStatusEffect("DesignerExplosives")) then
			return 0
		end
	end
	local disc = Jazz_NamedPerkParam(unit, "DesignerExplosives", "craft_discount", 30)
	if type(disc) ~= "number" or disc < 1 then
		disc = 30
	end
	return disc
end

function Jazz_IsCraftAmmoOrExplosives(operation_id)
	return operation_id == "CraftAmmo" or operation_id == "CraftExplosives"
end

-- Sector-wide: assigned crafter or Idle Barry in the same sector.
function Jazz_BarryCraftDiscountForSector(sector_id, operation_id)
	if not sector_id or not Jazz_IsCraftAmmoOrExplosives(operation_id) then
		return 0
	end
	local barry = 0
	if type(GetOperationProfessionals) == "function" then
		for _, merc in ipairs(GetOperationProfessionals(sector_id, operation_id) or empty_table) do
			barry = Max(barry, Jazz_BarryCraftDiscountPercent(merc))
		end
	end
	if barry <= 0 and type(GetPlayerMercsInSector) == "function" then
		for _, uid in ipairs(GetPlayerMercsInSector(sector_id) or empty_table) do
			local u = gv_UnitData and gv_UnitData[uid]
			if not u and g_Units then
				u = g_Units[uid]
			end
			barry = Max(barry, Jazz_BarryCraftDiscountPercent(u))
		end
	end
	return barry
end

function Jazz_ApplyBarryCraftPartsAmount(sector_id, operation_id, amount)
	if type(amount) ~= "number" or amount <= 0 then
		return amount
	end
	local disc = Jazz_BarryCraftDiscountForSector(sector_id, operation_id)
	if disc <= 0 then
		return amount
	end
	return Max(0, MulDivRound(amount, 100 - disc, 100))
end

function Jazz_CraftIngredientAmount(ing, sector_id, operation_id)
	if not ing then
		return 0
	end
	local amount = ing.amount or 0
	if ing.item == "Parts" then
		return Jazz_ApplyBarryCraftPartsAmount(sector_id, operation_id, amount)
	end
	return amount
end

function Jazz_CraftRecipeIngredients(recipe, sector_id, operation_id)
	if not recipe or not recipe.Ingredients then
		return empty_table
	end
	if Jazz_BarryCraftDiscountForSector(sector_id, operation_id) <= 0 then
		return recipe.Ingredients
	end
	local out = {}
	for i, ing in ipairs(recipe.Ingredients) do
		if ing.item == "Parts" then
			out[i] = {
				item = ing.item,
				amount = Jazz_ApplyBarryCraftPartsAmount(sector_id, operation_id, ing.amount or 0),
			}
		else
			out[i] = ing
		end
	end
	return out
end

--- Ensure craft_discount is in g_PresetParamCache (ResolveValue nil → no UI tag / wrap miss).
function Jazz_EnsureDesignerExplosivesCraftParam()
	local def = CharacterEffectDefs and CharacterEffectDefs.DesignerExplosives
	if not def then
		return
	end
	local cls = g_Classes and g_Classes.DesignerExplosives
	if cls then
		if not def.DisplayName and cls.DisplayName then
			def.DisplayName = cls.DisplayName
		end
		if cls.Description then
			def.Description = cls.Description
		end
	end
	if type(rawget(_G, "g_PresetParamCache")) ~= "table" then
		return
	end
	local cache = g_PresetParamCache[def]
	if not cache then
		cache = {}
		g_PresetParamCache[def] = cache
	end
	if cache.craft_discount == nil then
		cache.craft_discount = 30
	end
	if cache.hoursToProduce == nil then
		cache.hoursToProduce = 168
	end
	if cache.amountToProduce == nil then
		cache.amountToProduce = 2
	end
end

-- Single wrap for SectorOperation_ItemsCalcRes: Static Parts + Barry craft + Cord repair.
-- Retries until the vanilla calc exists (DataLoaded order).
-- NOTE: jazz Code/System_SectorOperations.lua redefines SectorOperation_ItemsCalcRes after
-- NamedPerks in metadata.code — discounts are applied inside that redefine. This wrap is a
-- safety net if SectorOperations is absent/dormant; it must rebind when overwritten.
function Jazz_InstallCraftPartsDiscountWrap()
	-- Prefer System_SectorOperations inlined discounts; do not wrap over them.
	if rawget(_G, "g_JAZZ_SectorOpsCraftDiscountInlined") then
		Jazz_EnsureDesignerExplosivesCraftParam()
		return true
	end
	local calc = rawget(_G, "SectorOperation_ItemsCalcRes")
	if type(calc) ~= "function" then
		return false
	end
	local wrapped_fn = rawget(_G, "g_JAZZ_CraftPartsDiscountFn")
	if wrapped_fn and calc == wrapped_fn then
		return true
	end
	-- Prefer unwrapped vanilla / earliest captured base, unless a later Code file replaced us.
	local base = calc
	if wrapped_fn and calc ~= wrapped_fn then
		base = calc
	elseif type(rawget(_G, "g_JAZZ_StaticPartsBase_ItemsCalc")) == "function" then
		base = g_JAZZ_StaticPartsBase_ItemsCalc
	end
	rawset(_G, "g_JAZZ_StaticPartsBase_ItemsCalc", base)
	rawset(_G, "g_JAZZ_BarryCraftBase_ItemsCalc", base)
	local function discount_fn(sector_id, operation_id)
		local parts = base(sector_id, operation_id)
		if type(parts) ~= "number" or parts <= 0 then
			return parts
		end
		if rawget(_G, "g_JAZZ_SectorOpsCraftDiscountInlined") then
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
		if operation_id == "CraftAmmo" or operation_id == "CraftExplosives" then
			local barry = 0
			for _, merc in ipairs(mercs) do
				barry = Max(barry, Jazz_BarryCraftDiscountPercent(merc))
			end
			if barry <= 0 and type(GetPlayerMercsInSector) == "function" then
				for _, uid in ipairs(GetPlayerMercsInSector(sector_id) or empty_table) do
					local u = gv_UnitData and gv_UnitData[uid]
					barry = Max(barry, Jazz_BarryCraftDiscountPercent(u))
				end
			end
			if barry > 0 then
				parts = Max(0, MulDivRound(parts, 100 - barry, 100))
			end
		elseif operation_id == "RepairItems" or operation_id == "Repair" then
			for _, merc in ipairs(mercs) do
				if Jazz_CordInBarCity(merc) then
					local disc = Jazz_NamedPerkParam(merc, "Jazz_Perk_Cord", "repair_parts_discount", 10)
					parts = Max(0, MulDivRound(parts, 100 - disc, 100))
					break
				end
			end
		end
		return parts
	end
	rawset(_G, "SectorOperation_ItemsCalcRes", discount_fn)
	rawset(_G, "g_JAZZ_CraftPartsDiscountFn", discount_fn)
	rawset(_G, "g_JAZZ_CraftPartsDiscountWrapped", true)
	Jazz_EnsureDesignerExplosivesCraftParam()
	return true
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
	-- Ira / craft-Parts wraps may need SectorOperations after first attempt.
	Jazz_EnsureDesignerExplosivesCraftParam()
	Jazz_InstallCraftPartsDiscountWrap()
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

-- List2 Larry: grenade/explosive damage + bleed live in Jazz_InstallDangerCloseExplosionWrap
-- (ExplosionPrecalcDamageAndStatusEffects). Firearm OnAttack path retired.
function Jazz_DangerCloseOnAttack(attacker, action, target, results, attack_args)
	return
end

--- Nil-safe List2 DangerClose for grenades/ordnance/traps.
--- Vanilla Bombard does ResolveValue("rangeThreshold")*SlabSizeX with no guard → Larry cannot throw.
function Jazz_InstallDangerCloseExplosionWrap()
	if rawget(_G, "g_JAZZ_DangerCloseExplosionWrapped") then
		return
	end
	if type(rawget(_G, "ExplosionPrecalcDamageAndStatusEffects")) ~= "function" then
		return
	end
	function ExplosionPrecalcDamageAndStatusEffects(self, attacker, target, attack_pos, damage, hit, effect, attack_args, record_breakdown, action, prediction)
		local dmg_mod, effects
		local is_unit = IsKindOf(target, "Unit")
		if is_unit then
			dmg_mod = hit.explosion_center and self.CenterUnitDamageMod or self.AreaUnitDamageMod
			effects = hit.explosion_center and self.CenterAppliedEffects or self.AreaAppliedEffects
		else
			dmg_mod = hit.explosion_center and self.CenterObjDamageMod or self.AreaObjDamageMod
		end
		damage = MulDivRound(damage, dmg_mod, 100)

		local bleed_stacks_to_add = 0
		if attacker and HasPerk(attacker, "DangerClose") and attack_pos then
			local min_r = Jazz_NamedPerkParam(attacker, "DangerClose", "minRange", 8)
			local bonus = Jazz_NamedPerkParam(attacker, "DangerClose", "damageBonus", 40)
			if not bonus or bonus == 0 then
				bonus = Jazz_NamedPerkParam(attacker, "DangerClose", "damageMod", 40)
			end
			local dist = DivRound(attacker:GetDist(attack_pos), const.SlabSizeX)
			if dist >= min_r then
				damage = damage + MulDivRound(damage, bonus, 100)
			end
			if is_unit then
				local env = false
				if type(JazzIsEnvironmentalAoeHit) == "function" then
					env = JazzIsEnvironmentalAoeHit(hit)
				else
					local aoe = (hit and hit.aoe_type) or self.aoeType or "none"
					env = aoe == "smoke" or aoe == "teargas" or aoe == "toxicgas" or aoe == "fire"
				end
				if not env then
					bleed_stacks_to_add = Jazz_NamedPerkParam(attacker, "DangerClose", "bleed_stacks", 2) or 0
				end
			end
		end

		BaseWeapon.PrecalcDamageAndStatusEffects(self, attacker, target, attack_pos, damage, hit, effect, attack_args, record_breakdown, action, prediction)
		if is_unit then
			for _, eff in ipairs(effects) do
				table.insert_unique(hit.effects, eff)
			end
			if bleed_stacks_to_add > 0 and hit.effects then
				for _ = 1, bleed_stacks_to_add do
					table.insert(hit.effects, "Bleeding")
				end
			end
		end
	end
	if rawget(_G, "Grenade") then
		Grenade.PrecalcDamageAndStatusEffects = ExplosionPrecalcDamageAndStatusEffects
	end
	if rawget(_G, "Ordnance") then
		Ordnance.PrecalcDamageAndStatusEffects = ExplosionPrecalcDamageAndStatusEffects
	end
	rawset(_G, "g_JAZZ_DangerCloseExplosionWrapped", true)
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

-- MD BuildingConfidence: ensure ±heal-by-level-diff after OnCalcHealAmount (combat + sat UnitData).
local function lInstallBuildingConfidenceHeal()
	if rawget(_G, "g_JAZZ_BuildingConfidenceHealWrapped") then
		return
	end
	if type(Unit) ~= "table" or type(Unit.CalcHealAmount) ~= "function" then
		return
	end
	rawset(_G, "g_JAZZ_BuildingConfidenceHealBase", Unit.CalcHealAmount)
	rawset(_G, "g_JAZZ_BuildingConfidenceHealWrapped", true)
	function Unit:CalcHealAmount(medkit, target)
		if not medkit then
			return 0
		end
		local base_heal = CombatActions.Bandage:ResolveValue("base_heal")
		local medical_heal = CombatActions.Bandage:ResolveValue("medical_max_heal")
		local heal_percent = base_heal + MulDivRound(self.Medical or 0, medical_heal, 100)
		local data = {
			heal_amount = 0,
			heal_percent = heal_percent,
			self_heal_percent = 50,
			heal_modifier = 100,
		}
		self:CallReactions("OnCalcHealAmount", target, self, medkit, data)
		if target ~= self and IsKindOf(target, "UnitBase") then
			target:CallReactions("OnCalcHealAmount", target, self, medkit, data)
		end
		Jazz_BuildingConfidenceApplyHealMod(self, target, data)
		heal_percent = data.heal_percent
		if target == self then
			heal_percent = MulDivRound(heal_percent, data.self_heal_percent, 100)
		end
		local heal_mod = MulDivRound(heal_percent, data.heal_modifier, 100)
		local max_hp = (IsValid(target) and target.MaxHitPoints) or self.MaxHitPoints
		return data.heal_amount + MulDivRound(max_hp, heal_mod, 100), MulDivRound(heal_percent, 100, Max(1, heal_mod))
	end
	local ud = rawget(_G, "UnitData")
	if type(ud) == "table" then
		ud.CalcHealAmount = Unit.CalcHealAmount
	end
end

local function lNamedPerks006OnCombatStart_SectionD()
	for _, u in ipairs(g_Units or empty_table) do
		if IsValid(u) and u.SetEffectValue then
			u:SetEffectValue("Jazz_BennyDecoyCd", nil)
			-- Simon starts charged (no CD) each combat; CD set after use until kill.
			u:SetEffectValue("Jazz_SimonPerfectCd", nil)
			u:SetEffectValue("Jazz_PierreRecruitUsed", nil)
		end
		if IsValid(u) and type(Jazz_ExplodingPalmRefreshUnitPerk) == "function" then
			Jazz_ExplodingPalmRefreshUnitPerk(u)
		end
	end
end

-- Vanilla WeGotThis (Gus Tango Down) does gv_Squads[target.Squad].units with no nil check.
-- NPC villains (Ghost, MercenaryCaptain, ErnyVillage_Boss) copy the perk; Squad is false.
local function lWeGotThisOnUnitKill(self, target, killedUnits)
	if not target or not target.CanActivatePerk or not target:CanActivatePerk(self.class) then
		return
	end
	local tempHp = (self.ResolveValue and self:ResolveValue("tempHp")) or 0
	local applied = false
	local squad_id = target.Squad
	local squad = squad_id and gv_Squads and gv_Squads[squad_id]
	if squad and squad.units then
		for _, id in ipairs(squad.units) do
			local unit = g_Units and g_Units[id]
			if unit and unit.ApplyTempHitPoints then
				unit:ApplyTempHitPoints(tempHp)
				applied = true
			end
		end
	end
	if not applied then
		for _, unit in ipairs(target.team and target.team.units or empty_table) do
			if IsValid(unit) and not unit:IsDead() and unit.ApplyTempHitPoints then
				unit:ApplyTempHitPoints(tempHp)
			end
		end
	end
	if target.ActivatePerk then
		target:ActivatePerk(self.class)
	end
end

local function lPatchWeGotThisKillReactions(reactions)
	if not reactions then
		return
	end
	for _, r in ipairs(reactions) do
		if r and r.Event == "OnUnitKill" then
			r.Handler = lWeGotThisOnUnitKill
		end
	end
end

function Jazz_InstallWeGotThisSquadGuard()
	local cls = g_Classes and g_Classes.WeGotThis
	if cls then
		lPatchWeGotThisKillReactions(cls.unit_reactions)
	end
	local def = CharacterEffectDefs and CharacterEffectDefs.WeGotThis
	if def then
		lPatchWeGotThisKillReactions(def.unit_reactions)
	end
	for _, unit in ipairs(g_Units or empty_table) do
		if IsValid(unit) and unit.GetStatusEffect then
			local eff = unit:GetStatusEffect("WeGotThis")
			if eff then
				lPatchWeGotThisKillReactions(eff.unit_reactions)
			end
		end
	end
	rawset(_G, "g_JAZZ_WeGotThisSquadGuardWrapped", true)
end

local function lInstallAllNamedPerks006()
	lInstallNamedPerks006()
	lInstallNamedPerks006Ops()
	lInstallNamedPerks006Signatures()
	lInstallNamedPerks006Economy()
	lInstallNamedPerks006Satellite()
	lInstallNamedPerks006SectionD()
	lInstallBuildingConfidenceHeal()
	Jazz_InstallDangerCloseExplosionWrap()
	Jazz_InstallWeGotThisSquadGuard()
end

function Jazz_NamedPerks006OnCombatStart()
	lNamedPerks006OnCombatStart_Signatures()
	lNamedPerks006OnCombatStart_Economy()
	lNamedPerks006OnCombatStart_Satellite()
	lNamedPerks006OnCombatStart_SectionD()
	if type(Jazz_MakeThemBleedSyncAll) == "function" then
		Jazz_MakeThemBleedSyncAll()
	end
end

function Jazz_NamedPerks006OnTurnStart()
	lNamedPerks006OnTurnStart_Signatures()
	lNamedPerks006OnTurnStart_Economy()
	lNamedPerks006OnTurnStart_Satellite()
	if type(Jazz_MakeThemBleedSyncAll) == "function" then
		Jazz_MakeThemBleedSyncAll()
	end
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
