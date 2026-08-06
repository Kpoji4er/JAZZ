UndefineClass('CustomPDA')
DefineClass.CustomPDA = {
	__parents = { "ToolItem" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "ToolItem",
	CanAppearInShop = false,
	Repairable = false,
	Icon = "UI/Icons/Items/custom_pda",
	DisplayName = T(396025298894, --[[ModItemInventoryItemCompositeDef CustomPDA DisplayName]] "Livewire's PDA"),
	DisplayNamePlural = T(170324531997, --[[ModItemInventoryItemCompositeDef CustomPDA DisplayNamePlural]] "Livewire's PDAs"),
	Description = T(405152148318, --[[ModItemInventoryItemCompositeDef CustomPDA Description]] "Useful for accessing the web and hacking military grade computers."),
	AdditionalHint = T(910763517564, --[[ModItemInventoryItemCompositeDef CustomPDA AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Дает доп. разведданные при взломе\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> На нем очень милые наклеечки"),
	locked = true,
	RestockWeight = 0,
}

