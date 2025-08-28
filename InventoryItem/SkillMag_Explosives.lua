UndefineClass('SkillMag_Explosives')
DefineClass.SkillMag_Explosives = {
	__parents = { "MiscItem" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "MiscItem",
	Repairable = false,
	Icon = "UI/Icons/Items/mag_the_red_wire",
	DisplayName = T(989274794141, "Красный провод"),
	DisplayNamePlural = T(357987311564, "Красный провод"),
	Description = T(643007081984, "Говорят, издательство недавно сгорело на работе."),
	AdditionalHint = T(981774563552, "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Используется через меню предмета\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Одноразовый предмет\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Повышает навык «Взрывчатка»"),
	UnitStat = "Explosives",
	Valuable = 1,
	Cost = 1500,
	CanAppearInShop = true,
	Tier = 2,
	MaxStock = 1,
	RestockWeight = 10,
	effect_moment = "on_use",
	Effects = {
		PlaceObj('UnitStatBoost', {
			Amount = 1,
			Stat = "Explosives",
		}),
	},
	action_name = T(759449615314, "ЧИТАТЬ"),
	destroy_item = true,
}

