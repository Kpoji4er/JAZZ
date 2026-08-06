UndefineClass('JAZZ_MagDrum_30_50')
DefineClass("JAZZ_MagDrum_30_50", {
	__parents = { "JAZZ_RemovableAttachment" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",

	object_class = "JAZZ_RemovableAttachment",
	Repairable = false,
	Icon = "Mod/e6L4ECj/magpictures/thompsondrum.png",
	DisplayName = T(990002223, --[[ModItemInventoryItemCompositeDef JAZZ_MagDrum_30_50 DisplayName]] "Бубен"),
	DisplayNamePlural = T(990002224, --[[ModItemInventoryItemCompositeDef JAZZ_MagDrum_30_50 DisplayNamePlural]] "Бубен"),
	AdditionalHint = T(990002225, --[[ModItemInventoryItemCompositeDef JAZZ_MagDrum_30_50 AdditionalHint]] "Съёмный модуль. Перетащите на совместимое оружие или установите в кабинете модификации."),
	Cost = 5000,
	CanAppearInShop = false,
	RestockWeight = 10,
	MaxStock = 1,
	Tier = 1,
	CategoryPair = "Components",
	MaxStacks = 1,
	RemovableComponentId = "JAZZ_MagDrum_30_50",
})
