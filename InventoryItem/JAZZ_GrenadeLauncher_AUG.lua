UndefineClass('JAZZ_GrenadeLauncher_AUG')
DefineClass.JAZZ_GrenadeLauncher_AUG = {
	__parents = { "JAZZ_RemovableAttachment" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",

	object_class = "JAZZ_RemovableAttachment",
	Repairable = false,
	Icon = "UI/Icons/Upgrades/m16_grenade_launcher",
	DisplayName = T(990002178, --[[ModItemInventoryItemCompositeDef JAZZ_GrenadeLauncher_AUG DisplayName]] "Grenade Launcher"),
	DisplayNamePlural = T(990002179, --[[ModItemInventoryItemCompositeDef JAZZ_GrenadeLauncher_AUG DisplayNamePlural]] "Grenade Launcher"),
	AdditionalHint = T(990002180, --[[ModItemInventoryItemCompositeDef JAZZ_GrenadeLauncher_AUG AdditionalHint]] "Съёмный модуль. Перетащите на совместимое оружие или установите в кабинете модификации."),
	Cost = 2000,
	CanAppearInShop = true,
	RestockWeight = 10,
	MaxStock = 1,
	Tier = 1,
	CategoryPair = "Components",
	MaxStacks = 1,
	RemovableComponentId = "JAZZ_GrenadeLauncher_AUG",
}
