UndefineClass('JAZZ_FlashHider')
DefineClass.JAZZ_FlashHider = {
	__parents = { "JAZZ_RemovableAttachment" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "WEAPONS-002 remountable → component JAZZ_FlashHider",
	object_class = "JAZZ_RemovableAttachment",
	RemovableComponentId = "JAZZ_FlashHider",
	Icon = "Mod/e6L4ECj/WeaponComponents/Carbine/CarbineFlashHider.png",
	DisplayName = T(990002136, --[[ModItemInventoryItemCompositeDef JAZZ_FlashHider DisplayName]] "Пламегаситель"),
	DisplayNamePlural = T(990002137, --[[ModItemInventoryItemCompositeDef JAZZ_FlashHider DisplayNamePlural]] "Пламегаситель"),
	AdditionalHint = T(990002138, --[[ModItemInventoryItemCompositeDef JAZZ_FlashHider AdditionalHint]] "Съёмный модуль. Перетащите на совместимое оружие или установите в кабинете модификации."),
	CanAppearInShop = true,
	MaxStock = 1,
	RestockWeight = 40,
	CategoryPair = "Muzzle",
}

