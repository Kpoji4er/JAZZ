function OnMsg.ClassesBuilt()
	SideDefs = {
		CampaignSide:new{ Id = "neutral",      DisplayName = T(521973101724, "Neutral") },
		CampaignSide:new{ Id = "player1",      DisplayName = T(222892508302, "Player 1"), Player = true },
		CampaignSide:new{ Id = "player2",      DisplayName = T(942355779355, "Player 2"), Player = true },
		CampaignSide:new{ Id = "enemy1",       DisplayName = T(692913892455, "Enemy 1"), Enemy = true },
		CampaignSide:new{ Id = "enemy2",       DisplayName = T(456135028453, "Enemy 2"), Enemy = true },
		CampaignSide:new{ Id = "enemyNeutral", DisplayName = T(607169506860, "Enemy Neutral"), },
		CampaignSide:new{ Id = "ally",         DisplayName = T(346100175449, "Ally"), },
        CampaignSide:new{ Id = "Rebels",         DisplayName = T(34610017544911, "Повстанцы"), loyalty = 0 },
        CampaignSide:new{ Id = "Legion",       DisplayName = T(69291389245512, "Легион"), Enemy = true, loyalty = 0 },
        CampaignSide:new{ Id = "Army",       DisplayName = T(69291389245511, "Армия"), Enemy = true, loyalty = 0 },
		CampaignSide:new{ Id = "Adonis",       DisplayName = T(45613502845311, "Адонис"), Enemy = true, loyalty = 0 },
	}
	Sides = table.map(SideDefs, "Id")
end


UndefineClass('SatelliteSquad')
DefineClass.SatelliteSquad = {
	__parents = { "PropertyObject", },
	__generated_by_class = "ClassDef",

	properties = {
		{ id = "Side", 
			editor = "combo", default = "enemy1", items = function (self) return Sides end, },
		{ id = "Name", 
			editor = "text", default = false, },
		{ id = "image", 
			editor = "text", default = false, },
		{ id = "UniqueId", 
			editor = "number", default = false, },
		{ id = "CurrentSector", 
			editor = "combo", default = false, items = function (self) return GetCampaignSectorsCombo() end, },
		{ id = "PreviousSector", 
			editor = "text", default = false, no_edit = true, },
		{ id = "PreviousLandSector", 
			editor = "text", default = false, no_edit = true, },
		{ id = "Sleep", 
			editor = "bool", default = false, },
		{ id = "Retreat", 
			editor = "bool", default = false, },
		{ id = "VisualPos", 
			editor = "point", default = false, },
		{ id = "XVisualPos", 
			editor = "point", default = false, },
		{ id = "route", 
			editor = "prop_table", default = false, },
		{ id = "water_route", 
			editor = "prop_table", default = false, },
		{ id = "water_travel", 
			editor = "bool", default = false, },
		{ id = "returning_water_travel", 
			editor = "bool", default = false, no_edit = true, },
		{ id = "water_travel_rest_timer", 
			editor = "number", default = 0, },
		{ id = "traversing_shortcut_start", 
			editor = "number", default = false, },
		{ id = "traversing_shortcut_start_sId", 
			editor = "text", default = false, translate = true, },
		{ id = "traversing_shortcut_water", 
			editor = "bool", default = false, no_edit = true, },
		{ id = "uninterruptable_travel", 
			editor = "bool", default = false, no_edit = true, },
		{ id = "joining_squad", 
			editor = "number", default = false, },
		{ id = "units", 
			editor = "prop_table", default = false, },
		{ id = "militia", help = "Militia squad", 
			editor = "bool", default = false, no_edit = true, },
		{ id = "arrival_squad", help = "Squad not on the map yet", 
			editor = "bool", default = false, no_edit = true, },
		{ id = "diamond_briefcase", 
			editor = "bool", default = false, no_edit = true, },
		{ id = "shipment_preset_id", 
			editor = "text", default = false, no_edit = true, translate = true, },
		{ id = "guardpost", 
			editor = "bool", default = false, no_edit = true, },
		{ id = "diamond_briefcase_dynamic", 
			editor = "bool", default = false, no_edit = true, },
		{ id = "always_visible", 
			editor = "bool", default = false, no_edit = true, },
		{ id = "villain", help = "Villain squad", 
			editor = "bool", default = false, no_edit = true, },
		{ id = "ref", help = "Used by UI in objects which pretend to be squads, because of duck typing it needs to be in the squad definition as well", 
			editor = "bool", default = false, dont_save = true, read_only = true, no_edit = true, },
		{ id = "enemy_squad_def", 
			editor = "text", default = false, no_edit = true, },
		{ id = "wait_in_sector", 
			editor = "number", default = false, no_edit = true, },
		{ id = "arrive_in_sector", 
			editor = "prop_table", default = false, no_edit = true, },
		{ id = "vrForActivity", 
			editor = "prop_table", default = false, },
		{ id = "squad_bag", 
			editor = "nested_list", default = false, no_edit = true, base_class = "InventoryItem", },
		{ id = "on_reach_quest", 
			editor = "text", default = false, no_edit = true, },
		{ id = "on_reach_var", 
			editor = "prop_table", default = false, no_edit = true, },
	},
}

--- Cancels the travel of the SatelliteSquad.
---
--- This function is called to cancel the travel of the SatelliteSquad. It sends a network sync event to notify other clients of the cancellation.
---
--- @function CancelTravel
--- @return nil
function SatelliteSquad:CancelTravel()
	NetSyncEvent("SquadCancelTravel", self.UniqueId)
end


UndefineClass('EnemySquads')
DefineClass.EnemySquads = {
	__parents = { "Preset", },
	__generated_by_class = "PresetDef",

	properties = {
		{ id = "displayName", name = "Squad Display Name", 
			editor = "text", default = false, translate = true, },
        { id = "Side", 
            editor = "combo", default = "enemy1", items = function (self) return Sides end, },                   	
		{ id = "SquadPowerRange", name = "Squad Power Range", help = "Shows min squad power: lowestPowerUnits * lowestAmountSpawned. And max squad power: highestPowerUnits * higestAmountSpawned", 
			editor = "text", default = false, dont_save = true, read_only = true, },
		{ id = "Units", 
			editor = "nested_list", default = false, base_class = "EnemySquadUnit", auto_expand = true, },
		{ category = "Bombard", id = "Bombard", 
			editor = "bool", default = false, },
		{ category = "Diamond Briefcase", id = "DiamondBriefcase", name = "Has Diamond Shipment", 
			editor = "bool", default = false, },
		{ category = "Diamond Briefcase", id = "DiamondBriefcaseCarrier", name = "Carrier", help = "Valid carries are unit defs with only a single unit to be spawned from them. The chance to spawn should be set to 100%", 
			editor = "choice", default = false, items = function (self) return self:GetValidCarriers() end, },
		{ category = "Bombard", id = "BombardOrdnance", name = "Ordnance", 
			editor = "preset_id", default = false, 
			no_edit = function(self) return not self.Bombard end, preset_class = "InventoryItemCompositeDef", preset_filter = function (preset, obj, prop_meta)
	return preset.object_class == "Ordnance"
end, 
},
		{ category = "Bombard", id = "BombardShots", name = "Num Shells", 
			editor = "number", default = 1, 
			no_edit = function(self) return not self.Bombard end, min = 1, },
		{ category = "Bombard", id = "BombardAreaRadius", name = "Area Radius", help = "in tiles", 
			editor = "number", default = 3, 
			no_edit = function(self) return not self.Bombard end, min = 1, max = 99, },
		{ category = "Bombard", id = "BombardLaunchOffset", name = "Launch Offset", help = "defines the direction of the fall together with Launch Angle; if left as 0 the shells will fall directly down", 
			editor = "number", default = 5000, 
			no_edit = function(self) return not self.Bombard end, scale = "m", },
		{ category = "Bombard", id = "BombardLaunchAngle", name = "Launch Angle", help = "defines the direction of the fall together with Launch Offset", 
			editor = "number", default = 1200, 
			no_edit = function(self) return not self.Bombard end, scale = "deg", },
		{ category = "Patrol", id = "patrolling", name = "Patrolling", help = "The squad will be set to travel between the specified waypoints when spawned.", 
			editor = "bool", default = false, no_edit = true },
		{ category = "Patrol", id = "waypoints", name = "Waypoints", 
			editor = "string_list", default = {}, no_edit = function(self) return not self.patrolling end, item_default = "", items = function (self) return GetCampaignSectorsCombo() end, no_edit = true },
		{ category = "AutoResolveTest", id = "playerSquadAutoTest", name = "Player Squad", help = "Leave as false to use current squad.", 
			editor = "combo", default = false, items = function (self) return EnemySquadsComboItems() end, },
		{ category = "AutoResolveTest", id = "buttonTestInAutoResolve", 
			editor = "buttons", default = false, buttons = { {name = "Test in AutoResolve", func = "TestInAutoResolve"}, }, template = true, },
	},
	GlobalMap = "EnemySquadDefs",
	EditorIcon = "CommonAssets/UI/Icons/group",
	EditorMenubar = "Scripting",
	EditorMenubarSortKey = "4010",
	EditorPreview = Untranslated("<Preview>"),
}

--- Checks if the `EnemySquads` object has any units defined. If there are no units, returns an error message.
---
--- @return string|nil An error message if there are no units defined, or `nil` if units are defined.
function EnemySquads:GetError()
	if #(self.Units or "") == 0 then
		return "Add units in squad"
	end
end

---
--- Returns a list of valid carrier units for the Diamond Briefcase feature.
---
--- A valid carrier unit is one that has a unit count min and max of 1, meaning it can only spawn a single unit.
--- The returned list contains the name and index of each valid carrier unit.
---
--- @return table An array of tables, where each inner table has a `name` and `value` field.
function EnemySquads:GetValidCarriers()
	local arr = { { } }
	for i, u in ipairs(self.Units) do
		if u.UnitCountMax == 1 and u.UnitCountMin == 1 then
			local name = u:GetEditorView()
			local item = { name = name, value = i }
			arr[#arr + 1] = item
		end
	end
	
	return arr
end

---
--- Returns a preview string for the enemy squad, containing the names of all the units in the squad.
---
--- @return string The preview string for the enemy squad.
function EnemySquads:GetPreview()
	local texts = {}
	for _, squad_unit_def in ipairs(self.Units) do
		texts[#texts + 1] = squad_unit_def:GetEditorView()
	end
	return table.concat(texts, ", ")
end

---
--- Returns a string representation of the minimum and maximum squad power for the enemy squad.
---
--- The squad power is calculated by summing the minimum and maximum power of all the units in the squad,
--- taking into account the unit count min and max for each unit group.
---
--- @return string A string in the format "minPower - maxPower" representing the squad power range.
function EnemySquads:GetSquadPowerRange()
	local minSquadPower = 0
	local maxSquadPower = 0
	for _, unitGroups in ipairs(self.Units) do
		local lowestPower
		local highestPower
		local minCount = unitGroups.UnitCountMin
		local maxCount = unitGroups.UnitCountMax
		for _, unitData in ipairs(unitGroups.weightedList) do
			local unitPreset = UnitDataDefs[unitData.unitType]
			if unitPreset then
				local power = GetPowerOfUnit(unitPreset, "noMods")
				if not lowestPower or lowestPower > power then
					lowestPower = power
				end
				if not highestPower or highestPower < power then
					highestPower = power
				end
			end
		end
		minSquadPower = minSquadPower + (lowestPower and (lowestPower * minCount) or 0)
		maxSquadPower = maxSquadPower + (highestPower and (highestPower * maxCount) or 0)
	end
	return tostring(minSquadPower) .. " - " .. tostring(maxSquadPower)
end

---
--- Tests the EnemySquads object in the satellite view auto-resolve mode.
---
--- If the satellite view is not active, prints a message and returns.
--- Otherwise, reveals all sectors, gets the selected squad from the satellite dialog,
--- and generates an enemy squad in sector A1. If the playerSquadAutoTest property is set,
--- it also generates a player squad in the same sector.
---
--- @param root table The root object of the property editor.
--- @param prop_id string The ID of the property being edited.
--- @param ged table The game editor object.
---
function EnemySquads:TestInAutoResolve(root, prop_id, ged)
	if not gv_SatelliteView then 
		print("Must be in sat view")
		return
	end
	RevealAllSectors()
	local dlg = GetSatelliteDialog()
	local selected_squad = dlg.selected_squad
	
	if not self.playerSquadAutoTest then
		NetEchoEvent("CheatSatelliteTeleportSquad", selected_squad.UniqueId, "B1")
	end
	
	local sector = gv_Sectors["A1"]
	sector.Side = "player1"
	local allySquads, enemySquads = GetSquadsInSector(sector.Id, nil, "includeMilitia")
	
	for _, squad in ipairs(enemySquads) do
		RemoveSquad(squad)
	end
	for _, squad in ipairs(allySquads) do
		RemoveSquad(squad)
	end
	
	GenerateEnemySquad(self.id, sector.Id, "Effect", nil, "enemy1")
	
	if self.playerSquadAutoTest then
		local isMilitia = EnemySquadDefs[self.playerSquadAutoTest] and EnemySquadDefs[self.playerSquadAutoTest].group == "MilitiaAutoresolveTest"
		GenerateEnemySquad(self.playerSquadAutoTest, sector.Id, "Effect", nil, isMilitia and "ally" or "player1", isMilitia)
	else
		NetEchoEvent("CheatSatelliteTeleportSquad", selected_squad.UniqueId, sector.Id)
	end
end