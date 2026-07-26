UndefineClass('SkillMag_Strength')
DefineClass.SkillMag_Strength = {
	__parents = { "MiscItem" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "MiscItem",
	Repairable = false,
	Icon = "UI/Icons/Items/mag_flex_em",
	DisplayName = T(949216271403, --[[ModItemInventoryItemCompositeDef SkillMag_Strength DisplayName]] "Flex 'em!"),
	DisplayNamePlural = T(246425010309, --[[ModItemInventoryItemCompositeDef SkillMag_Strength DisplayNamePlural]] "Flex 'em!"),
	Description = T(817037902641, --[[ModItemInventoryItemCompositeDef SkillMag_Strength Description]] "For bros who even lift."),
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
	action_name = T(919614237926, --[[ModItemInventoryItemCompositeDef SkillMag_Strength action_name]] "READ"),
	destroy_item = true,
}

