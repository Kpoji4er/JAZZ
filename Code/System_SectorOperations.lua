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