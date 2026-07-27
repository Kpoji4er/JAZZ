-- Regional strategic AI for Legion forces.
-- Static authoring lives in Region/SatelliteSector presets. Mutable state lives only here.

g_JAZZ_LegionAISpawning = false

g_JAZZ_BaseGetSatelliteIconImages = rawget(_G, "g_JAZZ_BaseGetSatelliteIconImages") or GetSatelliteIconImages
g_JAZZ_BaseGetSatelliteIconImagesSquad = rawget(_G, "g_JAZZ_BaseGetSatelliteIconImagesSquad") or GetSatelliteIconImagesSquad
g_JAZZ_BaseTFormatSquadNameColored = rawget(_G, "g_JAZZ_BaseTFormatSquadNameColored") or TFormat.SquadNameColored

local lSchemaVersion = 1

local lRegularRoles = {
	garrison = true,
	patrol = true,
	recon = true,
	qrf = true,
}

local lRoleImages = {
	major = "Mod/e6L4ECj/SquadsIcons/Enemy/legion_BASE_squad.png",
	supply = "Mod/e6L4ECj/SquadsIcons/Enemy/legion_SUPPLY_squad.png",
	shipment = "Mod/e6L4ECj/SquadsIcons/Enemy/legion_SHIPMENT_squad.png",
	recon = "Mod/e6L4ECj/SquadsIcons/Enemy/legion_RECON_squad.png",
	qrf = "Mod/e6L4ECj/SquadsIcons/Enemy/legion_QRF_squad.png",
	patrol = "Mod/e6L4ECj/SquadsIcons/Enemy/legion_PATROL_squad.png",
	garrison = "Mod/e6L4ECj/SquadsIcons/Enemy/legion_GARRISON_squad.png",
}

local lRoleCaps = {
	garrison = "GarrisonCap",
	patrol = "PatrolCap",
	recon = "ReconCap",
	qrf = "QRFCap",
}

local lRoleCosts = {
	garrison = "GarrisonCost",
	patrol = "PatrolCost",
	recon = "ReconCost",
	qrf = "QRFCost",
}

local lRoleMissions = {
	garrison = "GarrisonMissions",
	patrol = "PatrolMissions",
	recon = "ReconMissions",
	qrf = "QRFMissions",
}

local function lNewRootState()
	return {
		schema_version = lSchemaVersion,
		last_processed_hour = false,
		next_report_id = 1,
		spawn_serial = 1,
		major = {
			hq_sector = false,
			reserve = false,
			next_response_time = 0,
		},
		regions = {},
		outposts = {},
		squads = {},
		missing_defs_logged = {},
	}
end

GameVar("gv_JAZZ_LegionAI", lNewRootState)

local function lNow()
	return Game and Game.CampaignTime or 0
end

local function lHourScale()
	return const and const.Scale and const.Scale.h or 3600
end

local function lClampHeat(value)
	return Clamp(value or 0, 0, 1000)
end

local function lRegionId(region)
	return region and (region.id or region.Id)
end

local function lIsPlayerSide(side)
	return side == "player1" or side == "player2"
end

function JAZZ_IsLegionSide(side)
	return side == "enemy1" or side == "Legion"
end

local function lGetRegionPreset(region_id)
	if not Regions or not region_id then
		return false
	end
	if Regions[region_id] then
		return Regions[region_id]
	end
	for _, region in sorted_pairs(Regions) do
		if lRegionId(region) == region_id then
			return region
		end
	end
	return false
end

local function lContains(list, value)
	return list and table.find(list, value) and true or false
end

local function lConfig(region, field, fallback)
	local value = region and region[field]
	if value == nil or value == false then
		return fallback
	end
	return value
end


local function lGetSquadLookupId(context_or_squad)
	if type(context_or_squad) ~= "table" then
		return context_or_squad
	end
	local squad_id = context_or_squad.squad or context_or_squad.UniqueId or context_or_squad.id
	if type(squad_id) == "table" then
		squad_id = squad_id.UniqueId or squad_id.id
	end
	return squad_id
end

local function lGetLegionAISquadState(context_or_squad)
	local root = gv_JAZZ_LegionAI
	if type(root) ~= "table" or type(root.squads) ~= "table" then
		return false
	end
	local squad_id = lGetSquadLookupId(context_or_squad)
	if squad_id == nil then
		return false
	end
	return root.squads[squad_id] or root.squads[tostring(squad_id)] or root.squads[tonumber(squad_id)] or false
end
local function lInterval(region, field, fallback)
	return Max(lConfig(region, field, fallback), lHourScale())
end

local function lLog(message)
	if CombatLog and Untranslated then
		CombatLog("debug", Untranslated("[JAZZ Legion AI] " .. message))
	else
		print("[JAZZ Legion AI] " .. message)
	end
end

local function lManagedOutpost(region, sector_id)
	return region and region.LegionAIEnabled and lContains(region.ManagedOutposts, sector_id)
end

function JAZZ_IsLegionAIManagedGuardpost(sector_id)
	local root = gv_JAZZ_LegionAI
	if type(root) == "table" and root.outposts and root.outposts[sector_id] then
		return true
	end
	local region = GetRegionForSector and GetRegionForSector(sector_id)
	return lManagedOutpost(region, sector_id)
end

function JAZZ_IsLegionAIManagedSquad(squad_or_id)
	return not not lGetLegionAISquadState(squad_or_id)
end

local function lInitialRegionHeat(region)
	local heat = 0
	for _, sector_id in ipairs(region.Sectors or empty_table) do
		local sector = gv_Sectors and gv_Sectors[sector_id]
		heat = Max(heat, sector and sector.Heat or 0)
	end
	return lClampHeat(heat)
end

local function lEnsureOutpost(root, region, region_state, sector_id)
	local sector = gv_Sectors and gv_Sectors[sector_id]
	local controlled = sector and JAZZ_IsLegionSide(sector.Side) or false
	local outpost = root.outposts[sector_id]
	if not outpost then
		outpost = {
			sector_id = sector_id,
			region_id = lRegionId(region),
			enabled = controlled,
			supply = lConfig(region, "StartingSupply", 250),
			diamond_stock = 0,
			next_command_time = lNow() + lInterval(region, "CommandInterval", 6 * lHourScale()),
			reboot_until = 0,
			retake_targets = {},
		}
		root.outposts[sector_id] = outpost
	end
	outpost.retake_targets = outpost.retake_targets or {}
	outpost.region_id = lRegionId(region)
	region_state.outposts[sector_id] = true
	return outpost
end

local function lEnsureRegion(root, region)
	if not region or not region.LegionAIEnabled then
		return false
	end
	local region_id = lRegionId(region)
	if not region_id then
		return false
	end
	local region_state = root.regions[region_id]
	if not region_state then
		region_state = {
			region_id = region_id,
			heat = lInitialRegionHeat(region),
			intel_points = 0,
			reports = {},
			outposts = {},
			last_patrolled = {},
			next_heat_decay_time = lNow() + lInterval(region, "HeatDecayInterval", 7 * lHourScale()),
		}
		root.regions[region_id] = region_state
	end
	region_state.reports = region_state.reports or {}
	region_state.outposts = region_state.outposts or {}
	region_state.last_patrolled = region_state.last_patrolled or {}
	region_state.heat = lClampHeat(region_state.heat)

	for _, sector_id in ipairs(region.ManagedOutposts or empty_table) do
		lEnsureOutpost(root, region, region_state, sector_id)
	end

	local hq_sector = region.MajorHQSector
	if hq_sector and hq_sector ~= "" then
		root.major.hq_sector = root.major.hq_sector or hq_sector
		if root.major.reserve == false then
			root.major.reserve = lConfig(region, "MajorStartingReserve", 1000)
		end
	end
	return region_state
end

local function lAdoptLegacyPrimedSquads(root)
	for sector_id, outpost in sorted_pairs(root.outposts) do
		local guardpost = g_Guardposts and g_Guardposts[sector_id]
		local session_obj = guardpost and guardpost.session_obj
		local squad_id = session_obj and session_obj.primed_squad
		local squad = squad_id and gv_Squads and gv_Squads[squad_id]
		if squad
		and not session_obj.forced_attack
		and not root.squads[squad_id]
		then
			local region = lGetRegionPreset(outpost.region_id)
			root.squads[squad_id] = {
				squad_id = squad_id,
				region_id = outpost.region_id,
				home_sector = sector_id,
				role = "garrison",
				state = "ready_for_orders",
				missions_left = lConfig(region, "GarrisonMissions", 3),
				payload = {},
				task = false,
			}
			squad.image = lRoleImages.garrison
			session_obj.primed_squad = false
			session_obj.next_spawn_time = false
			session_obj.next_spawn_time_duration = false
			ObjModified(squad)
			local sector = gv_Sectors[sector_id]
			if sector then
				ObjModified(sector)
			end
			Msg("JAZZ_LegionAISquadManaged", squad_id, "garrison", sector_id)
		end
	end
end

local function lReconcileSquads(root)
	for squad_id, squad_state in sorted_pairs(root.squads) do
		local squad = gv_Squads and gv_Squads[squad_id]
		if not squad then
			root.squads[squad_id] = nil
		else
			local image = lRoleImages[squad_state.role]
			if image and squad.image ~= image then
				squad.image = image
				ObjModified(squad)
			end
		end
	end
end

function JAZZ_LegionAIEnsureState()
	if type(gv_JAZZ_LegionAI) ~= "table" then
		gv_JAZZ_LegionAI = lNewRootState()
	end
	local root = gv_JAZZ_LegionAI
	root.schema_version = root.schema_version or lSchemaVersion
	root.last_processed_hour = root.last_processed_hour or false
	root.next_report_id = root.next_report_id or 1
	root.spawn_serial = root.spawn_serial or 1
	root.major = root.major or { hq_sector = false, reserve = false, next_response_time = 0 }
	root.major.next_response_time = root.major.next_response_time or 0
	root.regions = root.regions or {}
	root.outposts = root.outposts or {}
	root.squads = root.squads or {}
	root.missing_defs_logged = root.missing_defs_logged or {}

	if root.schema_version ~= lSchemaVersion then
		lLog(string.format("unsupported save schema %s; feature disabled", tostring(root.schema_version)))
		return false
	end
	if not Regions or not gv_Sectors then
		return false
	end
	for _, region in sorted_pairs(Regions) do
		lEnsureRegion(root, region)
	end
	lAdoptLegacyPrimedSquads(root)
	lReconcileSquads(root)
	return root
end

function JAZZ_GetLegionAIRegionState(region_id, create)
	local root = create and JAZZ_LegionAIEnsureState() or gv_JAZZ_LegionAI
	if type(root) ~= "table" then
		return false
	end
	local state = root.regions and root.regions[region_id]
	if not state and create then
		local region = lGetRegionPreset(region_id)
		state = region and lEnsureRegion(root, region)
	end
	return state
end

local function lSectorIsSurface(sector)
	return sector and not sector.GroundSector and sector.Passability ~= "Blocked"
end

local function lSectorIsKey(sector)
	return sector
		and (sector.Guardpost
			or (sector.City and sector.City ~= "none")
			or sector.Mine
			or sector.Farm)
end

local function lSectorPriority(sector)
	if not sector then return 0 end
	if sector.Guardpost then return 400 end
	if sector.City and sector.City ~= "none" then return 300 end
	if sector.Mine then return 200 end
	if sector.Farm then return 100 end
	return 0
end

local function lPlayerSquadInSector(sector_id)
	for _, squad in sorted_pairs(gv_Squads or empty_table) do
		if lIsPlayerSide(squad.Side) and squad.CurrentSector == sector_id then
			return squad
		end
	end
	return false
end

local function lPlayerSquadNearSector(sector_id)
	for _, squad in sorted_pairs(gv_Squads or empty_table) do
		if lIsPlayerSide(squad.Side) and squad.CurrentSector then
			local sector = gv_Sectors[squad.CurrentSector]
			local distance = lSectorIsSurface(sector) and GetSectorDistance(sector_id, squad.CurrentSector)
			if distance and distance <= 1 then
				return squad
			end
		end
	end
	return false
end

local function lActiveRole(root, region_id, home_sector, role)
	for _, squad_state in sorted_pairs(root.squads) do
		if squad_state.region_id == region_id
			and (not home_sector or squad_state.home_sector == home_sector)
			and squad_state.role == role
			and squad_state.state ~= "retired"
		then
			return squad_state
		end
	end
	return false
end

local function lCountRegular(root, home_sector, role)
	local count = 0
	for _, squad_state in sorted_pairs(root.squads) do
		if squad_state.home_sector == home_sector
			and squad_state.state ~= "retired"
			and lRegularRoles[squad_state.role]
			and (not role or squad_state.role == role)
		then
			count = count + 1
		end
	end
	return count
end

local function lHasRoleTarget(root, region_id, role, target_sector)
	for _, squad_state in sorted_pairs(root.squads) do
		local task = squad_state.task
		if squad_state.region_id == region_id
			and squad_state.role == role
			and squad_state.state ~= "retired"
			and task
			and task.target_sector == target_sector
		then
			return true
		end
	end
	return false
end

local function lWeightedChoice(entries, context)
	if #entries == 0 then
		return false
	end
	table.sort(entries, function(a, b) return a.id < b.id end)
	local total = 0
	for _, entry in ipairs(entries) do
		total = total + Max(entry.weight or 0, 0)
	end
	if total <= 0 then
		return entries[1]
	end
	local roll = InteractionRand(total, "JAZZ_LegionAI_" .. context)
	for _, entry in ipairs(entries) do
		roll = roll - Max(entry.weight or 0, 0)
		if roll < 0 then
			return entry
		end
	end
	return entries[#entries]
end

local function lPatrolTarget(root, region, region_state, squad)
	local entries = {}
	for _, sector_id in ipairs(region.Sectors or empty_table) do
		local sector = gv_Sectors[sector_id]
		if sector_id ~= squad.CurrentSector
			and lSectorIsSurface(sector)
			and lSectorIsKey(sector)
			and not lIsPlayerSide(sector.Side)
		then
			local last_time = region_state.last_patrolled[sector_id] or 0
			local age_hours = Max(0, (lNow() - last_time) / lHourScale())
			entries[#entries + 1] = {
				id = sector_id,
				weight = lSectorPriority(sector) + (sector.Heat or 0) + Min(age_hours * 20, 1000),
			}
		end
	end
	local picked = lWeightedChoice(entries, "Patrol_" .. tostring(squad.UniqueId))
	return picked and picked.id
end

local function lHotSector(region)
	local best_id = false
	local best_heat = -1
	for _, sector_id in ipairs(region.Sectors or empty_table) do
		local sector = gv_Sectors[sector_id]
		local heat = sector and sector.Heat or 0
		if lSectorIsSurface(sector)
		and (heat > best_heat or (heat == best_heat and (not best_id or sector_id < best_id)))
		then
			best_id = sector_id
			best_heat = heat
		end
	end
	return best_id, best_heat
end

local function lReconTarget(region)
	local hot_sector, heat = lHotSector(region)
	if not hot_sector or heat < lConfig(region, "ReconHeatThreshold", 250) then
		return false
	end
	local entries = {}
	for _, sector_id in ipairs(region.Sectors or empty_table) do
		local sector = gv_Sectors[sector_id]
		local distance = lSectorIsSurface(sector) and GetSectorDistance(hot_sector, sector_id)
		if distance == 1 and not lIsPlayerSide(sector.Side) then
			entries[#entries + 1] = { id = sector_id, weight = 1 }
		end
	end
	local picked = lWeightedChoice(entries, "ReconStaging_" .. hot_sector)
	if picked then
		return picked.id, hot_sector
	end
	local sector = gv_Sectors[hot_sector]
	if sector and not lIsPlayerSide(sector.Side) then
		return hot_sector, hot_sector
	end
	return false
end

local function lGarrisonTarget(root, region, region_state)
	local priority = -1
	local entries = {}
	for _, sector_id in ipairs(region.Sectors or empty_table) do
		local sector = gv_Sectors[sector_id]
		if lSectorIsSurface(sector)
		and lSectorIsKey(sector)
		and JAZZ_IsLegionSide(sector.Side)
		and not lHasRoleTarget(root, region_state.region_id, "garrison", sector_id)
		then
			local sector_priority = lSectorPriority(sector)
			if sector_priority >= priority then
				if sector_priority > priority then
					priority = sector_priority
					entries = {}
				end
				entries[#entries + 1] = {
					id = sector_id,
					weight = 1 + (sector.Heat or 0),
				}
			end
		end
	end
	local picked = lWeightedChoice(entries, "Garrison_" .. region_state.region_id)
	return picked and picked.id
end

local function lRefreshRetakeTargets(region, outpost)
	for _, sector_id in ipairs(region.Sectors or empty_table) do
		local sector = gv_Sectors[sector_id]
		if lSectorIsSurface(sector) and lSectorIsKey(sector) and lIsPlayerSide(sector.Side) then
			outpost.retake_targets[sector_id] = true
		end
	end
end

local function lQRFRequest(root, region_state, outpost)
	local retake_ids = table.keys(outpost.retake_targets or empty_table, true)
	for _, sector_id in ipairs(retake_ids) do
		local sector = gv_Sectors[sector_id]
		if sector and lIsPlayerSide(sector.Side)
		and not lHasRoleTarget(root, region_state.region_id, "qrf", sector_id)
		then
			return {
				task_type = "retake",
				target_sector = sector_id,
			}
		end
		outpost.retake_targets[sector_id] = nil
	end

	local report_ids = table.keys(region_state.reports or empty_table, true)
	for _, report_id in ipairs(report_ids) do
		local report = region_state.reports[report_id]
		if report and report.delivered and not report.consumed and report.expires_at > lNow() then
			return {
				task_type = "qrf",
				target_sector = report.target_sector,
				report_id = report_id,
			}
		end
	end
	return false
end

local function lRoutePath(squad, target_sector)
	if not squad or not squad.CurrentSector or not target_sector then
		return false
	end
	if squad.CurrentSector == target_sector then
		return {}
	end
	return GenerateRouteDijkstra(
		squad.CurrentSector,
		target_sector,
		false,
		squad.units,
		"land_water",
		nil,
		squad.Side
	)
end

local function lSetRoute(squad, target_sector)
	local route = lRoutePath(squad, target_sector)
	if not route then
		return false
	end
	if #route == 0 then
		return "arrived"
	end
	NetSyncEvent("AssignSatelliteSquadRoute", squad.UniqueId, { route })
	return true
end

local function lNonEmptyList(primary, fallback)
	if primary and #primary > 0 then
		return primary
	end
	if fallback and #fallback > 0 then
		return fallback
	end
	return empty_table
end

local function lRoleSquadList(region, sector, role)
	if lRegularRoles[role] and not sector then
		return empty_table
	end
	if role == "garrison" then
		return lNonEmptyList(sector.EnemySquadsGarrisonList, sector.ExtraDefenderSquads)
	elseif role == "patrol" then
		return lNonEmptyList(sector.EnemySquadsPatroolList, sector.EnemySquadsList)
	elseif role == "recon" then
		return lNonEmptyList(sector.EnemySquadsReconList, sector.EnemySquadsList)
	elseif role == "qrf" then
		return lNonEmptyList(sector.EnemySquadsQRFList, sector.StrongEnemySquadsList)
	elseif role == "supply" then
		return region.SupplySquads
	elseif role == "shipment" then
		return region.ShipmentSquads
	elseif role == "major" then
		return region.MajorResponseSquads
	end
	return false
end

local function lPickSquadDef(list, context)
	local valid = {}
	for _, squad_def_id in ipairs(list or empty_table) do
		if EnemySquadDefs and EnemySquadDefs[squad_def_id] then
			valid[#valid + 1] = squad_def_id
		end
	end
	if #valid == 0 then
		return false
	end
	local index = InteractionRand(#valid, "JAZZ_LegionAI_SquadDef_" .. context) + 1
	return valid[index]
end

local function lEnsureDiamondCargo(squad)
	if squad.diamond_briefcase then
		return true
	end
	local carrier_id = squad.units and squad.units[1]
	local carrier = carrier_id and gv_UnitData[carrier_id]
	if not carrier then
		return false
	end
	local briefcase = PlaceInventoryItem("DiamondBriefcase")
	if not briefcase then
		return false
	end
	briefcase.drop_chance = 100
	carrier:AddItem("Inventory", briefcase)
	squad.diamond_briefcase = true
	return true
end

local function lSpawnManaged(root, region, home_sector, role, origin_sector, missions_left, payload)
	local source_sector = gv_Sectors[home_sector]
	local list = lRoleSquadList(region, source_sector, role)
	local squad_def_id = lPickSquadDef(list, role .. "_" .. home_sector)
	if not squad_def_id then
		local diagnostic_key = string.format("%s:%s", role, home_sector)
		if not root.missing_defs_logged[diagnostic_key] then
			root.missing_defs_logged[diagnostic_key] = true
			lLog(string.format("no valid squad definition for %s at %s; spawn disabled", role, home_sector))
		end
		return false
	end

	local serial = root.spawn_serial
	root.spawn_serial = serial + 1
	local base_session_id = string.format("JAZZLegionAI_%s_%s_%d", role, home_sector, serial)
	g_JAZZ_LegionAISpawning = true
	local squad_id = GenerateEnemySquad(squad_def_id, origin_sector, base_session_id, nil, "enemy1")
	g_JAZZ_LegionAISpawning = false
	local squad = squad_id and gv_Squads[squad_id]
	if not squad then
		return false
	end
	if role == "shipment" and not lEnsureDiamondCargo(squad) then
		lLog("shipment spawned without a valid DiamondBriefcase carrier; squad retired")
		RemoveSquad(squad)
		return false
	end

	squad.image = lRoleImages[role] or squad.image
	ObjModified(squad)
	root.squads[squad_id] = {
		squad_id = squad_id,
		region_id = lRegionId(region),
		home_sector = home_sector,
		role = role,
		state = "ready_for_orders",
		missions_left = missions_left or 1,
		payload = payload or {},
		task = false,
	}
	Msg("JAZZ_LegionAISquadManaged", squad_id, role, home_sector)
	return squad_id, root.squads[squad_id]
end

local function lRetireSquad(root, squad_id)
	local squad_state = root.squads[squad_id]
	local squad = gv_Squads[squad_id]
	if squad_state then
		squad_state.state = "retired"
	end
	if squad then
		RemoveSquad(squad)
	else
		root.squads[squad_id] = nil
	end
end

local function lBeginReturn(root, squad, squad_state)
	if not squad or not squad_state then
		return false
	end
	if squad.CurrentSector == squad_state.home_sector then
		lRetireSquad(root, squad.UniqueId)
		return true
	end
	squad_state.task = {
		task_type = "return",
		target_sector = squad_state.home_sector,
	}
	squad_state.state = "returning"
	ObjModified(squad)
	local routed = lSetRoute(squad, squad_state.home_sector)
	if not routed then
		squad_state.state = "orphaned"
		ObjModified(squad)
		return false
	elseif routed == "arrived" then
		lRetireSquad(root, squad.UniqueId)
	end
	return true
end

local function lCompleteRegularTask(root, squad, squad_state)
	squad_state.missions_left = Max((squad_state.missions_left or 1) - 1, 0)
	squad_state.task = false
	if squad_state.missions_left <= 0 then
		return lBeginReturn(root, squad, squad_state)
	end
	squad_state.state = "ready_for_orders"
	ObjModified(squad)
	return true
end

local function lOnSquadArrived(root, squad, squad_state)
	local task = squad_state and squad_state.task
	if not squad or not squad_state or not task then
		return
	end
	if task.target_sector and squad.CurrentSector ~= task.target_sector then
		return
	end

	if task.task_type == "return" then
		if squad_state.role == "supply" and (squad_state.payload.supply or 0) > 0 then
			root.major.reserve = (root.major.reserve or 0) + squad_state.payload.supply
			squad_state.payload.supply = 0
		end
		lRetireSquad(root, squad.UniqueId)
	elseif squad_state.role == "patrol" then
		local region_state = root.regions[squad_state.region_id]
		region_state.last_patrolled[squad.CurrentSector] = lNow()
		lCompleteRegularTask(root, squad, squad_state)
	elseif squad_state.role == "recon" then
		squad_state.state = "working"
		task.observe_until = lNow() + lConfig(lGetRegionPreset(squad_state.region_id), "ReconObservationTime", 3 * lHourScale())
	elseif squad_state.role == "supply" then
		local outpost = root.outposts[squad_state.home_sector]
		local region = lGetRegionPreset(squad_state.region_id)
		local outpost_sector = outpost and gv_Sectors[outpost.sector_id]
		local delivered = outpost
			and outpost.enabled
			and outpost_sector
			and JAZZ_IsLegionSide(outpost_sector.Side)
		if delivered then
			outpost.supply = Min(
				outpost.supply + (squad_state.payload.supply or 0),
				lConfig(region, "SupplyCapacity", 500)
			)
			squad_state.payload.supply = 0
		end
		squad_state.home_sector = root.major.hq_sector
		lBeginReturn(root, squad, squad_state)
	elseif squad_state.role == "shipment" then
		local hq = gv_Sectors[root.major.hq_sector]
		if hq and JAZZ_IsLegionSide(hq.Side) then
			root.major.reserve = (root.major.reserve or 0) + (squad_state.payload.diamonds or 0)
			squad_state.payload.diamonds = 0
			lRetireSquad(root, squad.UniqueId)
		else
			squad_state.state = "working"
		end
	elseif squad_state.role == "garrison" then
		squad_state.state = "working"
		task.hold_until = lNow() + lInterval(lGetRegionPreset(squad_state.region_id), "CommandInterval", 6 * lHourScale())
	elseif squad_state.role == "qrf" or squad_state.role == "major" then
		squad_state.state = "working"
		task.hold_until = lNow() + lInterval(lGetRegionPreset(squad_state.region_id), "CommandInterval", 6 * lHourScale())
	end
	if squad_state.state == "working" then
		ObjModified(squad)
	end
end

local function lAssignTask(root, region, region_state, outpost, squad, squad_state, request)
	if not request or not request.target_sector then
		return false
	end
	local task_type = request.task_type or squad_state.role
	squad_state.task = {
		task_type = task_type,
		target_sector = request.target_sector,
		observed_sector = request.observed_sector,
		report_id = request.report_id,
	}
	squad_state.state = "en_route"
	local routed = lSetRoute(squad, request.target_sector)
	if not routed then
		squad_state.task = false
		squad_state.state = "ready_for_orders"
		return false
	end
	if task_type == "retake" then
		outpost.retake_targets[request.target_sector] = nil
	elseif request.report_id then
		local report = region_state.reports[request.report_id]
		if report then
			report.consumed = true
		end
	end
	ObjModified(squad)
	Msg("JAZZ_LegionAITaskAssigned", squad.UniqueId, task_type, request.target_sector)
	if routed == "arrived" then
		lOnSquadArrived(root, squad, squad_state)
	end
	return true
end

local function lRoleRequest(root, region, region_state, outpost, squad, role)
	if role == "patrol" then
		local target = lPatrolTarget(root, region, region_state, squad)
		return target and { task_type = "patrol", target_sector = target }
	elseif role == "recon" then
		local staging, observed = lReconTarget(region)
		return staging and {
			task_type = "recon",
			target_sector = staging,
			observed_sector = observed,
		}
	elseif role == "qrf" then
		return lQRFRequest(root, region_state, outpost)
	elseif role == "garrison" then
		local target = lGarrisonTarget(root, region, region_state)
		return target and { task_type = "garrison", target_sector = target }
	end
	return false
end

local function lAssignReadySquads(root, region, region_state, outpost)
	for squad_id, squad_state in sorted_pairs(root.squads) do
		if squad_state.home_sector == outpost.sector_id
		and lRegularRoles[squad_state.role]
		and squad_state.state == "ready_for_orders"
		then
			local squad = gv_Squads[squad_id]
			if squad and not IsSquadTravelling(squad, "skip_tick_pass") and not IsConflictMode(squad.CurrentSector) then
				if squad_state.missions_left <= 0 then
					lBeginReturn(root, squad, squad_state)
				else
					local request = lRoleRequest(root, region, region_state, outpost, squad, squad_state.role)
					lAssignTask(root, region, region_state, outpost, squad, squad_state, request)
				end
			end
		end
	end
end

local function lSpawnRegularRole(root, region, region_state, outpost, role)
	local total_cap = lConfig(region, "RegularSquadCap", 6)
	local role_cap = lConfig(region, lRoleCaps[role], 0)
	if lCountRegular(root, outpost.sector_id) >= total_cap
	or lCountRegular(root, outpost.sector_id, role) >= role_cap
	then
		return false
	end
	local cost = lConfig(region, lRoleCosts[role], 0)
	if outpost.supply < cost then
		return false
	end

	local mock_squad = { CurrentSector = outpost.sector_id, UniqueId = root.spawn_serial }
	local request = lRoleRequest(root, region, region_state, outpost, mock_squad, role)
	if not request then
		return false
	end

	local missions = lConfig(region, lRoleMissions[role], 1)
	local squad_id, squad_state = lSpawnManaged(
		root,
		region,
		outpost.sector_id,
		role,
		outpost.sector_id,
		missions
	)
	local squad = squad_id and gv_Squads[squad_id]
	if not squad or not lAssignTask(root, region, region_state, outpost, squad, squad_state, request) then
		if squad then lRetireSquad(root, squad_id) end
		return false
	end
	outpost.supply = outpost.supply - cost
	return true
end

local function lTrySupplyConvoy(root, region, region_state, outpost)
	if lActiveRole(root, region_state.region_id, outpost.sector_id, "supply") then
		return false
	end
	local capacity = lConfig(region, "SupplyCapacity", 500)
	local trigger = MulDivRound(capacity, lConfig(region, "SupplyConvoyTriggerPercent", 40), 100)
	local cargo = lConfig(region, "SupplyConvoyCargo", 100)
	if outpost.supply >= trigger or (root.major.reserve or 0) < cargo then
		return false
	end
	local hq_sector = root.major.hq_sector
	local hq = hq_sector and gv_Sectors[hq_sector]
	if not hq or not JAZZ_IsLegionSide(hq.Side) then
		return false
	end
	local squad_id, squad_state = lSpawnManaged(
		root, region, outpost.sector_id, "supply", hq_sector, 1, { supply = cargo }
	)
	local squad = squad_id and gv_Squads[squad_id]
	if not squad then return false end
	squad_state.task = { task_type = "supply", target_sector = outpost.sector_id }
	squad_state.state = "en_route"
	local routed = lSetRoute(squad, outpost.sector_id)
	if not routed then
		lRetireSquad(root, squad_id)
		return false
	end
	root.major.reserve = root.major.reserve - cargo
	ObjModified(squad)
	if routed == "arrived" then lOnSquadArrived(root, squad, squad_state) end
	return true
end

local function lTryDiamondShipment(root, region, region_state, outpost)
	if lActiveRole(root, region_state.region_id, outpost.sector_id, "shipment") then
		return false
	end
	local threshold = lConfig(region, "DiamondShipmentThreshold", 50)
	if outpost.diamond_stock < threshold then
		return false
	end
	local hq_sector = root.major.hq_sector
	local hq = hq_sector and gv_Sectors[hq_sector]
	if not hq or not JAZZ_IsLegionSide(hq.Side) then
		return false
	end
	local squad_id, squad_state = lSpawnManaged(
		root, region, outpost.sector_id, "shipment", outpost.sector_id, 1, { diamonds = threshold }
	)
	local squad = squad_id and gv_Squads[squad_id]
	if not squad then return false end
	squad_state.task = { task_type = "shipment", target_sector = hq_sector }
	squad_state.state = "en_route"
	local routed = lSetRoute(squad, hq_sector)
	if not routed then
		lRetireSquad(root, squad_id)
		return false
	end
	outpost.diamond_stock = outpost.diamond_stock - threshold
	ObjModified(squad)
	if routed == "arrived" then lOnSquadArrived(root, squad, squad_state) end
	return true
end

local function lCompleteWorkingTasks(root, region, region_state, outpost)
	for squad_id, squad_state in sorted_pairs(root.squads) do
		local squad = gv_Squads[squad_id]
		local task = squad_state.task
		if squad
		and squad_state.home_sector == outpost.sector_id
		and squad_state.state == "working"
		and task
		and task.hold_until
		and task.hold_until <= lNow()
		then
			local target = gv_Sectors[task.target_sector]
			if squad_state.role == "garrison" and target and JAZZ_IsLegionSide(target.Side) then
				lCompleteRegularTask(root, squad, squad_state)
			elseif squad_state.role == "qrf" then
				if target and not lIsPlayerSide(target.Side) and not lPlayerSquadInSector(target.Id) then
					lCompleteRegularTask(root, squad, squad_state)
				elseif task.hold_until + lInterval(region, "CommandInterval", 6 * lHourScale()) <= lNow() then
					lCompleteRegularTask(root, squad, squad_state)
				end
			end
		end
	end
end

local function lRestoreOrphans(root, outpost)
	for squad_id, squad_state in sorted_pairs(root.squads) do
		if squad_state.home_sector == outpost.sector_id
		and lRegularRoles[squad_state.role]
		and squad_state.state == "orphaned"
		then
			squad_state.task = false
			squad_state.state = "ready_for_orders"
			local squad = gv_Squads[squad_id]
			if squad then ObjModified(squad) end
		end
	end
end

local function lRunCommandWindow(root, region, region_state, outpost)
	local sector = gv_Sectors[outpost.sector_id]
	outpost.enabled = sector and JAZZ_IsLegionSide(sector.Side) or false
	if not outpost.enabled or outpost.reboot_until > lNow() then
		return
	end

	lRestoreOrphans(root, outpost)
	lRefreshRetakeTargets(region, outpost)
	lCompleteWorkingTasks(root, region, region_state, outpost)
	lAssignReadySquads(root, region, region_state, outpost)

	-- Emergency/territorial work is filled before routine reconnaissance and patrol.
	lSpawnRegularRole(root, region, region_state, outpost, "qrf")
	while lSpawnRegularRole(root, region, region_state, outpost, "garrison") do end
	lSpawnRegularRole(root, region, region_state, outpost, "recon")
	while lSpawnRegularRole(root, region, region_state, outpost, "patrol") do end

	lTrySupplyConvoy(root, region, region_state, outpost)
	lTryDiamondShipment(root, region, region_state, outpost)
end

local function lParalyzeOutpost(root, outpost)
	outpost.enabled = false
	for squad_id, squad_state in sorted_pairs(root.squads) do
		local squad = gv_Squads[squad_id]
		if squad_state.home_sector == outpost.sector_id and squad then
			if lRegularRoles[squad_state.role] then
				squad_state.state = "orphaned"
				ObjModified(squad)
				if IsSquadTravelling(squad, "skip_tick_pass") then
					NetSyncEvent("SquadCancelTravel", squad_id)
				end
			elseif squad_state.role == "supply" then
				squad_state.home_sector = root.major.hq_sector
				lBeginReturn(root, squad, squad_state)
			end
		end
	end
end

local function lTickRecon(root)
	for squad_id, squad_state in sorted_pairs(root.squads) do
		local squad = gv_Squads[squad_id]
		local task = squad_state.task
		if squad
		and squad_state.role == "recon"
		and squad_state.state == "working"
		and task
		and task.task_type == "recon"
		then
			local spotted = lPlayerSquadNearSector(squad.CurrentSector)
			if spotted then
				task.report = {
					target_sector = spotted.CurrentSector,
					observed_at = lNow(),
				}
			end
			if spotted or (task.observe_until and task.observe_until <= lNow()) then
				if not task.report then
					local observed = task.observed_sector or squad.CurrentSector
					local observed_sector = gv_Sectors[observed]
					local region = lGetRegionPreset(squad_state.region_id)
					local reduction = lConfig(region, "ReconNoContactHeatReduction", 50)
					if observed_sector and reduction > 0 then
						local previous_heat = observed_sector.Heat or 0
						observed_sector.Heat = lClampHeat(previous_heat - reduction)
						task.heat_reduced = previous_heat - observed_sector.Heat
						ObjModified(observed_sector)
					end
					task.report = {
						target_sector = observed,
						observed_at = lNow(),
						generic = true,
						heat_reduced = task.heat_reduced or 0,
					}
				end
				task.task_type = "return_with_intel"
				task.target_sector = squad_state.home_sector
				squad_state.state = "returning"
				local routed = lSetRoute(squad, squad_state.home_sector)
				if not routed then
					squad_state.state = "orphaned"
				end
				ObjModified(squad)
				if routed == "arrived" then
					lOnSquadArrived(root, squad, squad_state)
				end
			end
		end
	end
end

local function lDeliverReconReport(root, squad, squad_state)
	local task = squad_state.task
	if not task or task.task_type ~= "return_with_intel" or squad.CurrentSector ~= squad_state.home_sector then
		return false
	end
	local region = lGetRegionPreset(squad_state.region_id)
	local region_state = root.regions[squad_state.region_id]
	local report = task.report
	if report then
		local report_id = root.next_report_id
		root.next_report_id = report_id + 1
		report.id = report_id
		report.delivered = true
		report.consumed = false
		report.expires_at = lNow() + lConfig(region, "ReportExpiryTime", 24 * lHourScale())
		report.source_squad = squad.UniqueId
		region_state.reports[report_id] = report
		region_state.intel_points = region_state.intel_points + (report.generic and 10 or 25)
	end
	return lCompleteRegularTask(root, squad, squad_state)
end

local function lExpireReports(region_state)
	for report_id, report in sorted_pairs(region_state.reports) do
		if not report or report.expires_at <= lNow() then
			region_state.reports[report_id] = nil
		end
	end
end

local function lTickEconomyAndHeat(root, region, region_state)
	local legion_cities = 0
	local legion_farms = 0
	local legion_mines = 0
	for _, sector_id in ipairs(region.Sectors or empty_table) do
		local sector = gv_Sectors[sector_id]
		if sector and JAZZ_IsLegionSide(sector.Side) then
			if sector.City and sector.City ~= "none" then legion_cities = legion_cities + 1 end
			if sector.Farm then legion_farms = legion_farms + 1 end
			if sector.Mine then legion_mines = legion_mines + 1 end
		end
	end

	for sector_id in sorted_pairs(region_state.outposts) do
		local outpost = root.outposts[sector_id]
		local sector = gv_Sectors[sector_id]
		if outpost.enabled and sector and JAZZ_IsLegionSide(sector.Side) then
			local income = lConfig(region, "PassiveSupplyPerHour", 5)
				+ legion_cities * lConfig(region, "CitySupplyBonus", 2)
				+ legion_farms * lConfig(region, "FarmSupplyBonus", 3)
			outpost.supply = Min(
				outpost.supply + income,
				lConfig(region, "SupplyCapacity", 500)
			)
			outpost.diamond_stock = outpost.diamond_stock
				+ legion_mines * lConfig(region, "MineDiamondPerHour", 5)
		end
	end

	if region_state.next_heat_decay_time <= lNow() then
		local interval = lInterval(region, "HeatDecayInterval", 7 * lHourScale())
		local cycles = 1 + math.floor((lNow() - region_state.next_heat_decay_time) / interval)
		region_state.heat = lClampHeat(
			region_state.heat - lConfig(region, "RegionHeatDecay", 5) * cycles
		)
		if JAZZ_DecaySectorHeat then
			JAZZ_DecaySectorHeat(region, lConfig(region, "SectorHeatDecay", 10) * cycles)
		end
		region_state.next_heat_decay_time = region_state.next_heat_decay_time + interval * cycles
	end
	lExpireReports(region_state)
end

local function lMajorTarget(region)
	local best_id = false
	local best_score = -1
	for _, sector_id in ipairs(region.Sectors or empty_table) do
		local sector = gv_Sectors[sector_id]
		local player_squad = sector and lPlayerSquadInSector(sector_id)
		local player_controlled = sector and lIsPlayerSide(sector.Side)
		if lSectorIsSurface(sector) and (player_controlled or player_squad) then
			local score = (sector.Heat or 0)
				+ lSectorPriority(sector)
				+ (player_controlled and 1000 or 0)
			if score > best_score or (score == best_score and (not best_id or sector_id < best_id)) then
				best_id = sector_id
				best_score = score
			end
		end
	end
	return best_id
end

local function lTryMajorResponse(root, region, region_state)
	if region_state.heat < lConfig(region, "MajorResponseHeat", 800)
	or root.major.next_response_time > lNow()
	or lActiveRole(root, region_state.region_id, false, "major")
	then
		return false
	end
	local cost = lConfig(region, "MajorResponseCost", 200)
	if (root.major.reserve or 0) < cost then
		return false
	end
	local hq_sector = root.major.hq_sector
	local hq = hq_sector and gv_Sectors[hq_sector]
	local target_sector = lMajorTarget(region)
	if not hq or not JAZZ_IsLegionSide(hq.Side) or not target_sector then
		return false
	end

	local squad_id, squad_state = lSpawnManaged(
		root,
		region,
		hq_sector,
		"major",
		hq_sector,
		1,
		{}
	)
	local squad = squad_id and gv_Squads[squad_id]
	if not squad then
		return false
	end
	squad_state.task = {
		task_type = "major_response",
		target_sector = target_sector,
	}
	squad_state.state = "en_route"
	local routed = lSetRoute(squad, target_sector)
	if not routed then
		lRetireSquad(root, squad_id)
		return false
	end
	root.major.reserve = root.major.reserve - cost
	ObjModified(squad)
	root.major.next_response_time = lNow()
		+ lConfig(region, "MajorResponseCooldown", 72 * lHourScale())
	if routed == "arrived" then
		lOnSquadArrived(root, squad, squad_state)
	end
	Msg("JAZZ_LegionAIMajorResponse", squad_id, target_sector)
	return true
end

local function lTickMajor(root)
	for squad_id, squad_state in sorted_pairs(root.squads) do
		if squad_state.role == "major" then
			local squad = gv_Squads[squad_id]
			local task = squad_state.task
			if squad and squad_state.state == "working" and task and task.hold_until
			and task.hold_until <= lNow()
			and not IsConflictMode(squad.CurrentSector)
			then
				lBeginReturn(root, squad, squad_state)
			elseif squad and squad_state.state == "orphaned" then
				lBeginReturn(root, squad, squad_state)
			end
		end
	end
end

local function lSetOutpostControlState(root, region, outpost)
	local sector = gv_Sectors[outpost.sector_id]
	local controlled = sector and JAZZ_IsLegionSide(sector.Side) or false
	if controlled == outpost.enabled then
		return
	end
	if controlled then
		outpost.enabled = true
		outpost.reboot_until = lNow()
			+ lConfig(region, "OutpostRebootDelay", 12 * lHourScale())
		outpost.next_command_time = Max(outpost.next_command_time or 0, outpost.reboot_until)
		Msg("JAZZ_LegionAIOutpostRecovered", outpost.sector_id, outpost.reboot_until)
	else
		lParalyzeOutpost(root, outpost)
		Msg("JAZZ_LegionAIOutpostLost", outpost.sector_id)
	end
end

local function lProcessOutpostWindow(root, region, region_state, outpost)
	lSetOutpostControlState(root, region, outpost)
	if not outpost.enabled or outpost.reboot_until > lNow() then
		return
	end
	local interval = lInterval(region, "CommandInterval", 6 * lHourScale())
	if not outpost.next_command_time then
		outpost.next_command_time = lNow() + interval
		return
	end
	if outpost.next_command_time > lNow() then
		return
	end
	lRunCommandWindow(root, region, region_state, outpost)
	repeat
		outpost.next_command_time = outpost.next_command_time + interval
	until outpost.next_command_time > lNow()
end

function JAZZ_LegionAIProcessHour()
	local root = JAZZ_LegionAIEnsureState()
	if not root then
		return false
	end
	local current_hour = DivRound(lNow(), lHourScale())
	if root.last_processed_hour == current_hour then
		return false
	end
	root.last_processed_hour = current_hour

	lTickRecon(root)
	lTickMajor(root)
	for region_id, region_state in sorted_pairs(root.regions) do
		local region = lGetRegionPreset(region_id)
		if region and region.LegionAIEnabled then
			lTickEconomyAndHeat(root, region, region_state)
			for sector_id in sorted_pairs(region_state.outposts) do
				local outpost = root.outposts[sector_id]
				if outpost then
					lProcessOutpostWindow(root, region, region_state, outpost)
				end
			end
			lTryMajorResponse(root, region, region_state)
		end
	end
	return true
end

function JAZZ_LegionAISetRegionHeat(region_id, value)
	local region_state = JAZZ_GetLegionAIRegionState(region_id, true)
	if not region_state then
		return false
	end
	region_state.heat = lClampHeat(value)
	return region_state.heat
end

function JAZZ_LegionAIChangeRegionHeat(region_id, amount)
	local region_state = JAZZ_GetLegionAIRegionState(region_id, true)
	if not region_state then
		return false
	end
	region_state.heat = lClampHeat(region_state.heat + (amount or 0))
	return region_state.heat
end

function JAZZ_LegionAIGetDiagnostics()
	local root = JAZZ_LegionAIEnsureState()
	if not root then
		return {
			enabled = false,
			reason = "state unavailable",
		}
	end
	local diagnostics = {
		enabled = true,
		schema_version = root.schema_version,
		major = table.copy(root.major),
		regions = {},
	}
	for region_id, region_state in sorted_pairs(root.regions) do
		local region = lGetRegionPreset(region_id)
		local region_data = {
			heat = region_state.heat,
			intel_points = region_state.intel_points,
			reports = table.count(region_state.reports),
			outposts = {},
			squads = {},
			caps = {
				regular = lConfig(region, "RegularSquadCap", 6),
				garrison = lConfig(region, "GarrisonCap", 2),
				patrol = lConfig(region, "PatrolCap", 2),
				recon = lConfig(region, "ReconCap", 1),
				qrf = lConfig(region, "QRFCap", 1),
			},
			costs = {
				garrison = lConfig(region, "GarrisonCost", 180),
				patrol = lConfig(region, "PatrolCost", 90),
				recon = lConfig(region, "ReconCost", 50),
				qrf = lConfig(region, "QRFCost", 140),
				supply_convoy = lConfig(region, "SupplyConvoyCargo", 150),
				major = lConfig(region, "MajorResponseCost", 300),
			},
			active_counts = { regular = 0 },
		}
		for sector_id in sorted_pairs(region_state.outposts) do
			local outpost = root.outposts[sector_id]
			region_data.outposts[sector_id] = outpost and {
				enabled = outpost.enabled,
				supply = outpost.supply,
				diamond_stock = outpost.diamond_stock,
				next_command_time = outpost.next_command_time,
				reboot_until = outpost.reboot_until,
				supply_capacity = lConfig(region, "SupplyCapacity", 500),
			} or false
		end
		for squad_id, squad_state in sorted_pairs(root.squads) do
			if squad_state.region_id == region_id then
				local role = squad_state.role or "unknown"
				region_data.active_counts[role] = (region_data.active_counts[role] or 0) + 1
				if lRegularRoles[role] then
					region_data.active_counts.regular = region_data.active_counts.regular + 1
				end
				region_data.squads[squad_id] = {
					role = squad_state.role,
					state = squad_state.state,
					home_sector = squad_state.home_sector,
					missions_left = squad_state.missions_left,
					task = squad_state.task and table.copy(squad_state.task) or false,
				}
			end
		end
		diagnostics.regions[region_id] = region_data
	end
	return diagnostics
end

-- The seven JAZZ role assets are final 64x64 PNGs and intentionally have no
-- vanilla `_2`/`_s` companions. Resolve by managed role, not potentially stale
-- SatelliteSquad.image, so save/load and ReloadLua keep the correct icon.
function JAZZ_GetLegionAISquadIcon(squad_or_id)
	local squad_state = lGetLegionAISquadState(squad_or_id)
	return squad_state and lRoleImages[squad_state.role] or false
end

function JAZZ_LegionAIGetSatelliteIconImages(context)
	local icon = context and JAZZ_GetLegionAISquadIcon(context)
	if icon then
		return icon, false
	end
	return g_JAZZ_BaseGetSatelliteIconImages(context)
end

function JAZZ_LegionAIGetSatelliteIconImagesSquad(squad, from_ui)
	local icon = squad and JAZZ_GetLegionAISquadIcon(squad)
	if icon then
		return icon
	end
	return g_JAZZ_BaseGetSatelliteIconImagesSquad(squad, from_ui)
end

local lRoleDisplayNames = {
	garrison = T(890000000001424, "Garrison"),
	patrol = T(890000000001425, "Patrol"),
	recon = T(890000000001426, "Recon"),
	qrf = T(890000000001427, "QRF"),
	major = T(890000000001428, "Major response"),
	supply = T(890000000001429, "Supply convoy"),
	shipment = T(890000000001430, "Diamond convoy"),
}

function JAZZ_GetLegionAISquadTaskText(squad_or_id)
	local squad_state = lGetLegionAISquadState(squad_or_id)
	if not squad_state then
		return false
	end

	local role = lRoleDisplayNames[squad_state.role] or Untranslated(tostring(squad_state.role))
	local task = squad_state.task
	local target = task and task.target_sector
	if squad_state.state == "orphaned" then
		return T{890000000001431, "<role> — outpost <home> lost; no contact", role = role, home = Untranslated(squad_state.home_sector)}
	elseif squad_state.state == "ready_for_orders" then
		return T{890000000001432, "<role> — awaiting orders from outpost <home>", role = role, home = Untranslated(squad_state.home_sector)}
	elseif squad_state.state == "returning" then
		if task and task.task_type == "return_with_intel" then
			return T{890000000001433, "<role> — returning with intelligence to <home>", role = role, home = Untranslated(squad_state.home_sector)}
		end
		return T{890000000001434, "<role> — returning to base <home>", role = role, home = Untranslated(squad_state.home_sector)}
	elseif not task then
		return T{890000000001435, "<role> — awaiting assignment", role = role}
	elseif squad_state.role == "garrison" then
		if squad_state.state == "working" then
			return T{890000000001436, "<role> — holding sector <target>", role = role, target = Untranslated(target or "?")}
		end
		return T{890000000001437, "<role> — moving to hold sector <target>", role = role, target = Untranslated(target or "?")}
	elseif squad_state.role == "patrol" then
		return T{890000000001438, "<role> — patrolling key sites; next: <target>", role = role, target = Untranslated(target or "?")}
	elseif squad_state.role == "recon" then
		local observed = task.observed_sector or target or "?"
		if squad_state.state == "working" then
			return T{890000000001439, "<role> — observing area <target>", role = role, target = Untranslated(observed)}
		end
		return T{890000000001440, "<role> — moving to observe area <target>", role = role, target = Untranslated(observed)}
	elseif squad_state.role == "qrf" then
		if task.task_type == "retake" then
			return T{890000000001441, "<role> — retaking sector <target>", role = role, target = Untranslated(target or "?")}
		end
		return T{890000000001442, "<role> — responding to intelligence in sector <target>", role = role, target = Untranslated(target or "?")}
	elseif squad_state.role == "major" then
		return T{890000000001443, "<role> — assaulting sector <target>", role = role, target = Untranslated(target or "?")}
	elseif squad_state.role == "supply" then
		return T{890000000001444, "<role> — delivering supplies to <target>", role = role, target = Untranslated(target or "?")}
	elseif squad_state.role == "shipment" then
		return T{890000000001445, "<role> — delivering diamonds to HQ <target>", role = role, target = Untranslated(target or "?")}
	end
	return T{890000000001446, "<role> — task in sector <target>", role = role, target = Untranslated(target or "?")}
end

-- SquadRolloverMap calls TFormat.SquadNameColored, not SquadWindow:GetRolloverText.
-- CreateRolloverWindow feeds the persistent SatelliteSquad directly to the template,
-- so mutating Name here never reached the UI and is left as a passthrough.
function JAZZ_LegionAISquadNameColored(context_obj)
	local squad_name = g_JAZZ_BaseTFormatSquadNameColored(context_obj)
	local task_text = context_obj and JAZZ_GetLegionAISquadTaskText(context_obj)
	if not task_text then
		return squad_name
	end
	return T{
		890000000001447,
		"<squad_name>\nTask: <task>",
		squad_name = squad_name,
		task = task_text,
	}
end

function SquadWindow:GetRolloverText()
	return self.context
end

-- POI Extension.lua loads after this file and replaces GetSatelliteIconImages.
-- Re-wrap after mod load/reload so managed role icons win without recursion:
-- base is captured only when the global is not already our wrapper.
local function lInstallLegionAIUIWrappers()
	if GetSatelliteIconImages ~= JAZZ_LegionAIGetSatelliteIconImages then
		g_JAZZ_BaseGetSatelliteIconImages = GetSatelliteIconImages
		GetSatelliteIconImages = JAZZ_LegionAIGetSatelliteIconImages
	end
	GetSatelliteIconImagesSquad = JAZZ_LegionAIGetSatelliteIconImagesSquad
	TFormat.SquadNameColored = JAZZ_LegionAISquadNameColored
end

GetSatelliteIconImages = JAZZ_LegionAIGetSatelliteIconImages
GetSatelliteIconImagesSquad = JAZZ_LegionAIGetSatelliteIconImagesSquad
TFormat.SquadNameColored = JAZZ_LegionAISquadNameColored

function OnMsg.ModsReloaded()
	lInstallLegionAIUIWrappers()
	JAZZ_LegionAIEnsureState()
end

function OnMsg.NewGame()
	gv_JAZZ_LegionAI = lNewRootState()
	JAZZ_LegionAIEnsureState()
end

function OnMsg.LoadGame()
	lInstallLegionAIUIWrappers()
	JAZZ_LegionAIEnsureState()
end

function OnMsg.InitSatelliteView()
	lInstallLegionAIUIWrappers()
	JAZZ_LegionAIEnsureState()
end

function OnMsg.NewHour()
	JAZZ_LegionAIProcessHour()
end

function OnMsg.SquadFinishedTraveling(squad)
	if not squad or not JAZZ_IsLegionAIManagedSquad(squad) then
		return
	end
	local root = gv_JAZZ_LegionAI
	local squad_state = root.squads[squad.UniqueId]
	if not squad_state then
		return
	end
	if squad_state.role == "recon"
	and squad_state.task
	and squad_state.task.task_type == "return_with_intel"
	then
		lDeliverReconReport(root, squad, squad_state)
	else
		lOnSquadArrived(root, squad, squad_state)
	end
end

function OnMsg.SquadDespawned(squad_id)
	local root = gv_JAZZ_LegionAI
	if type(root) == "table" and root.squads then
		root.squads[squad_id] = nil
	end
end

function OnMsg.SectorSideChanged(sector_id, old_side, new_side)
	local root = JAZZ_LegionAIEnsureState()
	if not root then
		return
	end
	local region = GetRegionForSector and GetRegionForSector(sector_id)
	local region_id = lRegionId(region)
	local region_state = region_id and root.regions[region_id]
	if not region or not region_state or not region.LegionAIEnabled then
		return
	end

	local outpost = root.outposts[sector_id]
	if outpost then
		lSetOutpostControlState(root, region, outpost)
	end

	local sector = gv_Sectors[sector_id]
	local current_side = new_side or sector and sector.Side
	if sector and lSectorIsKey(sector) then
		for outpost_id in sorted_pairs(region_state.outposts) do
			local managed_outpost = root.outposts[outpost_id]
			if managed_outpost then
				if lIsPlayerSide(current_side) then
					managed_outpost.retake_targets[sector_id] = true
				elseif JAZZ_IsLegionSide(current_side) then
					managed_outpost.retake_targets[sector_id] = nil
				end
			end
		end
	end
end

function OnMsg.ConflictEnd(sector)
	local sector_id = type(sector) == "table" and (sector.Id or sector.id) or sector
	if not sector_id then
		return
	end
	if JAZZ_ClampAllSectorHeat then
		JAZZ_ClampAllSectorHeat()
	end
	local root = gv_JAZZ_LegionAI
	if type(root) ~= "table" or not root.squads then
		return
	end
	for squad_id, squad_state in sorted_pairs(root.squads) do
		local squad = gv_Squads[squad_id]
		if squad and squad.CurrentSector == sector_id and squad_state.state == "working" then
			if squad_state.role == "major" and not lPlayerSquadInSector(sector_id) then
				lBeginReturn(root, squad, squad_state)
			elseif squad_state.role == "shipment" then
				local hq = gv_Sectors[root.major.hq_sector]
				if sector_id == root.major.hq_sector and hq and JAZZ_IsLegionSide(hq.Side) then
					root.major.reserve = (root.major.reserve or 0) + (squad_state.payload.diamonds or 0)
					squad_state.payload.diamonds = 0
					lRetireSquad(root, squad_id)
				end
			end
		end
	end
end
