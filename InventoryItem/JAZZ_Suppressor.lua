UndefineClass('JAZZ_Suppressor')
DefineClass.JAZZ_Suppressor = {
	__parents = { "JAZZ_RemovableAttachment" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "WEAPONS-002 remountable → component JAZZ_Suppressor",
	object_class = "JAZZ_RemovableAttachment",
	RemovableComponentId = "JAZZ_Suppressor",
	Icon = "UI/Icons/Upgrades/deserteagle_suppressor",
	DisplayName = T(990002382, --[[ModItemInventoryItemCompositeDef JAZZ_Suppressor DisplayName]] "Suppressor"),
	DisplayNamePlural = T(990002383, --[[ModItemInventoryItemCompositeDef JAZZ_Suppressor DisplayNamePlural]] "Suppressor"),
	AdditionalHint = T(990002384, --[[ModItemInventoryItemCompositeDef JAZZ_Suppressor AdditionalHint]] "Съёмный модуль. Перетащите на совместимое оружие или установите в кабинете модификации."),
	Cost = 4000,
	CanAppearInShop = true,
	Tier = 2,
	MaxStock = 1,
	RestockWeight = 28,
	CategoryPair = "Muzzle",
}

