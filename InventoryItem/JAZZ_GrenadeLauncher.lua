UndefineClass('JAZZ_GrenadeLauncher')
DefineClass.JAZZ_GrenadeLauncher = {
	__parents = { "JAZZ_RemovableAttachment" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "WEAPONS-002 remountable → component JAZZ_GrenadeLauncher",
	object_class = "JAZZ_RemovableAttachment",
	Icon = "UI/Icons/Upgrades/grenade_launcher_WP",
	DisplayName = T(990002175, --[[ModItemInventoryItemCompositeDef JAZZ_GrenadeLauncher DisplayName]] "Grenade Launcher"),
	DisplayNamePlural = T(990002176, --[[ModItemInventoryItemCompositeDef JAZZ_GrenadeLauncher DisplayNamePlural]] "Grenade Launcher"),
	AdditionalHint = T(990002177, --[[ModItemInventoryItemCompositeDef JAZZ_GrenadeLauncher AdditionalHint]] "Съёмный модуль. Перетащите на совместимое оружие или установите в кабинете модификации."),
	Cost = 5000,
	MaxStock = 1,
	RestockWeight = 10,
	CategoryPair = "Components",
}

