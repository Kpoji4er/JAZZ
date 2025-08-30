UndefineClass('SkillMag_Health')
DefineClass.SkillMag_Health = {
	__parents = { "MiscItem" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "MiscItem",
	Repairable = false,
	Icon = "UI/Icons/Items/mag_an_apple_a_day",
	DisplayName = T(524361455045, --[[ModItemInventoryItemCompositeDef SkillMag_Health DisplayName]] "Здоровое питание"),
	DisplayNamePlural = T(865014145428, --[[ModItemInventoryItemCompositeDef SkillMag_Health DisplayNamePlural]] "Здоровое питание"),
	Description = T(169052184605, --[[ModItemInventoryItemCompositeDef SkillMag_Health Description]] "На зависть всем врачам."),
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
	action_name = T(459203597656, --[[ModItemInventoryItemCompositeDef SkillMag_Health action_name]] "ЧИТАТЬ"),
	destroy_item = true,
}

