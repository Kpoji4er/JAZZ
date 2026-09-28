UndefineClass('JAZZ_SuppressorImproved')
DefineClass.JAZZ_SuppressorImproved = {
	__parents = { "JAZZ_RemovableAttachment" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "WEAPONS-002 remountable → component JAZZ_SuppressorImproved",
	object_class = "JAZZ_RemovableAttachment",
	Icon = "UI/Icons/Upgrades/shotgun_suppressor",
	DisplayName = T(990002385, --[[ModItemInventoryItemCompositeDef JAZZ_SuppressorImproved DisplayName]] "Улучшенный глушитель"),
	DisplayNamePlural = T(990002386, --[[ModItemInventoryItemCompositeDef JAZZ_SuppressorImproved DisplayNamePlural]] "Улучшенный глушитель"),
	AdditionalHint = T(990002387, --[[ModItemInventoryItemCompositeDef JAZZ_SuppressorImproved AdditionalHint]] "Съёмный модуль. Перетащите на совместимое оружие или установите в кабинете модификации."),
	Cost = 7500,
	CanAppearInShop = true,
	Tier = 4,
	MaxStock = 1,
	RestockWeight = 10,
	CategoryPair = "Muzzle",
}

