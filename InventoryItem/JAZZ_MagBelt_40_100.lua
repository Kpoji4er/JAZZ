UndefineClass('JAZZ_MagBelt_40_100')
DefineClass.JAZZ_MagBelt_40_100 = {
	__parents = { "JAZZ_RemovableAttachment" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "WEAPONS-002 remountable → component JAZZ_MagBelt_40_100",
	object_class = "JAZZ_RemovableAttachment",
	RemovableComponentId = "JAZZ_MagBelt_40_100",
	Icon = "UI/Icons/Upgrades/expanded_drum_G36_magazine",
	DisplayName = T(990002214, --[[ModItemInventoryItemCompositeDef JAZZ_MagBelt_40_100 DisplayName]] "Короб"),
	DisplayNamePlural = T(990002215, --[[ModItemInventoryItemCompositeDef JAZZ_MagBelt_40_100 DisplayNamePlural]] "Короб"),
	AdditionalHint = T(990002216, --[[ModItemInventoryItemCompositeDef JAZZ_MagBelt_40_100 AdditionalHint]] "Съёмный модуль. Перетащите на совместимое оружие или установите в кабинете модификации."),
	Cost = 5000,
	CanAppearInShop = true,
	Tier = 4,
	MaxStock = 1,
	RestockWeight = 10,
	CategoryPair = "Magazines",
}

