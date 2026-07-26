UndefineClass('SkillMag_Dexterity')
DefineClass.SkillMag_Dexterity = {
	__parents = { "MiscItem" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "MiscItem",
	Repairable = false,
	Icon = "UI/Icons/Items/mag_sleight_of_hand",
	DisplayName = T(742728199089, --[[ModItemInventoryItemCompositeDef SkillMag_Dexterity DisplayName]] "Sleight of Hand"),
	DisplayNamePlural = T(201148125710, --[[ModItemInventoryItemCompositeDef SkillMag_Dexterity DisplayNamePlural]] "Sleight of Hand"),
	Description = T(469561072760, --[[ModItemInventoryItemCompositeDef SkillMag_Dexterity Description]] "Much better read than Daily Prestidigitation."),
	AdditionalHint = T(430709598633, --[[ModItemInventoryItemCompositeDef SkillMag_Dexterity AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Используется через меню предмета\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Одноразовый предмет\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Повышает ловкость"),
	UnitStat = "Dexterity",
	Valuable = 1,
	Cost = 1500,
	CanAppearInShop = true,
	MaxStock = 1,
	RestockWeight = 10,
	effect_moment = "on_use",
	Effects = {
		PlaceObj('UnitStatBoost', {
			Amount = 1,
			Stat = "Dexterity",
		}),
	},
	action_name = T(161343355015, --[[ModItemInventoryItemCompositeDef SkillMag_Dexterity action_name]] "READ"),
	destroy_item = true,
}

