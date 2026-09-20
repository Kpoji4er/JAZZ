UndefineClass('JAZZ_MagNormalFine_FAL')
DefineClass.JAZZ_MagNormalFine_FAL = {
	__parents = { "JAZZ_RemovableAttachment" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "WEAPONS-002 remountable → component JAZZ_MagNormalFine_FAL",
	object_class = "JAZZ_RemovableAttachment",
	Icon = "UI/Icons/Upgrades/fnfal_mag_ergo_normal",
	DisplayName = T(990002589, --[[ModItemInventoryItemCompositeDef JAZZ_MagNormalFine_FAL DisplayName]] "Fine-Tuned Mag"),
	DisplayNamePlural = T(990002590, --[[ModItemInventoryItemCompositeDef JAZZ_MagNormalFine_FAL DisplayNamePlural]] "Fine-Tuned Mag"),
	AdditionalHint = T(990002591, --[[ModItemInventoryItemCompositeDef JAZZ_MagNormalFine_FAL AdditionalHint]] "Семья магазинов: FAL. Съёмный модуль. Перетащите на совместимое оружие или установите в кабинете модификации."),
	Cost = 1500,
	CanAppearInShop = true,
	Tier = 3,
	MaxStock = 1,
	RestockWeight = 18,
	CategoryPair = "Magazines",
}

