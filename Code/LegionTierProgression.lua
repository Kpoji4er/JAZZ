-- JAZZ-COMPAT-003: NoMaps Legion equipment tier (time / mine / WorldFlip).
-- JAZZ-COMPAT-008: Maps Legion equipment tier (time / mainland occupation / 5 mines).
-- Quest TCE by PlayerControlSectors are gated off; this file owns both profiles.

local QUEST_ID = "JAZZ_LegionTier"
local VAR_ID = "JAZZ_Legion_Tier"
local BETRAYAL_QUEST = "04_Betrayal"
local ERNIE_REGION_ID = "ErnieIsland"

local DAY = false
local function lDay()
	if not DAY then
		DAY = (const and const.Scale and const.Scale.day) or (24 * ((const and const.Scale and const.Scale.h) or 1))
	end
	return DAY
end

-- --- NoMaps intervals (COMPAT-003) ---
local NOMAPS_T1_SUB_INTERVAL_DAYS = 3
local NOMAPS_T2_UNLOCK_DELAY_DAYS = 3
local NOMAPS_T2_T3_SUB_INTERVAL_DAYS = 14

-- --- Maps intervals (COMPAT-008) ---
local MAPS_T1_SUB_INTERVAL_DAYS = 7
local MAPS_T2_T3_SUB_INTERVAL_DAYS = 30
local MAPS_T3_MINE_COUNT = 5

local MAX_SUB = {
	[1] = 3,
	[2] = 5,
	[3] = 3,
}

local NOMAPS_STATE_SCHEMA = 2
local MAPS_STATE_SCHEMA = 1

-- Default schema 1 so first load of older saves migrates (backdate mine delay if mine already held).
GameVar("gv_JAZZ_LegionTierNoMaps", function()
	return {
		schema = 1,
		first_mine_at = false, -- CampaignTime when player first owned a mine
		major = 1,
		major_started_at = false, -- CampaignTime when current major began
	}
end)

GameVar("gv_JAZZ_LegionTierMaps", function()
	return {
		schema = MAPS_STATE_SCHEMA,
		mainland_at = false, -- CampaignTime of first mainland sector occupation
		major = 1,
		major_started_at = false,
	}
end)

local function lNoMapsActive()
	return rawget(_G, "JAZZ_NoMapsIsActive") and JAZZ_NoMapsIsActive() or false
end

local function lMapsActive()
	return not lNoMapsActive()
end

local function lNow()
	return Game and Game.CampaignTime or 0
end

local function lSectorIsSurface(sector)
	return sector and not sector.GroundSector and sector.Passability ~= "Water" and sector.Passability ~= "Blocked"
end

local function lIsPlayerSide(side)
	return side == "player1" or side == "player2"
end

local g_JAZZ_ErnieSectorSet = false

-- Authored ErnieIsland.Sectors (items.lua); used if Regions not ready yet.
local ERNIE_SECTORS_FALLBACK = {
	"M1", "M2", "M3", "M4", "M5", "M6", "M7",
	"L1", "L2", "L3", "L4", "L5", "L6", "L7",
	"K2", "K3", "K4", "K5", "K6", "K7",
	"J2", "J3", "J4", "J5", "J6", "J7",
	"I2", "I3", "I4", "I5", "I6", "I7",
}

local function lErnieSectorSet()
	if g_JAZZ_ErnieSectorSet and next(g_JAZZ_ErnieSectorSet) then
		return g_JAZZ_ErnieSectorSet
	end
	local set = {}
	local region = rawget(_G, "Regions") and Regions[ERNIE_REGION_ID]
	local list = region and region.Sectors
	if type(list) ~= "table" or not list[1] then
		list = ERNIE_SECTORS_FALLBACK
	end
	for _, sid in ipairs(list) do
		set[sid] = true
	end
	if next(set) then
		g_JAZZ_ErnieSectorSet = set
	end
	return set
end

-- True for Ernie Island surface sectors. Used to refuse mainland unlock.
function JAZZ_IsErnieIslandSector(sector_or_id)
	local sector, sid
	if type(sector_or_id) == "string" then
		sid = sector_or_id
		sector = gv_Sectors and gv_Sectors[sid]
	else
		sector = sector_or_id
		sid = sector and (sector.Id or sector.id)
	end
	if not sid then
		return false
	end
	local set = lErnieSectorSet()
	if set[sid] then
		return true
	end
	-- Extra tags if Id missing from region list (mods / underground surface aliases).
	if not sector then
		return false
	end
	if sector.WeatherZone == "Erny" then
		return true
	end
	local city = sector.City
	if city == "ErnieVillage" or city == "Rebels_Ernie" or city == "SmugglersErnie" then
		return true
	end
	if sector.Label1 == "Ernie" or sector.Label2 == "Ernie" then
		return true
	end
	return false
end

-- Same signal Bobby Ray uses for shop tier 3: TriggerWorldFlip OR WorldFlipDone.
function JAZZ_IsWorldFlipProgressionActive()
	local quest = gv_Quests and gv_Quests[BETRAYAL_QUEST]
	if not quest then
		return false
	end
	local state = QuestGetState and QuestGetState(BETRAYAL_QUEST)
	local src = state or quest
	return not not (src.TriggerWorldFlip or src.WorldFlipDone)
end

function JAZZ_CountPlayerMines()
	local mines = 0
	for _, sector in sorted_pairs(gv_Sectors or empty_table) do
		if lSectorIsSurface(sector) and lIsPlayerSide(sector.Side) and sector.Mine then
			mines = mines + 1
		end
	end
	return mines
end

function JAZZ_PlayerOwnsMainlandSurfaceSector()
	for sid, sector in sorted_pairs(gv_Sectors or empty_table) do
		if lSectorIsSurface(sector) and lIsPlayerSide(sector.Side) and not JAZZ_IsErnieIslandSector(sid) then
			return true
		end
	end
	return false
end

local function lEnsureNoMapsState()
	local st = gv_JAZZ_LegionTierNoMaps
	if type(st) ~= "table" then
		st = {
			schema = NOMAPS_STATE_SCHEMA,
			first_mine_at = false,
			major = 1,
			major_started_at = false,
		}
		gv_JAZZ_LegionTierNoMaps = st
	end
	st.major = st.major or 1
	return st
end

local function lEnsureMapsState()
	local st = gv_JAZZ_LegionTierMaps
	if type(st) ~= "table" then
		st = {
			schema = MAPS_STATE_SCHEMA,
			mainland_at = false,
			major = 1,
			major_started_at = false,
		}
		gv_JAZZ_LegionTierMaps = st
	end
	st.major = st.major or 1
	return st
end

local function lGetCurrentTier()
	local quest = gv_Quests and gv_Quests[QUEST_ID]
	if not quest then
		return false
	end
	local state = QuestGetState and QuestGetState(QUEST_ID)
	if state and state[VAR_ID] ~= nil then
		return tonumber(state[VAR_ID]) or false
	end
	return tonumber(quest[VAR_ID]) or false
end

-- Console helper: bare `JAZZ_Legion_Tier` is a quest var, not a global (prints nothing).
-- Use: JAZZ_GetLegionTier()  or  GetQuestVar("JAZZ_LegionTier", "JAZZ_Legion_Tier")
function JAZZ_GetLegionTier()
	return lGetCurrentTier() or (GetQuestVar and GetQuestVar(QUEST_ID, VAR_ID)) or false
end

local function lSetTier(value)
	local quest = QuestGetState and QuestGetState(QUEST_ID)
	if not quest then
		return false
	end
	-- SetQuestVar → QuestTCEEvaluation needs Groups as a table; early NewGame may still have boolean.
	if type(rawget(_G, "Groups")) == "table" and SetQuestVar then
		SetQuestVar(quest, VAR_ID, value)
		return true
	end
	rawset(quest, VAR_ID, value)
	return true
end

local function lApplyTierRaise(computed, log_label, extra)
	local current = lGetCurrentTier() or 11
	local quest_state = QuestGetState and QuestGetState(QUEST_ID)
	local needs_rawset = quest_state and rawget(quest_state, VAR_ID) == nil
	if computed <= current and not needs_rawset then
		return false
	end
	local write = computed > current and computed or current
	if not lSetTier(write) then
		return false
	end
	if computed <= current then
		return false
	end
	if rawget(_G, "RegenerateLegionLoot") then
		RegenerateLegionLoot()
	end
	if CombatLog and Untranslated then
		CombatLog("debug", Untranslated(string.format(
			"[JAZZ Legion Tier] %s %d → %d%s",
			log_label,
			current,
			computed,
			extra or ""
		)))
	end
	if rawget(_G, "JAZZ_RIS_OnTierRaised") then
		JAZZ_RIS_OnTierRaised(computed)
	end
	return computed
end

local function lSubIntervalDays(major, t1_days, t2t3_days)
	if major == 1 then
		return t1_days
	end
	return t2t3_days
end

local function lComputeTierSub(now, major_started_at, major, interval_days)
	major = major or 1
	local max_sub = MAX_SUB[major] or 3
	local started = major_started_at or now or 0
	local elapsed = Max(0, (now or 0) - started)
	local interval = interval_days * lDay()
	if interval <= 0 then
		return major * 10 + 1
	end
	local step = math.floor(elapsed / interval)
	local sub = Min(max_sub, 1 + step)
	return major * 10 + sub
end

--- Latch major_started_at / bump major when target advances (shared Maps/NoMaps).
local function lAdvanceMajorState(st, now, target_major)
	if not st.major_started_at then
		st.major_started_at = now
		st.major = target_major
	elseif target_major > (st.major or 1) then
		st.major = target_major
		st.major_started_at = now
	end
end

---------------------------------------------------------------------------
-- NoMaps (COMPAT-003)
---------------------------------------------------------------------------

local function lMigrateNoMapsState(st, now, mines)
	if (st.schema or 0) >= NOMAPS_STATE_SCHEMA then
		return
	end
	-- Pre-timer / schema1 saves: if a mine is already held, do not re-wait 3 days.
	if mines >= 1 and not st.first_mine_at then
		st.first_mine_at = now - NOMAPS_T2_UNLOCK_DELAY_DAYS * lDay()
	end
	if not st.major_started_at then
		st.major_started_at = now
	end
	st.schema = NOMAPS_STATE_SCHEMA
end

local function lNoMapsSubIntervalDays(major)
	return lSubIntervalDays(major, NOMAPS_T1_SUB_INTERVAL_DAYS, NOMAPS_T2_T3_SUB_INTERVAL_DAYS)
end

function JAZZ_ComputeLegionTierNoMapsSub(now, major_started_at, major)
	return lComputeTierSub(now, major_started_at, major, lNoMapsSubIntervalDays(major or 1))
end

function JAZZ_ComputeLegionTierNoMapsMajor(now, first_mine_at, world_flip)
	if world_flip then
		return 3
	end
	if first_mine_at and (now - first_mine_at) >= NOMAPS_T2_UNLOCK_DELAY_DAYS * lDay() then
		return 2
	end
	return 1
end

function JAZZ_UpdateLegionTierForNoMaps()
	if not lNoMapsActive() then
		return false
	end
	if not gv_Quests or not gv_Quests[QUEST_ID] then
		return false
	end

	local now = lNow()
	local st = lEnsureNoMapsState()
	local mines = JAZZ_CountPlayerMines()
	lMigrateNoMapsState(st, now, mines)

	if mines >= 1 and not st.first_mine_at then
		st.first_mine_at = now
	end

	local world_flip = JAZZ_IsWorldFlipProgressionActive()
	local target_major = JAZZ_ComputeLegionTierNoMapsMajor(now, st.first_mine_at, world_flip)
	lAdvanceMajorState(st, now, target_major)

	local computed = JAZZ_ComputeLegionTierNoMapsSub(now, st.major_started_at, st.major)
	return lApplyTierRaise(computed, "NoMaps", string.format(
		" (major=%d mine_at=%s worldflip=%s)",
		st.major or 0,
		tostring(st.first_mine_at),
		tostring(world_flip)
	))
end

---------------------------------------------------------------------------
-- Maps (COMPAT-008)
---------------------------------------------------------------------------

local function lMapsSubIntervalDays(major)
	return lSubIntervalDays(major, MAPS_T1_SUB_INTERVAL_DAYS, MAPS_T2_T3_SUB_INTERVAL_DAYS)
end

function JAZZ_ComputeLegionTierMapsSub(now, major_started_at, major)
	return lComputeTierSub(now, major_started_at, major, lMapsSubIntervalDays(major or 1))
end

function JAZZ_ComputeLegionTierMapsMajor(mainland_at, mine_count)
	if (mine_count or 0) >= MAPS_T3_MINE_COUNT then
		return 3
	end
	if mainland_at then
		return 2
	end
	return 1
end

-- Occupation-only latch (SectorSideChanged → player). Not merc hire / travel.
function JAZZ_NoteMapsMainlandOccupation(sector_id)
	if not lMapsActive() then
		return false
	end
	if not sector_id then
		return false
	end
	local sector = gv_Sectors and gv_Sectors[sector_id]
	if not lSectorIsSurface(sector) then
		return false
	end
	if JAZZ_IsErnieIslandSector(sector_id) then
		return false
	end
	local st = lEnsureMapsState()
	if st.mainland_at then
		return false
	end
	st.mainland_at = lNow()
	return true
end

function JAZZ_UpdateLegionTierForMaps()
	if not lMapsActive() then
		return false
	end
	if not gv_Quests or not gv_Quests[QUEST_ID] then
		return false
	end

	local now = lNow()
	local st = lEnsureMapsState()
	st.schema = MAPS_STATE_SCHEMA

	-- Existing saves already on mainland geography: latch without requiring a new capture.
	if not st.mainland_at and JAZZ_PlayerOwnsMainlandSurfaceSector() then
		st.mainland_at = now
	end

	local mines = JAZZ_CountPlayerMines()
	local target_major = JAZZ_ComputeLegionTierMapsMajor(st.mainland_at, mines)
	lAdvanceMajorState(st, now, target_major)

	local computed = JAZZ_ComputeLegionTierMapsSub(now, st.major_started_at, st.major)
	return lApplyTierRaise(computed, "Maps", string.format(
		" (major=%d mainland_at=%s mines=%d)",
		st.major or 0,
		tostring(st.mainland_at),
		mines
	))
end

function JAZZ_UpdateLegionTierProgression()
	if lNoMapsActive() then
		return JAZZ_UpdateLegionTierForNoMaps()
	end
	return JAZZ_UpdateLegionTierForMaps()
end

---------------------------------------------------------------------------
-- Hooks
---------------------------------------------------------------------------

function OnMsg.SectorSideChanged(sector_id, old_side, side)
	if lNoMapsActive() then
		JAZZ_UpdateLegionTierForNoMaps()
		return
	end
	if lIsPlayerSide(side) and not lIsPlayerSide(old_side) then
		JAZZ_NoteMapsMainlandOccupation(sector_id)
	end
	JAZZ_UpdateLegionTierForMaps()
end

function OnMsg.SatelliteTick()
	JAZZ_UpdateLegionTierProgression()
end

function OnMsg.OpenSatelliteView()
	JAZZ_UpdateLegionTierProgression()
end

function OnMsg.LoadGame()
	-- Nomaps bootstrap may run after this handler (jazz loads first). Skip until active;
	-- nomaps calls update after bootstrap, and SatelliteTick / OpenSatelliteView recover.
	if lNoMapsActive() then
		JAZZ_UpdateLegionTierForNoMaps()
	elseif gv_Quests and gv_Quests[QUEST_ID] then
		JAZZ_UpdateLegionTierForMaps()
	end
end

function OnMsg.NewGame()
	if lNoMapsActive() then
		gv_JAZZ_LegionTierNoMaps = {
			schema = NOMAPS_STATE_SCHEMA,
			first_mine_at = false,
			major = 1,
			major_started_at = lNow(),
		}
		JAZZ_UpdateLegionTierForNoMaps()
		return
	end
	gv_JAZZ_LegionTierMaps = {
		schema = MAPS_STATE_SCHEMA,
		mainland_at = false,
		major = 1,
		major_started_at = lNow(),
	}
	JAZZ_UpdateLegionTierForMaps()
end
