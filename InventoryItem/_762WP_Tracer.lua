UndefineClass('_762WP_Tracer')
DefineClass._762WP_Tracer = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "Как ПС, но трассера",
	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/TEST.png",
	DisplayName = T(731781267010, --[[ModItemInventoryItemCompositeDef _762WP_Tracer DisplayName]] "7.62 mm WP Tracer"),
	DisplayNamePlural = T(277651293338, --[[ModItemInventoryItemCompositeDef _762WP_Tracer DisplayNamePlural]] "7.62 mm WP Tracer"),
	colorStyle = "AmmoTracerColor",
	Description = T(888848136617, --[[ModItemInventoryItemCompositeDef _762WP_Tracer Description]] "Трасирующий советский армейский патрон Т-45 калибра 7.62х39мм"),
	AdditionalHint = T(207401264401, --[[ModItemInventoryItemCompositeDef _762WP_Tracer AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Обеспечивает уверенное поражение целей обладающих 3-м классом брони\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Пораженные цели получают статус «<color EmStyle>Вне укрытия</color>» и лишаются его преимуществ"),
	Cost = 400,
	Tier = 2,
	MaxStock = 2,
	RestockWeight = 25,
	CategoryPair = "762WP",
	ShopStackSize = 30,
	MaxStacks = 5000,
	Caliber = "762WP",
	Modifications = {
		PlaceObj('CaliberModification', {
			mod_add = 2,
			target_prop = "PenetrationClass",
		}),
	},
	AppliedEffects = {
		"Exposed",
	},
	ammo_type_icon = "UI/Icons/Items/ta_tracer.png",
}

