UndefineClass('SkillMag_Mechanical')
DefineClass.SkillMag_Mechanical = {
	__parents = { "MiscItem" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "MiscItem",
	Repairable = false,
	Icon = "UI/Icons/Items/mag_screw_you",
	DisplayName = T(593394887790, --[[ModItemInventoryItemCompositeDef SkillMag_Mechanical DisplayName]] "Nuts and Bolts Magazine"),
	DisplayNamePlural = T(115283650556, --[[ModItemInventoryItemCompositeDef SkillMag_Mechanical DisplayNamePlural]] "Nuts and Bolts Magazine"),
	Description = T(882249328783, --[[ModItemInventoryItemCompositeDef SkillMag_Mechanical Description]] "Not to be confused with the NSFW magazine with the same name."),
	AdditionalHint = T(311674409919, --[[ModItemInventoryItemCompositeDef SkillMag_Mechanical AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Используется через меню предмета\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Одноразовый предмет\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Повышает навык «Механика»"),
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
	action_name = T(196171082016, --[[ModItemInventoryItemCompositeDef SkillMag_Mechanical action_name]] "READ"),
	destroy_item = true,
}

