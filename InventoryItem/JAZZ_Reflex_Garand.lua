UndefineClass('JAZZ_Reflex_Garand')
DefineClass.JAZZ_Reflex_Garand = {
	__parents = { "JAZZ_RemovableAttachment" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",

	object_class = "JAZZ_RemovableAttachment",
	Repairable = false,
	Icon = "Mod/e6L4ECj/WeaponComponents/Optics/GarandReflex.png",
	DisplayName = T(990002328, --[[ModItemInventoryItemCompositeDef JAZZ_Reflex_Garand DisplayName]] "Коллиматор"),
	DisplayNamePlural = T(990002329, --[[ModItemInventoryItemCompositeDef JAZZ_Reflex_Garand DisplayNamePlural]] "Коллиматор"),
	AdditionalHint = T(990002330, --[[ModItemInventoryItemCompositeDef JAZZ_Reflex_Garand AdditionalHint]] "Съёмный модуль. Перетащите на совместимое оружие или установите в кабинете модификации."),
	Cost = 3000,
	CanAppearInShop = true,
	RestockWeight = 10,
	MaxStock = 1,
	Tier = 1,
	CategoryPair = "Components",
	MaxStacks = 1,
	RemovableComponentId = "JAZZ_Reflex_Garand",
}
