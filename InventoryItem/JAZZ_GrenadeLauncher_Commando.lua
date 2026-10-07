UndefineClass('JAZZ_GrenadeLauncher_Commando')
DefineClass.JAZZ_GrenadeLauncher_Commando = {
	__parents = { "JAZZ_RemovableAttachment" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "WEAPONS-002 remountable → component JAZZ_GrenadeLauncher_Commando",
	object_class = "JAZZ_RemovableAttachment",
	RemovableComponentId = "JAZZ_GrenadeLauncher_Commando",
	Icon = "UI/Icons/Upgrades/m16_grenade_launcher",
	DisplayName = T(990002181, --[[ModItemInventoryItemCompositeDef JAZZ_GrenadeLauncher_Commando DisplayName]] "Grenade Launcher"),
	DisplayNamePlural = T(990002182, --[[ModItemInventoryItemCompositeDef JAZZ_GrenadeLauncher_Commando DisplayNamePlural]] "Grenade Launcher"),
	AdditionalHint = T(990002183, --[[ModItemInventoryItemCompositeDef JAZZ_GrenadeLauncher_Commando AdditionalHint]] "Съёмный модуль. Перетащите на совместимое оружие или установите в кабинете модификации."),
	Cost = 2000,
	MaxStock = 1,
	RestockWeight = 10,
	CategoryPair = "Components",
}

