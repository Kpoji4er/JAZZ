UndefineClass('JAZZ_Reflex_Pistol')
DefineClass.JAZZ_Reflex_Pistol = {
	__parents = { "JAZZ_RemovableAttachment" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "WEAPONS-002 remountable → component JAZZ_Reflex_Pistol",
	object_class = "JAZZ_RemovableAttachment",
	Icon = "Mod/e6L4ECj/WeaponComponents/Optics/ReflexOpen.png",
	DisplayName = T(990002340, --[[ModItemInventoryItemCompositeDef JAZZ_Reflex_Pistol DisplayName]] "Коллиматор Пистолетный"),
	DisplayNamePlural = T(990002341, --[[ModItemInventoryItemCompositeDef JAZZ_Reflex_Pistol DisplayNamePlural]] "Коллиматор Пистолетный"),
	AdditionalHint = T(990002342, --[[ModItemInventoryItemCompositeDef JAZZ_Reflex_Pistol AdditionalHint]] "Съёмный модуль. Перетащите на совместимое оружие или установите в кабинете модификации."),
	Cost = 4500,
	CanAppearInShop = true,
	Tier = 2,
	MaxStock = 1,
	RestockWeight = 28,
	CategoryPair = "Optics",
}

