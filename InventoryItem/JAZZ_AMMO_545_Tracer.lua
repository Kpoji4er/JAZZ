UndefineClass('JAZZ_AMMO_545_Tracer')
DefineClass.JAZZ_AMMO_545_Tracer = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "Как ПС, но Трассера",
	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/545T.png",
	DisplayName = T(965033233630, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_545_Tracer DisplayName]] "5,45 мм, Т"),
	DisplayNamePlural = T(430326314673, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_545_Tracer DisplayNamePlural]] "5,45 мм, Т"),
	colorStyle = "AmmoTracerColor",
	Description = T(212926171807, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_545_Tracer Description]] "Трассирующий армейский патрон 7Т3 калибра 5.45x39мм"),
	AdditionalHint = T(484217681832, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_545_Tracer AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Обеспечивает уверенное поражение целей обладающих 2-м классом брони\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Пораженные цели получают статус «<color EmStyle>Вне укрытия</color>» и лишаются его преимуществ"),
	Cost = 500,
	CanAppearInShop = true,
	Tier = 3,
	MaxStock = 2,
	RestockWeight = 25,
	CategoryPair = "545",
	ShopStackSize = 30,
	MaxStacks = 5000,
	Caliber = "JAZZ_Caliber_545",
	Modifications = {
		PlaceObj('CaliberModification', {
			mod_add = 1,
			target_prop = "PenetrationClass",
		}),
	},
	AppliedEffects = {
		"Exposed",
	},
}

