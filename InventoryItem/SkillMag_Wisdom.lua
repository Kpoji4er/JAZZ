UndefineClass('SkillMag_Wisdom')
DefineClass.SkillMag_Wisdom = {
	__parents = { "MiscItem" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "MiscItem",
	Repairable = false,
	Icon = "UI/Icons/Items/mag_grilled_bears_survival_guide",
	DisplayName = T(269425865026, --[[ModItemInventoryItemCompositeDef SkillMag_Wisdom DisplayName]] "Руководство Бори Гриля"),
	DisplayNamePlural = T(515674122433, --[[ModItemInventoryItemCompositeDef SkillMag_Wisdom DisplayNamePlural]] "Руководство Бори Гриля"),
	Description = T(526814679764, --[[ModItemInventoryItemCompositeDef SkillMag_Wisdom Description]] "Руководство по выживанию. Если вам откусил ногу медведь - пописайте на рану."),
	AdditionalHint = T(513564123523, --[[ModItemInventoryItemCompositeDef SkillMag_Wisdom AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Используется через меню предмета\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Одноразовый предмет\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Повышает интеллект"),
	UnitStat = "Wisdom",
	Valuable = 1,
	Cost = 1500,
	CanAppearInShop = true,
	MaxStock = 1,
	RestockWeight = 10,
	effect_moment = "on_use",
	Effects = {
		PlaceObj('UnitStatBoost', {
			Amount = 1,
			Stat = "Wisdom",
		}),
	},
	action_name = T(389102616843, --[[ModItemInventoryItemCompositeDef SkillMag_Wisdom action_name]] "ЧИТАТЬ"),
	destroy_item = true,
}

