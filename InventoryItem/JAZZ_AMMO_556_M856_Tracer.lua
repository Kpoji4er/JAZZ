UndefineClass('JAZZ_AMMO_556_M856_Tracer')
DefineClass.JAZZ_AMMO_556_M856_Tracer = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "Как M855 но трассера",
	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/556T.png",
	DisplayName = T(653808281542, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_556_M856_Tracer DisplayName]] "5,56 мм, M856"),
	DisplayNamePlural = T(493478127524, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_556_M856_Tracer DisplayNamePlural]] "5,56 мм, M856"),
	colorStyle = "AmmoTracerColor",
	Description = T(270211830133, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_556_M856_Tracer Description]] "Современный армейский трассирующий патрон калибра 5.56x45мм."),
	AdditionalHint = T(858940983513, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_556_M856_Tracer AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Обеспечивает уверенное поражение целей обладающих 3-м классом брони\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Пораженные цели получают статус «<color EmStyle>Вне укрытия</color>» и лишаются его преимуществ"),
	Cost = 500,
	CanAppearInShop = true,
	Tier = 2,
	RestockWeight = 25,
	CategoryPair = "556",
	ShopStackSize = 30,
	MaxStacks = 90,
	Caliber = "JAZZ_Caliber_556",
	Modifications = {
		PlaceObj('CaliberModification', {
			mod_add = 3,
			target_prop = "PenetrationClass",
		}),
	},
	AppliedEffects = {
		"Exposed",
	},
	ammo_type_icon = "UI/Icons/Items/ta_tracer.png",
}

