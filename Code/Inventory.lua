--function Inventory:CanHoldPlate()
--	local armorvest = self:GetItemInSlot("Torso")
--	local canholdplate = false
--	if armorvest then canholdplate = armorvest.CanHoldPlate end
--	print(armorvest)
--	return canholdplate
--end



function Inventory:CanAddItem(slot_name, item, left, top, local_changes)
	local pos,reason

	if not self:CheckClass(item, slot_name) then
		return false, "different class"		
	end	



	local armorvest = self:GetItemInSlot("Torso")
	local canholdplate = false
	if armorvest then canholdplate = self:GetItemInSlot("Torso").CanHoldPlate end

	local headitem = self:GetItemInSlot("Head")
	local blockfaceslot = false
	if headitem then blockfaceslot = self:GetItemInSlot("Head").BlockFaceSlot end

	if slot_name == "ArmorPlate" and not self:GetItemInSlot("Torso") then return false, "No torso item" end
	if slot_name == "ArmorPlate" and self:GetItemInSlot("Torso") and not canholdplate then return false, "Torse item bloks armor plates" end
	if slot_name == "HeadGear" and blockfaceslot then return false, "Head item blocks headgear slot" end

	reason = ""
	local stack = false
	if left and top then 
		-- check stack items
		local currentitem = self:GetItemInSlot(slot_name,false, left, top)
		if currentitem == item then
			if item:IsLargeItem() then
				--could be the other slot and it could be out of bounds
				if not self:IsEmptyPosition(slot_name, item, left, top, nil, local_changes) then
					return false, "full or smaller position"
				end
			end
			return point_pack(left, top), "current"
		end
		local is_current_stack = IsKindOf(currentitem, "InventoryStack")
		local same_stack = JazzInventoryItemsCanStack and JazzInventoryItemsCanStack(item, currentitem)
			or (not JazzInventoryItemsCanStack and item.class == currentitem.class)
		if is_current_stack and same_stack then
			local max = JazzGetStackMax and JazzGetStackMax(currentitem, self) or currentitem.MaxStacks
			if JazzApplyStackContext then
				JazzApplyStackContext(currentitem, self)
			end
			if (currentitem.Amount + item.Amount) > max then
				return false, "full stack"
			else
				reason = "stack items"
				stack = true
			end
		end
		-- chek if this pos in space is empty and big enough for the item
		if not stack and not self:IsEmptyPosition(slot_name, item, left, top, nil, local_changes) then
			return false, "full or smaller position"
		end
	else 
		left, top = self:FindEmptyPosition(slot_name, item, local_changes)
		if not left or not top then 
			return false, "inventory full"
		end
	end
	pos = point_pack(left, top)


	return pos, reason
end



function InventoryItem:GetDeteriorationKeywordNoPrefix()
	local color
	local keyword = ""

	-- Огнестрел
	if self.ArmorResource then
		local factory = self:GetFactoryResource() or 1000
		local max = self:GetMaxResource() or 1000
		if max <= 0 then max = 1 end
		local conditionPercent =( MulDivRound(max, 100, factory)) or 100
		if conditionPercent >= 80 then
			color = "item_green"
			keyword = T(4869897712911115, "")
		elseif conditionPercent >= 60 then
			color = "item_green"
			keyword = T(890000000001400, "заштопан")
		elseif  conditionPercent >= 40 then
			color = "yellow"
			keyword = T(890000000001405, "дырявое")
		elseif conditionPercent >= 15 then
			color = "red"
			keyword = T(890000000001397, "рваное")
		else
			color = "red"
			keyword = T(890000000001398, "порвано")
		end

	elseif self.WeaponResource then
		local factory = self:GetFactoryResource() or 1000
		local max = self:GetMaxResource() or 1000
		if max <= 0 then max = 1 end
		local conditionPercent =( MulDivRound(max, 100, factory)) or 100

		if conditionPercent >= 80 then
			color = "item_green"
			keyword = T(486989771291111, "")
		elseif conditionPercent >= 60 then
			color = "item_green"
			keyword = T(2998106563741111, "отремонт")
		elseif conditionPercent >= 40 then
			color = "yellow"
			keyword = T(5678579714391111, "изношенное")
		elseif conditionPercent >= 15 then
			color = "red"
			keyword = T(939310080350111, "ржавое")
		else
			color = "red"
			keyword = T(968409848233111, "сломанное")
		end
	end

	return T{
		997078176629,
		"<clr><keyword><closeclr>",
		clr = const.TagLookupTable[color],
		closeclr = const.TagLookupTable["/" .. color],
		keyword = keyword
	}
end


function InventoryItem:GetDeteriorationKeywordNoPrefixForInventory()

	
	local presets = Presets.ConstDef.Weapons
	local color = "item_green"
	local keyword = ""

	if self.ArmorResource then
		local factory = self:GetFactoryResource() or 1000
		local max = self:GetMaxResource() or 1000
		if max <= 0 then max = 1 end
		local conditionPercent =( MulDivRound(max, 100, factory)) or 100
		if conditionPercent >= 80 then
			color = "item_green"
			keyword = T(4869897712911115, "")
		elseif conditionPercent >= 60 then
			color = "item_green"
			keyword = T(890000000001400, "заштопан")
		elseif  conditionPercent >= 40 then
			color = "yellow"
			keyword = T(890000000001405, "дырявое")
		elseif conditionPercent >= 15 then
			color = "red"
			keyword = T(890000000001397, "рваное")
		else
			color = "red"
			keyword = T(890000000001398, "порвано")
		end

	elseif self.WeaponResource then
		local factory = self:GetFactoryResource() or 1000
		local max = self:GetMaxResource() or 1000
		if max <= 0 then max = 1 end
		local conditionPercent =( MulDivRound(max, 100, factory)) or 100

		if conditionPercent >= 80 then
			color = "item_green"
			keyword = T(486989771291111, "")
		elseif conditionPercent >= 60 then
			color = "item_green"
			keyword = T(2998106563741111, "отремонт")
		elseif conditionPercent >= 40 then
			color = "yellow"
			keyword = T(5678579714391111, "изношенное")
		elseif conditionPercent >= 15 then
			color = "red"
			keyword = T(939310080350111, "ржавое")
		else
			color = "red"
			keyword = T(968409848233111, "сломанное")
		end
	end
	
	
	return T{997078176629, "<clr><keyword><closeclr>",clr = const.TagLookupTable[color],closeclr  = const.TagLookupTable["/"..color],  keyword = keyword}
end


function InventoryItem:GetConditionText()
	return T{6862025595561, "<Deterioration> <percent(condPercent)>", Deterioration = self:GetDeteriorationKeywordNoPrefixForInventory(), condPercent = self.Condition}
end

function ScrapItem(inventory, slot_name, item, amount, squadBag, squadId)
	local is_stack = IsKindOf(item, "InventoryStack")
	if is_stack then
		amount = amount and Min(amount, item.Amount) or item.Amount
	end	
	amount = amount or 1
	-- JAZZ-WEAPONS-002: eject removable modules before scrapping the receiver.
	if IsKindOf(item, "FirearmBase") and JAZZ_EjectRemovableAttachmentsForScrap then
		local unit = IsKindOfClasses(inventory, "Unit", "UnitData") and inventory
		JAZZ_EjectRemovableAttachmentsForScrap(item, unit, squadBag)
	end
	local partsAmount = item:AmountOfScrapPartsFromItem() * amount
	local additional 
	if IsKindOf(item, "Firearm") then
		additional = item:GetSpecialScrapItems()
	end	
	
	if next(additional) then
		local units    = gv_Squads[squadId].units 
		local unit_id  = table.max(units,function(unit_id) return gv_UnitData[unit_id].Mechanical end)
		--print(unit_id)
		local max_mech   = gv_UnitData[unit_id].Mechanical/2
		local rnd_unit = gv_UnitData[units[1]]
		local rand = rnd_unit:Random(100)
		if rand<max_mech then
			local res_idx = 1 + rnd_unit:Random(#additional)
			local res = additional[res_idx]
			local res_item = PlaceInventoryItem(res.restype)
			if IsKindOf(res_item, "InventoryStack") then
				res_item.Amount = res.amount
			end
			local add_slot_name = GetContainerInventorySlotName(inventory)
			if add_slot_name=="Inventory" then
				AddItemsToInventory(inventory, {res_item})
			else
				inventory:AddItem(add_slot_name, res_item)
			end
		end
	end
	
	if item.ammo then
		UnloadWeapon(item, squadBag)
	end
	if partsAmount > 0 then
		local parts = PlaceInventoryItem("Parts")
		parts.Amount = partsAmount	
		squadBag:AddAndStackItem(parts)
	end
		
	if is_stack then
		item.Amount = Max(0, item.Amount - amount)
	end
	
	if not is_stack or item.Amount==0 then
		local removedItem, pos = inventory:RemoveItem(slot_name, item)
		DoneObject(removedItem)
	end
	
	if IsKindOf(inventory, "Unit") and slot_name == inventory.current_weapon and inventory:IsIdleCommand() then
		inventory:SetCommand("Idle")
	end
	
	ObjModified("inventory tabs")
	UpdateWeaponModificationPartsCounter()
end


--function SortItemsArray(items)
--	-- stack items
--	for i = 1, #items do
--		if IsKindOf(items[i], "InventoryStack") then
--			for j = i+1, #items do
--				if items[i].class == items[j].class then
--					local transferAmount = Min(items[i].MaxStacks - items[i].Amount, items[j].Amount)
--					items[i].Amount = items[i].Amount + transferAmount
--					items[j].Amount = items[j].Amount - transferAmount
--				end
--			end
--		end
--	end
--	
--	-- remove empty stacks
--	for i = #items, 1, -1 do
--		if items[i].Amount and items[i].Amount <= 0 then
--			local item = table.remove(items, i)
--			DoneObject(item)
--		end
--	end
--	
--	-- sort
--
--
--	for i = 1, #items do
--		if items[i].Deterioration and items[i+1].Deterioration then
--			for j = i+1, #items do
--				if items[i].Deterioration <= items[j].Deterioration then
--						local buf = items[i]
--						items[i] = items[j]
--						items[j] = buf
--				end
--			end
--		end
--	end
--
--	table.sortby_field(items, "class")
--	
--	return items
--end