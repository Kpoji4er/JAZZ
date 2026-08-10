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
