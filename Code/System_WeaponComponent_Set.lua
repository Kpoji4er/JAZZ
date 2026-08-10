-- JAZZ-ATTACH-001: MagazineSizeSet via ModificationType = "Set"
-- Vanilla FirearmBase:SetWeaponComponent only handles Add/Multiply/Subtract.
-- Engine formula: MulDivRound(base + mod_add, mod_mul, 1000).
-- Set must NOT use mul=0 (that always yields 0 → UI MagSize 1). Use mul=1000, add=N-base.

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
						-- Absolute overwrite: (base + (N - base)) * 1000/1000 = N.
						mul = 1000
						local base = self["base_" .. mod.StatToModify] or 0
						add = value - base
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

-- Old MagSizeSet used mul=0 → MagSize 0/1. Re-seat magazine comps so saves get N.
local function JazzFirearmHasBrokenMagSizeSet(weapon)
	for _, data in ipairs(weapon.applied_modifiers or empty_table) do
		if data.prop == "MagazineSize" and data.params and data.params[1] == 0 then
			return true
		end
	end
	return false
end

local function JazzFirearmUsesMagazineSizeSet(weapon)
	local mag_id = weapon.components and weapon.components.Magazine
	if not mag_id or mag_id == "" then
		return false
	end
	local def = WeaponComponents and WeaponComponents[mag_id]
	for _, modId in ipairs(def and def.ModificationEffects or empty_table) do
		local mod = WeaponComponentEffects and WeaponComponentEffects[modId]
		if mod and mod.ModificationType == "Set" and mod.StatToModify == "MagazineSize" then
			return true
		end
	end
	return false
end

local function JazzHealMagazineSizeSetOnFirearm(weapon)
	if not IsKindOf(weapon, "FirearmBase") then
		return
	end
	if not JazzFirearmUsesMagazineSizeSet(weapon) then
		return
	end
	local broken = JazzFirearmHasBrokenMagSizeSet(weapon)
	if not broken and (weapon.MagazineSize or 0) > 1 then
		return
	end
	local mag_id = weapon.components.Magazine
	weapon:SetWeaponComponent("Magazine", mag_id, "init")
	if broken and weapon.ammo and (weapon.ammo.Amount or 0) <= 1 and (weapon.MagazineSize or 0) > 1 then
		weapon.ammo.Amount = weapon.MagazineSize
	end
end

local function JazzHealMagazineSizeSetEverywhere()
	local function heal_container(container)
		if not container or not container.ForEachItem then
			return
		end
		container:ForEachItem("FirearmBase", function(item)
			JazzHealMagazineSizeSetOnFirearm(item)
		end)
	end
	if type(gv_UnitData) == "table" then
		for _, ud in sorted_pairs(gv_UnitData) do
			heal_container(ud)
		end
	end
	if type(gv_Squads) == "table" then
		for _, squad in sorted_pairs(gv_Squads) do
			local squad_id = squad and (squad.UniqueId or squad.squad_id)
			local bag = squad_id and GetSquadBagInventory and GetSquadBagInventory(squad_id)
			heal_container(bag)
		end
	end
	if type(g_Units) == "table" then
		for _, unit in sorted_pairs(g_Units) do
			heal_container(unit)
		end
	end
end

function OnMsg.LoadGame()
	JazzHealMagazineSizeSetEverywhere()
end

function OnMsg.NewGame()
	JazzHealMagazineSizeSetEverywhere()
end

