-- JAZZ-COMBAT-007: Energy ladder (Fit → Exhausted) + gradual Free Move + satellite warn/times.
-- Top-level globals for wrap flags (jazz-lua-globals).

g_JAZZ_EnergyLadderInstalled = rawget(_G, "g_JAZZ_EnergyLadderInstalled") or false
g_JAZZ_SetTiredBase = rawget(_G, "g_JAZZ_SetTiredBase") or false
g_JAZZ_EnergyStatusEffectBase = rawget(_G, "g_JAZZ_EnergyStatusEffectBase") or false
g_JAZZ_EnergyTimesPatched = rawget(_G, "g_JAZZ_EnergyTimesPatched") or false
g_JAZZ_FreeMoveUIInstalled = rawget(_G, "g_JAZZ_FreeMoveUIInstalled") or false
g_JAZZ_StatusEffectIconOpenBase = rawget(_G, "g_JAZZ_StatusEffectIconOpenBase") or false
g_JAZZ_FreeMoveRolloverPatched = rawget(_G, "g_JAZZ_FreeMoveRolloverPatched") or false
g_JAZZ_PDAMercRolloverAPBase = rawget(_G, "g_JAZZ_PDAMercRolloverAPBase") or false

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

---------------------------------------------------------------------------
-- JAZZ-COMBAT-008: Legs → foot travel slow; Ribs → faster energy drain; no HP tiredness mod.
---------------------------------------------------------------------------

g_JAZZ_EnergyTraumaTravelInstalled = rawget(_G, "g_JAZZ_EnergyTraumaTravelInstalled") or false
g_JAZZ_EnergyTraumaTravelWrapper = rawget(_G, "g_JAZZ_EnergyTraumaTravelWrapper") or false

local LEGS_FOOT_SLOW_PCT = { Light = 10, Medium = 20, Heavy = 30 }
local RIBS_TIREDNESS_MUL = { Light = 85, Medium = 70, Heavy = 55 }

--- Worst Legs trauma among squad units → foot travel time +pct (cap 30).
function JazzGetSquadFootTravelSlowPct(units)
	local worst = 0
	for _, u in ipairs(units or empty_table) do
		local ud = type(u) == "table" and u or (gv_UnitData and gv_UnitData[u])
		if ud and type(JazzGetTraumaTier) == "function" then
			local tier = JazzGetTraumaTier(ud, "Legs")
			local pct = tier and LEGS_FOOT_SLOW_PCT[tier]
			if pct and pct > worst then
				worst = pct
			end
		end
	end
	return worst
end

--- TravelTiredness threshold for one merc (Ribs shortens; HP no longer adjusts).
function JazzGetTirednessTravelThreshold(unit_data)
	local sat = rawget(const, "Satellite")
	local base = sat and sat.UnitTirednessTravelTime or 0
	if not unit_data or type(JazzGetTraumaTier) ~= "function" then
		return base
	end
	local tier = JazzGetTraumaTier(unit_data, "Ribs")
	local mul = tier and RIBS_TIREDNESS_MUL[tier] or 100
	return MulDivRound(base, mul, 100)
end

-- GetHPAdditionalTiredTime → 0 is defined in SatelliteSquad.lua (loads after this file).

local function lTravelUsesVehicle(route, units)
	if route and route.JAZZ_vehicle then
		return true
	end
	for _, u in ipairs(units or empty_table) do
		local ud = type(u) == "table" and u or (gv_UnitData and gv_UnitData[u])
		local squad = ud and ud.Squad and gv_Squads and gv_Squads[ud.Squad]
		if squad and squad.JAZZ_vehicle_id then
			return true
		end
	end
	return false
end

local function lIsFootTravelSegment(from_sector_id, to_sector_id, shortcut, isRiverSectors)
	if shortcut or isRiverSectors then
		return false
	end
	local from_s = gv_Sectors and gv_Sectors[from_sector_id]
	local to_s = to_sector_id and gv_Sectors and gv_Sectors[to_sector_id]
	if from_s and from_s.Passability == "Water" then
		return false
	end
	if to_s and to_s.Passability == "Water" then
		return false
	end
	local t1 = from_s and from_s.TerrainType
	local t2 = to_s and to_s.TerrainType
	if t1 == "Water" or t2 == "Water" then
		return false
	end
	return true
end

local function lInstallEnergyTraumaTravelHook()
	if type(GetSectorTravelTime) ~= "function" then
		return
	end
	if GetSectorTravelTime == rawget(_G, "g_JAZZ_EnergyTraumaTravelWrapper") then
		return
	end
	local orig = GetSectorTravelTime
	local function wrapper(from_sector_id, to_sector_id, route, units, pass_mode, a6, side, dir, cache_shortcuts, cache_neighbors)
		local t1, t2, t3, breakdown = orig(from_sector_id, to_sector_id, route, units, pass_mode, a6, side, dir, cache_shortcuts, cache_neighbors)
		if not t1 or t1 == false then
			return t1, t2, t3, breakdown
		end
		if pass_mode == "display_invalid" then
			return t1, t2, t3, breakdown
		end
		if lTravelUsesVehicle(route, units) then
			return t1, t2, t3, breakdown
		end

		local shortcut
		if to_sector_id and from_sector_id and not AreAdjacentSectors(from_sector_id, to_sector_id) then
			shortcut = GetShortcutByStartEnd(from_sector_id, to_sector_id)
		end
		local isRiverSectors = false
		if cache_shortcuts ~= nil then
			isRiverSectors = IsRiverSector(from_sector_id, not not shortcut, cache_shortcuts)
		else
			isRiverSectors = not shortcut and IsRiverSector(from_sector_id) and IsRiverSector(to_sector_id, "two_way")
		end
		if not lIsFootTravelSegment(from_sector_id, to_sector_id, shortcut, isRiverSectors) then
			return t1, t2, t3, breakdown
		end

		local slow = JazzGetSquadFootTravelSlowPct(units)
		if slow <= 0 then
			return t1, t2, t3, breakdown
		end

		local factor = 100 + slow
		t1 = MulDivRound(t1, factor, 100)
		t2 = t2 and MulDivRound(t2, factor, 100) or t2
		t3 = t3 and MulDivRound(t3, factor, 100) or t3
		-- Round like vanilla GetSectorTravelTime.
		t1 = DivCeil(t1, const.Scale.min) * const.Scale.min
		if t2 then
			t2 = DivCeil(t2, const.Scale.min) * const.Scale.min
		end
		if t3 then
			t3 = DivCeil(t3, const.Scale.min) * const.Scale.min
		end
		if breakdown then
			breakdown[#breakdown + 1] = {
				Text = T(890000000013121, "<em>(Injured legs)</em>"),
				Value = -slow,
				Category = "sector-special",
				special = "jazz_legs_trauma",
			}
		end
		return t1, t2, t3, breakdown
	end
	rawset(_G, "g_JAZZ_EnergyTraumaTravelWrapper", wrapper)
	GetSectorTravelTime = wrapper
	rawset(_G, "g_JAZZ_EnergyTraumaTravelInstalled", true)
end

---------------------------------------------------------------------------
-- Remaining Free Move AP in UI (icon overlay, status tooltip, merc AP line).
-- Vanilla GetUIActionPoints() hides free_move_ap, so 16+1 is Fit/morale only.
---------------------------------------------------------------------------

function JazzFreeMoveOwner(effect)
	if not effect then
		return nil
	end
	local function owns(unit)
		return unit and type(unit.GetStatusEffect) == "function" and unit:GetStatusEffect("FreeMove") == effect
	end
	local sel = rawget(_G, "SelectedObj")
	if owns(sel) then
		return sel
	end
	local units = rawget(_G, "g_Units")
	if type(units) == "table" then
		for _, u in ipairs(units) do
			if owns(u) then
				return u
			end
		end
	end
	return nil
end

function JazzFormatFreeMoveDescription(effect)
	local unit = JazzFreeMoveOwner(effect)
	local remain = (unit and unit.free_move_ap) or 0
	return T{890000000013122, "Move without spending AP. Remaining: <em><apn(remain)> AP</em>. Removed after attacking or after using up the allowance (based on Agility).", remain = remain}
end

local function lGetTemplateProp(node, name)
	if type(node) ~= "table" then
		return nil
	end
	local v = rawget(node, name)
	if v ~= nil then
		return v
	end
	if type(node.GetProperty) == "function" then
		local ok, val = pcall(node.GetProperty, node, name)
		if ok then
			return val
		end
	end
	return nil
end

local function lFindIconStackText(icon)
	for _, child in ipairs(icon) do
		if IsKindOf(child, "XText") then
			return child
		end
	end
	return nil
end

local hooked_fm_icon = {}
setmetatable(hooked_fm_icon, { __mode = "k" })

local function lHookFreeMoveIconText(icon)
	if not icon or hooked_fm_icon[icon] then
		return
	end
	local txt = lFindIconStackText(icon)
	if not txt then
		return
	end
	hooked_fm_icon[icon] = true
	local base = txt.OnContextUpdate
	txt.OnContextUpdate = function(self, context, ...)
		if context and IsKindOf(context, "FreeMove") then
			local unit = JazzFreeMoveOwner(context)
			local remain = (unit and unit.free_move_ap) or 0
			local scale = (const.Scale and const.Scale.AP) or 1000
			local n = remain > 0 and DivRound(remain, scale) or 0
			self:SetVisible(n > 0)
			self:SetText(Untranslated(tostring(n)))
			XContextControl.OnContextUpdate(self, context)
			return
		end
		if type(base) == "function" then
			return base(self, context, ...)
		end
		XContextControl.OnContextUpdate(self, context)
	end
end

local function lPatchPDAMercRolloverAP()
	local xts = rawget(_G, "XTemplates")
	local tmpl = xts and xts.PDAMercRollover
	if type(tmpl) ~= "table" then
		return
	end
	local target
	local function walk(node)
		if target or type(node) ~= "table" then
			return
		end
		local ts = lGetTemplateProp(node, "TextStyle")
		local ocu = lGetTemplateProp(node, "OnContextUpdate")
		if ts == "PDARolloverHeaderBeige" and type(ocu) == "function" then
			target = node
			return
		end
		for i = 1, #node do
			walk(node[i])
		end
	end
	walk(tmpl)
	if not target then
		return
	end
	local base = rawget(_G, "g_JAZZ_PDAMercRolloverAPBase")
	if type(base) ~= "function" then
		base = lGetTemplateProp(target, "OnContextUpdate")
		rawset(_G, "g_JAZZ_PDAMercRolloverAPBase", base)
	end
	if type(base) ~= "function" then
		return
	end
	local wrapped = function(self, context, ...)
		local result = base(self, context, ...)
		local combat = rawget(_G, "g_Combat")
		if combat and context and type(context.free_move_ap) == "number" then
			local remain = context.free_move_ap
			local scale = (const.Scale and const.Scale.AP) or 1000
			if remain >= scale then
				local cur = self:GetText()
				if cur then
					self:SetText(cur .. T{890000000013123, " <em>(<apn(fm)> FM)</em>", fm = remain})
				end
			end
		end
		return result
	end
	if type(target.SetProperty) == "function" then
		target:SetProperty("OnContextUpdate", wrapped)
	else
		target.OnContextUpdate = wrapped
	end
	rawset(_G, "g_JAZZ_FreeMoveRolloverPatched", true)
end

local function lInstallFreeMoveUI()
	local cls = rawget(_G, "StatusEffectIcon")
	if type(cls) == "table" and type(cls.Open) == "function" then
		local base = rawget(_G, "g_JAZZ_StatusEffectIconOpenBase")
		if type(base) ~= "function" then
			base = cls.Open
			rawset(_G, "g_JAZZ_StatusEffectIconOpenBase", base)
		end
		cls.Open = function(self)
			local result = base(self)
			lHookFreeMoveIconText(self)
			local txt = lFindIconStackText(self)
			if txt and type(txt.OnContextUpdate) == "function" then
				txt:OnContextUpdate(self.context)
			end
			return result
		end
		rawset(_G, "g_JAZZ_FreeMoveUIInstalled", true)
	end
	lPatchPDAMercRolloverAP()
end

function OnMsg.UnitAPChanged(unit)
	if not unit or type(unit.GetStatusEffect) ~= "function" then
		return
	end
	local fm = unit:GetStatusEffect("FreeMove")
	if fm then
		ObjModified(fm)
	end
end

lInstallFreeMoveUI()

-- Install after SatelliteSquad defines GetSectorTravelTime; re-wrap after jazz-maps vehicles if needed.
function OnMsg.ModsReloaded()
	lRemapTirednessConsts()
	lPatchSatelliteTimes()
	lPatchEnergyStatusEffectFormat()
	lInstallFreeMoveUI()
	if not rawget(_G, "g_JAZZ_EnergyLadderInstalled") then
		lInstallSetTiredWrap()
	elseif type(UnitProperties) == "table" and UnitProperties.SetTired ~= lJazzSetTired then
		rawset(_G, "g_JAZZ_SetTiredBase", UnitProperties.SetTired)
		UnitProperties.SetTired = lJazzSetTired
		rawset(_G, "g_JAZZ_EnergyLadderInstalled", true)
	end
	CreateRealTimeThread(function()
		Sleep(1)
		lInstallEnergyTraumaTravelHook()
		Sleep(50)
		-- If maps vehicle hook wrapped after us, wrap again so Legs slow sits outside vehicle speed-up.
		lInstallEnergyTraumaTravelHook()
	end)
end
