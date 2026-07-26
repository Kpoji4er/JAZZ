UndefineClass('Microchip')
DefineClass.Microchip = {
	__parents = { "MiscItem" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "MiscItem",
	Icon = "UI/Icons/Items/microchip",
	DisplayName = T(176640963638, --[[ModItemInventoryItemCompositeDef Microchip DisplayName]] "Chip"),
	DisplayNamePlural = T(767899744987, --[[ModItemInventoryItemCompositeDef Microchip DisplayNamePlural]] "Chips"),
	AdditionalHint = T(859152016185, --[[ModItemInventoryItemCompositeDef Microchip AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Используется при создании улучшенных компонентов для оружия"),
	Valuable = 1,
	Cost = 4900,
	CanAppearInShop = true,
	Tier = 3,
	MaxStock = 1,
	RestockWeight = 15,
	CategoryPair = "Components",
	MaxStacks = 500,
}

