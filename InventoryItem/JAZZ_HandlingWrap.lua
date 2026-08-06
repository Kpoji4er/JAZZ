UndefineClass('JAZZ_HandlingWrap')
DefineClass.JAZZ_HandlingWrap = {
	__parents = { "JAZZ_RemovableAttachment" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",

	object_class = "JAZZ_RemovableAttachment",
	Repairable = false,
	Icon = "Mod/e6L4ECj/WeaponComponents/Side/Wrap.png",
	DisplayName = T(990002190, --[[ModItemInventoryItemCompositeDef JAZZ_HandlingWrap DisplayName]] "Обмотка на цевье"),
	DisplayNamePlural = T(990002191, --[[ModItemInventoryItemCompositeDef JAZZ_HandlingWrap DisplayNamePlural]] "Обмотка на цевье"),
	AdditionalHint = T(990002192, --[[ModItemInventoryItemCompositeDef JAZZ_HandlingWrap AdditionalHint]] "Съёмный модуль. Перетащите на совместимое оружие или установите в кабинете модификации."),
	Cost = 1000,
	CanAppearInShop = false,
	RestockWeight = 10,
	MaxStock = 1,
	Tier = 1,
	CategoryPair = "Components",
	MaxStacks = 1,
	RemovableComponentId = "JAZZ_HandlingWrap",
}
