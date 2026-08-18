-- JAZZ-MED-006: kit stabilize (not healing), % HP heal by Medical, MaxHP debt, trauma status icons.
-- Load after Systems_Medicine.lua (see metadata.code).

JazzKitHealAtFullMedical = {
	FirstAidKit = 30,
	Medkit = 60,
	Reanimationsset = 100,
}

JazzTraumaMaxHpDebtByTier = {
	Light = 10,
	Medium = 30,
	Heavy = 60,
}

JazzTraumaIconBasePath = "Mod/e6L4ECj/Icons/StatusEffects/"

function JazzTraumaIsStabilized(effect)
	return effect and (effect:ResolveValue("jazz_stabilized") or 0) ~= 0
end

function JazzSetTraumaStabilized(effect, stabilized)
	if not effect or type(effect.SetParameter) ~= "function" then
		return false
	end
	effect:SetParameter("jazz_stabilized", stabilized and 1 or 0)
	return true
end

function JazzClearTraumaStabilizedOnEffect(effect)
	if JazzTraumaIsStabilized(effect) then
		JazzSetTraumaStabilized(effect, false)
		return true
	end
	return false
end

function JazzClearZoneTraumaStabilized(unit, zone)
	if not unit or not zone or type(unit.GetStatusEffect) ~= "function" then
		return false
	end
	local tier = JazzGetTraumaTier(unit, zone)
	if not tier then
		return false
	end
	local effect = unit:GetStatusEffect(JazzTraumaEffectId(zone, tier))
	local cleared = JazzClearTraumaStabilizedOnEffect(effect)
	if cleared and type(JazzApplyTraumaStatusIcon) == "function" then
		JazzApplyTraumaStatusIcon(effect)
	end
	return cleared
end

-- Combat tier for zone-specific penalties / Pain-on-use while stabilized (healing = full stored).
function JazzTraumaCombatTierFromEffect(effect, unit)
	if not effect then
		return false
	end
	local zone, stored = JazzParseTraumaEffectId(effect.class)
	if not zone or not stored then
		return false, zone
	end
	local live = effect
	if unit and type(unit.GetStatusEffect) == "function" then
		live = unit:GetStatusEffect(effect.class) or effect
	end
	if JazzTraumaIsHealing(live) then
		return stored, zone
	end
	if JazzTraumaIsStabilized(live) then
		local rank = JazzTraumaTierRank[stored] or 0
		if rank <= 1 then
			return false, zone
		end
		return JazzTraumaTiers[rank - 1], zone
	end
	return stored, zone
end

-- Helpers return 0 for Light-effective (stabilized Medium). Do not use `x or preset`:
-- Lua treats 0 as falsy and would restore the stored Medium/Heavy penalty.
function JazzTraumaResolveNum(effect, unit, fn, preset)
	if type(fn) == "function" then
		return fn(effect, unit)
	end
	if effect and type(effect.ResolveValue) == "function" then
		local v = effect:ResolveValue(preset)
		if v ~= nil then
			return v
		end
	end
	return 0
end

function JazzTraumaLegsMoveAp(effect, unit)
	local tier = JazzTraumaCombatTierFromEffect(effect, unit)
	if tier == "Heavy" then
		return 150
	elseif tier == "Medium" then
		return 50
	end
	return 0
end

function JazzTraumaBlocksFreeMove(effect, unit)
	local tier = JazzTraumaCombatTierFromEffect(effect, unit)
	return tier == "Medium" or tier == "Heavy"
end

function JazzTraumaRibsApLoss(effect, unit)
	local tier = JazzTraumaCombatTierFromEffect(effect, unit)
	if tier == "Heavy" then
		return 5
	elseif tier == "Medium" then
		return 2
	end
	return 0
end

function JazzTraumaArmsCthPenalty(effect, unit)
	local tier = JazzTraumaCombatTierFromEffect(effect, unit)
	if tier == "Heavy" then
		return 50
	elseif tier == "Medium" then
		return 20
	end
	return 0
end

function JazzTraumaHeadCthPenalty(effect, unit)
	local tier = JazzTraumaCombatTierFromEffect(effect, unit)
	if tier == "Heavy" then
		return 40
	elseif tier == "Medium" then
		return 15
	end
	return 0
end

function JazzTraumaHeadSightModifier(effect, unit)
	local tier = JazzTraumaCombatTierFromEffect(effect, unit)
	if tier == "Heavy" then
		return -50
	elseif tier == "Medium" then
		return -20
	end
	return 0
end

function JazzKitHealPercent(healer, kit_or_class)
	local class_id = type(kit_or_class) == "string" and kit_or_class or kit_or_class and kit_or_class.class
	local at_100 = JazzKitHealAtFullMedical[class_id or false]
	if not at_100 then
		return 0
	end
	local gate = JazzMedicineRequiredMedical(class_id) or 0
	local medical = healer and (healer.Medical or 0) or 0
	if gate > 0 and medical < gate then
		return 0
	end
	medical = Min(100, medical)
	if gate >= 100 then
		return at_100
	end
	-- at gate: 30% of kit_at_100; at Medical 100: full kit_at_100
	local t = medical <= gate and 0 or MulDivRound(medical - gate, 1000, 100 - gate)
	local scale = 30 + MulDivRound(70, t, 1000)
	return MulDivRound(at_100, scale, 100)
end

-- Kit heal amount (% of MaxHitPoints) + optional BuildingConfidence heal_modifier.
function JazzCalcKitHealAmount(healer, patient, kit_or_class)
	local class_id = type(kit_or_class) == "string" and kit_or_class or kit_or_class and kit_or_class.class
	local pct = JazzKitHealPercent(healer, class_id)
	local max_hp = (patient and patient.MaxHitPoints) or (healer and healer.MaxHitPoints) or 0
	local amount = MulDivRound(max_hp, pct, 100)
	local data = {
		heal_amount = 0,
		heal_percent = pct,
		self_heal_percent = 100,
		heal_modifier = 100,
	}
	if healer and type(healer.CallReactions) == "function" then
		healer:CallReactions("OnCalcHealAmount", patient, healer, kit_or_class, data)
	end
	if patient and patient ~= healer and IsKindOf(patient, "UnitBase") and type(patient.CallReactions) == "function" then
		patient:CallReactions("OnCalcHealAmount", patient, healer, kit_or_class, data)
	end
	if type(Jazz_BuildingConfidenceApplyHealMod) == "function" then
		Jazz_BuildingConfidenceApplyHealMod(healer, patient, data)
	end
	amount = data.heal_amount + MulDivRound(amount, data.heal_modifier, 100)
	return Max(0, amount), pct
end

function JazzResolveTraumaStatusIcon(effect)
	if not effect then
		return false
	end
	local class_name = effect.class
	if not class_name or not string.find(class_name, "^Trauma") then
		return false
	end
	local suffix = ""
	if JazzTraumaIsHealing(effect) then
		suffix = "Healing"
	elseif JazzTraumaIsStabilized(effect) then
		suffix = "Stabilized"
	end
	return JazzTraumaIconBasePath .. class_name .. suffix .. ".png"
end

function JazzApplyTraumaStatusIcon(effect)
	if not effect or type(effect.SetProperty) ~= "function" then
		return false
	end
	local path = JazzResolveTraumaStatusIcon(effect)
	if not path then
		return false
	end
	effect:SetProperty("Icon", path)
	return true
end

-- Heaviest Trauma* not healing and not stabilized, within kit cap.
function JazzFindKitEligibleUnstabilizedTrauma(unit, kit_class)
	if not unit then
		return
	end
	local max_rank = JazzKitTraumaMaxRank[kit_class or false] or 0
	if max_rank <= 0 then
		return
	end
	local best_zone, best_tier, best_effect, best_rank
	best_rank = 0
	for _, zone in ipairs(JazzTraumaZones) do
		local tier = JazzGetTraumaTier(unit, zone)
		if tier then
			local rank = JazzTraumaTierRank[tier] or 0
			if rank > 0 and rank <= max_rank then
				local effect = unit:GetStatusEffect(JazzTraumaEffectId(zone, tier))
				if effect and not JazzTraumaIsHealing(effect) and not JazzTraumaIsStabilized(effect) and rank > best_rank then
					best_rank = rank
					best_zone = zone
					best_tier = tier
					best_effect = effect
				end
			end
		end
	end
	if not best_effect then
		return
	end
	return best_zone, best_tier, best_effect
end

function JazzMarkKitTraumaStabilized(unit, kit_class)
	local zone, tier, effect = JazzFindKitEligibleUnstabilizedTrauma(unit, kit_class)
	if not effect then
		return false
	end
	JazzSetTraumaStabilized(effect, true)
	JazzApplyTraumaStatusIcon(effect)
	ObjModified(unit)
	if type(JazzPushTraumaToTwin) == "function" then
		JazzPushTraumaToTwin(unit)
	end
	return true, zone, tier
end

function JazzTraumaMaxHpDebtPercent(unit)
	if not unit or type(JazzGetTraumaTier) ~= "function" then
		return 0
	end
	local pct = 0
	for _, zone in ipairs(JazzTraumaZones or empty_table) do
		local tier = JazzGetTraumaTier(unit, zone)
		pct = pct + (JazzTraumaMaxHpDebtByTier[tier] or 0)
	end
	return pct
end

function JazzRecalcTraumaMaxHitPoints(unit)
	if not unit or type(RecalcMaxHitPoints) ~= "function" then
		return
	end
	RecalcMaxHitPoints(unit)
	local live, ud = nil, nil
	if type(lJazzStatusTwins) == "function" then
		-- private; fall through
	end
	if unit.session_id and gv_UnitData then
		ud = gv_UnitData[unit.session_id]
	end
	if ud and ud ~= unit then
		RecalcMaxHitPoints(ud)
	end
	if g_Units and unit.session_id then
		live = g_Units[unit.session_id]
		if live and live ~= unit then
			RecalcMaxHitPoints(live)
		end
	end
end

-- Redirect old kit-heal API → stabilize (MED-003 kit path superseded).
function JazzFindKitEligibleUnhealedTrauma(unit, kit_class)
	return JazzFindKitEligibleUnstabilizedTrauma(unit, kit_class)
end

function JazzMarkKitTraumaHealing(unit, kit_class)
	return JazzMarkKitTraumaStabilized(unit, kit_class)
end

function JazzMarkHeaviestTraumaHealing(unit)
	return JazzMarkKitTraumaStabilized(unit, "Reanimationsset")
end

g_JAZZ_MED006_RecalcWrapped = rawget(_G, "g_JAZZ_MED006_RecalcWrapped") or false
g_JAZZ_MED006_RecalcBase = rawget(_G, "g_JAZZ_MED006_RecalcBase") or false
g_JAZZ_MED006_StampBase = rawget(_G, "g_JAZZ_MED006_StampBase") or false
g_JAZZ_MED006_StampWrapped = rawget(_G, "g_JAZZ_MED006_StampWrapped") or false

local function lInstallMed006RecalcWrap()
	if rawget(_G, "g_JAZZ_MED006_RecalcWrapped") then
		return
	end
	if type(RecalcMaxHitPoints) ~= "function" then
		return
	end
	rawset(_G, "g_JAZZ_MED006_RecalcBase", RecalcMaxHitPoints)
	rawset(_G, "g_JAZZ_MED006_RecalcWrapped", true)
	function RecalcMaxHitPoints(unit)
		g_JAZZ_MED006_RecalcBase(unit)
		if not unit then
			return
		end
		local debt = JazzTraumaMaxHpDebtPercent(unit)
		if debt <= 0 then
			return
		end
		local maxhp = unit.MaxHitPoints or 0
		if maxhp <= 1 then
			return
		end
		local new_max = Max(1, MulDivRound(maxhp, 100 - Min(99, debt), 100))
		if new_max ~= maxhp then
			unit.MaxHitPoints = new_max
			if (unit.HitPoints or 0) > new_max then
				unit.HitPoints = new_max
			end
		end
	end
end

local function lInstallMed006StampWrap()
	local current = rawget(_G, "JazzStampStatusEffectUIProps")
	if type(current) ~= "function" then
		return
	end
	local our = rawget(_G, "g_JAZZ_MED006_StampWrapped")
	-- Re-bind if Systems_Medicine redefined the function after us.
	if our and current ~= JazzStampStatusEffectUIProps then
		rawset(_G, "g_JAZZ_MED006_StampWrapped", false)
	end
	if rawget(_G, "g_JAZZ_MED006_StampWrapped") then
		return
	end
	rawset(_G, "g_JAZZ_MED006_StampBase", current)
	rawset(_G, "g_JAZZ_MED006_StampWrapped", true)
	function JazzStampStatusEffectUIProps(effect, preset_id)
		local ok = g_JAZZ_MED006_StampBase(effect, preset_id)
		if effect and effect.class and string.find(effect.class, "^Trauma") then
			JazzApplyTraumaStatusIcon(effect)
		end
		return ok
	end
end

local function lMed006Install()
	lInstallMed006RecalcWrap()
	lInstallMed006StampWrap()
end

lMed006Install()

function OnMsg.DataLoaded()
	lMed006Install()
end

function OnMsg.ModsReloaded()
	lInstallMed006StampWrap()
end

function OnMsg.JAZZ_TraumaApplied(unit, zone, tier)
	if unit and type(RecalcMaxHitPoints) == "function" then
		RecalcMaxHitPoints(unit)
		if unit.session_id and gv_UnitData and gv_UnitData[unit.session_id] then
			RecalcMaxHitPoints(gv_UnitData[unit.session_id])
		end
	end
	local id = zone and tier and JazzTraumaEffectId(zone, tier)
	local effect = id and unit and unit.GetStatusEffect and unit:GetStatusEffect(id)
	if effect then
		JazzApplyTraumaStatusIcon(effect)
	end
end

function OnMsg.JAZZ_TraumaCleared(unit, zone)
	if unit and type(RecalcMaxHitPoints) == "function" then
		RecalcMaxHitPoints(unit)
		if unit.session_id and gv_UnitData and gv_UnitData[unit.session_id] then
			RecalcMaxHitPoints(gv_UnitData[unit.session_id])
		end
	end
end
