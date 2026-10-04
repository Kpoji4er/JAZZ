-- JAZZ-ATTACH-001: MagazineSizeSet via ModificationType = "Set"
-- Vanilla FirearmBase:SetWeaponComponent only handles Add/Multiply/Subtract.
-- Engine formula: MulDivRound(base + mod_add, mod_mul, 1000).
-- Set must NOT use mul=0 (that always yields 0 → UI MagSize 1). Use mul=1000, add=N-base.

-- Approved model QA: these parts no longer have interchangeable geometry.
local JazzModelFixedComponents = {
	M14SAW = { Barrel = "JAZZ_BarrelNormal" },
	M21 = { Barrel = "JAZZ_BarrelNormal" },
	MK14EBR = { Barrel = "JAZZ_BarrelNormal" },
	JAZZ_M14_MkIII = { Barrel = "JAZZ_BarrelNormal" },
	M16A4 = { Handgrip = "JAZZ_Handgrip_Default", Stock = "JAZZ_StockNormal" },
	M4A1 = { Handgrip = "JAZZ_Handgrip_Default" },
}

-- JAZZ-WEAPON-RAIL-001: paid dovetail / rail / conversion gates.
-- One FirearmBase:SetWeaponComponent. Callers in the modify dialog use JAZZ_RailReject.

local JAZZ_EASTERN_OPTIC = {
	JAZZ_Scope_PSO = true,
	JAZZ_Reflex_Cobra = true,
	JAZZ_Reflex_PKAS = true,
	JAZZ_CombatScope_1P29 = true,
	JAZZ_NightScope_NSPU = true,
}

local JAZZ_IRON_OPTIC = {
	JAZZ_CarryHandle_AR15 = true,
	JAZZ_G36Sight = true,
	JAZZ_AUGScope_Default = true,
	JAZZ_DefaultIronsight_AR15 = true,
	JAZZ_BaseIronsight_Anaconda = true,
}

local JAZZ_FAL_TAC = "JAZZ_FNFAL_TacHandguard"
local JAZZ_FAL_LONG = { JAZZ_BarrelLong = true, JAZZ_BarrelLongImproved = true }
local JAZZ_FAL_FOLD = { JAZZ_StockLightUnFolded = true, JAZZ_StockLightFolded = true }

local function jazz_is_iron(id)
	if not id or id == "" then
		return true
	end
	if JAZZ_IRON_OPTIC[id] then
		return true
	end
	return string.find(id, "IronSight", 1, true) or string.find(id, "Ironsight", 1, true)
end

local function jazz_is_grip(id)
	if not id or id == "" then
		return false
	end
	return string.find(id, "VerticalGrip", 1, true) or string.find(id, "TacGrip", 1, true)
end

local function jazz_part(id)
	if not id or id == "" then
		return ""
	end
	return id
end

JAZZ_RailRules = {
	AKM = { dove = "JAZZ_Dovetail_AK", nato = "JAZZ_Rail_NATO_AK", scope = "split" },
	AK74 = { dove = "JAZZ_Dovetail_AK", scope = "east" },
	AK74M = { nato = "JAZZ_Rail_NATO_AK", factory = true, scope = "split" },
	AK105 = { nato = "JAZZ_Rail_NATO_AK", factory = true, scope = "split" },
	AEK971 = { dove = "JAZZ_Dovetail_AK", nato = "JAZZ_Rail_NATO_AK", scope = "west" },
	AKSU = { dove = "JAZZ_Dovetail_AKSU", side = "dove" },
	DragunovSVD = { dove = "JAZZ_Dovetail_SVD", nato = "JAZZ_Rail_NATO_SVD", scope = "split" },
	AS_Val = { dove = "JAZZ_Dovetail_Val", nato = "JAZZ_Rail_NATO_Val", scope = "split", side = "nato" },
	VSS = { dove = "JAZZ_Dovetail_Val", nato = "JAZZ_Rail_NATO_Val", scope = "split" },
	PP19Bizon = { dove = "JAZZ_Dovetail_AK", scope = "east" },
	AR10 = { rail = "JAZZ_Rail_AR", scope = "rail" },
	CAR15 = { rail = "JAZZ_Rail_AR", scope = "rail" },
	M16A1 = { rail = "JAZZ_Rail_AR", scope = "rail" },
	M16A2 = { rail = "JAZZ_Rail_M16A2", rail2 = "JAZZ_Rail_M16A2_Side", scope = "rail", side = "rail2" },
	AUG = { rail = "JAZZ_Rail_AUG", rail2 = "JAZZ_Rail_AUG_Side", scope = "rail", side = "rail2" },
	FAMAS = { rail = "JAZZ_Rail_FAMAS", side = "rail" },
	FNFAL = { rail = "JAZZ_Rail_FAL", scope = "rail", side = "rail", grips = "rail", handguard_satisfies = JAZZ_FAL_TAC },
	G3A3 = { rail = "JAZZ_Rail_G3", scope = "rail" },
	G3A4 = { rail = "JAZZ_Rail_G3", scope = "rail" },
	G3SniperV1 = { rail = "JAZZ_Rail_G3", scope = "rail" },
	G36 = { rail = "JAZZ_Rail_G36", scope = "rail", side = "rail", grips = "rail" },
	HK21 = { rail = "JAZZ_Rail_HK21", scope = "rail", side = "rail", grips = "rail" },
	HK33 = { rail = "JAZZ_Rail_HK33", scope = "rail" },
	Galil = { rail = "JAZZ_Rail_Galil", scope = "rail", side = "rail" },
	M24Sniper = { rail = "JAZZ_Rail_M24", scope = "rail", side = "rail" },
	Winchester1894 = { rail = "JAZZ_Rail_Winchester", scope = "rail" },
	AA12 = { rail = "JAZZ_Rail_AA12", scope = "rail", side = "rail" },
	Ithaca = { rail = "JAZZ_Rail_Ithaca", scope = "rail" },
	R870 = { rail = "JAZZ_Rail_R870", scope = "rail", side = "rail" },
	UMP45 = { rail = "JAZZ_Rail_UMP", scope = "rail" },
	MP5K = { rail = "JAZZ_Rail_MP5K", scope = "rail" },
	UZI = { rail = "JAZZ_Rail_UZI", scope = "rail" },
	MicroUZI = { rail = "JAZZ_Rail_MicroUZI", scope = "rail", side = "rail" },
	M14SAW = { rail = "JAZZ_Rail_M14", scope = "rail" },
	M21 = { rail = "JAZZ_Rail_M21", scope = "rail", side = "rail", grips = "rail" },
	JAZZ_M14_MkIII = { rail = "JAZZ_Rail_MkIII", scope = "rail", side = "rail", grips = "rail" },
	M1A = { rail = "JAZZ_Rail_M1A", handguard = "JAZZ_HandguardM1ARail", scope = "rail", side = "handguard", grips = "handguard" },
	M4Commando = { rail = "JAZZ_Rail_Commando", side = "rail", grips = "rail" },
	PSG1 = { rail = "JAZZ_Rail_PSG", side = "rail" },
	Bereta92 = { rail = "JAZZ_Rail_Beretta", side = "rail" },
	CZ52 = { rail = "JAZZ_Rail_PistolUnder", side = "rail" },
	MAC1950 = { rail = "JAZZ_Rail_PistolUnder", side = "rail" },
	P220 = { rail = "JAZZ_Rail_P220", scope = "rail", side = "rail" },
	ColtAnaconda = { rail = "JAZZ_Rail_Anaconda", scope = "rail" },
	VZ58 = { handguard = "JAZZ_Handguard_RIS", scope = "handguard", grips = "handguard" },
	Mosin = { conv = "JAZZ_Conversion_Mosin", conv_scopes = { JAZZ_Scope_PU = true } },
	SVT40 = { conv = "JAZZ_Conversion_SVT", conv_scopes = { JAZZ_Scope_PU = true } },
	G43 = { conv = "JAZZ_Conversion_G43", conv_scopes = { JAZZ_Scope_ZF4 = true } },
	Springfield = { conv = "JAZZ_Conversion_Springfield", conv_scopes = { JAZZ_Scope_Springfield = true } },
	Gewehr98 = { conv = "JAZZ_Conversion_Gewehr", conv_any = true },
	STG44 = { conv = "JAZZ_Conversion_STG", conv_scopes = { JAZZ_Scope_ZF4 = true } },
	M1Garand = { conv = "JAZZ_Conversion_Garand", conv_scopes = { JAZZ_Reflex_Garand = true, JAZZ_Scope_Garand = true } },
}

local function jazz_scope_req(rule, scope)
	if not rule or jazz_is_iron(scope) then
		return nil
	end
	if rule.conv then
		if rule.conv_any or (rule.conv_scopes and rule.conv_scopes[scope]) then
			return "conv"
		end
		return nil
	end
	if rule.scope == "east" then
		return JAZZ_EASTERN_OPTIC[scope] and "dove" or "blocked"
	end
	if rule.scope == "west" then
		return "nato"
	end
	if rule.scope == "split" then
		return JAZZ_EASTERN_OPTIC[scope] and "dove" or "nato"
	end
	if rule.scope == "rail" then
		return "rail"
	end
	if rule.scope == "handguard" then
		return "handguard"
	end
	return nil
end

local function jazz_req_met(weapon, rule, req)
	local components = weapon.components or empty_table
	if req == "dove" then
		return rule.dove and components.Dovetail == rule.dove
	end
	if req == "nato" then
		local dove_ok = rule.factory or (rule.dove and components.Dovetail == rule.dove)
		return dove_ok and rule.nato and components.Rail == rule.nato
	end
	if req == "rail" then
		if rule.handguard_satisfies and components.Handguard == rule.handguard_satisfies then
			return true
		end
		return rule.rail and components.Rail == rule.rail
	end
	if req == "rail2" then
		return rule.rail2 and components.RailSide == rule.rail2
	end
	if req == "handguard" then
		return rule.handguard and components.Handguard == rule.handguard
	end
	if req == "conv" then
		return rule.conv and components.Conversion == rule.conv
	end
	return true
end

local function jazz_fal_reject(weapon, slot, part)
	local components = weapon.components or empty_table
	if slot == "Handguard" and part == JAZZ_FAL_TAC and JAZZ_FAL_FOLD[components.Stock or ""] then
		return true, components.Stock
	end
	if slot == "Handguard" and part ~= JAZZ_FAL_TAC and components.Handguard == JAZZ_FAL_TAC then
		if JAZZ_FAL_LONG[components.Barrel or ""] then
			return true, components.Barrel
		end
		if components.Stock == "JAZZ_StockHeavy" then
			return true, components.Stock
		end
		if (components.Scope or "") ~= "" and not jazz_is_iron(components.Scope) then
			return true, components.Scope
		end
		if (components.Side or "") ~= "" then
			return true, components.Side
		end
		if jazz_is_grip(components.Under) then
			return true, components.Under
		end
	end
	if slot == "Barrel" and JAZZ_FAL_LONG[part] and components.Handguard ~= JAZZ_FAL_TAC then
		return true, components.Handguard
	end
	if slot == "Stock" and part == "JAZZ_StockHeavy" and components.Handguard ~= JAZZ_FAL_TAC then
		return true, components.Handguard
	end
	if slot == "Stock" and JAZZ_FAL_FOLD[part] and components.Handguard == JAZZ_FAL_TAC then
		return true, components.Handguard
	end
	if slot == "Rail" and part ~= "" and components.Handguard == JAZZ_FAL_TAC then
		return true, components.Handguard
	end
	return false
end

function JAZZ_RailReject(weapon, slot, id)
	if type(id) ~= "string" or not weapon or not slot or not IsKindOf(weapon, "FirearmBase") then
		return false
	end
	if rawget(weapon, "_jazz_fal_replacing_rail") and slot == "Rail" and jazz_part(id) == "" then
		return false
	end
	local part = jazz_part(id)
	local rule = JAZZ_RailRules[weapon.class]
	if weapon.class == "FNFAL" then
		local rejected, blocker = jazz_fal_reject(weapon, slot, part)
		if rejected then
			return true, blocker
		end
	end
	if not rule then
		return false
	end
	local components = weapon.components or empty_table
	if part ~= "" then
		local req
		if slot == "Scope" then
			req = jazz_scope_req(rule, part)
			if req == "blocked" then
				return true
			end
			if req == "dove" and rule.nato and components.Rail == rule.nato then
				return true, components.Rail
			end
		elseif slot == "Side" and part ~= "JAZZ_HandlingWrap" and rule.side then
			req = rule.side
		elseif slot == "Under" and jazz_is_grip(part) and rule.grips then
			req = rule.grips
		end
		if req and not jazz_req_met(weapon, rule, req) then
			return true
		end
		if slot == "Rail" and rule.nato and part == rule.nato then
			if not rule.factory and rule.dove and components.Dovetail ~= rule.dove then
				return true
			end
			if JAZZ_EASTERN_OPTIC[components.Scope or ""] then
				return true, components.Scope
			end
		end
		if slot == "Handguard" and rule.handguard and part ~= rule.handguard then
			if rule.side == "handguard" and (components.Side or "") ~= "" then
				return true, components.Side
			end
			if rule.grips == "handguard" and jazz_is_grip(components.Under) then
				return true, components.Under
			end
			if jazz_scope_req(rule, components.Scope) == "handguard" then
				return true, components.Scope
			end
		end
		return false
	end
	if slot == "Dovetail" then
		if rule.nato and components.Rail == rule.nato then
			return true, components.Rail
		end
		if jazz_scope_req(rule, components.Scope) == "dove" then
			return true, components.Scope
		end
		if rule.side == "dove" and (components.Side or "") ~= "" then
			return true, components.Side
		end
	elseif slot == "Rail" then
		local scope_req = jazz_scope_req(rule, components.Scope)
		if scope_req == "nato" or scope_req == "rail" then
			if not (rule.handguard_satisfies and components.Handguard == rule.handguard_satisfies) then
				return true, components.Scope
			end
		end
		if (rule.side == "rail" or rule.side == "nato") and (components.Side or "") ~= ""
			and components.Side ~= "JAZZ_HandlingWrap" then
			return true, components.Side
		end
		if rule.grips == "rail" and jazz_is_grip(components.Under) then
			return true, components.Under
		end
	elseif slot == "RailSide" then
		if rule.side == "rail2" and (components.Side or "") ~= "" then
			return true, components.Side
		end
	elseif slot == "Conversion" then
		if jazz_scope_req(rule, components.Scope) == "conv" then
			return true, components.Scope
		end
	elseif slot == "Handguard" and part == "" then
		if rule.side == "handguard" and (components.Side or "") ~= "" then
			return true, components.Side
		end
		if rule.grips == "handguard" and jazz_is_grip(components.Under) then
			return true, components.Under
		end
		if jazz_scope_req(rule, components.Scope) == "handguard" then
			return true, components.Scope
		end
	end
	return false
end

function JAZZ_RailApplyConversionName(weapon)
	local rule = JAZZ_RailRules[weapon.class]
	if not rule or not rule.conv or weapon.class == "Mosin" then
		return
	end
	local installed = weapon.components and weapon.components.Conversion
	local preset = (g_Classes and g_Classes[weapon.class]) or _G[weapon.class]
	if installed == rule.conv then
		local component = WeaponComponents and WeaponComponents[installed]
		if component then
			weapon.DisplayName = component.DisplayName
			weapon.DisplayNamePlural = component.DisplayNamePlural or component.DisplayName
		end
	elseif preset then
		weapon.DisplayName = preset.DisplayName
		weapon.DisplayNamePlural = preset.DisplayNamePlural
	end
end

local JAZZ_AKM_FOLD = {
	JAZZ_StockLightUnFolded = true,
	JAZZ_StockLightFolded = true,
}

function JAZZ_AKMApplyName(weapon)
	if not weapon or weapon.class ~= "AKM" then
		return
	end
	local components = weapon.components
	local folded = components and JAZZ_AKM_FOLD[components.Stock]
	local dovetail = components and (components.Dovetail or "") ~= ""
	local preset = (g_Classes and g_Classes.AKM) or AKM
	local name
	if folded and dovetail then
		name = T(990003123, "AKMSN")
	elseif folded then
		name = T(990003121, "AKMS")
	elseif dovetail then
		name = T(990003122, "AKMN")
	end
	if name then
		weapon.DisplayName = name
		weapon.DisplayNamePlural = name
	elseif preset then
		weapon.DisplayName = preset.DisplayName
		weapon.DisplayNamePlural = preset.DisplayNamePlural
	end
end

local function jazz_ensure_component(weapon, slot_name, component_id)
	if not component_id or component_id == "" then
		return
	end
	local components = weapon.components
	if not components or components[slot_name] == component_id or (components[slot_name] or "") ~= "" then
		return
	end
	weapon:SetWeaponComponent(slot_name, component_id, "init")
end

local function jazz_ensure_req(weapon, rule, req)
	if not req or req == "blocked" or jazz_req_met(weapon, rule, req) then
		return
	end
	if (req == "dove" or req == "nato") and rule.dove and not rule.factory then
		jazz_ensure_component(weapon, "Dovetail", rule.dove)
	end
	if req == "nato" then
		jazz_ensure_component(weapon, "Rail", rule.nato)
	elseif req == "rail" then
		jazz_ensure_component(weapon, "Rail", rule.rail)
	elseif req == "rail2" then
		jazz_ensure_component(weapon, "RailSide", rule.rail2)
	elseif req == "handguard" then
		jazz_ensure_component(weapon, "Handguard", rule.handguard)
	elseif req == "conv" then
		jazz_ensure_component(weapon, "Conversion", rule.conv)
	end
end

function JAZZ_RailMigrateTacticalFAL(weapon)
	if not weapon or weapon.class ~= "JAZZ_FNFAL_Tactical" then
		return
	end
	weapon.components = weapon.components or {}
	weapon.components.Handguard = JAZZ_FAL_TAC
	weapon.class = "FNFAL"
	if g_Classes and g_Classes.FNFAL then
		setmetatable(weapon, g_Classes.FNFAL)
	end
	if JAZZ_FALApplyPresentation then
		JAZZ_FALApplyPresentation(weapon)
	end
end

function JAZZ_RailHealWeapon(weapon)
	if not weapon or not IsKindOf(weapon, "FirearmBase") then
		return
	end
	JAZZ_RailMigrateTacticalFAL(weapon)
	local rule = JAZZ_RailRules[weapon.class]
	if not rule or not weapon.components then
		return
	end
	local components = weapon.components
	jazz_ensure_req(weapon, rule, jazz_scope_req(rule, components.Scope))
	if rule.side and (components.Side or "") ~= "" and components.Side ~= "JAZZ_HandlingWrap" then
		jazz_ensure_req(weapon, rule, rule.side)
	end
	if rule.grips and jazz_is_grip(components.Under) then
		jazz_ensure_req(weapon, rule, rule.grips)
	end
	if weapon.class ~= "Mosin" then
		JAZZ_RailApplyConversionName(weapon)
	end
	JAZZ_AKMApplyName(weapon)
	if weapon.class == "FNFAL" and JAZZ_FALApplyPresentation then
		JAZZ_FALApplyPresentation(weapon)
	end
end


function FirearmBase:SetWeaponComponent(slot, id, is_init)
	local def = WeaponComponents[id]
	slot = slot or (def and def.Slot)
	local fixed = JazzModelFixedComponents[self.class]
	if fixed and fixed[slot] then
		id = fixed[slot]
		def = WeaponComponents[id]
	end
	
	-- M14 wood stock: Under accepts only a bipod or no component.
	if self.class == "M14SAW" and slot == "Under" and id ~= "JAZZ_Bipod_Under" then
		id = ""
		def = nil
	end

	if self.class == "MK14EBR" and slot == "Under" and id == "JAZZ_GrenadeLauncher_M14" then
		id = ""
		def = nil
	end

	if not slot then
		return
	end
	-- AR15 receiver optics use their own rail; only fore-end attachments need RIS.
	if self.class == "M4A1" or self.class == "M16A4" then
		local components = self.components or empty_table
		if (slot == "Side" or slot == "Under") and id and id ~= ""
			and components.Handguard ~= "JAZZ_Handguard_RIS" then
			return false
		end
		if slot == "Handguard" and id ~= "JAZZ_Handguard_RIS"
			and ((components.Side or "") ~= "" or (components.Under or "") ~= "") then
			return false
		end
	end
	
	if self.class == "FNFAL" and slot == "Handguard" and id == "JAZZ_FNFAL_TacHandguard" then
		local rail_now = (self.components and self.components.Rail) or ""
		if rail_now ~= "" then
			self._jazz_fal_replacing_rail = true
			self:SetWeaponComponent("Rail", "", is_init)
			self._jazz_fal_replacing_rail = nil
		end
	end
	if JAZZ_RailReject(self, slot, id) then
		return false
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
	
	if self.class ~= "Mosin" then
		JAZZ_RailApplyConversionName(self)
	end
	JAZZ_AKMApplyName(self)
	ObjModified(self)
	-- Fold/UnFoldStock returns before CombatActionEnd; refresh existing windows.
	if slot == "Stock" and not is_init and not rawget(self, "is_clone")
		and JazzWeaponIcon_ScheduleWeaponDisplayRefresh then
		JazzWeaponIcon_ScheduleWeaponDisplayRefresh()
	end
end

-- MP40 is MagNormal-only (32). Legacy MagLarge_50_MP40 from GenW loot / old saves → reseat.
local JazzObsoleteMagazineReseat = {
	JAZZ_MagLarge_50_MP40 = "JAZZ_MagNormal",
}

local function JazzReseatObsoleteMagazineOnFirearm(weapon)
	if not IsKindOf(weapon, "FirearmBase") then
		return
	end
	local mag_id = weapon.components and weapon.components.Magazine
	local replacement = mag_id and JazzObsoleteMagazineReseat[mag_id]
	if not replacement then
		return
	end
	local had_broken_one = weapon.ammo and (weapon.ammo.Amount or 0) <= 1
	weapon:SetWeaponComponent("Magazine", replacement, "init")
	if had_broken_one and weapon.ammo and (weapon.MagazineSize or 0) > 1 then
		weapon.ammo.Amount = weapon.MagazineSize
	elseif weapon.ammo and (weapon.ammo.Amount or 0) > (weapon.MagazineSize or 0) then
		weapon.ammo.Amount = weapon.MagazineSize
	end
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
			local fixed = JazzModelFixedComponents[item.class]
			for slot, id in sorted_pairs(fixed or empty_table) do
				if item.components and item.components[slot] ~= id then
					item:SetWeaponComponent(slot, id, "init")
				end
			end
			if item.class == "M14SAW" and item.components
				and (item.components.Under or "") ~= ""
				and item.components.Under ~= "JAZZ_Bipod_Under" then
				item:SetWeaponComponent("Under", "", "init")
			end
			if item.class == "MK14EBR" and item.components and item.components.Under == "JAZZ_GrenadeLauncher_M14" then
				item:SetWeaponComponent("Under", "", "init")
			end
			JazzReseatObsoleteMagazineOnFirearm(item)
			JazzHealMagazineSizeSetOnFirearm(item)
			JAZZ_RailHealWeapon(item)
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


-- JAZZ-WEAPON-PRESENTATION-001: align donor feed lips with the native magazine.
-- Absolute offsets in millimetres; preserve the native feed-box centre and top.
function AK103:UpdateVisualObj(vis)
    vis = vis or self.visual_obj
    if not IsValid(vis) or vis.weapon ~= self then return end
    FirearmBase.UpdateVisualObj(self, vis)
    local part = vis.parts and vis.parts.Magazine
    if not IsValid(part) then return end
    local component = self.components and self.components.Magazine
    if component == "JAZZ_MagNormal" and part:GetEntity() == "AKMWaffleMag" then
        part:SetAttachOffset(point(6, -9, -9))
    elseif component == "JAZZ_MagQuick_AK" and part:GetEntity() == "WeaponAttA_MagazineAK47_03" then
        part:SetAttachOffset(point(3, -10, -2))
    elseif component == "JAZZ_MagLarge_30_40" and part:GetEntity() == "WeaponAttA_MagazineAK47_02" then
        part:SetAttachOffset(point(3, -10, -2))
    elseif component == "JAZZ_MagDrum_30_75" and part:GetEntity() == "WeaponAttA_MagazineRPK74_03" then
        part:SetAttachOffset(point(-9, -10, -8))
    end
end

-- Type 56's stock magazine uses a lower model origin than the AKM donor set.
function Type56:UpdateVisualObj(vis)
    vis = vis or self.visual_obj
    if not IsValid(vis) or vis.weapon ~= self then return end
    FirearmBase.UpdateVisualObj(self, vis)
    local part = vis.parts and vis.parts.Magazine
    if not IsValid(part) then return end
    local component = self.components and self.components.Magazine
    local entity = part:GetEntity()
    if (component == "JAZZ_MagQuick_AK" and entity == "WeaponAttA_MagazineAK47_03")
        or (component == "JAZZ_MagLarge_30_40" and entity == "WeaponAttA_MagazineAK47_02")
        or (component == "JAZZ_MagDrum_30_75" and entity == "WeaponAttA_MagazineRPK74_03") then
        part:SetAttachOffset(point(0, 0, 23))
    end
end
