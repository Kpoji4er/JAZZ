UndefineClass('JAZZ_MagDrum_30_50_UZI')
DefineClass("JAZZ_MagDrum_30_50_UZI", {
	__parents = { "JAZZ_RemovableAttachment" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",

	object_class = "JAZZ_RemovableAttachment",
	Repairable = false,
	Icon = "UI/Icons/Upgrades/galil_magazine_large",
	DisplayName = T(990002529, --[[ModItemInventoryItemCompositeDef JAZZ_MagDrum_30_50_UZI DisplayName]] "Бубен"),
	DisplayNamePlural = T(990002530, --[[ModItemInventoryItemCompositeDef JAZZ_MagDrum_30_50_UZI DisplayNamePlural]] "Бубен"),
	AdditionalHint = T(990002531, --[[ModItemInventoryItemCompositeDef JAZZ_MagDrum_30_50_UZI AdditionalHint]] "Семья магазинов: UZI. Съёмный модуль. Перетащите на совместимое оружие или установите в кабинете модификации."),
	Cost = 5000,
	CanAppearInShop = true,
	RestockWeight = 10,
	MaxStock = 1,
	Tier = 1,
	CategoryPair = "Components",
	MaxStacks = 1,
	RemovableComponentId = "JAZZ_MagDrum_30_50_UZI",
})
