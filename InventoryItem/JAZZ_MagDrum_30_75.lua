UndefineClass('JAZZ_MagDrum_30_75')
DefineClass("JAZZ_MagDrum_30_75", {
	__parents = { "JAZZ_RemovableAttachment" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",

	object_class = "JAZZ_RemovableAttachment",
	Repairable = false,
	Icon = "UI/Icons/Upgrades/RPK74_drum_magazine",
	DisplayName = T(990002226, --[[ModItemInventoryItemCompositeDef JAZZ_MagDrum_30_75 DisplayName]] "Бубен"),
	DisplayNamePlural = T(990002227, --[[ModItemInventoryItemCompositeDef JAZZ_MagDrum_30_75 DisplayNamePlural]] "Бубен"),
	AdditionalHint = T(990002228, --[[ModItemInventoryItemCompositeDef JAZZ_MagDrum_30_75 AdditionalHint]] "Съёмный модуль. Перетащите на совместимое оружие или установите в кабинете модификации."),
	Cost = 5000,
	CanAppearInShop = true,
	RestockWeight = 10,
	MaxStock = 1,
	Tier = 1,
	CategoryPair = "Components",
	MaxStacks = 1,
	RemovableComponentId = "JAZZ_MagDrum_30_75",
})
