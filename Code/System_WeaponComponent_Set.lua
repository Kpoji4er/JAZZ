-- JAZZ-ATTACH-001: MagazineSizeSet via ModificationType = "Set"
-- Vanilla FirearmBase:SetWeaponComponent only handles Add/Multiply/Subtract.
-- Set -> AddModifier(id, prop, mul=0, add=N): value = MulDivRound(base, 0, 1000) + N = N.

function FirearmBase:SetWeaponComponent(slot, id, is_init)
	local def = WeaponComponents[id]
	slot = slot or (def and def.Slot)
	
	if not slot then
		return
	end
	
	local function unload_weapon(weapon)
		local squadBag = gv_SquadBag
		if not squadBag or not squadBag.squad_id then
			local ud = gv_UnitData[self.owner]
			if not ud then return end
			squadBag = GetSquadBagInventory(ud.Squad)
			assert(squadBag)
			if not squadBag then return end
		end
		UnloadWeapon(weapon, squadBag)
		InventoryUIResetSquadBag()
	end
	
	local reload_ammo_type
	if not rawget(self, "is_clone") and self.ammo and not is_init then
		if slot == "Magazine" or (self.ammo and self.ammo.Amount > self.MagazineSize) then
			reload_ammo_type = self.ammo.class
			unload_weapon(self)
		end
	end

	-- unregister all reactions, change components, register reactions back
	self:UnregisterReactions()

	-- Remove old component
	if (self.components[slot] or "") ~= "" then
		local component = self.components[slot]
		self:RemoveModifiers(component)
		
		local componentPreset = WeaponComponents[component]
		for _, modId in ipairs(componentPreset and componentPreset.ModificationEffects) do
			local mod = WeaponComponentEffects[modId]
			
			if mod.CaliberChange then
				self:ChangeCaliber(self["base_Caliber"])
			end
		end

		if self.subweapons[slot] then
			local subWep = self.subweapons[slot]
			if not rawget(self, "is_clone") then
				unload_weapon(subWep)
			end

			-- Subweapons refer to the weapon object as their visual obj
			-- in order for FX to play from it. We need to strip this property
			-- before calling delete as it will destroy the whole weapon.
			if self.visual_obj == subWep.visual_obj then
				subWep.visual_obj = false
			end
			subWep:delete()
			self.subweapons[slot] = nil
		end
		
		if componentPreset then
			for i, v in ipairs(componentPreset.Visuals) do
				if v:Match(self.class) then
					local slotId = v.Slot
					local componentSlot = table.find_value(self.ComponentSlots, "SlotType", slotId)
					self.components[slotId] = componentSlot and componentSlot.DefaultComponent or ""
				end
			end
		end
	end

	self.components[slot] = id or ""
	self:RegisterReactions()
	self.visual_obj_dirty = true
	
	-- Attach new component if any
	if def then
		for _, modId in ipairs(def.ModificationEffects) do
			local mod = WeaponComponentEffects[modId]
			if mod.StatToModify then
				local firstParam = mod.Parameters
				firstParam = firstParam and firstParam[1]
				firstParam = firstParam and firstParam.Name
				if firstParam then
					local value = def:ResolveValue(firstParam) or mod:ResolveValue(firstParam)
					assert(value) -- Weapon modification needs a value.
					value = value or 0
					
					-- Scale the value if needed
					local scale = mod.Scale
					scale = scale and const.Scale[scale]
					if scale then value = value * scale end
	
					local add = 0
					local mul = 1000
					if mod.ModificationType == "Add" then
						add = value
					elseif mod.ModificationType == "Multiply" then
						mul = value * 10
					elseif mod.ModificationType == "Subtract" then
						add = -value
					elseif mod.ModificationType == "Set" then
						-- Absolute overwrite (MagazineSizeSet / absolute MagazineSize).
						mul = 0
						add = value
					end
					
					self:AddModifier(id, mod.StatToModify, mul, add)
				end
			end
			
			if mod.CaliberChange then
				self:ChangeCaliber(mod.CaliberChange)
			end
		end
		
		assert(not def.EnableWeapon or not is_init) -- Default component shouldnt have a subweapon
		if def.EnableWeapon and not is_init then
			local is_async = rawget(self, "is_clone") or not self.id
			if is_async then
				InventoryItem.DetachIdInitialization("SetWeaponComponent")
			end
			local item = PlaceInventoryItem(def.EnableWeapon)
			if is_async then
				InventoryItem.AttachIdInitialization("SetWeaponComponent")
			end
			item.parent_weapon = self
			self.subweapons[slot] = item
			item.visual_obj = self:GetVisualObj()
		end
		
		if def.BlockSlots then
			for i, s in ipairs(def.BlockSlots) do
				self:SetWeaponComponent(s, false)
			end
		end
	end
		
	self:UpdateVisualObj()
	
	if reload_ammo_type then
		local ud = gv_UnitData[self.owner]
		local owner = g_Units[ud.session_id] or ud
		ud:ReloadWeapon(self, reload_ammo_type)
	end
	
	ObjModified(self)
end

