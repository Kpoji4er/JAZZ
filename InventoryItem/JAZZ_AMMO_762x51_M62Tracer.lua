UndefineClass('JAZZ_AMMO_762x51_M62Tracer')
DefineClass.JAZZ_AMMO_762x51_M62Tracer = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "Как M80, но трассера",
	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/762NATOM62.png",
	DisplayName = T(170269301418, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_762x51_M62Tracer DisplayName]] "7.62х51мм НАТО, M62"),
	DisplayNamePlural = T(970505261363, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_762x51_M62Tracer DisplayNamePlural]] "7.62х51мм НАТО, M62"),
	colorStyle = "AmmoTracerColor",
	Description = T(964415083636, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_762x51_M62Tracer Description]] "Трассирующий боеприпас натовского образца для автоматов, винтовок и пулеметов калибра 7,62 мм."),
	AdditionalHint = T(978612919293, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_762x51_M62Tracer AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Пораженные цели получают статус «<color EmStyle>Вне укрытия</color>» и лишаются его преимуществ\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Обеспечивает уверенное поражение целей обладающих 3-м классом брони"),
	Cost = 200,
	CanAppearInShop = true,
	Tier = 2,
	MaxStock = 10,
	RestockWeight = 25,
	CategoryPair = "762NATO",
	ShopStackSize = 30,
	MaxStacks = 40,
	Caliber = "JAZZ_Caliber_762x51",
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

