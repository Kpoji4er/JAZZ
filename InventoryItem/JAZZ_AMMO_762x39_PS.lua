UndefineClass('JAZZ_AMMO_762x39_PS')
DefineClass.JAZZ_AMMO_762x39_PS = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "ПС - Армейские. В основном у бобби рея",
	object_class = "Ammo",
	RepairCost = 400,
	Icon = "Mod/e6L4ECj/Ammopics/762x39PS.png",
	DisplayName = T(333321938927, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_762x39_PS DisplayName]] "7,62х39мм, ПС"),
	DisplayNamePlural = T(789710016757, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_762x39_PS DisplayNamePlural]] "7,62х39мм, ПС"),
	colorStyle = "AmmoGreenColor",
	Description = T(527669776671, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_762x39_PS Description]] "Стандартный советский армейский патрон ПС калибра 7.62х39мм"),
	AdditionalHint = T(253050921629, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_762x39_PS AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Обеспечивает уверенное поражение целей обладающих 3-м классом брони"),
	Cost = 300,
	CanAppearInShop = true,
	Tier = 3,
	MaxStock = 10,
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
}

