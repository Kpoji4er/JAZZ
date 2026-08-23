-- JAZZ-MED-007: trauma MaxHP debt after combat; CombatStart/End recalc.
-- Top-level wrap flags (jazz-lua-globals).

g_JAZZ_MED007_ForceDebt = rawget(_G, "g_JAZZ_MED007_ForceDebt") or false

--- True while this unit should keep a full (pre-debt) MaxHP ceiling.
function JazzUnitSkipsTraumaMaxHpDebt(unit)
	if rawget(_G, "g_JAZZ_MED007_ForceDebt") then
		return false
	end
	if not rawget(_G, "g_Combat") then
		return false
	end
	if not unit then
		return false
	end
	local sid = unit.session_id
	local live = sid and g_Units and g_Units[sid]
	if not live then
		return false
	end
	if not IsValid(live) then
		return false
	end
	if live.IsDead and live:IsDead() then
		return false
	end
	return true
end

local function lRecalcUnitAndTwin(unit)
	if not unit or type(RecalcMaxHitPoints) ~= "function" then
		return
	end
	RecalcMaxHitPoints(unit)
	local sid = unit.session_id
	if not sid or not gv_UnitData then
		return
	end
	local ud = gv_UnitData[sid]
	if ud and ud ~= unit then
		RecalcMaxHitPoints(ud)
	end
	local live = g_Units and g_Units[sid]
	if live and live ~= unit then
		RecalcMaxHitPoints(live)
	end
end

function JazzRecalcCombatTraumaMaxHitPoints()
	for _, unit in ipairs(g_Units or empty_table) do
		if unit then
			lRecalcUnitAndTwin(unit)
		end
	end
end

function JazzApplyPendingTraumaMaxHpDebt()
	rawset(_G, "g_JAZZ_MED007_ForceDebt", true)
	JazzRecalcCombatTraumaMaxHitPoints()
	rawset(_G, "g_JAZZ_MED007_ForceDebt", false)
end

function OnMsg.CombatStart()
	JazzRecalcCombatTraumaMaxHitPoints()
end

function OnMsg.CombatEnd()
	JazzApplyPendingTraumaMaxHpDebt()
end
