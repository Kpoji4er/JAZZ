-- Flag for NamedPerks craft wrap: Parts discounts for Static/Barry/Cord are inlined
-- in SectorOperation_ItemsCalcRes below (this file loads after System_NamedPerks.lua).
-- rawset: safe on ModsReloaded / DAP reload (no "new global" assert).
g_JAZZ_SectorOpsCraftDiscountInlined = rawget(_G, "g_JAZZ_SectorOpsCraftDiscountInlined") or false
g_JAZZ_TakeItemFromMercsBase = rawget(_G, "g_JAZZ_TakeItemFromMercsBase") or false
g_JAZZ_TakeItemFromMercsFn = rawget(_G, "g_JAZZ_TakeItemFromMercsFn") or false
g_JAZZ_CalcCraftResourcesBase = rawget(_G, "g_JAZZ_CalcCraftResourcesBase") or false
g_JAZZ_CalcCraftResourcesFn = rawget(_G, "g_JAZZ_CalcCraftResourcesFn") or false
g_JAZZ_ValidateRecipeIngBase = rawget(_G, "g_JAZZ_ValidateRecipeIngBase") or false
g_JAZZ_ValidateRecipeIngFn = rawget(_G, "g_JAZZ_ValidateRecipeIngFn") or false
rawset(_G, "g_JAZZ_SectorOpsCraftDiscountInlined", true)

--- Keep DesignerExplosives craft_discount / Description in sync (saves + stale CE defs).
local function Jazz_SectorOpsEnsureBarryCraftParam()
	local def = CharacterEffectDefs and CharacterEffectDefs.DesignerExplosives
	if not def then
		return
	end
	local cls = g_Classes and g_Classes.DesignerExplosives
	if cls then
		if cls.DisplayName then
			def.DisplayName = cls.DisplayName
		end
		if cls.Description then
			def.Description = cls.Description
		end
	end
	if type(rawget(_G, "g_PresetParamCache")) ~= "table" then
		return
	end
	local cache = g_PresetParamCache[def]
	if not cache then
		cache = {}
		g_PresetParamCache[def] = cache
	end
	if cache.craft_discount == nil then
		cache.craft_discount = 30
	end
	if cache.hoursToProduce == nil then
		cache.hoursToProduce = 168
	end
	if cache.amountToProduce == nil then
		cache.amountToProduce = 2
	end
end

Jazz_SectorOpsEnsureBarryCraftParam()

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
		local free_repair = operation:ResolveValue("free_repair") or 0
		local restore_condition_per_Part = operation:ResolveValue("restore_condition_per_Part")
		local parts_per_step = operation:ResolveValue("parts_per_step")
		for _, item_data in ipairs(queued_items) do
			local item = SectorOperationRepairItems_GetItemFromData(item_data)
			-- JAZZ-WEAPONS-002: Parts tick uses Condition % (0..100), not absolute
			-- WeaponResource/ArmorResource units. Absolute scale + removed *3 hack
			-- produced hundreds of Parts per rifle (e.g. 49% of WR≈8000 → ~825).
			restore_condition_per_Part = operation:ResolveValue("restore_condition_per_Part")
			local cur_cond, max_condition
			if item and (item.WeaponResource or item.ArmorResource) then
				local max_res = item:GetMaxResource() or item:GetFactoryResource() or 1
				if max_res <= 0 then
					max_res = 1
				end
				local cur_res = item:GetCurrentResource() or 0
				if item.GetConditionPercent then
					cur_cond = item:GetConditionPercent()
				else
					cur_cond = Clamp(MulDivRound(cur_res, 100, max_res), 0, 100)
				end
				max_condition = 100
			else
				cur_cond = item and (item.Condition or 0) or 0
				max_condition = item and (item:GetMaxCondition() or 100) or 0
			end
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

	-- UNITS-006 Parts discounts must live here: NamedPerks wrap of this global is
	-- overwritten by this file (metadata load order: NamedPerks → SectorOperations).
	if parts > 0 and type(GetOperationProfessionals) == "function" then
		local mercs = GetOperationProfessionals(sector_id, operation_id) or empty_table
		local best = 0
		for _, merc in ipairs(mercs) do
			if type(Jazz_StaticPartsDiscountPercent) == "function" then
				best = Max(best, Jazz_StaticPartsDiscountPercent(merc) or 0)
			end
		end
		if best > 0 then
			parts = Max(0, MulDivRound(parts, 100 - best, 100))
		end
		if operation_id == "CraftAmmo" or operation_id == "CraftExplosives" then
			-- Barry DesignerExplosives: −30% Parts on ammo/grenade craft (queued total).
			if type(Jazz_ApplyBarryCraftPartsAmount) == "function" then
				parts = Jazz_ApplyBarryCraftPartsAmount(sector_id, operation_id, parts)
			end
		elseif operation_id == "RepairItems" or operation_id == "Repair" then
			for _, merc in ipairs(mercs) do
				if type(Jazz_CordInBarCity) == "function" and Jazz_CordInBarCity(merc) then
					local disc = (type(Jazz_NamedPerkParam) == "function"
						and Jazz_NamedPerkParam(merc, "Jazz_Perk_Cord", "repair_parts_discount", 10))
						or 10
					parts = Max(0, MulDivRound(parts, 100 - disc, 100))
					break
				end
			end
		end
	end
	return parts
end

function GetHealingBonus(sector, operation_id)
	local bonus = 0
	local doctors = GetOperationProfessionals(sector.Id, operation_id, "Doctor")
	if #doctors>0 then
		bonus = 100
		local forgiving_mode = IsGameRuleActive("ForgivingMode")
		local min_stat_boost = GameRuleDefs.ForgivingMode:ResolveValue("MinStatBoost") or 0
		for _, unit in ipairs(doctors) do
			local stat = unit.Medical
			if HasPerk(unit, "Jazz_Perk_Spider") then stat = stat * 2 end
			if forgiving_mode and stat < min_stat_boost then
				stat = stat + (min_stat_boost-stat)/2
			end
			bonus = bonus + stat * 2
		end
	end
	return bonus
end

-- Large stacked squads (Jazz MercSquadMaxPeople=12 + multi-squad sectors) blow up
-- SectorOperationsAssignDlgUI: merc grid uses float / rows, no scroll, ActionBar
-- slides off-screen. Parent MainUI "Start" stays disabled while Assign is open, so
-- the player only sees a grey Start — Enter still confirms and charges money.
local function JazzAssignDlgId(dlg)
	return dlg and (dlg.Id or dlg.xtemplate or rawget(dlg, "xtemplate"))
end

local function JazzIsSectorOperationsAssignDlg(dlg)
	if not dlg then
		return false
	end
	local open = GetDialog("SectorOperationsAssignDlgUI")
	if open and open == dlg then
		return true
	end
	local id = JazzAssignDlgId(dlg)
	return id == "SectorOperationsAssignDlgUI" or id == "SectorOperationsAssignDlgUI_1"
end

function JazzFixSectorOperationsAssignDlgLayout(dlg)
	if not dlg or rawget(dlg, "jazz_assign_layout_fixed") then
		return
	end
	rawset(dlg, "jazz_assign_layout_fixed", true)

	local list = dlg.idMercsList or dlg:ResolveId("idMercsList")
	local bar = dlg.idActionBar or dlg:ResolveId("idActionBar")
	local screen = UIL and UIL.GetScreenSize and UIL.GetScreenSize()
	local max_h = 360
	if screen then
		max_h = Min(420, Max(220, MulDivRound(screen:y(), 42, 100)))
	end

	-- Clamp portrait grid so the assign card cannot push Confirm below the screen.
	-- Top rows stay selectable (Idle list is skill-sorted); full scroll is a follow-up.
	if list then
		list:SetMaxHeight(max_h)
		list:SetClip("self")
	end

	-- Keep Confirm/Close on the visible dialog frame, not under an oversized card.
	if bar and bar.parent ~= dlg then
		bar:SetParent(dlg)
		bar:SetDock(false)
		bar:SetHAlign("center")
		bar:SetVAlign("bottom")
		bar:SetZOrder(50)
		bar:SetMargins(box(20, 0, 20, 28))
		bar:SetDrawOnTop(true)
	end
end

local function JazzPatchAssignDlgMercGrid()
	local xt = rawget(_G, "XTemplates") and XTemplates.SectorOperationsAssignDlgUI
	if not xt then
		return
	end

	local function patch_foreach_run_after(foreach_node)
		if type(foreach_node) ~= "table" or type(foreach_node.run_after) ~= "function" then
			return false
		end
		if rawget(foreach_node, "jazz_assign_grid_int") then
			return true
		end
		local base = foreach_node.run_after
		foreach_node.run_after = function(child, context, item, i, n, last)
			base(child, context, item, i, n, last)
			local total = tonumber(last) or 0
			local idx = tonumber(i) or 0
			local dev = 10
			if total > 10 and (total % 10) < 3 then
				dev = math.floor(total / 2) + (total % 2)
			end
			if dev < 1 then
				dev = 1
			end
			local col = idx % dev
			if col == 0 then
				col = dev
			end
			local row = math.floor((idx + dev - 1) / dev)
			child:SetGridY(row)
			child:SetGridX(col)
		end
		rawset(foreach_node, "jazz_assign_grid_int", true)
		return true
	end

	local function walk(node, depth)
		if type(node) ~= "table" or (depth or 0) > 80 then
			return false
		end
		if node.Id == "idMercsList" then
			for _, child in ipairs(node) do
				-- XTemplateForEach carrying assign portrait grid run_after
				if type(child) == "table" and patch_foreach_run_after(child) then
					return true
				end
			end
		end
		for _, child in ipairs(node) do
			if type(child) == "table" and walk(child, (depth or 0) + 1) then
				return true
			end
		end
		for key, child in pairs(node) do
			if type(key) ~= "number" and type(child) == "table" and walk(child, (depth or 0) + 1) then
				return true
			end
		end
		return false
	end

	walk(xt, 0)
end

local function JazzPatchMainUIHideStartWhileAssignOpen()
	local xt = rawget(_G, "XTemplates") and XTemplates.SectorOperationMainUI
	if not xt then
		return
	end

	local function wrap_action(node)
		if rawget(node, "jazz_hide_start_while_assign") then
			return
		end
		if node.ActionId ~= "Start" or type(node.ActionState) ~= "function" then
			return
		end
		local base = node.ActionState
		node.ActionState = function(self, host)
			if GetDialog("SectorOperationsAssignDlgUI") then
				return "hidden"
			end
			return base(self, host)
		end
		rawset(node, "jazz_hide_start_while_assign", true)
	end

	local function walk(node, depth)
		if type(node) ~= "table" or (depth or 0) > 80 then
			return
		end
		wrap_action(node)
		for _, child in ipairs(node) do
			if type(child) == "table" then
				walk(child, (depth or 0) + 1)
			end
		end
		for key, child in pairs(node) do
			if type(key) ~= "number" and type(child) == "table" then
				walk(child, (depth or 0) + 1)
			end
		end
	end

	walk(xt, 0)
end

function JazzInstallSectorOperationsAssignUIFixes()
	JazzPatchAssignDlgMercGrid()
	JazzPatchMainUIHideStartWhileAssignOpen()
	JazzPatchCraftRecipeRolloverIngredients()
	JazzInstallBarryCraftConsumeWraps()
end

local function Jazz_CraftOpFromMercs(mercs)
	local uid = mercs and mercs[1]
	if not uid then
		return nil, nil
	end
	local unit = gv_UnitData and gv_UnitData[uid]
	if not unit then
		return nil, nil
	end
	local op = unit.Operation
	local sector_id
	if unit.GetSector then
		local sector = unit:GetSector()
		sector_id = sector and sector.Id
	end
	if not sector_id and unit.Squad and gv_Squads and gv_Squads[unit.Squad] then
		sector_id = gv_Squads[unit.Squad].CurrentSector
	end
	return sector_id, op
end

function JazzInstallBarryCraftConsumeWraps()
	local take = rawget(_G, "TakeItemFromMercs")
	if type(take) == "function" then
		local wrapped = rawget(_G, "g_JAZZ_TakeItemFromMercsFn")
		if not (wrapped and take == wrapped) then
			rawset(_G, "g_JAZZ_TakeItemFromMercsBase", take)
			local function wrap(mercs, item_id, count, ...)
				if item_id == "Parts" and type(count) == "number" and count > 0 then
					local sector_id, op = Jazz_CraftOpFromMercs(mercs)
					if (op == "CraftAmmo" or op == "CraftExplosives")
						and sector_id and type(Jazz_ApplyBarryCraftPartsAmount) == "function" then
						count = Jazz_ApplyBarryCraftPartsAmount(sector_id, op, count)
					end
				end
				return g_JAZZ_TakeItemFromMercsBase(mercs, item_id, count, ...)
			end
			rawset(_G, "TakeItemFromMercs", wrap)
			rawset(_G, "g_JAZZ_TakeItemFromMercsFn", wrap)
		end
	end

	local calc = rawget(_G, "SectorOperation_CalcCraftResources")
	if type(calc) == "function" then
		local wrapped = rawget(_G, "g_JAZZ_CalcCraftResourcesFn")
		if not (wrapped and calc == wrapped) then
			rawset(_G, "g_JAZZ_CalcCraftResourcesBase", calc)
			local function wrap(sector_id, operation_id)
				local res = g_JAZZ_CalcCraftResourcesBase(sector_id, operation_id)
				if type(res) == "table" and res.Parts and type(Jazz_ApplyBarryCraftPartsAmount) == "function" then
					res.Parts = Jazz_ApplyBarryCraftPartsAmount(sector_id, operation_id, res.Parts)
				end
				return res
			end
			rawset(_G, "SectorOperation_CalcCraftResources", wrap)
			rawset(_G, "g_JAZZ_CalcCraftResourcesFn", wrap)
		end
	end

	local validate = rawget(_G, "SectorOperation_ValidateRecipeIngredientsAmount")
	if type(validate) == "function" then
		local wrapped = rawget(_G, "g_JAZZ_ValidateRecipeIngFn")
		if not (wrapped and validate == wrapped) then
			rawset(_G, "g_JAZZ_ValidateRecipeIngBase", validate)
			local function wrap(mercs, recipe, res_items, cache)
				local sector_id, op = Jazz_CraftOpFromMercs(mercs)
				if recipe and (op == "CraftAmmo" or op == "CraftExplosives")
					and type(Jazz_CraftRecipeIngredients) == "function" then
					recipe = { Ingredients = Jazz_CraftRecipeIngredients(recipe, sector_id, op) }
				end
				return g_JAZZ_ValidateRecipeIngBase(mercs, recipe, res_items, cache)
			end
			rawset(_G, "SectorOperation_ValidateRecipeIngredientsAmount", wrap)
			rawset(_G, "g_JAZZ_ValidateRecipeIngFn", wrap)
		end
	end
end

function JazzPatchCraftRecipeRolloverIngredients()
	local xt = rawget(_G, "XTemplates") and XTemplates.RolloverOperationCraftRecipe
	if not xt then
		return
	end
	local function walk(node, depth)
		if type(node) ~= "table" or (depth or 0) > 40 then
			return false
		end
		if type(node.array) == "function" and type(node.run_after) == "function"
			and not rawget(node, "jazz_barry_craft_ings") then
			local base_array = node.array
			node.array = function(parent, context)
				local ings = base_array(parent, context)
				if type(Jazz_CraftRecipeIngredients) ~= "function" or not context then
					return ings
				end
				local control = context.control
				local dlg = control and GetDialog(control)
				if not dlg or not dlg.context then
					return ings
				end
				local sector_id = dlg.context.Id
				local host = dlg[1]
				local operation_id = host and host.context and host.context[1] and host.context[1].operation
				local recipe_id = control.item and control.item.recipe
				local recipe = recipe_id and CraftOperationsRecipes[recipe_id]
				return Jazz_CraftRecipeIngredients(recipe, sector_id, operation_id)
			end
			rawset(node, "jazz_barry_craft_ings", true)
			return true
		end
		for _, child in ipairs(node) do
			if type(child) == "table" and walk(child, (depth or 0) + 1) then
				return true
			end
		end
		for key, child in pairs(node) do
			if type(key) ~= "number" and type(child) == "table" and walk(child, (depth or 0) + 1) then
				return true
			end
		end
		return false
	end
	walk(xt, 0)
end

function OnMsg.DialogOpen(dlg, init_mode)
	if JazzIsSectorOperationsAssignDlg(dlg) then
		JazzFixSectorOperationsAssignDlgLayout(dlg)
	end
end

function OnMsg.DataLoaded()
	rawset(_G, "g_JAZZ_SectorOpsCraftDiscountInlined", true)
	Jazz_SectorOpsEnsureBarryCraftParam()
	JazzInstallSectorOperationsAssignUIFixes()
end

function OnMsg.ModsReloaded()
	rawset(_G, "g_JAZZ_SectorOpsCraftDiscountInlined", true)
	Jazz_SectorOpsEnsureBarryCraftParam()
	JazzInstallSectorOperationsAssignUIFixes()
end

JazzInstallSectorOperationsAssignUIFixes()
rawset(_G, "g_JAZZ_SectorOpsCraftDiscountInlined", true)
Jazz_SectorOpsEnsureBarryCraftParam()