-- JAZZ-COMPAT-001: truncated campaign autonomy when jazz-maps (FhNNYd) is not loaded.
-- No-op while FhNNYd is active. Does not replace quests/maps/dialogue from jazz-maps.

JAZZ_MAPS_MOD_ID = "FhNNYd"

GameVar("gv_JAZZ_StandaloneNoMaps", function()
	return {
		schema = 1,
		active = false,
		bootstrapped = false,
		injected = {},
		auto_regions = {},
		geared = {},
	}
end)

local function lJazzMapsLoaded()
	if rawget(_G, "IsModLoaded") then
		return not not IsModLoaded(JAZZ_MAPS_MOD_ID)
	end
	if rawget(_G, "GetModLoaded") then
		return not not GetModLoaded(JAZZ_MAPS_MOD_ID)
	end
	return ModsLoaded and table.find(ModsLoaded, "id", JAZZ_MAPS_MOD_ID) and true or false
end

local function lShouldRun()
	return not lJazzMapsLoaded()
end

local function lLog(msg)
	if CombatLog and Untranslated then
		CombatLog("debug", Untranslated("[JAZZ Standalone] " .. msg))
	else
		print("[JAZZ Standalone] " .. msg)
	end
end

local function lEnsureState()
	local root = gv_JAZZ_StandaloneNoMaps
	if type(root) ~= "table" then
		root = {
			schema = 1,
			active = false,
			bootstrapped = false,
			injected = {},
			auto_regions = {},
		}
		gv_JAZZ_StandaloneNoMaps = root
	end
	root.injected = root.injected or {}
	root.auto_regions = root.auto_regions or {}
	root.geared = root.geared or {}
	return root
end

local function lHasEnemySquad(id)
	return id and EnemySquadDefs and EnemySquadDefs[id] and true or false
end

local function lPickExisting(list)
	local out = {}
	for _, id in ipairs(list or empty_table) do
		if lHasEnemySquad(id) then
			out[#out + 1] = id
		end
	end
	return out
end

-- Vanilla / weak IDs → jazz EnemySquadDefs when present (units package).
local SQUAD_REMAP = {
	LegionAttackers_Balanced_Easy = "LegionAttackers_JazzBalanced_Easy_Assault",
	LegionAttackers_Balanced = "LegionAttackers_JazzBalanced_Easy_Assault",
	LegionRaidSquad = "LegionJAZZSquadT1",
	LegionRaidSquad_Easy = "LegionJAZZSquadT1",
	LegionDefenders_Easy = "LegionGlobalAI_Garrison",
	Adonis_Troops_Assault_Light = "Adonis_Troops_Assault_Light",
	ArmyAttackers_Balanced_Hard = "ArmyAttackers_Balanced_Hard",
}

local ROLE_LISTS = {
	garrison = { "LegionGlobalAI_Garrison", "LegionFortressDefenders", "FortressDefenders" },
	patrol = { "LegionGlobalAI_Patrol", "LegionJAZZSquadT1", "LegionAttackers_Balanced_Easy_Assault" },
	recon = { "LegionGlobalAI_Recon", "LegionJAZZSquadT1" },
	qrf = { "LegionJAZZSquadT2", "LegionHeavyTroops" },
	attack = { "LegionJAZZSquadT1", "LegionAttackers_Balanced_Easy_Assault", "LegionExtraSquadFireArms_T2" },
	strong = { "LegionJAZZSquadT2", "LegionHeavyTroops", "LegionJAZZSquadT3" },
	convoy = { "LegionGlobalAI_Convoy" },
	major = { "LegionJAZZSquadT3", "LegionHeavyTroops" },
}

local LOOT_POOLS = {
	common = { "Meds", "FragGrenade", "SmokeGrenade", "Lockpick", "Wirecutter" },
	ammo = { "_9mm_Basic", "_556_Basic", "_762NATO_Basic", "_762WP_Basic", "_12gauge_Buckshot" },
	weapons = { "AK47", "MP5", "UZI", "Galil", "FAMAS", "Glock18" },
}

local function lItemExists(class)
	return class and g_Classes and g_Classes[class] and true or false
end

local function lSectorCoords(sector_id)
	if type(sector_id) ~= "string" or #sector_id < 2 then
		return false
	end
	local row = string.byte(sector_id, 1)
	if not row or row < string.byte("A") or row > string.byte("Z") then
		return false
	end
	local col = tonumber(string.sub(sector_id, 2))
	if not col then
		return false
	end
	return col, row - string.byte("A") + 1
end

local function lSectorDist(a, b)
	local ax, ay = lSectorCoords(a)
	local bx, by = lSectorCoords(b)
	if not ax or not bx then
		return 10000
	end
	return Max(abs(ax - bx), abs(ay - by))
end

local function lSectorIsSurface(sector)
	return sector and not sector.GroundSector and sector.Passability ~= "Water" and sector.Passability ~= "Blocked"
end

local function lManagedOutpostSet()
	local managed = {}
	for _, region in sorted_pairs(Regions or empty_table) do
		if region.LegionAIEnabled then
			for _, sector_id in ipairs(region.ManagedOutposts or empty_table) do
				managed[sector_id] = true
			end
		end
	end
	return managed
end

local function lCollectGuardposts()
	local list = {}
	for sector_id, sector in sorted_pairs(gv_Sectors or empty_table) do
		if sector and sector.Guardpost and lSectorIsSurface(sector) then
			list[#list + 1] = sector_id
		end
	end
	table.sort(list)
	return list
end

local function lRegionDisplayName(sector_id, sector)
	local city_id = sector and sector.City
	if city_id and city_id ~= "none" and gv_Cities and gv_Cities[city_id] and gv_Cities[city_id].DisplayName then
		local city_name = _InternalTranslate and _InternalTranslate(gv_Cities[city_id].DisplayName) or tostring(city_id)
		return "Округ " .. city_name
	end
	local label = sector and sector.display_name
	if label then
		local text = _InternalTranslate and _InternalTranslate(label) or tostring(label)
		if text and text ~= "" then
			return "Округ " .. text
		end
	end
	return "Округ " .. tostring(sector_id)
end

local function lWireGuardpostSquadLists(sector)
	if not sector then
		return
	end
	local function fill(field, candidates)
		local current = sector[field]
		if type(current) == "table" and #current > 0 then
			return
		end
		local picked = lPickExisting(candidates)
		if #picked > 0 then
			sector[field] = picked
		end
	end
	fill("EnemySquadsGarrisonList", ROLE_LISTS.garrison)
	fill("EnemySquadsPatroolList", ROLE_LISTS.patrol)
	fill("EnemySquadsReconList", ROLE_LISTS.recon)
	fill("EnemySquadsQRFList", ROLE_LISTS.qrf)
	fill("EnemySquadsList", ROLE_LISTS.attack)
	fill("StrongEnemySquadsList", ROLE_LISTS.strong)
	fill("ExtraDefenderSquads", ROLE_LISTS.garrison)
end

local function lCreateAutoRegion(outpost_id, sectors)
	if not Regions or not outpost_id then
		return false
	end
	local region_id = "JAZZ_Auto_" .. outpost_id
	if Regions[region_id] then
		return Regions[region_id]
	end
	local sector = gv_Sectors[outpost_id]
	local convoy = lPickExisting(ROLE_LISTS.convoy)
	local major = lPickExisting(ROLE_LISTS.major)
	local region = PlaceObj("Region", {
		id = region_id,
		Id = region_id,
		group = "Default",
		DisplayName = lRegionDisplayName(outpost_id, sector),
		Description = "Автономный округ Legion AI (без jazz-maps).",
		Sectors = sectors,
		LegionAIEnabled = true,
		ManagedOutposts = { outpost_id },
		-- Truncated: HQ = outpost itself (no authored Major fortress required).
		MajorHQSector = outpost_id,
		RegularSquadCap = 5,
		GarrisonCap = 2,
		PatrolCap = 1,
		ReconCap = 1,
		QRFCap = 1,
		ReinforceCap = 1,
		TaxCap = 0,
		RecruiterCap = 0,
		SupplySquads = convoy,
		ShipmentSquads = convoy,
		TaxSquads = {},
		RecruiterSquads = {},
		ManpowerSquads = convoy,
		MajorResponseSquads = major,
		StartingSupply = 8000,
		StartingManpower = 12,
		PassiveSupplyPerHour = 0,
		MajorResponseHeat = 900,
	})
	Regions[region_id] = region
	return region
end

local function lAssignSectorsToOutposts(outposts)
	local buckets = {}
	for _, outpost_id in ipairs(outposts) do
		buckets[outpost_id] = { outpost_id }
	end
	for sector_id, sector in sorted_pairs(gv_Sectors or empty_table) do
		if not lSectorIsSurface(sector) then
			goto continue
		end
		local best, best_dist = false, 10000
		for _, outpost_id in ipairs(outposts) do
			local d = lSectorDist(sector_id, outpost_id)
			if d < best_dist or (d == best_dist and (not best or outpost_id < best)) then
				best, best_dist = outpost_id, d
			end
		end
		-- Keep regions local: ignore far wilderness (Chebyshev > 8).
		if best and best_dist <= 8 and sector_id ~= best then
			local list = buckets[best]
			list[#list + 1] = sector_id
		end
		::continue::
	end
	for _, outpost_id in ipairs(outposts) do
		table.sort(buckets[outpost_id])
	end
	return buckets
end

local function lRemapSquadId(squad_def_id)
	if not squad_def_id then
		return squad_def_id
	end
	local mapped = SQUAD_REMAP[squad_def_id]
	if mapped and lHasEnemySquad(mapped) then
		return mapped
	end
	if lHasEnemySquad(squad_def_id) then
		return squad_def_id
	end
	-- Prefer jazz tier squads when the vanilla def is missing entirely.
	local fallback = lPickExisting(ROLE_LISTS.attack)
	return fallback[1] or squad_def_id
end

local function lRemapSquadList(list)
	if type(list) ~= "table" then
		return list
	end
	local out = {}
	for _, id in ipairs(list) do
		out[#out + 1] = lRemapSquadId(id)
	end
	return out
end

local function lUpgradeSectorSquadRefs(sector)
	if not sector then
		return
	end
	for _, field in ipairs({
		"EnemySquadsList",
		"StrongEnemySquadsList",
		"ExtraDefenderSquads",
		"EnemySquadsGarrisonList",
		"EnemySquadsPatroolList",
		"EnemySquadsReconList",
		"EnemySquadsQRFList",
		"InitialSquads",
	}) do
		if type(sector[field]) == "table" and #sector[field] > 0 then
			sector[field] = lRemapSquadList(sector[field])
		end
	end
end

local function lInstallGenerateEnemySquadWrapper()
	if rawget(_G, "g_JAZZ_StandaloneGenerateEnemySquadWrapped") then
		return
	end
	local base = rawget(_G, "GenerateEnemySquad")
	if type(base) ~= "function" then
		return
	end
	g_JAZZ_StandaloneGenerateEnemySquadWrapped = true
	g_JAZZ_BaseGenerateEnemySquad = base
	function GenerateEnemySquad(squad_def_id, ...)
		if lShouldRun() then
			squad_def_id = lRemapSquadId(squad_def_id)
		end
		return g_JAZZ_BaseGenerateEnemySquad(squad_def_id, ...)
	end
end

local function lPickLootClass(pool, seed_key)
	local valid = {}
	for _, class in ipairs(pool or empty_table) do
		if lItemExists(class) then
			valid[#valid + 1] = class
		end
	end
	if #valid == 0 then
		return false
	end
	local idx = InteractionRand(#valid, seed_key) + 1
	return valid[idx]
end

local function lInjectContainerLoot()
	if not lShouldRun() or not gv_CurrentSectorId then
		return
	end
	local root = lEnsureState()
	local sector_key = gv_CurrentSectorId
	if root.injected[sector_key] then
		return
	end
	root.injected[sector_key] = true

	local containers = MapGet("map", "ItemContainer") or empty_table
	local count = 0
	for i, container in ipairs(containers) do
		if not IsValid(container) then
			goto next_container
		end
		local handle = container.handle or i
		local inject_key = sector_key .. ":" .. tostring(handle)
		if root.injected[inject_key] then
			goto next_container
		end
		root.injected[inject_key] = true

		local roll = InteractionRand(100, "JAZZ_StandaloneLoot_" .. inject_key)
		local class
		if roll < 35 then
			class = lPickLootClass(LOOT_POOLS.ammo, "JAZZ_StandaloneAmmo_" .. inject_key)
		elseif roll < 55 then
			class = lPickLootClass(LOOT_POOLS.common, "JAZZ_StandaloneCommon_" .. inject_key)
		elseif roll < 70 then
			class = lPickLootClass(LOOT_POOLS.weapons, "JAZZ_StandaloneWeapon_" .. inject_key)
		end
		if class then
			local item = PlaceInventoryItem(class)
			if item then
				if IsKindOf(item, "InventoryStack") then
					item.Amount = Max(1, InteractionRand(6, "JAZZ_StandaloneStack_" .. inject_key) + 2)
				end
				container:AddItem("Inventory", item)
				count = count + 1
			end
		end
		::next_container::
	end
	if count > 0 then
		lLog("injected loot into " .. count .. " containers in " .. tostring(sector_key))
	end
end

local function lRefreshEnemyLoadouts()
	if not gv_Squads then
		return
	end
	local root = lEnsureState()
	for _, squad in ipairs(gv_Squads) do
		for _, unit_id in ipairs(squad.units or empty_table) do
			if root.geared[unit_id] then
				goto next_unit
			end
			local unitdata = gv_UnitData and gv_UnitData[unit_id]
			if unitdata
				and not unitdata.IsMercenary
				and unitdata.IsDead and not unitdata:IsDead()
				and unitdata.Affiliation
				and (unitdata.Affiliation == "Legion"
					or unitdata.Affiliation == "Army"
					or unitdata.Affiliation == "Adonis"
					or unitdata.Affiliation == "Rebel")
			then
				-- jazz-units UnitData overrides already redefine vanilla IDs;
				-- force starting gear rebuild once so equipment matches mod defs.
				unitdata:ForEachItem(function(item, slot_name)
					unitdata:RemoveItem(slot_name, item)
				end)
				if unitdata.CreateStartingEquipment then
					unitdata:CreateStartingEquipment(unitdata.randomization_seed)
				end
				root.geared[unit_id] = true
			end
			::next_unit::
		end
	end
end

function JAZZ_StandaloneNoMapsBootstrap(force)
	local root = lEnsureState()
	if not lShouldRun() then
		root.active = false
		return false
	end
	if not gv_Sectors then
		return false
	end
	if root.bootstrapped and not force then
		return true
	end

	root.active = true
	lInstallGenerateEnemySquadWrapper()

	local managed = lManagedOutpostSet()
	local all_posts = lCollectGuardposts()
	local unmanaged = {}
	for _, sector_id in ipairs(all_posts) do
		if not managed[sector_id] then
			unmanaged[#unmanaged + 1] = sector_id
		end
		lWireGuardpostSquadLists(gv_Sectors[sector_id])
		lUpgradeSectorSquadRefs(gv_Sectors[sector_id])
	end

	-- Also remap non-guardpost enemy sector squad refs (InitialSquads etc.).
	for _, sector in sorted_pairs(gv_Sectors) do
		if sector and (sector.Side == "enemy1" or sector.Side == "enemy2" or sector.InitialSquads) then
			lUpgradeSectorSquadRefs(sector)
		end
	end

	if #unmanaged > 0 then
		local buckets = lAssignSectorsToOutposts(unmanaged)
		for _, outpost_id in ipairs(unmanaged) do
			local region = lCreateAutoRegion(outpost_id, buckets[outpost_id])
			if region then
				root.auto_regions[outpost_id] = region.id or region.Id
			end
		end
		lLog(string.format("auto regions: %d (unmanaged guardposts)", #unmanaged))
	else
		lLog("no unmanaged guardposts; keeping authored Legion AI regions only")
	end

	-- Ensure ErnieIsland / any authored managed posts still have jazz lists.
	for sector_id in pairs(managed) do
		lWireGuardpostSquadLists(gv_Sectors[sector_id])
		lUpgradeSectorSquadRefs(gv_Sectors[sector_id])
	end

	root.bootstrapped = true
	if rawget(_G, "JAZZ_LegionAIEnsureState") then
		JAZZ_LegionAIEnsureState()
	end
	lRefreshEnemyLoadouts()
	return true
end

function JAZZ_StandaloneNoMapsIsActive()
	return lShouldRun() and lEnsureState().active
end

function OnMsg.ModsReloaded()
	if lShouldRun() then
		lInstallGenerateEnemySquadWrapper()
	end
end

function OnMsg.NewGame()
	if not lShouldRun() then
		return
	end
	local root = lEnsureState()
	root.bootstrapped = false
	root.injected = {}
	root.auto_regions = {}
	root.geared = {}
	JAZZ_StandaloneNoMapsBootstrap(true)
end

function OnMsg.LoadGame()
	if not lShouldRun() then
		return
	end
	local root = lEnsureState()
	root.bootstrapped = false
	JAZZ_StandaloneNoMapsBootstrap(true)
end

function OnMsg.InitSatelliteView()
	if not lShouldRun() then
		return
	end
	JAZZ_StandaloneNoMapsBootstrap(false)
	lRefreshEnemyLoadouts()
end

function OnMsg.ExplorationStart()
	if not lShouldRun() then
		return
	end
	JAZZ_StandaloneNoMapsBootstrap(false)
	lInjectContainerLoot()
end

function OnMsg.CombatStart()
	if not lShouldRun() then
		return
	end
	lInjectContainerLoot()
end
