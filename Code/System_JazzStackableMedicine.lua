-- MED-001: load before InventoryItem medicine companions.
-- Field stacks (Bandage/Morphine) and kit stacks (IFAK/Medkit/Reanimationsset):
-- vanilla Medicine is not InventoryStack — loot stack_min/max would spawn N tiles
-- and InventoryUI would show Condition% ("100%") instead of Amount/MaxStacks.

local function lMedicineGlobal(name)
	local value = rawget(_G, name)
	if value ~= nil then
		return value
	end
	local mt = getmetatable(_G)
	local index = mt and mt.__index
	if type(index) == "function" then
		return index(_G, name)
	end
	if type(index) == "table" then
		return index[name]
	end
	return nil
end

UndefineClass("JazzStackableMedicine")
DefineClass.JazzStackableMedicine = {
	__parents = { "InventoryStack", "Medicine" },
}

function JazzStackableMedicine:HasCondition()
	return false
end

function JazzStackableMedicine:GetConditionPercent()
	return 100
end

function JazzStackableMedicine:IsMaxCondition()
	return true
end

function JazzStackableMedicine:IsCondition()
	return false
end

function JazzMedicineIsKitClass(class_id)
	return class_id == "FirstAidKit" or class_id == "Medkit" or class_id == "Reanimationsset"
end

function JazzMedicineIsFieldStack(class_id)
	return class_id == "JAZZ_Bandage" or class_id == "JAZZ_Morphine"
end

-- JAZZ-INV-005: one field item → 1 Meds. Kits stay on vanilla max_meds_parts salvage.
function Jazz_FieldMedicineSalvageMeds(class_id)
	if class_id == "JAZZ_Bandage" or class_id == "JAZZ_Morphine" then
		return 1
	end
	return 0
end

g_JAZZ_AmountOfSalvagedMedsBase = rawget(_G, "g_JAZZ_AmountOfSalvagedMedsBase") or false
g_JAZZ_SalvageItemBase = rawget(_G, "g_JAZZ_SalvageItemBase") or false
g_JAZZ_MedsSalvageWrapped = rawget(_G, "g_JAZZ_MedsSalvageWrapped") or false

function Jazz_AmountOfSalvagedMeds(item, condition, factor)
	if item and JazzMedicineIsFieldStack(item.class) then
		if (item.Amount or 0) > 0 then
			return Jazz_FieldMedicineSalvageMeds(item.class)
		end
		return 0
	end
	local base = rawget(_G, "g_JAZZ_AmountOfSalvagedMedsBase")
	if type(base) == "function" then
		return base(item, condition, factor)
	end
	return 0
end

function Jazz_SalvageItem(inventory, slot_name, item, squadBag)
	if item and JazzMedicineIsFieldStack(item.class) then
		local yield = Jazz_FieldMedicineSalvageMeds(item.class)
		if yield <= 0 or (item.Amount or 0) < 1 then
			return
		end
		if squadBag and squadBag.AddAndStackItem then
			local meds = PlaceInventoryItem("Meds")
			if meds then
				meds.Amount = yield
				squadBag:AddAndStackItem(meds)
			end
		end
		item.Amount = (item.Amount or 1) - 1
		if item.Amount <= 0 and inventory and inventory.RemoveItem then
			local removed = inventory:RemoveItem(slot_name, item)
			DoneObject(removed)
		end
		return
	end
	local base = rawget(_G, "g_JAZZ_SalvageItemBase")
	if type(base) == "function" then
		return base(inventory, slot_name, item, squadBag)
	end
end

local function Jazz_InstallFieldMedsSalvageWrap()
	if rawget(_G, "g_JAZZ_MedsSalvageWrapped") then
		local amount_fn = rawget(_G, "AmountOfSalvagedMeds")
		if amount_fn ~= Jazz_AmountOfSalvagedMeds then
			rawset(_G, "AmountOfSalvagedMeds", Jazz_AmountOfSalvagedMeds)
		end
		local salvage_fn = rawget(_G, "SalvageItem")
		if salvage_fn ~= Jazz_SalvageItem then
			rawset(_G, "SalvageItem", Jazz_SalvageItem)
		end
		return
	end
	local amount_base = rawget(_G, "AmountOfSalvagedMeds")
	local salvage_base = rawget(_G, "SalvageItem")
	if type(amount_base) ~= "function" or type(salvage_base) ~= "function" then
		return
	end
	if amount_base == Jazz_AmountOfSalvagedMeds or salvage_base == Jazz_SalvageItem then
		return
	end
	rawset(_G, "g_JAZZ_AmountOfSalvagedMedsBase", amount_base)
	rawset(_G, "g_JAZZ_SalvageItemBase", salvage_base)
	rawset(_G, "AmountOfSalvagedMeds", Jazz_AmountOfSalvagedMeds)
	rawset(_G, "SalvageItem", Jazz_SalvageItem)
	rawset(_G, "g_JAZZ_MedsSalvageWrapped", true)
end

local function Jazz_PatchInventoryFieldMedsSalvageUI()
	local templates = rawget(_G, "XTemplates")
	local xt = templates and templates.InventoryContextMenu
	if not xt then
		return
	end
	local function walk(node, depth)
		if type(node) ~= "table" or (depth or 0) > 64 then
			return false
		end
		if node.comment == "medicine" then
			for _, child in ipairs(node) do
				if type(child) == "table" and type(child.__condition) == "function" and not rawget(child, "JazzFieldMedsSalvagePatched") then
					local base = child.__condition
					child.__condition = function(parent, context)
						if base(parent, context) then
							return true
						end
						local item = context and context.item
						local same_sector = rawget(_G, "InventoryIsContainerOnSameSector")
						return context
							and type(same_sector) == "function" and same_sector(context)
							and item
							and JazzMedicineIsFieldStack(item.class)
					end
					rawset(child, "JazzFieldMedsSalvagePatched", true)
				end
			end
		end
		if node.Id == "salvage" and type(node.__condition) == "function" and not rawget(node, "JazzFieldMedsSalvageBtnPatched") then
			local base = node.__condition
			node.__condition = function(parent, context)
				local item = context and context.item
				if item and JazzMedicineIsFieldStack(item.class) then
					local same_sector = rawget(_G, "InventoryIsContainerOnSameSector")
					return type(same_sector) == "function" and same_sector(context)
						and (item.Amount or 0) > 0
						and Jazz_AmountOfSalvagedMeds(item) > 0
				end
				return base(parent, context)
			end
			rawset(node, "JazzFieldMedsSalvageBtnPatched", true)
		end
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
		return false
	end
	walk(xt, 0)
end

function OnMsg.DataLoaded()
	Jazz_InstallFieldMedsSalvageWrap()
	Jazz_PatchInventoryFieldMedsSalvageUI()
end

function OnMsg.ModsReloaded()
	Jazz_InstallFieldMedsSalvageWrap()
	Jazz_PatchInventoryFieldMedsSalvageUI()
end

Jazz_InstallFieldMedsSalvageWrap()
Jazz_PatchInventoryFieldMedsSalvageUI()

function JazzMedicineIsUsable(item)
	if not item then
		return false
	end
	if IsKindOf(item, "InventoryStack") then
		return (item.Amount or 0) > 0
	end
	return (item.Condition or 0) > 0
end

function JazzMedicineRequiredMedical(item_or_class)
	local class_id = type(item_or_class) == "string" and item_or_class or item_or_class and item_or_class.class
	if class_id == "FirstAidKit" then
		return 30
	end
	if class_id == "Medkit" then
		return 50
	end
	if class_id == "Reanimationsset" then
		return 80
	end
	return 0
end

function JazzMedicineMeetsRequirement(unit, item_or_class)
	local required = JazzMedicineRequiredMedical(item_or_class)
	local current = unit and (unit.Medical or 0) or false
	return required <= 0 or current and current >= required, required, current
end

function JazzMedicineRequirementWarning(unit, item_or_class)
	local _, required, current = JazzMedicineMeetsRequirement(unit, item_or_class)
	return T{
		890000000012013,
		"Medical too low: <current>/<required>",
		current = current or 0,
		required = required,
	}
end

function JazzMedicineRolloverUnit(context)
	local owner_id = context and context.owner
	local units = lMedicineGlobal("g_Units")
	local unit_data = lMedicineGlobal("gv_UnitData")
	local satellite = lMedicineGlobal("gv_SatelliteView")
	local unit = owner_id and units and units[owner_id]
	if owner_id and (satellite or not unit) then
		unit = unit_data and unit_data[owner_id]
	end
	if not unit then
		local get_inventory_unit = lMedicineGlobal("GetInventoryUnit")
		unit = type(get_inventory_unit) == "function" and get_inventory_unit() or false
	end
	if not unit then
		unit = lMedicineGlobal("SelectedObj")
	end
	if not unit then
		local selection = lMedicineGlobal("Selection")
		unit = selection and selection[1]
	end
	return unit or false
end
