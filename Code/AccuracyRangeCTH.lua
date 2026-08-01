-- JAZZ shooting model.
--
-- Keep the pure calculations in this file. Unit, weapon execution, AI and UI
-- call the same helpers so that prediction cannot drift from the real shot.

JAZZ_CTH_FACTOR_SCALE = 1000
JAZZ_CTH_PRODUCT_SCALE = 1000000000
JAZZ_CTH_VALID_SHOT_FLOOR = 2
-- After BDR/E: factor falls with acceleration toward this floor at WeaponRange (not to 0).
JAZZ_CTH_RANGE_FLOOR_FACTOR = 250 -- 0.25 * FACTOR_SCALE
-- Minimum curve exponent (>1 → accelerating falloff).

local function JAZZ_CTHRound(value)
	if value >= 0 then
		return math.floor(value + 0.5)
	end
	return math.ceil(value - 0.5)
end

local function JAZZ_CTHGetWeaponProperty(weapon, id, default)
	if not weapon then
		return default
	end

	local value
	if weapon.GetProperty then
		value = weapon:GetProperty(id)
	end
	if value == nil then
		value = weapon[id]
	end

	if value == nil then
		return default
	end
	return value
end

local function JAZZ_CTHGetComponentValue(weapon, effect_id, value_id)
	if not weapon or not GetComponentEffectValue then
		return nil
	end
	return GetComponentEffectValue(weapon, effect_id, value_id)
end

function JAZZ_CTHPercentToFactor(value, min_factor, max_factor)
	min_factor = min_factor or 50
	max_factor = max_factor or 2000
	return Clamp(JAZZ_CTH_FACTOR_SCALE + JAZZ_CTHRound((value or 0) * 10), min_factor, max_factor)
end

function JAZZ_CTHFactorToPercent(factor)
	return JAZZ_CTHRound(((factor or JAZZ_CTH_FACTOR_SCALE) - JAZZ_CTH_FACTOR_SCALE) / 10)
end

function JAZZ_CTHAddFactor(factors, id, name, factor, meta_text, category)
	factors[#factors + 1] = {
		id = id,
		name = name,
		factor = Clamp(JAZZ_CTHRound(factor or JAZZ_CTH_FACTOR_SCALE), 0, 4000),
		ui_value = JAZZ_CTHFactorToPercent(factor),
		value = JAZZ_CTHFactorToPercent(factor),
		metaText = meta_text,
		category = category,
		source_index = #factors + 1,
	}
end

local function JAZZ_CTHSortedFactors(factors)
	local sorted = {}
	for i, factor in ipairs(factors or empty_table) do
		sorted[i] = factor
	end
	table.sort(sorted, function(a, b)
		local a_id = tostring(a.id or "")
		local b_id = tostring(b.id or "")
		if a_id == b_id then
			return (a.source_index or 0) < (b.source_index or 0)
		end
		return a_id < b_id
	end)
	return sorted
end

function JAZZ_CTHCalculateFactorProduct(factors)
	-- JA3 preserves the integer/float distinction: starting from integer 1
	-- truncates the first sub-unit factor (1 * 900 / 1000) to zero.
	local product = 1.0
	for _, factor in ipairs(JAZZ_CTHSortedFactors(factors)) do
		product = product * factor.factor / JAZZ_CTH_FACTOR_SCALE
	end
	return product, JAZZ_CTHRound(product * JAZZ_CTH_PRODUCT_SCALE)
end

function JAZZ_CTHApplyFactors(core, factors, possible, min_chance, max_chance)
	if not possible then
		return 0, 0, 0
	end

	min_chance = min_chance or JAZZ_CTH_VALID_SHOT_FLOOR
	max_chance = max_chance or 100

	local capped_core = Clamp(core or 0, 0, 100)
	local product, fixed_product = JAZZ_CTHCalculateFactorProduct(factors)
	local before_clamp = capped_core * product
	local final = Clamp(JAZZ_CTHRound(before_clamp), min_chance, max_chance)

	-- before/after are diagnostic only. They never feed the result.
	local diagnostic = capped_core
	for _, factor in ipairs(JAZZ_CTHSortedFactors(factors)) do
		factor.before = diagnostic
		diagnostic = diagnostic * factor.factor / JAZZ_CTH_FACTOR_SCALE
		factor.after = diagnostic
	end

	return final, before_clamp, fixed_product
end

function JAZZ_CTHSkillCurve(value)
	value = Max(0, value or 0)
	if value == 0 then
		return 20
	end
	-- 20 + 0.25 * value^1.25 without float pow (MP-safe).
	-- value^0.25 ≈ isqrt(isqrt(value * 1e8)) / 100; value^1.25 * 100 ≈ value * that.
	local function isqrt(n)
		n = Max(0, n)
		local lo, hi = 0, n
		while lo < hi do
			local mid = DivRound(lo + hi + 1, 2)
			if mid <= 0 then
				lo = mid
			elseif mid > n / mid then
				hi = mid - 1
			elseif mid * mid <= n then
				lo = mid
			else
				hi = mid - 1
			end
		end
		return lo
	end
	local root2 = isqrt(value * 100000000) -- ≈ 1e4 * sqrt(value)
	local root4 = isqrt(root2) -- ≈ 100 * value^0.25
	local pow_x100 = value * root4 -- ≈ 100 * value^1.25
	return 20 + DivRound(pow_x100, 400)
end

function JAZZ_CTHGetAimMastery(marksmanship)
	local m = Clamp(marksmanship or 0, 0, 100)
	local mastery =
		MulDivRound(Min(m, 60), 20, 60)
		+ MulDivRound(Clamp(m - 60, 0, 20), 20, 20)
		+ MulDivRound(Clamp(m - 80, 0, 10), 20, 10)
		+ MulDivRound(Clamp(m - 90, 0, 6), 20, 6)
		+ MulDivRound(Clamp(m - 96, 0, 4), 20, 4)
	return Min(100, mastery)
end

function JAZZ_CTHGetAimProgress(weapon, aim)
	local max_aim = Max(0, JAZZ_CTHGetWeaponProperty(weapon, "MaxAimActions", 0))
	if max_aim <= 0 then
		return 0, max_aim
	end
	return Clamp(MulDivRound(aim or 0, 1000, max_aim), 0, 1000) / 1000.0, max_aim
end

function JAZZ_CTHGetShooterCore(attacker, weapon, aim)
	local dexterity = Clamp(attacker and attacker.Dexterity or 0, 0, 100)
	local marksmanship = Clamp(attacker and attacker.Marksmanship or 0, 0, 100)
	local level = attacker and attacker.GetLevel and attacker:GetLevel() or 1
	local snap_raw = (dexterity * 4 + marksmanship + level * 5) * 1.0 / 6
	local precision_raw = (marksmanship * 4 + dexterity + level * 5) * 1.0 / 6
	local snap = JAZZ_CTHSkillCurve(snap_raw)
	local precision = JAZZ_CTHSkillCurve(precision_raw)
	local aim_progress, max_aim = JAZZ_CTHGetAimProgress(weapon, aim)
	local shot_skill = snap + aim_progress * Max(precision - snap, 0)
	local aim_mastery = JAZZ_CTHGetAimMastery(marksmanship)
	local aim_accuracy = Max(0, JAZZ_CTHGetWeaponProperty(weapon, "AimAccuracy", 0))
	local aim_gain = Max(0, aim or 0) * aim_accuracy * aim_mastery * 1.0 / 100
	local core = shot_skill + aim_gain

	return core, {
		snap_raw = snap_raw,
		precision_raw = precision_raw,
		snap = snap,
		precision = precision,
		shot_skill = shot_skill,
		aim_mastery = aim_mastery,
		aim_accuracy = aim_accuracy,
		aim_gain = aim_gain,
		aim_progress = aim_progress,
		max_aim = max_aim,
	}
end

local function JAZZ_CTHBuildOpticProfile(weapon, effect_id, magnification_id, sub_magnification_id, aim_level_id, aim)
	local magnification, component = JAZZ_CTHGetComponentValue(weapon, effect_id, magnification_id)
	if not magnification then
		return nil
	end

	local sub_magnification = JAZZ_CTHGetComponentValue(weapon, effect_id, sub_magnification_id) or 0
	local aim_level = JAZZ_CTHGetComponentValue(weapon, effect_id, aim_level_id) or 0
	-- Near-penalty is always active while the optic is mounted. AimLevel only unlocks reach
	-- (long-range benefit). Gating both behind AimLevel made 6–10× scopes feel like irons at snap.
	local aim_ok = (aim or 0) >= aim_level

	magnification = Max(1, magnification + (sub_magnification or 0) * 1.0 / 10)
	local explicit_reach = JAZZ_CTHGetComponentValue(weapon, effect_id, "OpticReach")
	local explicit_min_range = JAZZ_CTHGetComponentValue(weapon, effect_id, "OpticMinRange")
	local explicit_near_factor = JAZZ_CTHGetComponentValue(weapon, effect_id, "OpticNearFactor")

	local reach = 0
	if aim_ok then
		reach = explicit_reach or Max(0, (magnification - 1) * 3)
	end
	-- Stronger tier spread than the old floor@0.55: 4×~82%, 6×~64%, 10×~35% at d=0.
	local min_range = explicit_min_range or (magnification >= 4 and JAZZ_CTHRound(magnification * 0.9) or 0)
	local near_factor = explicit_near_factor and explicit_near_factor * 10
		or (magnification >= 4 and JAZZ_CTHRound(Max(0.35, 1 - (magnification - 2) * 0.09) * JAZZ_CTH_FACTOR_SCALE)
		or JAZZ_CTH_FACTOR_SCALE)

	return {
		effect_id = effect_id,
		component_id = component and component.id or weapon.components and weapon.components.Scope,
		magnification = magnification,
		aim_level = aim_level,
		aim_ok = aim_ok,
		reach = reach,
		min_range = min_range,
		near_factor = Clamp(near_factor, 250, JAZZ_CTH_FACTOR_SCALE),
	}
end

local JAZZ_CTHFallbackOpticProfiles = {
	AdvancedHOLO = {magnification = 1.2, aim_level = 0, reach = 2, min_range = 0, near_factor = 1000},
	AnotherOptic = {magnification = 4, aim_level = 2, reach = 9, min_range = 4, near_factor = 820},
	CollimatorMP7 = {magnification = 1.2, aim_level = 0, reach = 2, min_range = 0, near_factor = 1000},
	LaserDot_Anaconda = {magnification = 1.2, aim_level = 0, reach = 2, min_range = 0, near_factor = 1000},
	LROptics = {magnification = 5, aim_level = 2, reach = 12, min_range = 5, near_factor = 730},
	LROpticsAdvanced = {magnification = 10, aim_level = 3, reach = 27, min_range = 9, near_factor = 350},
	LROptics_DragunovDefault = {magnification = 5, aim_level = 2, reach = 12, min_range = 5, near_factor = 730},
	PSG_DefaultScope = {magnification = 6, aim_level = 3, reach = 15, min_range = 5, near_factor = 640},
	ReflexSight = {magnification = 1.2, aim_level = 0, reach = 2, min_range = 0, near_factor = 1000},
	ReflexSightAdvanced = {magnification = 1.3, aim_level = 0, reach = 3, min_range = 0, near_factor = 1000},
	ReflexSightAdvanced_Glock = {magnification = 1.2, aim_level = 0, reach = 2, min_range = 0, near_factor = 1000},
	ScopeCOG = {magnification = 2, aim_level = 1, reach = 3, min_range = 0, near_factor = 1000},
	ScopeCOGQuick = {magnification = 3, aim_level = 1, reach = 6, min_range = 0, near_factor = 1000},
	ThermalScope = {magnification = 5, aim_level = 3, reach = 12, min_range = 4, near_factor = 840},
}

local function JAZZ_CTHGetFallbackOpticProfile(weapon, aim)
	local scope_id = weapon and weapon.components and weapon.components.Scope
	local profile = scope_id and JAZZ_CTHFallbackOpticProfiles[scope_id]
	if not profile and scope_id and (
		string.find(scope_id, "Reflex", 1, true)
		or string.find(scope_id, "Collimator", 1, true)
		or string.find(scope_id, "HOLO", 1, true)
	) then
		profile = {magnification = 1.2, aim_level = 0, reach = 2, min_range = 0, near_factor = 1000}
	end

	if not profile then
		return {
			effect_id = false,
			component_id = false,
			magnification = 1,
			aim_level = 0,
			reach = 0,
			min_range = 0,
			near_factor = JAZZ_CTH_FACTOR_SCALE,
		}
	end

	local aim_ok = (aim or 0) >= profile.aim_level
	return {
		effect_id = scope_id,
		component_id = scope_id,
		magnification = profile.magnification,
		aim_level = profile.aim_level,
		aim_ok = aim_ok,
		-- Near always; reach only when AimLevel met (same contract as ScopeMagnification comps).
		reach = aim_ok and profile.reach or 0,
		min_range = profile.min_range,
		near_factor = profile.near_factor,
	}
end

local function JAZZ_CTHMergeOpticProfiles(scope, auxiliary)
	-- Reach comes from the best unlocked optical mode; near-penalty from the highest mounted mag
	-- (carrying a 7–10× tube still hurts up close even if you are using the low-mag side).
	local near_src = scope or auxiliary
	if scope and auxiliary and auxiliary.magnification > scope.magnification then
		near_src = auxiliary
	end
	local reach = 0
	local reach_src = near_src
	if scope and scope.reach > reach then
		reach = scope.reach
		reach_src = scope
	end
	if auxiliary and auxiliary.reach > reach then
		reach = auxiliary.reach
		reach_src = auxiliary
	end
	return {
		effect_id = reach_src.effect_id or near_src.effect_id,
		component_id = reach_src.component_id or near_src.component_id,
		magnification = near_src.magnification,
		aim_level = reach_src.aim_level or near_src.aim_level,
		aim_ok = reach > 0,
		reach = reach,
		min_range = near_src.min_range,
		near_factor = near_src.near_factor,
	}
end

function JAZZ_CTHGetOpticProfile(weapon, aim)
	local scope = JAZZ_CTHBuildOpticProfile(
		weapon,
		"ScopeMagnification",
		"ScopeMagnification",
		"ScopeSubMagnification",
		"ScopeAimLevel",
		aim
	)
	local auxiliary = JAZZ_CTHBuildOpticProfile(
		weapon,
		"SmallMagnification",
		"SmallMagnification",
		"SmallSubMagnification",
		"SmallAimLevel",
		aim
	)

	if scope or auxiliary then
		return JAZZ_CTHMergeOpticProfiles(scope, auxiliary)
	end
	return JAZZ_CTHGetFallbackOpticProfile(weapon, aim)
end

function JAZZ_CTHGetRangeProfile(weapon, distance, unit, action, aim)
	local weapon_range
	if unit and action then
		weapon_range = action:GetMaxAimRange(unit, weapon)
	end
	weapon_range = weapon_range or JAZZ_CTHGetWeaponProperty(weapon, "WeaponRange", 0)

	if IsKindOf(unit, "UnitBase") then
		weapon_range = unit:CallReactions_Modify("OnUnitGetWeaponRange", weapon_range, weapon, action)
	end

	if not weapon_range or weapon_range <= 0 then
		return 0, {
			possible = false,
			distance = 0,
			weapon_range = weapon_range or 0,
		}
	end

	local tiles = Max(0, (distance or 0) * 1.0 / const.SlabSizeX)
	local bullet_drop_range = JAZZ_CTHGetWeaponProperty(weapon, "BulletDropRange", weapon_range * 1.0 / 2)
	bullet_drop_range = Clamp(bullet_drop_range, 0, weapon_range)
	local grouping = FirearmGetGrouping and FirearmGetGrouping(weapon)
		or JAZZ_CTHGetWeaponProperty(weapon, "Grouping", 50)
	local aim_progress = JAZZ_CTHGetAimProgress(weapon, aim)
	local optic = JAZZ_CTHGetOpticProfile(weapon, aim)
	local epsilon = 0.01
	local effective_range = Min(weapon_range - epsilon, bullet_drop_range + optic.reach * aim_progress)
	effective_range = Clamp(effective_range, 0, weapon_range - epsilon)
	-- Accelerating falloff after E/BDR; p>1. Floor ~25% at R (last valid tile).
	local curve_power = Max(1.25, bullet_drop_range * 0.05 + grouping * 1.0 / 100)
	local range_floor = JAZZ_CTH_RANGE_FLOOR_FACTOR

	local function falloff_factor(t)
		-- floor + (1 - floor) * (1 - t^p)  →  at t=0: 1.0, at t=1: floor
		return JAZZ_CTHRound(
			range_floor + (JAZZ_CTH_FACTOR_SCALE - range_floor) * (1 - t ^ curve_power)
		)
	end

	local possible = tiles < weapon_range
	local factor
	if not possible then
		factor = 0
	elseif tiles <= effective_range then
		factor = JAZZ_CTH_FACTOR_SCALE
	else
		local t = Clamp((tiles - effective_range) / (weapon_range - effective_range), 0, 1)
		factor = falloff_factor(t)
	end

	local unassisted_factor = factor
	if possible and optic.effect_id and optic.reach > 0 then
		local unassisted_effective = Min(weapon_range - epsilon, bullet_drop_range)
		if tiles <= unassisted_effective then
			unassisted_factor = JAZZ_CTH_FACTOR_SCALE
		else
			local unassisted_t = Clamp(
				(tiles - unassisted_effective) / (weapon_range - unassisted_effective),
				0,
				1
			)
			unassisted_factor = falloff_factor(unassisted_t)
		end
	end

	local optic_factor = JAZZ_CTH_FACTOR_SCALE
	if optic.effect_id and optic.min_range > 0 and tiles < optic.min_range then
		local proximity = Clamp((optic.min_range - tiles) / optic.min_range, 0, 1)
		optic_factor = JAZZ_CTHRound(
			JAZZ_CTH_FACTOR_SCALE
			+ (optic.near_factor - JAZZ_CTH_FACTOR_SCALE) * proximity
		)
	end

	-- Weapon close-range inefficiency (barrel-shifted); optic MinRange stacks via separate factor.
	local close_range = Max(0, JAZZ_CTHGetWeaponProperty(weapon, "CloseRange", 0) or 0)
	local close_range_factor_pct = Clamp(
		JAZZ_CTHGetWeaponProperty(weapon, "CloseRangeFactor", 100) or 100,
		25,
		100
	)
	local close_factor = JAZZ_CTH_FACTOR_SCALE
	if close_range > 0 and tiles < close_range then
		local factor0 = JAZZ_CTHRound(close_range_factor_pct * 10) -- percent → FACTOR_SCALE
		local proximity = Clamp((close_range - tiles) / close_range, 0, 1)
		close_factor = JAZZ_CTHRound(
			JAZZ_CTH_FACTOR_SCALE + (factor0 - JAZZ_CTH_FACTOR_SCALE) * proximity
		)
	end

	return Clamp(factor, 0, JAZZ_CTH_FACTOR_SCALE), {
		possible = possible,
		distance = tiles,
		weapon_range = weapon_range,
		bullet_drop_range = bullet_drop_range,
		grouping = grouping,
		effective_range = effective_range,
		curve_power = curve_power,
		range_floor = range_floor,
		aim_progress = aim_progress,
		optic = optic,
		close_range = close_range,
		close_range_factor_pct = close_range_factor_pct,
		close_factor = close_factor,
		optic_factor = optic_factor,
		unassisted_factor = Clamp(unassisted_factor, 0, JAZZ_CTH_FACTOR_SCALE),
	}
end

function GetRangeAccuracy(weapon, distance, unit, action, aim)
	local factor = JAZZ_CTHGetRangeProfile(weapon, distance, unit, action, aim)
	return Clamp(JAZZ_CTHRound(factor / 10), 0, 100)
end

function GetRangeDamageReduction(weapon, distance, unit, action)
	local factor, profile = JAZZ_CTHGetRangeProfile(weapon, distance, unit, action, 0)
	if not profile.possible then
		return 0
	end
	return Clamp(JAZZ_CTHRound(factor / 10), 1, 100)
end

local JAZZ_CTHProtectedShotsByAction = {
	AbakanBurst = 1,
	AbakanAutoFire = 1,
	JAZZ_ControllableBurst = 1,
}

local function JAZZ_CTHGetActionRecoil(weapon_recoil, action)
	if not action then
		return weapon_recoil, 0
	end

	local action_id = action.id
	local action_recoil = weapon_recoil
	if action_id == "MGBurstFire" or action_id == "GrizzlyPerk" then
		action_recoil = weapon_recoil * 0.8
	elseif action_id == "JAZZ_Fanning" then
		local configured = action.ResolveValue and action:ResolveValue("cth_loss_per_shot")
		action_recoil = type(configured) == "number" and configured or 20
	end

	return action_recoil, JAZZ_CTHProtectedShotsByAction[action_id] or 0
end

function JAZZ_CTHGetRecoilProfile(weapon, attacker, stance, action, attack_args)
	local weapon_recoil = Max(0, JAZZ_CTHGetWeaponProperty(weapon, "Recoil", 0))
	local base_recoil = Max(0, weapon and weapon.base_Recoil or weapon_recoil)
	local action_recoil, action_protected_shots = JAZZ_CTHGetActionRecoil(weapon_recoil, action)
	if attack_args and type(attack_args.cth_loss_per_shot) == "number" then
		action_recoil = Max(0, attack_args.cth_loss_per_shot)
	end

	local strength = Clamp(attacker and attacker.Strength or 50, 0, 100)
	local strength_factor = Clamp(1.25 - strength * 1.0 / 200, 0.75, 1.25)
	local stance_factor = stance == "Prone" and 0.75 or stance == "Crouch" and 0.90 or 1
	local support_factor = 1
	local perk_factor = 1
	local action_factor = 1
	local class_factor = 1
	local component_factor = base_recoil > 0 and (weapon_recoil * 1.0 / base_recoil) or 1
	local shots_before_recoil = action_protected_shots
	if attack_args and type(attack_args.shots_before_recoil) == "number" then
		shots_before_recoil = Max(0, attack_args.shots_before_recoil)
	end


	local deployed = attack_args and attack_args.deployed
	if not deployed and g_Overwatch and attacker and g_Overwatch[attacker] then
		deployed = g_Overwatch[attacker].permanent
	end

	local bipod_shots = JAZZ_CTHGetComponentValue(weapon, "ShotsBeforeRecoilProne", "ShotsBeforeRecoilProne")
	if stance == "Prone" and bipod_shots then
		support_factor = 0.65
		shots_before_recoil = shots_before_recoil + Max(0, bipod_shots)
	elseif deployed or attacker and attacker.HasStatusEffect and attacker:HasStatusEffect("BipodUnfolded") then
		support_factor = 0.65
	end

	if HasPerk and attacker and HasPerk(attacker, "AutoWeapons") then
		perk_factor = 0.85
	end
	if action and action.id == "GrizzlyPerk" then
		action_factor = 0.55
	end

	if not deployed and not (support_factor < 1) then
		if IsKindOf(weapon, "MachineGun") then
			class_factor = 1.35
		elseif IsKindOf(weapon, "LightMachineGun") then
			class_factor = 1.15
		elseif weapon.IsCumbersome and weapon:IsCumbersome() then
			class_factor = 1.10
		end
	end

	local effective_recoil =
		action_recoil
		* strength_factor
		* stance_factor
		* support_factor
		* perk_factor
		* action_factor
		* class_factor
	local retention = Clamp(1 - effective_recoil * 1.0 / 100, 0.15, 1)

	return {
		recoil = weapon_recoil,
		base_recoil = base_recoil,
		action_recoil = action_recoil,
		effective_recoil = effective_recoil,
		retention = JAZZ_CTHRound(retention * JAZZ_CTH_FACTOR_SCALE),
		strength_factor = strength_factor,
		stance_factor = stance_factor,
		support_factor = support_factor,
		component_factor = component_factor,
		perk_factor = perk_factor,
		action_factor = action_factor,
		class_factor = class_factor,
		shots_before_recoil = shots_before_recoil,
	}
end

function JAZZ_CTHGetBulletChance(first_bullet_chance, bullet_index, recoil_profile, possible)
	if possible == false then
		return 0
	end

	local protected_shots = recoil_profile and recoil_profile.shots_before_recoil or 0
	local exponent = Max(0, (bullet_index or 1) - 1 - protected_shots)
	local retention = recoil_profile and recoil_profile.retention or JAZZ_CTH_FACTOR_SCALE
	-- JA3 truncates integer/integer (850/1000 -> 0). Force float like JAZZ_CTHCalculateFactorProduct.
	local chance = (first_bullet_chance or 0) * 1.0
	if exponent > 0 then
		chance = chance * (retention * 1.0 / JAZZ_CTH_FACTOR_SCALE) ^ exponent
	end
	return Clamp(JAZZ_CTHRound(chance), JAZZ_CTH_VALID_SHOT_FLOOR, 100)
end
