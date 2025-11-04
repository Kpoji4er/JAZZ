UndefineClass('SkillMag_Marksmanship')
DefineClass.SkillMag_Marksmanship = {
	__parents = { "MiscItem" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "MiscItem",
	Repairable = false,
	Icon = "UI/Icons/Items/mag_long_distance_relations",
	DisplayName = T(805457297063, "Начинать надо издалека"),
	DisplayNamePlural = T(905685178126, "Начинать надо издалека"),
	Description = T(630599705437, "«Братишка, ты лучше сядь»."),
	AdditionalHint = T(690633844355, "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Используется через меню предмета\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Одноразовый предмет\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Повышает меткость"),
	UnitStat = "Marksmanship",
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
			Stat = "Marksmanship",
		}),
	},
	action_name = T(475947315094, "ЧИТАТЬ"),
	destroy_item = true,
}

