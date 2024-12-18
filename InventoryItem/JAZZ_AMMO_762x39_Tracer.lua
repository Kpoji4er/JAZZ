UndefineClass('JAZZ_AMMO_762x39_Tracer')
DefineClass.JAZZ_AMMO_762x39_Tracer = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "Как ПС, но трассера",
	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/762x39T.png",
	DisplayName = T(798317989173, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_762x39_Tracer DisplayName]] "7,62 мм СССР, ТРАС"),
	DisplayNamePlural = T(300974076449, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_762x39_Tracer DisplayNamePlural]] "7,62 мм СССР, ТРАС"),
	colorStyle = "AmmoTracerColor",
	Description = T(105546400626, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_762x39_Tracer Description]] "Трасирующий советский армейский патрон Т-45 калибра 7.62х39мм"),
	AdditionalHint = T(345979521367, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_762x39_Tracer AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Обеспечивает уверенное поражение целей обладающих 3-м классом брони\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Пораженные цели получают статус «<color EmStyle>Вне укрытия</color>» и лишаются его преимуществ"),
	Cost = 400,
	CanAppearInShop = true,
	Tier = 2,
	MaxStock = 2,
	RestockWeight = 25,
	CategoryPair = "762WP",
	ShopStackSize = 30,
	MaxStacks = 60,
	Caliber = "JAZZ_Caliber_762x39",
	Modifications = {
		PlaceObj('CaliberModification', {
			mod_add = 2,
			target_prop = "PenetrationClass",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 1,
			target_prop = "BulletDropRange",
		}),
	},
	AppliedEffects = {
		"Exposed",
	},
	ammo_type_icon = "UI/Icons/Items/ta_tracer.png",
}

