UndefineClass('JAZZ_MagDrum_30_100_G3')
DefineClass("JAZZ_MagDrum_30_100_G3", {
	__parents = { "JAZZ_RemovableAttachment" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",

	object_class = "JAZZ_RemovableAttachment",
	Repairable = false,
	Icon = "UI/Icons/Upgrades/galil_magazine_large",
	DisplayName = T(990002520, --[[ModItemInventoryItemCompositeDef JAZZ_MagDrum_30_100_G3 DisplayName]] "Бубен"),
	DisplayNamePlural = T(990002521, --[[ModItemInventoryItemCompositeDef JAZZ_MagDrum_30_100_G3 DisplayNamePlural]] "Бубен"),
	AdditionalHint = T(990002522, --[[ModItemInventoryItemCompositeDef JAZZ_MagDrum_30_100_G3 AdditionalHint]] "Семья магазинов: G3. Съёмный модуль. Перетащите на совместимое оружие или установите в кабинете модификации."),
	Cost = 5000,
	CanAppearInShop = true,
	RestockWeight = 10,
	MaxStock = 1,
	Tier = 1,
	CategoryPair = "Components",
	MaxStacks = 1,
	RemovableComponentId = "JAZZ_MagDrum_30_100_G3",
})
