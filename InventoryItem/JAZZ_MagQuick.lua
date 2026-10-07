UndefineClass('JAZZ_MagQuick')
DefineClass.JAZZ_MagQuick = {
	__parents = { "JAZZ_RemovableAttachment" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "WEAPONS-002 remountable → component JAZZ_MagQuick",
	object_class = "JAZZ_RemovableAttachment",
	RemovableComponentId = "JAZZ_MagQuick",
	Icon = "UI/Icons/Upgrades/quick_AK47_magazine",
	DisplayName = T(990002292, --[[ModItemInventoryItemCompositeDef JAZZ_MagQuick DisplayName]] "Quick Mag"),
	DisplayNamePlural = T(990002293, --[[ModItemInventoryItemCompositeDef JAZZ_MagQuick DisplayNamePlural]] "Quick Mag"),
	AdditionalHint = T(990002294, --[[ModItemInventoryItemCompositeDef JAZZ_MagQuick AdditionalHint]] "Съёмный модуль. Перетащите на совместимое оружие или установите в кабинете модификации."),
	Cost = 1500,
	MaxStock = 1,
	RestockWeight = 10,
	CategoryPair = "Components",
}

