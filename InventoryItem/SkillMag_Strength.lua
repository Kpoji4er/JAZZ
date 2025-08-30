UndefineClass('SkillMag_Strength')
DefineClass.SkillMag_Strength = {
	__parents = { "MiscItem" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "MiscItem",
	Repairable = false,
	Icon = "UI/Icons/Items/mag_flex_em",
	DisplayName = T(906939250168, --[[ModItemInventoryItemCompositeDef SkillMag_Strength DisplayName]] "Качай железо!"),
	DisplayNamePlural = T(561764144197, --[[ModItemInventoryItemCompositeDef SkillMag_Strength DisplayNamePlural]] "Качай железо!"),
	Description = T(952959192834, --[[ModItemInventoryItemCompositeDef SkillMag_Strength Description]] "Сила есть - интеллекта не надо."),
	AdditionalHint = T(970224447052, --[[ModItemInventoryItemCompositeDef SkillMag_Strength AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Используется через меню предмета\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Одноразовый предмет\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Повышает силу"),
	UnitStat = "Strength",
	Valuable = 1,
	Cost = 1500,
	CanAppearInShop = true,
	MaxStock = 1,
	RestockWeight = 10,
	effect_moment = "on_use",
	Effects = {
		PlaceObj('UnitStatBoost', {
			Amount = 1,
			Stat = "Strength",
		}),
	},
	action_name = T(562074647455, --[[ModItemInventoryItemCompositeDef SkillMag_Strength action_name]] "ЧИТАТЬ"),
	destroy_item = true,
}

