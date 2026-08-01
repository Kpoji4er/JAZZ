UndefineClass('JAZZ_MagDrum_30_100')
DefineClass("JAZZ_MagDrum_30_100", {
	__parents = { "JAZZ_RemovableAttachment" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",

	object_class = "JAZZ_RemovableAttachment",
	Repairable = false,
	Icon = "UI/Icons/Upgrades/expanded_drum_G36_magazine",
	DisplayName = T(990002217, --[[ModItemInventoryItemCompositeDef JAZZ_MagDrum_30_100 DisplayName]] "Бубен"),
	DisplayNamePlural = T(990002218, --[[ModItemInventoryItemCompositeDef JAZZ_MagDrum_30_100 DisplayNamePlural]] "Бубен"),
	AdditionalHint = T(990002219, --[[ModItemInventoryItemCompositeDef JAZZ_MagDrum_30_100 AdditionalHint]] "Съёмный модуль. Перетащите на совместимое оружие или установите в кабинете модификации."),
	Cost = 5000,
	CanAppearInShop = true,
	RestockWeight = 10,
	MaxStock = 1,
	Tier = 1,
	CategoryPair = "Components",
	MaxStacks = 1,
	RemovableComponentId = "JAZZ_MagDrum_30_100",
})
