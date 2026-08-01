UndefineClass('JAZZ_GrenadeLauncher_M14')
DefineClass.JAZZ_GrenadeLauncher_M14 = {
	__parents = { "JAZZ_RemovableAttachment" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",

	object_class = "JAZZ_RemovableAttachment",
	Repairable = false,
	Icon = "UI/Icons/Upgrades/m16_grenade_launcher",
	DisplayName = T(990002187, --[[ModItemInventoryItemCompositeDef JAZZ_GrenadeLauncher_M14 DisplayName]] "Grenade Launcher"),
	DisplayNamePlural = T(990002188, --[[ModItemInventoryItemCompositeDef JAZZ_GrenadeLauncher_M14 DisplayNamePlural]] "Grenade Launcher"),
	AdditionalHint = T(990002189, --[[ModItemInventoryItemCompositeDef JAZZ_GrenadeLauncher_M14 AdditionalHint]] "Съёмный модуль. Перетащите на совместимое оружие или установите в кабинете модификации."),
	Cost = 2000,
	CanAppearInShop = true,
	RestockWeight = 10,
	MaxStock = 1,
	Tier = 1,
	CategoryPair = "Components",
	MaxStacks = 1,
	RemovableComponentId = "JAZZ_GrenadeLauncher_M14",
}
