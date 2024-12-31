function SpawnWorldFlipAttackSquads()
	local adonisSquads = {"Adonis_Troops_Assault_Light", "Adonis_Troops_Assault_Heavy", "Adonis_Heavy_Troops", "Adonis_Heavy_Troops_Alt","Adonis_SpecOps_Heavy"}
	local armySquads = {"ArmySpecOps", "ArmySpecOps_alt", "ArmyAttackers_Balanced_Hard","ArmyAttackers_Balanced_Alt"}
	
	-- For each destination sector a random squad from the array is spawned starting from the source sector
	-- If the destination sector is not taken by the player the squad is instantly spawned there
	local attackLanes = {
		{
			source = "G6",
			destSectorIds = {"F7", "H7", "H8", "H9"}, -- Camp Savane, Fleatown areas
			squadDefs = adonisSquads
		},
		{
			source = "E4",
			destSectorIds = {"A2", "B2"}, -- Diamond Red
			squadDefs = adonisSquads
		},
		{
			source = "E4",
			destSectorIds = {"D7", "C7", "D8", "D10"}, -- Fosse Noir, Pantagruel areas
			squadDefs = adonisSquads
		},
		{
			source = "J8",
			destSectorIds = {"G10"}, -- Barrier Camp
			squadDefs = adonisSquads
		},
		{
			source = "K14",
			destSectorIds = {"K10", "K9", "L8"}, -- Old Diamond, Cacao areas
			squadDefs = armySquads
		},
		{
			source = "J16",
			destSectorIds = {"H14"}, -- Croc Camp
			squadDefs = armySquads
		},
		{
			source = "I20",
			destSectorIds = {"I18", "F19", "D17", "D18", "F13", "E16"}, -- I18 Wassergrab, E16 Camp Sauvage, F13 Chalet, F19 Camp Bien Chien, D17 D18 Ille Morat areas
			squadDefs = armySquads
		},
	}
	
	-- Sectors that are not flipped automatically when they are not player controlled
	local dontFlipAutomatically = { C7 = true, D8 = true, L8 = true, K9 = true, F19 = true, D17 = true }
	
	local consequentSquadDelay = const.Scale.h * 2
	local maxDelay = const.Scale.h * 12
	for _, lane in ipairs(attackLanes) do
		local attackSquad = 0
		for _, destSectorId in ipairs(lane.destSectorIds) do
			local sector = gv_Sectors[destSectorId]
			local squadDefId = lane.squadDefs[InteractionRand(#lane.squadDefs, "WorldFlip")+1]
			if IsPlayerSide(sector.Side) then
				local attackSquadId = TriggerSquadAttack.__exec({Squad = squadDefId, source_sector_id = lane.source, effect_target_sector_ids = {destSectorId}, custom_quest_id = false})
				if attackSquadId then -- Throttle attacks to prevent overlap
					SatelliteSquadWaitInSector(gv_Squads[attackSquadId], Game.CampaignTime + Min((consequentSquadDelay * attackSquad), maxDelay))
					attackSquad = attackSquad + 1
				end
			else
				if not dontFlipAutomatically[destSectorId] then
					SectorSquadDespawn.__exec({sector_id = destSectorId, Militia = true, Enemies = true})
					SectorSpawnSquad.__exec({sector_id = destSectorId, squad_def_id = squadDefId, side = "enemy1"})
				end
			end
		end
	end
	
	gv_Sectors.H4.PatrolRespawnTime = const.Scale.h * 100
end