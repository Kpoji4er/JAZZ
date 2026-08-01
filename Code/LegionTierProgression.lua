-- JAZZ-COMPAT-003: NoMaps-only Legion equipment tier progression (time-based).
-- Major: T1 start → T2 after first mine + 3 days → T3 on WorldFlip.
-- Sub: T1 every 3 days; T2/T3 every 14 days. Maps/Ernie keep quest TCE.

local QUEST_ID = "JAZZ_LegionTier"
local VAR_ID = "JAZZ_Legion_Tier"
local BETRAYAL_QUEST = "04_Betrayal"

local DAY = false
local function lDay()
	if not DAY then
		DAY = (const and const.Scale and const.Scale.day) or (24 * ((const and const.Scale and const.Scale.h) or 1))
	end
	return DAY
end

-- T1 sub step; also delay from first mine until T2 unlock.
local T1_SUB_INTERVAL_DAYS = 3
local T2_UNLOCK_DELAY_DAYS = 3
-- T2 / T3 sub step
local T2_T3_SUB_INTERVAL_DAYS = 14

local MAX_SUB = {
	[1] = 3,
	[2] = 5,
	[3] = 3,
}

local STATE_SCHEMA = 2

-- Default schema 1 so first load of older saves migrates (backdate mine delay if mine already held).
GameVar("gv_JAZZ_LegionTierNoMaps", function()
	return {
		schema = 1,
		first_mine_at = false, -- CampaignTime when player first owned a mine
		major = 1,
		major_started_at = false, -- CampaignTime when current major began
	}
end)

local function lNoMapsActive()
	return rawget(_G, "JAZZ_NoMapsIsActive") and JAZZ_NoMapsIsActive() or false
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

local function lEnsureTierState()
	local st = gv_JAZZ_LegionTierNoMaps
	if type(st) ~= "table" then
		st = {
			schema = STATE_SCHEMA,
			first_mine_at = false,
			major = 1,
			major_started_at = false,
		}
		gv_JAZZ_LegionTierNoMaps = st
	end
	st.major = st.major or 1
	return st
end

local function lSubIntervalDays(major)
	if major == 1 then
		return T1_SUB_INTERVAL_DAYS
	end
	return T2_T3_SUB_INTERVAL_DAYS
end

-- Pure formula for tests / diagnostics.
-- now, major_started_at: CampaignTime; major: 1..3
function JAZZ_ComputeLegionTierNoMapsSub(now, major_started_at, major)
	major = major or 1
	local max_sub = MAX_SUB[major] or 3
	local started = major_started_at or now or 0
	local elapsed = Max(0, (now or 0) - started)
	local interval = lSubIntervalDays(major) * lDay()
	if interval <= 0 then
		return major * 10 + 1
	end
	local step = math.floor(elapsed / interval)
	local sub = Min(max_sub, 1 + step)
	return major * 10 + sub
end

-- Target major only (no sub). first_mine_at may be false.
function JAZZ_ComputeLegionTierNoMapsMajor(now, first_mine_at, world_flip)
	if world_flip then
		return 3
	end
	if first_mine_at and (now - first_mine_at) >= T2_UNLOCK_DELAY_DAYS * lDay() then
		return 2
	end
	return 1
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

local function lMigrateState(st, now, mines)
	if (st.schema or 0) >= STATE_SCHEMA then
		return
	end
	-- Pre-timer / schema1 saves: if a mine is already held, do not re-wait 3 days.
	if mines >= 1 and not st.first_mine_at then
		st.first_mine_at = now - T2_UNLOCK_DELAY_DAYS * lDay()
	end
	if not st.major_started_at then
		st.major_started_at = now
	end
	st.schema = STATE_SCHEMA
end

-- Only raises tier (never rolls back). Returns new tier or false if unchanged/inactive.
function JAZZ_UpdateLegionTierForNoMaps()
	if not lNoMapsActive() then
		return false
	end
	if not gv_Quests or not gv_Quests[QUEST_ID] then
		return false
	end

	local now = lNow()
	local st = lEnsureTierState()
	local mines = JAZZ_CountPlayerMines()
	lMigrateState(st, now, mines)

	if mines >= 1 and not st.first_mine_at then
		st.first_mine_at = now
	end

	local world_flip = JAZZ_IsWorldFlipProgressionActive()
	local target_major = JAZZ_ComputeLegionTierNoMapsMajor(now, st.first_mine_at, world_flip)

	if not st.major_started_at then
		st.major_started_at = now
		st.major = target_major
	elseif target_major > (st.major or 1) then
		st.major = target_major
		st.major_started_at = now
	end

	local computed = JAZZ_ComputeLegionTierNoMapsSub(now, st.major_started_at, st.major)
	local current = lGetCurrentTier() or 11
	-- Always rawset when loot conditions cannot see metatable default (rawget nil).
	local quest_state = QuestGetState and QuestGetState(QUEST_ID)
	local needs_rawset = quest_state and rawget(quest_state, VAR_ID) == nil
	if computed <= current and not needs_rawset then
		return false
	end
	if not lSetTier(computed > current and computed or current) then
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
			"[JAZZ Legion Tier] NoMaps %d → %d (major=%d mine_at=%s worldflip=%s)",
			current,
			computed,
			st.major or 0,
			tostring(st.first_mine_at),
			tostring(world_flip)
		)))
	end
	return computed
end

function OnMsg.SectorSideChanged(sector_id, old_side, side)
	JAZZ_UpdateLegionTierForNoMaps()
end

function OnMsg.SatelliteTick()
	JAZZ_UpdateLegionTierForNoMaps()
end

function OnMsg.OpenSatelliteView()
	JAZZ_UpdateLegionTierForNoMaps()
end

function OnMsg.LoadGame()
	-- Nomaps bootstrap (same message) may run after this handler because jazz loads
	-- first. Skip until active; nomaps calls JAZZ_UpdateLegionTierForNoMaps after bootstrap,
	-- and SatelliteTick / OpenSatelliteView recover otherwise.
	if lNoMapsActive() then
		JAZZ_UpdateLegionTierForNoMaps()
	end
end

function OnMsg.NewGame()
	-- Same race as LoadGame: nomaps sets active during its NewGame bootstrap.
	if not lNoMapsActive() then
		return
	end
	gv_JAZZ_LegionTierNoMaps = {
		schema = STATE_SCHEMA,
		first_mine_at = false,
		major = 1,
		major_started_at = lNow(),
	}
	JAZZ_UpdateLegionTierForNoMaps()
end
