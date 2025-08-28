UndefineClass('SkillMag_Leadership')
DefineClass.SkillMag_Leadership = {
	__parents = { "MiscItem" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "MiscItem",
	Repairable = false,
	Icon = "UI/Icons/Items/mag_puntastic_dad_jokes",
	DisplayName = T(337969805989, "Шутки-самосмейки"),
	DisplayNamePlural = T(761905965424, "Шутки-самосмейки"),
	Description = T(251292542025, "Как стать душой частной военной компании."),
	AdditionalHint = T(575413455352, "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Используется через меню предмета\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Одноразовый предмет\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Повышает лидерство"),
	UnitStat = "Leadership",
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
			Stat = "Leadership",
		}),
	},
	action_name = T(406257852737, "ЧИТАТЬ"),
	destroy_item = true,
}

