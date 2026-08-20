-- R.I.S. cumulative tactical snapshot + language-neutral after-action records.

MapVar("g_JAZZ_RIS_CombatSnap", false)
MapVar("g_JAZZ_RIS_CombatSnaps", {})

g_JAZZ_RIS_CombatInstalled = rawget(_G, "g_JAZZ_RIS_CombatInstalled") or false
g_JAZZ_RIS_UnitMarkerSpawnOrig = rawget(_G, "g_JAZZ_RIS_UnitMarkerSpawnOrig") or false
g_JAZZ_RIS_UnitMarkerSpawnBase = rawget(_G, "g_JAZZ_RIS_UnitMarkerSpawnBase") or false
g_JAZZ_RIS_UnitMarkerSpawnWrap = rawget(_G, "g_JAZZ_RIS_UnitMarkerSpawnWrap") or false
g_JAZZ_RIS_UnitMarkerSpawnWrapped = rawget(_G, "g_JAZZ_RIS_UnitMarkerSpawnWrapped") or false

local RIS_SNAP_SCHEMA = 3
local RIS_AAR_RECORD_VERSION = 2

local function lState()
	local migrate = rawget(_G, "JAZZ_RIS_MigrateState")
	if type(migrate) == "function" then
		return migrate()
	end
	local st = rawget(_G, "gv_JAZZ_RIS")
	if type(st) ~= "table" then
		return false
	end
	st.kills = type(st.kills) == "table" and st.kills or {}
	st.battles = type(st.battles) == "table" and st.battles or {}
	st.dossiers = type(st.dossiers) == "table" and st.dossiers or {}
	st.quest_met = type(st.quest_met) == "table" and st.quest_met or {}
	return st
end

local function lThreshold()
	return tonumber(rawget(_G, "JAZZ_RIS_KILL_THRESHOLD")) or 3
end

local function lCap()
	return tonumber(rawget(_G, "JAZZ_RIS_BATTLE_CAP")) or 20
end

local function lNow()
	local game = rawget(_G, "Game")
	return game and game.CampaignTime or 0
end

local function lCurrentSectorId()
	return rawget(_G, "gv_CurrentSectorId")
end

local function lSectorId(sector)
	if type(sector) == "table" then
		return sector.Id or sector.id
	end
	if type(sector) == "string" then
		return sector
	end
	return lCurrentSectorId()
end

local function lSectorObject(sector_id, supplied)
	if type(supplied) == "table" then
		return supplied
	end
	local sectors = rawget(_G, "gv_Sectors")
	return type(sectors) == "table" and sector_id and sectors[sector_id] or false
end

local function lIsValidUnit(unit)
	if type(unit) ~= "table" and type(unit) ~= "userdata" then
		return false
	end
	local isValid = rawget(_G, "IsValid")
	if type(isValid) ~= "function" then
		return true
	end
	local ok, valid = pcall(isValid, unit)
	if ok and valid then
		return true
	end
	-- Satellite UnitData is a Lua object rather than a placed map object.
	return type(unit) == "table"
		and type(unit.session_id) == "string"
		and unit.Squad ~= nil
end

local function lIsDead(unit)
	return type(unit.IsDead) == "function" and unit:IsDead() or (tonumber(unit.HitPoints) or 0) <= 0
end

local function lIsConflictParticipant(unit)
	if not lIsValidUnit(unit) or unit.conflict_ignore then
		return false
	end
	local isDefeated = unit.IsDefeatedVillain
	if type(isDefeated) == "function" then
		local ok, defeated = pcall(isDefeated, unit)
		if ok and defeated then
			return false
		end
	end
	return true
end

--- Returns "player", "enemy", or false. Team diplomacy flags take precedence.
local function lSideKind(unit)
	local team = unit and unit.team
	local dead = unit and lIsDead(unit)
	if type(team) == "table" then
		if team.player_team == true or team.player_ally == true then
			return "player"
		end
		if team.player_enemy == true then
			return "enemy"
		end
		-- Living neutrals stay out. Corpses are often moved to enemyNeutral
		-- before UnitDied, so that flag must not hide a map-placed kill.
		if not dead
			and (team.neutral == true or team.side == "neutral" or team.side == "enemyNeutral")
		then
			return false
		end
		-- Conservative fallback for lifecycle windows before diplomacy flags are refreshed.
		if team.side == "player1" or team.side == "player2" or team.side == "ally" then
			return "player"
		end
		if team.side == "enemy1" or team.side == "enemy2" then
			return "enemy"
		end
	end
	-- Auto-resolve works on UnitData, which has no tactical team object.
	local squads = rawget(_G, "gv_Squads")
	local squad = type(squads) == "table" and unit and unit.Squad and squads[unit.Squad]
	local side = (type(squad) == "table" and squad.Side) or (unit and unit.Side)
	if side == "player1" or side == "player2" or side == "ally" then
		return "player"
	end
	if side == "enemy1" or side == "enemy2" then
		return "enemy"
	end
	if dead then
		local id = unit.unitdatadef_id or unit.class
		if type(id) == "string" and string.match(id, "^JAZZ_Legion_") then
			return "enemy"
		end
		local aff = unit.Affiliation
		if aff == "Legion" or aff == "Army" or aff == "Adonis" then
			return "enemy"
		end
	end
	return false
end

local function lUnitHandle(unit)
	if not unit then
		return false
	end
	if type(unit.session_id) == "string" and unit.session_id ~= "" then
		return "session:" .. unit.session_id
	end
	local handle = unit.handle
	if not handle and type(unit.GetHandle) == "function" then
		handle = unit:GetHandle()
	end
	if handle and handle ~= 0 then
		return handle
	end
	return false
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

local function lIsStableT(value)
	local isT = rawget(_G, "IsT")
	if type(isT) == "function" then
		local ok, translated = pcall(isT, value)
		if not ok or not translated then
			return false
		end
	end
	local getId = rawget(_G, "TGetID")
	if type(getId) == "function" then
		local ok, id = pcall(getId, value)
		return ok and type(id) == "number" and id ~= 0
	end
	return type(value) == "table" and type(value[1]) == "number"
end

local function lDisplayNameRef(unit)
	if not unit then
		return false
	end
	local pick = unit.Nick
	if not pick or pick == "" then
		pick = unit.Name
	end
	if lIsStableT(pick) then
		return pick
	end
	if type(pick) ~= "string" or pick == "" then
		return false
	end
	if pick == unit.session_id or pick == unit.unitdatadef_id or pick == unit.class then
		return false
	end
	return pick
end

local function lIsNamedOpponent(unit)
	if not unit then
		return false
	end
	if unit.elite or unit.villain then
		return true
	end
	local id = unit.session_id or unit.unitdatadef_id
	if type(id) ~= "string" then
		return false
	end
	local keys = rawget(_G, "JAZZ_RIS_KEY_NPCS")
	local dossiers = rawget(_G, "JAZZ_RIS_QUEST_DOSSIERS")
	return (type(keys) == "table" and keys[id])
		or (type(dossiers) == "table" and dossiers[id])
		or false
end

local function lAllUnits()
	local getAllUnits = rawget(_G, "GetAllUnits")
	if type(getAllUnits) == "function" then
		local ok, units = pcall(getAllUnits)
		if ok and type(units) == "table" then
			return units
		end
	end
	local units = rawget(_G, "g_Units")
	if type(units) == "table" then
		return units
	end
	return rawget(_G, "empty_table") or {}
end

local function lHeatForSector(sector_id, supplied)
	local sector = lSectorObject(sector_id, supplied)
	return sector and (tonumber(sector.CombatHeat) or 0) or 0
end

local function lNewSnap(sector_id, sector)
	local resolveContext = rawget(_G, "JAZZ_RIS_ResolveSectorContext")
	local sectorContext = type(resolveContext) == "function"
		and resolveContext(sector_id)
		or false
	return {
		schema_version = RIS_SNAP_SCHEMA,
		sector_id = sector_id,
		started_at = lNow(),
		heat_start = lHeatForSector(sector_id, sector),
		heat_delta = 0,
		player_start = 0,
		enemy_start = 0,
		player_kia = 0,
		enemy_kia = 0,
		player_wia = 0,
		enemy_wia = 0,
		seen_units = {},
		unit_sides = {},
		baseline_hp = {},
		counted_deaths = {},
		player_wounded = {},
		enemy_wounded = {},
		elites = {},
		sector_ctx = sectorContext,
		ambush = false,
		finalized = false,
	}
end

local function lTrackNamed(snap, unit, fate)
	if type(snap) ~= "table" or not lIsNamedOpponent(unit) then
		return
	end
	local handle = lUnitHandle(unit)
	local nameRef = lDisplayNameRef(unit)
	if not handle then
		return
	end
	local sessionId = type(unit.session_id) == "string" and unit.session_id or false
	for _, row in ipairs(snap.elites) do
		if row.handle == handle or (sessionId and row.session_id == sessionId) then
			row.handle = handle
			row.session_id = row.session_id or sessionId
			if fate == "killed" or row.fate ~= "killed" then
				row.fate = fate or row.fate
			end
			row.name_ref = row.name_ref or nameRef
			return
		end
	end
	snap.elites[#snap.elites + 1] = {
		handle = handle,
		session_id = sessionId,
		unit_id = type(unit.unitdatadef_id) == "string" and unit.unitdatadef_id
			or (type(unit.class) == "string" and unit.class or false),
		name_ref = nameRef,
		fate = fate or "threat",
	}
end

local function lMarkWounded(snap, handle, side)
	if side == "player" then
		snap.player_wounded[handle] = true
	elseif side == "enemy" then
		snap.enemy_wounded[handle] = true
	end
end

local function lCaptureUnit(snap, unit, include_dead)
	if type(snap) ~= "table" or not lIsConflictParticipant(unit) then
		return false, false, false
	end
	local handle = lUnitHandle(unit)
	local side = handle and snap.unit_sides[handle] or lSideKind(unit)
	local dead = lIsDead(unit)
	if not side or not handle or (dead and not include_dead) then
		return false, false, false
	end
	local isNew = not snap.seen_units[handle]
	if isNew then
		snap.seen_units[handle] = true
		snap.unit_sides[handle] = side
		snap.baseline_hp[handle] = tonumber(unit.HitPoints)
		if side == "player" then
			snap.player_start = (tonumber(snap.player_start) or 0) + 1
		else
			snap.enemy_start = (tonumber(snap.enemy_start) or 0) + 1
		end
	end
	side = snap.unit_sides[handle] or side
	local hp = tonumber(unit.HitPoints)
	local baselineHp = tonumber(snap.baseline_hp[handle])
	if not baselineHp and hp then
		baselineHp = hp
		snap.baseline_hp[handle] = hp
	end
	if not dead and hp and baselineHp and hp < baselineHp then
		lMarkWounded(snap, handle, side)
	end
	if side == "enemy" then
		lTrackNamed(snap, unit, dead and "killed" or "threat")
	end
	return handle, side, isNew
end

local function lCountDeath(snap, unit, allow_unseen)
	local handle = lUnitHandle(unit)
	if not handle then
		return false, false
	end
	if not snap.seen_units[handle] then
		if not allow_unseen then
			return false, false
		end
		lCaptureUnit(snap, unit, true)
		if not snap.seen_units[handle] then
			return false, false
		end
	end
	local side = snap.unit_sides[handle] or lSideKind(unit)
	if not side or snap.counted_deaths[handle] then
		return false, side
	end
	snap.counted_deaths[handle] = true
	snap.player_wounded[handle] = nil
	snap.enemy_wounded[handle] = nil
	if side == "player" then
		snap.player_kia = (tonumber(snap.player_kia) or 0) + 1
	else
		snap.enemy_kia = (tonumber(snap.enemy_kia) or 0) + 1
		lTrackNamed(snap, unit, "killed")
	end
	return true, side
end

local function lScanUnits(snap, count_seen_deaths)
	local livingHostile = false
	for _, unit in pairs(lAllUnits()) do
		if lIsConflictParticipant(unit) then
			if lIsDead(unit) then
				if count_seen_deaths then
					lCountDeath(snap, unit, true)
				end
			else
				local _, side = lCaptureUnit(snap, unit, false)
				if side == "enemy" then
					livingHostile = true
				end
			end
		end
	end
	return livingHostile
end

local function lScanSatelliteUnits(snap)
	local livingHostile = false
	local units = rawget(_G, "gv_UnitData")
	for _, unit in pairs(type(units) == "table" and units or {}) do
		local handle = lUnitHandle(unit)
		if handle and snap.seen_units[handle] and lIsConflictParticipant(unit) then
			local dead = lIsDead(unit)
			local _, side = lCaptureUnit(snap, unit, true)
			if dead then
				lCountDeath(snap, unit, false)
			elseif side == "enemy" and not snap.counted_deaths[handle] then
				livingHostile = true
			end
		end
	end
	return livingHostile
end

local function lSnapStore()
	local store = rawget(_G, "g_JAZZ_RIS_CombatSnaps")
	if type(store) ~= "table" then
		store = {}
		rawset(_G, "g_JAZZ_RIS_CombatSnaps", store)
	end
	local legacy = rawget(_G, "g_JAZZ_RIS_CombatSnap")
	if type(legacy) == "table" and legacy.sector_id then
		store[legacy.sector_id] = store[legacy.sector_id] or legacy
		rawset(_G, "g_JAZZ_RIS_CombatSnap", false)
	end
	return store
end

local function lEnsureSnap(sector_id, sector)
	sector_id = sector_id or lCurrentSectorId()
	if not sector_id then
		return false
	end
	local store = lSnapStore()
	local snap = store[sector_id]
	if type(snap) ~= "table" or snap.finalized then
		snap = lNewSnap(sector_id, sector)
		store[sector_id] = snap
	end
	local legacySnap = (tonumber(snap.schema_version) or 0) < RIS_SNAP_SCHEMA
	snap.sector_id = snap.sector_id or sector_id
	snap.started_at = tonumber(snap.started_at) or lNow()
	snap.seen_units = type(snap.seen_units) == "table" and snap.seen_units or {}
	snap.unit_sides = type(snap.unit_sides) == "table" and snap.unit_sides or {}
	snap.baseline_hp = type(snap.baseline_hp) == "table" and snap.baseline_hp or {}
	snap.counted_deaths = type(snap.counted_deaths) == "table" and snap.counted_deaths or {}
	snap.player_wounded = type(snap.player_wounded) == "table" and snap.player_wounded or {}
	snap.enemy_wounded = type(snap.enemy_wounded) == "table" and snap.enemy_wounded or {}
	snap.elites = type(snap.elites) == "table" and snap.elites or {}
	if legacySnap then
		-- Schema 3 uses session ids before transient map handles so tactical and
		-- satellite views describe the same participant exactly once.
		snap.seen_units = {}
		snap.unit_sides = {}
		snap.baseline_hp = {}
		snap.counted_deaths = {}
		snap.player_wounded = {}
		snap.enemy_wounded = {}
	end
	snap.schema_version = RIS_SNAP_SCHEMA
	if legacySnap
		and sector_id == lCurrentSectorId()
		and ((tonumber(snap.player_start) or 0) > 0 or (tonumber(snap.enemy_start) or 0) > 0)
	then
		-- Old mid-conflict snapshots have aggregate starts but no handle sets. Adopt every
		-- currently living unit without incrementing those preserved aggregates.
		for _, unit in pairs(lAllUnits()) do
			if lIsValidUnit(unit) and not lIsDead(unit) then
				local handle = lUnitHandle(unit)
				local side = lSideKind(unit)
				if handle and side then
					snap.seen_units[handle] = true
					snap.unit_sides[handle] = side
					snap.baseline_hp[handle] = tonumber(unit.HitPoints)
					if side == "enemy" then
						lTrackNamed(snap, unit, "threat")
					end
				end
			end
		end
	end
	return snap
end

local function lInPlayerConflict(sector_id)
	sector_id = sector_id or lCurrentSectorId()
	if sector_id and type(lSnapStore()[sector_id]) == "table" then
		return true
	end
	if sector_id and lCurrentSectorId() and sector_id ~= lCurrentSectorId() then
		return false
	end
	if rawget(_G, "g_Combat") or rawget(_G, "g_StartingCombat") then
		return true
	end
	local gameState = rawget(_G, "GameState")
	if type(gameState) == "table" and gameState.Conflict then
		return true
	end
	return false
end

local function lCaptureSquadList(snap, squads)
	local unitData = rawget(_G, "gv_UnitData")
	for _, squad in ipairs(type(squads) == "table" and squads or {}) do
		local ids = type(squad) == "table" and type(squad.units) == "table"
			and squad.units or {}
		for _, id in ipairs(ids) do
			local unit = type(unitData) == "table" and unitData[id]
			if unit and not lIsDead(unit) then
				lCaptureUnit(snap, unit, false)
			end
		end
	end
end

local function lCaptureSatelliteConflict(sector_id)
	local sector = lSectorObject(sector_id)
	local snap = lEnsureSnap(sector_id, sector)
	local getSquads = rawget(_G, "GetSquadsInSector")
	if type(getSquads) == "function" then
		local ok, allied, enemies = pcall(
			getSquads,
			sector_id,
			"exclude_travelling",
			"include_militia",
			"exclude_arriving",
			"exclude_retreating"
		)
		if ok then
			lCaptureSquadList(snap, allied)
			lCaptureSquadList(snap, enemies)
			return snap
		end
	end
	-- Defensive fallback for early lifecycle windows where the helper is absent.
	local squads = rawget(_G, "gv_Squads")
	local rows = {}
	for _, squad in pairs(type(squads) == "table" and squads or {}) do
		if type(squad) == "table"
			and squad.CurrentSector == sector_id
			and not squad.arrival_squad
			and not squad.Retreat
		then
			rows[#rows + 1] = squad
		end
	end
	lCaptureSquadList(snap, rows)
	return snap
end

local function lNoteEnemyPresence(unit)
	if not lIsConflictParticipant(unit) or lSideKind(unit) ~= "enemy" then
		return
	end
	local id = lUnitTypeId(unit)
	local enqueue = rawget(_G, "JAZZ_RIS_EnqueueUnitSighting")
	if id and type(enqueue) == "function" then
		enqueue(id)
	end
end

local function lCaptureSpawnedUnit(unit)
	if not unit or not lInPlayerConflict() then
		return
	end
	local sectorId = lCurrentSectorId()
	local snap = lEnsureSnap(sectorId)
	if type(snap) ~= "table" or snap.finalized then
		return
	end
	local squads = rawget(_G, "gv_Squads")
	local squad = type(squads) == "table" and unit.Squad and squads[unit.Squad]
	if type(squad) == "table"
		and squad.CurrentSector
		and sectorId
		and squad.CurrentSector ~= sectorId
	then
		return
	end
	local dead = lIsDead(unit)
	lCaptureUnit(snap, unit, dead)
	if dead then
		lCountDeath(snap, unit, true)
	else
		lNoteEnemyPresence(unit)
	end
end

local function lCaptureMarkerObjects(objects)
	if type(objects) ~= "table" then
		return
	end
	for _, unit in pairs(objects) do
		lCaptureSpawnedUnit(unit)
	end
end

local function lCapturePlacedUnits(snap, count_deaths)
	if type(snap) ~= "table" then
		return
	end
	local mapGet = rawget(_G, "MapGet")
	if type(mapGet) ~= "function" then
		return
	end
	local ok, markers = pcall(mapGet, "map", "UnitMarker")
	if not ok or type(markers) ~= "table" then
		return
	end
	for _, marker in pairs(markers) do
		if type(marker) == "table" or type(marker) == "userdata" then
			lCaptureMarkerObjects(marker.objects)
			if count_deaths then
				local objects = marker.objects
				if type(objects) == "table" then
					for _, unit in pairs(objects) do
						if lIsDead(unit) then
							lCountDeath(snap, unit, true)
						end
					end
				end
			end
		end
	end
end

local function lCaptureMarkerSpawn(marker, objects)
	lCaptureMarkerObjects(objects or (marker and marker.objects))
end

-- Depth: if another wrap (jazz-nomaps) stored this function as its base, and we
-- later stole the slot and stored *that* wrap as our base, calling base
-- recurses until C stack overflow and Flag Hill / marker maps spawn nobody.
local lMarkerSpawnDepth = 0
local lWrappedMarkerSpawn

local function lCallMarkerSpawnBase(self, fn, ...)
	if type(fn) ~= "function" or fn == lWrappedMarkerSpawn then
		return nil
	end
	local wrap = rawget(_G, "g_JAZZ_RIS_UnitMarkerSpawnWrap")
	if wrap and fn == wrap then
		return nil
	end
	return fn(self, ...)
end

lWrappedMarkerSpawn = function(self, ...)
	local orig = rawget(_G, "g_JAZZ_RIS_UnitMarkerSpawnOrig")
	local base = rawget(_G, "g_JAZZ_RIS_UnitMarkerSpawnBase")
	if lMarkerSpawnDepth > 0 then
		return lCallMarkerSpawnBase(self, orig, ...)
	end
	lMarkerSpawnDepth = lMarkerSpawnDepth + 1
	local objects = lCallMarkerSpawnBase(self, base, ...)
	lMarkerSpawnDepth = lMarkerSpawnDepth - 1
	lCaptureMarkerSpawn(self, objects)
	return objects
end

local function lInstallUnitMarkerWrap()
	local cls = rawget(_G, "UnitMarker")
	if type(cls) ~= "table" or type(cls.SpawnObjects) ~= "function" then
		return
	end
	local current = cls.SpawnObjects
	local wrap = rawget(_G, "g_JAZZ_RIS_UnitMarkerSpawnWrap")
	local orig = rawget(_G, "g_JAZZ_RIS_UnitMarkerSpawnOrig")
	if rawget(_G, "g_JAZZ_RIS_UnitMarkerSpawnWrapped") then
		if current == wrap or current == lWrappedMarkerSpawn then
			cls.SpawnObjects = lWrappedMarkerSpawn
			rawset(_G, "g_JAZZ_RIS_UnitMarkerSpawnWrap", lWrappedMarkerSpawn)
			return
		end
		-- UnitPropertiesStats (or vanilla) restored the class method after ReloadLua.
		if orig and current == orig then
			cls.SpawnObjects = lWrappedMarkerSpawn
			rawset(_G, "g_JAZZ_RIS_UnitMarkerSpawnWrap", lWrappedMarkerSpawn)
			return
		end
		-- Another wrapper owns the slot (NoMaps). Stay in that chain; never re-base
		-- onto it — that pairs RIS.base=nomaps with nomaps.base=RIS.
		return
	end
	rawset(_G, "g_JAZZ_RIS_UnitMarkerSpawnOrig", current)
	rawset(_G, "g_JAZZ_RIS_UnitMarkerSpawnBase", current)
	cls.SpawnObjects = lWrappedMarkerSpawn
	rawset(_G, "g_JAZZ_RIS_UnitMarkerSpawnWrap", lWrappedMarkerSpawn)
	rawset(_G, "g_JAZZ_RIS_UnitMarkerSpawnWrapped", true)
end

local function lAdoptCurrentMapUnits(count_deaths)
	lInstallUnitMarkerWrap()
	local snap = lEnsureSnap(lCurrentSectorId())
	if type(snap) ~= "table" or snap.finalized then
		return snap
	end
	if count_deaths then
		lScanUnits(snap, true)
	else
		for _, unit in pairs(lAllUnits()) do
			if lIsConflictParticipant(unit) and not lIsDead(unit) then
				lCaptureUnit(snap, unit, false)
				lNoteEnemyPresence(unit)
			end
		end
	end
	lCapturePlacedUnits(snap, count_deaths)
	return snap
end

local function lNoteDeathMails(unit, recorded_side)
	if recorded_side ~= "enemy" and lSideKind(unit) ~= "enemy" then
		return
	end
	local nameRef = lDisplayNameRef(unit)
	if unit.elite and nameRef then
		local enqueueElite = rawget(_G, "JAZZ_RIS_EnqueueEliteObit")
		if type(enqueueElite) == "function" then
			enqueueElite(nameRef, nil, lUnitHandle(unit))
		end
	end
	local sid = unit.session_id or unit.unitdatadef_id
	local enqueueNpc = rawget(_G, "JAZZ_RIS_EnqueueNpcObit")
	if type(sid) == "string" and type(enqueueNpc) == "function" then
		enqueueNpc(sid, nameRef)
	end
end

function JAZZ_RIS_OnKill(unit, attacker)
	local id = lUnitTypeId(unit)
	if not id then
		return
	end
	local st = lState()
	if not st then
		return
	end
	st.kills[id] = (tonumber(st.kills[id]) or 0) + 1
	if st.kills[id] >= lThreshold() then
		st.dossiers[id] = true
	end
	local enqueue = rawget(_G, "JAZZ_RIS_EnqueueUnitSighting")
	if type(enqueue) == "function" then
		enqueue(id)
	end
	JAZZ_RIS_NoteQuestMeet("Legion")
	ObjModified("jazz_ris")
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
	if type(bank) ~= "table" or not bank[id] then
		return
	end
	st.quest_met[id] = true
	ObjModified("jazz_ris")
end

local function lQuestParams(state)
	local params = {}
	for key, value in pairs(type(state) == "table" and state or {}) do
		local valueType = type(value)
		if type(key) == "string"
			and (
				valueType == "string"
				or valueType == "number"
				or valueType == "boolean"
				or lIsStableT(value)
			)
		then
			params[key] = value
		end
	end
	return params
end

local function lAppendQuest(ctx, id, source, note, params)
	if type(id) ~= "string" or id == "" then
		return
	end
	for _, existing in ipairs(ctx.quest_ids) do
		if existing == id then
			return
		end
	end
	ctx.quest_ids[#ctx.quest_ids + 1] = id
	ctx.quest_sources[id] = source
	if lIsStableT(note) then
		ctx.quest_notes[id] = note
	end
	if type(params) == "table" and next(params) then
		ctx.quest_params[id] = params
	end
end

--- Resolve stable sector/quest references only; translation happens in the browser.
function JAZZ_RIS_ResolveSectorContext(sector_id)
	local ctx = {
		sector_id = sector_id,
		poi_ref = false,
		quest_ids = {},
		quest_sources = {},
		quest_notes = {},
		quest_params = {},
		quest_linked = false,
	}
	local sector = lSectorObject(sector_id)
	if sector then
		local poi = sector.Label or sector.intel_shortcut or sector.City
		if lIsStableT(poi) then
			ctx.poi_ref = poi
		end
	end

	local getAssociated = rawget(_G, "GetQuestsAssociatedWithSector")
	if sector_id and type(getAssociated) == "function" then
		local ok, associated = pcall(getAssociated, sector_id)
		if ok and type(associated) == "table" then
			for _, quest in ipairs(associated) do
				local preset = quest and quest.preset
				local id = preset and preset.id
				local note = quest and quest.notes and quest.notes[1] and quest.notes[1].Text
				lAppendQuest(ctx, id, "badge", note, lQuestParams(quest and quest.state))
			end
		end
	end
	ctx.quest_linked = #ctx.quest_ids > 0
	return ctx
end

local function lMergeSectorContext(initial, current)
	if type(initial) ~= "table" then
		return current
	end
	if type(current) ~= "table" then
		return initial
	end
	initial.quest_ids = type(initial.quest_ids) == "table" and initial.quest_ids or {}
	initial.quest_sources = type(initial.quest_sources) == "table" and initial.quest_sources or {}
	initial.quest_notes = type(initial.quest_notes) == "table" and initial.quest_notes or {}
	initial.quest_params = type(initial.quest_params) == "table" and initial.quest_params or {}
	local seen = {}
	for _, id in ipairs(initial.quest_ids) do
		seen[id] = true
	end
	for _, id in ipairs(type(current.quest_ids) == "table" and current.quest_ids or {}) do
		if not seen[id] then
			initial.quest_ids[#initial.quest_ids + 1] = id
			seen[id] = true
		end
		local source = current.quest_sources and current.quest_sources[id]
		if source == "badge" or not initial.quest_sources[id] then
			initial.quest_sources[id] = source
		end
		if not initial.quest_notes[id] and current.quest_notes then
			initial.quest_notes[id] = current.quest_notes[id]
		end
		if not initial.quest_params[id] and current.quest_params then
			initial.quest_params[id] = current.quest_params[id]
		end
	end
	initial.quest_linked = not not (initial.quest_linked or current.quest_linked)
	initial.poi_ref = initial.poi_ref or current.poi_ref
	return initial
end

local function lWeatherBand(sector_id)
	local gameState = rawget(_G, "GameState")
	if type(gameState) == "table" and (not sector_id or sector_id == lCurrentSectorId()) then
		if gameState.Night or gameState.Underground then
			return "night"
		end
		if gameState.Fog then
			return "fog"
		end
		if gameState.DustStorm then
			return "dust"
		end
		if gameState.Heat then
			return "heat"
		end
		if gameState.RainHeavy or gameState.RainLight then
			return "rain"
		end
	end
	local getWeather = rawget(_G, "GetCurrentSectorWeather")
	local sectorId = sector_id or lCurrentSectorId()
	local weather = sectorId and type(getWeather) == "function" and getWeather(sectorId) or false
	if weather == "RainLight" or weather == "RainHeavy" then
		return "rain"
	end
	if weather == "Fog" then
		return "fog"
	end
	if weather == "DustStorm" then
		return "dust"
	end
	if weather == "Heat" or weather == "FireStorm" then
		return "heat"
	end
	if weather == "ClearSky" or weather == "Clear" then
		return "clear"
	end
	return "default"
end

local function lOutcome(playerWon, isRetreat)
	if isRetreat then
		return "retreat"
	end
	return playerWon and "win" or "loss"
end

local function lIntensityBand(snap, playerWon, isRetreat)
	local heat = tonumber(snap.heat_delta) or 0
	local playerKia = tonumber(snap.player_kia) or 0
	local enemyKia = tonumber(snap.enemy_kia) or 0
	local totalStart = math.max(1, tonumber(snap.player_start) or 0)
		+ math.max(1, tonumber(snap.enemy_start) or 0)
	local rate = math.floor(((playerKia + enemyKia) * 100 + totalStart / 2) / totalStart)
	if heat >= 40 or rate >= 55 or (not playerWon and not isRetreat and rate >= 35) then
		return "high"
	end
	if heat >= 15 or rate >= 25 then
		return "mid"
	end
	return "low"
end

local function lHashIndex(count, key)
	if count <= 0 then
		return 1
	end
	local hash = 0
	key = tostring(key or "")
	for i = 1, #key do
		hash = (hash * 131 + string.byte(key, i)) % 2147483647
	end
	return (hash % count) + 1
end

local function lHeadlineCount(key)
	local aar = rawget(_G, "JAZZ_RIS_AAR")
	local bank = type(aar) == "table" and type(aar.headlines) == "table" and aar.headlines[key]
	return type(bank) == "table" and math.max(1, #bank) or 1
end

local function lClosingKey(intensity, playerWon, isRetreat, hostilesRemain)
	if hostilesRemain then
		return "noise"
	end
	if intensity == "low" and playerWon then
		return "quiet"
	end
	if intensity == "high" and (not playerWon or isRetreat) then
		return "disaster"
	end
	return "noise"
end

local function lCountSet(set, deaths)
	local count = 0
	for handle in pairs(type(set) == "table" and set or {}) do
		if not (type(deaths) == "table" and deaths[handle]) then
			count = count + 1
		end
	end
	return count
end

local function lFinalizeNamedFates(snap, playerWon, isRetreat, scanMap)
	local present = {}
	local function note(unit)
		if not lIsConflictParticipant(unit) or not lIsNamedOpponent(unit) then
			return
		end
		local handle = lUnitHandle(unit)
		local side = handle and snap.unit_sides[handle] or lSideKind(unit)
		if side ~= "enemy" or not handle or present[handle] then
			return
		end
		present[handle] = true
		if lIsDead(unit) then
			lTrackNamed(snap, unit, "killed")
		elseif snap.enemy_wounded[handle] then
			lTrackNamed(snap, unit, "wounded")
		else
			lTrackNamed(snap, unit, "threat")
		end
	end
	if scanMap then
		for _, unit in pairs(lAllUnits()) do
			note(unit)
		end
	end
	local unitData = rawget(_G, "gv_UnitData")
	for _, unit in pairs(type(unitData) == "table" and unitData or {}) do
		local handle = lUnitHandle(unit)
		if handle and snap.seen_units[handle] then
			note(unit)
		end
	end
	for _, row in ipairs(snap.elites) do
		if row.fate ~= "killed" and not present[row.handle] then
			row.fate = "escaped"
		end
	end
end

local function lCaptureFinalizeSnap(sector, playerWon, isRetreat, autoResolve)
	local sectorId = lSectorId(sector)
	local store = lSnapStore()
	local existing = sectorId and store[sectorId]
	local hadMatchingSnap = type(existing) == "table" and not existing.finalized
	local snap
	if hadMatchingSnap then
		snap = lEnsureSnap(sectorId, sector)
	else
		-- Lifecycle recovery: if ConflictStart was missed (old save/reload or
		-- another handler's early exit), capture every participant still
		-- recoverable instead of emitting a guaranteed 0/0 report.
		snap = sectorId and lCaptureSatelliteConflict(sectorId)
			or lNewSnap(sectorId, sector)
	end
	snap.sector_id = snap.sector_id or sectorId

	local scanMap = not autoResolve and sectorId and sectorId == lCurrentSectorId()
	local livingHostile = false
	if scanMap then
		lInstallUnitMarkerWrap()
		livingHostile = lScanUnits(snap, true)
		lCapturePlacedUnits(snap, true)
	end
	livingHostile = lScanSatelliteUnits(snap) or livingHostile
	snap.player_wia = lCountSet(snap.player_wounded, snap.counted_deaths)
	snap.enemy_wia = lCountSet(snap.enemy_wounded, snap.counted_deaths)
	snap.heat_delta = math.max(
		0,
		lHeatForSector(snap.sector_id, sector) - (tonumber(snap.heat_start) or 0)
	)
	snap.sector_ctx = lMergeSectorContext(
		snap.sector_ctx,
		JAZZ_RIS_ResolveSectorContext(snap.sector_id)
	)
	snap.hostiles_remain = playerWon and livingHostile or false
	lFinalizeNamedFates(snap, playerWon, isRetreat, scanMap)
	return snap
end

local function lCopyStableElites(rows)
	local copy = {}
	for _, row in ipairs(type(rows) == "table" and rows or {}) do
		copy[#copy + 1] = {
			handle = row.handle,
			session_id = row.session_id,
			unit_id = row.unit_id,
			name_ref = row.name_ref,
			fate = row.fate or "threat",
		}
	end
	table.sort(copy, function(a, b)
		return tostring(a.handle or "") < tostring(b.handle or "")
	end)
	return copy
end

local function lCopyArray(values)
	local copy = {}
	for i, value in ipairs(type(values) == "table" and values or {}) do
		copy[i] = value
	end
	return copy
end

local function lCopyMap(values)
	local copy = {}
	for key, value in pairs(type(values) == "table" and values or {}) do
		copy[key] = value
	end
	return copy
end

local function lCopyQuestParams(values)
	local copy = {}
	for questId, params in pairs(type(values) == "table" and values or {}) do
		if type(params) == "table" then
			copy[questId] = lCopyMap(params)
		end
	end
	return copy
end

local function lBuildAARRecord(snap, playerWon, isRetreat, autoResolve)
	local outcome = lOutcome(playerWon, isRetreat)
	local intensity = lIntensityBand(snap, playerWon, isRetreat)
	local headlineKey = outcome .. "|" .. intensity
	local ctx = snap.sector_ctx or JAZZ_RIS_ResolveSectorContext(snap.sector_id)
	local characterKey = outcome
	if snap.ambush then
		characterKey = "ambush"
	elseif ctx.quest_linked then
		characterKey = "quest_" .. outcome
	end
	local game = rawget(_G, "Game")
	local seed = table.concat({
		tostring(game and game.id or ""),
		tostring(snap.sector_id or ""),
		tostring(snap.started_at or 0),
		tostring(snap.player_start or 0),
		tostring(snap.enemy_start or 0),
		tostring(snap.player_kia or 0),
		tostring(snap.enemy_kia or 0),
		headlineKey,
	}, "|")
	return {
		schema_version = RIS_SNAP_SCHEMA,
		record_version = RIS_AAR_RECORD_VERSION,
		version = RIS_AAR_RECORD_VERSION,
		kind = "aar",
		time = lNow(),
		sector_id = snap.sector_id,
		outcome = outcome,
		headline_key = headlineKey,
		headline_index = lHashIndex(lHeadlineCount(headlineKey), seed),
		weather_key = lWeatherBand(snap.sector_id),
		intensity_key = intensity,
		character_key = characterKey,
		closing_key = lClosingKey(intensity, playerWon, isRetreat, snap.hostiles_remain),
		autoResolve = autoResolve and true or false,
		player_start = tonumber(snap.player_start) or 0,
		enemy_start = tonumber(snap.enemy_start) or 0,
		player_kia = tonumber(snap.player_kia) or 0,
		enemy_kia = tonumber(snap.enemy_kia) or 0,
		player_wia = tonumber(snap.player_wia) or 0,
		enemy_wia = tonumber(snap.enemy_wia) or 0,
		heat_delta = tonumber(snap.heat_delta) or 0,
		ambush = snap.ambush and true or false,
		hostiles_remain = snap.hostiles_remain and true or false,
		quest_ids = lCopyArray(ctx.quest_ids),
		quest_sources = lCopyMap(ctx.quest_sources),
		quest_notes = lCopyMap(ctx.quest_notes),
		quest_params = lCopyQuestParams(ctx.quest_params),
		quest_linked = ctx.quest_linked and true or false,
		poi_ref = ctx.poi_ref,
		elites = lCopyStableElites(snap.elites),
	}
end

local function lConflictToken(sectorId, playerWon, isRetreat, autoResolve)
	return table.concat({
		tostring(sectorId or ""),
		tostring(lNow()),
		playerWon and "win" or "loss",
		isRetreat and "retreat" or "stand",
		autoResolve and "auto" or "tactical",
	}, "|")
end

local function lPersistAAR(st, entry)
	table.insert(st.battles, 1, entry)
	while #st.battles > lCap() do
		table.remove(st.battles)
	end
end

function JAZZ_RIS_FinalizeBattle(sector, playerWon, isRetreat, autoResolve)
	local st = lState()
	if not st then
		return false
	end
	local sectorId = lSectorId(sector)
	local token = lConflictToken(sectorId, playerWon, isRetreat, autoResolve)
	local store = lSnapStore()
	local current = sectorId and store[sectorId]
	if type(current) ~= "table" and st.last_battle_token == token then
		if sectorId then
			store[sectorId] = nil
		end
		return false
	end
	if type(current) == "table" and current.finalized then
		store[sectorId] = nil
		return false
	end
	local snap = lCaptureFinalizeSnap(sector, playerWon, isRetreat, autoResolve)
	snap.finalized = true
	lPersistAAR(st, lBuildAARRecord(snap, playerWon, isRetreat, autoResolve))
	st.last_battle_token = token
	if sectorId then
		store[sectorId] = nil
	end
	ObjModified("jazz_ris")
	return true
end

function OnMsg.AutoResolveChoice(sector_id, choice)
	if choice ~= "AutoResolve" then
		return
	end
	local snap = sector_id and lSnapStore()[sector_id]
	if type(snap) == "table" and not snap.finalized then
		snap.auto_resolve_pending = true
	end
end

function OnMsg.ModsReloaded()
	lInstallUnitMarkerWrap()
end

function OnMsg.EnterSector()
	if not lInPlayerConflict() then
		lInstallUnitMarkerWrap()
		return
	end
	lAdoptCurrentMapUnits(false)
end

function OnMsg.ConflictStart(sector_id)
	lInstallUnitMarkerWrap()
	if sector_id then
		lCaptureSatelliteConflict(sector_id)
	end
end

function OnMsg.CombatStart()
	lAdoptCurrentMapUnits(false)
end

function OnMsg.UnitCreated(unit)
	if not unit or not lInPlayerConflict() then
		return
	end
	local delayed = rawget(_G, "DelayedCall")
	if type(delayed) == "function" then
		delayed(0, function()
			lCaptureSpawnedUnit(unit)
		end)
		return
	end
	lCaptureSpawnedUnit(unit)
end

function OnMsg.UnitDowned(unit)
	if not unit or not lInPlayerConflict() then
		return
	end
	local snap = lEnsureSnap(lCurrentSectorId())
	local handle, side = lCaptureUnit(snap, unit, true)
	if handle and side then
		lMarkWounded(snap, handle, side)
	end
end

local function lHandleUnitDeath(unit, attacker, sector_id)
	sector_id = sector_id or lCurrentSectorId()
	if not unit or not lInPlayerConflict(sector_id) then
		return
	end
	local snap = lEnsureSnap(sector_id)
	local handle = lUnitHandle(unit)
	local side = handle and snap.unit_sides[handle] or lSideKind(unit)
	if not side then
		return
	end
	local counted, countedSide = lCountDeath(snap, unit, true)
	if not counted then
		return
	end
	if countedSide == "enemy" then
		lNoteDeathMails(unit, countedSide)
		JAZZ_RIS_OnKill(unit, attacker)
	end
end

function OnMsg.UnitDiedOnSector(unit, sector_id)
	lHandleUnitDeath(unit, false, sector_id)
end

function OnMsg.UnitDied(unit, attacker, results)
	lHandleUnitDeath(unit, attacker, lCurrentSectorId())
end

function OnMsg.CombatEnd()
	local sectorId = lCurrentSectorId()
	local snap = sectorId and lSnapStore()[sectorId]
	if type(snap) == "table" and not snap.finalized then
		lScanUnits(snap, true)
		lCapturePlacedUnits(snap, true)
		snap.player_wia = lCountSet(snap.player_wounded, snap.counted_deaths)
		snap.enemy_wia = lCountSet(snap.enemy_wounded, snap.counted_deaths)
	end
end

function OnMsg.ConflictEnd(sector, _, playerAttacked, playerWon, autoResolve, isRetreat, startedFromMap)
	if not sector then
		return
	end
	if playerAttacked == false and not playerWon and not isRetreat then
		if type(lSnapStore()[lSectorId(sector)]) ~= "table" then
			return
		end
	end
	local sectorId = lSectorId(sector)
	local snap = sectorId and lSnapStore()[sectorId]
	autoResolve = autoResolve
		or (type(snap) == "table" and snap.auto_resolve_pending)
	JAZZ_RIS_FinalizeBattle(
		sector,
		playerWon and true or false,
		isRetreat and true or false,
		autoResolve and true or false
	)
end

function OnMsg.AutoResolvedConflict(sector_id)
	local st = lState()
	if not st or type(st.battles) ~= "table" then
		return
	end
	for _, battle in ipairs(st.battles) do
		if type(battle) == "table"
			and battle.sector_id == sector_id
			and tonumber(battle.time) == tonumber(lNow())
		then
			if not battle.autoResolve then
				battle.autoResolve = true
				ObjModified("jazz_ris")
			end
			return
		end
	end
end

local function lRefreshQuestMeets()
	local bank = rawget(_G, "JAZZ_RIS_QUEST_DOSSIERS")
	if type(bank) ~= "table" then
		return
	end
	local isMet = rawget(_G, "IsMet")
	local unitData = rawget(_G, "gv_UnitData")
	for id in pairs(bank) do
		if id ~= "Legion" then
			local met = false
			if type(isMet) == "function" then
				met = isMet(id) and true or false
			elseif type(unitData) == "table" and unitData[id] and unitData[id].IsMet then
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
