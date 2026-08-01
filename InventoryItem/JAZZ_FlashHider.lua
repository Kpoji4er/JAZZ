UndefineClass('JAZZ_FlashHider')
DefineClass.JAZZ_FlashHider = {
	__parents = { "JAZZ_RemovableAttachment" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",

	object_class = "JAZZ_RemovableAttachment",
	Repairable = false,
	Icon = "Mod/e6L4ECj/WeaponComponents/Carbine/CarbineFlashHider.png",
	DisplayName = T(990002136, --[[ModItemInventoryItemCompositeDef JAZZ_FlashHider DisplayName]] "Пламегаситель"),
	DisplayNamePlural = T(990002137, --[[ModItemInventoryItemCompositeDef JAZZ_FlashHider DisplayNamePlural]] "Пламегаситель"),
	AdditionalHint = T(990002138, --[[ModItemInventoryItemCompositeDef JAZZ_FlashHider AdditionalHint]] "Съёмный модуль. Перетащите на совместимое оружие или установите в кабинете модификации."),
	Cost = 1000,
	CanAppearInShop = true,
	RestockWeight = 10,
	MaxStock = 1,
	Tier = 1,
	CategoryPair = "Components",
	MaxStacks = 1,
	RemovableComponentId = "JAZZ_FlashHider",
}
