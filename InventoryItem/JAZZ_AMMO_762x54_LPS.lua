UndefineClass('JAZZ_AMMO_762x54_LPS')
DefineClass.JAZZ_AMMO_762x54_LPS = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "ЛПС - Основной патрон у легиона",
	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/762x54RLPS.png",
	DisplayName = T(685074706095, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_762x54_LPS DisplayName]] "7,62x54R мм ЛПС"),
	DisplayNamePlural = T(544176135141, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_762x54_LPS DisplayNamePlural]] "7,62x54R мм ЛПС"),
	colorStyle = "AmmoBasicColor",
	Description = T(316044940928, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_762x54_LPS Description]] "Советский винтовочный боеприпас калибра 7.62х54мм с пулей ЛПС"),
	AdditionalHint = T(382555567328, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_762x54_LPS AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Обеспечивает уверенное поражение целей обладающих 3-м классом брони"),
	Cost = 240,
	CanAppearInShop = true,
	Tier = 2,
	MaxStock = 5,
	CategoryPair = "762x54",
	ShopStackSize = 30,
	MaxStacks = 40,
	Caliber = "JAZZ_Caliber_762x54R",
	Modifications = {
		PlaceObj('CaliberModification', {
			mod_add = 2,
			target_prop = "PenetrationClass",
		}),
		PlaceObj('CaliberModification', {
			mod_mul = 900,
			target_prop = "Damage",
		}),
	},
}

