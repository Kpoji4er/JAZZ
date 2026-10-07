UndefineClass('JAZZ_MagQuick_AUG')
DefineClass.JAZZ_MagQuick_AUG = {
	__parents = { "JAZZ_RemovableAttachment" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "WEAPONS-002 remountable → component JAZZ_MagQuick_AUG",
	object_class = "JAZZ_RemovableAttachment",
	RemovableComponentId = "JAZZ_MagQuick_AUG",
	Icon = "Mod/e6L4ECj/WeaponComponents/Magazine/AUG_MagQuick.png",
	DisplayName = T(990002607, --[[ModItemInventoryItemCompositeDef JAZZ_MagQuick_AUG DisplayName]] "Quick Mag"),
	DisplayNamePlural = T(990002608, --[[ModItemInventoryItemCompositeDef JAZZ_MagQuick_AUG DisplayNamePlural]] "Quick Mag"),
	AdditionalHint = T(990002609, --[[ModItemInventoryItemCompositeDef JAZZ_MagQuick_AUG AdditionalHint]] "Семья магазинов: AUG. Съёмный модуль. Перетащите на совместимое оружие или установите в кабинете модификации."),
	Cost = 1500,
	CanAppearInShop = true,
	Tier = 4,
	MaxStock = 1,
	RestockWeight = 10,
	CategoryPair = "Magazines",
}

