-- JAZZ-STRATEGY-014: faction hostility overlay + outpost ownership.
-- Public matrix API is shared by sat + tactical (one source of truth).

g_JAZZ_FactionOverlayReady = rawget(_G, "g_JAZZ_FactionOverlayReady") or false
-- Wrap flags: top-level only (never first-touch in OnMsg).
g_JAZZ_TeamIsEnemySideWrapped = rawget(_G, "g_JAZZ_TeamIsEnemySideWrapped") or false
g_JAZZ_TeamIsEnemySideBase = rawget(_G, "g_JAZZ_TeamIsEnemySideBase") or false

local SCHEMA = 1

GameVar("gv_JAZZ_FactionOverlay", function()
	return {
		schema_version = SCHEMA,
		-- sector_id → owner faction id (player/legion/adonis/army/rebels/unknown)
		owners = {},
		-- squad UniqueId → faction id (optional; inferred when missing)
		squad_factions = {},
	}
end)

local REL_ALLY = "ally"
local REL_NEUTRAL = "neutral"
local REL_HOSTILE = "hostile"

local function lEnsureRoot()
	local root = gv_JAZZ_FactionOverlay
	if type(root) ~= "table" then
		root = {
			schema_version = SCHEMA,
			owners = {},
			squad_factions = {},
		}
		gv_JAZZ_FactionOverlay = root
	end
	root.owners = root.owners or {}
	root.squad_factions = root.squad_factions or {}
	if (root.schema_version or 0) < SCHEMA then
		root.schema_version = SCHEMA
	end
	return root
end

function JAZZ_FactionOverlayEnsureState()
	return lEnsureRoot()
end

---Normalize faction id tokens used by the overlay.
function JAZZ_NormalizeFactionId(faction)
	if not faction or faction == "" then
		return false
	end
	faction = string.lower(tostring(faction))
	if faction == "player1" or faction == "player2" or faction == "player" then
		return "player"
	end
	if faction == "enemy1" or faction == "legion" then
		return "legion"
	end
	if faction == "enemy2" then
		-- Reserved: treat as adonis unless squad tag overrides.
		return "adonis"
	end
	if faction == "ally" or faction == "militia" then
		return "rebels"
	end
	if faction == "adonis" or faction == "army" or faction == "rebels" or faction == "smugglers" then
		return faction
	end
	return faction
end

local function lWorldFlip()
	return rawget(_G, "JAZZ_IsWorldFlipProgressionActive") and JAZZ_IsWorldFlipProgressionActive() or false
end

---Static + flip-aware relation. Same API for sat and tactical.
---@return string "ally"|"neutral"|"hostile"
function JAZZ_GetFactionRelation(a, b)
	a = JAZZ_NormalizeFactionId(a)
	b = JAZZ_NormalizeFactionId(b)
	if not a or not b then
		return REL_NEUTRAL
	end
	if a == b then
		return REL_ALLY
	end

	local function pair(x, y)
		return (a == x and b == y) or (a == y and b == x)
	end
	local function involves(f)
		return a == f or b == f
	end
	local function other(f)
		return a == f and b or a
	end

	-- Player ↔ Rebels: ally
	if pair("player", "rebels") then
		return REL_ALLY
	end

	-- Adonis ↔ Army: peace
	if pair("adonis", "army") then
		return REL_NEUTRAL
	end

	-- Rebels always hostile to other AI factions
	if involves("rebels") then
		local o = other("rebels")
		if o == "legion" or o == "adonis" or o == "army" then
			return REL_HOSTILE
		end
	end

	-- Legion ↔ Adonis / Army: hostile
	if pair("legion", "adonis") or pair("legion", "army") then
		return REL_HOSTILE
	end

	-- Legion ↔ player: hostile
	if pair("legion", "player") then
		return REL_HOSTILE
	end

	-- Adonis / Army ↔ player: neutral until World Flip, then hostile
	if pair("adonis", "player") or pair("army", "player") then
		return lWorldFlip() and REL_HOSTILE or REL_NEUTRAL
	end

	-- Smugglers mini-faction: neutral to all until dedicated director
	if involves("smugglers") then
		return REL_NEUTRAL
	end

	return REL_NEUTRAL
end

function JAZZ_AreFactionsHostile(a, b)
	return JAZZ_GetFactionRelation(a, b) == REL_HOSTILE
end

function JAZZ_AreFactionsAllied(a, b)
	return JAZZ_GetFactionRelation(a, b) == REL_ALLY
end

---Infer faction from vanilla Side when no overlay tag exists.
function JAZZ_InferFactionFromSide(side)
	if side == "player1" or side == "player2" then
		return "player"
	end
	if side == "enemy1" or side == "Legion" then
		return "legion"
	end
	if side == "enemy2" then
		return "adonis"
	end
	if side == "ally" then
		return "rebels"
	end
	return "unknown"
end

function JAZZ_GetSquadFaction(squad_or_id)
	local root = lEnsureRoot()
	local squad_id = squad_or_id
	local squad = false
	if type(squad_or_id) == "table" then
		squad = squad_or_id
		squad_id = squad.UniqueId or squad.id
	else
		squad = gv_Squads and gv_Squads[squad_or_id]
	end
	if squad_id ~= nil then
		local tagged = root.squad_factions[squad_id] or root.squad_factions[tostring(squad_id)]
		if tagged then
			return JAZZ_NormalizeFactionId(tagged)
		end
	end
	if squad and squad.jazz_faction then
		return JAZZ_NormalizeFactionId(squad.jazz_faction)
	end
	-- Infer from EnemySquadDef / Name before Side (Adonis/Army often share enemy1).
	if squad then
		local def_id = squad.enemy_squad_def or squad.EnemySquadDefId or squad.Name
		if type(def_id) == "table" then
			def_id = def_id.id or def_id.Id or def_id.group
		end
		if type(def_id) == "string" then
			if string.find(def_id, "Adonis", 1, true) then
				return "adonis"
			end
			if string.find(def_id, "Army", 1, true) then
				return "army"
			end
			if string.find(def_id, "Rebel", 1, true) or string.find(def_id, "Militia", 1, true) then
				return "rebels"
			end
			if string.find(def_id, "Legion", 1, true) then
				return "legion"
			end
		end
	end
	-- Managed Legion AI squads are always legion.
	if squad and rawget(_G, "JAZZ_IsLegionAIManagedSquad") and JAZZ_IsLegionAIManagedSquad(squad) then
		return "legion"
	end
	return JAZZ_InferFactionFromSide(squad and squad.Side)
end

function JAZZ_SetSquadFaction(squad_or_id, faction)
	local root = lEnsureRoot()
	local squad_id = squad_or_id
	local squad = false
	if type(squad_or_id) == "table" then
		squad = squad_or_id
		squad_id = squad.UniqueId or squad.id
	else
		squad = gv_Squads and gv_Squads[squad_or_id]
	end
	faction = JAZZ_NormalizeFactionId(faction)
	if not faction or squad_id == nil then
		return false
	end
	root.squad_factions[squad_id] = faction
	if squad then
		squad.jazz_faction = faction
	end
	return true
end

function JAZZ_GetSectorOwnerFaction(sector_id)
	if not sector_id then
		return false
	end
	local root = lEnsureRoot()
	local tagged = root.owners[sector_id]
	if tagged then
		return JAZZ_NormalizeFactionId(tagged)
	end
	local sector = gv_Sectors and gv_Sectors[sector_id]
	return JAZZ_InferFactionFromSide(sector and sector.Side)
end

function JAZZ_SetSectorOwnerFaction(sector_id, faction, reason)
	if not sector_id then
		return false
	end
	local root = lEnsureRoot()
	faction = JAZZ_NormalizeFactionId(faction) or "unknown"
	local prev = root.owners[sector_id]
	root.owners[sector_id] = faction
	Msg("JAZZ_FactionOwnerChanged", sector_id, prev, faction, reason)
	return true
end

---Player-controlled for logistics avoid (STRATEGY-018): player1/player2 only.
function JAZZ_IsPlayerControlledSector(sector_id)
	local sector = type(sector_id) == "table" and sector_id or (gv_Sectors and gv_Sectors[sector_id])
	local side = sector and sector.Side
	return side == "player1" or side == "player2"
end

---Repair/migrate owners for managed Legion outposts (enemy1 → legion).
function JAZZ_FactionOverlayRepairOwners()
	local root = lEnsureRoot()
	local legion_root = rawget(_G, "gv_JAZZ_LegionAI")
	if type(legion_root) == "table" and type(legion_root.outposts) == "table" then
		for sector_id, outpost in pairs(legion_root.outposts) do
			if not root.owners[sector_id] then
				local sector = gv_Sectors and gv_Sectors[sector_id]
				if sector and (sector.Side == "enemy1" or sector.Side == "Legion") then
					root.owners[sector_id] = "legion"
					outpost.owner_faction = "legion"
				elseif sector and (sector.Side == "player1" or sector.Side == "player2") then
					root.owners[sector_id] = "player"
					outpost.owner_faction = "player"
				else
					root.owners[sector_id] = "unknown"
					outpost.owner_faction = outpost.owner_faction or "unknown"
				end
			elseif outpost and not outpost.owner_faction then
				outpost.owner_faction = root.owners[sector_id]
			end
		end
	end
	return root
end

-- Tactical / sat helper: should two squads fight?
function JAZZ_SquadsAreHostile(squad_a, squad_b)
	if not squad_a or not squad_b then
		return false
	end
	return JAZZ_AreFactionsHostile(JAZZ_GetSquadFaction(squad_a), JAZZ_GetSquadFaction(squad_b))
end

-- Gate: Adonis/Army should not open sat conflict vs player before World Flip.
function JAZZ_FactionMayAttackPlayerOnSat(attacker_faction)
	attacker_faction = JAZZ_NormalizeFactionId(attacker_faction)
	if attacker_faction == "legion" then
		return true
	end
	if attacker_faction == "adonis" or attacker_faction == "army" then
		return lWorldFlip()
	end
	if attacker_faction == "rebels" then
		return false
	end
	return true
end

function OnMsg.NewGame()
	JAZZ_FactionOverlayEnsureState()
end

function OnMsg.LoadGame()
	JAZZ_FactionOverlayEnsureState()
	JAZZ_FactionOverlayRepairOwners()
end

rawset(_G, "g_JAZZ_FactionOverlayReady", true)

-- Tactical hostility: one matrix with sat (STRATEGY-014 REQ-006).
-- Never bare-read engine globals (Team / g_Units) — use rawget (undefined → Assert).
local function lTeamFaction(team)
	if not team then
		return false
	end
	if team.jazz_faction then
		return JAZZ_NormalizeFactionId(team.jazz_faction)
	end
	local g_units = rawget(_G, "g_Units")
	local gv_ud = rawget(_G, "gv_UnitData")
	-- Prefer unit/squad tags over vanilla Side (all Flip factions may share enemy1).
	for _, unit in ipairs(team.units or empty_table) do
		local ud = unit
		if type(unit) ~= "table" then
			ud = (g_units and g_units[unit]) or (gv_ud and gv_ud[unit]) or false
		end
		if ud then
			if ud.jazz_faction then
				return JAZZ_NormalizeFactionId(ud.jazz_faction)
			end
			local squad_id = ud.Squad
			if squad_id and rawget(_G, "JAZZ_GetSquadFaction") then
				local f = JAZZ_GetSquadFaction(squad_id)
				if f and f ~= "unknown" then
					return f
				end
			end
		end
	end
	return JAZZ_InferFactionFromSide(team.side or team.Side)
end

local function lInstallTeamEnemyWrap()
	if rawget(_G, "g_JAZZ_TeamIsEnemySideWrapped") then
		return
	end
	local team_class = rawget(_G, "Team")
	if type(team_class) ~= "table" then
		return
	end
	local base = team_class.IsEnemySide
	if type(base) ~= "function" then
		return
	end
	rawset(_G, "g_JAZZ_TeamIsEnemySideBase", base)
	rawset(_G, "g_JAZZ_TeamIsEnemySideWrapped", true)
	team_class.IsEnemySide = function(self, other)
		local fa = lTeamFaction(self)
		local fb = lTeamFaction(other)
		if fa and fb and fa ~= "unknown" and fb ~= "unknown" then
			local rel = JAZZ_GetFactionRelation(fa, fb)
			if rel == REL_HOSTILE then
				return true
			end
			if rel == REL_ALLY or rel == REL_NEUTRAL then
				return false
			end
		end
		return g_JAZZ_TeamIsEnemySideBase(self, other)
	end
end

function OnMsg.ModsReloaded()
	JAZZ_FactionOverlayEnsureState()
	lInstallTeamEnemyWrap()
end

function OnMsg.CombatStart()
	lInstallTeamEnemyWrap()
end

-- Propagate squad jazz_faction onto units entering tactical.
function OnMsg.UnitCreated(unit)
	if not unit or unit.jazz_faction then
		return
	end
	local squad_id = unit.Squad
	if squad_id and rawget(_G, "JAZZ_GetSquadFaction") then
		local f = JAZZ_GetSquadFaction(squad_id)
		if f and f ~= "unknown" then
			unit.jazz_faction = f
		end
	end
end
