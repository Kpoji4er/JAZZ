UndefineClass('JAZZ_SuppressorImproved')
DefineClass.JAZZ_SuppressorImproved = {
	__parents = { "JAZZ_RemovableAttachment" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",

	object_class = "JAZZ_RemovableAttachment",
	Repairable = false,
	Icon = "UI/Icons/Upgrades/shotgun_suppressor",
	DisplayName = T(990002385, --[[ModItemInventoryItemCompositeDef JAZZ_SuppressorImproved DisplayName]] "Улучшенный глушитель"),
	DisplayNamePlural = T(990002386, --[[ModItemInventoryItemCompositeDef JAZZ_SuppressorImproved DisplayNamePlural]] "Улучшенный глушитель"),
	AdditionalHint = T(990002387, --[[ModItemInventoryItemCompositeDef JAZZ_SuppressorImproved AdditionalHint]] "Съёмный модуль. Перетащите на совместимое оружие или установите в кабинете модификации."),
	Cost = 7500,
	CanAppearInShop = true,
	RestockWeight = 10,
	MaxStock = 1,
	Tier = 4,
	CategoryPair = "Muzzle",
	MaxStacks = 1,
	RemovableComponentId = "JAZZ_SuppressorImproved",
}
