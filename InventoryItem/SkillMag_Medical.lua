UndefineClass('SkillMag_Medical')
DefineClass.SkillMag_Medical = {
	__parents = { "MiscItem" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "MiscItem",
	Repairable = false,
	Icon = "UI/Icons/Items/mag_national_paramedic",
	DisplayName = T(843836306167, --[[ModItemInventoryItemCompositeDef SkillMag_Medical DisplayName]] "National Paramedic"),
	DisplayNamePlural = T(324921685110, --[[ModItemInventoryItemCompositeDef SkillMag_Medical DisplayNamePlural]] "National Paramedic"),
	Description = T(526556854684, --[[ModItemInventoryItemCompositeDef SkillMag_Medical Description]] "90+ beats to which you can perform CPR."),
	AdditionalHint = T(438853574488, --[[ModItemInventoryItemCompositeDef SkillMag_Medical AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Используется через меню предмета\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Одноразовый предмет\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Повышает навык «Медицина»"),
	UnitStat = "Medical",
	Valuable = 1,
	Cost = 1500,
	CanAppearInShop = true,
	Tier = 1,
	MaxStock = 1,
	RestockWeight = 10,
	effect_moment = "on_use",
	Effects = {
		PlaceObj('UnitStatBoost', {
			Amount = 1,
			Stat = "Medical",
		}),
	},
	action_name = T(889884758137, --[[ModItemInventoryItemCompositeDef SkillMag_Medical action_name]] "READ"),
	destroy_item = true,
}

