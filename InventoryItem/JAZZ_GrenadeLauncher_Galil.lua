UndefineClass('JAZZ_GrenadeLauncher_Galil')
DefineClass.JAZZ_GrenadeLauncher_Galil = {
	__parents = { "JAZZ_RemovableAttachment" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "WEAPONS-002 remountable → component JAZZ_GrenadeLauncher_Galil",
	object_class = "JAZZ_RemovableAttachment",
	Icon = "UI/Icons/Upgrades/m16_grenade_launcher",
	DisplayName = T(990002184, --[[ModItemInventoryItemCompositeDef JAZZ_GrenadeLauncher_Galil DisplayName]] "Grenade Launcher"),
	DisplayNamePlural = T(990002185, --[[ModItemInventoryItemCompositeDef JAZZ_GrenadeLauncher_Galil DisplayNamePlural]] "Grenade Launcher"),
	AdditionalHint = T(990002186, --[[ModItemInventoryItemCompositeDef JAZZ_GrenadeLauncher_Galil AdditionalHint]] "Съёмный модуль. Перетащите на совместимое оружие или установите в кабинете модификации."),
	Cost = 5000,
	MaxStock = 1,
	RestockWeight = 10,
	CategoryPair = "Components",
}

