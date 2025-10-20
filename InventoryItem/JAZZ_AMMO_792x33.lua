UndefineClass('JAZZ_AMMO_792x33')
DefineClass.JAZZ_AMMO_792x33 = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ammo",
	RepairCost = 400,
	Icon = "Mod/e6L4ECj/Ammopics/792x33.png",
	DisplayName = T(333321938927, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_792x33 DisplayName]] "792x33мм"),
	DisplayNamePlural = T(789710016757, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_792x33 DisplayNamePlural]] "792x33мм"),
	colorStyle = "AmmoGreenColor",
	Description = T(527669776671, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_792x33 Description]] "Стандартный советский армейский патрон ПС калибра 7.62х39мм"),
	AdditionalHint = T(253050921629, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_792x33 AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Обеспечивает уверенное поражение целей обладающих 2-м классом брони"),
	Cost = 300,
	CanAppearInShop = true,
	Tier = 3,
	MaxStock = 10,
	CategoryPair = "762WP",
	ShopStackSize = 30,
	MaxStacks = 60,
	Caliber = "JAZZ_Caliber_792x33",
	Modifications = {
		PlaceObj('CaliberModification', {
			mod_add = 1,
			target_prop = "PenetrationClass",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 1,
			target_prop = "BulletDropRange",
		}),
	},
}

