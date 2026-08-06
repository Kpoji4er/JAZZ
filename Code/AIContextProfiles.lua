-- JAZZ-AI-CTX-001 / CMD-001 helpers: context profiles + officer aura directives.

MapVar("JazzAI_TeamDirectives", {})
MapVar("JazzAI_PeekStreak", {})
MapVar("JazzAI_SniperUselessStreak", {})
MapVar("JazzAI_FlarePushUntil", false)
MapVar("JazzAI_TeamActed", {})
MapVar("JazzAI_TeamActedTurn", false)

-- ACT-002: who already finished AIPlayAttacks this combat turn (smoke self-cover gate).
function JazzAI_EnsureTeamActedTable()
	local turn = g_Combat and g_Combat.current_turn
	if JazzAI_TeamActedTurn ~= turn then
		JazzAI_TeamActed = {}
		JazzAI_TeamActedTurn = turn
	end
	JazzAI_TeamActed = JazzAI_TeamActed or {}
end

function JazzAI_MarkUnitActed(unit)
	if not IsValid(unit) then
		return
	end
	JazzAI_EnsureTeamActedTable()
	JazzAI_TeamActed[unit.session_id or unit.handle] = true
end

function JazzAI_AllyHasActed(ally)
	if not IsValid(ally) then
		return false
	end
	JazzAI_EnsureTeamActedTable()
	return not not JazzAI_TeamActed[ally.session_id or ally.handle]
end

function JazzAI_CountIndoorRatio()
	-- Lightweight heuristic: sample pass slabs near combat units.
	local indoor, total = 0, 0
	for _, u in ipairs(g_Units or empty_table) do
		if IsValid(u) and not u:IsDead() then
			local dest = GetPackedPosAndStance(u)
			if dest then
				total = total + 1
				if AICheckIndoors and AICheckIndoors(dest) then
					indoor = indoor + 1
				end
			end
		end
	end
	if total <= 0 then
		return 0
	end
	return MulDivRound(indoor, 100, total)
end

function JazzAI_IsUrbanContext()
	local ratio = JazzAI_CountIndoorRatio()
	if ratio >= 35 then
		return true
	end
	local sector = gv_CurrentSectorId and gv_Sectors and gv_Sectors[gv_CurrentSectorId]
	if sector and sector.City and sector.City ~= "none" then
		return true
	end
	return false
end

function JazzAI_ResolveContextProfile()
	local profile = {
		id = "Default",
		TakeCoverMul = 100,
		FlankingMul = 100,
		MobileShotMul = 100,
		OverwatchMinScore = nil,
		SniperHold = false,
		NoFlareWait = false,
		Urban = JazzAI_IsUrbanContext(),
	}
	if profile.Urban then
		profile.id = "Urban"
		profile.TakeCoverMul = 150
		profile.MobileShotMul = 80
	end
	if GameState.Night or GameState.Underground then
		profile.id = profile.Urban and "UrbanNight" or "Night"
		profile.TakeCoverMul = Max(profile.TakeCoverMul, 140)
		profile.SniperHold = true
		profile.OverwatchMinScore = 150
		profile.MobileShotMul = 70
	elseif GameState.Fog or GameState.DustStorm then
		profile.id = "FogDust"
		profile.TakeCoverMul = Max(profile.TakeCoverMul, 160)
		profile.FlankingMul = 70
		profile.NoFlareWait = true -- F12: no illuminate-wait
		profile.OverwatchMinScore = 120
		profile.MobileShotMul = 60
	elseif GameState.FireStorm then
		profile.id = "FireStorm"
		profile.TakeCoverMul = 130
	elseif GameState.RainHeavy then
		profile.id = "RainHeavy"
		profile.TakeCoverMul = 120
		profile.MobileShotMul = 85
	end
	return profile
end

function JazzAI_ApplyProfileToContext(context)
	if not context then
		return
	end
	context.jazz_profile = JazzAI_ResolveContextProfile()
end

-- CMD-001 officer aura
-- Unit.class is often just "Unit"; prefer unitdatadef_id (e.g. RebelSergeant_Immortal_M1).
function JazzAI_OfficerAuraUnitClassName(unit)
	if not unit then
		return ""
	end
	local id = unit.unitdatadef_id or unit.className or unit.class or ""
	if id == "Unit" then
		id = unit.unitdatadef_id or unit.className or ""
	end
	return id
end

function JazzAI_OfficerAuraRadius(unit)
	local class = JazzAI_OfficerAuraUnitClassName(unit)
	-- Named NPC commanders with captain-tier (map-wide) aura. Class substring
	-- "Captain" already covers Legion/Adonis captains; add rebel/special IDs here.
	local captain_named = rawget(_G, "JazzAI_OfficerAuraCaptainUnitDefs")
	if captain_named and class ~= "" and captain_named[class] then
		return 1000
	end
	local function has_leader_kw()
		local keys = unit and unit.AIKeywords
		if not keys then
			local def = unit and unit.unitdatadef_id and UnitDataDefs and UnitDataDefs[unit.unitdatadef_id]
			keys = def and def.AIKeywords
		end
		if not keys then
			return false
		end
		for _, k in ipairs(keys) do
			if k == "Leader" then
				return true
			end
		end
		return false
	end
	if class:find("Captain", 1, true) or class:find("MercenaryCaptain", 1, true) then
		return 1000 -- whole map
	end
	if class:find("Lieutenant", 1, true) then
		return 25
	end
	if class:find("Sergeant", 1, true) or has_leader_kw() then
		return 15
	end
	return 0
end

-- Captain-tier map aura for named NPC commanders (not class-name Captain).
JazzAI_OfficerAuraCaptainUnitDefs = {
	Rebel_NPC_Ghost = true, -- Dyalo "Ghost" — rebel named commander
}

-- CMD-001 distance bands (tiles to nearest enemy from the officer).
local JazzAI_DirectivePushMax = 12
local JazzAI_DirectiveEnvelopMin = 24
local JazzAI_DirectiveHideMin = 18

function JazzAI_UnitHpPercent(unit)
	if not IsValid(unit) then
		return 100
	end
	return MulDivRound(unit.HitPoints or 0, 100, Max(1, unit.MaxHitPoints or 1))
end

-- Heavy losses: ≥2 dead and ≥25% of squad dead, or ≥50% of living allies ≤45% HP (≥2 wounded).
function JazzAI_TeamNeedsFallBack(unit)
	local team = unit and unit.team
	if not team or not team.units then
		return false
	end
	local living, wounded, dead = 0, 0, 0
	for _, ally in ipairs(team.units) do
		if ally:IsDead() then
			dead = dead + 1
		else
			living = living + 1
			if JazzAI_UnitHpPercent(ally) <= 45 then
				wounded = wounded + 1
			end
		end
	end
	local total = living + dead
	if total <= 0 then
		return false
	end
	if dead >= 2 and MulDivRound(dead, 100, total) >= 25 then
		return true
	end
	if living > 0 and wounded >= 2 and MulDivRound(wounded, 100, living) >= 50 then
		return true
	end
	return false
end

-- Lowest-HP visible enemy at ≤40% HP (clear finish target).
function JazzAI_FindFocusFireTarget(unit)
	if not IsValid(unit) then
		return false
	end
	local enemies = GetEnemies and GetEnemies(unit)
	if not enemies then
		return false
	end
	local best, best_hpp = false, 101
	for _, enemy in ipairs(enemies) do
		if IsValid(enemy) and not enemy:IsDead() then
			local visible = (HasVisibilityTo and HasVisibilityTo(unit.team, enemy))
				or (HasVisibilityTo and HasVisibilityTo(unit, enemy))
			if visible then
				local hpp = JazzAI_UnitHpPercent(enemy)
				if hpp <= 40 and hpp < best_hpp then
					best, best_hpp = enemy, hpp
				end
			end
		end
	end
	return best
end

-- Player winning a long-range firefight: distant healthy mercs + wounded allies / peek pressure.
function JazzAI_ShouldTakeCoverFromRange(unit, tiles)
	if (tiles or 0) < JazzAI_DirectiveHideMin then
		return false
	end
	local team = unit and unit.team
	if not team or not team.units then
		return false
	end
	local ally_n, ally_hurt = 0, 0
	for _, ally in ipairs(team.units) do
		if not ally:IsDead() then
			ally_n = ally_n + 1
			if JazzAI_UnitHpPercent(ally) < 70 then
				ally_hurt = ally_hurt + 1
			end
		end
	end
	local scale = const.SlabSizeX
	local far_healthy, peek_pressure = 0, 0
	local enemies = (GetEnemies and GetEnemies(unit)) or empty_table
	for _, enemy in ipairs(enemies) do
		if IsValid(enemy) and not enemy:IsDead() then
			local et = DivRound(unit:GetDist(enemy), scale)
			if et >= 16 and JazzAI_UnitHpPercent(enemy) >= 60 then
				far_healthy = far_healthy + 1
			end
			if JazzAI_EnemyPeekStreak and JazzAI_EnemyPeekStreak(enemy) >= 2 then
				peek_pressure = peek_pressure + 1
			end
		end
	end
	if far_healthy >= 1 and ally_hurt >= 1 then
		return true
	end
	if peek_pressure >= 1 and ally_hurt >= 1 then
		return true
	end
	if tiles >= JazzAI_DirectiveEnvelopMin and ally_n > 0 and MulDivRound(ally_hurt, 100, ally_n) >= 40 then
		return true
	end
	return false
end

function JazzAI_UnitCanAttemptHidden(unit)
	if not IsValid(unit) or unit:IsDead() then
		return false
	end
	if unit:HasStatusEffect("Hidden") then
		return true
	end
	if not unit.GetStanceToStealth or not unit.CanStealth then
		return false
	end
	local stance = unit:GetStanceToStealth()
	return not not unit:CanStealth(stance)
end

-- Prefer GoHidden when a meaningful share of the living team can stealth.
function JazzAI_TeamCanMostlyStealth(unit)
	local team = unit and unit.team
	if not team or not team.units then
		return false
	end
	local able, total = 0, 0
	for _, ally in ipairs(team.units) do
		if not ally:IsDead() then
			total = total + 1
			if JazzAI_UnitCanAttemptHidden(ally) then
				able = able + 1
			end
		end
	end
	return total > 0 and MulDivRound(able, 100, total) >= 40
end

-- Attempt Hidden status (not PickCustom — ROLE-002 forbids Hide() there).
function JazzAI_TryUnitGoHidden(unit)
	if not IsValid(unit) or unit:IsDead() then
		return false
	end
	if unit:HasStatusEffect("Hidden") then
		return true
	end
	if not unit.GetStanceToStealth or not unit.CanStealth or not unit.Hide then
		return false
	end
	local stance = unit:GetStanceToStealth()
	if unit:CanStealth(stance) then
		unit:Hide()
		return unit:HasStatusEffect("Hidden")
	end
	return false
end

function JazzAI_ApplyGoHiddenDirective(source, radius, team)
	if not team or not team.units or not IsValid(source) then
		return
	end
	for _, ally in ipairs(team.units) do
		if not ally:IsDead() then
			if ally == source or JazzAI_IsInOfficerAura(ally, source, radius) then
				JazzAI_TryUnitGoHidden(ally)
			end
		end
	end
end

-- Convenient fighting houses: urban / indoor-heavy map (same signal as CTX Urban).
function JazzAI_ShouldOccupyBuildings(unit)
	if JazzAI_IsUrbanContext and JazzAI_IsUrbanContext() then
		return true
	end
	return (JazzAI_CountIndoorRatio and JazzAI_CountIndoorRatio() or 0) >= 30
end

function JazzAI_PickOfficerDirective(unit, profile)
	profile = profile or JazzAI_ResolveContextProfile()
	-- Survival first.
	if JazzAI_TeamNeedsFallBack(unit) then
		return "FallBack"
	end
	-- Low vis: prefer real Hidden when enough of the team can stealth.
	if profile.SniperHold or profile.id == "FogDust" then
		if JazzAI_TeamCanMostlyStealth(unit) then
			return "GoHidden"
		end
		return "LowVisHold"
	end
	local enemy, dist = GetNearestEnemy(unit)
	if not enemy then
		if JazzAI_ShouldOccupyBuildings(unit) then
			return "OccupyBuildings"
		end
		return "HoldLine"
	end
	local tiles = dist and DivRound(dist, const.SlabSizeX) or 99
	if JazzAI_FindFocusFireTarget(unit) then
		return "FocusFire"
	end
	if JazzAI_ShouldTakeCoverFromRange(unit, tiles) then
		if JazzAI_TeamCanMostlyStealth(unit) then
			return "GoHidden"
		end
		return "TakeCover"
	end
	if tiles <= JazzAI_DirectivePushMax then
		return "Push"
	end
	-- Urban mid-range: hold buildings instead of open HoldLine.
	if JazzAI_ShouldOccupyBuildings(unit) and tiles < JazzAI_DirectiveEnvelopMin then
		return "OccupyBuildings"
	end
	if tiles >= JazzAI_DirectiveEnvelopMin then
		return "Envelop"
	end
	return "HoldLine"
end

function JazzAI_GetTeamFocusTarget(unit)
	if not unit or not unit.team then
		return false
	end
	local team = unit.team
	local entry = (JazzAI_TeamDirectives or empty_table)[team.side or team.handle or tostring(team)]
	if not entry or entry.directive ~= "FocusFire" or not entry.source or entry.source:IsDead() then
		return false
	end
	if not JazzAI_IsInOfficerAura(unit, entry.source, entry.radius) then
		return false
	end
	local focus = entry.focus_target
	if not IsValid(focus) or focus:IsDead() then
		return false
	end
	return focus
end

function JazzAI_IsInOfficerAura(unit, source, radius)
	if not IsValid(unit) or not IsValid(source) or unit:IsDead() then
		return false
	end
	if (radius or 0) >= 1000 then
		return true
	end
	local dist = DivRound(unit:GetDist(source), const.SlabSizeX)
	return dist <= (radius or 0)
end

function JazzAI_SetAuraEffect(unit, effect_id, enabled)
	if not IsValid(unit) then
		return
	end
	local has = unit:HasStatusEffect(effect_id)
	if enabled and not has then
		unit:AddStatusEffect(effect_id)
	elseif not enabled and has then
		unit:RemoveStatusEffect(effect_id)
	end
end

-- Player-facing directive labels (tooltip). Radii stay internal — not shown in UI text.
function JazzAI_GetDirectiveDisplayName(directive)
	if directive == "HoldLine" then
		return T(890000000006106, --[[JazzAI directive HoldLine]] "Держать линию")
	elseif directive == "Push" then
		return T(890000000006107, --[[JazzAI directive Push]] "Давить")
	elseif directive == "Envelop" then
		return T(890000000006108, --[[JazzAI directive Envelop]] "Охват")
	elseif directive == "LowVisHold" then
		return T(890000000006109, --[[JazzAI directive LowVisHold]] "Низкая видимость — держать")
	elseif directive == "FallBack" then
		return T(890000000006110, --[[JazzAI directive FallBack]] "Отход")
	elseif directive == "FocusFire" then
		return T(890000000006111, --[[JazzAI directive FocusFire]] "Сосредоточить огонь")
	elseif directive == "OccupyBuildings" then
		return T(890000000006115, --[[JazzAI directive OccupyBuildings]] "Занимать дома")
	elseif directive == "TakeCover" then
		return T(890000000006116, --[[JazzAI directive TakeCover]] "Спрятаться")
	elseif directive == "GoHidden" then
		return T(890000000006117, --[[JazzAI directive GoHidden]] "Скрыться")
	end
	return false
end

function JazzAI_FindStatusEffectOwner(effect)
	if not effect or not effect.class then
		return false
	end
	for _, u in ipairs(g_Units or empty_table) do
		if IsValid(u) and u:GetStatusEffect(effect.class) == effect then
			return u
		end
	end
	return false
end

function JazzAI_GetEffectDirective(effect)
	if not effect then
		return false
	end
	-- InstParameters only — do not use ResolveValue("directive") here: Description
	-- ResolveValue is overridden on aura perks and must not recurse into this helper.
	local directive
	if effect.InstParameters then
		local found = table.find_value(effect.InstParameters, "Name", "directive")
		if found and found.Value and found.Value ~= "" and found.Value ~= false then
			directive = found.Value
		end
	end
	if directive then
		return directive
	end
	local owner = JazzAI_FindStatusEffectOwner(effect)
	if not owner then
		return false
	end
	directive = JazzAI_GetTeamDirective(owner)
	if directive then
		return directive
	end
	-- Source tooltip / ally officer: team entry may exist even if radius gate fails.
	local team = owner.team
	if not team then
		return false
	end
	local entry = (JazzAI_TeamDirectives or empty_table)[team.side or team.handle or tostring(team)]
	if entry and entry.directive and entry.directive ~= "" then
		return entry.directive
	end
	return false
end

function JazzAI_SetAuraDirectiveParam(unit, effect_id, directive)
	if not IsValid(unit) then
		return
	end
	local eff = unit:GetStatusEffect(effect_id)
	if eff and eff.SetParameter then
		eff:SetParameter("directive", directive or false)
	end
end

-- Strip a previously appended order line if ResolveValue/GetProperty re-entered format.
local function JazzAI_StripOfficerAuraOrderLine(base_desc)
	if type(base_desc) ~= "string" then
		return base_desc
	end
	local markers = { "Текущий приказ:", "Следует приказу:", "Current order:", "Following order:" }
	for _, marker in ipairs(markers) do
		local cut = string.find(base_desc, marker, 1, true)
		if cut and cut > 1 then
			base_desc = string.match(base_desc, "^(.-)%s*\n") or string.sub(base_desc, 1, cut - 1)
			base_desc = string.gsub(base_desc, "%s+$", "")
			break
		end
	end
	return base_desc
end

-- If badge exists but MapVar/InstParameter was cleared (CombatStart gap, hot-reload),
-- ensure the owning officer writes a real directive before the tooltip renders.
function JazzAI_EnsureEffectDirective(effect)
	local directive = JazzAI_GetEffectDirective(effect)
	if directive then
		return directive
	end
	local owner = JazzAI_FindStatusEffectOwner(effect)
	if not owner or not owner.team then
		return false
	end
	if JazzAI_OfficerAuraRadius(owner) > 0 then
		JazzAI_WriteOfficerAura(owner)
	else
		JazzAI_RefreshOfficerAurasForTeam(owner.team)
	end
	return JazzAI_GetEffectDirective(effect)
end

-- kind: "source" (commander) or "influence" (receiver).
-- Consumed via ResolveValue("Description") on Jazz_Perk_OfficerAura* (combat-badge INFO).
function JazzAI_FormatOfficerAuraDescription(effect, base, kind)
	base = JazzAI_StripOfficerAuraOrderLine(base or "")
	local order = JazzAI_GetDirectiveDisplayName(JazzAI_EnsureEffectDirective(effect))
	if not order then
		-- Last resort: default HoldLine so a visible officer badge never shows "not chosen".
		order = JazzAI_GetDirectiveDisplayName("HoldLine")
			or T(890000000006114, --[[JazzAI officer aura no order]] "приказ не выбран")
	end
	local line
	if kind == "influence" then
		line = T{890000000006113, --[[JazzAI officer aura influence current order]] "Следует приказу: <em><order></em>", order = order}
	else
		line = T{890000000006112, --[[JazzAI officer aura current order]] "Текущий приказ: <em><order></em>", order = order}
	end
	return table.concat({ base, line }, "\n\n")
end

function JazzAI_WriteOfficerAura(unit)
	if not unit or not unit.team then
		return
	end
	local radius = JazzAI_OfficerAuraRadius(unit)
	if radius <= 0 then
		JazzAI_SetAuraEffect(unit, "Jazz_Perk_OfficerAura", false)
		return
	end
	local profile = JazzAI_ResolveContextProfile()
	local directive = JazzAI_PickOfficerDirective(unit, profile)
	local team = unit.team
	JazzAI_TeamDirectives = JazzAI_TeamDirectives or {}
	local key = team.side or team.handle or tostring(team)
	local entry = JazzAI_TeamDirectives[key] or {}
	entry.directive = directive
	entry.source = unit
	entry.radius = radius
	entry.pos = unit:GetPos()
	if directive == "FocusFire" then
		entry.focus_target = JazzAI_FindFocusFireTarget(unit) or false
	else
		entry.focus_target = false
	end
	JazzAI_TeamDirectives[key] = entry

	-- Commander: visible command aura perk
	JazzAI_SetAuraEffect(unit, "Jazz_Perk_OfficerAura", true)
	JazzAI_SetAuraEffect(unit, "Jazz_Perk_OfficerAuraInfluence", false)
	JazzAI_SetAuraDirectiveParam(unit, "Jazz_Perk_OfficerAura", directive)

	-- Allies in radius: under aura influence perk
	for _, ally in ipairs(team.units) do
		if ally ~= unit and not ally:IsDead() then
			local in_aura = JazzAI_IsInOfficerAura(ally, unit, radius)
			JazzAI_SetAuraEffect(ally, "Jazz_Perk_OfficerAuraInfluence", in_aura)
			JazzAI_SetAuraEffect(ally, "Jazz_Perk_OfficerAura", false)
			if in_aura then
				JazzAI_SetAuraDirectiveParam(ally, "Jazz_Perk_OfficerAuraInfluence", directive)
			end
		end
	end

	if directive == "GoHidden" then
		JazzAI_ApplyGoHiddenDirective(unit, radius, team)
	end
end

function JazzAI_RefreshOfficerAurasForTeam(team)
	if not team or not team.units then
		return
	end
	local best, best_rank = false, -1
	for _, u in ipairs(team.units) do
		if not u:IsDead() then
			local r = JazzAI_OfficerAuraRadius(u)
			if r > best_rank then
				best_rank = r
				best = u
			end
		end
	end
	if best then
		JazzAI_WriteOfficerAura(best)
	else
		for _, u in ipairs(team.units) do
			JazzAI_SetAuraEffect(u, "Jazz_Perk_OfficerAura", false)
			JazzAI_SetAuraEffect(u, "Jazz_Perk_OfficerAuraInfluence", false)
		end
	end
end

-- Refresh every combat team (player / ally / enemy) so Rebel officers like Burda
-- get JazzAI_TeamDirectives written even before their own UnitBeginTurn.
function JazzAI_RefreshAllOfficerAuras()
	local seen = {}
	for _, u in ipairs(g_Units or empty_table) do
		local team = u and u.team
		if team and not seen[team] then
			seen[team] = true
			JazzAI_RefreshOfficerAurasForTeam(team)
		end
	end
end

function JazzAI_GetTeamDirective(unit)
	if not unit or not unit.team then
		return false
	end
	local team = unit.team
	local entry = (JazzAI_TeamDirectives or empty_table)[team.side or team.handle or tostring(team)]
	if not entry or not entry.source or entry.source:IsDead() then
		return false
	end
	if not JazzAI_IsInOfficerAura(unit, entry.source, entry.radius) then
		return false
	end
	return entry.directive
end

function JazzAI_NoteEnemyPeek(enemy)
	if not IsValid(enemy) then
		return
	end
	JazzAI_PeekStreak = JazzAI_PeekStreak or {}
	local key = enemy.handle or tostring(enemy)
	JazzAI_PeekStreak[key] = (JazzAI_PeekStreak[key] or 0) + 1
end

function JazzAI_EnemyPeekStreak(enemy)
	if not enemy then
		return 0
	end
	JazzAI_PeekStreak = JazzAI_PeekStreak or {}
	return JazzAI_PeekStreak[enemy.handle or tostring(enemy)] or 0
end

function OnMsg.CombatStart()
	JazzAI_TeamDirectives = {}
	JazzAI_PeekStreak = {}
	JazzAI_SniperUselessStreak = {}
	JazzAI_FlarePushUntil = false
	JazzAI_TeamActed = {}
	JazzAI_TeamActedTurn = false
	-- Write directives immediately so ally officers (Burda) show a real order
	-- before the first UnitBeginTurn — CombatStart alone used to leave MapVar empty.
	JazzAI_RefreshAllOfficerAuras()
end

function OnMsg.CombatEnd()
	for _, u in ipairs(g_Units or empty_table) do
		JazzAI_SetAuraEffect(u, "Jazz_Perk_OfficerAura", false)
		JazzAI_SetAuraEffect(u, "Jazz_Perk_OfficerAuraInfluence", false)
	end
	JazzAI_TeamDirectives = {}
end

function OnMsg.UnitBeginTurn(unit)
	-- Refresh all teams so ally Rebel officers keep directive + badge on player turns too.
	if IsValid(unit) and not unit:IsDead() then
		JazzAI_RefreshAllOfficerAuras()
		-- Re-attempt Hidden each turn while GoHidden is active (CanStealth may open after stance/move).
		if JazzAI_GetTeamDirective(unit) == "GoHidden" then
			JazzAI_TryUnitGoHidden(unit)
		end
	end
end

function OnMsg.UnitAttack(attacker)
	if IsValid(attacker) and IsMerc(attacker) then
		JazzAI_NoteEnemyPeek(attacker)
	end
end
