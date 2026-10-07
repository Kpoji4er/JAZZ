UndefineClass('JAZZ_G36Sight')
DefineClass.JAZZ_G36Sight = {
	__parents = { "JAZZ_RemovableAttachment" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "WEAPONS-002 remountable → component JAZZ_G36Sight",
	object_class = "JAZZ_RemovableAttachment",
	RemovableComponentId = "JAZZ_G36Sight",
	Icon = "UI/Icons/Upgrades/g36_scope_01",
	DisplayName = T(990002166, --[[ModItemInventoryItemCompositeDef JAZZ_G36Sight DisplayName]] "Прицел G36 1.5x"),
	DisplayNamePlural = T(990002167, --[[ModItemInventoryItemCompositeDef JAZZ_G36Sight DisplayNamePlural]] "Прицел G36 1.5x"),
	AdditionalHint = T(990002168, --[[ModItemInventoryItemCompositeDef JAZZ_G36Sight AdditionalHint]] "Съёмный модуль. Перетащите на совместимое оружие или установите в кабинете модификации."),
	Cost = 0,
	MaxStock = 1,
	RestockWeight = 10,
	CategoryPair = "Components",
}

