UndefineClass('Microchip')
DefineClass.Microchip = {
	__parents = { "MiscItem" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "MiscItem",
	Icon = "UI/Icons/Items/microchip",
	DisplayName = T(171241193345, "Чип"),
	DisplayNamePlural = T(722836023605, "Чипы"),
	AdditionalHint = T(859152016185, "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Используется при создании улучшенных компонентов для оружия"),
	Valuable = 1,
	Cost = 4900,
	CanAppearInShop = true,
	Tier = 3,
	MaxStock = 1,
	RestockWeight = 15,
	CategoryPair = "Components",
	MaxStacks = 500,
}

