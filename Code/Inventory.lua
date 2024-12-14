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
	--print(canholdplate)



	

    --print(self.Inventory)
    --if slot_name ~= "InventoryDead" and (not self:GetItemInSlot("Torso") or not self:GetItemInSlot("Torso").CanHoldPlate) and self:GetItemInSlot("ArmorPlate")  then 
    --    local armorplate = self:GetItemInSlot("ArmorPlate")
    --    self:RemoveItem("ArmorPlate",armorplate)
    --    self:AddItem("Inventory",armorplate)
    --end
--
	--if slot_name ~= "InventoryDead" and (self:GetItemInSlot("Head") and not self:GetItemInSlot("Head").BlockFaceSlot) and self:GetItemInSlot("HeadGear")  then 
    --    local HeadGear = self:GetItemInSlot("HeadGear")
    --    self:RemoveItem("HeadGear",HeadGear)
    --    self:AddToInventory(HeadGear)
    --end


   -- if slot_name == "Torso" then return false, "full or smaller

	-- if not given left and top find empty space
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
		if is_current_stack and item.class == currentitem.class then 
			if (currentitem.Amount + item.Amount)>currentitem.MaxStacks then
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

  --  if slot_name ~= "InventoryDead" and (not self:GetItemInSlot("Torso") or canholdplate == false) and self:GetItemInSlot("ArmorPlate") then 
  --      local armorplate = self:GetItemInSlot("ArmorPlate")
--		--local slot = self:GetSlotData(slot_name)
--	--	local args = {item = armorplate, dest_container = self, dest_slot = "Inventory"}
--	--	local r, r2 = MoveItem(args)
--		
  --      self:RemoveItem("ArmorPlate",armorplate)
--		--PlaceInventoryItem(armorplate)
--		--AddItemsToInventory(self, armorplate)
--		self:AddItem("Inventory",armorplate)
--
  --  end

	return pos, reason
end



function InventoryItem:GetDeteriorationKeywordNoPrefix()
	if not self.Deterioration then 
		return "" 
	end
	
	local presets = Presets.ConstDef.Weapons
	local color --AP_Main_SmallRed
	local keyword = ""
	local conditionPercent = self.Deterioration
	
	if conditionPercent<=1 then
		color = "item_green"
		keyword =  T(486989771291111, "идеальное")
	elseif conditionPercent<=5 then
		color = "item_green"
		keyword =  T(2998106563741111, "отремонтированное")
	elseif conditionPercent<=20 then
		color = "yellow"
		keyword = T(5678579714391111, "изношенное")
	elseif conditionPercent<=50 then
		color = "red"
		keyword = T(939310080350111, "ржавое")
	else--if conditionPercent>=presets.ItemConditionBroken.name then
		color = "red"
		keyword =  T(968409848233111, "сломанное")
	end
	return T{997078176629, "<clr><keyword><closeclr>",clr = const.TagLookupTable[color],closeclr  = const.TagLookupTable["/"..color],  keyword = keyword}
end


function ScrapItem(inventory, slot_name, item, amount, squadBag, squadId)
	local is_stack = IsKindOf(item, "InventoryStack")
	if is_stack then
		amount = amount and Min(amount, item.Amount) or item.Amount
	end	
	amount = amount or 1
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