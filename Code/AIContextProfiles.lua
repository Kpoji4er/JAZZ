-- JAZZ-AI-CTX-001 / CMD-001 helpers: context profiles + officer aura directives.

MapVar("JazzAI_TeamDirectives", {})
MapVar("JazzAI_PeekStreak", {})
MapVar("JazzAI_FlarePushUntil", false)

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
function JazzAI_OfficerAuraRadius(unit)
	local class = (unit and (unit.class or "")) or ""
	local function has_leader_kw()
		local keys = unit and unit.AIKeywords
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

function JazzAI_PickOfficerDirective(unit, profile)
	profile = profile or JazzAI_ResolveContextProfile()
	if profile.SniperHold or profile.id == "FogDust" then
		return "LowVisHold"
	end
	local enemy, dist = GetNearestEnemy(unit)
	if not enemy then
		return "HoldLine"
	end
	local tiles = dist and DivRound(dist, const.SlabSizeX) or 99
	if tiles <= 8 then
		return "Push"
	end
	if tiles >= 16 then
		return "Envelop"
	end
	return "HoldLine"
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
	JazzAI_TeamDirectives[key] = entry

	-- Commander: visible command aura perk
	JazzAI_SetAuraEffect(unit, "Jazz_Perk_OfficerAura", true)
	JazzAI_SetAuraEffect(unit, "Jazz_Perk_OfficerAuraInfluence", false)

	-- Allies in radius: under aura influence perk
	for _, ally in ipairs(team.units) do
		if ally ~= unit and not ally:IsDead() then
			local in_aura = JazzAI_IsInOfficerAura(ally, unit, radius)
			JazzAI_SetAuraEffect(ally, "Jazz_Perk_OfficerAuraInfluence", in_aura)
			JazzAI_SetAuraEffect(ally, "Jazz_Perk_OfficerAura", false)
		end
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
	JazzAI_FlarePushUntil = false
end

function OnMsg.CombatEnd()
	for _, u in ipairs(g_Units or empty_table) do
		JazzAI_SetAuraEffect(u, "Jazz_Perk_OfficerAura", false)
		JazzAI_SetAuraEffect(u, "Jazz_Perk_OfficerAuraInfluence", false)
	end
	JazzAI_TeamDirectives = {}
end

function OnMsg.UnitBeginTurn(unit)
	-- Refresh aura from living officers so badges stay correct as units move
	if IsValid(unit) and unit.team and not unit:IsDead() then
		if JazzAI_OfficerAuraRadius(unit) > 0 then
			JazzAI_WriteOfficerAura(unit)
		else
			JazzAI_RefreshOfficerAurasForTeam(unit.team)
		end
	end
end

function OnMsg.UnitAttack(attacker)
	if IsValid(attacker) and IsMerc(attacker) then
		JazzAI_NoteEnemyPeek(attacker)
	end
end
