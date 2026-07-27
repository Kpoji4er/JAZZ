UndefineClass('SkillMag_Health')
DefineClass.SkillMag_Health = {
	__parents = { "MiscItem" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "MiscItem",
	Repairable = false,
	Icon = "UI/Icons/Items/mag_an_apple_a_day",
	DisplayName = T(890000000001482, --[[ModItemInventoryItemCompositeDef SkillMag_Health DisplayName]] "An Apple a Day"),
	DisplayNamePlural = T(890000000001502, --[[ModItemInventoryItemCompositeDef SkillMag_Health DisplayNamePlural]] "An Apple a Day"),
	Description = T(862144835554, --[[ModItemInventoryItemCompositeDef SkillMag_Health Description]] "Doctors really hate this one simple trick."),
	AdditionalHint = T(617196311086, --[[ModItemInventoryItemCompositeDef SkillMag_Health AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Используется через меню предмета\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Одноразовый предмет\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Повышает здоровье"),
	UnitStat = "Health",
	Valuable = 1,
	Cost = 1500,
	CanAppearInShop = true,
	MaxStock = 1,
	RestockWeight = 10,
	effect_moment = "on_use",
	Effects = {
		PlaceObj('UnitStatBoost', {
			Amount = 1,
			Stat = "Health",
		}),
	},
	action_name = T(499509380474, --[[ModItemInventoryItemCompositeDef SkillMag_Health action_name]] "READ"),
	destroy_item = true,
}

