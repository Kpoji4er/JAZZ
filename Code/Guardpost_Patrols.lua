-- Regional strategic AI for Legion forces.
-- Static authoring lives in Region/SatelliteSector presets. Mutable state lives only here.

g_JAZZ_LegionAISpawning = false
-- Injected into CreateNewSatelliteSquad via GenerateEnemySquad so SquadWindow:SpawnSquadIcon
-- sees the role PNG before Msg("SquadSpawned") binds XMapRollerableContextImage:SetImage.
g_JAZZ_LegionAIPendingSquadImage = false

g_JAZZ_BaseGetSatelliteIconImages = rawget(_G, "g_JAZZ_BaseGetSatelliteIconImages") or GetSatelliteIconImages
g_JAZZ_BaseGetSatelliteIconImagesSquad = rawget(_G, "g_JAZZ_BaseGetSatelliteIconImagesSquad") or GetSatelliteIconImagesSquad
g_JAZZ_BaseTFormatSquadNameColored = rawget(_G, "g_JAZZ_BaseTFormatSquadNameColored") or TFormat.SquadNameColored

g_JAZZ_BaseSquadWindowCreateRolloverWindow = rawget(_G, "g_JAZZ_BaseSquadWindowCreateRolloverWindow") or SquadWindow.CreateRolloverWindow

local lSchemaVersion = 3

local lRegularRoles = {
	garrison = true,
	patrol = true,
	recon = true,
	qrf = true,
	reinforce = true,
}

-- Role icons are final 64x64 PNGs with no vanilla `_2`/`_s` companions.
-- Paths must keep the `.png` extension: GetSatelliteIconImagesSquad otherwise
-- appends `_2` for map icons, and Mod/ file assets do not resolve without it.
local lRoleImages = {
	major = "Mod/e6L4ECj/SquadsIcons/Enemy/legion_RETRIBUTION_squad.png",
	supply = "Mod/e6L4ECj/SquadsIcons/Enemy/legion_SUPPLY_squad.png",
	shipment = "Mod/e6L4ECj/SquadsIcons/Enemy/legion_SHIPMENT_squad.png",
	recon = "Mod/e6L4ECj/SquadsIcons/Enemy/legion_RECON_squad.png",
	qrf = "Mod/e6L4ECj/SquadsIcons/Enemy/legion_QRF_squad.png",
	patrol = "Mod/e6L4ECj/SquadsIcons/Enemy/legion_PATROL_squad.png",
	garrison = "Mod/e6L4ECj/SquadsIcons/Enemy/legion_GARRISON_squad.png",
	reinforce = "Mod/e6L4ECj/SquadsIcons/Enemy/legion_REINFORCE_squad.png",
	tax = "Mod/e6L4ECj/SquadsIcons/Enemy/legion_TAX_squad.png",
	recruiter = "Mod/e6L4ECj/SquadsIcons/Enemy/legion_RECRUITER_squad.png",
	manpower = "Mod/e6L4ECj/SquadsIcons/Enemy/legion_MANPOWER_squad.png",
}

-- Short role titles for satellite Name / rollover (not EnemySquadDef DisplayName).
local lRoleDisplayNames = {
	garrison = T(890000000001424, "Garrison"),
	patrol = T(890000000001425, "Patrol"),
	recon = T(890000000001426, "Recon"),
	qrf = T(890000000001427, "QRF"),
	reinforce = T(890000000001631, "Reinforce"),
	major = T(890000000001428, "Retribution"),
	supply = T(890000000001429, "Supply convoy"),
	shipment = T(890000000001430, "Diamond convoy"),
	tax = T(890000000001634, "Tax collector"),
	recruiter = T(890000000001636, "Recruiter"),
	manpower = T(890000000001637, "Manpower convoy"),
}

local function lEnsureRoleIconPng(icon)
	if type(icon) ~= "string" or icon == "" then
		return false
	end
	if icon:sub(-4):lower() == ".png" then
		return icon
	end
	-- Existing saves / interim commits may have stored the path without extension.
	if icon:find("SquadsIcons/Enemy/", 1, true) then
		return icon .. ".png"
	end
	return false
end

local function lResolveLegionAISquadIcon(squad)
	if not squad then
		return false
	end

	if type(squad) ~= "table" then
		return lEnsureRoleIconPng(JAZZ_GetLegionAISquadIcon and JAZZ_GetLegionAISquadIcon(squad))
	end

	-- Only managed / explicit JAZZ PNG overrides short-circuit vanilla. Generic
	-- squad.image paths must keep vanilla `_2` handling for map icons.
	local icon = lEnsureRoleIconPng(squad.JAZZSquadIcon or squad.jazz_squad_icon)
	if not icon and JAZZ_GetLegionAISquadIcon then
		icon = lEnsureRoleIconPng(JAZZ_GetLegionAISquadIcon(squad))
	end
	if not icon then
		icon = lEnsureRoleIconPng(type(squad.image) == "string" and squad.image)
	end
	return icon or false
end

-- SquadWindow:SpawnSquadIcon binds via SetImage(GetSatelliteIconImagesSquad(...)).
-- DrawContent reads self.Image, so live windows need an explicit SetImage refresh.
local function lRefreshSatelliteSquadIcon(squad)
	if not squad or not squad.UniqueId then
		return
	end
	local wnd = g_SatelliteUI and g_SatelliteUI.squad_to_wnd and g_SatelliteUI.squad_to_wnd[squad.UniqueId]
	local icon_wnd = wnd and wnd.idSquadIcon
	if not icon_wnd or not icon_wnd.SetImage then
		return
	end
	local icon = GetSatelliteIconImagesSquad(squad)
	if icon then
		icon_wnd:SetImage(icon)
	end
end

local function lApplySquadRoleIcon(squad, role)
	local image = role and lRoleImages[role] or false
	if not squad then
		return false
	end
	local name = role and lRoleDisplayNames[role]
	if name then
		-- UI reads SatelliteSquad.Name in many places; keep role title, not shared EnemySquadDef name.
		squad.Name = name
	end
	if not image then
		if name then
			ObjModified(squad)
		end
		return not not name
	end
	squad.image = image
	squad.jazz_squad_icon = image
	lRefreshSatelliteSquadIcon(squad)
	ObjModified(squad)
	return true
end

local lRoleCaps = {
	garrison = "GarrisonCap",
	patrol = "PatrolCap",
	recon = "ReconCap",
	qrf = "QRFCap",
	reinforce = "ReinforceCap",
}

local lRoleCosts = {
	garrison = "GarrisonCost",
	patrol = "PatrolCost",
	recon = "ReconCost",
	qrf = "QRFCost",
	reinforce = "ReinforceCost",
}

local lRoleMissions = {
	garrison = "GarrisonMissions",
	patrol = "PatrolMissions",
	recon = "ReconMissions",
	qrf = "QRFMissions",
	reinforce = "ReinforceMissions",
}

local function lNewRootState()
	return {
		schema_version = lSchemaVersion,
		last_processed_hour = false,
		next_report_id = 1,
		spawn_serial = 1,
		major = {
			hq_sector = false,
			money = false,
			manpower = false,
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

-- STRATEGY-016: diamond/$ generation ×0.25 (owner ÷4). Manpower floors keep early escorts spawnable.
JAZZ_LegionEconomyScalePct = rawget(_G, "JAZZ_LegionEconomyScalePct") or 25

local lEconomyScaleKeys = {
	StartingSupply = true,
	MajorStartingReserve = true,
	StartingManpower = true,
	MajorStartingManpower = true,
	PassiveSupplyPerHour = true,
	CitySupplyBonus = true,
	FarmSupplyBonus = true,
	MineDiamondPerHour = true,
	PoiMoneyCap = true,
	DiamondShipmentThreshold = true,
	SupplyConvoyCargo = true,
	TaxCargoMax = true,
	FarmRecruitsPerDay = true,
	CityRecruitsPerDay = true,
	GuardpostRecruitsPerDay = true,
	PortRecruitsPerDay = true,
}

local lEconomyScaleFloors = {
	StartingManpower = 8,
	MajorStartingManpower = 16,
	FarmRecruitsPerDay = 1,
	CityRecruitsPerDay = 1,
	GuardpostRecruitsPerDay = 1,
	PortRecruitsPerDay = 1,
	DiamondShipmentThreshold = 1000,
	SupplyConvoyCargo = 1000,
	TaxCargoMax = 1000,
	StartingSupply = 500,
	PoiMoneyCap = 1000,
}

local function lConfig(region, field, fallback)
	local value = region and region[field]
	if value == nil or value == false then
		value = fallback
	end
	if lEconomyScaleKeys[field] and type(value) == "number" then
		local pct = tonumber(rawget(_G, "JAZZ_LegionEconomyScalePct")) or 25
		value = DivRound(value * pct, 100)
		local floor = lEconomyScaleFloors[field]
		if floor and value > 0 then
			value = Max(floor, value)
		end
	end
	return value
end

local function lMajorMoneyCapacity(region)
	return lConfig(region, "MajorReserveCapacity", 1200000)
end

local function lClampMajorMoney(root, region, value)
	return Clamp(value or 0, 0, lMajorMoneyCapacity(region))
end

local function lAddMajorMoney(root, region, amount)
	root.major.money = lClampMajorMoney(root, region, (root.major.money or 0) + (amount or 0))
	return root.major.money
end

local function lMajorManpowerCapacity(region)
	return lConfig(region, "MajorManpowerCapacity", 600)
end

local function lAddMajorManpower(root, region, amount)
	root.major.manpower = Clamp(
		(root.major.manpower or 0) + (amount or 0),
		0,
		lMajorManpowerCapacity(region)
	)
	return root.major.manpower
end

local function lOutpostMoneyCapacity(region)
	return lConfig(region, "SupplyCapacity", 120000)
end

local function lPayloadMoney(payload)
	if type(payload) ~= "table" then
		return 0
	end
	return payload.money or payload.supply or payload.diamonds or 0
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

-- STRATEGY-021: mainland LateAwakenMinTier regions stay half-asleep until Legion tier.
local function lLegionTierNumber()
	local tier = (JAZZ_GetLegionTier and JAZZ_GetLegionTier()) or 11
	return tonumber(tier) or 11
end

local function lRegionLateAwakenMin(region)
	return tonumber(region and region.LateAwakenMinTier) or 0
end

local function lRegionDormant(region)
	local min_tier = lRegionLateAwakenMin(region)
	if min_tier <= 0 then
		return false
	end
	return lLegionTierNumber() < min_tier
end

local function lDormantIncomeDiv(region)
	return lRegionDormant(region) and 10 or 1
end

local function lNoteMajorDelivery(outpost)
	if not outpost then
		return
	end
	outpost.major_delivery_done = true
	-- STRATEGY-023: shared region — one Major delivery unlocks recruiter for all outposts.
	local root = gv_JAZZ_LegionAI
	local region = lGetRegionPreset(outpost.region_id)
	if root and region and #(region.ManagedOutposts or empty_table) >= 2 then
		for _, sector_id in ipairs(region.ManagedOutposts or empty_table) do
			local sibling = root.outposts[sector_id]
			if sibling then
				sibling.major_delivery_done = true
			end
		end
	end
end

local function lOutpostSupplyTrigger(region)
	local capacity = lOutpostMoneyCapacity(region)
	return MulDivRound(capacity, lConfig(region, "SupplyConvoyTriggerPercent", 40), 100)
end

local function lOutpostWantsSupply(root, region, outpost)
	if not outpost or not outpost.enabled then
		return false
	end
	local cargo = lConfig(region, "SupplyConvoyCargo", 12000)
	if (root.major.money or 0) < cargo then
		return false
	end
	return (outpost.money or 0) < lOutpostSupplyTrigger(region)
end

--- Among enabled outposts that want supply, prefer higher MajorSupplyPriority,
--- then lowest money (then sector id).
local function lIsNeediestSupplyOutpost(root, candidate)
	if not candidate then
		return false
	end
	local cand_region = lGetRegionPreset(candidate.region_id)
	local cand_pri = tonumber(cand_region and cand_region.MajorSupplyPriority) or 0
	local cand_money = candidate.money or 0
	local cand_id = candidate.sector_id or ""
	for _, outpost in sorted_pairs(root.outposts or empty_table) do
		if outpost.enabled and outpost.sector_id ~= cand_id then
			local region = lGetRegionPreset(outpost.region_id)
			if region and lOutpostWantsSupply(root, region, outpost) then
				local other_pri = tonumber(region.MajorSupplyPriority) or 0
				local other_money = outpost.money or 0
				local other_id = outpost.sector_id or ""
				if other_pri > cand_pri
					or (other_pri == cand_pri and other_money < cand_money)
					or (other_pri == cand_pri and other_money == cand_money and other_id < cand_id)
				then
					return false
				end
			end
		end
	end
	return true
end

--- Among enabled outposts with manpower==0, prefer MajorSupplyPriority then lowest money.
local function lIsNeediestManpowerOutpost(root, candidate)
	if not candidate or (candidate.manpower or 0) > 0 then
		return false
	end
	local cand_region = lGetRegionPreset(candidate.region_id)
	local cand_pri = tonumber(cand_region and cand_region.MajorSupplyPriority) or 0
	local cand_money = candidate.money or 0
	local cand_id = candidate.sector_id or ""
	for _, outpost in sorted_pairs(root.outposts or empty_table) do
		if outpost.enabled and outpost.sector_id ~= cand_id and (outpost.manpower or 0) <= 0 then
			local region = lGetRegionPreset(outpost.region_id)
			local other_pri = tonumber(region and region.MajorSupplyPriority) or 0
			local other_money = outpost.money or 0
			local other_id = outpost.sector_id or ""
			if other_pri > cand_pri
				or (other_pri == cand_pri and other_money < cand_money)
				or (other_pri == cand_pri and other_money == cand_money and other_id < cand_id)
			then
				return false
			end
		end
	end
	return true
end

local function lContains(list, value)
	return list and table.find(list, value) and true or false
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

-- STRATEGY-023: multi-outpost Regions share $ / manpower / diamond stock.
local function lRegionHasSharedOutposts(region)
	return region and #(region.ManagedOutposts or empty_table) >= 2
end

local function lSyncSharedOutpostResources(root, region, source)
	if not root or not source or not lRegionHasSharedOutposts(region) then
		return
	end
	local money = source.money or 0
	local manpower = source.manpower or 0
	local diamond = source.diamond_stock or 0
	for _, sector_id in ipairs(region.ManagedOutposts or empty_table) do
		local outpost = root.outposts[sector_id]
		if outpost then
			outpost.money = money
			outpost.manpower = manpower
			outpost.diamond_stock = diamond
		end
	end
end

local function lFindEnabledSiblingOutpost(root, region_id, exclude_sector)
	if not root or not region_id then
		return false, false
	end
	for sector_id, outpost in sorted_pairs(root.outposts or empty_table) do
		if outpost
			and outpost.region_id == region_id
			and outpost.enabled
			and sector_id ~= exclude_sector
		then
			return sector_id, outpost
		end
	end
	return false, false
end

--- Claim orphans whose home is disabled; rehome to this enabled outpost (same region).
local function lClaimRegionOrphans(root, outpost)
	if not root or not outpost or not outpost.enabled then
		return 0
	end
	local claimed = 0
	for squad_id, squad_state in sorted_pairs(root.squads or empty_table) do
		if squad_state.region_id == outpost.region_id
			and squad_state.state == "orphaned"
			and lRegularRoles[squad_state.role]
		then
			local home = root.outposts[squad_state.home_sector]
			if not home or not home.enabled or squad_state.home_sector == outpost.sector_id then
				squad_state.home_sector = outpost.sector_id
				squad_state.task = false
				squad_state.state = "ready_for_orders"
				claimed = claimed + 1
				local squad = gv_Squads and gv_Squads[squad_id]
				if squad then
					ObjModified(squad)
				end
			end
		end
	end
	return claimed
end

local function lEnsureOutpost(root, region, region_state, sector_id)
	local sector = gv_Sectors and gv_Sectors[sector_id]
	local controlled = sector and JAZZ_IsLegionSide(sector.Side) or false
	local outpost = root.outposts[sector_id]
	if not outpost then
		-- STRATEGY-023: additional outposts in a shared region start empty and pull from siblings.
		local start_money = lConfig(region, "StartingSupply", 12000)
		local start_manpower = lConfig(region, "StartingManpower", 20)
		if lRegionHasSharedOutposts(region) then
			for _, other_id in ipairs(region.ManagedOutposts or empty_table) do
				if other_id ~= sector_id and root.outposts[other_id] then
					start_money = 0
					start_manpower = 0
					break
				end
			end
		end
		outpost = {
			sector_id = sector_id,
			region_id = lRegionId(region),
			enabled = controlled,
			owner_faction = "legion",
			money = start_money,
			manpower = start_manpower,
			diamond_stock = 0,
			next_command_time = lNow() + lInterval(region, "CommandInterval", 12 * lHourScale()),
			reboot_until = 0,
			retake_targets = {},
			last_tax_time = 0,
			last_recruiter_time = 0,
			last_spawn_time = 0,
			outbound_manpower = 0,
			logistics_open_at = lNow() + 72 * lHourScale(),
		}
		root.outposts[sector_id] = outpost
		if start_money == 0 and lRegionHasSharedOutposts(region) then
			for _, other_id in ipairs(region.ManagedOutposts or empty_table) do
				local other = root.outposts[other_id]
				if other and other_id ~= sector_id then
					lSyncSharedOutpostResources(root, region, other)
					break
				end
			end
		end
	end
	outpost.retake_targets = outpost.retake_targets or {}
	outpost.last_tax_time = outpost.last_tax_time or 0
	outpost.last_recruiter_time = outpost.last_recruiter_time or 0
	outpost.last_spawn_time = outpost.last_spawn_time or 0
	outpost.outbound_manpower = outpost.outbound_manpower or 0
	-- STRATEGY-019: new outposts set logistics_open_at at create; existing saves open now.
	if outpost.logistics_open_at == nil then
		outpost.logistics_open_at = 0
	end
	if outpost.manpower == false or outpost.manpower == nil then
		outpost.manpower = lConfig(region, "StartingManpower", 20)
	end
	-- STRATEGY-014: owner_faction — Legion director only when legion owns.
	if not outpost.owner_faction then
		if controlled then
			outpost.owner_faction = "legion"
		elseif sector and lIsPlayerSide(sector.Side) then
			outpost.owner_faction = "player"
		else
			outpost.owner_faction = "unknown"
		end
		if rawget(_G, "JAZZ_SetSectorOwnerFaction") then
			JAZZ_SetSectorOwnerFaction(sector_id, outpost.owner_faction, "ensure")
		end
	elseif rawget(_G, "JAZZ_GetSectorOwnerFaction") then
		local overlay = JAZZ_GetSectorOwnerFaction(sector_id)
		if overlay and overlay ~= "unknown" then
			outpost.owner_faction = overlay
		end
	end
	local legion_owns = outpost.owner_faction == "legion"
	-- Refresh each ensure: stale enabled=false after paralyzed/empty-region sessions.
	outpost.enabled = controlled and legion_owns
	outpost.region_id = lRegionId(region)
	region_state.outposts[sector_id] = true
	return outpost
end

-- NoMaps (COMPAT-004): never latch Major HQ from maps-only regions / disabled regions.
local function lJazzMapsModLoaded()
	if rawget(_G, "IsModLoaded") then
		return not not IsModLoaded("FhNNYd")
	end
	if rawget(_G, "GetModLoaded") then
		return not not GetModLoaded("FhNNYd")
	end
	return ModsLoaded and table.find(ModsLoaded, "id", "FhNNYd") and true or false
end

local function lNoMapsProfileLikely()
	local active = rawget(_G, "JAZZ_NoMapsIsActive")
	if active and active() then
		return true
	end
	-- jazz NewGame runs before nomaps bootstrap: detect package without maps.
	if lJazzMapsModLoaded() then
		return false
	end
	if rawget(_G, "IsModLoaded") then
		return not not IsModLoaded("7MsJ2Eq")
	end
	if rawget(_G, "GetModLoaded") then
		return not not GetModLoaded("7MsJ2Eq")
	end
	return ModsLoaded and table.find(ModsLoaded, "id", "7MsJ2Eq") and true or false
end

local function lMayAdoptMajorHQ(region)
	if not region or not region.LegionAIEnabled then
		return false
	end
	local rid = lRegionId(region)
	if rid == "ErnieIsland" or rid == "PortCacaoEnvirons" or rid == "GreatDesert" or rid == "MountainSteppe" or rid == "FleatownEnvirons" or rid == "LaBarrier" or rid == "GreatForest" then
		if lNoMapsProfileLikely() then
			return false
		end
	end
	return true
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
			poi_money = {},
			poi_recruits = {},
			next_poi_pulse_time = lNow(), -- first hour accrues POI $ / recruits
			next_heat_decay_time = lNow() + lInterval(region, "HeatDecayInterval", 7 * lHourScale()),
		}
		root.regions[region_id] = region_state
	end
	region_state.reports = region_state.reports or {}
	region_state.outposts = region_state.outposts or {}
	region_state.last_patrolled = region_state.last_patrolled or {}
	region_state.poi_money = region_state.poi_money or {}
	region_state.poi_recruits = region_state.poi_recruits or {}
	-- Prefer unified 3-day POI pulse; fall back from legacy daily recruit timer.
	-- Treat 0 as unset (Lua falsy) but also sanitize timers stuck far in the past
	-- from ForcePoiPulse/debug or pre-campaign GameVar init.
	if not region_state.next_poi_pulse_time or region_state.next_poi_pulse_time <= 0 then
		region_state.next_poi_pulse_time = region_state.next_recruit_time
			and region_state.next_recruit_time > 0
			and region_state.next_recruit_time
			or (lNow() + lInterval(region, "POIGenerationInterval", 96 * lHourScale()))
	end
	local money_cap = lConfig(region, "PoiMoneyCap", 12000)
	for sector_id, money in pairs(region_state.poi_money) do
		if type(money) == "number" and money > money_cap then
			region_state.poi_money[sector_id] = money_cap
		elseif type(money) == "number" and money < 0 then
			region_state.poi_money[sector_id] = 0
		end
	end
	region_state.heat = lClampHeat(region_state.heat)

	for _, sector_id in ipairs(region.ManagedOutposts or empty_table) do
		lEnsureOutpost(root, region, region_state, sector_id)
	end

	local hq_sector = region.MajorHQSector
	if hq_sector and hq_sector ~= "" and lMayAdoptMajorHQ(region) then
		root.major.hq_sector = root.major.hq_sector or hq_sector
		if root.major.money == false or root.major.money == nil then
			root.major.money = lClampMajorMoney(
				root,
				region,
				lConfig(region, "MajorStartingReserve", 120000)
			)
		else
			root.major.money = lClampMajorMoney(root, region, root.major.money)
		end
		if root.major.manpower == false or root.major.manpower == nil then
			root.major.manpower = lConfig(region, "MajorStartingManpower", 80)
		end
		root.major.manpower = Clamp(
			root.major.manpower or 0,
			0,
			lConfig(region, "MajorManpowerCapacity", 600)
		)
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
			lApplySquadRoleIcon(squad, "garrison")
			session_obj.primed_squad = false
			session_obj.next_spawn_time = false
			session_obj.next_spawn_time_duration = false
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
			-- Icon + role display name (tax/recruiter/etc. must not keep shared Convoy title).
			lApplySquadRoleIcon(squad, squad_state.role)
		end
	end
end

local function lMigrateSchemaToMoney(root)
	-- Abstract supply/reserve units are not dollars; reset pools to starting $.
	root.major = root.major or {}
	root.major.money = false
	root.major.reserve = nil
	for _, outpost in sorted_pairs(root.outposts or empty_table) do
		local region = lGetRegionPreset(outpost.region_id)
		outpost.money = lConfig(region, "StartingSupply", 12000)
		outpost.supply = nil
		outpost.diamond_stock = 0
	end
	for _, squad_state in sorted_pairs(root.squads or empty_table) do
		local payload = squad_state.payload
		if type(payload) == "table" then
			payload.money = lPayloadMoney(payload)
			payload.supply = nil
			payload.diamonds = nil
		end
	end
	root.schema_version = 2
	lLog("migrated Legion AI economy schema to money ($); outpost/major pools reset to starting values")
end

local function lMigrateSchemaToManpower(root)
	root.major = root.major or {}
	root.major.manpower = false
	for _, outpost in sorted_pairs(root.outposts or empty_table) do
		outpost.manpower = false
		outpost.last_recruiter_time = outpost.last_recruiter_time or 0
	end
	for _, region_state in sorted_pairs(root.regions or empty_table) do
		region_state.poi_recruits = region_state.poi_recruits or {}
		region_state.next_poi_pulse_time = region_state.next_poi_pulse_time
			or region_state.next_recruit_time
			or (lNow() + 72 * lHourScale())
	end
	root.schema_version = 3
	lLog("migrated Legion AI schema to manpower pools (v3)")
end

function JAZZ_LegionAIEnsureState()
	if type(gv_JAZZ_LegionAI) ~= "table" then
		gv_JAZZ_LegionAI = lNewRootState()
	end
	local root = gv_JAZZ_LegionAI
	root.schema_version = root.schema_version or 1
	root.last_processed_hour = root.last_processed_hour or false
	root.next_report_id = root.next_report_id or 1
	root.spawn_serial = root.spawn_serial or 1
	root.major = root.major or { hq_sector = false, money = false, manpower = false, next_response_time = 0 }
	root.major.next_response_time = root.major.next_response_time or 0
	root.regions = root.regions or {}
	root.outposts = root.outposts or {}
	root.squads = root.squads or {}
	root.missing_defs_logged = root.missing_defs_logged or {}
	root.global_spawn = root.global_spawn or { window_start = 0, used = 0 }

	if root.schema_version > lSchemaVersion then
		lLog(string.format("unsupported save schema %s; feature disabled", tostring(root.schema_version)))
		return false
	end
	if root.schema_version < 2 then
		lMigrateSchemaToMoney(root)
	elseif root.major.money == nil and root.major.reserve ~= nil then
		lMigrateSchemaToMoney(root)
	end
	root.major.reserve = nil
	if root.schema_version < 3 then
		lMigrateSchemaToManpower(root)
	end

	if not Regions or not gv_Sectors then
		return false
	end
	for _, region in sorted_pairs(Regions) do
		lEnsureRegion(root, region)
	end
	for _, outpost in sorted_pairs(root.outposts) do
		local region = lGetRegionPreset(outpost.region_id)
		if outpost.money == nil then
			outpost.money = lConfig(region, "StartingSupply", 12000)
			outpost.supply = nil
		end
		outpost.money = Clamp(outpost.money or 0, 0, lOutpostMoneyCapacity(region))
		outpost.diamond_stock = outpost.diamond_stock or 0
		if outpost.manpower == false or outpost.manpower == nil then
			outpost.manpower = lConfig(region, "StartingManpower", 20)
		end
		outpost.manpower = Clamp(outpost.manpower or 0, 0, lConfig(region, "ManpowerCapacity", 32))
		if not outpost.owner_faction then
			local sector = gv_Sectors and gv_Sectors[outpost.sector_id]
			if sector and lIsPlayerSide(sector.Side) then
				outpost.owner_faction = "player"
			elseif sector and JAZZ_IsLegionSide(sector.Side) then
				outpost.owner_faction = "legion"
			else
				outpost.owner_faction = "unknown"
			end
		end
	end
	if rawget(_G, "JAZZ_FactionOverlayRepairOwners") then
		JAZZ_FactionOverlayRepairOwners()
	end
	if root.major.manpower == false or root.major.manpower == nil then
		local any_region = false
		for _, region in sorted_pairs(Regions or empty_table) do
			if region.LegionAIEnabled then
				any_region = region
				break
			end
		end
		root.major.manpower = lConfig(any_region, "MajorStartingManpower", 80)
	end
	local major_cap = 600
	for _, region in sorted_pairs(Regions or empty_table) do
		if region.LegionAIEnabled then
			major_cap = lConfig(region, "MajorManpowerCapacity", 600)
			break
		end
	end
	root.major.manpower = Clamp(root.major.manpower or 0, 0, major_cap)
	lAdoptLegacyPrimedSquads(root)
	lReconcileSquads(root)
	return root
end

--- Force Major HQ sector (NoMaps COMPAT-004). Overwrites any prior latch (e.g. Ernie B28).
function JAZZ_LegionAIForceMajorHQ(sector_id)
	local root = JAZZ_LegionAIEnsureState()
	if type(root) ~= "table" or type(root.major) ~= "table" then
		return false
	end
	if type(sector_id) ~= "string" or sector_id == "" then
		return false
	end
	if not (gv_Sectors and gv_Sectors[sector_id]) then
		return false
	end
	root.major.hq_sector = sector_id
	return true
end

--- Adopt existing Legion enemy squads on managed outposts as garrison (HotDiamonds InitialSquads).
function JAZZ_LegionAIAdoptOutpostDefenders()
	local root = JAZZ_LegionAIEnsureState()
	if type(root) ~= "table" then
		return 0
	end
	local adopted = 0
	for sector_id, outpost in sorted_pairs(root.outposts or empty_table) do
		if type(outpost) ~= "table" then
			goto next_outpost
		end
		-- Already have a managed garrison for this home → skip to avoid doubles.
		local has_garrison = false
		for _, squad_state in sorted_pairs(root.squads or empty_table) do
			if squad_state.home_sector == sector_id
				and squad_state.role == "garrison"
				and squad_state.state ~= "retired"
			then
				has_garrison = true
				break
			end
		end
		if has_garrison then
			goto next_outpost
		end
		local best_id, best_n = false, -1
		for _, squad in sorted_pairs(gv_Squads or empty_table) do
			if squad
				and not squad.arrival_squad
				and squad.CurrentSector == sector_id
				and JAZZ_IsLegionSide(squad.Side)
				and not root.squads[squad.UniqueId]
			then
				local n = #(squad.units or empty_table)
				if n > best_n then
					best_n = n
					best_id = squad.UniqueId
				end
			end
		end
		if best_id then
			local region = lGetRegionPreset(outpost.region_id)
			root.squads[best_id] = {
				squad_id = best_id,
				region_id = outpost.region_id,
				home_sector = sector_id,
				role = "garrison",
				state = "ready_for_orders",
				missions_left = lConfig(region, "GarrisonMissions", 3),
				payload = {},
				task = false,
			}
			local squad = gv_Squads[best_id]
			if squad then
				lApplySquadRoleIcon(squad, "garrison")
				ObjModified(squad)
			end
			local sector = gv_Sectors[sector_id]
			if sector then
				ObjModified(sector)
			end
			Msg("JAZZ_LegionAISquadManaged", best_id, "garrison", sector_id)
			adopted = adopted + 1
		end
		::next_outpost::
	end
	return adopted
end

-- Surface helper must be declared before SeedPoiEconomy (Lua locals are not visible above).
local function lSectorIsSurface(sector)
	return sector and not sector.GroundSector and sector.Passability ~= "Water" and sector.Passability ~= "Blocked"
end

--- Seed POI money/recruits so tax/recruiter can fire early (NoMaps COMPAT-004).
function JAZZ_LegionAISeedPoiEconomy(opts)
	local root = JAZZ_LegionAIEnsureState()
	if type(root) ~= "table" then
		return 0
	end
	opts = opts or empty_table
	local money_seed = opts.money or 1500
	local recruit_seed = opts.recruits or 10
	local seeded = 0
	-- Inline surface test: do not call chunk-local lSectorIsSurface (strict _G / load-order).
	local function sector_is_surface(sector)
		return sector and not sector.GroundSector and sector.Passability ~= "Water" and sector.Passability ~= "Blocked"
	end
	for region_id, region_state in sorted_pairs(root.regions or empty_table) do
		local region = lGetRegionPreset(region_id)
		if not region or not region.LegionAIEnabled then
			goto next_region
		end
		region_state.poi_money = region_state.poi_money or {}
		region_state.poi_recruits = region_state.poi_recruits or {}
		local money_cap = lConfig(region, "PoiMoneyCap", 12000)
		local recruit_cap = lConfig(region, "PoiRecruitCap", 24)
		for _, sector_id in ipairs(region.Sectors or empty_table) do
			local sector = gv_Sectors and gv_Sectors[sector_id]
			if not sector or not sector_is_surface(sector) then
				goto next_sector
			end
			-- Prefer Farm / City POIs (same signals as tax/recruiter circuits).
			local is_poi = sector.Mine
				or (sector.City and sector.City ~= "none")
				or sector.Guardpost
			if not is_poi then
				goto next_sector
			end
			local cur_m = region_state.poi_money[sector_id] or 0
			if cur_m < money_seed then
				region_state.poi_money[sector_id] = Min(money_cap, money_seed)
				seeded = seeded + 1
			end
			local cur_r = region_state.poi_recruits[sector_id] or 0
			if cur_r < recruit_seed then
				region_state.poi_recruits[sector_id] = Min(recruit_cap, recruit_seed)
				seeded = seeded + 1
			end
			::next_sector::
		end
		-- Allow first pulse soon so seed is usable.
		if (region_state.next_poi_pulse_time or 0) > lNow() + 6 * lHourScale() then
			region_state.next_poi_pulse_time = lNow() + lHourScale()
		end
		::next_region::
	end
	return seeded
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

-- Key sites for patrol/garrison/retake (includes city-tagged wilderness hubs).
local function lSectorIsKey(sector)
	return sector
		and (sector.Guardpost
			or (sector.City and sector.City ~= "none")
			or sector.Mine
			or sector.Farm
			or sector.Port
			or sector.Hospital)
end

-- Tax/recruit only on real economic POI — not every wilderness tile sharing City=Ernie.
local function lSectorIsEconomicPOI(sector)
	if not sector then
		return false
	end
	if sector.Farm or sector.Mine or sector.Guardpost or sector.Port then
		return true
	end
	if sector.City and sector.City ~= "none" and (sector.Militia or sector.Hospital) then
		return true
	end
	return false
end

local function lSectorPriority(sector)
	if not sector then return 0 end
	if sector.Guardpost then return 400 end
	if sector.Port then return 350 end
	if sector.City and sector.City ~= "none" and (sector.Militia or sector.Hospital or sector.Guardpost) then
		return 300
	end
	if sector.Mine then return 200 end
	if sector.Farm then return 100 end
	if sector.Hospital then return 80 end
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

-- Any non-arrival Legion/enemy squad already in the sector counts as defense,
-- including campaign-preplaced squads outside gv_JAZZ_LegionAI management.
local function lSectorHasLegionDefense(sector_id)
	for _, squad in sorted_pairs(gv_Squads or empty_table) do
		if squad
		and squad.CurrentSector == sector_id
		and not squad.arrival_squad
		and JAZZ_IsLegionSide(squad.Side)
		then
			return true
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

local function lCountImportantLegionSectors(region)
	local count = 0
	for _, sector_id in ipairs(region.Sectors or empty_table) do
		local sector = gv_Sectors[sector_id]
		if sector and JAZZ_IsLegionSide(sector.Side) and lSectorIsKey(sector) and lSectorIsSurface(sector) then
			count = count + 1
		end
	end
	return count
end

local function lGarrisonCap(region)
	-- Cap = important Legion sectors + 1 (fallback to preset if region empty)
	-- + authored GarrisonCapBonus (STRATEGY-022 barrier / doctrine).
	local key_count = lCountImportantLegionSectors(region)
	local base
	if key_count > 0 then
		base = key_count + 1
	else
		base = lConfig(region, "GarrisonCap", 2)
	end
	local bonus = tonumber(region and region.GarrisonCapBonus) or 0
	return base + Max(0, bonus)
end

local function lPatrolSectorPool(region)
	local pool = {}
	local seen = {}
	local function add_from(reg)
		if not reg then
			return
		end
		for _, sector_id in ipairs(reg.Sectors or empty_table) do
			if not seen[sector_id] then
				seen[sector_id] = true
				pool[#pool + 1] = sector_id
			end
		end
	end
	add_from(region)
	for _, rid in ipairs(region and region.ExportPatrolRegionIds or empty_table) do
		add_from(lGetRegionPreset(rid))
	end
	return pool
end

local function lCountRegionRole(root, region_id, role)
	local count = 0
	for _, squad_state in sorted_pairs(root.squads) do
		if squad_state.region_id == region_id
			and squad_state.role == role
			and squad_state.state ~= "retired"
		then
			count = count + 1
		end
	end
	return count
end

local function lOutpostCanSpawn(outpost)
	-- Combat fill only: one new regular spawn per outpost per 48h (STRATEGY-016 cadence).
	-- Late-awaken dormant: ×10 gate (STRATEGY-021).
	-- Logistics (tax/recruiter/supply/shipment/manpower) use their own cooldowns
	-- and must not be starved by garrison/patrol while-loops in the same window.
	local gate = 48 * lHourScale()
	local region = outpost and lGetRegionPreset(outpost.region_id)
	if lRegionDormant(region) then
		gate = gate * 10
	end
	return (outpost.last_spawn_time or 0) + gate <= lNow()
end

local function lMarkOutpostSpawn(outpost)
	outpost.last_spawn_time = lNow()
end

-- STRATEGY-019: global new-spawn pool (map-wide), sized by Legion major tier.
local function lLegionMajorTier()
	local tier = (JAZZ_GetLegionTier and JAZZ_GetLegionTier()) or 11
	tier = tonumber(tier) or 11
	return Max(1, DivRound(tier, 10))
end

local function lGlobalSpawnSlotCap()
	local major = lLegionMajorTier()
	if major >= 3 then
		return 3
	end
	if major >= 2 then
		return 2
	end
	return 1
end

local function lEnsureGlobalSpawnState(root)
	root.global_spawn = root.global_spawn or { window_start = 0, used = 0 }
	local window = 24 * lHourScale()
	local gs = root.global_spawn
	if (gs.window_start or 0) + window <= lNow() then
		gs.window_start = lNow()
		gs.used = 0
	end
	return gs
end

local function lCanConsumeGlobalSpawn(root)
	if type(root) ~= "table" then
		return false
	end
	local gs = lEnsureGlobalSpawnState(root)
	return (gs.used or 0) < lGlobalSpawnSlotCap()
end

local function lConsumeGlobalSpawn(root)
	local gs = lEnsureGlobalSpawnState(root)
	gs.used = (gs.used or 0) + 1
end

--- Tax/recruiter: wait logistics_open_at (72h after outpost enable) before first spawn.
local function lLogisticsOpen(outpost)
	if not outpost then
		return false
	end
	local open_at = outpost.logistics_open_at or 0
	return open_at <= lNow()
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
			and squad_state.state ~= "retired"
			and task
			and task.target_sector == target_sector
			and (squad_state.role == role or task.task_type == role)
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
	for _, sector_id in ipairs(lPatrolSectorPool(region)) do
		local sector = gv_Sectors[sector_id]
		-- Side is ignored: patrol may enter player-controlled key/POI sectors.
		-- ExportPatrolRegionIds (STRATEGY-022) extend the pool into neighbor regions.
		if sector_id ~= squad.CurrentSector
			and lSectorIsSurface(sector)
			and lSectorIsKey(sector)
		then
			local last_time = region_state.last_patrolled[sector_id] or 0
			local age_hours = Max(0, (lNow() - last_time) / lHourScale())
			-- Prefer empty sectors (no player squad present).
			local empty_bonus = lPlayerSquadInSector(sector_id) and 0 or 500
			entries[#entries + 1] = {
				id = sector_id,
				weight = lSectorPriority(sector) + (sector.Heat or 0) + Min(age_hours * 20, 1000) + empty_bonus,
			}
		end
	end
	local picked = lWeightedChoice(entries, "Patrol_" .. tostring(squad.UniqueId))
	return picked and picked.id
end

local function lSectorNeighborsPlayerThreat(sector_id, region)
	for _, other_id in ipairs(region.Sectors or empty_table) do
		if other_id ~= sector_id then
			local other = gv_Sectors[other_id]
			local distance = lSectorIsSurface(other) and GetSectorDistance(sector_id, other_id)
			if distance == 1 and (lIsPlayerSide(other.Side) or lPlayerSquadInSector(other_id)) then
				return true
			end
		end
	end
	return false
end

local function lReinforceTarget(root, region, region_state)
	local entries = {}
	for _, sector_id in ipairs(region.Sectors or empty_table) do
		local sector = gv_Sectors[sector_id]
		if lSectorIsSurface(sector)
		and lSectorIsKey(sector)
		and JAZZ_IsLegionSide(sector.Side)
		and not lHasRoleTarget(root, region_state.region_id, "reinforce", sector_id)
		and lSectorNeighborsPlayerThreat(sector_id, region)
		then
			local empty_bonus = lPlayerSquadInSector(sector_id) and 0 or 400
			entries[#entries + 1] = {
				id = sector_id,
				weight = lSectorPriority(sector) + (sector.Heat or 0) + empty_bonus,
			}
		end
	end
	local picked = lWeightedChoice(entries, "Reinforce_" .. region_state.region_id)
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
		and not lSectorHasLegionDefense(sector_id)
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

-- Major↔outpost convoys may cross water freely (island logistics).
-- All other managed roles prefer land; water only if no land path exists.
local lMajorSeaConvoyRoles = {
	supply = true,
	shipment = true,
	manpower = true,
}

-- JAZZ-STRATEGY-018: these roles must avoid player-controlled sectors.
local lAvoidPlayerRoles = {
	shipment = true,
	supply = true,
	tax = true,
	manpower = true,
	recruiter = true,
	reinforce = true,
}

local function lManagedSquadRole(squad)
	local root = gv_JAZZ_LegionAI
	local squad_state = root and root.squads and squad and root.squads[squad.UniqueId]
	return squad_state and squad_state.role or false
end

local function lRoutePathForRole(from_sector, to_sector, role, side, units)
	if not from_sector or not to_sector then
		return false
	end
	if from_sector == to_sector then
		return {}
	end
	local allow_water_first = role and lMajorSeaConvoyRoles[role]
	local avoid_player = role and lAvoidPlayerRoles[role]
	if avoid_player then
		rawset(_G, "g_JAZZ_RouteAvoidPlayer", true)
	end
	local route = false
	if not allow_water_first then
		route = GenerateRouteDijkstra(
			from_sector,
			to_sector,
			false,
			units,
			"land_only",
			nil,
			side or "enemy1"
		)
	end
	if not route then
		-- Enemy/Legion boatless water edges; "land_water" needs player port + boat money.
		route = GenerateRouteDijkstra(
			from_sector,
			to_sector,
			false,
			units,
			"land_water_boatless",
			nil,
			side or "enemy1"
		)
	end
	if avoid_player then
		rawset(_G, "g_JAZZ_RouteAvoidPlayer", false)
	end
	return route
end

local function lRoutePath(squad, target_sector)
	if not squad or not squad.CurrentSector or not target_sector then
		return false
	end
	local role = lManagedSquadRole(squad)
	return lRoutePathForRole(squad.CurrentSector, target_sector, role, squad.Side, squad.units)
end

---True if role can reach destination without entering player Side (018 spawn gate).
local function lHasAvoidPlayerRoute(from_sector, to_sector, role, side, units)
	if not lAvoidPlayerRoles[role] then
		return true
	end
	local route = lRoutePathForRole(from_sector, to_sector, role, side, units)
	return route and true or false
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
	if role == "garrison" or role == "reinforce" then
		return lNonEmptyList(sector.EnemySquadsGarrisonList, sector.ExtraDefenderSquads)
	elseif role == "patrol" then
		return lNonEmptyList(sector.EnemySquadsPatroolList, sector.EnemySquadsList)
	elseif role == "recon" then
		return lNonEmptyList(sector.EnemySquadsReconList, sector.EnemySquadsList)
	elseif role == "qrf" then
		return lNonEmptyList(sector.EnemySquadsQRFList, sector.StrongEnemySquadsList)
	elseif role == "supply" then
		return region.SupplySquads
	elseif role == "tax" then
		return lNonEmptyList(region.TaxSquads, region.SupplySquads)
	elseif role == "recruiter" then
		return lNonEmptyList(region.RecruiterSquads, region.SupplySquads)
	elseif role == "manpower" then
		return lNonEmptyList(region.ManpowerSquads, region.SupplySquads)
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

-- STRATEGY-017: tagged mission cargo survives loot regen; pocket TinyDiamonds stay untagged.
local function lIsMoneyCargoItem(item)
	return item
		and (item.class == "DiamondBriefcase" or item.class == "TinyDiamonds")
		and item.jazz_legion_ai_cargo
end

local function lMoneyCargoItemValue(item)
	if not item then
		return 0
	end
	if item.class == "DiamondBriefcase" then
		return 12000
	end
	if item.class == "TinyDiamonds" then
		return 500 * (item.Amount or 1)
	end
	return 0
end

local function lClearTaggedMoneyCargo(squad)
	if not squad then
		return
	end
	for _, session_id in ipairs(squad.units or empty_table) do
		local ud = gv_UnitData[session_id]
		if ud and ud.ForEachItemInSlot then
			local doomed = {}
			ud:ForEachItemInSlot("Inventory", function(item)
				if lIsMoneyCargoItem(item) then
					doomed[#doomed + 1] = item
				end
			end)
			for _, item in ipairs(doomed) do
				ud:RemoveItem("Inventory", item)
				if IsValid(item) then
					DoneObject(item)
				end
			end
		end
		local live = g_Units and g_Units[session_id]
		if live and live.ForEachItemInSlot then
			local doomed = {}
			live:ForEachItemInSlot("Inventory", function(item)
				if lIsMoneyCargoItem(item) then
					doomed[#doomed + 1] = item
				end
			end)
			for _, item in ipairs(doomed) do
				live:RemoveItem("Inventory", item)
				if IsValid(item) then
					DoneObject(item)
				end
			end
		end
	end
	squad.diamond_briefcase = nil
end

local function lSquadTaggedMoneyCargoValue(squad)
	local total = 0
	if not squad then
		return 0
	end
	for _, session_id in ipairs(squad.units or empty_table) do
		local ud = gv_UnitData[session_id]
		if ud and ud.ForEachItem then
			ud:ForEachItem(function(item)
				if lIsMoneyCargoItem(item) then
					total = total + lMoneyCargoItemValue(item)
				end
			end)
		end
	end
	return total
end

local function lTryAddCargoItem(squad, item)
	if not squad or not item then
		return false
	end
	item.drop_chance = 100
	item.jazz_legion_ai_cargo = true
	for _, session_id in ipairs(squad.units or empty_table) do
		local ud = gv_UnitData[session_id]
		if ud then
			local pos = ud:AddItem("Inventory", item)
			if pos then
				local live = g_Units and g_Units[session_id]
				if live and live ~= ud and live.AddItem then
					-- Keep tactical unit inventory aligned when already spawned into conflict.
					local copy = PlaceInventoryItem(item.class)
					if copy then
						copy.drop_chance = 100
						copy.jazz_legion_ai_cargo = true
						if item.class == "TinyDiamonds" then
							copy.Amount = item.Amount or 1
						end
						live:AddItem("Inventory", copy)
					end
				end
				return true
			end
		end
	end
	if IsValid(item) then
		DoneObject(item)
	end
	return false
end

--- Place valuables matching dollars (DB @$12000 + TinyDiamonds @$500 ceil).
-- Clears previous tagged cargo first. Returns false if any chunk failed to place.
local function lSyncMoneyCargo(squad, dollars)
	if not squad then
		return false
	end
	dollars = math.max(0, math.floor(tonumber(dollars) or 0))
	lClearTaggedMoneyCargo(squad)
	if dollars <= 0 then
		return true
	end
	if not (squad.units and squad.units[1] and gv_UnitData[squad.units[1]]) then
		return false
	end
	local remaining = dollars
	while remaining >= 12000 do
		local briefcase = PlaceInventoryItem("DiamondBriefcase")
		if not briefcase or not lTryAddCargoItem(squad, briefcase) then
			lClearTaggedMoneyCargo(squad)
			return false
		end
		remaining = remaining - 12000
	end
	local coins = remaining > 0 and math.ceil(remaining / 500) or 0
	for _ = 1, coins do
		local chip = PlaceInventoryItem("TinyDiamonds")
		if not chip or not lTryAddCargoItem(squad, chip) then
			lClearTaggedMoneyCargo(squad)
			return false
		end
	end
	squad.diamond_briefcase = dollars >= 12000 or nil
	return true
end

local function lEnsureMoneyCargo(squad, dollars)
	return lSyncMoneyCargo(squad, dollars)
end

local function lEnsureDiamondCargo(squad)
	return lEnsureMoneyCargo(squad, 12000)
end

local function lResyncManagedMoneyCargo(root)
	root = root or gv_JAZZ_LegionAI
	if type(root) ~= "table" or not root.squads then
		return 0
	end
	local fixed = 0
	for squad_id, squad_state in sorted_pairs(root.squads) do
		local role = squad_state and squad_state.role
		if role == "tax" or role == "shipment" or role == "supply" then
			local dollars = lPayloadMoney(squad_state.payload)
			local squad = gv_Squads[squad_id]
			if squad and dollars > 0 then
				local have = lSquadTaggedMoneyCargoValue(squad)
				-- Allow Tiny ceil slack (±500): resync when missing cargo or flag-only leftovers.
				if have + 500 < dollars or (have == 0 and dollars > 0) then
					if lSyncMoneyCargo(squad, dollars) then
						fixed = fixed + 1
					else
						lLog(string.format("money cargo resync failed for %s squad %s ($%d)", tostring(role), tostring(squad_id), dollars))
					end
				end
			elseif squad and dollars <= 0 and lSquadTaggedMoneyCargoValue(squad) > 0 then
				lClearTaggedMoneyCargo(squad)
			end
		end
	end
	return fixed
end

function JAZZ_LegionAIResyncMoneyCargo()
	return lResyncManagedMoneyCargo(JAZZ_LegionAIEnsureState and JAZZ_LegionAIEnsureState() or gv_JAZZ_LegionAI)
end

local function lRecruitUnitTemplate(region)
	return lConfig(region, "RecruiterUnitTemplate", "JAZZ_Legion_Recruit")
end

local function lSquadRecruitRoom(squad, cargo_max, have)
	local max_people = Max((const.Satellite and const.Satellite.MercSquadMaxPeople) or 18, 28)
	local room_squad = Max(0, max_people - #(squad.units or empty_table))
	local room_cargo = Max(0, (cargo_max or 16) - (have or 0))
	return Min(room_squad, room_cargo)
end

-- Create N recruit UnitData and attach them to squad. Returns added session ids.
local function lAddRecruitUnitsToSquad(root, squad, count, unit_template, context)
	local added = {}
	if not squad or not count or count <= 0 then
		return added
	end
	unit_template = unit_template or "JAZZ_Legion_Recruit"
	if not (UnitDataDefs and UnitDataDefs[unit_template]) then
		lLog(string.format("recruit unit template missing: %s", tostring(unit_template)))
		return added
	end
	if not CreateUnitData then
		lLog("CreateUnitData unavailable; cannot add recruits")
		return added
	end

	local serial = root.spawn_serial or 1
	root.spawn_serial = serial + 1
	local base = string.format("JAZZLegionRecruit_%s_%s_%d", context or "x", tostring(squad.CurrentSector or "sec"), serial)
	local templates = {}
	for _ = 1, count do
		templates[#templates + 1] = unit_template
	end

	local session_ids
	if GenerateUnitsFromTemplates then
		local ok, result = pcall(GenerateUnitsFromTemplates, squad.CurrentSector or squad.CurrentSector, templates, base)
		if ok then
			session_ids = result
		else
			lLog(string.format("GenerateUnitsFromTemplates failed: %s", tostring(result)))
		end
	end

	if type(session_ids) ~= "table" or #session_ids == 0 then
		session_ids = {}
		for i = 1, count do
			local session_id = string.format("%s_%d", base, i)
			local ok, err = pcall(CreateUnitData, unit_template, session_id, InteractionRand(nil, "JAZZ_LegionRecruit"))
			if ok and gv_UnitData[session_id] then
				session_ids[#session_ids + 1] = session_id
			else
				lLog(string.format("CreateUnitData recruit failed: %s", tostring(err)))
			end
		end
	end

	for _, session_id in ipairs(session_ids) do
		if gv_UnitData[session_id] and AddUnitToSquad then
			AddUnitToSquad(squad.UniqueId, session_id, false, true)
			added[#added + 1] = session_id
		end
	end
	if #added > 0 then
		ObjModified(gv_Squads)
		ObjModified(squad)
	end
	return added
end

-- Despawn recruited units still in the squad. Returns how many were removed.
local function lStripRecruitedUnits(squad, recruited_ids, limit)
	local removed = 0
	local keep = {}
	limit = limit or 100000
	for _, session_id in ipairs(recruited_ids or empty_table) do
		local ud = gv_UnitData[session_id]
		if ud and squad and table.find(squad.units, session_id) then
			if removed < limit then
				RemoveUnitFromSquad(ud, "despawn")
				removed = removed + 1
			else
				keep[#keep + 1] = session_id
			end
		end
	end
	return removed, keep
end

-- All recruit cargo currently in the squad (tracked ids + any JAZZ_Legion_Recruit present).
local function lGatherRecruitCargoIds(squad, tracked_ids, unit_template)
	unit_template = unit_template or "JAZZ_Legion_Recruit"
	local ids = {}
	local seen = {}
	for _, session_id in ipairs(tracked_ids or empty_table) do
		if squad and table.find(squad.units, session_id) and not seen[session_id] then
			ids[#ids + 1] = session_id
			seen[session_id] = true
		end
	end
	for _, session_id in ipairs(squad and squad.units or empty_table) do
		if not seen[session_id] then
			local ud = gv_UnitData[session_id]
			local class_id = ud and (ud.class or ud.unitdatadef_id or ud.species)
			if class_id == unit_template then
				ids[#ids + 1] = session_id
				seen[session_id] = true
			end
		end
	end
	return ids
end

local function lSpawnManaged(root, region, home_sector, role, origin_sector, missions_left, payload, unit_template_ids)
	-- STRATEGY-019: map-wide new-spawn budget (idle reuse does not call this).
	if not lCanConsumeGlobalSpawn(root) then
		return false
	end
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
	local image = lRoleImages[role] or false
	-- Mirror diamond/weapon shipment: image must exist before SquadSpawned → SpawnSquadIcon.
	g_JAZZ_LegionAIPendingSquadImage = image
	g_JAZZ_LegionAISpawning = true
	local squad_id = GenerateEnemySquad(squad_def_id, origin_sector, base_session_id, unit_template_ids, "enemy1")
	g_JAZZ_LegionAISpawning = false
	g_JAZZ_LegionAIPendingSquadImage = false
	local squad = squad_id and gv_Squads[squad_id]
	if not squad then
		return false
	end
	lConsumeGlobalSpawn(root)
	if (role == "shipment" or role == "supply") and lPayloadMoney(payload) > 0 then
		if not lEnsureMoneyCargo(squad, lPayloadMoney(payload)) then
			lLog(string.format("%s spawned without valuables matching payload $; squad retired", role))
			RemoveSquad(squad)
			return false
		end
	end

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
	if rawget(_G, "JAZZ_SetSquadFaction") then
		JAZZ_SetSquadFaction(squad, "legion")
	end
	lApplySquadRoleIcon(squad, role)
	Msg("JAZZ_LegionAISquadManaged", squad_id, role, home_sector)
	return squad_id, root.squads[squad_id]
end

local function lRetireSquad(root, squad_id)
	local squad_state = root.squads[squad_id]
	local squad = gv_Squads[squad_id]
	if squad_state then
		squad_state.state = "retired"
	end
	if not squad then
		if root.squads then
			root.squads[squad_id] = nil
		end
		return
	end
	-- Immediate remove on the calling sync path. Do NOT defer via RealTimeThread
	-- (MP desync vs other NetSync) or GameTimeThread (may not tick in satellite).
	RemoveSquad(squad)
	if type(root) == "table" and root.squads then
		root.squads[squad_id] = nil
	end
end

local function lSquadLivingUnitInfos(squad)
	local templates = {}
	local living = 0
	local wounded = 0
	for _, session_id in ipairs(squad.units or empty_table) do
		local ud = gv_UnitData[session_id]
		if ud then
			local dead = (ud.HitPoints or 0) <= 0 or (ud.IsDead and ud:IsDead())
			if not dead then
				living = living + 1
				local template = ud.class or ud.unitdatadef_id or ud.species
				templates[#templates + 1] = template
				local low_hp = (ud.MaxHitPoints or 0) > 0
					and (ud.HitPoints or 0) < MulDivRound(ud.MaxHitPoints, 50, 100)
				local has_wound = ud.HasStatusEffect and ud:HasStatusEffect("Wounded")
				if low_hp or has_wound then
					wounded = wounded + 1
				end
			end
		end
	end
	return living, wounded, templates
end

local function lPurgeDeadAndHealSquad(squad)
	if not squad then
		return
	end
	local to_remove = {}
	for _, session_id in ipairs(squad.units or empty_table) do
		local ud = gv_UnitData[session_id]
		if ud then
			local dead = (ud.HitPoints or 0) <= 0 or (ud.IsDead and ud:IsDead())
			if dead then
				to_remove[#to_remove + 1] = session_id
			else
				ud.HitPoints = ud.MaxHitPoints or ud.HitPoints
				if ud.RemoveStatusEffect then
					ud:RemoveStatusEffect("Wounded")
				end
			end
		end
	end
	for _, session_id in ipairs(to_remove) do
		local ud = gv_UnitData[session_id]
		if ud and RemoveUnitFromSquad then
			RemoveUnitFromSquad(ud)
		end
	end
end

local function lSquadNeedsWoundedRetreat(squad, role)
	if not squad or not JAZZ_GetLegionRoleMinSize then
		return false
	end
	local min_size = JAZZ_GetLegionRoleMinSize(role) or 1
	local living, wounded = lSquadLivingUnitInfos(squad)
	if living <= 0 then
		return true
	end
	if living < min_size then
		return true
	end
	if wounded >= Max(1, DivRound(living, 2)) then
		return true
	end
	return false
end

local function lTryTopUpSquad(root, region, outpost, squad, squad_state)
	if not squad or not squad_state or not outpost or not JAZZ_GenerateLegionSquadTopUp then
		return false
	end
	if squad.CurrentSector ~= squad_state.home_sector then
		return false
	end
	local living, _, templates = lSquadLivingUnitInfos(squad)
	local optimal = JAZZ_GetLegionRoleOptimalSize(squad_state.role) or living
	if living >= optimal then
		return false
	end
	local topup = JAZZ_GenerateLegionSquadTopUp(
		templates,
		squad_state.role,
		outpost.money or 0,
		outpost.manpower,
		squad_state.role .. "_refit_" .. tostring(squad.UniqueId) .. "_" .. tostring(root.spawn_serial),
		JAZZ_GetLegionSquadGrowthProgress and JAZZ_GetLegionSquadGrowthProgress(
			root.regions[squad_state.region_id] and root.regions[squad_state.region_id].heat
		) or 0
	)
	if not topup or #(topup.units or empty_table) == 0 then
		return false
	end
	if (outpost.money or 0) < (topup.money_cost or 0) then
		return false
	end
	if outpost.manpower ~= nil and (outpost.manpower or 0) < (topup.manpower_cost or 0) then
		return false
	end
	AddUnitsToSquad(squad, topup.units, nil, InteractionRand(nil, "JAZZ_LegionRefit"))
	outpost.money = (outpost.money or 0) - (topup.money_cost or 0)
	if outpost.manpower ~= nil then
		outpost.manpower = Max((outpost.manpower or 0) - (topup.manpower_cost or 0), 0)
	end
	ObjModified(squad)
	Msg("JAZZ_LegionAISquadRefit", squad.UniqueId, topup.manpower_cost, topup.money_cost)
	return true
end

local function lRefreshMissions(squad_state, region)
	if not squad_state then
		return
	end
	local missions_key = lRoleMissions[squad_state.role]
	if missions_key then
		squad_state.missions_left = Max(1, lConfig(region, missions_key, 1))
	else
		-- Logistics / one-shot roles: one order per outing.
		squad_state.missions_left = 1
	end
end

local function lRandDuration(min_t, max_t, context)
	min_t = min_t or 0
	max_t = max_t or min_t
	if max_t < min_t then
		min_t, max_t = max_t, min_t
	end
	local span = max_t - min_t
	if span <= 0 then
		return min_t
	end
	return min_t + InteractionRand(span + 1, context)
end

-- After mission budget (or logistics delivery): heal/top-up, then mandatory rest
-- at home for all roles except garrison. Empty squads still retire.
local function lBeginBaseRest(root, squad, squad_state)
	if not squad or not squad_state then
		return false
	end
	lPurgeDeadAndHealSquad(squad)
	local living = lSquadLivingUnitInfos(squad)
	if living <= 0 then
		lRetireSquad(root, squad.UniqueId)
		return true
	end
	squad_state.task = false
	local region = lGetRegionPreset(squad_state.region_id)
	local outpost = root.outposts[squad_state.home_sector]
	if outpost and lRegularRoles[squad_state.role] then
		lTryTopUpSquad(root, region, outpost, squad, squad_state)
		living = lSquadLivingUnitInfos(squad)
		if living <= 0 then
			lRetireSquad(root, squad.UniqueId)
			return true
		end
		local optimal = JAZZ_GetLegionRoleOptimalSize and JAZZ_GetLegionRoleOptimalSize(squad_state.role) or living
		if living < optimal then
			squad_state.state = "wounded"
			squad_state.rest_until = nil
			ObjModified(squad)
			return true
		end
	end
	if squad_state.role == "garrison" then
		lRefreshMissions(squad_state, region)
		squad_state.state = "ready_for_orders"
		squad_state.rest_until = nil
		ObjModified(squad)
		return true
	end
	local min_t = lConfig(region, "BaseRestMin", 12 * lHourScale())
	local max_t = lConfig(region, "BaseRestMax", 36 * lHourScale())
	squad_state.state = "resting"
	squad_state.rest_until = lNow() + lRandDuration(
		min_t,
		max_t,
		"JAZZ_Rest_" .. tostring(squad.UniqueId) .. "_" .. tostring(root.spawn_serial or 0)
	)
	ObjModified(squad)
	return true
end

local function lFinishBaseRest(root, squad, squad_state)
	if not squad or not squad_state then
		return false
	end
	local region = lGetRegionPreset(squad_state.region_id)
	local outpost = root.outposts[squad_state.home_sector]
	if outpost and lRegularRoles[squad_state.role] then
		lPurgeDeadAndHealSquad(squad)
		lTryTopUpSquad(root, region, outpost, squad, squad_state)
		local living = lSquadLivingUnitInfos(squad)
		if living <= 0 then
			lRetireSquad(root, squad.UniqueId)
			return true
		end
		local optimal = JAZZ_GetLegionRoleOptimalSize and JAZZ_GetLegionRoleOptimalSize(squad_state.role) or living
		if living < optimal then
			squad_state.state = "wounded"
			squad_state.rest_until = nil
			ObjModified(squad)
			return true
		end
	end
	lRefreshMissions(squad_state, region)
	squad_state.state = "ready_for_orders"
	squad_state.rest_until = nil
	ObjModified(squad)
	return true
end

local function lEnterBaseRefit(root, squad, squad_state)
	-- Budget return / logistics park: rest cycle (garrison skips timer).
	return lBeginBaseRest(root, squad, squad_state)
end

local function lBeginReturn(root, squad, squad_state, reason)
	if not squad or not squad_state then
		return false
	end
	reason = reason or "rest"
	if squad.CurrentSector == squad_state.home_sector then
		if reason == "wounded" then
			lPurgeDeadAndHealSquad(squad)
			local living = lSquadLivingUnitInfos(squad)
			if living <= 0 then
				lRetireSquad(root, squad.UniqueId)
				return true
			end
			local region = lGetRegionPreset(squad_state.region_id)
			local outpost = root.outposts[squad_state.home_sector]
			if outpost then
				lTryTopUpSquad(root, region, outpost, squad, squad_state)
			end
			living = lSquadLivingUnitInfos(squad)
			local optimal = JAZZ_GetLegionRoleOptimalSize and JAZZ_GetLegionRoleOptimalSize(squad_state.role) or living
			if living > 0 and living < optimal then
				squad_state.task = false
				squad_state.state = "wounded"
				ObjModified(squad)
				return true
			end
		end
		return lBeginBaseRest(root, squad, squad_state)
	end
	squad_state.task = {
		task_type = reason == "wounded" and "return_wounded" or "return",
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
		return lBeginReturn(root, squad, squad_state, reason)
	end
	return true
end

local function lCompleteRegularTask(root, squad, squad_state)
	squad_state.missions_left = Max((squad_state.missions_left or 1) - 1, 0)
	squad_state.task = false
	if squad_state.missions_left <= 0 then
		return lBeginReturn(root, squad, squad_state, "rest")
	end
	squad_state.state = "ready_for_orders"
	ObjModified(squad)
	return true
end

local function lFindIdleHomeRole(root, home_sector, role)
	if not home_sector or not role then
		return false, false
	end
	for squad_id, squad_state in sorted_pairs(root.squads) do
		if squad_state.home_sector == home_sector
			and squad_state.role == role
			and squad_state.state == "ready_for_orders"
			and (squad_state.missions_left or 0) > 0
		then
			local squad = gv_Squads[squad_id]
			if squad
				and squad.CurrentSector == home_sector
				and not IsSquadTravelling(squad, "skip_tick_pass")
				and not IsConflictMode(squad.CurrentSector)
			then
				return squad, squad_state
			end
		end
	end
	return false, false
end

local function lPatrolDwellDuration(region, squad)
	local min_t = lConfig(region, "PatrolSectorDwellMin", 6 * lHourScale())
	local max_t = lConfig(region, "PatrolSectorDwellMax", 24 * lHourScale())
	return lRandDuration(
		min_t,
		max_t,
		"JAZZ_PatrolDwell_" .. tostring(squad and squad.UniqueId or 0)
	)
end

local function lBuildPatrolPath(squad, target_sector)
	local route = lRoutePath(squad, target_sector)
	if not route then
		return false
	end
	local path = {}
	for _, sector_id in ipairs(route) do
		path[#path + 1] = sector_id
	end
	if #path == 0 or path[#path] ~= target_sector then
		path[#path + 1] = target_sector
	end
	return path
end

local function lStartPatrolSectorDwell(root, squad, squad_state)
	local task = squad_state.task
	local region = lGetRegionPreset(squad_state.region_id)
	if not task then
		return false
	end
	task.task_type = "patrol_dwell"
	task.hold_until = lNow() + lPatrolDwellDuration(region, squad)
	squad_state.state = "working"
	ObjModified(squad)
	return true
end

local function lAdvancePatrolAfterDwell(root, squad, squad_state)
	local task = squad_state.task
	if not task then
		return lCompleteRegularTask(root, squad, squad_state)
	end
	local region_state = root.regions[squad_state.region_id]
	if region_state then
		region_state.last_patrolled = region_state.last_patrolled or {}
		region_state.last_patrolled[squad.CurrentSector] = lNow()
	end
	task.path_index = (task.path_index or 1) + 1
	local path = task.path or empty_table
	if task.path_index > #path then
		return lCompleteRegularTask(root, squad, squad_state)
	end
	task.target_sector = path[task.path_index]
	task.task_type = "patrol"
	task.hold_until = nil
	squad_state.state = "en_route"
	ObjModified(squad)
	local routed = lSetRoute(squad, task.target_sector)
	if not routed then
		squad_state.state = "orphaned"
		ObjModified(squad)
		return false
	elseif routed == "arrived" then
		lStartPatrolSectorDwell(root, squad, squad_state)
	end
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

	if task.task_type == "return" or task.task_type == "return_wounded" then
		local cargo = lPayloadMoney(squad_state.payload)
		if squad_state.role == "supply" and cargo > 0 then
			lAddMajorMoney(root, lGetRegionPreset(squad_state.region_id), cargo)
			squad_state.payload.money = 0
			lClearTaggedMoneyCargo(squad)
		end
		if squad_state.role == "manpower" then
			local region = lGetRegionPreset(squad_state.region_id)
			local recruited = lGatherRecruitCargoIds(
				squad,
				squad_state.payload and squad_state.payload.recruited_ids,
				lRecruitUnitTemplate(region)
			)
			local delivered = select(1, lStripRecruitedUnits(squad, recruited))
			if delivered <= 0 then
				delivered = squad_state.payload and squad_state.payload.manpower or 0
			end
			if delivered > 0 then
				lAddMajorManpower(root, region, delivered)
			end
			if squad_state.payload then
				squad_state.payload.manpower = 0
				squad_state.payload.recruited_ids = {}
			end
		end
		lBeginReturn(root, squad, squad_state, task.task_type == "return_wounded" and "wounded" or "rest")
	elseif squad_state.role == "patrol" then
		lStartPatrolSectorDwell(root, squad, squad_state)
	elseif squad_state.role == "recon" and (task.task_type == "garrison" or task.task_type == "reinforce") then
		squad_state.state = "working"
		task.hold_until = lNow() + lInterval(lGetRegionPreset(squad_state.region_id), "CommandInterval", 12 * lHourScale())
	elseif squad_state.role == "qrf" and (task.task_type == "garrison" or task.task_type == "reinforce") then
		squad_state.state = "working"
		task.hold_until = lNow() + lInterval(lGetRegionPreset(squad_state.region_id), "CommandInterval", 12 * lHourScale())
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
			outpost.money = Min(
				(outpost.money or 0) + lPayloadMoney(squad_state.payload),
				lOutpostMoneyCapacity(region)
			)
			squad_state.payload.money = 0
			lClearTaggedMoneyCargo(squad)
			lNoteMajorDelivery(outpost)
			lSyncSharedOutpostResources(root, region, outpost)
		end
		-- Park/rest at Major HQ after delivery (home becomes HQ).
		squad_state.home_sector = root.major.hq_sector
		lBeginReturn(root, squad, squad_state, "rest")
	elseif squad_state.role == "shipment" then
		local hq = gv_Sectors[root.major.hq_sector]
		if hq and JAZZ_IsLegionSide(hq.Side) then
			lAddMajorMoney(root, lGetRegionPreset(squad_state.region_id), lPayloadMoney(squad_state.payload))
			squad_state.payload.money = 0
			lClearTaggedMoneyCargo(squad)
			lBeginReturn(root, squad, squad_state, "rest")
		else
			squad_state.state = "working"
		end
	elseif squad_state.role == "tax" then
		local region_state = root.regions[squad_state.region_id]
		local region = lGetRegionPreset(squad_state.region_id)
		local outpost = root.outposts[squad_state.home_sector]
		local circuit = task.circuit or empty_table
		local index = task.circuit_index or 1
		if index <= #circuit and squad.CurrentSector == circuit[index] then
			local cargo_max = lConfig(region, "TaxCargoMax", 12000)
			local have = lPayloadMoney(squad_state.payload)
			local room = Max(0, cargo_max - have)
			local stock = region_state.poi_money[circuit[index]] or 0
			local collected = Min(stock, room)
			region_state.poi_money[circuit[index]] = stock - collected
			squad_state.payload = squad_state.payload or {}
			squad_state.payload.money = have + collected
			if collected > 0 or (have + collected) > 0 then
				if not lSyncMoneyCargo(squad, squad_state.payload.money) then
					lLog(string.format("tax cargo sync failed at %s ($%d)", tostring(circuit[index]), squad_state.payload.money))
				end
			end
			task.circuit_index = index + 1
			-- Stop circuit early when cargo is full.
			local full = (have + collected) >= cargo_max
			if not full and task.circuit_index <= #circuit then
				task.target_sector = circuit[task.circuit_index]
				squad_state.state = "en_route"
				ObjModified(squad)
				local routed = lSetRoute(squad, task.target_sector)
				if not routed then
					squad_state.state = "orphaned"
				elseif routed == "arrived" then
					lOnSquadArrived(root, squad, squad_state)
				end
			else
				task.target_sector = squad_state.home_sector
				task.task_type = "tax_return"
				squad_state.state = "en_route"
				ObjModified(squad)
				local routed = lSetRoute(squad, squad_state.home_sector)
				if not routed then
					squad_state.state = "orphaned"
				elseif routed == "arrived" then
					lOnSquadArrived(root, squad, squad_state)
				end
			end
		elseif task.task_type == "tax_return" and squad.CurrentSector == squad_state.home_sector then
			if outpost then
				outpost.money = Min(
					(outpost.money or 0) + lPayloadMoney(squad_state.payload),
					lOutpostMoneyCapacity(region)
				)
				squad_state.payload.money = 0
				lClearTaggedMoneyCargo(squad)
				lSyncSharedOutpostResources(root, region, outpost)
			end
			squad_state.missions_left = 0
			lBeginBaseRest(root, squad, squad_state)
		end
	elseif squad_state.role == "recruiter" then
		local region_state = root.regions[squad_state.region_id]
		local region = lGetRegionPreset(squad_state.region_id)
		local outpost = root.outposts[squad_state.home_sector]
		local circuit = task.circuit or empty_table
		local index = task.circuit_index or 1
		if index <= #circuit and squad.CurrentSector == circuit[index] then
			local cargo_max = lConfig(region, "RecruiterCargoMax", 16)
			squad_state.payload = squad_state.payload or {}
			squad_state.payload.recruited_ids = squad_state.payload.recruited_ids or {}
			local have = #(squad_state.payload.recruited_ids)
			local room = lSquadRecruitRoom(squad, cargo_max, have)
			local stock = region_state.poi_recruits[circuit[index]] or 0
			local want = Min(stock, room)
			local added = lAddRecruitUnitsToSquad(
				root,
				squad,
				want,
				lRecruitUnitTemplate(region),
				"poi_" .. tostring(circuit[index])
			)
			for _, session_id in ipairs(added) do
				squad_state.payload.recruited_ids[#squad_state.payload.recruited_ids + 1] = session_id
			end
			local collected = #added
			if want > 0 and collected <= 0 then
				lLog(string.format(
					"recruiter %s failed to materialize %d recruits at %s (stock=%d room=%d)",
					tostring(squad.UniqueId),
					want,
					tostring(circuit[index]),
					stock,
					room
				))
			end
			region_state.poi_recruits[circuit[index]] = Max(0, stock - collected)
			squad_state.payload.manpower = #(squad_state.payload.recruited_ids)
			task.circuit_index = index + 1
			local full = #(squad_state.payload.recruited_ids) >= cargo_max
				or lSquadRecruitRoom(squad, cargo_max, #(squad_state.payload.recruited_ids)) <= 0
			if not full and task.circuit_index <= #circuit then
				task.target_sector = circuit[task.circuit_index]
				squad_state.state = "en_route"
				ObjModified(squad)
				local routed = lSetRoute(squad, task.target_sector)
				if not routed then
					squad_state.state = "orphaned"
				elseif routed == "arrived" then
					lOnSquadArrived(root, squad, squad_state)
				end
			else
				task.target_sector = squad_state.home_sector
				task.task_type = "recruiter_return"
				squad_state.state = "en_route"
				ObjModified(squad)
				local routed = lSetRoute(squad, squad_state.home_sector)
				if not routed then
					squad_state.state = "orphaned"
				elseif routed == "arrived" then
					lOnSquadArrived(root, squad, squad_state)
				end
			end
		elseif task.task_type == "recruiter_return" and squad.CurrentSector == squad_state.home_sector then
			if outpost then
				local capacity = lConfig(region, "ManpowerCapacity", 32)
				local room = Max(0, capacity - (outpost.manpower or 0))
				local recruit_template = lRecruitUnitTemplate(region)
				local recruited = lGatherRecruitCargoIds(
					squad,
					squad_state.payload and squad_state.payload.recruited_ids,
					recruit_template
				)
				local delivered, leftover = lStripRecruitedUnits(squad, recruited, room)
				-- Overflow recruits still on squad → outbound queue, then strip rest.
				if #leftover > 0 then
					local overflow = select(1, lStripRecruitedUnits(squad, leftover, #leftover))
					outpost.outbound_manpower = (outpost.outbound_manpower or 0) + overflow
				elseif delivered <= 0 and (squad_state.payload and squad_state.payload.manpower or 0) > 0 then
					-- Legacy abstract payload fallback.
					delivered = Min(room, squad_state.payload.manpower or 0)
					local overflow = Max(0, (squad_state.payload.manpower or 0) - delivered)
					outpost.outbound_manpower = (outpost.outbound_manpower or 0) + overflow
				end
				outpost.manpower = Min((outpost.manpower or 0) + delivered, capacity)
				lSyncSharedOutpostResources(root, region, outpost)
				lLog(string.format(
					"recruiter %s deposited %d manpower at %s (now %d, outbound %d); resting",
					tostring(squad.UniqueId),
					delivered,
					tostring(outpost.sector_id),
					outpost.manpower or 0,
					outpost.outbound_manpower or 0
				))
				if squad_state.payload then
					squad_state.payload.manpower = 0
					squad_state.payload.recruited_ids = {}
				end
				ObjModified(squad)
			end
			squad_state.missions_left = 0
			lBeginBaseRest(root, squad, squad_state)
		end
	elseif squad_state.role == "manpower" then
		local outpost = root.outposts[squad_state.home_sector]
		local region = lGetRegionPreset(squad_state.region_id)
		if task.task_type == "manpower_outbound" then
			local hq = root.major.hq_sector and gv_Sectors[root.major.hq_sector]
			if hq and JAZZ_IsLegionSide(hq.Side) and squad.CurrentSector == root.major.hq_sector then
				local recruited = lGatherRecruitCargoIds(
					squad,
					squad_state.payload and squad_state.payload.recruited_ids,
					lRecruitUnitTemplate(region)
				)
				local delivered = select(1, lStripRecruitedUnits(squad, recruited))
				if delivered <= 0 then
					delivered = squad_state.payload and squad_state.payload.manpower or 0
				end
				lAddMajorManpower(root, region, delivered)
				if squad_state.payload then
					squad_state.payload.manpower = 0
					squad_state.payload.recruited_ids = {}
				end
				-- Return to outpost home for rest (home_sector stays outpost).
				lBeginReturn(root, squad, squad_state, "rest")
			else
				squad_state.state = "orphaned"
			end
		else
			local outpost_sector = outpost and gv_Sectors[outpost.sector_id]
			local delivered_ok = outpost
				and outpost.enabled
				and outpost_sector
				and JAZZ_IsLegionSide(outpost_sector.Side)
			if delivered_ok then
				local capacity = lConfig(region, "ManpowerCapacity", 32)
				local room = Max(0, capacity - (outpost.manpower or 0))
				local recruited = lGatherRecruitCargoIds(
					squad,
					squad_state.payload and squad_state.payload.recruited_ids,
					lRecruitUnitTemplate(region)
				)
				local deposited, leftover = lStripRecruitedUnits(squad, recruited, room)
				if deposited <= 0 and (squad_state.payload.manpower or 0) > 0 then
					deposited = Min(room, squad_state.payload.manpower or 0)
					squad_state.payload.manpower = Max(0, (squad_state.payload.manpower or 0) - deposited)
				else
					squad_state.payload = squad_state.payload or {}
					squad_state.payload.recruited_ids = leftover
					squad_state.payload.manpower = #leftover
				end
				outpost.manpower = Min((outpost.manpower or 0) + deposited, capacity)
				if deposited > 0 then
					lNoteMajorDelivery(outpost)
					lSyncSharedOutpostResources(root, region, outpost)
				end
			end
			squad_state.home_sector = root.major.hq_sector
			lBeginReturn(root, squad, squad_state, "rest")
		end
	elseif squad_state.role == "garrison" or squad_state.role == "reinforce"
		or task.task_type == "garrison" or task.task_type == "reinforce"
	then
		squad_state.state = "working"
		task.hold_until = lNow() + lInterval(lGetRegionPreset(squad_state.region_id), "CommandInterval", 12 * lHourScale())
	elseif squad_state.role == "qrf" or squad_state.role == "major" then
		squad_state.state = "working"
		task.hold_until = lNow() + lInterval(lGetRegionPreset(squad_state.region_id), "CommandInterval", 12 * lHourScale())
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
	local task = {
		task_type = task_type,
		target_sector = request.target_sector,
		observed_sector = request.observed_sector,
		report_id = request.report_id,
	}
	if task_type == "patrol" then
		local path = lBuildPatrolPath(squad, request.target_sector)
		if not path or #path == 0 then
			return false
		end
		task.path = path
		task.path_index = 1
		task.target_sector = path[1]
		task.task_type = "patrol"
	end
	squad_state.task = task
	squad_state.state = "en_route"
	local routed = lSetRoute(squad, task.target_sector)
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
	Msg("JAZZ_LegionAITaskAssigned", squad.UniqueId, task.task_type, task.target_sector)
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
	elseif role == "reinforce" then
		local target = lReinforceTarget(root, region, region_state)
		return target and { task_type = "reinforce", target_sector = target }
	end
	return false
end

local function lIdleAssistRequest(root, region, region_state, role)
	-- Only recon/QRF may assist garrison when they have nothing else to do.
	if role ~= "recon" and role ~= "qrf" then
		return false
	end
	local garrison = lGarrisonTarget(root, region, region_state)
	if garrison then
		return { task_type = "garrison", target_sector = garrison }
	end
	local reinforce = lReinforceTarget(root, region, region_state)
	if reinforce then
		return { task_type = "reinforce", target_sector = reinforce }
	end
	return false
end

local function lAssignReadySquads(root, region, region_state, outpost)
	for squad_id, squad_state in sorted_pairs(root.squads) do
		if squad_state.home_sector == outpost.sector_id
		and lRegularRoles[squad_state.role]
		and (squad_state.state == "ready_for_orders"
			or squad_state.state == "wounded"
			or squad_state.state == "resting")
		then
			local squad = gv_Squads[squad_id]
			if squad and not IsSquadTravelling(squad, "skip_tick_pass") and not IsConflictMode(squad.CurrentSector) then
				if squad.CurrentSector == outpost.sector_id then
					if squad_state.state == "resting" then
						if (squad_state.rest_until or 0) <= lNow() then
							lFinishBaseRest(root, squad, squad_state)
						end
					elseif squad_state.state == "wounded" or squad_state.state == "ready_for_orders" then
						lPurgeDeadAndHealSquad(squad)
						lTryTopUpSquad(root, region, outpost, squad, squad_state)
						local living = lSquadLivingUnitInfos(squad)
						local growth = JAZZ_GetLegionSquadGrowthProgress and JAZZ_GetLegionSquadGrowthProgress(
							root.regions[squad_state.region_id] and root.regions[squad_state.region_id].heat
						) or 0
						local optimal = JAZZ_GetLegionRoleOptimalSize and JAZZ_GetLegionRoleOptimalSize(squad_state.role, growth) or living
						if living <= 0 then
							lRetireSquad(root, squad_id)
						elseif living < optimal then
							squad_state.state = "wounded"
							squad_state.task = false
							ObjModified(squad)
						elseif squad_state.state == "wounded" then
							-- Healed/topped to optimal after wounded wait → mandatory rest before new orders.
							lBeginBaseRest(root, squad, squad_state)
						end
					end
				end
				if squad_state.state == "ready_for_orders" and (squad_state.missions_left or 0) > 0 then
					local request = lRoleRequest(root, region, region_state, outpost, squad, squad_state.role)
					if not request then
						request = lIdleAssistRequest(root, region, region_state, squad_state.role)
					end
					if request then
						lAssignTask(root, region, region_state, outpost, squad, squad_state, request)
					end
					-- else: sit idle at base — no despawn
				elseif squad_state.state == "ready_for_orders" and (squad_state.missions_left or 0) <= 0 then
					lBeginReturn(root, squad, squad_state, "rest")
				end
			end
		end
	end
end

local function lSpawnRegularRole(root, region, region_state, outpost, role)
	if role == "qrf" and lRegionDormant(region) then
		return false
	end
	if not lOutpostCanSpawn(outpost) then
		return false
	end
	local total_cap = lConfig(region, "RegularSquadCap", 7)
	local role_cap = role == "garrison" and lGarrisonCap(region) or lConfig(region, lRoleCaps[role], 0)
	if role == "garrison" then
		if lCountRegionRole(root, region_state.region_id, "garrison") >= role_cap then
			return false
		end
	elseif lCountRegular(root, outpost.sector_id) >= total_cap
		or lCountRegular(root, outpost.sector_id, role) >= role_cap
	then
		return false
	end

	local mock_squad = { CurrentSector = outpost.sector_id, UniqueId = root.spawn_serial }
	local request = lRoleRequest(root, region, region_state, outpost, mock_squad, role)
	if not request then
		return false
	end

	local unit_templates = false
	local money_cost = lConfig(region, lRoleCosts[role], 0)
	local manpower_cost = 0
	local growth = JAZZ_GetLegionSquadGrowthProgress and JAZZ_GetLegionSquadGrowthProgress(region_state.heat) or 0
	if JAZZ_LegionRoleUsesCompositionGenerator and JAZZ_LegionRoleUsesCompositionGenerator(role)
		and not (JAZZ_LegionRoleIsLogisticsEscort and JAZZ_LegionRoleIsLogisticsEscort(role))
	then
		local composition = JAZZ_GenerateLegionSquadComposition(
			role,
			outpost.money or 0,
			outpost.manpower or 0,
			"auto",
			role .. "_" .. outpost.sector_id .. "_" .. tostring(root.spawn_serial),
			growth
		)
		-- No free EnemySquadDef fallback: combat roles always spend $ + manpower.
		if not composition then
			return false
		end
		unit_templates = composition.units
		money_cost = composition.money_cost or 0
		manpower_cost = composition.manpower_cost or #(composition.units or empty_table)
	elseif (outpost.money or 0) < money_cost then
		return false
	end
	if (outpost.money or 0) < money_cost then
		return false
	end
	if (outpost.manpower or 0) < manpower_cost then
		return false
	end

	local missions = lConfig(region, lRoleMissions[role], 1)
	local squad_id, squad_state = lSpawnManaged(
		root,
		region,
		outpost.sector_id,
		role,
		outpost.sector_id,
		missions,
		nil,
		unit_templates
	)
	local squad = squad_id and gv_Squads[squad_id]
	if not squad then
		return false
	end
	-- STRATEGY-018: reinforce may spawn without a valid avoid-player route (hold).
	local assigned = lAssignTask(root, region, region_state, outpost, squad, squad_state, request)
	if not assigned then
		if role == "reinforce" then
			squad_state.state = "ready_for_orders"
			squad_state.task = false
			squad_state.hold_for_path = true
			lLog(string.format("reinforce at %s holding: no avoid-player path to target", tostring(outpost.sector_id)))
		else
			lRetireSquad(root, squad_id)
			return false
		end
	else
		squad_state.hold_for_path = nil
	end
	-- Charge actual living bodies if generator under-counted.
	local spawned = #(squad.units or empty_table)
	if spawned > manpower_cost then
		manpower_cost = spawned
	end
	if (outpost.manpower or 0) < manpower_cost then
		-- Should be rare (generator gated); retire rather than spawn free troops.
		lLog(string.format(
			"%s spawn at %s aborted after create: need %d manpower, have %d",
			tostring(role),
			tostring(outpost.sector_id),
			manpower_cost,
			outpost.manpower or 0
		))
		lRetireSquad(root, squad_id)
		return false
	end
	outpost.money = (outpost.money or 0) - money_cost
	outpost.manpower = Max((outpost.manpower or 0) - manpower_cost, 0)
	if squad_state then
		squad_state.spawn_money_cost = money_cost
		squad_state.spawn_manpower_cost = manpower_cost
	end
	lLog(string.format(
		"spawned %s at %s: -$%d -%d manpower (left $%d / %d people)",
		tostring(role),
		tostring(outpost.sector_id),
		money_cost,
		manpower_cost,
		outpost.money or 0,
		outpost.manpower or 0
	))
	lMarkOutpostSpawn(outpost)
	return true
end

local function lGrowthProgress(region_state)
	if JAZZ_GetLegionSquadGrowthProgress then
		return JAZZ_GetLegionSquadGrowthProgress(region_state and region_state.heat)
	end
	return 0
end

-- STRATEGY-016: logistics escorts use composition sizes (not full EnemySquadDef 15–25).
-- Soft $ budget — escorts are not charged money; templates only.
local function lEscortUnitTemplates(role, region_state, context)
	if not JAZZ_GenerateLegionSquadComposition then
		return false
	end
	local composition = JAZZ_GenerateLegionSquadComposition(
		role,
		100000,
		nil,
		"poor",
		context or role,
		lGrowthProgress(region_state)
	)
	return composition and composition.units or false
end

local function lTrySupplyConvoy(root, region, region_state, outpost)
	local capacity = lOutpostMoneyCapacity(region)
	local trigger = MulDivRound(capacity, lConfig(region, "SupplyConvoyTriggerPercent", 40), 100)
	local cargo = lConfig(region, "SupplyConvoyCargo", 12000)
	if (outpost.money or 0) >= trigger or (root.major.money or 0) < cargo then
		return false
	end
	-- STRATEGY-021: Major feeds the poorest outpost first.
	if not lIsNeediestSupplyOutpost(root, outpost) then
		return false
	end
	local hq_sector = root.major.hq_sector
	local hq = hq_sector and gv_Sectors[hq_sector]
	if not hq or not JAZZ_IsLegionSide(hq.Side) then
		return false
	end
	local function lDispatchSupply(squad, squad_state)
		squad_state.home_sector = outpost.sector_id
		squad_state.payload = squad_state.payload or {}
		squad_state.payload.money = cargo
		if not lEnsureMoneyCargo(squad, cargo) then
			lLog("supply reuse failed to load cargo $")
			return false
		end
		squad_state.task = { task_type = "supply", target_sector = outpost.sector_id }
		squad_state.state = "en_route"
		local routed = lSetRoute(squad, outpost.sector_id)
		if not routed then
			squad_state.task = false
			squad_state.state = "ready_for_orders"
			return false
		end
		root.major.money = (root.major.money or 0) - cargo
		ObjModified(squad)
		if routed == "arrived" then
			lOnSquadArrived(root, squad, squad_state)
		end
		return true
	end
	-- Prefer idle supply parked at HQ after previous rest.
	local idle_squad, idle_state = lFindIdleHomeRole(root, hq_sector, "supply")
	if idle_squad then
		return lDispatchSupply(idle_squad, idle_state)
	end
	if lActiveRole(root, region_state.region_id, outpost.sector_id, "supply")
		or lActiveRole(root, region_state.region_id, hq_sector, "supply")
	then
		return false
	end
	-- STRATEGY-018: do not spawn supply without avoid-player path HQ→outpost.
	if not lHasAvoidPlayerRoute(hq_sector, outpost.sector_id, "supply", "enemy1", empty_table) then
		return false
	end
	local squad_id, squad_state = lSpawnManaged(
		root, region, outpost.sector_id, "supply", hq_sector, 1, { money = cargo },
		lEscortUnitTemplates("supply", region_state, "supply_" .. outpost.sector_id)
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
	root.major.money = (root.major.money or 0) - cargo
	ObjModified(squad)
	if routed == "arrived" then lOnSquadArrived(root, squad, squad_state) end
	return true
end

local function lTryDiamondShipment(root, region, region_state, outpost)
	local threshold = lConfig(region, "DiamondShipmentThreshold", 12000)
	if (outpost.diamond_stock or 0) < threshold then
		return false
	end
	local hq_sector = root.major.hq_sector
	local hq = hq_sector and gv_Sectors[hq_sector]
	if not hq or not JAZZ_IsLegionSide(hq.Side) then
		return false
	end
	local function lDispatchShipment(squad, squad_state)
		squad_state.payload = squad_state.payload or {}
		squad_state.payload.money = threshold
		if not lEnsureMoneyCargo(squad, threshold) then
			lLog("shipment reuse failed to load valuables")
			return false
		end
		squad_state.task = { task_type = "shipment", target_sector = hq_sector }
		squad_state.state = "en_route"
		local routed = lSetRoute(squad, hq_sector)
		if not routed then
			squad_state.task = false
			squad_state.state = "ready_for_orders"
			return false
		end
		outpost.diamond_stock = outpost.diamond_stock - threshold
		ObjModified(squad)
		if routed == "arrived" then
			lOnSquadArrived(root, squad, squad_state)
		end
		return true
	end
	local idle_squad, idle_state = lFindIdleHomeRole(root, outpost.sector_id, "shipment")
	if idle_squad then
		return lDispatchShipment(idle_squad, idle_state)
	end
	if lActiveRole(root, region_state.region_id, outpost.sector_id, "shipment") then
		return false
	end
	-- STRATEGY-018: do not spawn shipment without avoid-player path outpost→HQ.
	if not lHasAvoidPlayerRoute(outpost.sector_id, hq_sector, "shipment", "enemy1", empty_table) then
		return false
	end
	local squad_id, squad_state = lSpawnManaged(
		root, region, outpost.sector_id, "shipment", outpost.sector_id, 1, { money = threshold },
		lEscortUnitTemplates("shipment", region_state, "shipment_" .. outpost.sector_id)
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

local function lCountHomeRole(root, home_sector, role)
	local count = 0
	for _, squad_state in sorted_pairs(root.squads) do
		if squad_state.home_sector == home_sector
			and squad_state.role == role
			and squad_state.state ~= "retired"
		then
			count = count + 1
		end
	end
	return count
end

local function lTaxCircuitSectors(region, region_state)
	local list = {}
	local total = 0
	for _, sector_id in ipairs(region.Sectors or empty_table) do
		local money = region_state.poi_money[sector_id] or 0
		if money > 0 then
			local sector = gv_Sectors[sector_id]
			if sector and JAZZ_IsLegionSide(sector.Side) and lSectorIsEconomicPOI(sector) then
				list[#list + 1] = sector_id
				total = total + money
			end
		end
	end
	table.sort(list)
	return list, total
end

local function lTryTaxCollector(root, region, region_state, outpost)
	if not lLogisticsOpen(outpost) then
		return false
	end
	local cooldown = lConfig(region, "TaxCooldown", 48 * lHourScale())
	if (outpost.last_tax_time or 0) + cooldown > lNow() then
		return false
	end
	local circuit, total = lTaxCircuitSectors(region, region_state)
	if total < lConfig(region, "TaxThreshold", 1000) or #circuit == 0 then
		return false
	end
	local function lDispatchTax(squad, squad_state)
		squad_state.payload = squad_state.payload or {}
		squad_state.payload.money = 0
		squad_state.task = {
			task_type = "tax",
			circuit = circuit,
			circuit_index = 1,
			target_sector = circuit[1],
		}
		squad_state.state = "en_route"
		local routed = lSetRoute(squad, circuit[1])
		if not routed then
			squad_state.task = false
			squad_state.state = "ready_for_orders"
			return false
		end
		outpost.last_tax_time = lNow()
		ObjModified(squad)
		if routed == "arrived" then
			lOnSquadArrived(root, squad, squad_state)
		end
		return true
	end
	local idle_squad, idle_state = lFindIdleHomeRole(root, outpost.sector_id, "tax")
	if idle_squad then
		return lDispatchTax(idle_squad, idle_state)
	end
	local cap = lConfig(region, "TaxCap", 1)
	if lCountHomeRole(root, outpost.sector_id, "tax") >= cap then
		return false
	end
	if not lHasAvoidPlayerRoute(outpost.sector_id, circuit[1], "tax", "enemy1", empty_table) then
		return false
	end
	local squad_id, squad_state = lSpawnManaged(
		root, region, outpost.sector_id, "tax", outpost.sector_id, 1, { money = 0 },
		lEscortUnitTemplates("tax", region_state, "tax_" .. outpost.sector_id)
	)
	local squad = squad_id and gv_Squads[squad_id]
	if not squad then
		return false
	end
	if not lDispatchTax(squad, squad_state) then
		lRetireSquad(root, squad_id)
		return false
	end
	return true
end

local function lRecruitCircuitSectors(region, region_state)
	local list = {}
	local total = 0
	for _, sector_id in ipairs(region.Sectors or empty_table) do
		local recruits = region_state.poi_recruits[sector_id] or 0
		if recruits > 0 then
			local sector = gv_Sectors[sector_id]
			if sector and JAZZ_IsLegionSide(sector.Side) and lSectorIsEconomicPOI(sector) then
				list[#list + 1] = sector_id
				total = total + recruits
			end
		end
	end
	table.sort(list)
	return list, total
end

local function lTryRecruiter(root, region, region_state, outpost)
	if not lLogisticsOpen(outpost) then
		return false
	end
	-- Late-awaken: recruiter only after first Major supply/manpower delivery.
	if lRegionLateAwakenMin(region) > 0 and not outpost.major_delivery_done then
		return false
	end
	local cooldown = lConfig(region, "RecruiterCooldown", 48 * lHourScale())
	if (outpost.last_recruiter_time or 0) + cooldown > lNow() then
		return false
	end
	local circuit, total = lRecruitCircuitSectors(region, region_state)
	if total < lConfig(region, "RecruiterThreshold", 8) or #circuit == 0 then
		return false
	end
	local function lDispatchRecruiter(squad, squad_state)
		squad_state.payload = squad_state.payload or {}
		squad_state.payload.manpower = 0
		squad_state.payload.recruited_ids = {}
		squad_state.task = {
			task_type = "recruiter",
			circuit = circuit,
			circuit_index = 1,
			target_sector = circuit[1],
		}
		squad_state.state = "en_route"
		local routed = lSetRoute(squad, circuit[1])
		if not routed then
			squad_state.task = false
			squad_state.state = "ready_for_orders"
			return false
		end
		outpost.last_recruiter_time = lNow()
		ObjModified(squad)
		if routed == "arrived" then
			lOnSquadArrived(root, squad, squad_state)
		end
		return true
	end
	local idle_squad, idle_state = lFindIdleHomeRole(root, outpost.sector_id, "recruiter")
	if idle_squad then
		return lDispatchRecruiter(idle_squad, idle_state)
	end
	local cap = lConfig(region, "RecruiterCap", 1)
	if lCountHomeRole(root, outpost.sector_id, "recruiter") >= cap then
		return false
	end
	if not lHasAvoidPlayerRoute(outpost.sector_id, circuit[1], "recruiter", "enemy1", empty_table) then
		return false
	end
	local squad_id, squad_state = lSpawnManaged(
		root, region, outpost.sector_id, "recruiter", outpost.sector_id, 1, { manpower = 0, recruited_ids = {} },
		lEscortUnitTemplates("recruiter", region_state, "recruiter_" .. outpost.sector_id)
	)
	local squad = squad_id and gv_Squads[squad_id]
	if not squad then
		return false
	end
	if not lDispatchRecruiter(squad, squad_state) then
		lRetireSquad(root, squad_id)
		return false
	end
	return true
end

local function lTryManpowerConvoy(root, region, region_state, outpost)
	-- Major → outpost only when the outpost has no manpower left.
	if (outpost.manpower or 0) > 0 then
		return false
	end
	-- STRATEGY-021: among empty outposts, feed the poorest $ first.
	if not lIsNeediestManpowerOutpost(root, outpost) then
		return false
	end
	if lActiveRole(root, region_state.region_id, outpost.sector_id, "manpower") then
		return false
	end
	local cargo = lConfig(region, "ManpowerConvoyCargo", 16)
	if (root.major.manpower or 0) < cargo then
		return false
	end
	local hq_sector = root.major.hq_sector
	local hq = hq_sector and gv_Sectors[hq_sector]
	if not hq or not JAZZ_IsLegionSide(hq.Side) then
		return false
	end
	if not lHasAvoidPlayerRoute(hq_sector, outpost.sector_id, "manpower", "enemy1", empty_table) then
		return false
	end
	local squad_id, squad_state = lSpawnManaged(
		root, region, outpost.sector_id, "manpower", hq_sector, 1, { manpower = 0, recruited_ids = {} },
		lEscortUnitTemplates("manpower", region_state, "manpower_in_" .. outpost.sector_id)
	)
	local squad = squad_id and gv_Squads[squad_id]
	if not squad then
		return false
	end
	local added = lAddRecruitUnitsToSquad(root, squad, cargo, lRecruitUnitTemplate(region), "inbound")
	if #added <= 0 then
		lLog(string.format("manpower inbound failed to spawn %d recruits", cargo))
		lRetireSquad(root, squad_id)
		return false
	end
	squad_state.payload.recruited_ids = added
	squad_state.payload.manpower = #added
	squad_state.task = { task_type = "manpower", target_sector = outpost.sector_id }
	squad_state.state = "en_route"
	local routed = lSetRoute(squad, outpost.sector_id)
	if not routed then
		lRetireSquad(root, squad_id)
		return false
	end
	root.major.manpower = Max((root.major.manpower or 0) - #added, 0)
	ObjModified(squad)
	if routed == "arrived" then
		lOnSquadArrived(root, squad, squad_state)
	end
	return true
end

-- Outpost surplus recruits → Major via the same manpower caravan role (reverse route).
local function lTryManpowerOutbound(root, region, region_state, outpost)
	if lActiveRole(root, region_state.region_id, outpost.sector_id, "manpower") then
		return false
	end
	local pending = outpost.outbound_manpower or 0
	if pending <= 0 then
		return false
	end
	local cargo_max = lConfig(region, "ManpowerConvoyCargo", 16)
	local cargo = Min(pending, cargo_max)
	if cargo <= 0 then
		return false
	end
	local hq_sector = root.major.hq_sector
	local hq = hq_sector and gv_Sectors[hq_sector]
	if not hq or not JAZZ_IsLegionSide(hq.Side) then
		return false
	end
	if not lHasAvoidPlayerRoute(outpost.sector_id, hq_sector, "manpower", "enemy1", empty_table) then
		return false
	end
	local squad_id, squad_state = lSpawnManaged(
		root, region, outpost.sector_id, "manpower", outpost.sector_id, 1, { manpower = 0, recruited_ids = {} },
		lEscortUnitTemplates("manpower", region_state, "manpower_out_" .. outpost.sector_id)
	)
	local squad = squad_id and gv_Squads[squad_id]
	if not squad then
		return false
	end
	local added = lAddRecruitUnitsToSquad(root, squad, cargo, lRecruitUnitTemplate(region), "outbound")
	if #added <= 0 then
		lLog(string.format("manpower outbound failed to spawn %d recruits", cargo))
		lRetireSquad(root, squad_id)
		return false
	end
	squad_state.payload.recruited_ids = added
	squad_state.payload.manpower = #added
	squad_state.task = {
		task_type = "manpower_outbound",
		target_sector = hq_sector,
	}
	squad_state.state = "en_route"
	local routed = lSetRoute(squad, hq_sector)
	if not routed then
		lRetireSquad(root, squad_id)
		return false
	end
	outpost.outbound_manpower = Max(0, pending - #added)
	ObjModified(squad)
	if routed == "arrived" then
		lOnSquadArrived(root, squad, squad_state)
	end
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
			if task.task_type == "patrol_dwell" then
				lAdvancePatrolAfterDwell(root, squad, squad_state)
			else
				local target = gv_Sectors[task.target_sector]
				local assist = task.task_type == "garrison" or task.task_type == "reinforce"
				if (squad_state.role == "garrison" or squad_state.role == "reinforce" or assist)
				and target and JAZZ_IsLegionSide(target.Side)
				then
					lCompleteRegularTask(root, squad, squad_state)
				elseif squad_state.role == "qrf" then
					if target and not lIsPlayerSide(target.Side) and not lPlayerSquadInSector(target.Id) then
						lCompleteRegularTask(root, squad, squad_state)
					elseif task.hold_until + lInterval(region, "CommandInterval", 12 * lHourScale()) <= lNow() then
						lCompleteRegularTask(root, squad, squad_state)
					end
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

	lClaimRegionOrphans(root, outpost)
	lRestoreOrphans(root, outpost)
	lRefreshRetakeTargets(region, outpost)
	lCompleteWorkingTasks(root, region, region_state, outpost)
	lAssignReadySquads(root, region, region_state, outpost)

	-- STRATEGY-019: tax/recruiter first, then combat fill, then supply logistics.
	-- Global spawn pool (tier 1/2/3 → 1/2/3 new lSpawnManaged / 24h) gates all new creates.
	lTryTaxCollector(root, region, region_state, outpost)
	lTryRecruiter(root, region, region_state, outpost)

	-- Need-gated fill: qrf/recon only with threat/noise; garrison only undefended
	-- key/POI; reinforce on player-adjacent borders; patrol if a target exists.
	-- Combat uses a shared 1/48h outpost spawn slot (STRATEGY-016).
	lSpawnRegularRole(root, region, region_state, outpost, "qrf")
	while lSpawnRegularRole(root, region, region_state, outpost, "garrison") do end
	lSpawnRegularRole(root, region, region_state, outpost, "reinforce")
	lSpawnRegularRole(root, region, region_state, outpost, "recon")
	while lSpawnRegularRole(root, region, region_state, outpost, "patrol") do end

	lTrySupplyConvoy(root, region, region_state, outpost)
	lTryDiamondShipment(root, region, region_state, outpost)
	lTryManpowerOutbound(root, region, region_state, outpost)
	lTryManpowerConvoy(root, region, region_state, outpost)
	-- STRATEGY-023: push spends/gains to sibling outposts.
	lSyncSharedOutpostResources(root, region, outpost)
end

local function lParalyzeOutpost(root, outpost)
	local region = lGetRegionPreset(outpost.region_id)
	local sibling_id, sibling = lFindEnabledSiblingOutpost(root, outpost.region_id, outpost.sector_id)
	if sibling then
		-- Merge treasury into surviving outpost, then rehome regular squads.
		local cap = lOutpostMoneyCapacity(region)
		sibling.money = Min((sibling.money or 0) + (outpost.money or 0), cap)
		sibling.manpower = (sibling.manpower or 0) + (outpost.manpower or 0)
		sibling.diamond_stock = (sibling.diamond_stock or 0) + (outpost.diamond_stock or 0)
		outpost.money = 0
		outpost.manpower = 0
		outpost.diamond_stock = 0
		lSyncSharedOutpostResources(root, region, sibling)
		for squad_id, squad_state in sorted_pairs(root.squads) do
			local squad = gv_Squads[squad_id]
			if squad_state.home_sector == outpost.sector_id and squad then
				if lRegularRoles[squad_state.role] then
					squad_state.home_sector = sibling_id
					squad_state.task = false
					squad_state.state = "ready_for_orders"
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
		outpost.enabled = false
		return
	end
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
	local legion_mines = 0
	for _, sector_id in ipairs(region.Sectors or empty_table) do
		local sector = gv_Sectors[sector_id]
		if sector and JAZZ_IsLegionSide(sector.Side) and sector.Mine then
			legion_mines = legion_mines + 1
		end
	end

	local shared = lRegionHasSharedOutposts(region)
	local income_outpost = false
	for sector_id in sorted_pairs(region_state.outposts) do
		local outpost = root.outposts[sector_id]
		local sector = gv_Sectors[sector_id]
		if outpost and outpost.enabled and sector and JAZZ_IsLegionSide(sector.Side) then
			if shared then
				income_outpost = income_outpost or outpost
			else
				-- Base passive stays on outpost; city/farm $ wait for tax pulse; mine → shipment stock.
				local income = lConfig(region, "PassiveSupplyPerHour", 0)
				income = DivRound(income, lDormantIncomeDiv(region))
				outpost.money = Min(
					(outpost.money or 0) + income,
					lOutpostMoneyCapacity(region)
				)
				local mine_income = legion_mines * lConfig(region, "MineDiamondPerHour", 250)
				mine_income = DivRound(mine_income, lDormantIncomeDiv(region))
				outpost.diamond_stock = (outpost.diamond_stock or 0) + mine_income
			end
		end
	end
	if income_outpost then
		local income = lConfig(region, "PassiveSupplyPerHour", 0)
		income = DivRound(income, lDormantIncomeDiv(region))
		income_outpost.money = Min(
			(income_outpost.money or 0) + income,
			lOutpostMoneyCapacity(region)
		)
		local mine_income = legion_mines * lConfig(region, "MineDiamondPerHour", 250)
		mine_income = DivRound(mine_income, lDormantIncomeDiv(region))
		income_outpost.diamond_stock = (income_outpost.diamond_stock or 0) + mine_income
		lSyncSharedOutpostResources(root, region, income_outpost)
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

	-- City/farm $ and recruits accrue on economic POIs every N days (default 3).
	local pulse_due = region_state.next_poi_pulse_time or region_state.next_recruit_time or 0
	if pulse_due > 0 and pulse_due <= lNow() then
		local interval = lInterval(region, "POIGenerationInterval", 96 * lHourScale())
		local raw_cycles = 1 + math.floor((lNow() - pulse_due) / interval)
		local max_catchup = lConfig(region, "POIGenerationMaxCatchup", 1)
		local cycles = Min(raw_cycles, max_catchup)
		local money_cap = lConfig(region, "PoiMoneyCap", 12000)
		if raw_cycles > max_catchup then
			lLog(string.format(
				"POI pulse %s: clamped catch-up %d → %d cycles",
				tostring(region_state.region_id),
				raw_cycles,
				cycles
			))
		end
		for _ = 1, cycles do
			for _, sector_id in ipairs(region.Sectors or empty_table) do
				local sector = gv_Sectors[sector_id]
				if sector and lSectorIsEconomicPOI(sector) then
					if JAZZ_IsLegionSide(sector.Side) then
						local money_add = 0
						if sector.City and sector.City ~= "none" and (sector.Militia or sector.Hospital) then
							money_add = money_add + lConfig(region, "CitySupplyBonus", 2500)
						end
						if sector.Farm then
							money_add = money_add + lConfig(region, "FarmSupplyBonus", 800)
						end
						-- Mines/ports/guardposts do not accrue tax stock here.
						if money_add > 0 then
							money_add = DivRound(money_add, lDormantIncomeDiv(region))
							region_state.poi_money[sector_id] = Min(
								(region_state.poi_money[sector_id] or 0) + money_add,
								money_cap
							)
						end
					end
					if JAZZ_IsLegionSide(sector.Side) or lIsPlayerSide(sector.Side) then
						local recruit_add = 0
						local cap = 0
						if sector.City and sector.City ~= "none" and (sector.Militia or sector.Hospital) then
							recruit_add = recruit_add + lConfig(region, "CityRecruitsPerDay", 3)
							cap = lConfig(region, "CityRecruitCap", 16)
						end
						if sector.Farm then
							recruit_add = recruit_add + lConfig(region, "FarmRecruitsPerDay", 2)
							cap = Max(cap, lConfig(region, "FarmRecruitCap", 8))
						end
						-- Guardpost/Port also feed the recruiter circuit (Ernie often has few Militia cities).
						if sector.Guardpost then
							recruit_add = recruit_add + lConfig(region, "GuardpostRecruitsPerDay", 2)
							cap = Max(cap, lConfig(region, "GuardpostRecruitCap", 12))
						end
						if sector.Port then
							recruit_add = recruit_add + lConfig(region, "PortRecruitsPerDay", 1)
							cap = Max(cap, lConfig(region, "PortRecruitCap", 8))
						end
						if recruit_add > 0 then
							recruit_add = DivRound(recruit_add, lDormantIncomeDiv(region))
							if recruit_add > 0 then
								region_state.poi_recruits[sector_id] = Min(
									(region_state.poi_recruits[sector_id] or 0) + recruit_add,
									cap
								)
							end
						end
					end
				end
			end
		end
		-- Advance from "now", not from a stale due time * raw_cycles (that recreates the bomb).
		region_state.next_poi_pulse_time = lNow() + interval
		region_state.next_recruit_time = region_state.next_poi_pulse_time
	elseif pulse_due <= 0 then
		region_state.next_poi_pulse_time = lNow()
			+ lInterval(region, "POIGenerationInterval", 96 * lHourScale())
		region_state.next_recruit_time = region_state.next_poi_pulse_time
	end

	lExpireReports(region_state)
end

-- Retribution (role "major"): prefer delivered recon reports, else max player noise.
local function lMajorTarget(region, region_state)
	local best_id = false
	local best_score = -1
	local best_report_id = false
	local report_ids = table.keys(region_state.reports or empty_table, true)
	for _, report_id in ipairs(report_ids) do
		local report = region_state.reports[report_id]
		if report and report.delivered and not report.consumed and report.expires_at > lNow() then
			local sector = gv_Sectors[report.target_sector]
			local score = 2000
				+ (sector and sector.Heat or 0)
				+ lSectorPriority(sector or {})
			if score > best_score or (score == best_score and (not best_id or report.target_sector < best_id)) then
				best_id = report.target_sector
				best_score = score
				best_report_id = report_id
			end
		end
	end
	if best_id then
		return best_id, best_report_id
	end

	best_score = -1
	for _, sector_id in ipairs(region.Sectors or empty_table) do
		local sector = gv_Sectors[sector_id]
		local player_squad = sector and lPlayerSquadInSector(sector_id)
		local player_controlled = sector and lIsPlayerSide(sector.Side)
		if lSectorIsSurface(sector) and (player_controlled or player_squad) then
			local score = (sector.Heat or 0)
				+ lSectorPriority(sector)
				+ (player_controlled and 1000 or 0)
				+ (player_squad and 500 or 0)
			if score > best_score or (score == best_score and (not best_id or sector_id < best_id)) then
				best_id = sector_id
				best_score = score
			end
		end
	end
	return best_id, false
end

local function lTryMajorResponse(root, region, region_state)
	if region_state.heat < lConfig(region, "MajorResponseHeat", 800)
	or root.major.next_response_time > lNow()
	then
		return false
	end
	local hq_sector = root.major.hq_sector
	local hq = hq_sector and gv_Sectors[hq_sector]
	local target_sector, report_id = lMajorTarget(region, region_state)
	if not hq or not JAZZ_IsLegionSide(hq.Side) or not target_sector then
		return false
	end
	local function lDispatchMajor(squad, squad_state, charge)
		squad_state.task = {
			task_type = "major_response",
			target_sector = target_sector,
			report_id = report_id or nil,
		}
		squad_state.state = "en_route"
		local routed = lSetRoute(squad, target_sector)
		if not routed then
			squad_state.task = false
			squad_state.state = "ready_for_orders"
			return false
		end
		if report_id then
			local report = region_state.reports[report_id]
			if report then
				report.consumed = true
			end
		end
		if charge then
			root.major.money = (root.major.money or 0) - (charge.money or 0)
			root.major.manpower = Max((root.major.manpower or 0) - (charge.manpower or 0), 0)
			squad_state.spawn_money_cost = charge.money
			squad_state.spawn_manpower_cost = charge.manpower
		end
		ObjModified(squad)
		root.major.next_response_time = lNow()
			+ lConfig(region, "MajorResponseCooldown", 72 * lHourScale())
		if routed == "arrived" then
			lOnSquadArrived(root, squad, squad_state)
		end
		Msg("JAZZ_LegionAIMajorResponse", squad.UniqueId, target_sector)
		return true
	end
	local idle_squad, idle_state = lFindIdleHomeRole(root, hq_sector, "major")
	if idle_squad then
		return lDispatchMajor(idle_squad, idle_state, false)
	end
	if lActiveRole(root, region_state.region_id, false, "major") then
		return false
	end
	local fallback_cost = lConfig(region, "MajorResponseCost", 50000)
	local unit_templates = false
	local cost = fallback_cost
	local manpower_cost = 0
	if JAZZ_GenerateLegionSquadComposition then
		local composition = JAZZ_GenerateLegionSquadComposition(
			"major",
			root.major.money or 0,
			root.major.manpower or 0,
			"auto",
			"major_" .. tostring(root.spawn_serial),
			lGrowthProgress(region_state)
		)
		if not composition then
			return false
		end
		unit_templates = composition.units
		cost = composition.money_cost or 0
		manpower_cost = composition.manpower_cost or #(composition.units or empty_table)
	end
	if (root.major.money or 0) < cost then
		return false
	end
	if (root.major.manpower or 0) < manpower_cost then
		return false
	end

	local squad_id, squad_state = lSpawnManaged(
		root,
		region,
		hq_sector,
		"major",
		hq_sector,
		1,
		{},
		unit_templates
	)
	local squad = squad_id and gv_Squads[squad_id]
	if not squad then
		return false
	end
	local spawned = #(squad.units or empty_table)
	if spawned > manpower_cost then
		manpower_cost = spawned
	end
	if (root.major.manpower or 0) < manpower_cost then
		lRetireSquad(root, squad_id)
		return false
	end
	if not lDispatchMajor(squad, squad_state, { money = cost, manpower = manpower_cost }) then
		lRetireSquad(root, squad_id)
		return false
	end
	return true
end

local function lTickRestingSquads(root)
	for squad_id, squad_state in sorted_pairs(root.squads) do
		if squad_state.state == "resting" and (squad_state.rest_until or 0) <= lNow() then
			local squad = gv_Squads[squad_id]
			if squad
				and squad.CurrentSector == squad_state.home_sector
				and not IsSquadTravelling(squad, "skip_tick_pass")
				and not IsConflictMode(squad.CurrentSector)
			then
				lFinishBaseRest(root, squad, squad_state)
			end
		end
	end
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
				lBeginReturn(root, squad, squad_state, "rest")
			elseif squad and squad_state.state == "orphaned" then
				lBeginReturn(root, squad, squad_state, "rest")
			end
		end
	end
end

local function lSetOutpostControlState(root, region, outpost)
	local sector = gv_Sectors[outpost.sector_id]
	local controlled = sector and JAZZ_IsLegionSide(sector.Side) or false
	-- STRATEGY-014: who captured owns — sync owner_faction.
	if sector then
		local owner = outpost.owner_faction or "unknown"
		if lIsPlayerSide(sector.Side) then
			owner = "player"
		elseif JAZZ_IsLegionSide(sector.Side) then
			local stamped = rawget(_G, "JAZZ_GetSectorOwnerFaction") and JAZZ_GetSectorOwnerFaction(outpost.sector_id)
			if stamped == "adonis" or stamped == "army" or stamped == "rebels" then
				owner = stamped
			else
				owner = "legion"
			end
		end
		outpost.owner_faction = owner
		if rawget(_G, "JAZZ_SetSectorOwnerFaction") then
			JAZZ_SetSectorOwnerFaction(outpost.sector_id, owner, "side_changed")
		end
	end
	local want_enabled = controlled and outpost.owner_faction == "legion"
	if want_enabled == outpost.enabled then
		return
	end
	if want_enabled then
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
	local interval = lInterval(region, "CommandInterval", 12 * lHourScale())
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

local function lTickWoundedRetreats(root)
	for squad_id, squad_state in sorted_pairs(root.squads) do
		if lRegularRoles[squad_state.role]
			and squad_state.state ~= "retired"
			and squad_state.state ~= "returning"
			and squad_state.state ~= "wounded"
			and squad_state.state ~= "resting"
			and squad_state.state ~= "orphaned"
		then
			local squad = gv_Squads[squad_id]
			if squad
				and squad.CurrentSector ~= squad_state.home_sector
				and not IsSquadTravelling(squad, "skip_tick_pass")
				and not IsConflictMode(squad.CurrentSector)
			then
				local living = lSquadLivingUnitInfos(squad)
				local weak_garrison = squad_state.role == "garrison" and living > 0 and living <= 10
				if weak_garrison or lSquadNeedsWoundedRetreat(squad, squad_state.role) then
					lBeginReturn(root, squad, squad_state, weak_garrison and "rest" or "wounded")
				end
			end
		end
	end
end

-- Legion hospital: satellite enemies have no meaningful HP — buff for combat instead.
local function lTickHospitalHeals(root)
	for squad_id, squad_state in sorted_pairs(root.squads) do
		if squad_state.state == "retired" then
			goto continue_hospital
		end
		local squad = gv_Squads[squad_id]
		if not squad or IsSquadTravelling(squad, "skip_tick_pass") or IsConflictMode(squad.CurrentSector) then
			goto continue_hospital
		end
		local sector = gv_Sectors[squad.CurrentSector]
		if not sector or not sector.Hospital or sector.HospitalLocked then
			goto continue_hospital
		end
		squad_state.hospital_buffed = true
		squad_state.hospital_buff_until = lNow() + 24 * lHourScale()
		for _, session_id in ipairs(squad.units or empty_table) do
			local ud = gv_UnitData[session_id]
			if ud and ud.AddStatusEffect and CharacterEffectDefs and CharacterEffectDefs.Inspired then
				if not (ud.HasStatusEffect and ud:HasStatusEffect("Inspired")) then
					ud:AddStatusEffect("Inspired")
				end
			end
		end
		ObjModified(squad)
		::continue_hospital::
	end
end

-- Re-apply hospital buff when units enter tactical (UnitData effects can be wiped on spawn).
function OnMsg.CombatStart()
	local root = gv_JAZZ_LegionAI
	if type(root) ~= "table" or not root.squads then
		return
	end
	if not (CharacterEffectDefs and CharacterEffectDefs.Inspired) then
		return
	end
	for _, unit in ipairs(g_Units or empty_table) do
		local squad_id = unit and unit.Squad
		local squad_state = squad_id and root.squads[squad_id]
		if squad_state
			and squad_state.hospital_buffed
			and (squad_state.hospital_buff_until or 0) > lNow()
			and unit.AddStatusEffect
			and not (unit.HasStatusEffect and unit:HasStatusEffect("Inspired"))
		then
			unit:AddStatusEffect("Inspired")
		end
	end
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

	-- STRATEGY-017: restore valuables wiped by loot regen / gear refresh.
	lResyncManagedMoneyCargo(root)

	lTickRecon(root)
	lTickMajor(root)
	lTickRestingSquads(root)
	lTickWoundedRetreats(root)
	lTickHospitalHeals(root)
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
	diagnostics.major.money_capacity = false
	diagnostics.major.manpower_capacity = false
	for region_id, region_state in sorted_pairs(root.regions) do
		local region = lGetRegionPreset(region_id)
		if not diagnostics.major.money_capacity then
			diagnostics.major.money_capacity = lMajorMoneyCapacity(region)
		end
		if not diagnostics.major.manpower_capacity then
			diagnostics.major.manpower_capacity = lMajorManpowerCapacity(region)
		end
		local region_data = {
			heat = region_state.heat,
			intel_points = region_state.intel_points,
			reports = table.count(region_state.reports),
			outposts = {},
			squads = {},
			poi_money_total = 0,
			poi_recruits_total = 0,
			caps = {
				regular = lConfig(region, "RegularSquadCap", 7),
				garrison = lGarrisonCap(region),
				patrol = lConfig(region, "PatrolCap", 2),
				recon = lConfig(region, "ReconCap", 1),
				qrf = lConfig(region, "QRFCap", 1),
				reinforce = lConfig(region, "ReinforceCap", 1),
			},
			costs = {
				garrison = lConfig(region, "GarrisonCost", 120000),
				patrol = lConfig(region, "PatrolCost", 18000),
				recon = lConfig(region, "ReconCost", 8000),
				qrf = lConfig(region, "QRFCost", 40000),
				reinforce = lConfig(region, "ReinforceCost", 25000),
				supply_convoy = lConfig(region, "SupplyConvoyCargo", 12000),
				major = lConfig(region, "MajorResponseCost", 50000),
			},
			active_counts = { regular = 0 },
		}
		for sector_id, money in sorted_pairs(region_state.poi_money or empty_table) do
			region_data.poi_money_total = region_data.poi_money_total + (money or 0)
		end
		for sector_id, recruits in sorted_pairs(region_state.poi_recruits or empty_table) do
			region_data.poi_recruits_total = region_data.poi_recruits_total + (recruits or 0)
		end
		for sector_id in sorted_pairs(region_state.outposts) do
			local outpost = root.outposts[sector_id]
			region_data.outposts[sector_id] = outpost and {
				enabled = outpost.enabled,
				money = outpost.money,
				manpower = outpost.manpower,
				outbound_manpower = outpost.outbound_manpower or 0,
				diamond_stock = outpost.diamond_stock,
				next_command_time = outpost.next_command_time,
				reboot_until = outpost.reboot_until,
				money_capacity = lOutpostMoneyCapacity(region),
				manpower_capacity = lConfig(region, "ManpowerCapacity", 32),
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

-- Compact money/manpower snapshot for console smoke tests.
function JAZZ_LegionAIGetEconomy()
	local root = JAZZ_LegionAIEnsureState()
	if not root then
		return { enabled = false, reason = "state unavailable" }
	end
	local snap = {
		enabled = true,
		schema_version = root.schema_version,
		major = {
			hq = root.major.hq_sector,
			money = root.major.money,
			manpower = root.major.manpower,
		},
		outposts = {},
		poi = {},
	}
	for region_id, region_state in sorted_pairs(root.regions) do
		local region = lGetRegionPreset(region_id)
		snap.major.money_capacity = snap.major.money_capacity or lMajorMoneyCapacity(region)
		snap.major.manpower_capacity = snap.major.manpower_capacity or lMajorManpowerCapacity(region)
		local poi_money = {}
		local poi_recruits = {}
		for sector_id, money in sorted_pairs(region_state.poi_money or empty_table) do
			if (money or 0) > 0 then
				poi_money[sector_id] = money
			end
		end
		for sector_id, recruits in sorted_pairs(region_state.poi_recruits or empty_table) do
			if (recruits or 0) > 0 then
				poi_recruits[sector_id] = recruits
			end
		end
		snap.poi[region_id] = {
			money = poi_money,
			recruits = poi_recruits,
		}
		for sector_id in sorted_pairs(region_state.outposts) do
			local outpost = root.outposts[sector_id]
			if outpost then
				snap.outposts[sector_id] = {
					region = region_id,
					enabled = outpost.enabled,
					money = outpost.money or 0,
					money_capacity = lOutpostMoneyCapacity(region),
					manpower = outpost.manpower or 0,
					manpower_capacity = lConfig(region, "ManpowerCapacity", 32),
					outbound_manpower = outpost.outbound_manpower or 0,
					diamond_stock = outpost.diamond_stock or 0,
				}
			end
		end
	end
	return snap
end

function JAZZ_LegionAIPrintEconomy()
	local snap = JAZZ_LegionAIGetEconomy()
	if not snap.enabled then
		print("[JAZZ LegionAI] economy unavailable:", snap.reason or "?")
		return snap
	end
	print(string.format(
		"[JAZZ LegionAI] Major HQ=%s  $%s/%s  manpower %s/%s",
		tostring(snap.major.hq),
		tostring(snap.major.money),
		tostring(snap.major.money_capacity),
		tostring(snap.major.manpower),
		tostring(snap.major.manpower_capacity)
	))
	for sector_id, op in sorted_pairs(snap.outposts) do
		print(string.format(
			"[JAZZ LegionAI] Outpost %s (%s) enabled=%s  $%s/%s  manpower %s/%s  outbound=%s  diamonds=%s",
			tostring(sector_id),
			tostring(op.region),
			tostring(op.enabled),
			tostring(op.money),
			tostring(op.money_capacity),
			tostring(op.manpower),
			tostring(op.manpower_capacity),
			tostring(op.outbound_manpower),
			tostring(op.diamond_stock)
		))
	end
	for region_id, poi in sorted_pairs(snap.poi) do
		print(string.format("[JAZZ LegionAI] POI stocks %s:", tostring(region_id)))
		for sector_id, money in sorted_pairs(poi.money or empty_table) do
			print(string.format("  %s money=$%s", tostring(sector_id), tostring(money)))
		end
		for sector_id, recruits in sorted_pairs(poi.recruits or empty_table) do
			print(string.format("  %s recruits=%s", tostring(sector_id), tostring(recruits)))
		end
	end
	return snap
end

-- Force one POI money/recruit pulse now (debug/smoke).
-- IMPORTANT: do not set timer to 0 — that used to replay thousands of catch-up cycles.
function JAZZ_LegionAIForcePoiPulse()
	local root = JAZZ_LegionAIEnsureState()
	if not root then
		return false
	end
	for _, region_state in sorted_pairs(root.regions) do
		region_state.next_poi_pulse_time = lNow()
		region_state.next_recruit_time = lNow()
	end
	root.last_processed_hour = false
	JAZZ_LegionAIProcessHour()
	return JAZZ_LegionAIGetEconomy()
end

-- Clamp absurd POI $ stocks (debug recovery after catch-up blowup).
function JAZZ_LegionAISanitizePoiMoney()
	local root = JAZZ_LegionAIEnsureState()
	if not root then
		return false
	end
	for region_id, region_state in sorted_pairs(root.regions) do
		local region = lGetRegionPreset(region_id)
		local money_cap = lConfig(region, "PoiMoneyCap", 12000)
		for sector_id, money in pairs(region_state.poi_money or empty_table) do
			if type(money) == "number" and money > money_cap then
				lLog(string.format(
					"sanitize poi_money %s:%s $%s → $%s",
					tostring(region_id),
					tostring(sector_id),
					tostring(money),
					tostring(money_cap)
				))
				region_state.poi_money[sector_id] = money_cap
			end
		end
	end
	return JAZZ_LegionAIGetEconomy()
end

-- The JAZZ role assets are final 64x64 PNGs and intentionally have no
-- vanilla `_2`/`_s` companions. Resolve by managed role, not potentially stale
-- SatelliteSquad.image, so save/load and ReloadLua keep the correct icon.
function JAZZ_GetLegionAISquadIcon(squad_or_id)
	local squad_state = lGetLegionAISquadState(squad_or_id)
	return squad_state and lRoleImages[squad_state.role] or false
end

function JAZZ_LegionAIGetSatelliteIconImages(context)
	local squad = context and (context.squad or context)
	local icon = lResolveLegionAISquadIcon(squad)
	if icon then
		return icon, false
	end
	return g_JAZZ_BaseGetSatelliteIconImages(context)
end

function JAZZ_LegionAIGetSatelliteIconImagesSquad(squad, from_ui)
	local icon = lResolveLegionAISquadIcon(squad)
	if icon then
		return icon
	end
	return g_JAZZ_BaseGetSatelliteIconImagesSquad(squad, from_ui)
end

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
	elseif squad_state.state == "resting" then
		return T{890000000001644, "<role> - resting and refitting at <home>", role = role, home = Untranslated(tostring(squad_state.home_sector or "?"))}
	elseif squad_state.state == "wounded" then
		return T{890000000001641, "<role> — wounded at outpost <home>; awaiting reinforcements", role = role, home = Untranslated(squad_state.home_sector)}
	elseif squad_state.state == "ready_for_orders" then
		return T{890000000001432, "<role> — awaiting orders from outpost <home>", role = role, home = Untranslated(squad_state.home_sector)}
	elseif squad_state.state == "returning" then
		if task and task.task_type == "return_wounded" then
			return T{890000000001642, "<role> — retreating wounded to <home>", role = role, home = Untranslated(squad_state.home_sector)}
		end
		if task and task.task_type == "return_with_intel" then
			local intel_sector = (task.report and task.report.target_sector)
				or task.observed_sector
				or "?"
			return T{
				890000000001433,
				"<role> — returning with intelligence about <sector> to <home>",
				role = role,
				sector = Untranslated(intel_sector),
				home = Untranslated(squad_state.home_sector),
			}
		end
		return T{890000000001434, "<role> — returning to base <home>", role = role, home = Untranslated(squad_state.home_sector)}
	elseif not task then
		return T{890000000001435, "<role> — awaiting assignment", role = role}
	elseif task.task_type == "patrol_dwell" then
		return T{890000000001645, "<role> - holding patrol sector <target>", role = role, target = Untranslated(target or "?")}
	elseif task.task_type == "garrison" or task.task_type == "reinforce" then
		if squad_state.state == "working" then
			return T{890000000001646, "<role> - reinforcing garrison at <target>", role = role, target = Untranslated(target or "?")}
		end
		return T{890000000001633, "<role> — moving to reinforce sector <target>", role = role, target = Untranslated(target or "?")}
	elseif squad_state.role == "garrison" then
		if squad_state.state == "working" then
			return T{890000000001436, "<role> — holding sector <target>", role = role, target = Untranslated(target or "?")}
		end
		return T{890000000001437, "<role> — moving to hold sector <target>", role = role, target = Untranslated(target or "?")}
	elseif squad_state.role == "reinforce" then
		if squad_state.state == "working" then
			return T{890000000001632, "<role> — reinforcing border sector <target>", role = role, target = Untranslated(target or "?")}
		end
		return T{890000000001633, "<role> — moving to reinforce sector <target>", role = role, target = Untranslated(target or "?")}
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
		return T{
			890000000001444,
			"<role> — delivering $<money> to <target>",
			role = role,
			money = Untranslated(tostring(lPayloadMoney(squad_state.payload))),
			target = Untranslated(target or "?"),
		}
	elseif squad_state.role == "shipment" then
		return T{
			890000000001445,
			"<role> — delivering $<money> to HQ <target>",
			role = role,
			money = Untranslated(tostring(lPayloadMoney(squad_state.payload))),
			target = Untranslated(target or "?"),
		}
	elseif squad_state.role == "tax" then
		return T{
			890000000001635,
			"<role> — collecting taxes ($<money>); next: <target>",
			role = role,
			money = Untranslated(tostring(lPayloadMoney(squad_state.payload))),
			target = Untranslated(target or "?"),
		}
	elseif squad_state.role == "recruiter" then
		return T{
			890000000001638,
			"<role> — recruiting (<people> people); next: <target>",
			role = role,
			people = Untranslated(tostring((task and squad_state.payload and squad_state.payload.manpower) or 0)),
			target = Untranslated(target or "?"),
		}
	elseif squad_state.role == "manpower" then
		return T{
			890000000001639,
			"<role> — delivering <people> recruits to <target>",
			role = role,
			people = Untranslated(tostring((squad_state.payload and squad_state.payload.manpower) or 0)),
			target = Untranslated(target or "?"),
		}
	end
	return T{890000000001446, "<role> — task in sector <target>", role = role, target = Untranslated(target or "?")}
end

-- SquadRolloverMap inherits SquadRollover. Its idCurrentSquadCont owns the
-- displayed/cycled squad, while the parent VList is the stable place for an
-- extra task row that is not destroyed by XContentTemplate:RespawnContent().
local function lUpdateLegionAITaskPanel(squad_content)
	local panel = squad_content and rawget(squad_content, "jazz_legion_ai_task_panel")
	if not panel then
		return
	end

	local squads = rawget(squad_content, "allSquads")
	local selected = rawget(squad_content, "selectedSquad") or 1
	local squad = squads and squads[selected] or squad_content.context
	local ok, task_text = pcall(JAZZ_GetLegionAISquadTaskText, squad)
	if not ok then
		lLog(string.format("task text failed: %s", tostring(task_text)))
		task_text = false
	end
	-- Never let a bad T / SetText error kill the whole SquadRolloverMap.
	local set_ok, set_err = pcall(function()
		panel:SetText(task_text or "")
		panel:SetVisible(not not task_text)
	end)
	if not set_ok then
		lLog(string.format("task panel set failed: %s", tostring(set_err)))
	end
end

local function lAttachLegionAITaskPanel(rollover)
	local squad_content = rollover and rollover:ResolveId("idCurrentSquadCont")
	if not squad_content or rawget(squad_content, "jazz_legion_ai_task_panel") then
		return
	end

	local outer_content = squad_content.parent
	if not outer_content then
		return
	end

	local panel = XText:new({
		Id = "idJAZZLegionAITask",
		Margins = box(0, 6, 0, 0),
		Padding = box(8, 6, 8, 6),
		HAlign = "stretch",
		FoldWhenHidden = true,
		HandleMouse = false,
		TextStyle = "SquadMapRollover",
		Translate = true,
		Visible = false,
		Background = RGBA(32, 35, 47, 255),
	}, outer_content, squad_content.context)
	rawset(squad_content, "jazz_legion_ai_task_panel", panel)

	local base_update = squad_content.UpdateMultiSquadSection
	if type(base_update) == "function" then
		squad_content.UpdateMultiSquadSection = function(self, ...)
			local result = base_update(self, ...)
			pcall(lUpdateLegionAITaskPanel, self)
			return result
		end
	end

	panel:Open()
	lUpdateLegionAITaskPanel(squad_content)
end

function JAZZ_LegionAICreateRolloverWindow(self, gamepad, context, pos)
	local rollover = g_JAZZ_BaseSquadWindowCreateRolloverWindow(self, gamepad, context, pos)
	if rollover then
		local ok, err = pcall(lAttachLegionAITaskPanel, rollover)
		if not ok then
			lLog(string.format("task panel attach failed: %s", tostring(err)))
		end
	end
	return rollover
end

function SquadWindow:GetRolloverText()
	return self.context
end

-- POI Extension.lua loads after this file and replaces GetSatelliteIconImages.
-- Re-wrap after mod load/reload so managed role icons win without recursion.
local function lInstallLegionAIUIWrappers()
	if GetSatelliteIconImages ~= JAZZ_LegionAIGetSatelliteIconImages then
		g_JAZZ_BaseGetSatelliteIconImages = GetSatelliteIconImages
		GetSatelliteIconImages = JAZZ_LegionAIGetSatelliteIconImages
	end
	if GetSatelliteIconImagesSquad ~= JAZZ_LegionAIGetSatelliteIconImagesSquad then
		g_JAZZ_BaseGetSatelliteIconImagesSquad = GetSatelliteIconImagesSquad
		GetSatelliteIconImagesSquad = JAZZ_LegionAIGetSatelliteIconImagesSquad
	end
	if SquadWindow.CreateRolloverWindow ~= JAZZ_LegionAICreateRolloverWindow then
		g_JAZZ_BaseSquadWindowCreateRolloverWindow = SquadWindow.CreateRolloverWindow
		SquadWindow.CreateRolloverWindow = JAZZ_LegionAICreateRolloverWindow
	end
	TFormat.SquadNameColored = g_JAZZ_BaseTFormatSquadNameColored
end

GetSatelliteIconImages = JAZZ_LegionAIGetSatelliteIconImages
GetSatelliteIconImagesSquad = JAZZ_LegionAIGetSatelliteIconImagesSquad
SquadWindow.CreateRolloverWindow = JAZZ_LegionAICreateRolloverWindow
TFormat.SquadNameColored = g_JAZZ_BaseTFormatSquadNameColored

function OnMsg.ModsReloaded()
	lInstallLegionAIUIWrappers()
	JAZZ_LegionAIEnsureState()
end

function OnMsg.NewGame()
	lInstallLegionAIUIWrappers()
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

function OnMsg.ConflictStart(sector_id)
	-- STRATEGY-017: ensure diamond cargo exists before tactical loot.
	if JAZZ_LegionAIResyncMoneyCargo then
		JAZZ_LegionAIResyncMoneyCargo()
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
				lBeginReturn(root, squad, squad_state, "rest")
			elseif squad_state.role == "shipment" then
				local hq = gv_Sectors[root.major.hq_sector]
				if sector_id == root.major.hq_sector and hq and JAZZ_IsLegionSide(hq.Side) then
					lAddMajorMoney(root, lGetRegionPreset(squad_state.region_id), lPayloadMoney(squad_state.payload))
					squad_state.payload.money = 0
					lClearTaggedMoneyCargo(squad)
					lBeginReturn(root, squad, squad_state, "rest")
				end
			end
		end
	end
end
