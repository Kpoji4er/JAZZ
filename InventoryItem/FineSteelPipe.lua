UndefineClass('FineSteelPipe')
DefineClass.FineSteelPipe = {
	__parents = { "MiscItem" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "MiscItem",
	Repairable = false,
	Icon = "UI/Icons/Items/fine_steel_pipe",
	DisplayName = T(290395795637, --[[ModItemInventoryItemCompositeDef FineSteelPipe DisplayName]] "Steel Pipe"),
	DisplayNamePlural = T(384360336628, --[[ModItemInventoryItemCompositeDef FineSteelPipe DisplayNamePlural]] "Steel Pipes"),
	AdditionalHint = T(906442723868, --[[ModItemInventoryItemCompositeDef FineSteelPipe AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Используется при создании улучшенных компонентов для оружия"),
	Cost = 2900,
	CanAppearInShop = true,
	Tier = 2,
	MaxStock = 1,
	RestockWeight = 15,
	CategoryPair = "Components",
	MaxStacks = 500,
}

