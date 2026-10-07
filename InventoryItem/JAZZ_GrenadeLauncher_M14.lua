UndefineClass('JAZZ_GrenadeLauncher_M14')
DefineClass.JAZZ_GrenadeLauncher_M14 = {
	__parents = { "JAZZ_RemovableAttachment" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "WEAPONS-002 remountable → component JAZZ_GrenadeLauncher_M14",
	object_class = "JAZZ_RemovableAttachment",
	RemovableComponentId = "JAZZ_GrenadeLauncher_M14",
	Icon = "UI/Icons/Upgrades/m16_grenade_launcher",
	DisplayName = T(990002187, --[[ModItemInventoryItemCompositeDef JAZZ_GrenadeLauncher_M14 DisplayName]] "Grenade Launcher"),
	DisplayNamePlural = T(990002188, --[[ModItemInventoryItemCompositeDef JAZZ_GrenadeLauncher_M14 DisplayNamePlural]] "Grenade Launcher"),
	AdditionalHint = T(990002189, --[[ModItemInventoryItemCompositeDef JAZZ_GrenadeLauncher_M14 AdditionalHint]] "Съёмный модуль. Перетащите на совместимое оружие или установите в кабинете модификации."),
	Cost = 2000,
	MaxStock = 1,
	RestockWeight = 10,
	CategoryPair = "Components",
}

