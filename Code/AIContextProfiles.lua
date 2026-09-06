-- JAZZ-AI-CTX-001 / CMD-001 helpers: context profiles + officer aura directives.

MapVar("JazzAI_TeamDirectives", {})
MapVar("JazzAI_TeamDirectiveFatigue", {})
MapVar("JazzAI_PeekStreak", {})
MapVar("JazzAI_SniperUselessStreak", {})
MapVar("JazzAI_FlarePushUntil", false)
MapVar("JazzAI_TeamActed", {})
MapVar("JazzAI_TeamActedTurn", false)
MapVar("JazzAI_TeamActSlots", {})
MapVar("JazzAI_TeamActSlotsTurn", false)
MapVar("JazzAI_TeamExplosiveThrows", {})
MapVar("JazzAI_TeamExplosiveThrowTurn", false)
MapVar("JazzAI_TeamFallBackState", {})

-- Optional jazz-units exports. Bare-read of a missing name asserts
-- (mod env ≠ units env / GetRawG). CombatAI binds the full list; stub here
-- if this file reloads first.
if type(rawget(_G, "JazzAI_BindAllUnitsExports")) == "function" then
	JazzAI_BindAllUnitsExports()
else
	rawset(_G, "JazzAI_PickTeamSemiSniper", rawget(_G, "JazzAI_PickTeamSemiSniper") or false)
	rawset(_G, "JazzAI_PickTeamPseudoMG", rawget(_G, "JazzAI_PickTeamPseudoMG") or false)
	rawset(_G, "JazzAI_PickTeamPusher", rawget(_G, "JazzAI_PickTeamPusher") or false)
	rawset(_G, "JazzAI_InferRoleFamily", rawget(_G, "JazzAI_InferRoleFamily") or false)
	rawset(_G, "JazzAI_UnitIsDynamicPseudoMG", rawget(_G, "JazzAI_UnitIsDynamicPseudoMG") or false)
	rawset(_G, "JazzAI_UnitIsDedicatedMG", rawget(_G, "JazzAI_UnitIsDedicatedMG") or false)
	rawset(_G, "JazzAI_UnitIsDynamicSemiSniper", rawget(_G, "JazzAI_UnitIsDynamicSemiSniper") or false)
	rawset(_G, "JazzAI_UnitIsDedicatedSniper", rawget(_G, "JazzAI_UnitIsDedicatedSniper") or false)
	rawset(_G, "JazzAI_UnitIsDynamicPusher", rawget(_G, "JazzAI_UnitIsDynamicPusher") or false)
	rawset(_G, "JazzAI_TryMedicSwitch", rawget(_G, "JazzAI_TryMedicSwitch") or false)
	rawset(_G, "JazzAI_FactionArchetypePrefix", rawget(_G, "JazzAI_FactionArchetypePrefix") or false)
end

-- JAZZ-AI-007: recontact standoff (tiles from last_known) and scout path margin.
JazzAI_RecontactStandMin = 14
JazzAI_RecontactStandMax = 20
JazzAI_RecontactMapEdgeTiles = 8
JazzAI_RecontactPathMargin = 24
-- JAZZ-AI-008: stay bonus when dest is an egress perch (CheckLOS to peek cell).
JazzAI_EgressPerchStayBonus = 180
-- JAZZ-AI-009: FallBack peel dest that breaks LoS and can OW the vacated tile.
JazzAI_BreakLosOwDestBonus = 220
-- CMD-003: Push when a spotter has a live shot; cling window for non-perch on Heights.
JazzAI_DirectivePushLiveShot = 600
JazzAI_HeightsClingMin = 2
JazzAI_HeightsClingMax = 10

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
	if type(rawget(_G, "JazzAI_BindAllUnitsExports")) == "function" then
		JazzAI_BindAllUnitsExports()
	end
	context.jazz_profile = JazzAI_ResolveContextProfile()
	local unit = context.unit
	local directive = unit and JazzAI_GetTeamDirective and JazzAI_GetTeamDirective(unit)
	context.jazz_directive = directive or false
	context.jazz_fallback = directive == "FallBack"
	local perch = unit and JazzAI_UnitIsLinePerchHolder and JazzAI_UnitIsLinePerchHolder(unit, context)
	local spotter = unit and JazzAI_UnitIsHeightsSpotter and JazzAI_UnitIsHeightsSpotter(unit)
	-- HighGround ×175% only for perch on Heights, or optics that must stay up on Push.
	context.jazz_occupy_heights = (directive == "OccupyHeights" and perch)
		or (directive == "Push" and spotter)
	context.jazz_heights_cling = false
	context.jazz_cling_anchor = false
	if directive == "OccupyHeights" and unit and not perch then
		context.jazz_heights_cling = true
		if JazzAI_PickHeightsClingAnchor then
			context.jazz_cling_anchor = JazzAI_PickHeightsClingAnchor(unit) or false
		end
		context.jazz_profile.TakeCoverMul = Max(context.jazz_profile.TakeCoverMul or 100, 150)
	end
	if context.jazz_fallback then
		context.jazz_profile.TakeCoverMul = Max(context.jazz_profile.TakeCoverMul or 100, 180)
	end
	-- Heavy / Rocketeer / Ordnance: prefer staying behind the front.
	if unit and JazzAI_UnitWantsRearGuard and JazzAI_UnitWantsRearGuard(unit) then
		context.jazz_rear_guard = true
	end
	-- Mortar (Bombard) cannot fire indoors — never sit in buildings.
	if unit and JazzAI_UnitNeedsOutdoorFire and JazzAI_UnitNeedsOutdoorFire(unit) then
		context.jazz_need_outdoors = true
	end
	-- Dynamic pseudo-MG: bias toward Overwatch like Machinegunner.
	local is_pseudo = JazzAI_BindUnitsExport and JazzAI_BindUnitsExport("JazzAI_UnitIsDynamicPseudoMG")
	if unit and type(is_pseudo) == "function" and is_pseudo(unit) then
		context.jazz_pseudo_mg = true
		context.jazz_profile.OverwatchMinScore = Min(context.jazz_profile.OverwatchMinScore or 300, 80)
	end
	-- Dedicated / pseudo MG: stay near squad (OptLoc half-cover chase used to pull them alone).
	local is_mg = JazzAI_BindUnitsExport and JazzAI_BindUnitsExport("JazzAI_UnitIsDedicatedMG")
	if unit and ((type(is_mg) == "function" and is_mg(unit)) or context.jazz_pseudo_mg) then
		context.jazz_mg_tether = true
	end
end

function JazzAI_UnitNeedsOutdoorFire(unit)
	if not IsValid(unit) then
		return false
	end
	local class = (unit.unitdatadef_id or unit.className or unit.class or "")
	if type(class) == "string" and class:find("Mortar", 1, true) then
		return true
	end
	if unit.GetEquippedWeapons then
		for _, slot in ipairs({ "Handheld A", "Handheld B" }) do
			for _, w in ipairs(unit:GetEquippedWeapons(slot) or empty_table) do
				if IsKindOf(w, "Mortar") then
					return true
				end
			end
		end
	end
	local wep = unit.GetActiveWeapons and unit:GetActiveWeapons()
	if IsKindOf(wep, "Mortar") then
		return true
	end
	return false
end

function JazzAI_UnitWantsRearGuard(unit)
	if not IsValid(unit) then
		return false
	end
	local infer = JazzAI_BindUnitsExport and JazzAI_BindUnitsExport("JazzAI_InferRoleFamily")
		or rawget(_G, "JazzAI_InferRoleFamily")
	if type(infer) == "function" and infer(unit) == "Heavy" then
		return true
	end
	local keys = unit.AIKeywords
	if keys then
		for _, k in ipairs(keys) do
			if k == "Ordnance" then
				return true
			end
		end
	end
	local class = (unit.unitdatadef_id or unit.className or unit.class or "")
	if type(class) == "string" and (class:find("Rocketeer", 1, true) or class:find("Mortar", 1, true)
		or class:find("Heavy", 1, true)) then
		return true
	end
	if unit.GetEquippedWeapons then
		for _, slot in ipairs({ "Handheld A", "Handheld B" }) do
			for _, w in ipairs(unit:GetEquippedWeapons(slot) or empty_table) do
				if IsKindOfClasses(w, "RocketLauncher", "MissileLauncher", "Mortar") then
					return true
				end
			end
		end
	end
	return false
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
local JazzAI_DirectiveHeightsMin = 10
local JazzAI_DirectiveCloseThreat = 8
local JazzAI_DirectiveFatiguePerTurn = 80
local JazzAI_FocusFireMinThreat = 40
-- CMD-001 / owner 2026-08-21: FocusFire target score ×2 (was 1.8).
JazzAI_FocusFireScoreMul = 2

function JazzAI_UnitHpPercent(unit)
	if not IsValid(unit) then
		return 100
	end
	return MulDivRound(unit.HitPoints or 0, 100, Max(1, unit.MaxHitPoints or 1))
end

function JazzAI_CountLocalLivingAllies(unit, radius)
	local team = unit and unit.team
	if not team or not team.units then
		return 0
	end
	radius = radius or 8
	local scale = const.SlabSizeX
	local n = 0
	for _, ally in ipairs(team.units) do
		if not ally:IsDead() and DivRound(unit:GetDist(ally), scale) <= radius then
			n = n + 1
		end
	end
	return n
end

function JazzAI_TeamCasualtyCounts(team)
	if not team or not team.units then
		return 0, 0, 0, 0
	end
	local living, dead = 0, 0
	for _, ally in ipairs(team.units) do
		if ally:IsDead() then
			dead = dead + 1
		else
			living = living + 1
		end
	end
	local total = living + dead
	local pct = total > 0 and MulDivRound(dead, 100, total) or 0
	return living, dead, total, pct
end

function JazzAI_FallBackBand(pct)
	if (pct or 0) >= 70 then
		return 70
	end
	if pct >= 50 then
		return 50
	end
	if pct >= 30 then
		return 30
	end
	return 0
end

function JazzAI_GetFallBackState(team)
	local key = JazzAI_TeamDirectiveKey(team)
	if not key then
		return false
	end
	JazzAI_TeamFallBackState = JazzAI_TeamFallBackState or {}
	local st = JazzAI_TeamFallBackState[key]
	if not st then
		st = { committed = false, last_band = 0 }
		JazzAI_TeamFallBackState[key] = st
	end
	return st
end

-- Heavy losses: eligibility dead≥2 & ≥30%. Start is a per-band chance; cancel on merge (007).
function JazzAI_TeamNeedsFallBack(unit)
	local team = unit and unit.team
	if not team or not team.units then
		return false
	end
	local st = JazzAI_GetFallBackState(team)
	if not st then
		return false
	end
	if JazzAI_CountLocalLivingAllies(unit, 8) >= 3 then
		st.committed = false
		return false
	end
	local _, dead, total, pct = JazzAI_TeamCasualtyCounts(team)
	if total <= 0 or dead < 2 or pct < 30 then
		return false
	end
	if st.committed then
		return true
	end
	local enemy = GetNearestEnemy and GetNearestEnemy(unit)
	if not enemy then
		return false
	end
	local band = JazzAI_FallBackBand(pct)
	if band <= (st.last_band or 0) then
		return false
	end
	local roll = InteractionRand(100, "JazzAI_FallBack")
	st.last_band = band
	st.committed = roll < pct
	return st.committed
end

function JazzAI_UnitHasFlankKeyword(unit)
	local keys = unit and unit.AIKeywords
	if not keys then
		return false
	end
	for _, k in ipairs(keys) do
		if k == "Flank" then
			return true
		end
	end
	return false
end

local function JazzAI_RecontactInferFamily(unit)
	local infer = rawget(_G, "JazzAI_InferRoleFamily")
	if type(infer) ~= "function" and type(rawget(_G, "JazzAI_BindUnitsExport")) == "function" then
		infer = JazzAI_BindUnitsExport("JazzAI_InferRoleFamily")
	end
	if type(infer) == "function" then
		return infer(unit)
	end
	return false
end

-- 0 = scout/flanker, 1 = assaulter/roughneck fallback, false = not a creeper.
function JazzAI_RecontactCreeperRank(unit)
	if not IsValid(unit) or unit:IsDead() then
		return false
	end
	local family = JazzAI_RecontactInferFamily(unit)
	if family == "Leader" or family == "MG" or family == "Heavy" or family == "Medic" then
		return false
	end
	local arch = tostring(unit.current_archetype or unit.archetype or "")
	local class = tostring(unit.unitdatadef_id or "")
	if family == "Scout" or JazzAI_UnitHasFlankKeyword(unit)
		or string.find(arch, "Flanker", 1, true)
		or string.find(class, "Flanker", 1, true)
		or string.find(class, "Scout", 1, true) then
		return 0
	end
	if family == "Pusher" or string.find(arch, "Assaulter", 1, true)
		or string.find(class, "Assault", 1, true)
		or string.find(class, "Roughneck", 1, true) then
		return 1
	end
	return false
end

function JazzAI_UnitIsRecontactProbeCandidate(unit)
	return JazzAI_RecontactCreeperRank(unit) ~= false
end

function JazzAI_AssignRecontactProbes(team)
	if not team or not team.units then
		return
	end
	local key = JazzAI_TeamDirectiveKey(team)
	JazzAI_TeamDirectives = JazzAI_TeamDirectives or {}
	local entry = JazzAI_TeamDirectives[key] or {}
	JazzAI_TeamDirectives[key] = entry
	local known
	for _, u in ipairs(team.units) do
		if not u:IsDead() and u.last_known_enemy_pos then
			known = u.last_known_enemy_pos
			break
		end
	end
	local cands = {}
	for _, u in ipairs(team.units) do
		local rank = JazzAI_RecontactCreeperRank(u)
		if rank then
			cands[#cands + 1] = { unit = u, rank = rank }
		end
	end
	table.sort(cands, function(a, b)
		if a.rank ~= b.rank then
			return a.rank < b.rank
		end
		if known then
			local da, db = a.unit:GetDist(known), b.unit:GetDist(known)
			if da ~= db then
				return da < db
			end
		end
		return (a.unit.handle or 0) < (b.unit.handle or 0)
	end)
	local creeper = cands[1] and cands[1].unit or false
	entry.recontact_creeper = creeper
	entry.recontact_probes = { creeper, false }
end

function JazzAI_UnitIsRecontactCreeper(unit)
	if not IsValid(unit) or not unit.team then
		return false
	end
	local entry = (JazzAI_TeamDirectives or empty_table)[JazzAI_TeamDirectiveKey(unit.team)]
	return entry and entry.recontact_creeper == unit
end

function JazzAI_UnitIsRecontactProbe(unit)
	return JazzAI_UnitIsRecontactCreeper(unit)
end

function JazzAI_RecontactCreeperShouldHide(unit)
	if not JazzAI_UnitIsRecontactCreeper(unit) then
		return false
	end
	local vis = unit.GetVisibleEnemies and unit:GetVisibleEnemies()
	return vis and #vis > 0
end

function JazzAI_TilesToLastKnown(unit, pos)
	local known = unit and unit.last_known_enemy_pos
	if not known then
		return false
	end
	local from = pos or (unit.GetPos and unit:GetPos())
	if not from then
		return false
	end
	return DivRound(from:Dist(known), const.SlabSizeX)
end

function JazzAI_ShouldRecontactScout(unit, picked)
	if not IsValid(unit) then
		return false
	end
	if picked == "Medic" or picked == "Deserter" or picked == "Melee"
		or picked == "Legion_Regroup" or picked == "PinnedDown" then
		return false
	end
	if JazzAI_GetTeamDirective and JazzAI_GetTeamDirective(unit) == "FallBack" then
		return false
	end
	if not JazzAI_UnitIsRecontactCreeper(unit) then
		return false
	end
	local vis = unit.GetVisibleEnemies and unit:GetVisibleEnemies()
	if vis and #vis > 0 then
		return false
	end
	if not unit.last_known_enemy_pos then
		return false
	end
	local tiles = JazzAI_TilesToLastKnown(unit)
	return tiles and tiles > (JazzAI_RecontactStandMax or 20)
end

function JazzAI_UnitIsFarmTarget(unit)
	if not IsValid(unit) or unit:IsDead() then
		return false
	end
	local team = unit.team
	if not team or team.player_team then
		return false
	end
	local seen, sees = false, false
	for _, other in ipairs(g_Teams or empty_table) do
		if other.player_team then
			for _, p in ipairs(other.units or empty_table) do
				if IsValid(p) and not p:IsDead() then
					if HasVisibilityTo(p, unit) or HasVisibilityTo(other, unit) then
						seen = true
					end
					if HasVisibilityTo(unit, p) or HasVisibilityTo(team, p) then
						sees = true
					end
				end
			end
		end
	end
	return seen and not sees
end

function JazzAI_DestNearMapEdge(dest_pos, edge_tiles)
	if not dest_pos then
		return false
	end
	local box = GetMapBox and GetMapBox()
	if not box or type(box.minx) ~= "function" then
		return false
	end
	local pad = (edge_tiles or JazzAI_RecontactMapEdgeTiles or 8) * const.SlabSizeX
	local x, y = dest_pos:xy()
	local minx, miny = box:minx(), box:miny()
	local maxx, maxy = box:maxx(), box:maxy()
	return x <= minx + pad or y <= miny + pad or x >= maxx - pad or y >= maxy - pad
end

function JazzAI_LastKnownNearMapEdge(unit, edge_tiles)
	local known = unit and unit.last_known_enemy_pos
	return known and JazzAI_DestNearMapEdge(known, edge_tiles)
end

function JazzAI_ScoreRecontactDest(context, dest)
	local unit = context and context.unit
	if not IsValid(unit) then
		return 0
	end
	local score = 0
	local x, y, z = stance_pos_unpack(dest)
	local dest_pos = point(x, y, z)
	local stay = context.unit_stance_pos
	local is_stay = stay and stance_pos_dist(dest, stay) == 0

	-- JAZZ-AI-008: line perch that sees player egress holds; skip walk-to-sound.
	if is_stay and JazzAI_ContextStayIsEgressPerch and JazzAI_ContextStayIsEgressPerch(context) then
		return JazzAI_EgressPerchStayBonus or 180
	end

	if JazzAI_UnitIsFarmTarget and JazzAI_UnitIsFarmTarget(unit) then
		if is_stay then
			score = score - 160
		else
			score = score + 50
			local nearest, ndist
			for _, team in ipairs(g_Teams or empty_table) do
				if team.player_team then
					for _, p in ipairs(team.units or empty_table) do
						if IsValid(p) and not p:IsDead()
							and (HasVisibilityTo(p, unit) or HasVisibilityTo(team, unit)) then
							local d = dest_pos:Dist(p:GetPos())
							if not ndist or d < ndist then
								nearest, ndist = p, d
							end
						end
					end
				end
			end
			if nearest then
				local cover = GetCoverFrom and GetCoverFrom(dest, GetPackedPosAndStance(nearest)) or 0
				if cover > 0 then
					score = score + 40
				end
			end
		end
	end

	local known = unit.last_known_enemy_pos
	local vis = unit.GetVisibleEnemies and unit:GetVisibleEnemies()
	local no_vis = not vis or #vis == 0
	if known and no_vis then
		local d_tiles = DivRound(dest_pos:Dist(known), const.SlabSizeX)
		local cur = JazzAI_TilesToLastKnown(unit) or d_tiles
		local stand_min = JazzAI_RecontactStandMin or 14
		local stand_max = JazzAI_RecontactStandMax or 20
		local creeper = JazzAI_UnitIsRecontactCreeper and JazzAI_UnitIsRecontactCreeper(unit)
		if creeper then
			if d_tiles < cur then
				score = score + 80
			elseif d_tiles > cur then
				score = score - 40
			end
			if d_tiles >= stand_min and d_tiles <= stand_max then
				score = score + 60
			elseif d_tiles < stand_min then
				score = score - 50
			end
			if JazzAI_DestNearMapEdge(dest_pos) and not JazzAI_LastKnownNearMapEdge(unit) then
				score = score - 60
			end
		end
	end
	return score
end

function JazzAI_EnemyFocusThreatScore(officer, enemy)
	if not IsValid(officer) or not IsValid(enemy) or enemy:IsDead() then
		return 0
	end
	local score = 10
	local wep = enemy.GetActiveWeapons and enemy:GetActiveWeapons()
	if wep then
		if IsKindOf(wep, "SniperRifle") then
			score = score + 80
		elseif IsKindOfClasses(wep, "MachineGun", "HeavyWeapon") then
			score = score + 70
		end
	end
	-- Also check secondary / all equipped firearms for MG/sniper.
	if enemy.GetEquippedWeapons then
		for _, slot in ipairs({ "Handheld A", "Handheld B" }) do
			for _, w in ipairs(enemy:GetEquippedWeapons(slot) or empty_table) do
				if IsKindOf(w, "SniperRifle") then
					score = Max(score, 90)
				elseif IsKindOfClasses(w, "MachineGun", "HeavyWeapon") then
					score = Max(score, 80)
				end
			end
		end
	end
	local scale = const.SlabSizeX
	local closest = DivRound(officer:GetDist(enemy), scale)
	local team = officer.team
	if team and team.units then
		local radius = JazzAI_OfficerAuraRadius(officer)
		for _, ally in ipairs(team.units) do
			if not ally:IsDead() and (ally == officer or JazzAI_IsInOfficerAura(ally, officer, radius)) then
				local d = DivRound(ally:GetDist(enemy), scale)
				if d < closest then
					closest = d
				end
			end
		end
	end
	if closest <= JazzAI_DirectiveCloseThreat then
		score = score + 90 - closest * 5
	end
	local hpp = JazzAI_UnitHpPercent(enemy)
	if hpp <= 55 then
		score = score + (55 - hpp)
	end
	return score
end

-- Threat-priority focus target (sniper / MG / close / finish). Returns unit, score.
function JazzAI_FindFocusFireTarget(unit)
	if not IsValid(unit) then
		return false, 0
	end
	local enemies = GetEnemies and GetEnemies(unit)
	if not enemies then
		return false, 0
	end
	local best, best_score = false, 0
	for _, enemy in ipairs(enemies) do
		if IsValid(enemy) and not enemy:IsDead() then
			local visible = (HasVisibilityTo and HasVisibilityTo(unit.team, enemy))
				or (HasVisibilityTo and HasVisibilityTo(unit, enemy))
			if visible then
				local s = JazzAI_EnemyFocusThreatScore(unit, enemy)
				if s > best_score then
					best, best_score = enemy, s
				end
			end
		end
	end
	if best and best_score >= JazzAI_FocusFireMinThreat then
		return best, best_score
	end
	return false, 0
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
-- Hide() → DoChangeStance → PlayTransitionAnims → Sleep. BeginTurn fires
-- UnitBeginTurn via procall: IsGameTimeThread() is true, but CanYield() is not.
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
	if not unit:CanStealth(stance) then
		return false
	end
	local function apply_hide()
		if not IsValid(unit) or unit:IsDead() then
			return
		end
		if unit:HasStatusEffect("Hidden") then
			return
		end
		local st = unit:GetStanceToStealth()
		if unit:CanStealth(st) then
			unit:Hide()
		end
	end
	-- Always a fresh thread: inline Hide() from Msg/BeginTurn asserts.
	CreateGameTimeThread(apply_hide)
	return true
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

-- Outdoor elevation worth taking: not indoor-dominant, some height variance among units.
function JazzAI_MapHasHeightVariance(unit)
	local indoor = JazzAI_CountIndoorRatio and JazzAI_CountIndoorRatio() or 0
	if indoor >= 40 then
		return false
	end
	local min_z, max_z, n = nil, nil, 0
	for _, u in ipairs(g_Units or empty_table) do
		if IsValid(u) and not u:IsDead() then
			local x, y, z = u:GetGridCoords()
			if z then
				n = n + 1
				min_z = min_z and Min(min_z, z) or z
				max_z = max_z and Max(max_z, z) or z
			end
		end
	end
	if n < 2 or not min_z or not max_z then
		-- Flat / tiny maps: still allow heights if clearly outdoor.
		return indoor <= 15
	end
	return (max_z - min_z) >= 1
end

function JazzAI_AllyNeedsMedicHeal(unit)
	if not IsValid(unit) or unit:IsDead() then
		return false
	end
	if type(rawget(_G, "JazzHasAnyBleed")) == "function" and JazzHasAnyBleed(unit) then
		return true
	end
	if unit:HasStatusEffect("Bleeding") or unit:HasStatusEffect("BleedingMedium")
		or unit:HasStatusEffect("BleedingHeavy") then
		return true
	end
	return unit.HitPoints < MulDivRound(unit.MaxHitPoints or 1, 85, 100)
end

function JazzAI_PickHeightsClingAnchor(unit)
	if not IsValid(unit) or not unit.team then
		return false
	end
	if JazzAI_UnitNeedsHealSlot and JazzAI_UnitNeedsHealSlot(unit) then
		local best, best_d
		local maxd = 45 * (const.SlabSizeX or 1200)
		for _, ally in ipairs(unit.team.units or empty_table) do
			if ally ~= unit and IsValid(ally) and not ally:IsDead()
				and JazzAI_AllyNeedsMedicHeal(ally) then
				local d = unit:GetDist(ally)
				if d <= maxd and (not best or d < best_d) then
					best, best_d = ally, d
				end
			end
		end
		if best then
			return best
		end
		-- Self-heal only: no cling. Other wounded absent → perch/officer below.
		if JazzAI_AllyNeedsMedicHeal(unit) then
			return false
		end
	end
	local entry = (JazzAI_TeamDirectives or empty_table)[JazzAI_TeamSideKey(unit.team)]
	local source = entry and entry.source
	local radius = entry and entry.radius
	local best, best_d
	if IsValid(source) then
		for _, ally in ipairs(unit.team.units or empty_table) do
			if ally ~= unit and IsValid(ally) and not ally:IsDead()
				and JazzAI_IsInOfficerAura(ally, source, radius)
				and JazzAI_UnitIsLinePerchHolder and JazzAI_UnitIsLinePerchHolder(ally) then
				local d = unit:GetDist(ally)
				if not best or d < best_d then
					best, best_d = ally, d
				end
			end
		end
	end
	if best then
		return best
	end
	return (IsValid(source) and source) or false
end

function JazzAI_UnitHasLiveShot(unit)
	if not IsValid(unit) or unit:IsDead() then
		return false
	end
	local weapon = unit.GetActiveWeapons and unit:GetActiveWeapons("Firearm")
	if not weapon then
		weapon = unit.GetActiveWeapons and unit:GetActiveWeapons()
	end
	if not IsKindOf(weapon, "Firearm") then
		return false
	end
	local maxd = weapon.GetMaxRange and weapon:GetMaxRange()
	if not maxd or maxd <= 0 then
		maxd = (weapon.WeaponRange or 30) * const.SlabSizeX
	end
	local attack = unit.GetDefaultAttackAction and unit:GetDefaultAttackAction()
	if attack and attack.GetUIState then
		local st = select(1, attack:GetUIState({ unit }))
		if st and st ~= "enabled" then
			return false
		end
	end
	for _, enemy in ipairs(g_Units or empty_table) do
		if IsValid(enemy) and enemy.team and unit.IsOnEnemySide and unit:IsOnEnemySide(enemy)
			and not enemy:IsDead() then
			local vis = false
			local okv, v = pcall(HasVisibilityTo, unit, enemy)
			if okv and v then
				vis = true
			elseif unit.team then
				local okt, tv = pcall(HasVisibilityTo, unit.team, enemy)
				if okt and tv then
					vis = true
				end
			end
			if vis and unit:GetDist(enemy) <= maxd then
				local okc, any = pcall(CheckLOS, { enemy }, unit, maxd)
				if okc and any then
					return true
				end
			end
		end
	end
	return false
end

function JazzAI_AuraHasLiveSpotterShot(officer)
	if not IsValid(officer) or not officer.team then
		return false
	end
	local radius = JazzAI_OfficerAuraRadius(officer)
	if (radius or 0) <= 0 then
		return false
	end
	local entry = (JazzAI_TeamDirectives or empty_table)[JazzAI_TeamSideKey(officer.team)]
	for _, u in ipairs(officer.team.units or empty_table) do
		if IsValid(u) and not u:IsDead() and JazzAI_IsInOfficerAura(u, officer, radius) then
			local spotter = JazzAI_UnitIsHeightsSpotter and JazzAI_UnitIsHeightsSpotter(u)
			if not spotter and entry and entry.semi_sniper == u then
				spotter = true
			end
			if spotter and JazzAI_UnitHasLiveShot(u) then
				return true
			end
		end
	end
	return false
end

function JazzAI_ShouldOccupyHeights(unit, tiles)
	if not JazzAI_MapHasHeightVariance(unit) then
		return false
	end
	if JazzAI_ShouldOccupyBuildings(unit) and (JazzAI_CountIndoorRatio() or 0) >= 35 then
		return false -- prefer houses when heavily indoor/urban
	end
	tiles = tiles or 99
	return tiles >= JazzAI_DirectiveHeightsMin
end

function JazzAI_TeamDirectiveKey(team)
	if not team then
		return false
	end
	return team.side or team.handle or tostring(team)
end

function JazzAI_GetDirectiveFatigue(team)
	local key = JazzAI_TeamDirectiveKey(team)
	if not key then
		return false, 0
	end
	JazzAI_TeamDirectiveFatigue = JazzAI_TeamDirectiveFatigue or {}
	local fat = JazzAI_TeamDirectiveFatigue[key]
	if not fat then
		return false, 0
	end
	return fat.last or false, fat.turns or 0
end

function JazzAI_NoteDirectiveFatigue(team, directive)
	local key = JazzAI_TeamDirectiveKey(team)
	if not key or not directive then
		return
	end
	JazzAI_TeamDirectiveFatigue = JazzAI_TeamDirectiveFatigue or {}
	local fat = JazzAI_TeamDirectiveFatigue[key]
	local turn = g_Combat and g_Combat.current_turn or 0
	if fat and fat.last == directive then
		-- RefreshAllOfficerAuras runs every UnitBeginTurn — count at most once per combat turn.
		if fat.turn == turn then
			return
		end
		fat.turns = (fat.turns or 1) + 1
		fat.turn = turn
	else
		fat = { last = directive, turns = 1, turn = turn }
	end
	JazzAI_TeamDirectiveFatigue[key] = fat
end

local function JazzAI_FatiguePenalty(directive, last, turns)
	if not last or last ~= directive or (turns or 0) <= 0 then
		return 0
	end
	local per = JazzAI_DirectiveFatiguePerTurn
	if directive == "FallBack" then
		per = MulDivRound(per, 25, 100) -- survival: almost no fatigue
	end
	return turns * per
end

-- Score-based officer directive picker with fatigue on the repeated order.
function JazzAI_PickOfficerDirective(unit, profile)
	profile = profile or JazzAI_ResolveContextProfile()
	local team = unit and unit.team
	local last, turns = JazzAI_GetDirectiveFatigue(team)
	local enemy, dist = GetNearestEnemy(unit)
	local tiles = enemy and dist and DivRound(dist, const.SlabSizeX) or 99
	local focus, threat = JazzAI_FindFocusFireTarget(unit)
	local candidates = {}

	local function add(id, base)
		if not id or not base then
			return
		end
		local score = base - JazzAI_FatiguePenalty(id, last, turns)
		candidates[#candidates + 1] = { id = id, score = score }
	end

	if JazzAI_TeamNeedsFallBack(unit) then
		add("FallBack", 1000)
	end
	if profile.SniperHold or profile.id == "FogDust" then
		if JazzAI_TeamCanMostlyStealth(unit) then
			add("GoHidden", 800)
		else
			add("LowVisHold", 750)
		end
	end
	if focus then
		add("FocusFire", 700 + Min(80, threat or 0))
	end
	if enemy and JazzAI_ShouldTakeCoverFromRange(unit, tiles) then
		if JazzAI_TeamCanMostlyStealth(unit) then
			add("GoHidden", 650)
		else
			add("TakeCover", 600)
		end
	end
	if JazzAI_ShouldOccupyHeights(unit, tiles) then
		add("OccupyHeights", 520)
	end
	if JazzAI_AuraHasLiveSpotterShot(unit) then
		add("Push", JazzAI_DirectivePushLiveShot or 600)
	end
	if enemy and tiles <= JazzAI_DirectivePushMax then
		add("Push", 500)
	end
	if JazzAI_ShouldOccupyBuildings(unit) and (not enemy or tiles < JazzAI_DirectiveEnvelopMin) then
		add("OccupyBuildings", 450)
	end
	if enemy and tiles >= JazzAI_DirectiveEnvelopMin then
		add("Envelop", 400)
	end
	add("HoldLine", 300)

	local best_id, best_score = "HoldLine", -999999
	for _, c in ipairs(candidates) do
		if c.score > best_score or (c.score == best_score and c.id < best_id) then
			best_id, best_score = c.id, c.score
		end
	end
	return best_id
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

function JazzAI_ScaleFocusFireTargetScore(unit, target, score)
	if not score or score <= 0 or not unit or not target then
		return score
	end
	local focus = JazzAI_GetTeamFocusTarget(unit)
	if focus and target == focus then
		return score * (JazzAI_FocusFireScoreMul or 2)
	end
	return score
end

-- Player-facing FocusFire target for aura INFO (commander + influence).
-- Reads the team MapVar even if the wearer slightly left radius but still has the badge.
function JazzAI_GetFocusFireTargetDisplayName(effect)
	local owner = JazzAI_FindStatusEffectOwner(effect)
	if not owner or not owner.team then
		return false
	end
	local team = owner.team
	local entry = (JazzAI_TeamDirectives or empty_table)[team.side or team.handle or tostring(team)]
	if not entry or entry.directive ~= "FocusFire" then
		return false
	end
	local focus = entry.focus_target
	if not IsValid(focus) or (focus.IsDead and focus:IsDead()) then
		return false
	end
	if focus.GetDisplayName then
		return focus:GetDisplayName()
	end
	return focus.Nick or focus.Name or false
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
	elseif directive == "OccupyHeights" then
		return T(890000000006118, --[[JazzAI directive OccupyHeights]] "Занять высоты")
	end
	return false
end

-- Small Influence buffs by current order (player-facing tooltip line).
function JazzAI_GetDirectiveBuffDisplay(directive)
	if directive == "HoldLine" or directive == "Envelop" or directive == "OccupyBuildings"
		or directive == "LowVisHold" or directive == "OccupyHeights" then
		return T(890000000006119, --[[JazzAI directive buff CTH2]] "+2 к шансу попадания")
	elseif directive == "Push" then
		return T(890000000006120, --[[JazzAI directive buff AP1]] "+1 ОД на ход")
	elseif directive == "FocusFire" then
		return T(890000000006121, --[[JazzAI directive buff CTH5]] "+5 к шансу попадания")
	elseif directive == "FallBack" then
		return T(890000000006122, --[[JazzAI directive buff def5]] "−5 к шансу попадания по этому бойцу")
	elseif directive == "TakeCover" then
		return T(890000000006123, --[[JazzAI directive buff def3]] "−3 к шансу попадания по этому бойцу")
	end
	return false
end

function JazzAI_GetDirectiveCthAttackBonus(directive)
	if directive == "FocusFire" then
		return 5
	end
	if directive == "HoldLine" or directive == "Envelop" or directive == "OccupyBuildings"
		or directive == "LowVisHold" or directive == "OccupyHeights" then
		return 2
	end
	return 0
end

function JazzAI_GetDirectiveCthDefenseBonus(directive)
	if directive == "FallBack" then
		return 5
	end
	if directive == "TakeCover" then
		return 3
	end
	return 0
end

function JazzAI_GetDirectiveApBonus(directive)
	if directive == "Push" then
		return 1
	end
	return 0
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
	local markers = {
		"Текущий приказ:", "Следует приказу:", "Current order:", "Following order:",
		"Эффект приказа:", "Order effect:",
		"Цель:", "Target:",
	}
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
	local directive = JazzAI_EnsureEffectDirective(effect)
	local order = JazzAI_GetDirectiveDisplayName(directive)
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
	local parts = { base, line }
	if directive == "FocusFire" then
		local target_name = JazzAI_GetFocusFireTargetDisplayName(effect)
		if target_name then
			parts[#parts + 1] = T{890000000006125, --[[JazzAI officer aura FocusFire target]] "Цель: <em><name></em>", name = target_name}
		end
	end
	if kind == "influence" then
		local buff = JazzAI_GetDirectiveBuffDisplay(directive)
		if buff then
			parts[#parts + 1] = T{890000000006124, --[[JazzAI officer aura order effect]] "Эффект приказа: <em><buff></em>", buff = buff}
		end
	end
	return table.concat(parts, "\n\n")
end

-- JAZZ-AI-CMD-002: cheap team turn sequencer (Early support → Normal line → Late press).
function JazzAI_UnitSlotKey(unit)
	if not unit then
		return false
	end
	return unit.session_id or unit.handle
end

function JazzAI_TeamSideKey(team)
	if not team then
		return false
	end
	return team.side or team.handle or tostring(team)
end

local function JazzAI_LivingTeamUnits(team)
	local list = {}
	for _, u in ipairs((team and team.units) or empty_table) do
		if IsValid(u) and not u:IsDead() then
			list[#list + 1] = u
		end
	end
	table.sort(list, function(a, b)
		return (a.handle or 0) < (b.handle or 0)
	end)
	return list
end

local function JazzAI_UnitHasKeyword(unit, kw)
	return unit and table.find(unit.AIKeywords or empty_table, kw)
end

local function JazzAI_UnitArchetypeId(unit)
	local a = unit and (unit.current_archetype or unit.archetype)
	if type(a) == "table" then
		return a.id or a.Id or ""
	end
	return tostring(a or "")
end

local function JazzAI_UnitHasAoeGrenade(unit, aoe)
	if not unit then
		return false
	end
	local found = false
	unit:ForEachItem(function(item)
		if found then
			return
		end
		if IsKindOfClasses(item, "Grenade", "Ordnance") and (item.aoeType or "none") == aoe then
			found = true
		end
	end)
	return found
end

function JazzAI_UnitHasFlareGear(unit)
	if not unit then
		return false
	end
	if unit:GetItemInSlot("Handheld A", "FlareGun") or unit:GetItemInSlot("Handheld B", "FlareGun") then
		return true
	end
	local found = false
	unit:ForEachItem(function(item)
		if found then
			return
		end
		if IsKindOf(item, "Flare") or IsKindOf(item, "FlareGun") then
			found = true
		end
	end)
	return found
end

function JazzAI_TeamHasUnlitThreat(unit)
	if not unit or not unit.team then
		return false
	end
	local illuminate = rawget(_G, "IsIlluminated")
	for _, other in ipairs(g_Units or empty_table) do
		if IsValid(other) and not other:IsDead() and unit.IsOnEnemySide and unit:IsOnEnemySide(other) then
			if type(illuminate) ~= "function" then
				return true
			end
			local ok, lit = pcall(illuminate, other)
			if not ok or not lit then
				return true
			end
		end
	end
	return false
end

function JazzAI_UnitCanFlareEarly(unit)
	if not (GameState.Night or GameState.Underground) then
		return false
	end
	if not JazzAI_UnitHasFlareGear(unit) then
		return false
	end
	return JazzAI_TeamHasUnlitThreat(unit)
end

local function JazzAI_TeamHasCurtainSignal(team)
	local overwatch = rawget(_G, "g_Overwatch")
	if type(overwatch) == "table" then
		for _ in pairs(overwatch) do
			return true
		end
	end
	local units = rawget(_G, "g_Units") or empty_table
	for _, u in ipairs(units) do
		if IsValid(u) and not u:IsDead() and u.last_attack_pos then
			return true
		end
	end
	return false
end

function JazzAI_PickTeamSmokeThrower(team)
	local units = JazzAI_LivingTeamUnits(team)
	local entry = (JazzAI_TeamDirectives or empty_table)[JazzAI_TeamSideKey(team)]
	local source = entry and entry.source
	local radius = entry and entry.radius
	local pool = units
	if source and radius then
		local in_aura = {}
		for _, u in ipairs(units) do
			if JazzAI_IsInOfficerAura(u, source, radius) then
				in_aura[#in_aura + 1] = u
			end
		end
		if #in_aura > 0 then
			pool = in_aura
		end
	end
	local curtain = JazzAI_TeamHasCurtainSignal(team)
	local best, best_score
	for _, u in ipairs(pool) do
		if JazzAI_UnitHasAoeGrenade(u, "smoke") then
			local score = 10
			if curtain then
				score = score + 50
			end
			if JazzAI_UnitHasKeyword(u, "Smoke") then
				score = score + 20
			end
			if not best or score > best_score or (score == best_score and (u.handle or 0) < (best.handle or 0)) then
				best, best_score = u, score
			end
		end
	end
	return best or false
end

function JazzAI_GetTeamSmokeThrower(team)
	if not team then
		return false
	end
	local entry = (JazzAI_TeamDirectives or empty_table)[JazzAI_TeamSideKey(team)]
	if entry and entry.smoke then
		return entry.smoke
	end
	return false
end

function JazzAI_UnitNeedsHealSlot(unit)
	local id = JazzAI_UnitArchetypeId(unit)
	local is_medic = JazzAI_UnitHasKeyword(unit, "Heal") or string.find(id, "Medic", 1, true)
	if not is_medic then
		return false
	end
	local try_medic = rawget(_G, "JazzAI_TryMedicSwitch")
	if type(try_medic) == "function" then
		return try_medic(unit) and true or false
	end
	if not unit or not unit.team then
		return false
	end
	local function needs(u)
		if not u or u:IsDead() then
			return false
		end
		if type(rawget(_G, "JazzHasAnyBleed")) == "function" and JazzHasAnyBleed(u) then
			return true
		end
		if u:HasStatusEffect("Bleeding") or u:HasStatusEffect("BleedingMedium") or u:HasStatusEffect("BleedingHeavy") then
			return true
		end
		return u.HitPoints < MulDivRound(u.MaxHitPoints or 1, 85, 100)
	end
	if needs(unit) then
		return true
	end
	for _, ally in ipairs(unit.team.units or empty_table) do
		if ally ~= unit and needs(ally) then
			return true
		end
	end
	return false
end

function JazzAI_UnitNeedsMGSetup(unit)
	if not unit then
		return false
	end
	if unit:HasStatusEffect("StationedMachineGun") then
		return false
	end
	if unit.HasPreparedAttack and unit:HasPreparedAttack() then
		return false
	end
	local weapon = unit.GetActiveWeapons and unit:GetActiveWeapons("Firearm")
	if not weapon then
		return false
	end
	return IsKindOf(weapon, "MachineGun") or JazzAI_UnitHasKeyword(unit, "MG")
end

function JazzAI_UnitIsPressRole(unit)
	local id = JazzAI_UnitArchetypeId(unit)
	if string.find(id, "Assaulter", 1, true) or string.find(id, "Flanker", 1, true) then
		return true
	end
	if JazzAI_UnitHasKeyword(unit, "Flank") then
		return true
	end
	local team = unit and unit.team
	local entry = team and (JazzAI_TeamDirectives or empty_table)[JazzAI_TeamSideKey(team)]
	if entry and entry.pusher == unit then
		return true
	end
	return false
end

function JazzAI_UnitIsLineRole(unit)
	local id = JazzAI_UnitArchetypeId(unit)
	if string.find(id, "Frontliner", 1, true) or string.find(id, "Sniper", 1, true)
		or string.find(id, "Machinegunner", 1, true) or string.find(id, "Marksman", 1, true)
	then
		return true
	end
	if JazzAI_UnitHasKeyword(unit, "Sniper") or JazzAI_UnitHasKeyword(unit, "Marksman")
		or JazzAI_UnitHasKeyword(unit, "Control")
	then
		return true
	end
	if unit and unit:HasStatusEffect("StationedMachineGun") then
		return true
	end
	return false
end

function JazzAI_PickUnitActKind(unit, smoke_thrower)
	if JazzAI_UnitNeedsHealSlot(unit) then
		return "heal"
	end
	if JazzAI_UnitCanFlareEarly(unit) then
		return "flare"
	end
	if smoke_thrower and unit == smoke_thrower then
		return "smoke"
	end
	if JazzAI_UnitNeedsMGSetup(unit) then
		return "mg_setup"
	end
	if JazzAI_UnitIsRecontactCreeper and JazzAI_UnitIsRecontactCreeper(unit) then
		return "recontact"
	end
	-- Assigned pusher Late even if the fighter is a Frontliner (Push assign).
	local team = unit and unit.team
	local entry = team and (JazzAI_TeamDirectives or empty_table)[JazzAI_TeamSideKey(team)]
	if entry and entry.pusher == unit then
		return "press"
	end
	if JazzAI_UnitIsLineRole(unit) then
		return "line"
	end
	if JazzAI_UnitIsPressRole(unit) then
		return "press"
	end
	return "line"
end

function JazzAI_ActKindPhase(kind)
	if kind == "heal" or kind == "flare" or kind == "smoke" or kind == "mg_setup" or kind == "recontact" then
		return "Early"
	end
	if kind == "press" then
		return "Late"
	end
	return "Normal"
end

function JazzAI_AssignTeamActSlots(team)
	if not team then
		return
	end
	if type(rawget(_G, "JazzAI_RefreshOfficerAurasForTeam")) == "function" then
		JazzAI_RefreshOfficerAurasForTeam(team)
	end
	local turn = g_Combat and g_Combat.current_turn
	local side = JazzAI_TeamSideKey(team)
	JazzAI_TeamActSlots = JazzAI_TeamActSlots or {}
	if JazzAI_TeamActSlotsTurn ~= turn then
		JazzAI_TeamActSlots = {}
		JazzAI_TeamActSlotsTurn = turn
		JazzAI_TeamExplosiveThrows = {}
		JazzAI_TeamExplosiveThrowTurn = turn
	end
	local smoke = JazzAI_PickTeamSmokeThrower(team)
	JazzAI_TeamDirectives = JazzAI_TeamDirectives or {}
	local entry = JazzAI_TeamDirectives[side] or {}
	entry.smoke = smoke or false
	JazzAI_TeamDirectives[side] = entry
	JazzAI_AssignRecontactProbes(team)
	for _, u in ipairs(JazzAI_LivingTeamUnits(team)) do
		if type(JazzAI_UsesJazzCombatAI) ~= "function" or JazzAI_UsesJazzCombatAI(u) then
			local kind = JazzAI_PickUnitActKind(u, smoke)
			local key = JazzAI_UnitSlotKey(u)
			if key then
				JazzAI_TeamActSlots[key] = {
					phase = JazzAI_ActKindPhase(kind),
					kind = kind,
					source = "CMD-002",
				}
			end
		end
	end
end

function JazzAI_GetUnitActSlot(unit)
	local key = JazzAI_UnitSlotKey(unit)
	if not key then
		return false
	end
	JazzAI_TeamActSlots = JazzAI_TeamActSlots or {}
	return JazzAI_TeamActSlots[key] or false
end

function JazzAI_ExplosiveThrowBudget()
	local game = rawget(_G, "Game")
	local diff = game and game.game_difficulty or "Normal"
	if diff == "VeryHard" then
		return false
	end
	if diff == "Hard" then
		return 3
	end
	return 1
end

function JazzAI_TeamExplosiveThrowCount(unit)
	if not unit or not unit.team then
		return 0
	end
	local turn = g_Combat and g_Combat.current_turn
	if JazzAI_TeamExplosiveThrowTurn ~= turn then
		JazzAI_TeamExplosiveThrows = {}
		JazzAI_TeamExplosiveThrowTurn = turn
	end
	JazzAI_TeamExplosiveThrows = JazzAI_TeamExplosiveThrows or {}
	return JazzAI_TeamExplosiveThrows[JazzAI_TeamSideKey(unit.team)] or 0
end

function JazzAI_ScaleExplosiveGrenadeScore(unit, score)
	local budget = JazzAI_ExplosiveThrowBudget()
	if budget == false then
		return score
	end
	if (JazzAI_TeamExplosiveThrowCount(unit) or 0) >= budget then
		return MulDivRound(score or 0, 25, 100)
	end
	return score
end

function JazzAI_NoteTeamExplosiveThrow(unit, grenade)
	if not unit or not unit.team or not grenade then
		return
	end
	if JazzAI_ExplosiveThrowBudget() == false then
		return
	end
	if IsKindOf(grenade, "Flare") or (grenade.aoeType or "none") == "smoke" then
		return
	end
	local turn = g_Combat and g_Combat.current_turn
	if JazzAI_TeamExplosiveThrowTurn ~= turn then
		JazzAI_TeamExplosiveThrows = {}
		JazzAI_TeamExplosiveThrowTurn = turn
	end
	JazzAI_TeamExplosiveThrows = JazzAI_TeamExplosiveThrows or {}
	local key = JazzAI_TeamSideKey(unit.team)
	JazzAI_TeamExplosiveThrows[key] = (JazzAI_TeamExplosiveThrows[key] or 0) + 1
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
	JazzAI_NoteDirectiveFatigue(team, directive)
	JazzAI_TeamDirectives = JazzAI_TeamDirectives or {}
	local key = team.side or team.handle or tostring(team)
	local entry = JazzAI_TeamDirectives[key] or {}
	local prev_directive = entry.directive
	entry.directive = directive
	entry.source = unit
	entry.radius = radius
	entry.pos = unit:GetPos()
	if directive == "FocusFire" then
		entry.focus_target = JazzAI_FindFocusFireTarget(unit) or false
	else
		entry.focus_target = false
	end
	-- Commander assigns fill-in roles inside the aura (not whole map outside radius).
	-- Priority: semi_sniper > pseudo_mg > pusher (one role per fighter).
	-- Picker impl lives in jazz-units; names are registered above via rawget.
	local exclude = {}
	local pick_sniper = rawget(_G, "JazzAI_PickTeamSemiSniper")
	if type(pick_sniper) == "function" then
		entry.semi_sniper = pick_sniper(team, unit, radius) or false
	else
		entry.semi_sniper = false
	end
	if entry.semi_sniper then
		exclude[entry.semi_sniper] = true
	end
	local pick_mg = rawget(_G, "JazzAI_PickTeamPseudoMG")
	if type(pick_mg) == "function" then
		entry.pseudo_mg = pick_mg(team, unit, radius) or false
		if entry.pseudo_mg and exclude[entry.pseudo_mg] then
			entry.pseudo_mg = false
		end
	else
		entry.pseudo_mg = false
	end
	if entry.pseudo_mg then
		exclude[entry.pseudo_mg] = true
	end
	local pick_pusher = rawget(_G, "JazzAI_PickTeamPusher")
	if type(pick_pusher) == "function" then
		entry.pusher = pick_pusher(team, unit, radius, exclude) or false
	else
		entry.pusher = false
	end
	JazzAI_TeamDirectives[key] = entry
	local bark = rawget(_G, "JazzAI_BarkOnDirective")
	if type(bark) == "function" then
		bark(unit, prev_directive, directive, entry)
	end

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
		JazzAI_AssignRecontactProbes(team)
	else
		for _, u in ipairs(team.units) do
			JazzAI_SetAuraEffect(u, "Jazz_Perk_OfficerAura", false)
			JazzAI_SetAuraEffect(u, "Jazz_Perk_OfficerAuraInfluence", false)
		end
		JazzAI_AssignRecontactProbes(team)
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
	JazzAI_TeamDirectiveFatigue = {}
	JazzAI_PeekStreak = {}
	JazzAI_SniperUselessStreak = {}
	JazzAI_FlarePushUntil = false
	JazzAI_TeamActed = {}
	JazzAI_TeamActedTurn = false
	JazzAI_TeamActSlots = {}
	JazzAI_TeamActSlotsTurn = false
	JazzAI_TeamExplosiveThrows = {}
	JazzAI_TeamExplosiveThrowTurn = false
	JazzAI_TeamFallBackState = {}
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
	JazzAI_TeamDirectiveFatigue = {}
	JazzAI_TeamActSlots = {}
	JazzAI_TeamActSlotsTurn = false
	JazzAI_TeamExplosiveThrows = {}
	JazzAI_TeamExplosiveThrowTurn = false
	JazzAI_TeamFallBackState = {}
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
