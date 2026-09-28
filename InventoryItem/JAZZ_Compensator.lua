UndefineClass('JAZZ_Compensator')
DefineClass.JAZZ_Compensator = {
	__parents = { "JAZZ_RemovableAttachment" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "WEAPONS-002 remountable → component JAZZ_Compensator",
	object_class = "JAZZ_RemovableAttachment",
	Icon = "UI/Icons/Upgrades/MP5_compensator",
	DisplayName = T(990002130, --[[ModItemInventoryItemCompositeDef JAZZ_Compensator DisplayName]] "Compensator"),
	DisplayNamePlural = T(990002131, --[[ModItemInventoryItemCompositeDef JAZZ_Compensator DisplayNamePlural]] "Compensator"),
	AdditionalHint = T(990002132, --[[ModItemInventoryItemCompositeDef JAZZ_Compensator AdditionalHint]] "Съёмный модуль. Перетащите на совместимое оружие или установите в кабинете модификации."),
	Cost = 3000,
	CanAppearInShop = true,
	Tier = 2,
	MaxStock = 1,
	RestockWeight = 28,
	CategoryPair = "Muzzle",
}

