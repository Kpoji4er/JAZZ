UndefineClass('Cookie')
DefineClass.Cookie = {
	__parents = { "MiscItem" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "MiscItem",
	Icon = "UI/Icons/Items/cookie",
	DisplayName = T(124351111212, --[[ModItemInventoryItemCompositeDef Cookie DisplayName]] "Biscuit"),
	DisplayNamePlural = T(982005397246, --[[ModItemInventoryItemCompositeDef Cookie DisplayNamePlural]] "Biscuits"),
	AdditionalHint = T(370231096119, --[[ModItemInventoryItemCompositeDef Cookie AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Используется через меню предмета\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Одноразовый предмет\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Вкусно и питательно"),
	CategoryPair = "Medicine",
	MaxStacks = 20,
	effect_moment = "on_use",
	Effects = {
		PlaceObj('RechargeCDs', {}),
		PlaceObj('RestoreHealth', {
			amount = 5,
		}),
	},
	action_name = T(646507120531, --[[ModItemInventoryItemCompositeDef Cookie action_name]] "EAT"),
	destroy_item = true,
}

