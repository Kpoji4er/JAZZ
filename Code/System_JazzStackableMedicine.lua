-- MED-001: load before InventoryItem medicine companions.
-- Field stacks (Bandage/Morphine) and kit stacks (IFAK/Medkit/Reanimationsset):
-- vanilla Medicine is not InventoryStack — loot stack_min/max would spawn N tiles
-- and InventoryUI would show Condition% ("100%") instead of Amount/MaxStacks.

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
