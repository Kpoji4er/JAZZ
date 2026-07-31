-- JAZZ-COMPAT-003: NoMaps Legion equipment tier —
-- major from mines (I→II) + WorldFlip (III); sub from sectors.
-- Maps / Ernie profile keeps quest TCE on PlayerControlSectors (gated off while NoMaps active).

local QUEST_ID = "JAZZ_LegionTier"
local VAR_ID = "JAZZ_Legion_Tier"
local BETRAYAL_QUEST = "04_Betrayal"

local function lNoMapsActive()
	return rawget(_G, "JAZZ_NoMapsIsActive") and JAZZ_NoMapsIsActive() or false
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

function JAZZ_CountPlayerSurfaceSectorsAndMines()
	local sectors, mines = 0, 0
	for _, sector in sorted_pairs(gv_Sectors or empty_table) do
		if lSectorIsSurface(sector) and lIsPlayerSide(sector.Side) then
			sectors = sectors + 1
			if sector.Mine then
				mines = mines + 1
			end
		end
	end
	return sectors, mines
end

-- Pure formula for tests / diagnostics. Returns encoded tier 11..33 (valid set).
-- world_flip: boolean — unlocks major III (same as 04_Betrayal WorldFlip flags).
function JAZZ_ComputeLegionTierNoMaps(mines, sectors, world_flip)
	mines = mines or 0
	sectors = sectors or 0
	local major
	if world_flip then
		major = 3
	elseif mines >= 1 then
		major = 2
	else
		major = 1
	end
	local sub
	if major == 1 then
		if sectors <= 1 then
			sub = 1
		elseif sectors <= 3 then
			sub = 2
		else
			sub = 3
		end
	elseif major == 2 then
		if sectors <= 2 then
			sub = 1
		elseif sectors <= 4 then
			sub = 2
		elseif sectors <= 6 then
			sub = 3
		elseif sectors <= 8 then
			sub = 4
		else
			sub = 5
		end
	else
		if sectors <= 4 then
			sub = 1
		elseif sectors <= 7 then
			sub = 2
		else
			sub = 3
		end
	end
	return major * 10 + sub
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
	if not quest or not SetQuestVar then
		return false
	end
	SetQuestVar(quest, VAR_ID, value)
	return true
end

-- Only raises tier (never rolls back). Returns new tier or false if unchanged/inactive.
function JAZZ_UpdateLegionTierForNoMaps()
	if not lNoMapsActive() then
		return false
	end
	if not gv_Quests or not gv_Quests[QUEST_ID] then
		return false
	end
	local sectors, mines = JAZZ_CountPlayerSurfaceSectorsAndMines()
	local world_flip = JAZZ_IsWorldFlipProgressionActive()
	local computed = JAZZ_ComputeLegionTierNoMaps(mines, sectors, world_flip)
	local current = lGetCurrentTier() or 11
	if computed <= current then
		return false
	end
	if not lSetTier(computed) then
		return false
	end
	if rawget(_G, "RegenerateLegionLoot") then
		RegenerateLegionLoot()
	end
	if CombatLog and Untranslated then
		CombatLog("debug", Untranslated(string.format(
			"[JAZZ Legion Tier] NoMaps %d → %d (mines=%d sectors=%d worldflip=%s)",
			current,
			computed,
			mines,
			sectors,
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
	JAZZ_UpdateLegionTierForNoMaps()
end

function OnMsg.NewGame()
	JAZZ_UpdateLegionTierForNoMaps()
end
