-- JAZZ-COMBAT-007: Energy ladder (Fit → Exhausted) + gradual Free Move + satellite warn/times.
-- Top-level globals for wrap flags (jazz-lua-globals).

g_JAZZ_EnergyLadderInstalled = rawget(_G, "g_JAZZ_EnergyLadderInstalled") or false
g_JAZZ_SetTiredBase = rawget(_G, "g_JAZZ_SetTiredBase") or false
g_JAZZ_EnergyStatusEffectBase = rawget(_G, "g_JAZZ_EnergyStatusEffectBase") or false
g_JAZZ_EnergyTimesPatched = rawget(_G, "g_JAZZ_EnergyTimesPatched") or false

local ENERGY_CE = { "WellRested", "Fit", "Winded", "Fatigued", "Tired", "Exhausted" }

local function lPatchSatelliteTimes()
	if rawget(_G, "g_JAZZ_EnergyTimesPatched") then
		return
	end
	local sat = rawget(const, "Satellite")
	if type(sat) ~= "table" then
		return
	end
	-- Vanilla intent ~16h travel / ~8h rest per step. Ladder has 4 down-steps:
	-- ~8h travel (½) and ~6h rest (¾) so total-to-Exhausted ≈ old 2-step travel budget.
	if sat.UnitTirednessTravelTime then
		sat.UnitTirednessTravelTime = DivRound(sat.UnitTirednessTravelTime, 2)
	end
	if sat.UnitTirednessRestTime then
		sat.UnitTirednessRestTime = MulDivRound(sat.UnitTirednessRestTime, 6, 8)
	end
	rawset(_G, "g_JAZZ_EnergyTimesPatched", true)
end

local function lRemapTirednessConsts()
	const.utWellRested = -1
	const.utNormal = 0
	const.utWinded = 1
	const.utFatigued = 2
	const.utTired = 3
	const.utExhausted = 4
	-- Unconscious stays a separate CE; do not map it through Tiredness.

	UnitTirednessEffect = {
		[const.utWellRested] = "WellRested",
		[const.utNormal] = "Fit",
		[const.utWinded] = "Winded",
		[const.utFatigued] = "Fatigued",
		[const.utTired] = "Tired",
		[const.utExhausted] = "Exhausted",
	}
end

local function lClearEnergyEffects(obj)
	for _, id in ipairs(ENERGY_CE) do
		obj:RemoveStatusEffect(id)
	end
end

local function lJazzSetTired(self, value)
	value = Clamp(value or 0, const.utWellRested, const.utExhausted)
	if self.Tiredness == value then
		return
	end

	lClearEnergyEffects(self)
	-- Do not strip Unconscious via energy ladder (vanilla did; that fought real Unconscious CE).

	local oldValue = self.Tiredness or 0
	self.Tiredness = value

	local effect = UnitTirednessEffect[value]
	if effect and g_Classes[effect] then
		self:AddStatusEffect(effect)
	end

	if oldValue <= 0 and value > 0 then
		Msg("UnitTiredAdded", self)
	elseif oldValue > 0 and value <= 0 then
		Msg("UnitTiredRemoved", self)
	end
	if value - oldValue > 0 then
		Msg("UnitTiredLevelAdded", self, value)
	end
	if value - oldValue < 0 then
		Msg("UnitTiredLevelRemoved", self, value)
	end
end

function JazzEnergyOpeningFmBonus(target, effect)
	if not g_Combat or not target or not effect then
		return 0
	end
	local turns = effect:ResolveValue("opening_fm_turns") or 0
	if turns <= 0 then
		return 0
	end
	local turn = g_Combat.current_turn or 1
	if turn > turns then
		return 0
	end
	return effect:ResolveValue("opening_fm_bonus") or 0
end

function JazzEnergyLogStep(unit, new_level)
	if not unit or not IsMerc(unit) then
		return
	end
	local effect_id = UnitTirednessEffect[new_level]
	local name = unit.Nick or unit.Name
	if effect_id == "Winded" then
		CombatLog("important", T{890000000013113, "<name> is now Winded.", name = name})
	elseif effect_id == "Fatigued" then
		CombatLog("important", T{890000000013114, "<name> is now Fatigued.", name = name})
	elseif effect_id == "Tired" then
		CombatLog("important", T{890000000013115, "<name> is now Tired.", name = name})
	elseif effect_id == "Exhausted" then
		CombatLog("important", T{890000000013116, "<name> is now Exhausted.", name = name})
	elseif effect_id == "Fit" or effect_id == "WellRested" then
		CombatLog("important", T{890000000013117, "<name> has recovered energy (<level>).", name = name, level = TFormat.tiredness(nil, new_level)})
	end
end

--- Multi-stage travel warn (50% then 20% remaining) before next energy step.
function JazzEnergyTravelWarn(unit_data, threshold)
	if not unit_data or not threshold or threshold <= 0 then
		return
	end
	local remaining = threshold - (unit_data.TravelTime or 0)
	if remaining <= 0 then
		return
	end
	local stage = unit_data.JazzEnergyWarnStage or 0
	local pct_left = MulDivRound(remaining, 100, threshold)
	local new_stage = stage
	if pct_left <= 20 and stage < 20 then
		new_stage = 20
	elseif pct_left <= 50 and stage < 50 then
		new_stage = 50
	else
		return
	end
	unit_data.JazzEnergyWarnStage = new_stage
	local nick = unit_data.Nick
	local t = unit_data.Tiredness or 0
	if t <= const.utNormal then
		CombatLog("important", T{890000000013109, "<name> is getting winded.", name = nick})
	elseif t == const.utWinded then
		CombatLog("important", T{890000000013110, "<name> is getting fatigued.", name = nick})
	elseif t == const.utFatigued then
		CombatLog("important", T{890000000013111, "<name> is getting tired.", name = nick})
	elseif t == const.utTired then
		CombatLog("important", T{890000000013112, "<name> is getting exhausted.", name = nick})
	end
end

local function lPatchEnergyStatusEffectFormat()
	local energyEffects = { "WellRested", "Fit" }
	local redEffects = { "Winded", "Fatigued", "Tired", "Exhausted", "Unconscious" }
	local noEnergyEffect = T(102280983313, "Normal")

	local function format(context_obj)
		if not context_obj then
			return noEnergyEffect
		end
		for _, ef in ipairs(redEffects) do
			if context_obj:HasStatusEffect(ef) then
				local cls = g_Classes[ef]
				if cls and cls.ResolveValue and cls:ResolveValue("ap_loss") then
					return T{648417490486, "<error><EffectName></error> (<ApValue>AP)", EffectName = cls.DisplayName, ApValue = cls:ResolveValue("ap_loss")}
				elseif cls then
					return T{753249704554, "<error><EffectName></error>", EffectName = cls.DisplayName}
				end
			end
		end
		for _, ef in ipairs(energyEffects) do
			if context_obj:HasStatusEffect(ef) then
				local cls = g_Classes[ef]
				if cls and cls.ResolveValue and cls:ResolveValue("ap_gain") then
					return T{213633160729, "<effectName> (+<apValue>AP)", effectName = cls.DisplayName, apValue = cls:ResolveValue("ap_gain")}
				elseif cls then
					return cls.DisplayName
				end
			end
		end
		return noEnergyEffect
	end

	if type(TFormat) == "table" then
		TFormat.EnergyStatusEffect = format
	end
	rawset(_G, "RedEnergyEffects", redEffects)
end

local function lInstallSetTiredWrap()
	if rawget(_G, "g_JAZZ_EnergyLadderInstalled") then
		return
	end
	lRemapTirednessConsts()
	lPatchSatelliteTimes()
	lPatchEnergyStatusEffectFormat()

	local props = rawget(_G, "UnitProperties")
	if type(props) == "table" and type(props.SetTired) == "function" then
		rawset(_G, "g_JAZZ_SetTiredBase", props.SetTired)
		props.SetTired = lJazzSetTired
	end

	-- Unit:SetTired delegates to UnitProperties — keep in sync if defined.
	local unit = rawget(_G, "Unit")
	if type(unit) == "table" then
		function unit:SetTired(value)
			UnitProperties.SetTired(self, value)
		end
	end

	rawset(_G, "g_JAZZ_EnergyLadderInstalled", true)
end

-- Install on file load and after ModsReloaded (const / classes may arrive later).
lInstallSetTiredWrap()

function OnMsg.ModsReloaded()
	-- Re-apply const remap if another mod reset tables; keep wrap idempotent.
	lRemapTirednessConsts()
	lPatchSatelliteTimes()
	lPatchEnergyStatusEffectFormat()
	if not rawget(_G, "g_JAZZ_EnergyLadderInstalled") then
		lInstallSetTiredWrap()
	elseif type(UnitProperties) == "table" and UnitProperties.SetTired ~= lJazzSetTired then
		rawset(_G, "g_JAZZ_SetTiredBase", UnitProperties.SetTired)
		UnitProperties.SetTired = lJazzSetTired
		rawset(_G, "g_JAZZ_EnergyLadderInstalled", true)
	end
end

-- Ensure mercs sitting at Tiredness==0 actually have Fit after load/combat start.
local function lEnsureFitOnUnits(list)
	for _, unit in ipairs(list or empty_table) do
		if IsKindOf(unit, "UnitProperties") and (unit.Tiredness or 0) == const.utNormal then
			if not unit:HasStatusEffect("Fit") then
				unit:AddStatusEffect("Fit")
			end
		end
	end
end

function OnMsg.CombatStart()
	lEnsureFitOnUnits(g_Units)
end

function OnMsg.EnterSector()
	CreateGameTimeThread(function()
		Sleep(1)
		lEnsureFitOnUnits(g_Units)
		for _, ud in sorted_pairs(gv_UnitData or empty_table) do
			if IsMerc(ud) and (ud.Tiredness or 0) == const.utNormal and not ud:HasStatusEffect("Fit") then
				ud:AddStatusEffect("Fit")
			end
		end
	end)
end
