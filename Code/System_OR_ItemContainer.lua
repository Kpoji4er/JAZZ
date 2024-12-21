-- base class handling the syncronization to sector inventory

UndefineClass('ItemContainer')
DefineClass.ItemContainer = {
	__parents = { "SectorInventoryObj", "Lockpickable", "BoobyTrappable" },
	flags = { efSelectable = true },
	inventory_slots = {
		{ slot_name = "Inventory", width = 7, height = 2, base_class = "InventoryItem", enabled = true, dont_save = true },
	},
	bOpened = false,
	interacting_unit = false,
}

function ItemContainer:GameInit()
	PlayFX("Spawn", "start", self)
end

function ItemContainer:Done()
	PlayFX("Spawn", "end", self)
end

function ItemContainer:Open(unit)
	NetUpdateHash("ItemContainer:Open", self, self.lockpickState)
	if self:CannotOpen() then
		NetUpdateHash("ItemContainer:Open:CannotOpen")
		return self:PlayCannotOpenFX(unit)
	end
	
	if self:TriggerTrap(unit) then
		NetUpdateHash("ItemContainer:Open:TriggerTrap")
		return false
	end
	
	self:PlayLockpickableFX("open")
	
	local visuals = ResolveInteractableVisualObjects(self)
	for i,obj in ipairs(visuals) do
		NetUpdateHash("ItemContainer:Open_loop", i, obj, obj:GetStateText(), obj:GetEntity(), IsValidEntity(obj:GetEntity()), obj:HasState("open"))
		if obj:GetStateText() == "idle" and IsValidEntity(obj:GetEntity()) and obj:HasState("open") then
			if obj:HasState("opening") then
				local anim_duration = GetAnimDuration(obj, "opening")
				NetUpdateHash("ItemContainer:Open_Sleep", anim_duration, obj, obj:GetStateText())
				obj:SetState("opening")
				Sleep(anim_duration)
			end
			obj:SetState("open")
			break
		end
	end
	
	self.bOpened = true

	local cdata = self:GetSectorContainerData()
	if cdata then
		cdata[2] = self.bOpened
		-- add items
		local items = {}
		self:ForEachItem(function(item, slot_name, left, top, items)
			items[#items + 1] = item
		end, items)
		cdata[3] = items
	end
	
	return true
end

function ItemContainer:IsOpened()
	return self.bOpened
end

function ItemContainer:GetTitle()
	return T(532393878412, "Item container")
end

function ItemContainer:GetInteractionCombatAction(unit)
	if self.interacting_unit then return end
	
	local trapAction, icon = BoobyTrappable.GetInteractionCombatAction(self, unit)
	if trapAction then return trapAction, icon end
	
	if self:CannotOpen() then
		local baseAction = Lockpickable.GetInteractionCombatAction(self, unit)
		if baseAction then return baseAction end 
	end
	
	return Presets.CombatAction.Interactions.Interact_LootContainer
end

function ItemContainer:RegisterInteractingUnit(unit)
	assert(not self.interacting_unit)
	self.interacting_unit = unit
	self:DespawnCheck()
end

function MultipleRegisterInteractingUnit(containers, unit)
	for i, container in ipairs(containers) do
		if not container.interacting_unit then
			container:RegisterInteractingUnit(unit)
		end
	end
end

function ItemContainer:UnregisterInteractingUnit(unit)
	assert(self.interacting_unit == unit)
	self.interacting_unit = nil
	self:DespawnCheck()
end

function MultipleUnregisterInteractingUnit(containers, unit)
	for i, container in ipairs(containers) do
		if container.interacting_unit == unit then
			container:UnregisterInteractingUnit(unit)
		end
	end
end

function ItemContainer:EndInteraction(unit)
	Interactable.EndInteraction(self, unit)
end

function ItemContainer:LockpickStateChanged(status)
	local state = false
	if self:CannotOpen() then
		state = "idle"
	elseif status == "open" then
		state = "open"
	end
	if not state then return end
	
	local visuals = ResolveInteractableVisualObjects(self)
	for i,obj in ipairs(visuals) do
		if obj:HasState(state) then obj:SetState(state) end
	end
end

function ItemContainer:SetDynamicData(data)
	self.bOpened = data.bOpened
	if self.bOpened then
		local visuals = ResolveInteractableVisualObjects(self)
		for i,obj in ipairs(visuals) do
			if obj:HasState("open") then
				obj:SetState("open")
			end
		end
	end
end

function ItemContainer:GetDynamicData(data)
	if self.bOpened then
		data.bOpened = self.bOpened
	end
end

function NetSyncEvents.OpenContainer(container, unit_id)
	if not container then return end

	local unit = g_Units[unit_id]
	if not container:IsOpened() then
		container:Open(unit)
	end
end

function OnMsg.LockpickableBrokeOpen(self)
	-- Breaking an inventory objects incurs a condition penalty
	-- and a chance to destroy non guaranteed drop items.
	local destroyedAny
	if IsKindOf(self, "Inventory") then
		self:ForEachItem(function(item, slot_name, left, top)
			if IsKindOf(item, "ItemWithCondition") then
				local conditionDamage = 20 + InteractionRand(30, "Lockpick")
				self:ItemModifyCondition(item, -conditionDamage)
			end
			if not item.guaranteed_drop or IsKindOf(item, "QuestItem") then
				-- destroy some of the stack items
				if IsKindOf(item, "InventoryStack") then
					local oldAmount = item.Amount
					local percentRemoved = 20 + InteractionRand(30, "Lockpick")
					item.Amount = MulDivRound(item.Amount, percentRemoved, 100)
					item.Amount = Max(item.Amount, 1)
					
					destroyedAny = true
					CombatLog("debug", (oldAmount - item.Amount) .. " " .. item.class .. " were destroyed when opening box")
				end
			end
		end)
		ObjModified(self)
	end
	
	if destroyedAny then
		CombatLog("important", T(146944507889, "Some items were destroyed while attempting to open the box"))
	end
end

-- Handle destroying of item container visual objects dropping the loot on the ground.
function OnMsg.DamageDone(attacker, target, damage, hit_descr)
	if not target:IsDead() then return end -- Check if object died
	if not target:HasMember("spawner") or not IsKindOf(target.spawner, "ItemContainer") then return end -- Object is part of item container
	local spawner = target.spawner
	if not spawner:GetItemInSlot("Inventory") then return end -- Container has items in it
	if not spawner.enabled then return end
	
	-- All of the container's objects are dead (destroyed)
	local spawnerObjs = spawner.objects
	local allDead = true
	for i, o in ipairs(spawnerObjs) do
		if IsKindOf(o, "CombatObject") and not o:IsDead() then
			allDead = false
			break
		end
	end
	
	-- Drop guaranteed drop item, dump everything else.
	if allDead then
		local items = {}
		spawner:ForEachItemInSlot("Inventory", function(item, slot, left, top, items)
			if item.guaranteed_drop or IsKindOf(item, "QuestItem") then
				items[#items + 1] = item
			else
				CombatLog("debug", "Item " .. item.class .. " was destroyed when destroying box")
			end
		end, items)
		spawner:ClearSlot("Inventory")
		
		if #items > 0 then
			local container = GetDropContainer(spawner)
			for i, item in ipairs(items) do
				container:AddItem("Inventory", item)
			end
			local x, y, z = FindFallDownPos(container)
			if not x then return end
			CreateGameTimeThread(GravityFall, container, point(x, y, z))
		end
	end
end

-- ItemDropContainer
UndefineClass('ItemDropContainer')
DefineClass.ItemDropContainer = {
	DisplayName = T(131517457472, "Dropped Items"),
	__parents = { "ItemContainer", "SyncObject", "GameDynamicSpawnObject" },
	entity = "JungleCamp_Backpack_01",
	flags = { efCollision = false, efApplyToGrids = false },
	despawn_time = 0,
	despawn_thread = false,
	discovered = true,
	bOpened = true,
	__toluacode = empty_func, --fixes assert when trying to generate game record with invalid item drop containers
}

function ItemDropContainer:Done()
	DeleteThread(self.despawn_thread)
	self:UpdateInteractableBadge(false)
end

function ItemDropContainer:GetInteractionPos(unit)
	local positions = ItemContainer.GetInteractionPos(self, unit)
	if type(positions) == "table" then
		if unit and not table.find(positions, GetPassSlab(self)) then
			positions = ItemContainer.GetInteractionPos(self) -- return occupied positions too (backward compatibility)
		end
	end
	return positions
end

function ItemDropContainer:GetInteractionCombatAction(unit)
	-- Disable interaction when there is another unit on the container tile,
	-- because the unit on the tile could drop items without interacting with the container.
	-- Only one player could view/change the container at a time.
	-- We do it for both single and multiplayer for consistency, but it's required only to
	-- disable interaction when the other player controlled unit is on the tile.
	if not next(self.Inventory) then
		return false
	end
	if unit then
		local mypos = point_pack(SnapToVoxel(self:GetPosXYZ()))
		local upos = point_pack(SnapToVoxel(unit:GetPosXYZ()))
		if upos ~= mypos then
			local x, y = point_unpack(mypos)
			local tile_unit = MapGetFirst(x, y, const.SlabSizeX/2, "Unit", function(u, mypos)
				return not u:IsDead() and mypos == point_pack(SnapToVoxel(u:GetPosXYZ()))
			end, mypos)
			if tile_unit then
				return false
			end
		end
	end
	return ItemContainer.GetInteractionCombatAction(self, unit)
end

function ItemDropContainer:DespawnCheck()
	local despawn = not self.interacting_unit and not next(self.Inventory)
	if despawn == IsValidThread(self.despawn_thread) then
		return
	end
	if despawn then
		NetUpdateHash("DespawnCheck", self)
		self.despawn_thread = CreateGameTimeThread(function(self)
			Sleep(self.despawn_time)
			self.despawn_thread = nil
			DoneObject(self)
		end, self)
	else
		DeleteThread(self.despawn_thread)
		self.despawn_thread = false
	end
end

-- walks through all item containers in that sector
UndefineClass('SectorStash')
DefineClass.SectorStash = {
	__parents = { "Inventory" },
	inventory_slots = {
		{slot_name = "Inventory",  width = 7, height = 1, base_class = "InventoryItem", enabled = true },
	},
	sector_id = false,
	pickup_netsent = false,
	DisplayName = T(660371035462, "Sector stash"),
}

function SectorStash:ResetBinding()
	--the traditional inventory structure of this container is not sync ordered, therefore enum funcs with it will iterate in an async order;
	--however the "virtual" container data should be the same
	--so, rebuild async container before sync op
	local id = self.sector_id
	self:Clear()
	self:SetSectorId(id)
end

function SectorStash:GetSlotDataDim(slot_name)
	local slot_data = self:GetSlotData(slot_name)
	local width = slot_data.width
	local count = #self[slot_name] + 2 --self:CountItemsInSlot(slot_name)*2 -- pretend all are 2 tiles length
	local height = count/width + (count%width==0 and 0 or 1) + 1
	local height = Max(self:GetMaxTopPos(slot_name), height)
	height = Max(4, height)
	return width, height, width
end

function SectorStash:GetMaxTopPos(slot_name)
	local items = self[slot_name]
	if not next(items) then return 1 end
	local slot_data = self:GetSlotData(slot_name)
	local max = 0
	for i = #items, 1, -2 do
		local item, pos = items[i], items[i-1]
		local l,t = point_unpack(pos)
		max = Max(max, t)
	end
	return max
end

function SectorStash:Clear()
	local invSlot = self["Inventory"]
	if not IsKindOf(invSlot, "InventorySlot") then return end
	DoneObject(invSlot)
	invSlot = false
	self.sector_id = false
	self["Inventory"] = InventorySlot:new()
end

function SectorStash:GetVirtualContainerData()
	local sector = gv_Sectors and gv_Sectors[self.sector_id]
	local sector_inventory = sector and sector.sector_inventory
	local idx = table.find(sector_inventory, 1, "virtual")
	if idx then
		return sector_inventory[idx], sector_inventory, idx
	end
end

function SectorStash:AddDeadUnitsItems(filter)
	if not gv_Sectors or not self.sector_id then
		return
	end
	local units_list = gv_Sectors[self.sector_id].dead_units
	for _, session_id in ipairs(units_list) do
		local ud = gv_UnitData[session_id]
		if ud and ud:IsDead() then
			ud:ForEachItemInSlot("InventoryDead", function(item, slot, left, top, self)
				if not filter or filter(item) then
				Inventory.AddItem(self, "Inventory", item)
				end
			end, self)
		end
	end
end

function SectorStash:RemoveDeadUnitsItem(item)
	if not gv_Sectors or not self.sector_id then
		return
	end
	local found = false
	local itm, pos
	local units_list = gv_Sectors[self.sector_id].dead_units
	for _, session_id in ipairs(units_list) do
		local ud = gv_UnitData[session_id]
		if ud and ud:IsDead() then
			itm, pos = ud:RemoveItem("InventoryDead", item)	
			if itm then
				found = true
				break
			end
		end
	end
	return itm, pos
end

function SectorStash:AddVirtualContainer()
	if not gv_Sectors or not self.sector_id then
		return
	end
	local cdata, sector_inventory, idx = self:GetVirtualContainerData()
	if not cdata then
		cdata = { "virtual", true }
		local sector = gv_Sectors[self.sector_id]
		if not sector then
			sector = {}
			gv_Sectors[self.sector_id] = sector
		end
		sector.sector_inventory = sector.sector_inventory or {}
		sector_inventory = sector.sector_inventory 
		table.insert(sector.sector_inventory, cdata)
	end
	return cdata, #sector_inventory
end

function SectorStash:SetSectorId(sector_id, filter)
	local sector_id = sector_id or gv_CurrentSectorId	
	
	if self.sector_id == sector_id then
		return
	end
	
	self:Clear()
	
	self.sector_id = sector_id
	self:AddDeadUnitsItems(filter)
	local containers = gv_Sectors[sector_id].sector_inventory or empty_table
	self:AddVirtualContainer()
	for cidx, container in ipairs(containers) do
		if container[2] then -- opened
			local items = container[3] or empty_table
			for idx, item in sorted_pairs(items) do
				if not filter or filter(item) then
					Inventory.AddItem(self,"Inventory", item)
				end
			end
		end
	end
end

function SectorStash:AddItem(slot_name, item, left, top, local_execution, use_pos)
	-- add to virtual container	
	local cdata = self:GetVirtualContainerData()
	if not cdata then
		AddToSectorInventory(self.sector_id, item)
	end	

	if cdata then
		cdata[3] = cdata[3] or {}
		local val, idx = table.find_value(cdata[3], item)
		if val then
			cdata[3][idx]=item -- if something is changed
		else
			table.insert(cdata[3], item)
		end	
	end
	local x, y
	if left then
		x, y = left, top
	end
	return Inventory.AddItem(self,"Inventory", item, x, y)
end

function SectorStash:RemoveItem(slot_name, item, no_update)
	local _, pos = Inventory.RemoveItem(self, slot_name, item, no_update)
	-- remove from dead units
	local itm, pos = self:RemoveDeadUnitsItem(item)
	if itm then 
		return itm , pos
	end	
	--remove from container	

	local containers = gv_Sectors[self.sector_id].sector_inventory or empty_table
	local found = false
	for cidx, container in ipairs(containers) do
		local items = container[3] or empty_table
		for i = #items, 1, -1 do
			if items[i]==item then
				table.remove(items, i)
				if container[1]~= "virtual" then
					local obj = HandleToObject[container[1]]
					if IsKindOf(obj, "SectorInventoryObj") then 
						obj:SyncWithSectorInventory()
--[[				else -- debug
						for i, obj in sorted_pairs(HandleToObject) do
							if IsKindOf(obj, "SectorInventoryObj") then
								if obj:GetItemPos(item) then
									print("change container handle")
									gv_Sectors[self.sector_id].sector_inventory[cidx][1] = obj:GetHandle()
									obj:SyncWithSectorInventory()
								end
							end
						end
--]]						
					end
				end
				found = true
				break
			end
		end
		if found then
			break
		end	
	end
	return item, pos
end

function SectorStash:GetMaxTilesInSlot(slot_name)
	local width, height = self:GetSlotDataDim(slot_name)
	return width*height
end

