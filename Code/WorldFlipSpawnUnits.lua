function SpawnWorldFlipAttackSquads()
	local adonisSquads = {
		"Adonis_Troops_Assault_Light",
		"Adonis_Troops_Assault_Heavy",
		"Adonis_Heavy_Troops",
		"Adonis_Heavy_Troops_Alt",
		"Adonis_SpecOps_Heavy",
	}
	local armySquads = {
		"ArmySpecOps",
		"ArmySpecOps_alt",
		"ArmyAttackers_Balanced_Hard",
		"ArmyAttackers_Balanced_Alt",
	}

	local function filterDefs(list)
		local out = {}
		for _, id in ipairs(list) do
			if EnemySquadDefs and EnemySquadDefs[id] then
				out[#out + 1] = id
			end
		end
		return out
	end

	local function laneFaction(squadDefs)
		if squadDefs == adonisSquads then
			return "adonis"
		end
		if squadDefs == armySquads then
			return "army"
		end
		-- After filterDefs, lists are new tables — match by first known id.
		local sample = squadDefs and squadDefs[1]
		if sample and string.find(sample, "Adonis", 1, true) then
			return "adonis"
		end
		if sample and string.find(sample, "Army", 1, true) then
			return "army"
		end
		return "adonis"
	end

	local function stampOwner(sector_id, faction)
		if rawget(_G, "JAZZ_SetSectorOwnerFaction") then
			JAZZ_SetSectorOwnerFaction(sector_id, faction, "world_flip")
		end
		local root = rawget(_G, "gv_JAZZ_LegionAI")
		if type(root) == "table" and root.outposts and root.outposts[sector_id] then
			root.outposts[sector_id].owner_faction = faction
			-- Legion director must stop spawning from this fort (014).
			if root.outposts[sector_id].enabled and faction ~= "legion" then
				root.outposts[sector_id].enabled = false
			end
		end
	end

	local function tagSquadsInSector(sector_id, faction)
		if not rawget(_G, "JAZZ_SetSquadFaction") then
			return
		end
		for _, squad in ipairs(GetSectorSquads(sector_id) or empty_table) do
			if squad and IsEnemySquad(squad.UniqueId) then
				JAZZ_SetSquadFaction(squad, faction)
			end
		end
	end

	adonisSquads = filterDefs(adonisSquads)
	armySquads = filterDefs(armySquads)
	if #adonisSquads == 0 and #armySquads == 0 then
		print("[JAZZ WorldFlip] no EnemySquadDefs available; skipping attack lanes")
		return
	end

	-- Destinations use vanilla HotDiamonds sector IDs (also valid under jazz-maps mainland).
	local attackLanes = {
		{
			source = "G6",
			destSectorIds = { "F7", "H7", "H8", "H9" }, -- Camp Savane, Fleatown areas
			squadDefs = adonisSquads,
		},
		{
			source = "E4",
			destSectorIds = { "A2", "B2" }, -- Diamond Red
			squadDefs = adonisSquads,
		},
		{
			source = "E4",
			destSectorIds = { "D7", "C7", "D8", "D10" }, -- Fosse Noir, Pantagruel areas
			squadDefs = adonisSquads,
		},
		{
			source = "J8",
			destSectorIds = { "G10" }, -- Barrier Camp
			squadDefs = adonisSquads,
		},
		{
			source = "K14",
			destSectorIds = { "K10", "K9", "L8" }, -- Old Diamond, Cacao areas
			squadDefs = armySquads,
		},
		{
			source = "J16",
			destSectorIds = { "H14" }, -- Croc Camp
			squadDefs = armySquads,
		},
		{
			source = "I20",
			destSectorIds = { "I18", "F19", "D17", "D18", "F13", "E16" },
			squadDefs = armySquads,
		},
	}

	local dontFlipAutomatically = {
		C7 = true,
		D8 = true,
		L8 = true,
		K9 = true,
		F19 = true,
		D17 = true,
	}

	local consequentSquadDelay = const.Scale.h * 2
	local maxDelay = const.Scale.h * 12
	for _, lane in ipairs(attackLanes) do
		if not lane.squadDefs or #lane.squadDefs == 0 then
			goto next_lane
		end
		if not gv_Sectors[lane.source] then
			print("[JAZZ WorldFlip] missing source sector " .. tostring(lane.source))
			goto next_lane
		end
		local faction = laneFaction(lane.squadDefs)
		local attackSquad = 0
		for _, destSectorId in ipairs(lane.destSectorIds) do
			local sector = gv_Sectors[destSectorId]
			if not sector then
				print("[JAZZ WorldFlip] missing dest sector " .. tostring(destSectorId))
				goto next_dest
			end
			local squadDefId = lane.squadDefs[InteractionRand(#lane.squadDefs, "WorldFlip") + 1]
			if not squadDefId or not EnemySquadDefs[squadDefId] then
				goto next_dest
			end
			if IsPlayerSide(sector.Side) then
				local attackSquadId = TriggerSquadAttack.__exec({
					Squad = squadDefId,
					source_sector_id = lane.source,
					effect_target_sector_ids = { destSectorId },
					custom_quest_id = false,
				})
				if attackSquadId then
					local attackSquadObj = gv_Squads[attackSquadId]
					if attackSquadObj and rawget(_G, "JAZZ_SetSquadFaction") then
						JAZZ_SetSquadFaction(attackSquadObj, faction)
					end
					SatelliteSquadWaitInSector(
						attackSquadObj,
						Game.CampaignTime + Min(consequentSquadDelay * attackSquad, maxDelay)
					)
					attackSquad = attackSquad + 1
				end
			elseif not dontFlipAutomatically[destSectorId] then
				SectorSquadDespawn.__exec({
					sector_id = destSectorId,
					Militia = true,
					Enemies = true,
				})
				SectorSpawnSquad.__exec({
					sector_id = destSectorId,
					squad_def_id = squadDefId,
					side = "enemy1",
				})
				-- STRATEGY-014: capturer owns the fort — do not reset to Legion.
				stampOwner(destSectorId, faction)
				tagSquadsInSector(destSectorId, faction)
			end
			::next_dest::
		end
		::next_lane::
	end

	-- Vanilla Ernie fortress is H4 (jazz-maps relocates it to I7).
	local fortress = gv_Sectors.H4 or gv_Sectors.I7
	if fortress then
		fortress.PatrolRespawnTime = const.Scale.h * 100
	end
end
