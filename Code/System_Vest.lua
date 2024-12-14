-- base class handling the syncronization to sector inventory

DefineClass.Vest = {
	__parents = { "InventoryItem", --"SectorInventoryObj" 
	},
	flags = { efSelectable = true },
	properties = {
		{ id = "Slot", editor = "combo", default = "Vest", template = true, items = function (self) return {"Vest","Backpack"} end, },
		{ id = "width",    name = "Width",  editor = "number", default = 4, slider = true, min = 1, max = 6, },
		{ id = "height",    name = "Height", editor = "number", default = 1, slider = true, min = 1, max = 4, },
	},
	inventory_slots = {
		{ slot_name = "InventoryVest", width = 6, height = 3, base_class = "InventoryItem", enabled = true },
	},
	bOpened = false,
	interacting_unit = false,
}

DefineClass.InventoryVest = {
	__parents = { "Inventory", "PropertyObject" },	
	inventory_slots = {
		--{slot_name = "Inventory",  width = 4, height = 1, base_class = "InventoryItem", enabled = true },
	},
}	


function Vest:GetInventoryMaxSlots(slot_name)
	return 14
end

function InventoryVest:GetDist2D(obj) return obj:GetDist2D(obj) end


function Vest:GetMaxTilesInSlot(slot_name)
	if slot_name=="Inventory" then
		return self:GetInventoryMaxSlots()
	elseif slot_name=="InventoryDead" then
		local max_slots = 24
		local rem = max_slots % 4
		if rem > 0 then
			max_slots = max_slots + 4 - rem
		end
		
		return max_slots
	else
		return Inventory.GetMaxTilesInSlot(self,slot_name)
	end
end

function Vest:AddItem(slot_name, item, left, top, local_execution)
	local pos, reason = Inventory.AddItem(self, slot_name, item, left, top)
	if not pos then return pos, reason end
	
	item.owner = IsMerc(self.owner) and self.session_id or false -- Dont bloat save with non-merc owners.
	if not local_execution then
		Msg("ItemAdded", self, item, slot_name, pos)
	end
	item:OnAdd(self, slot_name, pos, item)

	return pos, reason
end

-- add already generated items (from loot table) into inventory, stack them if can
--function AddItemsToInventory(inventoryObj, items, bLog)
--	local pos, reason
--	for i = #items, 1, -1 do
--		local item =  items[i]
--		if IsKindOf(item, "InventoryStack") then
--			inventoryObj:ForEachItemDef(item.class, 
--				function(curitm, slot_name, item_left, item_top)
--					if slot_name~="Inventory" then return end
--					
--				   if curitm.Amount < curitm.MaxStacks then
--						local to_add = Min(curitm.MaxStacks - curitm.Amount, item.Amount)
--						curitm.Amount =curitm.Amount + to_add
--						curitm.drop_chance = Max(curitm.drop_chance, item.drop_chance)
--						if bLog then
--							Msg("InventoryAddItem", inventoryObj, curitm, to_add)
--						end
--						item.Amount =  item.Amount - to_add			
--						if item.Amount <= 0 then
--							DoneObject(item)
--							item = false
--							table.remove(items, i)
--							return "break"
--						end
--					end
--				end)
--		end
--		if item then 
--			pos, reason = inventoryObj:AddItem("Inventory", item)
--			if pos then
--				if bLog then
--					Msg("InventoryAddItem", inventoryObj, item, IsKindOf(item, "InventoryStack") and item.Amount or 1)
--				end
--				table.remove(items, i)
--			end
--		else
--			pos = true
--		end				
--	end
--	ObjModified(inventoryObj)
--	return pos, reason
--end

--function Vest:AddItemsToInventory(items)
--	return AddItemsToInventory(self, items, true)
--end
--
--function InventoryItem:OnAdd(u, slot, pos, item)
--	if IsKindOf(u, "UnitBase") and slot ~= "SetpieceWeapon" then
--		self:RegisterReactions(u)
--		self:OnItemGained(u, slot)
--	end
--	if IsKindOf(u.owner, "UnitBase") and slot ~= "SetpieceWeapon" then
--		self:RegisterReactions(u.owner)
--		self:OnItemGained(u.owner, slot)
--	end
--end
--
--function InventoryItem:OnRemove(u, slot) 
--	if IsKindOf(u, "UnitBase") and slot ~= "SetpieceWeapon" then
--		self:UnregisterReactions(u)
--		self:OnItemLost(u, slot)
--	if IsKindOf(u.owner, "UnitBase") and slot ~= "SetpieceWeapon" then
--		self:UnregisterReactions(u.owner)
--		self:OnItemLost(u.owner, slot)
--	end	
--	end
--end