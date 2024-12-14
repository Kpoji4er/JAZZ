UndefineClass('JAZZ_AMMO_762x51_M80')
DefineClass.JAZZ_AMMO_762x51_M80 = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "М80 - Армейские.",
	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/762NATOM80.png",
	DisplayName = T(155135485934, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_762x51_M80 DisplayName]] "7.62х51мм НАТО, M80"),
	DisplayNamePlural = T(688496678363, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_762x51_M80 DisplayNamePlural]] "7.62х51мм НАТО, M80"),
	colorStyle = "AmmoGreenColor",
	Description = T(296800783973, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_762x51_M80 Description]] "Стандартный армейский патрон М80 калибра 7.62х51мм НАТО"),
	AdditionalHint = T(623835325820, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_762x51_M80 AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Обеспечивает уверенное поражение целей обладающих 3-м классом брони"),
	Cost = 100,
	CanAppearInShop = true,
	Tier = 2,
	MaxStock = 30,
	RestockWeight = 50,
	CategoryPair = "762NATO",
	ShopStackSize = 30,
	MaxStacks = 5000,
	Caliber = "JAZZ_Caliber_762x51",
	Modifications = {
		PlaceObj('CaliberModification', {
			mod_add = 2,
			target_prop = "PenetrationClass",
		}),
	},
}

