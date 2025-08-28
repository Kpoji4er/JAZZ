UndefineClass('SkillMag_Mechanical')
DefineClass.SkillMag_Mechanical = {
	__parents = { "MiscItem" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "MiscItem",
	Repairable = false,
	Icon = "UI/Icons/Items/mag_screw_you",
	DisplayName = T(481761492155, "Поршни и цилиндры"),
	DisplayNamePlural = T(937997865248, "Поршни и цилиндры"),
	Description = T(780424103597, "Не путать с одноимённым журналом 18+."),
	AdditionalHint = T(311674409919, "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Используется через меню предмета\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Одноразовый предмет\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Повышает навык «Механика»"),
	UnitStat = "Mechanical",
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
			Stat = "Mechanical",
		}),
	},
	action_name = T(421574848456, "ЧИТАТЬ"),
	destroy_item = true,
}

