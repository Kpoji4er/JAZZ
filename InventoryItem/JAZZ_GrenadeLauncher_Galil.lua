UndefineClass('JAZZ_GrenadeLauncher_Galil')
DefineClass.JAZZ_GrenadeLauncher_Galil = {
	__parents = { "JAZZ_RemovableAttachment" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",

	object_class = "JAZZ_RemovableAttachment",
	Repairable = false,
	Icon = "UI/Icons/Upgrades/m16_grenade_launcher",
	DisplayName = T(990002184, --[[ModItemInventoryItemCompositeDef JAZZ_GrenadeLauncher_Galil DisplayName]] "Grenade Launcher"),
	DisplayNamePlural = T(990002185, --[[ModItemInventoryItemCompositeDef JAZZ_GrenadeLauncher_Galil DisplayNamePlural]] "Grenade Launcher"),
	AdditionalHint = T(990002186, --[[ModItemInventoryItemCompositeDef JAZZ_GrenadeLauncher_Galil AdditionalHint]] "Съёмный модуль. Перетащите на совместимое оружие или установите в кабинете модификации."),
	Cost = 5000,
	CanAppearInShop = false,
	RestockWeight = 10,
	MaxStock = 1,
	Tier = 1,
	CategoryPair = "Components",
	MaxStacks = 1,
	RemovableComponentId = "JAZZ_GrenadeLauncher_Galil",
}
