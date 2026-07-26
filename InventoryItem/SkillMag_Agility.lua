UndefineClass('SkillMag_Agility')
DefineClass.SkillMag_Agility = {
	__parents = { "MiscItem" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "MiscItem",
	Repairable = false,
	Icon = "UI/Icons/Items/mag_parkour",
	DisplayName = T(429725650602, --[[ModItemInventoryItemCompositeDef SkillMag_Agility DisplayName]] "Parkour!"),
	DisplayNamePlural = T(183969949257, --[[ModItemInventoryItemCompositeDef SkillMag_Agility DisplayNamePlural]] "Parkour!"),
	Description = T(151166074388, --[[ModItemInventoryItemCompositeDef SkillMag_Agility Description]] "«Я почти уверен, что кричать <color EmStyle>«Паркур»</color> не обязательно»."),
	AdditionalHint = T(653157983531, --[[ModItemInventoryItemCompositeDef SkillMag_Agility AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Используется через меню предмета\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Одноразовый предмет\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Повышает проворность"),
	UnitStat = "Agility",
	Valuable = 1,
	Cost = 1500,
	CanAppearInShop = true,
	MaxStock = 1,
	RestockWeight = 10,
	effect_moment = "on_use",
	Effects = {
		PlaceObj('UnitStatBoost', {
			Amount = 1,
			Stat = "Agility",
		}),
	},
	action_name = T(966696056779, --[[ModItemInventoryItemCompositeDef SkillMag_Agility action_name]] "READ"),
	destroy_item = true,
}

