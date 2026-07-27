UndefineClass('SkillMag_Wisdom')
DefineClass.SkillMag_Wisdom = {
	__parents = { "MiscItem" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "MiscItem",
	Repairable = false,
	Icon = "UI/Icons/Items/mag_grilled_bears_survival_guide",
	DisplayName = T(890000000001496, --[[ModItemInventoryItemCompositeDef SkillMag_Wisdom DisplayName]] "Grilled Bears' Survival Guide"),
	DisplayNamePlural = T(890000000001506, --[[ModItemInventoryItemCompositeDef SkillMag_Wisdom DisplayNamePlural]] "Grilled Bears' Survival Guide"),
	Description = T(672223422197, --[[ModItemInventoryItemCompositeDef SkillMag_Wisdom Description]] "The latest pee-based recipes for your outdoor trips."),
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
	action_name = T(887349045271, --[[ModItemInventoryItemCompositeDef SkillMag_Wisdom action_name]] "READ"),
	destroy_item = true,
}

