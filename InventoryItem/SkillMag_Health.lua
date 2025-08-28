UndefineClass('SkillMag_Health')
DefineClass.SkillMag_Health = {
	__parents = { "MiscItem" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "MiscItem",
	Repairable = false,
	Icon = "UI/Icons/Items/mag_an_apple_a_day",
	DisplayName = T(524361455045, "Здоровое питание"),
	DisplayNamePlural = T(865014145428, "Здоровое питание"),
	Description = T(169052184605, "На зависть всем врачам."),
	AdditionalHint = T(617196311086, "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Используется через меню предмета\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Одноразовый предмет\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Повышает здоровье"),
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
	action_name = T(459203597656, "ЧИТАТЬ"),
	destroy_item = true,
}

