UndefineClass('SkillMag_Marksmanship')
DefineClass.SkillMag_Marksmanship = {
	__parents = { "MiscItem" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "MiscItem",
	Repairable = false,
	Icon = "UI/Icons/Items/mag_long_distance_relations",
	DisplayName = T(262432851703, --[[ModItemInventoryItemCompositeDef SkillMag_Marksmanship DisplayName]] "Long Distance Relations"),
	DisplayNamePlural = T(130303695300, --[[ModItemInventoryItemCompositeDef SkillMag_Marksmanship DisplayNamePlural]] "Long Distance Relations"),
	Description = T(658693817283, --[[ModItemInventoryItemCompositeDef SkillMag_Marksmanship Description]] "The articles really hit the mark."),
	AdditionalHint = T(690633844355, --[[ModItemInventoryItemCompositeDef SkillMag_Marksmanship AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Используется через меню предмета\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Одноразовый предмет\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Повышает меткость"),
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
	action_name = T(889536988208, --[[ModItemInventoryItemCompositeDef SkillMag_Marksmanship action_name]] "READ"),
	destroy_item = true,
}

