UndefineClass('SkillMag_Explosives')
DefineClass.SkillMag_Explosives = {
	__parents = { "MiscItem" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "MiscItem",
	Repairable = false,
	Icon = "UI/Icons/Items/mag_the_red_wire",
	DisplayName = T(200077030182, --[[ModItemInventoryItemCompositeDef SkillMag_Explosives DisplayName]] "The Red Wire"),
	DisplayNamePlural = T(698234423645, --[[ModItemInventoryItemCompositeDef SkillMag_Explosives DisplayNamePlural]] "The Red Wire"),
	Description = T(267053043531, --[[ModItemInventoryItemCompositeDef SkillMag_Explosives Description]] "Recently blew up after several issues."),
	AdditionalHint = T(981774563552, --[[ModItemInventoryItemCompositeDef SkillMag_Explosives AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Используется через меню предмета\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Одноразовый предмет\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Повышает навык «Взрывчатка»"),
	UnitStat = "Explosives",
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
			Stat = "Explosives",
		}),
	},
	action_name = T(259798743067, --[[ModItemInventoryItemCompositeDef SkillMag_Explosives action_name]] "READ"),
	destroy_item = true,
}

