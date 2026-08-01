UndefineClass('JAZZ_Reflex_Pistol')
DefineClass.JAZZ_Reflex_Pistol = {
	__parents = { "JAZZ_RemovableAttachment" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",

	object_class = "JAZZ_RemovableAttachment",
	Repairable = false,
	Icon = "Mod/e6L4ECj/WeaponComponents/Optics/ReflexOpen.png",
	DisplayName = T(990002340, --[[ModItemInventoryItemCompositeDef JAZZ_Reflex_Pistol DisplayName]] "Коллиматор Пистолетный"),
	DisplayNamePlural = T(990002341, --[[ModItemInventoryItemCompositeDef JAZZ_Reflex_Pistol DisplayNamePlural]] "Коллиматор Пистолетный"),
	AdditionalHint = T(990002342, --[[ModItemInventoryItemCompositeDef JAZZ_Reflex_Pistol AdditionalHint]] "Съёмный модуль. Перетащите на совместимое оружие или установите в кабинете модификации."),
	Cost = 4500,
	CanAppearInShop = true,
	RestockWeight = 10,
	MaxStock = 1,
	Tier = 1,
	CategoryPair = "Components",
	MaxStacks = 1,
	RemovableComponentId = "JAZZ_Reflex_Pistol",
}
