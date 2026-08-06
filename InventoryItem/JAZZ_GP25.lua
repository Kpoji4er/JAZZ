UndefineClass('JAZZ_GP25')
DefineClass.JAZZ_GP25 = {
	__parents = { "JAZZ_RemovableAttachment" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",

	object_class = "JAZZ_RemovableAttachment",
	Repairable = false,
	Icon = "UI/Icons/Upgrades/grenade_launcher_WP",
	DisplayName = T(990002169, --[[ModItemInventoryItemCompositeDef JAZZ_GP25 DisplayName]] "ГП-25"),
	DisplayNamePlural = T(990002170, --[[ModItemInventoryItemCompositeDef JAZZ_GP25 DisplayNamePlural]] "ГП-25"),
	AdditionalHint = T(990002171, --[[ModItemInventoryItemCompositeDef JAZZ_GP25 AdditionalHint]] "Съёмный модуль. Перетащите на совместимое оружие или установите в кабинете модификации."),
	Cost = 5000,
	CanAppearInShop = false,
	RestockWeight = 10,
	MaxStock = 1,
	Tier = 1,
	CategoryPair = "Components",
	MaxStacks = 1,
	RemovableComponentId = "JAZZ_GP25",
}
