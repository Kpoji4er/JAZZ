UndefineClass('JAZZ_AMMO_762x54_Tracer')
DefineClass.JAZZ_AMMO_762x54_Tracer = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "ЛПС, но Трассирующие",
	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/762x54RTracer.png",
	DisplayName = T(351000794380, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_762x54_Tracer DisplayName]] "7,62x54R мм Т"),
	DisplayNamePlural = T(502291306563, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_762x54_Tracer DisplayNamePlural]] "7,62x54R мм Т"),
	colorStyle = "AmmoTracerColor",
	Description = T(556350640822, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_762x54_Tracer Description]] "Советский трассирующий винтовочный боеприпас калибра 7.62х54мм с пулей T46"),
	AdditionalHint = T(469781530211, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_762x54_Tracer AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Обеспечивает уверенное поражение целей обладающих 3-м классом брони\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Пораженные цели получают статус «<color EmStyle>Вне укрытия</color>» и лишаются его преимуществ"),
	Cost = 280,
	CanAppearInShop = true,
	Tier = 2,
	MaxStock = 20,
	RestockWeight = 25,
	CategoryPair = "762x54",
	ShopStackSize = 30,
	MaxStacks = 5000,
	Caliber = "JAZZ_Caliber_762x54R",
	Modifications = {
		PlaceObj('CaliberModification', {
			mod_add = 2,
			target_prop = "PenetrationClass",
		}),
	},
	AppliedEffects = {
		"Exposed",
	},
}

