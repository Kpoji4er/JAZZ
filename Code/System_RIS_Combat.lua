-- R.I.S. Phase B: kill tracking + after-action reports (JAZZ-UI-RIS-001).

MapVar("g_JAZZ_RIS_CombatSnap", false)

g_JAZZ_RIS_CombatInstalled = rawget(_G, "g_JAZZ_RIS_CombatInstalled") or false

local function lState()
	local st = rawget(_G, "gv_JAZZ_RIS")
	if not st then
		return false
	end
	if type(st.kills) ~= "table" then
		st.kills = {}
	end
	if type(st.battles) ~= "table" then
		st.battles = {}
	end
	if type(st.dossiers) ~= "table" then
		st.dossiers = {}
	end
	if type(st.quest_met) ~= "table" then
		st.quest_met = {}
	end
	return st
end

local function lThreshold()
	return rawget(_G, "JAZZ_RIS_KILL_THRESHOLD") or 3
end

local function lCap()
	return rawget(_G, "JAZZ_RIS_BATTLE_CAP") or 20
end

local function lIsPlayerSide(unit)
	return unit and unit.team and (unit.team.player_team or unit.team.side == "player1" or unit.team.side == "player2")
end

local function lIsEnemySide(unit)
	return unit and unit.team and not lIsPlayerSide(unit) and unit.team.side ~= "neutral"
end

local function lUnitTypeId(unit)
	if not unit then
		return false
	end
	local id = unit.unitdatadef_id or unit.class
	if type(id) == "string" and string.match(id, "^JAZZ_Legion_") then
		return id
	end
	return false
end

local function lDisplayName(unit)
	if not unit then
		return false
	end
	local nick = unit.Nick
	local name = unit.Name
	local pick = nick or name
	if not pick or pick == "" then
		return false
	end
	-- Reject empty / missing localization placeholders.
	if type(pick) == "table" and not pick[1] then
		return false
	end
	return pick
end

local function lHashPick(list, key)
	if type(list) ~= "table" or #list == 0 then
		return false
	end
	local h = 0
	key = tostring(key or "")
	for i = 1, #key do
		h = (h * 131 + string.byte(key, i)) % 2147483647
	end
	return list[(h % #list) + 1]
end

local function lWeatherBand()
	if GameState then
		if GameState.Night or GameState.Underground then
			return "night"
		end
		if GameState.Fog then
			return "fog"
		end
		if GameState.DustStorm then
			return "dust"
		end
		if GameState.Heat then
			return "heat"
		end
		if GameState.RainHeavy or GameState.RainLight then
			return "rain"
		end
	end
	local wid = gv_CurrentSectorId and type(GetCurrentSectorWeather) == "function" and GetCurrentSectorWeather(gv_CurrentSectorId)
	if wid == "RainLight" or wid == "RainHeavy" then
		return "rain"
	end
	if wid == "Fog" then
		return "fog"
	end
	if wid == "DustStorm" then
		return "dust"
	end
	if wid == "Heat" or wid == "FireStorm" then
		return "heat"
	end
	if wid == "ClearSky" or wid == "Clear" then
		return "clear"
	end
	return "default"
end

local function lIntensityBand(snap, playerWon, isRetreat)
	local heat = tonumber(snap and snap.heat_delta) or 0
	local pkia = tonumber(snap and snap.player_kia) or 0
	local ekia = tonumber(snap and snap.enemy_kia) or 0
	local start_e = Max(1, tonumber(snap and snap.enemy_start) or 1)
	local rate = MulDivRound(ekia + pkia, 100, start_e + Max(1, tonumber(snap and snap.player_start) or 1))
	if heat >= 40 or rate >= 55 or (not playerWon and not isRetreat and rate >= 35) then
		return "high"
	end
	if heat >= 15 or rate >= 25 then
		return "mid"
	end
	return "low"
end

local function lEnsureSnap()
	local snap = g_JAZZ_RIS_CombatSnap
	if type(snap) == "table" then
		return snap
	end
	local sector = gv_Sectors and gv_Sectors[gv_CurrentSectorId]
	local heat0 = sector and (tonumber(sector.CombatHeat) or 0) or 0
	local p, e = 0, 0
	if type(GetAllUnits) == "function" then
		for _, u in ipairs(GetAllUnits() or empty_table) do
			if IsValid(u) and not u:IsDead() then
				if lIsPlayerSide(u) then
					p = p + 1
				elseif lIsEnemySide(u) then
					e = e + 1
				end
			end
		end
	elseif g_Units then
		for _, u in pairs(g_Units) do
			if IsValid(u) and not u:IsDead() then
				if lIsPlayerSide(u) then
					p = p + 1
				elseif lIsEnemySide(u) then
					e = e + 1
				end
			end
		end
	end
	snap = {
		sector_id = gv_CurrentSectorId,
		heat_start = heat0,
		player_start = p,
		enemy_start = e,
		player_kia = 0,
		enemy_kia = 0,
		player_wia = 0,
		enemy_wia = 0,
		elites = {},
		ambush = false,
		started = true,
		sector_ctx = JAZZ_RIS_ResolveSectorContext(gv_CurrentSectorId),
	}
	g_JAZZ_RIS_CombatSnap = snap
	return snap
end

local function lTrackElite(unit, fate)
	if not unit or not unit.elite then
		return
	end
	local name = lDisplayName(unit)
	if not name then
		return
	end
	local snap = lEnsureSnap()
	local handle = unit.handle or unit.session_id or tostring(name)
	for _, row in ipairs(snap.elites) do
		if row.handle == handle then
			row.fate = fate
			return
		end
	end
	snap.elites[#snap.elites + 1] = {
		handle = handle,
		name = name,
		fate = fate,
	}
end

function JAZZ_RIS_OnKill(unit, attacker)
	local id = lUnitTypeId(unit)
	if not id then
		return
	end
	if not lIsPlayerSide(attacker) then
		-- Count Legion deaths in player conflicts even without a clear attacker attribution.
		if not (g_Combat or g_Teams) then
			return
		end
	end
	local st = lState()
	if not st then
		return
	end
	st.kills[id] = (tonumber(st.kills[id]) or 0) + 1
	if st.kills[id] >= lThreshold() then
		st.dossiers[id] = true
	end
	if rawget(_G, "JAZZ_RIS_EnqueueUnitSighting") then
		JAZZ_RIS_EnqueueUnitSighting(id)
	end
	JAZZ_RIS_NoteQuestMeet("Legion")
	ObjModified("jazz_ris")
end

local function lNoteEnemyPresence(unit)
	if not lIsEnemySide(unit) then
		return
	end
	local id = lUnitTypeId(unit)
	if id and rawget(_G, "JAZZ_RIS_EnqueueUnitSighting") then
		JAZZ_RIS_EnqueueUnitSighting(id)
	end
end

local function lNoteDeathMails(unit)
	if not lIsEnemySide(unit) then
		return
	end
	local name = lDisplayName(unit)
	if unit.elite and name and rawget(_G, "JAZZ_RIS_EnqueueEliteObit") then
		JAZZ_RIS_EnqueueEliteObit(name)
	end
	local sid = unit.session_id or unit.unitdatadef_id
	if sid and rawget(_G, "JAZZ_RIS_EnqueueNpcObit") then
		JAZZ_RIS_EnqueueNpcObit(sid, name or sid)
	end
end

function JAZZ_RIS_NoteQuestMeet(id)
	if type(id) ~= "string" then
		return
	end
	local st = lState()
	if not st then
		return
	end
	local bank = rawget(_G, "JAZZ_RIS_QUEST_DOSSIERS")
	if not bank or not bank[id] then
		return
	end
	st.quest_met[id] = true
	ObjModified("jazz_ris")
end

local function lTr(t)
	if not t then
		return ""
	end
	if type(_InternalTranslate) == "function" then
		local ok, s = pcall(_InternalTranslate, t)
		if ok and s then
			return s
		end
	end
	return tostring(t)
end

--- Resolve human sector name + quest threads pinned to this grid (badges) / active quest fallback.
function JAZZ_RIS_ResolveSectorContext(sector_id)
	local sector = gv_Sectors and sector_id and gv_Sectors[sector_id]
	local sector_name = ""
	if sector and type(GetSectorName) == "function" then
		sector_name = lTr(GetSectorName(sector))
	elseif sector_id then
		sector_name = tostring(sector_id)
	end
	local poi = false
	if sector then
		poi = sector.Label or sector.intel_shortcut or sector.City
		if type(poi) == "table" then
			poi = lTr(poi)
		elseif poi then
			poi = tostring(poi)
		end
		if poi == "" or poi == "none" or poi == "None" then
			poi = false
		end
	end
	local quests = {}
	if sector_id and type(GetQuestsAssociatedWithSector) == "function" then
		for _, q in ipairs(GetQuestsAssociatedWithSector(sector_id) or empty_table) do
			local preset = q.preset
			if preset then
				local qname = preset.DisplayName or preset.display_name or preset.id
				local note = false
				if q.notes and q.notes[1] and q.notes[1].Text then
					note = lTr(q.notes[1].Text)
				end
				quests[#quests + 1] = {
					id = preset.id,
					name = lTr(qname),
					note = note,
					source = "badge",
				}
			end
		end
	end
	local quest_link = #quests > 0
	if not quest_link and type(GetActiveQuest) == "function" then
		local aq = GetActiveQuest()
		local st = aq and gv_Quests and gv_Quests[aq]
		local preset = aq and Quests and Quests[aq]
		if st and not st.Completed and not st.Failed and preset then
			quests[#quests + 1] = {
				id = aq,
				name = lTr(preset.DisplayName or preset.display_name or aq),
				note = false,
				source = "active",
			}
		end
	end
	return {
		sector_id = sector_id,
		sector_name = sector_name,
		poi = poi,
		quests = quests,
		quest_linked = quest_link, -- true only when sector badges pin a quest
	}
end

local function lBuildAARText(snap, playerWon, isRetreat, autoResolve)
	local aar = rawget(_G, "JAZZ_RIS_AAR")
	if not aar then
		return false, false
	end
	local ctx = snap.sector_ctx or JAZZ_RIS_ResolveSectorContext(snap.sector_id)
	snap.sector_ctx = ctx
	local outcome = "loss"
	if isRetreat then
		outcome = "retreat"
	elseif playerWon then
		outcome = "win"
	end
	local inten = lIntensityBand(snap, playerWon, isRetreat)
	local key = string.format("%s|%s", outcome, inten)
	local bank = aar.headlines[key] or aar.headlines["win|mid"]
	local seed = table.concat({
		tostring(Game and Game.id or ""),
		tostring(snap.sector_id or ""),
		tostring(Game and Game.CampaignTime or 0),
		tostring(#(snap.elites or "")),
		key,
	}, "|")
	local headline = lHashPick(bank, seed) or bank[1]
	local weather = (aar.weather and aar.weather[lWeatherBand()]) or aar.weather.default
	local intensity = aar.intensity[inten] or aar.intensity.mid
	local forces = T{
		aar.forces,
		player = tostring(snap.player_start or 0),
		enemy = tostring(snap.enemy_start or 0),
	}
	local parts = {
		lTr(headline),
		"",
	}
	-- Sector line (always when we have an id/name)
	if ctx and (ctx.sector_name or ctx.sector_id) and aar.sector then
		local secName = ctx.sector_name ~= "" and ctx.sector_name or tostring(ctx.sector_id or "?")
		if ctx.poi and aar.sector.poi then
			parts[#parts + 1] = lTr(T{ aar.sector.poi, sector = secName, poi = ctx.poi })
		else
			parts[#parts + 1] = lTr(T{ aar.sector.line, sector = secName })
		end
		parts[#parts + 1] = ""
	end
	-- Quest thread(s)
	if aar.quest and ctx then
		local qs = ctx.quests or empty_table
		if #qs == 0 then
			parts[#parts + 1] = lTr(aar.quest.none)
		elseif #qs == 1 then
			local q = qs[1]
			if q.source == "active" and not ctx.quest_linked then
				parts[#parts + 1] = lTr(T{ aar.quest.active, quest = q.name })
			elseif q.note and q.note ~= "" then
				parts[#parts + 1] = lTr(T{ aar.quest.one, quest = q.name, note = q.note })
			else
				parts[#parts + 1] = lTr(T{ aar.quest.one_nonote, quest = q.name })
			end
		else
			local names = {}
			for _, q in ipairs(qs) do
				names[#names + 1] = q.name
			end
			parts[#parts + 1] = lTr(T{ aar.quest.many, quests = table.concat(names, "; ") })
		end
		parts[#parts + 1] = ""
	end
	parts[#parts + 1] = lTr(weather)
	parts[#parts + 1] = lTr(intensity)
	parts[#parts + 1] = lTr(forces)
	local charKey = outcome
	if snap.ambush then
		charKey = "ambush"
	elseif ctx and ctx.quest_linked then
		charKey = "quest_" .. outcome
		if not aar.character[charKey] then
			charKey = outcome
		end
	end
	local character = aar.character[charKey] or aar.character.win
	parts[#parts + 1] = lTr(character)
	parts[#parts + 1] = lTr(T{
		aar.losses,
		pkia = tostring(snap.player_kia or 0),
		pwia = tostring(snap.player_wia or 0),
		ekia = tostring(snap.enemy_kia or 0),
		ewia = tostring(snap.enemy_wia or 0),
	})
	if autoResolve then
		parts[#parts + 1] = ""
		parts[#parts + 1] = "(Satellite resolve — limited field detail.)"
	end
	table.sort(snap.elites or {}, function(a, b)
		return tostring(a.name) < tostring(b.name)
	end)
	for _, row in ipairs(snap.elites or empty_table) do
		local fate = row.fate or "threat"
		local tpl = aar.elite[fate] or aar.elite.threat
		parts[#parts + 1] = ""
		parts[#parts + 1] = lTr(T{ tpl, name = row.name })
	end
	local closeKey = "noise"
	if inten == "low" and playerWon then
		closeKey = "quiet"
	elseif inten == "high" and (not playerWon or isRetreat) then
		closeKey = "disaster"
	end
	parts[#parts + 1] = ""
	parts[#parts + 1] = lTr(aar.closing[closeKey] or aar.closing.noise)
	local title = lTr(headline)
	if ctx and ctx.sector_name and ctx.sector_name ~= "" then
		title = string.format("%s — %s", title, ctx.sector_name)
	end
	local body = table.concat(parts, "\n")
	return title, body
end

function JAZZ_RIS_FinalizeBattle(sector, playerWon, isRetreat, autoResolve)
	local st = lState()
	if not st then
		return
	end
	local snap = g_JAZZ_RIS_CombatSnap
	if type(snap) ~= "table" then
		-- Auto-resolve / no tactical snap: minimal stub.
		snap = {
			sector_id = sector and sector.Id or gv_CurrentSectorId,
			heat_start = 0,
			heat_delta = sector and (tonumber(sector.CombatHeat) or 0) or 0,
			player_start = 0,
			enemy_start = 0,
			player_kia = 0,
			enemy_kia = 0,
			player_wia = 0,
			enemy_wia = 0,
			elites = {},
			ambush = false,
		}
	else
		local sectorObj = sector or (gv_Sectors and gv_Sectors[snap.sector_id])
		local heat_now = sectorObj and (tonumber(sectorObj.CombatHeat) or 0) or 0
		snap.heat_delta = Max(0, heat_now - (tonumber(snap.heat_start) or 0))
	end
	snap.sector_id = snap.sector_id or (sector and sector.Id) or gv_CurrentSectorId
	snap.sector_ctx = JAZZ_RIS_ResolveSectorContext(snap.sector_id)
	-- Mark surviving named elites as threat/escaped.
	if g_Units then
		for _, u in pairs(g_Units) do
			if IsValid(u) and u.elite and lIsEnemySide(u) and lDisplayName(u) then
				if u:IsDead() then
					lTrackElite(u, "killed")
				elseif (u.IsDowned and u:IsDowned()) or (u.HasStatusEffect and u:HasStatusEffect("BleedingOut")) then
					lTrackElite(u, "wounded")
				elseif isRetreat or not playerWon then
					lTrackElite(u, "escaped")
				else
					lTrackElite(u, "threat")
				end
			end
		end
	end
	local title, body = lBuildAARText(snap, playerWon, isRetreat, autoResolve)
	if not title then
		g_JAZZ_RIS_CombatSnap = false
		return
	end
	local entry = {
		time = Game and Game.CampaignTime or 0,
		sector = snap.sector_id or (sector and sector.Id),
		sector_name = snap.sector_ctx and snap.sector_ctx.sector_name or false,
		quest_ids = false,
		quest_linked = snap.sector_ctx and snap.sector_ctx.quest_linked or false,
		title = title,
		body = body,
		outcome = isRetreat and "retreat" or (playerWon and "win" or "loss"),
	}
	if snap.sector_ctx and snap.sector_ctx.quests then
		local ids = {}
		for _, q in ipairs(snap.sector_ctx.quests) do
			ids[#ids + 1] = q.id
		end
		entry.quest_ids = ids
	end
	table.insert(st.battles, 1, entry)
	while #st.battles > lCap() do
		table.remove(st.battles)
	end
	g_JAZZ_RIS_CombatSnap = false
	ObjModified("jazz_ris")
end

function OnMsg.CombatStart()
	g_JAZZ_RIS_CombatSnap = false
	lEnsureSnap()
	if g_Units then
		for _, u in pairs(g_Units) do
			if IsValid(u) and not u:IsDead() then
				lNoteEnemyPresence(u)
			end
		end
	end
end

function OnMsg.UnitDied(unit, attacker, results)
	if not unit then
		return
	end
	if lIsEnemySide(unit) then
		local snap = lEnsureSnap()
		snap.enemy_kia = (snap.enemy_kia or 0) + 1
		if unit.elite then
			lTrackElite(unit, "killed")
		end
		lNoteDeathMails(unit)
		JAZZ_RIS_OnKill(unit, attacker)
	elseif lIsPlayerSide(unit) then
		local snap = g_JAZZ_RIS_CombatSnap
		if type(snap) == "table" then
			snap.player_kia = (snap.player_kia or 0) + 1
		end
	end
end

function OnMsg.ConflictEnd(sector, _, playerAttacked, playerWon, autoResolve, isRetreat, startedFromMap)
	if not sector then
		return
	end
	-- Only file when the player was involved.
	if playerAttacked == false and not playerWon and not isRetreat then
		-- still allow if tactical combat existed on this sector
		if not g_JAZZ_RIS_CombatSnap then
			return
		end
	end
	JAZZ_RIS_FinalizeBattle(sector, playerWon and true or false, isRetreat and true or false, autoResolve and true or false)
end

-- Quest / person-of-interest unlocks when met.
function OnMsg.UnitDataCreated(unit)
	if unit and unit.session_id then
		local id = unit.session_id
		if rawget(_G, "JAZZ_RIS_QUEST_DOSSIERS") and JAZZ_RIS_QUEST_DOSSIERS[id] then
			-- wait until IsMet
		end
	end
end

function OnMsg.CombatEnd()
	-- Living wounded pass
	if not g_Units then
		return
	end
	for _, u in pairs(g_Units) do
		if IsValid(u) and u.elite and lIsEnemySide(u) and not u:IsDead() then
			local lowHp = u.HitPoints and u.HitPoints < MulDivRound(u.MaxHitPoints or 100, 35, 100)
			if (u.IsDowned and u:IsDowned()) or lowHp then
				lTrackElite(u, "wounded")
			end
		end
	end
end

-- Poll met flags for quest cards on satellite open / load.
local function lRefreshQuestMeets()
	local bank = rawget(_G, "JAZZ_RIS_QUEST_DOSSIERS")
	if not bank then
		return
	end
	for id in pairs(bank) do
		if id ~= "Legion" then
			local isMetFn = rawget(_G, "IsMet")
			local met = false
			if type(isMetFn) == "function" then
				met = isMetFn(id) and true or false
			elseif gv_UnitData and gv_UnitData[id] and gv_UnitData[id].IsMet then
				met = true
			end
			if met then
				JAZZ_RIS_NoteQuestMeet(id)
			end
		end
	end
end

function OnMsg.OpenSatelliteView()
	lRefreshQuestMeets()
end

function OnMsg.LoadGame()
	DelayedCall(0, lRefreshQuestMeets)
end

function OnMsg.NewGame()
	DelayedCall(0, lRefreshQuestMeets)
end
