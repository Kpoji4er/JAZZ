UndefineClass('OpticalLens')
DefineClass.OpticalLens = {
	__parents = { "MiscItem" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "MiscItem",
	Icon = "UI/Icons/Items/optical_lens",
	DisplayName = T(894385255221, --[[ModItemInventoryItemCompositeDef OpticalLens DisplayName]] "Lens"),
	DisplayNamePlural = T(339259119696, --[[ModItemInventoryItemCompositeDef OpticalLens DisplayNamePlural]] "Lenses"),
	AdditionalHint = T(421377090006, --[[ModItemInventoryItemCompositeDef OpticalLens AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Используется при создании улучшенных компонентов для оружия"),
	Cost = 3400,
	CanAppearInShop = false,
	Tier = 2,
	MaxStock = 1,
	RestockWeight = 15,
	CategoryPair = "Components",
	MaxStacks = 500,
}

