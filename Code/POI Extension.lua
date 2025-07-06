POIDescriptions = {
	{id = "Guardpost", display_name = T(783261626976, "Outpost"), descr = T(349382017874, "Enemy outposts organize attacking squads to take over nearby sectors. They also block water travel near them"), icon = "guard_post"},
	{id = "Mine",      display_name = T(574641095788, "Mine"),      descr = T(694639203124, "Mines provide daily income based on the <em>Loyalty</em> of the nearest settlement"), icon = "mine"},
	{id = "Port",      display_name = T(682491033993, "Port"),      descr = T(301024708154, "You can initiate travel over water sectors from a port under your control. Boat travel usually costs money"), icon = "port"},
	{id = "Hospital",  display_name = T(928160208169, "Hospital"),  descr = T(113589428451, "Hospitals allow fast healing of wounds for money via the Hospital Treatment Operation"), icon = "hospital"},
	{id = "RepairShop",  display_name = T(333237565365, "Repair Shop"),  descr = T(653771367256, "Repair shops allow mercs to craft ammo and explosives via the corresponding operations"), icon = "repair_shop"},
	{id = "Farm",  display_name = T(178686311281123, "Ферма"),  descr = T(1786863112821, "Фермы приносят доход в зависимости от лояльности ближайшего города"), icon = "farm"},
    {id = "Donations",  display_name = T(178686311281214, "Пожертвования"),  descr = T(1786863112822, "Добровольные пожертвования в зависимости от лояльности"), icon = "donations"},
	{id = "Bunker",  display_name = T(1786863112811235, "Укрепления"),  descr = T(1786863112823, "Данный сектор укреплен"), icon = "bunker"},
	{id = "Slon",  display_name = T(1786863112811236, "Слоновая кость"),  descr = T(1786863112824, "В этом секторе добывают слоновую кость. Доход не зависит от лояльности"), icon = "slon"},
	{id = "Wood",  display_name = T(178686311281127, "Лесозаготовки"),  descr = T(1786863112825, "В этом секторе добывают древесину"), icon = "wood"},
}

function GetSectorPOITypes()
	return { "all", "Mine", "Guardpost", "Bunker", "Port", "Farm", "Donations" }
end

PlaceObj('PropertyDefBool', {
    'category', "Farm",
    'id', "Farm",
})
PlaceObj('PropertyDefNumber', {
    'category', "Farm",
    'id', "DailyIncomeFarm",
    'help', "Profit per day at 100% loyalty",
    'extra_code', "no_edit = function(self) return not self.Farm end",
    'default', 1000,
    'min', 0,
})

PlaceObj('PropertyDefBool', {
    'category', "Donations",
    'id', "Donations",
})
PlaceObj('PropertyDefNumber', {
    'category', "Donations",
    'id', "DailyIncomeDonations",
    'help', "Profit per day at 100% loyalty",
    'extra_code', "no_edit = function(self) return not self.donations end",
    'default', 1000,
    'min', 0,
})
PlaceObj('PropertyDefBool', {
    'category', "Bunker",
    'id', "Bunker",
})
--PlaceObj('PropertyDefNumber', {
--    'category', "City",
--    'id', "DailyIncome",
--    'help', "Profit per day at 100% loyalty",
--    'extra_code', "no_edit = function(self) return not self.City end",
--    'default', 0,
--    'min', 0,
--})

PlaceObj('PropertyDefBool', {
    'category', "Slon",
    'id', "Slon",
})
PlaceObj('PropertyDefNumber', {
    'category', "Slon",
    'id', "DailyIncomeSlon",
    'help', "Profit per day at 100% loyalty",
    'extra_code', "no_edit = function(self) return not self.Slon end",
    'default', 10000,
    'min', 0,
})

PlaceObj('PropertyDefBool', {
    'category', "Wood",
    'id', "Wood",
})
PlaceObj('PropertyDefNumber', {
    'category', "Wood",
    'id', "DailyIncomeWood",
    'help', "Profit per day at 100% loyalty",
    'extra_code', "no_edit = function(self) return not self.Wood end",
    'default', 1000,
    'min', 0,
})

UndefineClass('SatelliteSectorGedFilter')
DefineClass.SatelliteSectorGedFilter = {
	__parents = { "GedFilter", },
	__generated_by_class = "ClassDef",

	properties = {
		{ id = "HideGenerated", name = "Hide inherited/empty", 
			editor = "bool", default = false, },
		{ id = "City", 
			editor = "choice", default = "don't care", items = function (self) return table.iappend({"don't care", "any", "none"}, table.map(GetCurrentCampaignPreset().Cities, "Id")) end, },
		{ id = "Farm", 
			editor = "choice", default = "don't care", items = function (self) return { true, false, "don't care" } end, },
        { id = "Donations", 
			editor = "choice", default = "don't care", items = function (self) return { true, false, "don't care" } end, },    
        { id = "Mine", 
			editor = "choice", default = "don't care", items = function (self) return { true, false, "don't care" } end, },
		{ id = "Slon", 
			editor = "choice", default = "don't care", items = function (self) return { true, false, "don't care" } end, },
		{ id = "Wood", 
			editor = "choice", default = "don't care", items = function (self) return { true, false, "don't care" } end, },
		{ id = "Events", 
			editor = "choice", default = "don't care", items = function (self) return { true, false, "don't care" } end, },
		{ id = "Guardpost", 
			editor = "choice", default = "don't care", items = function (self) return { true, false, "don't care" } end, },
		{ id = "Bunker", 
			editor = "choice", default = "don't care", items = function (self) return { true, false, "don't care" } end, },	
		{ id = "Region", 
			editor = "choice", default = "don't care", items = function (self) return PresetsCombo("GameStateDef", "region", "don't care") end, },
		{ id = "Port", 
			editor = "choice", default = "don't care", items = function (self) return { true, false, "don't care" } end, },
		{ id = "Militia", 
			editor = "choice", default = "don't care", items = function (self) return { true, false, "don't care" } end, },
		{ id = "Music", 
			editor = "choice", default = false, items = function (self) return PresetsCombo("RadioStationPreset") end, },
		{ id = "Weather", 
			editor = "text", default = false, },
	},
}

function SatelliteSectorGedFilter:FilterObject(sector)
	if self.HideGenerated and (sector.inherited or sector.generated) then return false end
	if self.Mine ~= "don't care" and self.Mine ~= sector.Mine then return false end
	if self.Guardpost ~= "don't care" and self.Guardpost ~= sector.Guardpost then return false end
	if self.Bunker ~= "don't care" and self.Bunker ~= sector.Bunker then return false end	
	if self.City == "any" then
		if sector.City == "none" then return false end
	elseif self.City ~= "don't care" and self.City ~= sector.City then return false end
	if self.Events ~= "don't care" and self.Events ~= (sector.Events and #sector.Events > 0) then return false end
	if self.Region ~= "don't care" then
	  local region = sector.Map and MapData[sector.Map] and MapData[sector.Map].Region
	  if self.Region ~= region then return false end
	end
	if self.Port ~= "don't care" and self.Port ~= sector.Port then
		return false
	end
	if self.Militia ~= "don't care" and self.Militia ~= sector.Militia then
		return false
	end
	
	if self.Music then
		local music_match
		if sector.MusicCombat and string.match(sector.MusicCombat, self.Music) then
			music_match = true
		end
		if sector.MusicConflict and string.match(sector.MusicConflict, self.Music) then
			music_match = true
		end
		if sector.MusicExploration and string.match(sector.MusicExploration, self.Music) then
			music_match = true
		end
		if not music_match then
			return false
		end
	end
	
	if self.Weather then
		if not (sector.WeatherZone and string.match(string.lower(sector.WeatherZone), string.lower(self.Weather)) )then
			return false
		end
	end
	
	return true
end


UndefineClass('SatelliteSector')
DefineClass.SatelliteSector = {
	__parents = { "CampaignObject", },
	__generated_by_class = "ClassDef",

	properties = {
		{ id = "SetId", 
			editor = "func", default = function (self, id)
if self.modId then return end
self.name = id
CampaignObject.SetId(self, id)
end, no_edit = true, params = "self, id", },
		{ id = "Setdisplay_name", 
			editor = "func", default = function (self, display_name)
self.display_name = display_name
if self.modId then return end
if display_name then
	self.name = string.format("%s %s", self.Id, _InternalTranslate(display_name))
else
	self.name = self.Id
end
end, no_edit = true, params = "self, display_name", },
		{ id = "OnEditorSetProperty", 
			editor = "func", default = function (self, prop_id)
if not self.modId and prop_id == "Roads" or prop_id == "BlockTravel" then
	SatelliteSectorSetDirectionsProp(self, prop_id)
end
if g_SatelliteUI then
	g_SatelliteUI:UpdateSectorVisuals(self.Id)
end
if prop_id == "WeatherZone" then
	g_WeatherZones = false
end
end, no_edit = true, params = "self, prop_id", },
		{ category = "Data", id = "generated_hint", help = "<center>This is an automatically-generated empty sector.", 
			editor = "help", default = false, no_edit = function(self) return not self.generated end, },
		{ category = "Data", id = "inherited_hint", help = "<center>This is an inherited sector - use the button below to override it in this DLC.", 
			editor = "help", default = false, no_edit = function(self) return not self.inherited end, },
		{ category = "Data", id = "edit_sector_button", 
			editor = "buttons", default = false, buttons = { {name = "Edit sector", func = "EditGeneratedSector", is_hidden = function(self) if self.modId or config.ModdingToolsInUserMode then return true end

return IsKindOf(self, "GedMultiSelectAdapter") or not self.inherited and not self.generated end }, }, },
		{ id = "Id", 
			editor = "text", default = false, read_only = true, },
		{ category = "Underground", id = "HideUnderground", name = "Hide underground", 
			editor = "bool", default = false, no_edit = function(self) return self.GroundSector end, },
		{ category = "Underground", id = "CanGoUp", name = "Can go overground", help = "Whether this underground sector has a travel connection to its overground sector.", 
			editor = "bool", default = true, no_edit = function(self) return not self.GroundSector end, },
		{ category = "Underground", id = "underground_sector_buttons", 
			editor = "buttons", default = false, buttons = { {name = "Add underground sector", func = "AddUndergroundSector", is_hidden = function(self) if IsKindOf(self, "GedMultiSelectAdapter") then return true end

if self.modId or config.ModdingToolsInUserMode then return true end

local campaign = GetParentTableOfKind(self, "CampaignPreset")
return not self.Id or
			self.Id:ends_with("_Underground") or
		(campaign and table.find(campaign.Sectors, "Id", self.Id .. "_Underground")) end },  {name = "Select underground sector", func = "SelectUndergroundSector", is_hidden = function(self) if IsKindOf(self, "GedMultiSelectAdapter") then return true end

if self.modId or config.ModdingToolsInUserMode then return true end

local campaign = GetParentTableOfKind(self, "CampaignPreset")
return not self.Id or
			self.Id:ends_with("_Underground") or
		not (campaign and table.find(campaign.Sectors, "Id", self.Id .. "_Underground")) end },  {name = "Remove sector", func = "RemoveSector", is_hidden = function(self) if self.modId or config.ModdingToolsInUserMode then return true end

return IsKindOf(self, "GedMultiSelectAdapter") or not self.Id or self.inherited or not self.Id:ends_with("_Underground") end }, }, },
		{ id = "MapPosition", help = "delete me", 
			editor = "point", default = false, dont_save = true, no_edit = true, },
		{ id = "XMapPosition", 
			editor = "point", default = false, no_edit = true, },
		{ id = "IconMapPosition", 
			editor = "point", default = false, dont_save = true, no_edit = true, },
		{ id = "Map", name = "Map", 
			editor = "combo", default = false, items = function (self) return ListMaps() end, },
		{ id = "MapTier", name = "Tier", help = "Used in the 'PlayerIsInSectorsOfTier' conditional effect to, for example, spawn loot on the map.", 
			editor = "number", default = 0, scale = 10, step = 5, min = 0, max = 50, },
		{ id = "Label1", name = "Label 1", 
			editor = "text", default = false, no_edit = function(self) return config.ModdingToolsInUserMode end, },
		{ id = "modId", 
			editor = "text", default = false, no_edit = true, },
		{ id = "Label2", name = "Label 2", 
			editor = "text", default = false, no_edit = function(self) return config.ModdingToolsInUserMode end, },
		{ id = "RunLoyaltyLogic", name = "Run loyalty logic", help = "Whether this sector will grant/remove loyalty on conflict resolution", 
			editor = "bool", default = true, },
		{ id = "GroundSector", 
			editor = "text", default = false, no_edit = true, },
		{ id = "template_key", 
			editor = "text", default = false, read_only = true, no_edit = true, },
		{ id = "display_name", name = "Display name", 
			editor = "text", default = false, translate = true, context = SatelliteSectorLocContext(), },
		{ id = "Side", 
			editor = "combo", default = "enemy1", items = function (self) return Sides end, },
		{ id = "StickySide", name = "Sticky side", help = "Prevents changing the side of the sector unless it is forced from a conditinal effect or 'SatelliteSectorSetSide' with 'force' param.", 
			editor = "bool", default = false, },
		{ category = "Travel", id = "TerrainType", name = "Terrain type", help = "Terrain type modifies the travel time", 
			editor = "preset_id", default = "Savanna", 
			no_edit = function(self) return self.GroundSector end, preset_class = "SectorTerrain", },
		{ id = "WeatherZone", name = "Weather zone", help = "Weather Zone the sector belongs to. Sectors within the same Weather Zone have the same weather cycle.", 
			editor = "combo", default = "Default", items = function (self)
local campaignPreset
if self.modId then
	local modItem = GetParentTableOfKind(self, "ModItemSector")
	campaignPreset = modItem and CampaignPresets[modItem.campaignId]
else
	campaignPreset = GetCurrentCampaignPreset()
end
return campaignPreset and WeatherZoneCombo(campaignPreset) or {}
end, },
		{ category = "Travel", id = "Passability", 
			editor = "combo", default = "Land", 
			no_edit = function(self) return self.GroundSector end, items = function (self) return {"Land", "Water", "Land and Water", "Blocked"} end, },
		{ category = "City", id = "City", name = "Associated city", 
			editor = "combo", default = "none", items = function (self) return table.iappend({"none"}, table.map(GetCurrentCampaignPreset().Cities, "Id")) end, },
		{ category = "City", id = "ShowCity", name = "Show city name", help = "Whether to show the city name on the sector", 
			editor = "bool", default = false, },
--        { category = "City", id = "DailyIncome", help = "Profit per day at 100% loyalty", 
--			editor = "number", default = 0, 
--			no_edit = function(self) return not self.City end, min = 0, },
		{ id = "reveal_allowed", help = "This sector can be revealed by the player, and traits on them are shown in the satellite view. At the start of the campaign mainland sectors are not visible.", 
			editor = "bool", default = false, no_edit = true, },
		{ id = "never_autoresolve", name = "Never autoresolve", help = "Conflicts on this sector can never be autoresolved", 
			editor = "bool", default = false, },
		{ id = "discovered", name = "Discovered", help = "The player has been to this sector, or has started travelling to it via some method. In use only for underground sectors.", 
			editor = "bool", default = true, },
		{ category = "Conflict", id = "AutoResolveDefenderBonus", name = "AutoResolve defender bonus", help = "Percent by which defender power is increased in this sector", 
			editor = "number", default = 0, min = 0, },
		{ category = "Mine", id = "Mine", 
			editor = "bool", default = false, },
		{ category = "Mine", id = "DailyIncome", help = "Profit per day at 100% loyalty", 
			editor = "number", default = 1000, 
			no_edit = function(self) return not self.Mine end, min = 0, },
		{ id = "intel_progress", name = "Intel progress", 
			editor = "number", default = 0, no_edit = true, },
		{ category = "Mine", id = "Depletion", 
			editor = "bool", default = false, 
			no_edit = function(self) return not self.Mine end, },
		{ category = "Mine", id = "DepletionTime", help = "In how many days the mine will deplete. This should be randomized each game around this value.", 
			editor = "number", default = 90, 
			no_edit = function(self) return not self.Mine end, min = 1, max = 500, },
		{ category = "Mine", id = "mine_work_days", 
			editor = "number", default = false, no_edit = true, },
		{ category = "Mine", id = "mine_depleted", 
			editor = "bool", default = false, no_edit = true, },
		{ category = "Mine", id = "mine_enabled", 
			editor = "bool", default = true, no_edit = true, },
		{ category = "Mine", id = "income_mods", 
			editor = "prop_table", default = false, no_edit = true, },
		{ category = "Mine", id = "depletion_mods", 
			editor = "prop_table", default = false, no_edit = true, },
        { category = "Farm", id = "Farm", 
			editor = "bool", default = false, },
		{ category = "Farm", id = "DailyIncomeFarm", help = "Profit per day at 100% loyalty", 
			editor = "number", default = 1000, 
			no_edit = function(self) return not self.Farm end, min = 0, },
        { category = "Farm", id = "FarmLocked", name = "Farm locked", 
			editor = "bool", default = false, 
			no_edit = function(self) return self.GroundSector end, },   
        { category = "Donations", id = "Donations", 
			editor = "bool", default = false, },
		{ category = "Donations", id = "DailyIncomeDonations", help = "Profit per day at 100% loyalty", 
			editor = "number", default = 1000, 
			no_edit = function(self) return not self.Donations end, min = 0, },  
        { category = "Donations", id = "DonationsLocked", name = "Donations locked", 
			editor = "bool", default = false, 
			no_edit = function(self) return self.GroundSector end, },      
		{ category = "Slon", id = "Slon", 
			editor = "bool", default = false, },
		{ category = "Slon", id = "DailyIncomeSlon", help = "Profit per day at 100% loyalty", 
			editor = "number", default = 10000, 
			no_edit = function(self) return not self.Slon end, min = 0, },
        { category = "Slon", id = "SlonLocked", name = "Slon locked", 
			editor = "bool", default = false, 
			no_edit = function(self) return self.GroundSector end, },   
		{ category = "Wood", id = "Wood", 
			editor = "bool", default = false, },
		{ category = "Wood", id = "DailyIncomeWood", help = "Profit per day at 100% loyalty", 
			editor = "number", default = 1000, 
			no_edit = function(self) return not self.Wood end, min = 0, },
        { category = "Wood", id = "WoodLocked", name = "Wood locked", 
			editor = "bool", default = false, 
			no_edit = function(self) return self.GroundSector end, },   	
		{ category = "Hospital", id = "Hospital", 
			editor = "bool", default = false, 
			no_edit = function(self) return self.GroundSector end, },
		{ category = "Hospital", id = "HospitalLocked", name = "Hospital locked", 
			editor = "bool", default = false, 
			no_edit = function(self) return self.GroundSector end, },
			{ category = "Bunker", id = "Bunker", 
			editor = "bool", default = false, 
			no_edit = function(self) return self.GroundSector end, },	
		{ category = "Guardpost", id = "Guardpost", 
			editor = "bool", default = false, 
			no_edit = function(self) return self.GroundSector end, },
		{ category = "Guardpost", id = "Region", name = "Region", help = "Регион", 
			editor = "preset_id_list", default = {}, 
			no_edit = function(self) return not self.Guardpost end, preset_class = "Region", item_default = "", },
		{ category = "Guardpost", id = "PatrolRespawnTime", name = "Attack spawn (+24h preparation)", 
			editor = "number", default = 172800, 
			no_edit = function(self) return not self.Guardpost end, scale = "h", min = 0, },
		{ category = "Guardpost", id = "InitialSpawn", name = "Initial squad spawn", 
			editor = "bool", default = false, 
			no_edit = function(self) return not self.Guardpost end, },
		{ category = "Guardpost", id = "TargetSectors", name = "Target sectors", help = "Target sectors for spawned enemy squads.", 
			editor = "string_list", default = {}, 
			no_edit = function(self) return not self.Guardpost end, item_default = "", items = function (self) return GetCampaignSectorsCombo("") end, },
		{ category = "Guardpost", id = "ExtraDefenderSquads", name = "Extra defender squads", help = "Squads that will be spawned as extra defenders (4th shield)", 
			editor = "preset_id_list", default = {}, 
			no_edit = function(self) return not self.Guardpost end, preset_class = "EnemySquads", item_default = "", },
		{ category = "Guardpost", id = "EnemySquadsList", name = "Enemy squads list", help = "A random squad from the list will be chosen on guardpost spawn time", 
			editor = "preset_id_list", default = {}, 
			no_edit = function(self) return not self.Guardpost end, preset_class = "EnemySquads", item_default = "", },
		{ category = "Guardpost", id = "StrongEnemySquadsList", name = "Strong enemy squads list", help = 'When the guardpost performs a "strong attack" it will swap the currently primed squad with one from this array.', 
			editor = "preset_id_list", default = {}, 
			no_edit = function(self) return not self.Guardpost end, preset_class = "EnemySquads", item_default = "", },
		{ category = "Militia", id = "Militia", 
			editor = "bool", default = false, 
			no_edit = function(self) return self.GroundSector end, },
		{ category = "Militia", id = "MaxMilitia", 
			editor = "number", default = 8, 
			no_edit = function(self) return not self.Militia end, min = 1, max = 50, },
		{ category = "Militia", id = "MilitiaTrainingCost", name = "Training cost", 
			editor = "number", default = 750, 
			no_edit = function(self) return not self.Militia end, min = 1, max = 10000, },
		{ category = "Conflict", id = "ForceConflict", name = "Force conflict", 
			editor = "bool", default = false, },
		{ category = "Conflict", id = "InitialSquads", name = "Initial squads", 
			editor = "string_list", default = {}, item_default = "", items = function (self) return table.keys(EnemySquadDefs, true) end, },
		{ category = "Conflict", id = "CustomConflictDescr", name = "Custom conflict description", help = "The first time a conflict is initiated in this sector, this description preset will be shown.", 
			editor = "combo", default = false, items = function (self) return PresetGroupCombo("ConflictDescription", "Default") end, },
		{ category = "Militia", id = "militia_training", 
			editor = "bool", default = false, no_edit = true, },
		{ category = "Militia", id = "militia_training_progress", 
			editor = "number", default = 0, no_edit = true, },
		{ category = "Militia", id = "militia_squad_id", 
			editor = "number", default = false, no_edit = true, },
		{ category = "Militia", id = "militia_training_payed_cost", 
			editor = "number", default = false, no_edit = true, },
		{ category = "Operation", id = "training_stat", 
			editor = "text", default = false, no_edit = true, },
		{ category = "Operation", id = "custom_operations", 
			editor = "prop_table", default = false, no_edit = true, },
		{ category = "Operation", id = "operations_temp_data", help = "Temp data for assigned mercs before the actual operation start/change. Valid only when the UI is opened in  'change' mode.", 
			editor = "prop_table", default = false, dont_save = true, no_edit = true, },
		{ category = "Operation", id = "started_operations", help = "Started operations for the sector", 
			editor = "prop_table", default = false, no_edit = true, },
		{ id = "Intel", 
			editor = "bool", default = true, },
		{ id = "intel_discovered", 
			editor = "bool", default = false, no_edit = true, },
		{ id = "player_visited", help = "Marked as visited when a player squad reaches the sector's center on the satellite.", 
			editor = "bool", default = false, no_edit = true, },
		{ id = "autoresolve_disabled", 
			editor = "bool", default = false, no_edit = true, },
		{ id = "InterestingSector", name = "Interesting sector", help = "Will be listed as one after GatherIntel operation completes and will start voice responses if passed by.", 
			editor = "bool", default = false, },
		{ id = "MinFlareCarriers", name = "Min flare carriers", help = "Minimum number of Roaming NPCs to carry a light during Night or Underground", 
			editor = "number", default = 1, slider = true, min = 0, max = 80, },
		{ id = "MaxFlareCarriers", name = "Max flare carriers", help = "Minimum number of Roaming NPCs to carry a light during Night or Underground", 
			editor = "number", default = 3, slider = true, min = function(self) return self.MinFlareCarriers end, max = function(self) return 80 end, },
		{ id = "RAndRAllowed", name = "R&R allowed", help = "R&R operation is available in this sector", 
			editor = "bool", default = false, },
		{ id = "RepairShop", name = "Repair shop", help = "Allows Craft Ammo, Craft Explosives operations in this sector", 
			editor = "bool", default = false, },
		{ category = "Travel", id = "bidirectionalRoadApply", name = "Apply roads to adjacent sectors", 
			editor = "bool", default = false, no_edit = function(self) return not self.modId end, },
		{ category = "Travel", id = "Roads", name = "Roads", help = "Roads only improve the quality of travel and lack of a road doesn't prevent travel between sectors", 
			editor = "directions_set", default = false, 
			no_edit = function(self) return self.GroundSector end, },
		{ category = "Travel", id = "ImpassableForEnemies", name = "Impassable for enemies", help = "Enemy squads can't pass through this sector", 
			editor = "bool", default = false, },
		{ category = "Diamond Briefcase", id = "ImpassableForDiamonds", name = "Impassable for diamonds", help = "Diamond shipments can't pass through this sector", 
			editor = "bool", default = false, },
		{ category = "Travel", id = "bidirectionalBlockApply", name = "Apply block travel to adjacent sectors", 
			editor = "bool", default = false, no_edit = function(self) return not self.modId end, },
		{ category = "Travel", id = "BlockTravel", name = "Block travel", help = "Blocks travel and adds ui indication for that in the satellite view (red/white line)", 
			editor = "directions_set", default = false, },
		{ category = "Travel", id = "BlockTravelRiver", name = "Block travel - invisible", help = "Blocks travel without displaying it on the sat view", 
			editor = "directions_set", default = false, 
			no_edit = function(self) return self.GroundSector end, },
		{ category = "Region",
				id = "Heat",
				name = "Heat",
				help = "Накопленная жара в этом секторе, влияет на реакцию AI.",
				editor = "number",
				default = 0,
				no_edit = true,
				min = 0,
				max = 1000, },
		{ category = "Region",
				id = "CombatHeat",
				name = "CombatHeat",
				help = "Накопленная жара этом бою.",
				editor = "number",
				default = 0,
				no_edit = true,
				min = 0,
				max = 2000, },
		{ id = "sector_data", 
			editor = "text", default = false, no_edit = true, },
		{ id = "dead_units", help = "All dead units on the map before removing and converting them to bags. Used for adding their staff to the stash", 
			editor = "nested_list", default = false, no_edit = true, base_class = "InventoryItem", },
		{ id = "sector_inventory", 
			editor = "nested_list", default = false, no_edit = true, base_class = "InventoryItem", },
		{ id = "sector_repair_items", 
			editor = "nested_list", default = false, no_edit = true, base_class = "InventoryItem", },
		{ id = "sector_repair_items_queued", 
			editor = "nested_list", default = false, no_edit = true, base_class = "InventoryItem", },
		{ id = "sector_craft_ammo_items_queued", 
			editor = "nested_list", default = false, no_edit = true, base_class = "InventoryItem", },
		{ id = "sector_craft_explosive_items_queued", 
			editor = "nested_list", default = false, no_edit = true, base_class = "InventoryItem", },
		{ id = "conflict", 
			editor = "prop_table", default = false, no_edit = true, },
		{ id = "conflict_backup", 
			editor = "prop_table", default = false, no_edit = true, },
		{ id = "guardpost_obj", 
			editor = "nested_obj", default = false, no_edit = true, base_class = "GuardpostSessionObject", },
		{ id = "image", name = "Image", 
			editor = "ui_image", default = "UI/SatelliteView/SectorImages/_Highlands", image_preview_size = 200, },
		{ id = "override_loading_screen", 
			editor = "ui_image", default = false, no_edit = true, image_preview_size = 200, },
		{ category = "Events", id = "Events", 
			editor = "nested_list", default = false, base_class = "SectorEvent", },
		{ id = "ExecutedEvents", 
			editor = "prop_table", default = false, no_edit = true, },
		{ category = "Port", id = "Port", name = "Port", 
			editor = "bool", default = false, },
		{ category = "Port", id = "PortLocked", name = "Port locked", 
			editor = "bool", default = false, },
		{ category = "Port", id = "CanBeUsedForArrival", name = "Can be used for arrival", 
			editor = "bool", default = false, },
		{ category = "Port", id = "BobbyRayDeliveryCostMultiplier", name = "Bobby Ray delivery cost multiplier", 
			editor = "number", default = 100, no_edit = function(self) return not self.CanBeUsedForArrival end, scale = "%", },
		{ category = "Port", id = "SectorImagePreview", name = "Sector image preview", 
			editor = "ui_image", default = "UI/PDA/ss_i1.png", no_edit = function(self) return not self.CanBeUsedForArrival end, },
		{ category = "Diamond Briefcase", id = "DBSourceSector", name = "Source sector", help = "Travelling squads carrying diamond shipments will spawn on this sector.", 
			editor = "bool", default = false, },
		{ category = "Diamond Briefcase", id = "DBDestinationSector", name = "Destination sector", help = "Travelling squads carrying diamond shipments will path to this sector.", 
			editor = "bool", default = false, },
		{ category = "Diamond Briefcase", id = "DBRecalc", help = "You only need to run this once when applying multiple changes. It will take a while!", 
			editor = "buttons", default = false, buttons = { {name = "Recalculate Diamond Routes", func = "GenerateDBCacheStatic", is_hidden = function(self) return config.ModdingToolsInUserMode end }, }, },
		{ category = "Port", id = "PricePerTile", name = "Price per tile", 
			editor = "number", default = false, },
		{ id = "enabled_auto_deploy", 
			editor = "bool", default = true, no_edit = true, },
		{ id = "awareness_sequence", name = "Awareness sequence", 
			editor = "choice", default = "Standard", items = function (self) return { "Standard", "Skip Setpiece", "Skip All" } end, },
		{ id = "last_enter_campaign_time", 
			editor = "number", default = 0, no_edit = true, },
		{ id = "last_own_campaign_time", 
			editor = "number", default = 0, no_edit = true, },
		{ category = "Music", id = "MusicCombat", name = "Music combat", help = "Music in turn based mode", 
			editor = "combo", default = "Battle_Easy", items = function (self) return PresetsCombo("RadioStationPreset") end, },
		{ category = "Music", id = "MusicConflict", name = "Music conflict", help = "In real time exploration but the sector is still in conflict", 
			editor = "combo", default = "Village_Conflict", items = function (self) return PresetsCombo("RadioStationPreset") end, },
		{ category = "Music", id = "MusicExploration", name = "Music exploration", help = "Real time exploration and there is no conflict in the sector", 
			editor = "combo", default = "Jungle_Exploration", items = function (self) return PresetsCombo("RadioStationPreset") end, },
		{ category = "Squads", id = "enemy_squads", 
			editor = "nested_list", default = false, dont_save = true, no_edit = true, base_class = "SatelliteSquad", },
		{ category = "Squads", id = "ally_squads", 
			editor = "nested_list", default = false, dont_save = true, no_edit = true, base_class = "SatelliteSquad", },
		{ category = "Squads", id = "underground_squads", 
			editor = "nested_list", default = false, dont_save = true, no_edit = true, base_class = "SatelliteSquad", },
		{ category = "Squads", id = "ally_and_militia_squads", 
			editor = "nested_list", default = false, dont_save = true, no_edit = true, base_class = "SatelliteSquad", },
		{ category = "Squads", id = "all_squads", 
			editor = "nested_list", default = false, dont_save = true, no_edit = true, base_class = "SatelliteSquad", },
		{ category = "Warning State", id = "warningStateEnabled", name = "Enable warning state", help = "If enabled the first time you are discovered by enemies you will enter a Warning State.\nA timer is set. Enemies become neutral until the timer expires. And effects can be executed.", 
			editor = "bool", default = false, },
		{ category = "Warning State", id = "warningReceived", name = "Warning received", 
			editor = "bool", default = false, no_edit = true, },
		{ category = "Warning State", id = "inWarningState", 
			editor = "bool", default = false, no_edit = true, },
		{ category = "Warning State", id = "warningTimerText", name = "Warning timer text", help = "Text to display when the Warning State is active.", 
			editor = "text", default = T(888882045986, --[[ClassDef Satellite View SatelliteSector default]] "Exit the Area"), no_edit = function(self) return not self.warningStateEnabled end, translate = true, },
		{ category = "Warning State", id = "warningStateTimer", name = "Warning state timer", help = "How long (sec) will the Warning State hold.", 
			editor = "number", default = 30000, no_edit = function(self) return not self.warningStateEnabled end, scale = "sec", min = 0, },
		{ category = "Warning State", id = "warningBanters", name = "Warning banters", help = "List of banters from which to choose one to play when spotted by the nearest enemy.", 
			editor = "preset_id_list", default = {}, no_edit = function(self) return not self.warningStateEnabled end, preset_class = "BanterDef", item_default = "", },
		{ category = "Combat Tasks", id = "combatTaskGenerate", name = "When to generate", help = "When to generate Combat Tasks. Chances and cooldowns are independant and are always taken into account.", 
			editor = "choice", default = "always", items = function (self) return {"always", "afterFirstConflict", "never"} end, },
		{ category = "Combat Tasks", id = "combatTaskAmount", name = "Maximum amount", help = "Maximum Combat Tasks that can be given.", 
			editor = "number", default = 1, min = 0, },
		{ category = "Combat Tasks", id = "firstConflictWon", 
			editor = "bool", default = false, no_edit = true, },
		{ id = "conflictLoyaltyGained", help = "Checks whether to give loyalty on Conflict Win. Resets on sector lost and sector defended.", 
			editor = "bool", default = false, no_edit = true, },
		{ id = "startingEnemy", help = "Количество врагов на начало боя", 
			editor = "number", default = 0, no_edit = true, },	
	},
	EditorView = Untranslated("<if_any(inherited,generated)><color 128 128 128></if><Id><opt(u(display_name),' ','')><if(inherited)> [inherited]</if><if(generated)> [generated - empty]</if>"),
	FilterClass = "SatelliteSectorGedFilter",
	generated = false,
	inherited = false,
}

function SatelliteSector:GetError()
	local errors = {}
	
	if self.Guardpost and not next(self.EnemySquadsList) then
		table.insert(errors, string.format("%s: Please select at least one enemy squad for guardpost", self.Id))
	elseif self.Guardpost then
		for _, squad in ipairs(self.EnemySquadsList) do
			if squad == "" then
				table.insert(errors, string.format("Please remove empty entries from guardpost enemy squads", self.Id))
				break
			end
		end
	end
	
	local radios = Presets.RadioStationPreset["Default"]
	if not radios[self.MusicCombat] then
		table.insert(errors, string.format("%s: '%s' Music Combat radio station is invalid!", self.Id, self.MusicCombat))
	end
	if not radios[self.MusicConflict] then
		table.insert(errors, string.format("%s: '%s' Music Conflict radio station is invalid!", self.Id, self.MusicConflict))
	end
	if not radios[self.MusicExploration] then
		table.insert(errors, string.format("%s: '%s' Music Exploration radio station is invalid!", self.Id, self.MusicExploration))
	end
	
	local mapdata = MapData[self.Map]
	local region = mapdata and mapdata.Region
	if region and GameStateDefs[region].WeatherCycle and not self.WeatherZone then
		table.insert(errors, string.format("Sectors from region %s need to have WeatherZone defined", region))
	end
	
	return next(errors) and table.concat(errors, "\n") or nil
end

function SatelliteSector:OnEditorNew(parent, ged, is_paste)
	if parent.mod and IsKindOf(parent, "ModItemSector") then
		self.Id = parent.sectorId
		self.Map = parent:GetMapName()
		self.modId = parent.mod.id
		self.bidirectionalRoadApply = true
		self.bidirectionalBlockApply = true
		parent.SatelliteSectorObj = self
		parent:PostLoad()
	end
end

function SatelliteSector:EditGeneratedSector(root, prop_id, ged)
	self.inherited = nil
	self.generated = nil
	ObjModified(self)
	ged:SetUiStatus("editing_sector", "Editing sector...")
	if g_SatelliteUI then
		g_SatelliteUI:RebuildSectorGrid()
	end
	ged:SetUiStatus("editing_sector")
end

function SatelliteSector:AddUndergroundSector(root, prop_id, ged)
	CreateRealTimeThread(function()
		local id = self.Id .. "_Underground"
		local sector = PlaceObject("SatelliteSector")
		sector.GroundSector = self.Id
		sector:SetId(id)
		
		local sectors = GetParentTable(self)
		local idx = table.find(sectors, "Id", self.Id) + 1
		table.insert(sectors, idx, sector)
		UpdateParentTable(sector, sectors)
		
		ged:SetUiStatus("add_sector", "Adding sector...")
		CreateSessionCampaignObject(sector, SatelliteSector, gv_Sectors, "Sectors")
		if g_SatelliteUI then
			g_SatelliteUI:RebuildSectorGrid()
		end
		ObjModified(sectors)
		Sleep(100)
		ged:SetSelection("root", { idx }, nil, "notify")
		ged:SetUiStatus("add_sector")
	end)
end

function SatelliteSector:SelectUndergroundSector(root, prop_id, ged)
	CreateRealTimeThread(function()
		ged:ResetFilter("root")
		Sleep(100)
		ged:SetSelection("root", { table.find(GetParentTable(self), "Id", self.Id .. "_Underground") }, nil, "notify")
	end)
end

function SatelliteSector:RemoveSector(root, prop_id, ged)
	CreateRealTimeThread(function()
		local sectors = GetParentTable(self)
		table.remove_value(sectors, self)
		GetParentTableOfKind(self, "CampaignPreset"):PostLoad() -- rerun sector inheritance
		if not table.find(sectors, "Id", self.Id) then
			DeleteSessionCampaignObject(self, SatelliteSector, gv_Sectors)
		end
		
		ged:SetUiStatus("remove_sector", "Removing sector...")
		if g_SatelliteUI then
			g_SatelliteUI:RebuildSectorGrid()
		end
		ObjModified(sectors)
		Sleep(100)
		ged:SetSelection("root", { table.find(GetParentTable(self), "Id", self.Id:gsub("_Underground", "")) }, nil, "notify")
		ged:SetUiStatus("remove_sector")
	end)
end

function SatelliteSector:GenerateDBCacheStatic(root, prop_id, ged)
	GenerateDynamicDBPathCache("save", ged)
end

function SatelliteSector:GetTravelPrice(squad)
	local cost = self.PricePerTile or const.Satellite.DefaultPortPricePerTile
	local discounts = false
	
	local cityHere = gv_Cities[self.City]
	if cityHere and cityHere.Loyalty > 0 then
			local discount = Lerp(0, 50, cityHere.Loyalty, 100)
			cost = cost - MulDivRound(cost, discount, 100)
			
			if not discounts then discounts = {} end
			discounts[#discounts + 1] = {
				label = T(342530626078, "Loyalty"),
				percent = discount
			}
	end
	
	if IsKindOf(squad, "SatelliteSquad") then
		for _, id in ipairs(squad.units) do
			local unit = gv_UnitData[id]
			if HasPerk(unit, "Negotiator") then
				local discount = CharacterEffectDefs.Negotiator:ResolveValue("discountPercent")
				if not discounts then discounts = {} end
				discounts[#discounts + 1] = {
					label = T{542222741234, "<Nick> <em>(<perkName>)</em>", Nick = unit.Nick, perkName = CharacterEffectDefs.Negotiator.DisplayName},
					percent = discount,
				}
				cost = cost - MulDivRound(cost, discount, 100)
				break
			end
		end
	end
	
	return cost, discounts
end

function SatelliteSector:IsReadOnly()
	return self.generated or self.inherited or (config.ModdingToolsInUserMode and not self.modId)
end



function GetMineIncome(sector_id, showEvenIfUnowned)
	local sector = gv_Sectors[sector_id]

	-- No income for this sector
--	if (not sector.Mine and not sector.Farm and not sector.City) or not sector.mine_enabled then
    if not sector.Mine or not sector.mine_enabled then
		return
	end

	
	local city_loyalty = GetCityLoyalty(sector.City) or 100
	if sector.Side ~= "player1" then
		if showEvenIfUnowned then
			city_loyalty = 50
		else
			return
		end
	end
	
	local sectorDepletionTime = GetSectorDepletionTime(sector)
	local perc = 100
	if sector.Depletion and sector.mine_work_days and sector.mine_work_days > sectorDepletionTime then
		local daysSinceStartedDepleting = sector.mine_work_days - sectorDepletionTime
		perc = Lerp(100, 0, daysSinceStartedDepleting, const.Satellite.MineDepletingDays)
		perc = Max(0, perc)
	end
	
	local difficultyPreset = GameDifficulties[GetGameDifficulty()]
	local difficultyPercent = difficultyPreset and difficultyPreset:ResolveValue("DepletedMineIncomePerc")
	local incomeAtDepletion = difficultyPercent or 0
	perc = Max(perc, incomeAtDepletion)
	
	if perc == 0 then
		return
	end
	
	local income = GetSectorDailyIncomeMine(sector)
	income = perc * income / 100
	return income * (50 + city_loyalty / 2 ) / 100
end

function GetFarmIncome(sector_id, showEvenIfUnowned, type)
	local sector = gv_Sectors[sector_id]

	-- No income for this sector
--	if (not sector.Mine and not sector.Farm and not sector.City) or not sector.mine_enabled then
    if  not sector.Farm then
		return
	end

	
	local city_loyalty = GetCityLoyalty(sector.City) or 100
	if sector.Side ~= "player1" then
		if showEvenIfUnowned then
			city_loyalty = 10
		else
			return
		end
	end
	
	local income = 0
	if city_loyalty > 10 then
	income = GetSectorDailyIncomeFarm(sector)
	else income = 0 end

	return income * (10 + city_loyalty / 10 * 9 ) / 100
end

function GetWoodIncome(sector_id, showEvenIfUnowned, type)
	local sector = gv_Sectors[sector_id]

	-- No income for this sector
--	if (not sector.Mine and not sector.Farm and not sector.City) or not sector.mine_enabled then
    if  not sector.Wood then
		return
	end

	
	local city_loyalty = GetCityLoyalty(sector.City) or 100
	if sector.Side ~= "player1" then
		if showEvenIfUnowned then
			city_loyalty = 10
		else
			return
		end
	end
	
	local income = 0
	if city_loyalty > 10 then
	income = GetSectorDailyIncomeWood(sector)
	else income = 0 end

	return income * (10 + city_loyalty / 10 * 9 ) / 100
end

function GetSlonIncome(sector_id, showEvenIfUnowned, type)
	local sector = gv_Sectors[sector_id]

	-- No income for this sector
--	if (not sector.Mine and not sector.Farm and not sector.City) or not sector.mine_enabled then
    if  not sector.Wood then
		return
	end

	
	local city_loyalty = GetCityLoyalty(sector.City) or 100
	if sector.Side ~= "player1" then
		if showEvenIfUnowned then
			city_loyalty = 10
		else
			return
		end
	end
	
	local income = 0
	if city_loyalty > 10 then
	income = GetSectorDailyIncomeSlon(sector)
	else income = 0 end

	return income-- * (50 + city_loyalty / 10 * 5 ) / 100
end


function GetDonationsIncome(sector_id, showEvenIfUnowned, type)
	local sector = gv_Sectors[sector_id]

	-- No income for this sector
--	if (not sector.Mine and not sector.Farm and not sector.City) or not sector.mine_enabled then
    if  not sector.Donations then
		return
	end

	
	local city_loyalty = GetCityLoyalty(sector.City) or 100
	if sector.Side ~= "player1" then
		if showEvenIfUnowned then
			city_loyalty = 10
		else
			return
		end
	end
	
	local income = 0
	if city_loyalty > 50 then
	income = GetSectorDailyIncomeDonations(sector)
	else income = 0 end

	return income * city_loyalty / 100
end


function PointOfInterestRolloverClass:GetPOITitleForRollover(buildingId, sector)
	if not buildingId or not sector or not g_SatelliteUI then return end
	
	local poiPreset = table.find_value(POIDescriptions, "id", buildingId)
	if not poiPreset then return false end
	
	local rightText = false
	if buildingId == "Port" then
		local selectedSquad = g_SatelliteUI.selected_squad
		local travelCost = sector:GetTravelPrice(selectedSquad)

		if sector.PortLocked then
			rightText = T(319590646964, "Inactive")
		else
			rightText = T{241693398390, "<moneyWithSign(cost)>/sector",
				cost = -travelCost
			}
		end
	elseif buildingId == "Mine" or buildingId == "City" then
		local income  = GetMineIncome(sector.Id, "evenIfUnowned")
		if income then
			rightText = T{374101510295, "<moneyWithSign(income)>/day", income = income}
		elseif sector.mine_depleted then
			rightText = T(670636571444, "Depleted")
		end
    elseif buildingId == "Farm" and not sector.FarmLocked then
        local income = GetFarmIncome(sector.Id, "evenIfUnowned")
        if income then
			rightText = T{374101510295, "<moneyWithSign(income)>/day", income = income}
        end
        if sector.FarmLocked then
			rightText = T(319590646964, "Inactive")
		end
    elseif buildingId == "Donations" and not sector.DonationsLocked then
        local income = GetDonationsIncome(sector.Id, "evenIfUnowned")
        if income then
			rightText = T{374101510295, "<moneyWithSign(income)>/day", income = income}
        end
	elseif buildingId == "Slon" and not sector.DonationsLocked then
        local income = GetSlonIncome(sector.Id, "evenIfUnowned")
        if income then
			rightText = T{374101510295, "<moneyWithSign(income)>/day", income = income}
        end
	elseif buildingId == "Wood" and not sector.DonationsLocked then
        local income = GetWoodIncome(sector.Id, "evenIfUnowned")
        if income then
			rightText = T{374101510295, "<moneyWithSign(income)>/day", income = income}
        end		
        if sector.DonationsLocked then
			rightText = T(319590646964, "Inactive")
		end    
	elseif buildingId == "Hospital" then
		if sector.HospitalLocked then
			rightText = T(319590646964, "Inactive")
		end
	end
	
	if rightText then
		rightText = T{985521229804, "<right><style PDASectorInfo_ValueLight><text></style>", text = rightText}
		return poiPreset.display_name .. rightText
	end
	
	return poiPreset.display_name
end


function GetSatelliteIconImages(context)
	local base_img, upper_img = "UI/Icons/SateliteView/icon_neutral", "UI/Icons/SateliteView/hospital"
	local side = context.side
	local is_enemy = side=="enemy1" or side=="enemy2"
	local is_player = side=="player1" or side=="player2"
	local is_ally = is_player or side== "ally"
	local is_neutral = side=="neutral"

	if is_enemy then
		base_img = "UI/Icons/SateliteView/icon_enemy"
	elseif is_ally then
		base_img = "UI/Icons/SateliteView/icon_ally"
	end
	local squad_id = context.squad
	local squad = gv_Squads[squad_id]

	if squad then
		if is_ally then
			base_img = "UI/Icons/SateliteView/merc_squad"
			if is_player then
				upper_img = (squad.image and squad.image.."_s") or "UI/Icons/SquadLogo/squad_logo_01_s"
			else
				upper_img = "UI/Icons/SquadLogo/squad_logo_01_s"
			end
		elseif squad.diamond_briefcase then
			local shipmentPresetId = squad.shipment_preset_id
			local shipmentPreset = shipmentPresetId and ShipmentPresets[shipmentPresetId]
			base_img = shipmentPreset and shipmentPreset.squad_icon or "UI/Icons/SateliteView/enemy_squad_diamonds"
			upper_img = false
		elseif squad.image then
			base_img = squad.image
			upper_img = false
		end
	end

	local building = context.building
	if #(building or "") > 0 then
		local image
		local preset = table.find_value(POIDescriptions, "id", building)
		if preset and preset.icon then
			image = preset and preset.icon
			if building == "Mine" and context.sector and context.sector.mine_depleted then
				image = image .. "_depleted"
			elseif is_neutral and image then
				image = image .. "_neutral"
			end
		end
		upper_img = image and ("Mod/e6L4ECj/Satmapicons/" .. image .. ".png")
	end
	local intel = context.intel
	if intel~= nil then
		local image = intel and "intel_available" or "intel_missing"
		upper_img = "Mod/e6L4ECj/Satmapicons/"..image
	end
	local suf  = context.map and "_2" or ""
	return base_img..suf, upper_img
end


function GetSectorDailyIncome(sector)
	return GetSectorDailyIncomeMine(sector)+GetSectorDailyIncomeFarm(sector)+GetSectorDailyIncomeDonations(sector)+GetSectorDailyIncomeWood(sector)+GetSectorDailyIncomeSlon(sector)
end

function GetSectorDailyIncomeSector(baseVal,sector)
--	local baseVal = 0
--    if sector.DailyIncome then baseVal = baseVal + sector.DailyIncome end

	local baseValDiffPerc = PercentModifyByDifficulty(GameDifficulties[Game.game_difficulty]:ResolveValue("sectorDailyIncomeBonus"))
	baseVal = MulDivRound(baseVal, baseValDiffPerc, 100)
	
	local percentAccum = 100
	for i, m in ipairs(sector.income_mods) do
		percentAccum = percentAccum + (m - 100)
	end
	return MulDivRound(baseVal, percentAccum, 100)
end

function GetSectorDailyIncomeMine(sector)
	local baseVal = 0
    if sector.DailyIncome then baseVal = baseVal + sector.DailyIncome end

	return GetSectorDailyIncomeSector(baseVal, sector)
end

function GetSectorDailyIncomeFarm(sector)
	local baseVal = 0
    if sector.DailyIncomeFarm and not sector.FarmLocked then baseVal = baseVal + sector.DailyIncomeFarm end

	return GetSectorDailyIncomeSector(baseVal, sector)
end

function GetSectorDailyIncomeDonations(sector)
	local baseVal = 0
    if sector.DailyIncomeDonations and not sector.DonationsLocked then baseVal = baseVal + sector.DailyIncomeDonations end

	return GetSectorDailyIncomeSector(baseVal, sector)
end

function GetSectorDailyIncomeSlon(sector)
	local baseVal = 0
    if sector.DailyIncomeSlon and not sector.SlonLocked then baseVal = baseVal + sector.DailyIncomeSlon end

	return GetSectorDailyIncomeSector(baseVal, sector)
end

function GetSectorDailyIncomeWood(sector)
	local baseVal = 0
    if sector.DailyIncomeWood and not sector.WoodLocked then baseVal = baseVal + sector.DailyIncomeWood end

	return GetSectorDailyIncomeSector(baseVal, sector)
end

local function GetAllSources(id)
	return (GetMineIncome(id) or 0) + (GetFarmIncome(id) or 0) + (GetDonationsIncome(id) or 0) + (GetWoodIncome(id) or 0) + (GetSlonIncome(id) or 0)
end

function GetIncome(days)
	local income = 0
	days = days or 1
	
	for id, sector in sorted_pairs(gv_Sectors) do
		income = income + GetAllSources(id)
	end
	
	income =  income + GetForgivingModeDailyIncome()
	
	return income * days
end

function OnMsg.SectorsTick(tick, ticks_per_day)
	for id, sector in sorted_pairs(gv_Sectors) do
		local income = GetAllSources(id)
		if income then
			income = GetAmountPerTick(income, tick, ticks_per_day)
			AddMoney(income, "income", "noCombatLog")
			if tick + 1 == ticks_per_day then
				sector.mine_work_days = (sector.mine_work_days or 0) + 1
				
				local sectorDepletionTime = GetSectorDepletionTime(sector)
				if not sector.mine_depleted and sector.Depletion and sector.mine_work_days >= sectorDepletionTime + const.Satellite.MineDepletingDays then
					sector.mine_depleted = true
					CombatLog("important", T{268514931670, "<SectorName(sector)> is depleted.", sector = sector})
					if g_SatelliteUI then g_SatelliteUI:UpdateSectorVisuals(id) end
				end
			end
		end
		
		-- If an enemy had a waiting conflict for this sector that it needs to stop waiting due
		-- to the squad dying or whatever else
		local conflict = sector and sector.conflict
		if conflict and conflict.waiting and not conflict.player_attacking and not EnemyWantsToWait(id) then
			EnterConflict(sector)
		end
		
		ExecuteSectorEvents("SE_OnTick", id)
	end
end





