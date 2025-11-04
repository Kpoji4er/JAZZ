UndefineClass('SkillMag_Dexterity')
DefineClass.SkillMag_Dexterity = {
	__parents = { "MiscItem" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "MiscItem",
	Repairable = false,
	Icon = "UI/Icons/Items/mag_sleight_of_hand",
	DisplayName = T(546644843752, "Легкость рук"),
	DisplayNamePlural = T(721718349706, "Легкость рук"),
	Description = T(783661118476, "Гораздо интереснее «Ежедневных фокусов»."),
	AdditionalHint = T(430709598633, "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Используется через меню предмета\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Одноразовый предмет\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Повышает ловкость"),
	UnitStat = "Dexterity",
	Valuable = 1,
	Cost = 1500,
	CanAppearInShop = true,
	MaxStock = 1,
	RestockWeight = 10,
	effect_moment = "on_use",
	Effects = {
		PlaceObj('UnitStatBoost', {
			Amount = 1,
			Stat = "Dexterity",
		}),
	},
	action_name = T(501093218367, "ЧИТАТЬ"),
	destroy_item = true,
}

