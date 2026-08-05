-- JAZZ-WEAPONS-002: weapon condition is an absolute resource triad.
-- Condition remains a vanilla/UI compatibility field for non-firearms only.

if FirstLoad then
	JAZZ_HasRemovableComponentOption = false
	JAZZ_ResolveRemovableComponentId = false
	JAZZ_DepositRemovableAttachment = false
	JAZZ_CreateRemovableAttachment = false
	JAZZ_IsRemovableWeaponComponent = false
	JAZZ_GetRemovableAttachmentThreshold = false
	JAZZ_GetSquadMechanical = false
	JAZZ_SyncAllRemovableAttachmentPresentation = false
	JAZZ_NormalizeRemovableAttachmentStack = false
	JAZZ_ResolveRemovableAttachmentIcon = false
	JAZZ_GetRemovableBreakChance = false
	JAZZ_WeaponHasRemovableScope = false
	JAZZ_DepositScopeParts = false
	JAZZ_InstallRemovableAttachment = false
	JAZZ_RemoveRemovableAttachment = false
	JAZZ_FindSlotForRemovableComponent = false
	JAZZ_EjectRemovableAttachmentsForScrap = false
end

local function JazzCeilDiv(value, divisor)
	if value <= 0 then
		return 0
	end
	return DivRound(value + divisor - 1, divisor)
end

-- FirearmBase / InventoryItem method assignment after ClassesBuilt asserts
-- ("object should not have dynamic members"). Normal cold load & ReloadLua use
-- FirstLoad. Accidental DAP dofile must skip sealed class bodies.
if FirstLoad then

InventoryItemProperties.properties[#InventoryItemProperties.properties + 1] = {
	category = "JAZZ Attachments",
	id = "RemovableComponentId",
	name = "Removable Component ID",
	editor = "text",
	default = false,
	template = false,
}

function FirearmBase:GetWeaponResourceMax()
	local maximum = self:GetMaxResource() or self:GetFactoryResource() or 1
	return Max(1, maximum)
end

function FirearmBase:GetWeaponResourceCurrent()
	return Clamp(self:GetCurrentResource() or 0, 0, self:GetWeaponResourceMax())
end

function FirearmBase:GetWeaponResourcePercent()
	return Clamp(MulDivRound(self:GetWeaponResourceCurrent(), 100, self:GetWeaponResourceMax()), 0, 100)
end

function FirearmBase:ClampWeaponResource()
	local maximum = self:GetWeaponResourceMax()
	self.WeaponResource = Clamp(self.WeaponResource or maximum, 0, maximum)
	return self.WeaponResource, maximum
end

function FirearmBase:DamageWeaponResourceMaxPercent(percent)
	local current, maximum = self:GetWeaponResourceCurrent(), self:GetWeaponResourceMax()
	local loss = Max(1, MulDivRound(maximum, percent, 100))
	self.WeaponResourceMax = Max(1, maximum - loss)
	self.WeaponResource = Min(current, self.WeaponResourceMax)
	ObjModified(self)
	return loss
end

function FirearmBase:DamageWeaponResourceMaxUnits(units)
	local current, maximum = self:GetWeaponResourceCurrent(), self:GetWeaponResourceMax()
	self.WeaponResourceMax = Max(1, maximum - Clamp(units or 0, 0, 1))
	self.WeaponResource = Min(current, self.WeaponResourceMax)
	ObjModified(self)
end

function FirearmBase:IsMaxCondition()
	return self:GetWeaponResourceCurrent() >= self:GetWeaponResourceMax()
end

function FirearmBase:GetRepairBarrelPartsCost(restored_current)
	local factory = Max(1, self:GetFactoryResource() or 1)
	local restored_pct = MulDivRound(Max(0, restored_current or 0), 100, factory)
	return JazzCeilDiv(restored_pct, 10)
end

function JAZZ_WeaponHasRemovableScope(weapon)
	if not weapon or not weapon.components then
		return false
	end
	local cid = weapon.components.Scope
	if type(cid) ~= "string" or cid == "" then
		return false
	end
	if cid:find("Iron", 1, true) or cid:find("Ironsight", 1, true) then
		return false
	end
	return JAZZ_IsRemovableWeaponComponent(cid, "Scope")
end

function FirearmBase:GetRepairScopePartsCost(restored_current)
	if not JAZZ_WeaponHasRemovableScope(self) then
		return 0
	end
	local factory = Max(1, self:GetFactoryResource() or 1)
	local restored_pct = MulDivRound(Max(0, restored_current or 0), 100, factory)
	return JazzCeilDiv(restored_pct, 20)
end

function FirearmBase:GetRepairResourceCosts(restored_current, parts_cost)
	return {
		Parts = Max(0, parts_cost or 0),
		JAZZ_BarrelParts = self:GetRepairBarrelPartsCost(restored_current),
		JAZZ_ScopeParts = self:GetRepairScopePartsCost(restored_current),
	}
end

function ItemWithCondition:AmountOfScrapPartsFromItem()
	local parts = self:GetScrapParts()
	local condition = IsKindOf(self, "FirearmBase") and self:GetWeaponResourcePercent() or self.Condition or 100
	if condition < 50 then
		parts = DivRound(parts, 20)
	end
	return Max(1, parts)
end

function FirearmBase:GetSpecialScrapItems()
	-- Vanilla sums AdditionalCosts only. Do NOT add component.Cost — that field is the
	-- modification Parts/money cost (e.g. JAZZ_BarrelNormal Cost=50) and produced
	-- absurd JAZZ_BarrelParts payouts (50+2=52) with 0 meaningful Parts feel.
	local special = {}
	for _, component_id in sorted_pairs(self.components or empty_table) do
		local comp = WeaponComponents[component_id]
		if not comp then
			goto continue
		end
		for _, cost in ipairs(comp.AdditionalCosts or empty_table) do
			local cost_type = cost.Type
			if cost_type == "JAZZ_BarrelParts" or cost_type == "JAZZ_ScopeParts" then
				local amount = cost.Amount or 0
				if amount > 0 then
					local idx = table.find(special, "restype", cost_type)
					if idx then
						special[idx].amount = (special[idx].amount or 0) + amount
					else
						special[#special + 1] = { restype = cost_type, amount = amount }
					end
				end
			end
		end
		::continue::
	end
	return special
end

-- Repair operation still passes percentage deltas to ItemModifyCondition.  Convert
-- them directly to current resource; never reconstruct current from Condition.
-- Positive repair debits JAZZ_BarrelParts (/10) and JAZZ_ScopeParts (/20 if remountable Scope).
local VanillaItemModifyCondition = Inventory.ItemModifyCondition
function Inventory:ItemModifyCondition(item, amount)
	if not IsKindOf(item, "FirearmBase") then
		return VanillaItemModifyCondition(self, item, amount)
	end
	local maximum = item:GetWeaponResourceMax()
	local previous = item:GetWeaponResourceCurrent()
	local current_pct = MulDivRound(previous, 100, maximum)
	local new_pct = Clamp(current_pct + (amount or 0), 0, 100)
	local current = MulDivRound(maximum, new_pct, 100)
	local restored = current - previous
	if restored > 0 and not CheatEnabled("FreeParts") then
		local barrel_cost = item:GetRepairBarrelPartsCost(restored)
		local scope_cost = item:GetRepairScopePartsCost(restored)
		if barrel_cost > 0 or scope_cost > 0 then
			local sector_id = self.Squad and gv_Squads[self.Squad] and gv_Squads[self.Squad].CurrentSector
			if not sector_id and IsKindOf(self, "Unit") then
				sector_id = gv_UnitData[self.session_id] and gv_UnitData[self.session_id].Sector
			end
			if not sector_id then
				return previous
			end
			local available_barrel = GetSectorOperationResource(gv_Sectors[sector_id], "JAZZ_BarrelParts") or 0
			local available_scope = GetSectorOperationResource(gv_Sectors[sector_id], "JAZZ_ScopeParts") or 0
			if available_barrel < barrel_cost or available_scope < scope_cost then
				return previous
			end
			if barrel_cost > 0 then
				PaySectorOperationResource(sector_id, "JAZZ_BarrelParts", barrel_cost)
			end
			if scope_cost > 0 then
				PaySectorOperationResource(sector_id, "JAZZ_ScopeParts", scope_cost)
			end
		end
	end
	item.WeaponResource = current
	Msg("InventoryChange", self)
	if previous ~= current then
		Msg("ItemChangeCondition", item, previous, current, self)
	end
	ObjModified(item)
	ObjModified(self)
	return current
end

-- resource: absolute WeaponResource units, or nil/false to clear jam without wear.
-- Do not pass Condition (0..100%) — that zeros most guns (Condition ≤100 << max).
function FirearmBase:RepairJammed(resource, unit_owner)
	self.jammed = false
	if type(resource) == "number" then
		self.WeaponResource = Clamp(resource, 0, self:GetWeaponResourceMax())
	end
	self:ClampWeaponResource()
	NetUpdateHash("WeaponUnjam", self.class, self.id, self.WeaponResource, self:GetWeaponResourceMax())
	if unit_owner then
		CreateFloatingText(unit_owner, T(123820160317, "Unjammed"))
		Msg("InventoryChange", unit_owner)
		if IsKindOf(unit_owner, "Unit") then
			unit_owner:RecalcUIActions()
		end
		ObjModified(unit_owner)
		PlayFX("UnjamWeapon", "start", unit_owner, self.class)
	end
end

-- Keep existing current-resource degradation, then apply the independent,
-- deterministic per-shot maximum-resource wear and jam damage.
local JazzReliabilityCheck = FirearmBase.ReliabilityCheck
function FirearmBase:ReliabilityCheck(attacker, num_shots)
	local jammed, condition_percent = JazzReliabilityCheck(self, attacker, num_shots)
	local item = self.parent_weapon or self
	if attacker and not attacker.infinite_condition then
		for _ = 1, num_shots or 1 do
			if attacker:Random(200) == 0 then -- 0.5% per fired shot; loss is at most one unit.
				item:DamageWeaponResourceMaxUnits(1)
			end
		end
	end
	if jammed then
		local resource_pct = item:GetWeaponResourcePercent()
		local wear = 100 - resource_pct
		local mechanical = attacker and attacker.Mechanical or 0
		local mechanic_deficit = Max(0, 100 - mechanical)
		local critical_chance = Clamp(
			5 + MulDivRound(wear, 35, 100) + MulDivRound(mechanic_deficit, 25, 100),
			5,
			65
		)
		local critical = attacker and attacker:Random(100) < critical_chance
		item:DamageWeaponResourceMaxPercent(critical and 3 or 0.5)
		item.jazz_last_jam_type = critical and "critical" or "ordinary"
		NetUpdateHash("JAZZWeaponJam", item.class, item.id, item.jazz_last_jam_type, item.WeaponResource, item.WeaponResourceMax)
	end
	return jammed, item:GetWeaponResourcePercent()
end

-- Jam % lives only in inventory card rollover (RolloverInventoryWeaponBase XTemplate
-- → GetDisplayJamChancePercent). Do not append a second line via GetRolloverHint.

end -- FirstLoad: sealed FirearmBase / Inventory / Firearm method defs

-- Vanilla rebuilds SectorOperationResouces in a ClassesBuilt thread *after* WaitDataLoaded.
-- Register BarrelParts / ScopeParts only once that table exists (Parts present).
local function JazzRegisterSectorResource(id, fallback_name_t)
	if SectorOperationResouces[id] then
		return true
	end
	local item = InventoryItemDefs and InventoryItemDefs[id]
	local resource = {
		id = id,
		name = item and item.DisplayName or fallback_name_t,
		icon = (item and item.Icon) or "UI/Icons/Items/parts",
		additional = true,
		context = function(sector)
			return sector
		end,
		current = function(sector)
			if type(sector) == "string" then
				sector = gv_Sectors[sector]
			end
			return GetSectorOperationResource(sector, id)
		end,
		pay = function(sector_id, cost)
			if CheatEnabled("FreeParts") then
				cost = 0
			end
			PaySectorOperationResource(sector_id, id, cost)
		end,
		restore = function(merc, cost)
			if CheatEnabled("FreeParts") then
				cost = 0
			end
			RestoreSectorOperationResource(merc, id, cost)
		end,
	}
	SectorOperationResouces[#SectorOperationResouces + 1] = resource
	SectorOperationResouces[id] = resource
	return true
end

function JazzEnsureBarrelPartsResource()
	if type(SectorOperationResouces) ~= "table" then
		return false
	end
	if not SectorOperationResouces.Parts then
		return false
	end
	JazzRegisterSectorResource("JAZZ_BarrelParts", T(990002002, "Ствольные запчасти"))
	JazzRegisterSectorResource("JAZZ_ScopeParts", T(990002500, "Детали прицелов"))
	return SectorOperationResouces.JAZZ_BarrelParts and SectorOperationResouces.JAZZ_ScopeParts
end

function JazzEnsureScopePartsResource()
	return JazzEnsureBarrelPartsResource()
end

local jazz_component_costs_remapped = false

local function JazzRemapWeaponComponentCosts()
	if jazz_component_costs_remapped or not WeaponComponents then
		return
	end
	jazz_component_costs_remapped = true
	for _, component in pairs(WeaponComponents) do
		local slot = component.Slot
		local additional = component.AdditionalCosts
		if additional then
			for _, cost in ipairs(additional) do
				if cost.Type == "FineSteelPipe" then
					-- BarrelParts only for barrels; furniture/optics legacy pipe → Parts.
					cost.Type = (slot == "Barrel") and "JAZZ_BarrelParts" or "Parts"
				elseif cost.Type == "JAZZ_BarrelParts" and slot ~= "Barrel" then
					cost.Type = "Parts"
				elseif cost.Type == "OpticalLens" or cost.Type == "Microchip" then
					cost.Type = "Parts"
				end
			end
		end
		if slot == "Barrel" and (component.Cost or 0) > 0 then
			component.AdditionalCosts = component.AdditionalCosts or {}
			local already = false
			for _, cost in ipairs(component.AdditionalCosts) do
				if cost.Type == "JAZZ_BarrelParts" then
					already = true
					break
				end
			end
			if not already then
				component.AdditionalCosts[#component.AdditionalCosts + 1] = {
					Type = "JAZZ_BarrelParts",
					Amount = component.Cost,
				}
			end
			component.Cost = 0
		end
	end
end

-- Force CloseRange* effect copy without stale "Ствол:"/"Barrel:" loc cache.
local JazzCloseRangeEffectDescriptions = {
	CloseRangeIncrease = "Ближняя зона: Увеличивает ближнюю зону на <CloseRangeIncrease>",
	CloseRangeDecrease = "Ближняя зона: Уменьшает ближнюю зону на <CloseRangeDecrease>",
	CloseRangeFactorIncrease = "Ближняя зона: Усиливает эффективность на ближней дистанции на <CloseRangeFactorIncrease>",
	CloseRangeFactorDecrease = "Ближняя зона: Ослабляет эффективность на ближней дистанции на <CloseRangeFactorDecrease>",
}

function JazzFixCloseRangeEffectDescriptions()
	if not WeaponComponentEffects then
		return
	end
	for id, text in pairs(JazzCloseRangeEffectDescriptions) do
		local effect = WeaponComponentEffects[id]
		if effect then
			effect.Description = Untranslated(text)
		end
	end
end

local function JazzInitWeaponResources()
	JazzEnsureBarrelPartsResource()
	JazzRemapWeaponComponentCosts()
	JazzFixCloseRangeEffectDescriptions()
end

function OnMsg.DataLoaded()
	JazzInitWeaponResources()
end

-- Forward-declare: local bind lives below RemovableAttachment helpers. Without this,
-- OnMsg.ClassesBuilt resolves a nil global (assert on ReloadLua / ClassesBuilt).
local JazzBindRemovableAttachmentMethods

-- Mirror vanilla SatelliteSectorOperations.lua: rebuild happens in a post-DataLoaded thread.
function OnMsg.ClassesBuilt()
	JazzBindRemovableAttachmentMethods()
	CreateRealTimeThread(function()
		WaitDataLoaded()
		local deadline = RealTime() + 5000
		while RealTime() < deadline do
			if JazzEnsureBarrelPartsResource() then
				JazzRemapWeaponComponentCosts()
				JazzFixCloseRangeEffectDescriptions()
				return
			end
			Sleep(10)
		end
		JazzRemapWeaponComponentCosts()
		JazzFixCloseRangeEffectDescriptions()
	end)
end

local JazzLegacyPartMigration = {
	FineSteelPipe = "JAZZ_BarrelParts",
	OpticalLens = "Parts",
	Microchip = "Parts",
}

local function JazzMigrateLegacyPartInInventory(inventory, old_id, new_id)
	if not inventory or not inventory.ForEachItemDef then
		return
	end
	local replacements = {}
	inventory:ForEachItemDef(old_id, function(item, slot_name)
		replacements[#replacements + 1] = { item = item, slot = slot_name }
	end)
	for _, entry in ipairs(replacements) do
		local item, slot = entry.item, entry.slot
		local amount = IsKindOf(item, "InventoryStack") and item.Amount or 1
		local removed = inventory:RemoveItem(slot, item)
		if removed then
			DoneObject(removed)
			local replacement = PlaceInventoryItem(new_id)
			replacement.Amount = amount
			if IsKindOf(inventory, "SquadBag") then
				inventory:AddAndStackItem(replacement)
			else
				local pos = inventory:AddItem(slot, replacement)
				if not pos then
					local squad = inventory.Squad and GetSquadBagInventory(inventory.Squad)
					if squad then
						squad:AddAndStackItem(replacement)
					else
						DoneObject(replacement)
					end
				end
			end
		end
	end
end

function OnMsg.PreLoadSessionData()
	for _, unit in pairs(gv_UnitData or empty_table) do
		for old_id, new_id in pairs(JazzLegacyPartMigration) do
			JazzMigrateLegacyPartInInventory(unit, old_id, new_id)
		end
	end
	for squad_id in pairs(gv_Squads or empty_table) do
		local bag = GetSquadBagInventory(squad_id)
		for old_id, new_id in pairs(JazzLegacyPartMigration) do
			JazzMigrateLegacyPartInInventory(bag, old_id, new_id)
		end
	end
end

-- v1 remountable contract.  The inventory representation is intentionally
-- generic: a JAZZ_RemovableAttachment instance stores the live component ID.
-- This avoids hundreds of mesh clones while retaining an instance per module.
local JazzRemovableSlots = {
	Scope = true,
	Muzzle = true,
	Side = true,
	Under = true,
	Bipod = true,
	Magazine = true,
	GrenadeLauncher = true,
}

function JAZZ_IsRemovableWeaponComponent(component_id, slot)
	local component = WeaponComponents and WeaponComponents[component_id]
	slot = slot or component and component.Slot
	if not component or not JazzRemovableSlots[slot] or component_id == "" then
		return false
	end
	-- Irons / baseline mags are permanent (or baseline), not lootable modules.
	local id = component_id
	if id:find("Iron", 1, true) or id:find("Ironsight", 1, true) then
		return false
	end
	if id == "JAZZ_MagNormal" or id == "MagNormal" then
		return false
	end
	-- Integral suppressor is part of the receiver (PB, Val, MP5SD, …) — never remount/scrap-eject.
	if id:find("SuppressorIntegrated", 1, true) then
		return false
	end
	return true
end

function JAZZ_GetRemovableAttachmentThreshold(component_id, slot)
	local component = WeaponComponents and WeaponComponents[component_id]
	slot = slot or component and component.Slot
	return (slot == "GrenadeLauncher" or component and component.EnableWeapon) and 40 or 30
end

-- Inventory tile: prefer Visuals.Icon (cabinet/component art), then ChipIcon, then Icon.
function JAZZ_ResolveRemovableAttachmentIcon(component)
	if not component then
		return
	end
	for _, visual in ipairs(component.Visuals or empty_table) do
		if (visual.Icon or "") ~= "" then
			return visual.Icon
		end
	end
	if (component.ChipIcon or "") ~= "" then
		return component.ChipIcon
	end
	if (component.Icon or "") ~= "" then
		return component.Icon
	end
end

-- Per-component InventoryItem companions UndefineClass/DefineClass and wipe methods
-- that were attached to JAZZ_RemovableAttachment. Keep behavior on free functions +
-- InventoryItem hooks (those are never regenerated away).
function JAZZ_RemovableAttachment_GetBoundWeaponComponent(self)
	local id = self and self.RemovableComponentId
	if type(id) ~= "string" or id == "" then
		return
	end
	return WeaponComponents and WeaponComponents[id]
end

function JAZZ_RemovableAttachment_SyncPresentationFromComponent(self)
	local component = JAZZ_RemovableAttachment_GetBoundWeaponComponent(self)
	if not component then
		return false
	end
	local icon = JAZZ_ResolveRemovableAttachmentIcon(component)
	if icon then
		self.Icon = icon
	end
	if component.DisplayName then
		self.DisplayName = component.DisplayName
		self.DisplayNamePlural = component.DisplayName
	end
	return true
end

function JAZZ_RemovableAttachment_GetItemUIIcon(self)
	JAZZ_RemovableAttachment_SyncPresentationFromComponent(self)
	return self.Icon
end

-- Reverse index: WeaponComponent id → firearm class ids that list it in AvailableComponents.
local jazz_removable_compat_index

function JAZZ_InvalidateRemovableCompatIndex()
	jazz_removable_compat_index = false
end

function JAZZ_EnsureRemovableCompatIndex()
	if jazz_removable_compat_index then
		return jazz_removable_compat_index
	end
	local index = {}
	for class_id, def in pairs(InventoryItemDefs or empty_table) do
		local class = g_Classes[class_id]
		if class and IsKindOf(class, "FirearmBase") then
			for _, slot_def in ipairs(class.ComponentSlots or empty_table) do
				for _, cid in ipairs(slot_def.AvailableComponents or empty_table) do
					local list = index[cid]
					if not list then
						list = {}
						index[cid] = list
					end
					if not table.find(list, class_id) then
						list[#list + 1] = class_id
					end
				end
			end
		end
	end
	jazz_removable_compat_index = index
	return index
end

function JAZZ_GetCompatibleWeaponClassIdsForComponent(component_id)
	if type(component_id) ~= "string" or component_id == "" then
		return empty_table
	end
	local index = JAZZ_EnsureRemovableCompatIndex()
	local list = index[component_id]
	if list then
		return list
	end
	if component_id:starts_with("JAZZ_") then
		return index[string.sub(component_id, 6)] or empty_table
	end
	return index["JAZZ_" .. component_id] or empty_table
end

local function JazzTranslateDisplayName(t)
	if not t then
		return ""
	end
	local text = _InternalTranslate(t)
	if type(text) == "string" and text:find("%S") and not (IsLookupTag and IsLookupTag(text)) then
		return text
	end
	return tostring(t)
end

-- Short human list for rollover titles (cap keeps header readable).
function JAZZ_FormatCompatibleWeaponsForTitle(component_id, max_names)
	max_names = max_names or 4
	local class_ids = JAZZ_GetCompatibleWeaponClassIdsForComponent(component_id)
	if not next(class_ids) then
		return ""
	end
	local rows = {}
	for _, class_id in ipairs(class_ids) do
		local class = g_Classes[class_id]
		local label = JazzTranslateDisplayName(class and class.DisplayName) 
		if label == "" then
			label = class_id
		end
		rows[#rows + 1] = { id = class_id, label = label }
	end
	table.sort(rows, function(a, b)
		return a.label < b.label
	end)
	local names = {}
	for i, row in ipairs(rows) do
		if i > max_names then
			names[#names + 1] = "…"
			break
		end
		names[#names + 1] = row.label
	end
	return table.concat(names, ", ")
end

function OnMsg.ModsReloaded()
	JAZZ_InvalidateRemovableCompatIndex()
end

function OnMsg.DataLoaded()
	JAZZ_InvalidateRemovableCompatIndex()
end

function JAZZ_RemovableAttachment_GetRolloverTitle(self)
	local component = JAZZ_RemovableAttachment_GetBoundWeaponComponent(self)
	local name = (component and component.DisplayName) or self.DisplayName
	local weapons = JAZZ_FormatCompatibleWeaponsForTitle(self and self.RemovableComponentId)
	if weapons ~= "" and name then
		return T{990002450, "<weapons>: <name>", weapons = Untranslated(weapons), name = name}
	end
	return name
end

function JAZZ_RemovableAttachment_GetRolloverHint(self)
	local lines = {}
	local component = JAZZ_RemovableAttachment_GetBoundWeaponComponent(self)
	if component and GetWeaponComponentDescription then
		local text = GetWeaponComponentDescription(component)
		if text and text ~= "" then
			lines[#lines + 1] = text
		end
	end
	if self.AdditionalHint and self.AdditionalHint ~= "" then
		lines[#lines + 1] = self.AdditionalHint
	end
	if #lines == 0 then
		return ""
	end
	return table.concat(lines, "\n")
end

function JAZZ_RemovableAttachment_GetRolloverHintWithCondition(self)
	local hint = JAZZ_RemovableAttachment_GetRolloverHint(self)
	local condition = self:GetConditionKeyword()
	if condition and condition ~= "" then
		if hint and hint ~= "" then
			return table.concat({ hint, condition }, "\n")
		end
		return condition
	end
	return hint
end

JazzBindRemovableAttachmentMethods = function()
	local class = rawget(_G, "JAZZ_RemovableAttachment")
	if not class then
		return
	end
	class.GetBoundWeaponComponent = JAZZ_RemovableAttachment_GetBoundWeaponComponent
	class.SyncPresentationFromComponent = JAZZ_RemovableAttachment_SyncPresentationFromComponent
	class.GetItemUIIcon = JAZZ_RemovableAttachment_GetItemUIIcon
	class.GetRolloverTitle = JAZZ_RemovableAttachment_GetRolloverTitle
	class.GetRolloverHint = JAZZ_RemovableAttachment_GetRolloverHint
	class.GetRolloverHintWithCondition = JAZZ_RemovableAttachment_GetRolloverHintWithCondition
end

JazzBindRemovableAttachmentMethods()

if FirstLoad then

local VanillaInventoryItemGetRolloverHint = InventoryItem.GetRolloverHint
function InventoryItem:GetRolloverHint()
	if IsKindOf(self, "JAZZ_RemovableAttachment") then
		return JAZZ_RemovableAttachment_GetRolloverHint(self)
	end
	return VanillaInventoryItemGetRolloverHint(self)
end

local VanillaInventoryItemGetRolloverHintWithCondition = InventoryItem.GetRolloverHintWithCondition
function InventoryItem:GetRolloverHintWithCondition()
	if IsKindOf(self, "JAZZ_RemovableAttachment") then
		return JAZZ_RemovableAttachment_GetRolloverHintWithCondition(self)
	end
	return VanillaInventoryItemGetRolloverHintWithCondition(self)
end

local VanillaInventoryItemGetRolloverTitle = InventoryItem.GetRolloverTitle
function InventoryItem:GetRolloverTitle()
	if IsKindOf(self, "JAZZ_RemovableAttachment") then
		return JAZZ_RemovableAttachment_GetRolloverTitle(self)
	end
	return VanillaInventoryItemGetRolloverTitle(self)
end

local VanillaInventoryItemGetItemUIIcon = InventoryItem.GetItemUIIcon
function InventoryItem:GetItemUIIcon()
	if IsKindOf(self, "JAZZ_RemovableAttachment") then
		return JAZZ_RemovableAttachment_GetItemUIIcon(self)
	end
	return VanillaInventoryItemGetItemUIIcon(self)
end

end -- FirstLoad: InventoryItem rollover/icon hooks

function JAZZ_NormalizeRemovableAttachmentStack(item)
	if not IsKindOf(item, "JAZZ_RemovableAttachment") then
		return
	end
	-- Never allow class-merge: MergeStackIntoContainer keys only on item.class.
	item.MaxStacks = 1
	item.Amount = 1
end

function JAZZ_CreateRemovableAttachment(component_id)
	if not JAZZ_IsRemovableWeaponComponent(component_id) then
		return
	end
	-- Prefer per-component InventoryItem catalog (editor-spawnable Id == component id).
	local item
	local def = InventoryItemDefs and InventoryItemDefs[component_id]
	if def then
		local candidate = PlaceInventoryItem(component_id)
		if IsKindOf(candidate, "JAZZ_RemovableAttachment") then
			item = candidate
		elseif candidate then
			DoneObject(candidate)
		end
	end
	if not item then
		item = PlaceInventoryItem("JAZZ_RemovableAttachment")
	end
	if item then
		item.RemovableComponentId = component_id
		JAZZ_NormalizeRemovableAttachmentStack(item)
		item:SyncPresentationFromComponent()
	end
	return item
end

-- Prefer a free inventory slot over AddAndStackItem: all remountables share one class, so
-- stack-merge by class would destroy distinct RemovableComponentId instances
-- (e.g. collimator + compensator → Amount=2 Compensator).
function JAZZ_DepositRemovableAttachment(attachment, destination_bag, unit)
	if not attachment then
		return false
	end
	JAZZ_NormalizeRemovableAttachmentStack(attachment)
	local function try_add(container)
		if not container then
			return false
		end
		local slot = (GetContainerInventorySlotName and GetContainerInventorySlotName(container)) or "Inventory"
		if container.AddItem then
			local pos = container:AddItem(slot, attachment)
			if pos then
				ObjModified(container)
				return true
			end
		end
		if AddItemsToInventory then
			local placed = AddItemsToInventory(container, { attachment })
			if placed then
				ObjModified(container)
				return true
			end
		end
		return false
	end
	if try_add(destination_bag) then
		return true
	end
	if unit and try_add(unit) then
		return true
	end
	local squad_id = unit and unit.Squad
	if squad_id and try_add(GetSquadBagInventory(squad_id)) then
		return true
	end
	DoneObject(attachment)
	return false
end

local function JazzSyncRemovableAttachmentPresentationIn(container)
	if not container or not container.ForEachItem then
		return
	end
	container:ForEachItem("JAZZ_RemovableAttachment", function(item)
		JAZZ_NormalizeRemovableAttachmentStack(item)
		JAZZ_RemovableAttachment_SyncPresentationFromComponent(item)
	end)
end

function JAZZ_SyncAllRemovableAttachmentPresentation()
	for _, unit in pairs(gv_UnitData or empty_table) do
		JazzSyncRemovableAttachmentPresentationIn(unit)
	end
	for squad_id in pairs(gv_Squads or empty_table) do
		JazzSyncRemovableAttachmentPresentationIn(GetSquadBagInventory(squad_id))
	end
end

function OnMsg.LoadGame()
	DelayedCall(0, JAZZ_SyncAllRemovableAttachmentPresentation)
end

-- Same contract as ModifyWeaponDlg:GetModificationDifficultyParams — best Mechanical in the squad.
function JAZZ_GetSquadMechanical(unit)
	if not unit then
		return 0
	end
	local best = unit.Mechanical or 0
	local squad_id = unit.Squad
	local squad = squad_id and gv_Squads and gv_Squads[squad_id]
	for _, sid in ipairs((squad and squad.units) or empty_table) do
		local mate = (gv_UnitData and gv_UnitData[sid]) or (g_Units and g_Units[sid])
		local mech = mate and mate.Mechanical or 0
		if mech > best then
			best = mech
		end
	end
	return best
end

function JAZZ_GetRemovableBreakChance(weapon)
	if not weapon or not weapon.GetWeaponResourcePercent then
		return 0
	end
	return Clamp(100 - (weapon:GetWeaponResourcePercent() or 100), 0, 95)
end

function JAZZ_DepositScopeParts(destination_bag, unit, amount)
	amount = Max(1, amount or 1)
	local item = PlaceInventoryItem("JAZZ_ScopeParts")
	if not item then
		return false
	end
	if IsKindOf(item, "InventoryStack") then
		item.Amount = amount
	end
	local function try_add(container)
		if not container then
			return false
		end
		if container.AddAndStackItem then
			container:AddAndStackItem(item)
			ObjModified(container)
			return true
		end
		local slot = (GetContainerInventorySlotName and GetContainerInventorySlotName(container)) or "Inventory"
		if container.AddItem and container:AddItem(slot, item) then
			ObjModified(container)
			return true
		end
		return false
	end
	if try_add(destination_bag) then
		return true
	end
	if unit and try_add(unit) then
		return true
	end
	local squad_id = unit and unit.Squad
	if squad_id and try_add(GetSquadBagInventory(squad_id)) then
		return true
	end
	DoneObject(item)
	return false
end

local function JazzAttachmentOperationPasses(unit, component_id, slot)
	local threshold = JAZZ_GetRemovableAttachmentThreshold(component_id, slot)
	local mechanical = JAZZ_GetSquadMechanical(unit)
	if mechanical >= threshold then
		return true
	end
	local chance = Clamp(MulDivRound(Max(0, mechanical), 100, threshold), 5, 95)
	local roller = unit
	if type(unit) == "table" and not unit.Random and unit.session_id then
		roller = g_Units and g_Units[unit.session_id] or unit
	end
	if roller and roller.Random then
		return roller:Random(100) < chance
	end
	return InteractionRand(100, "JAZZ_RemovableAttach") < chance
end

-- Free functions (not sealed FirearmBase methods) so ReloadLua / editor dofile stay strict-safe.
function JAZZ_RemoveRemovableAttachment(weapon, unit, slot, destination_bag)
	if not weapon then
		return false, "no-weapon"
	end
	local component_id = weapon.components and weapon.components[slot]
	if not JAZZ_IsRemovableWeaponComponent(component_id, slot) then
		return false, "not-removable"
	end
	if not JazzAttachmentOperationPasses(unit, component_id, slot) then
		weapon:DamageWeaponResourceMaxPercent(1)
		local break_chance = JAZZ_GetRemovableBreakChance(weapon)
		local roller = unit
		if type(unit) == "table" and not unit.Random and unit.session_id then
			roller = g_Units and g_Units[unit.session_id] or unit
		end
		local roll
		if roller and roller.Random then
			roll = roller:Random(100)
		else
			roll = InteractionRand(100, "JAZZ_RemovableBreak")
		end
		if roll < break_chance then
			weapon:SetWeaponComponent(slot, false)
			if slot == "Scope" and not (component_id:find("Iron", 1, true) or component_id:find("Ironsight", 1, true)) then
				local bag = destination_bag or (unit and unit.Squad and GetSquadBagInventory(unit.Squad))
				JAZZ_DepositScopeParts(bag, unit, 1)
			end
			ObjModified(weapon)
			ObjModified(unit)
			return false, "broken"
		end
		return false, "failed"
	end
	local attachment = JAZZ_CreateRemovableAttachment(component_id)
	if not attachment then
		return false, "attachment-create-failed"
	end
	weapon:SetWeaponComponent(slot, false)
	if not JAZZ_DepositRemovableAttachment(attachment, destination_bag, unit) then
		return false, "no-destination"
	end
	return true, attachment
end

-- Vanilla leftovers (Compensator) vs JAZZ twins (JAZZ_Compensator): bag items may carry
-- either id; install must pick the id listed in this weapon's AvailableComponents.
-- Free functions (not new FirearmBase methods) so ReloadLua / editor dofile stay strict-safe.
function JAZZ_HasRemovableComponentOption(weapon, component_id)
	if not weapon or type(component_id) ~= "string" or component_id == "" then
		return false
	end
	local component = WeaponComponents and WeaponComponents[component_id]
	if not component then
		return false
	end
	local preferred = component.Slot
	for _, slot_def in ipairs(weapon.ComponentSlots or empty_table) do
		local slot = slot_def.SlotType
		if slot == preferred or (not preferred and JazzRemovableSlots[slot]) then
			if table.find(slot_def.AvailableComponents or empty_table, component_id) then
				return true, slot
			end
		end
	end
	return false
end

function JAZZ_ResolveRemovableComponentId(weapon, component_id)
	if not weapon or type(component_id) ~= "string" or component_id == "" then
		return
	end
	local candidates = { component_id }
	if component_id:starts_with("JAZZ_") then
		candidates[#candidates + 1] = string.sub(component_id, 6)
	else
		candidates[#candidates + 1] = "JAZZ_" .. component_id
	end
	for _, cand in ipairs(candidates) do
		local ok, slot = JAZZ_HasRemovableComponentOption(weapon, cand)
		if ok then
			return cand, slot
		end
	end
end

if FirstLoad then

function FirearmBase:JAZZ_InstallRemovableAttachment(unit, slot, attachment, source_inventory)
	return JAZZ_InstallRemovableAttachment(self, unit, slot, attachment, source_inventory)
end

function FirearmBase:JAZZ_RemoveRemovableAttachment(unit, slot, destination_bag)
	return JAZZ_RemoveRemovableAttachment(self, unit, slot, destination_bag)
end

function FirearmBase:JAZZ_FindSlotForRemovableComponent(component_id)
	return JAZZ_FindSlotForRemovableComponent(self, component_id)
end

function FirearmBase:JAZZ_EjectRemovableAttachmentsForScrap(unit, destination_bag)
	return JAZZ_EjectRemovableAttachmentsForScrap(self, unit, destination_bag)
end

end -- FirstLoad: thin FirearmBase wrappers → free functions

function JAZZ_InstallRemovableAttachment(weapon, unit, slot, attachment, source_inventory)
	if not weapon then
		return false, "no-weapon"
	end
	local raw_id = attachment and attachment.RemovableComponentId
	local component_id, resolved_slot = JAZZ_ResolveRemovableComponentId(weapon, raw_id)
	if not component_id then
		component_id = raw_id
	end
	slot = slot or resolved_slot
	if not JAZZ_IsRemovableWeaponComponent(component_id, slot) then
		return false, "not-removable"
	end
	local component = WeaponComponents[component_id]
	slot = slot or (component and component.Slot)
	if not slot then
		return false, "no-slot"
	end
	if not JAZZ_HasRemovableComponentOption(weapon, component_id) then
		return false, "incompatible"
	end
	if not JazzAttachmentOperationPasses(unit, component_id, slot) then
		weapon:DamageWeaponResourceMaxPercent(1)
		return false, "failed"
	end
	if source_inventory then
		local removed = source_inventory:RemoveItem("Inventory", attachment)
			or (source_inventory.RemoveItem and source_inventory:RemoveItem(source_inventory:GetItemSlot(attachment), attachment))
		if not removed then
			return false, "attachment-not-owned"
		end
	end
	local previous = weapon.components and weapon.components[slot]
	if previous and previous ~= "" and JAZZ_IsRemovableWeaponComponent(previous, slot) then
		local bag = unit and unit.Squad and GetSquadBagInventory(unit.Squad)
		local ejected = JAZZ_CreateRemovableAttachment(previous)
		if ejected and not JAZZ_DepositRemovableAttachment(ejected, bag, unit) then
			DoneObject(ejected)
		end
	end
	weapon:SetWeaponComponent(slot, component_id)
	DoneObject(attachment)
	return true
end

function JAZZ_FindSlotForRemovableComponent(weapon, component_id)
	local _, slot = JAZZ_ResolveRemovableComponentId(weapon, component_id)
	return slot
end

function JAZZ_EjectRemovableAttachmentsForScrap(weapon, unit, destination_bag)
	if not weapon then
		return
	end
	destination_bag = destination_bag or (unit and unit.Squad and GetSquadBagInventory(unit.Squad))
	if not destination_bag then
		return
	end
	-- Snapshot first: SetWeaponComponent mutates components while iterating.
	local to_eject = {}
	for slot, component_id in sorted_pairs(weapon.components or empty_table) do
		if JAZZ_IsRemovableWeaponComponent(component_id, slot) then
			to_eject[#to_eject + 1] = { slot = slot, component_id = component_id }
		end
	end
	for _, entry in ipairs(to_eject) do
		-- Scrap eject is free (no Mech roll): player already loses the receiver.
		local attachment = JAZZ_CreateRemovableAttachment(entry.component_id)
		weapon:SetWeaponComponent(entry.slot, false)
		if attachment then
			JAZZ_DepositRemovableAttachment(attachment, destination_bag, unit)
		end
	end
end

