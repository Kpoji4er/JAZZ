function SectorOperationRepairItems_FillMostDamagedItems(sector_id)
	local all = table.icopy(gv_Sectors[sector_id].sector_repair_items)
	table.iappend(all, table.icopy(gv_Sectors[sector_id].sector_repair_items_queued))
	table.sortby(all,function(item) 
		local itm = SectorOperationRepairItems_GetItemFromData(item)
		return itm and itm.Condition or -1 
	end )	
	
	local width, idx = 0, 0
	local queued = {}
	local rem
    local rows = 1;
	while rows<3  and idx<#all do
		idx = idx+1
		local item = all[idx]
		local itm = SectorOperationRepairItems_GetItemFromData(item)
		local item_width = itm and itm:IsLargeItem() and 2 or 1
		width = width + item_width

		if width>=12 then
			rows = rows + 1
            width = 0
            idx = idx + 1
            rem = 12-(width - item_width)
		end

        if rows>3 then
			idx = idx-1			
			rem = 12-(width - item_width)
			break
		end
		queued[#queued+1] = item
	end	
		
	local tbl_all= {}	
	for i = idx+1, #all do
		local added = false
		if rem and rem>0 then
			local item = all[i]
			local itm = SectorOperationRepairItems_GetItemFromData(item)
			local item_width = itm and itm:IsLargeItem() and 2 or 1
			if item_width<=rem then
				queued[#queued+1] = item
				rem = rem - item_width
				added = true
			end
		end
		if not added then
			tbl_all[#tbl_all+1] = all[i]
		end
	end
	
	NetSyncEvent("ChangeSectorOperationItemsOrder",sector_id,"RepairItems", TableWithItemsToNet(tbl_all), TableWithItemsToNet(queued))
	return tbl_all, queued, idx
end

function XDragContextWindow:OnMouseButtonDoubleClick(pos, button)
	if button == "L" then
	--if not IsMouseViaGamepadActive() then
		local ctrl = self.drag_win
		if not ctrl then return "break" end	
		if not ctrl.idItem:GetEnabled() then return "break" end
		
		local operation_id = self.context[1].operation
		local dlg = GetDialog(self)
		local dlg_context = dlg and dlg.context
		local sector = dlg_context
		local sector_id = dlg_context.Id
		local is_repair = operation_id=="RepairItems"
		local search_id =  is_repair and "id" or "item_id"
		local serch_context = is_repair and ctrl.context.id or ctrl.context.class
		
		local queue, all = SectorOperationItems_GetTables(sector_id,operation_id )
		if self.Id=="idAllItems" then
			local item, idx = table.find_value(all, search_id, serch_context)
			local itm = item and SectorOperationRepairItems_GetItemFromData(item)

			local itm_width = itm and itm:IsLargeItem() and 2 or 1
			if SectorOperationItems_ItemsCount(queue) + itm_width <= 36 then
				if is_repair then 
					table.remove(all,idx)
				end	
				table.insert(queue,item)
			end	
		else
			local item, idx = table.find_value(queue, search_id, serch_context)
			table.remove(queue,idx)
			if is_repair then 
				table.insert(all,item)
			end	
		end
		self.drag_win:delete()
		self.drag_win = false
		self:StopDrag()
		SectorOperationValidateItemsToCraft(sector_id, operation_id)
		NetSyncEvent("SectorOperationItemsUpdateLists", sector_id,operation_id, TableWithItemsToNet(all), TableWithItemsToNet(queue))
		SectorOperation_ItemsUpdateItemLists(dlg:ResolveId("node"))
		return "break"		
---end
	end
end

function XDragContextWindow:OnDragDrop(target, drag_win, drop_res, pt)
	if not drag_win or drag_win == target then
		return 
	end
	target = target or self
	local self_slot = self.slot_name
	local target_slot = target.slot_name
	local target_wnd = target
	for i, wnd in ipairs(target) do
		if wnd:MouseInWindow(pt) then
			target_wnd =  wnd
			break
		end	
	end
	
	local operation_id = self.context[1].operation
	local is_repair = operation_id=="RepairItems"
	local dlg = GetDialog(self)or GetDialog(target_wnd)
	local dlg_context = dlg and dlg.context
	target_wnd = target_wnd or drag_win
	local context = drag_win.context
	local target_context = target_wnd:GetContext()
	local sector = dlg_context
	local sector_id = dlg_context.Id
	local self_queue, target_queue

	local a_all   = SectorOperationItems_GetAllItems(sector_id, operation_id)
	local a_queue = SectorOperationItems_GetItemsQueue(sector_id, operation_id)
	
	if self_slot=="ItemsQueue" then
		self_queue = a_queue
	elseif self_slot=="AllItems" then
		self_queue = a_all or {}
	end
	if target_slot=="ItemsQueue" then
		target_queue = a_queue
	elseif target_slot=="AllItems" then
		target_queue = a_all or {}
	end
	
	local cur_idx    = is_repair and table.find(self_queue,"id", context.id) or table.find(self_queue,"item_id", context.class)
	local target_idx = is_repair and table.find(target_queue, "id", target_context.id)	 or table.find(target_queue,"item_id", target_context.class)
	local itm        = self_queue[cur_idx]
	local item = itm and SectorOperationRepairItems_GetItemFromData(itm)
	local itm_width  = is_repair and (item and item:IsLargeItem() and 2 or 1) or 1
	
	if self_slot==target_slot then
		if cur_idx then
			if target_idx then
				target_queue[cur_idx], target_queue[target_idx] = target_queue[target_idx],target_queue[cur_idx]
			else	
				local itm = table.remove(self_queue,cur_idx)
				target_queue[#target_queue+1] = itm
			end	
		end
	elseif target_slot~="ItemsQueue" or (SectorOperationItems_ItemsCount(target_queue) + itm_width) <= 36 then 
		local itm
		if is_repair or self_slot=="ItemsQueue" then
			itm  = table.remove(self_queue,cur_idx)
		else
			itm = table.copy(self_queue[cur_idx])
		end
		if is_repair or target_slot=="ItemsQueue" then
			if not target_idx then
				target_queue[#target_queue+1] = itm
			else	
				table.insert(target_queue,target_idx,itm)
			end	
		end
	end
	local s_queue, s_all = SectorOperationItems_GetTables(sector_id, operation_id)
	local all    = target_slot=="AllItems" and target_queue  or self_slot=="AllItems" and self_queue or s_all
	local queued = target_slot=="ItemsQueue" and target_queue  or self_slot=="ItemsQueue" and self_queue or s_queue 
	
	drag_win:delete()
	SectorOperationValidateItemsToCraft(sector_id, operation_id)
	NetSyncEvent("SectorOperationItemsUpdateLists", sector_id,operation_id, TableWithItemsToNet(all), TableWithItemsToNet(queued))
	local mercs = GetOperationProfessionals(sector_id, operation_id)
	local eta = next(mercs) and GetOperationTimeLeft(mercs[1], operation_id) or 0
	local timeLeft = eta and Game.CampaignTime + eta
	AddTimelineEvent("activity-temp", timeLeft, "operation", { operationId = operation_id, sectorId = sector_id})
	
	self:RespawnContent()
	target:RespawnContent()
	local node = self:ResolveId("node")
	node:OnContextUpdate(node:GetContext())
	local node = target:ResolveId("node")
	node:OnContextUpdate(node:GetContext())
	ObjModified(target_queue)
	ObjModified(self_queue)
end

local priority_slots = {"Handheld A", "Handheld B", "Head", "Torso", "Legs", "HeadGear", "PocketInventory"}
function SectorOperationFillItemsToRepair(sector_id, mercs, check_only)
	-- priority of mercs whose item will be repaired:
	--[[
		1. My personal equipped Weapons
		2. My personal Armor items
		3. My squadmates equipped Weapons
		4. My squadmates equipped Armor items
		5. Weapons in the bag of any merc (starting form first bag on down)
		6. Armor items in merc bags
		7. Other squad on sector - weapons
		8. Other squad on sector - armor
		9. Sector stash - weapons
		10. Sector stash - armor
	--]]
	-- remove queued items
	local queue = gv_Sectors[sector_id].sector_repair_items_queued
	if not check_only  then
		gv_Sectors[sector_id].sector_repair_items  = {}
	end 
	--local all_to_repair = gv_Sectors[sector_id].sector_repair_items or {}
	local all_to_repair = {}
	local chek_only_var = {var_bool=false}
	--equipped weapons and armors 
	local act_mercs ={}
	for _, slot in ipairs(priority_slots) do
		for _,merc in ipairs(mercs) do
			act_mercs[merc.session_id] = true
			merc:ForEachItemInSlot(slot, "ItemWithCondition", function(item, slot_name, left, top, all_to_repair, chek_only_var)
				if item and not item:IsMaxCondition() and item.Repairable then
				   if check_only then
						chek_only_var.var_bool =  true
						return "break"
					end
					if not table.find(all_to_repair, "id", item.id) and not table.find(queue, "id", item.id) then
						table.insert(all_to_repair,{ unit = merc.session_id, id = item.id, slot = slot, pos_left = left, pos_top = top})
					end
				end
			end,all_to_repair,chek_only_var)	
		end
	end
	
	if chek_only_var.var_bool then
		return true
	end	

	local all_sector_mercs = GetPlayerSectorUnits(sector_id)	
	all_sector_mercs = table.ifilter(all_sector_mercs, function(idx,m) return m.Operation~="Traveling" and m.Operation~= "Arriving" end)
	--squadmates equipped weapons and armors 
	for _, slot in ipairs(priority_slots) do
		for _,merc in ipairs(mercs) do
			table.remove_value(all_sector_mercs, "session_id", merc.session_id)
			local squad = merc.Squad
			local units = gv_Squads[squad].units
			for _, unit_id in ipairs(units) do
				if not act_mercs[unit_id] then
					table.remove_value(all_sector_mercs, "session_id", unit_id)
					local unit = gv_UnitData[unit_id]
					unit:ForEachItemInSlot(slot, "ItemWithCondition", function(item, slot_name, left, top, all_to_repair, chek_only_var)
						if item and not item:IsMaxCondition() and item.Repairable then
							if check_only then
								chek_only_var.var_bool =  true
								return "break"
							end
							if not table.find(all_to_repair, "id", item.id) and not table.find(queue, "id", item.id) then
								table.insert(all_to_repair,{ unit = unit_id,  id = item.id, slot = slot, pos_left = left, pos_top = top})
							end
						end
					end,all_to_repair,chek_only_var)
				end
			end
		end
	end
	
	if chek_only_var.var_bool then
		return true
	end	

	-- in inventory weapons than armors
	for _,merc in ipairs(mercs) do
		local squad = merc.Squad
		local units = gv_Squads[squad].units
		for _, unit_id in ipairs(units) do
			local unit = gv_UnitData[unit_id]
			local slot = GetContainerInventorySlotName(unit)
			unit:ForEachItemInSlot(slot, "ItemWithCondition", function(item, slot_name, left, top, all_to_repair, chek_only_var)
				if not item:IsMaxCondition() and item.Repairable and item:IsWeapon() then
					if check_only then 
						chek_only_var.var_bool =  true
						return "break" 
					end
					if not table.find(all_to_repair, "id", item.id) and not table.find(queue, "id", item.id) then
						table.insert(all_to_repair,{ unit = unit_id, id = item.id, slot = slot, pos_left = left, pos_top = top})
					end	
				end
			end, all_to_repair,chek_only_var)
		end
	end
	
	if chek_only_var.var_bool then
		return true
	end	
	
	for _,merc in ipairs(mercs) do
		local squad = merc.Squad
		local units = gv_Squads[squad].units
		for _, unit_id in ipairs(units) do
			local unit = gv_UnitData[unit_id]
			local slot = GetContainerInventorySlotName(unit)
			unit:ForEachItemInSlot(slot, "ItemWithCondition", function(item, slot_name, left, top,all_to_repair,chek_only_var)
				if not item:IsMaxCondition() and item.Repairable and not item:IsWeapon() then
					if check_only then 
						chek_only_var.var_bool =  true
						return "break" 
					end
					if not table.find(all_to_repair, "id", item.id) and not table.find(queue, "id", item.id)  then
						table.insert(all_to_repair,{ unit = unit_id, id = item.id, slot = slot, pos_left = left, pos_top = top})
					end
				end
			end,all_to_repair,chek_only_var)
		end
	end
	
	if chek_only_var.var_bool then
		return true
	end	
	
	-- mercs from other squads on sector equipped
	-- equipped
	for _, slot in ipairs(priority_slots) do
		for _,merc in ipairs(all_sector_mercs) do
			merc:ForEachItemInSlot(slot, "ItemWithCondition", function(item, slot_name, left, top, all_to_repair, chek_only_var)
				if item and not item:IsMaxCondition() and item.Repairable then
				   if check_only then
						chek_only_var.var_bool =  true
						return "break"
					end
					if not table.find(all_to_repair, "id", item.id) and not table.find(queue, "id", item.id) then
						table.insert(all_to_repair,{ unit = merc.session_id, id = item.id, slot = slot, pos_left = left, pos_top = top})
					end
				end
			end,all_to_repair,chek_only_var)	
		end
	end
	
	if chek_only_var.var_bool then
		return true
	end	
	
	-- other squads bags -  weapons
	for _,unit in ipairs(all_sector_mercs) do
		local slot = GetContainerInventorySlotName(unit)
		unit:ForEachItemInSlot(slot, "ItemWithCondition", function(item, slot_name, left, top,all_to_repair,chek_only_var)
			if not item:IsMaxCondition() and item.Repairable and item:IsWeapon() then
				if check_only then 
					chek_only_var.var_bool =  true
					return "break" 
				end
				if not table.find(all_to_repair, "id", item.id) and not table.find(queue, "id", item.id)  then
					table.insert(all_to_repair,{ unit = unit.session_id, id = item.id, slot = slot, pos_left = left, pos_top = top})
				end
			end
		end,all_to_repair,chek_only_var)
	end

	if chek_only_var.var_bool then
		return true
	end	
-- other squads bags -  armors
	for _,unit in ipairs(all_sector_mercs) do
		local slot = GetContainerInventorySlotName(unit)
		unit:ForEachItemInSlot(slot, "ItemWithCondition", function(item, slot_name, left, top,all_to_repair,chek_only_var)
			if not item:IsMaxCondition() and item.Repairable and not item:IsWeapon() then
				if check_only then 
					chek_only_var.var_bool =  true
					return "break" 
				end
				if not table.find(all_to_repair, "id", item.id) and not table.find(queue, "id", item.id)  then
					table.insert(all_to_repair,{ unit = unit.session_id, id = item.id, slot = slot, pos_left = left, pos_top = top})
				end
			end
		end,all_to_repair,chek_only_var)
	end

	if chek_only_var.var_bool then
		return true
	end	

	-- sector stash
	local stash = gv_Sectors[sector_id].sector_inventory or empty_table
	for cidx, container in ipairs(stash) do
		if container[2] then -- is opened
			local items = container[3] or empty_table
			for idx, item in ipairs(items) do			
				if not item:IsMaxCondition() and item.Repairable then
					if check_only then 
						chek_only_var.var_bool =  true
						break 
					end
					if not table.find(all_to_repair, "id", item.id) and not table.find(queue, "id", item.id)  then
						table.insert(all_to_repair,{ unit = "stash", id = item.id})
					end
				end	
			end
		end
	end

	if chek_only_var.var_bool then
		return true
	end
	
	if check_only then 
		return false
	end
	
	gv_Sectors[sector_id].sector_repair_items = all_to_repair
	return all_to_repair
end

function AreAllEquippedItemsRepaired(merc)
	for i = 1, #priority_slots do
		local item, left, top = merc:GetItemInSlot(priority_slots[i])
		if item and not item:IsMaxCondition() then
			return false
		end
	end
	
	return true
end




---
--- Calculates the number of parts required to repair the items in the queue for the specified sector and operation.
---
--- @param sector_id string The ID of the sector where the operation is taking place.
--- @param operation_id string The ID of the operation.
--- @return number The total number of parts required to repair the queued items.
function SectorOperation_ItemsCalcRes(sector_id, operation_id)
	local queued_items = SectorOperationItems_GetItemsQueue(sector_id, operation_id)
	local operation = SectorOperations[operation_id]
	local parts = 0	

	if operation_id=="RepairItems" then
		local free_repair = operation:ResolveValue("free_repair")
		local restore_condition_per_Part = operation:ResolveValue("restore_condition_per_Part")
		local parts_per_step = operation:ResolveValue("parts_per_step")
		for _, item_data in ipairs(queued_items) do
			local item = SectorOperationRepairItems_GetItemFromData(item_data)
			local cur_cond = item and (item:GetCurrentResource() or item.Condition) or 0
			local repairability = item.Repairability or item.Reliability or 100
			local loss = MulDivRound(repaired, (100 - repairability) * (100 - sum_stat/4), 100 * 100)
			local max_condition = item and (item:GetMaxResource() or item:GetMaxCondition()) or 0
			max_condition = max_condition - loss;
			local to_repair = max_condition - cur_cond

			--use parts
			if to_repair > 0 then
				if to_repair <= free_repair then
				else
					local border = 0
					while border<max_condition do
						local diff = restore_condition_per_Part
						border = border + diff	
						if cur_cond<border and cur_cond+diff>=border then
							parts = parts + parts_per_step
							cur_cond  = cur_cond + diff
							if max_condition - cur_cond<=free_repair then
								break
							end	
						end
					end
				end
			end
		end	
	end
	if IsCraftOperationId(operation_id) then
		for _, item_data in ipairs(queued_items) do
			local item = CraftOperationsRecipes[item_data.recipe]
			for __,ing in ipairs(item.Ingredients) do
				if ing.item == "Parts" then
					parts = parts + ing.amount
				end
			end
		end	
	end
	return parts
end