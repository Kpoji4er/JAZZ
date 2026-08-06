UndefineClass('JAZZ_FullChoke')
DefineClass.JAZZ_FullChoke = {
	__parents = { "JAZZ_RemovableAttachment" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",

	object_class = "JAZZ_RemovableAttachment",
	Repairable = false,
	Icon = "UI/Icons/Upgrades/shotgun_full_choke",
	DisplayName = T(990002160, --[[ModItemInventoryItemCompositeDef JAZZ_FullChoke DisplayName]] "Full Choke"),
	DisplayNamePlural = T(990002161, --[[ModItemInventoryItemCompositeDef JAZZ_FullChoke DisplayNamePlural]] "Full Choke"),
	AdditionalHint = T(990002162, --[[ModItemInventoryItemCompositeDef JAZZ_FullChoke AdditionalHint]] "Съёмный модуль. Перетащите на совместимое оружие или установите в кабинете модификации."),
	Cost = 2000,
	CanAppearInShop = true,
	RestockWeight = 40,
	MaxStock = 1,
	Tier = 1,
	CategoryPair = "Muzzle",
	MaxStacks = 1,
	RemovableComponentId = "JAZZ_FullChoke",
}
