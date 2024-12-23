UndefineClass('JAZZ_AMMO_3006')
DefineClass.JAZZ_AMMO_3006 = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "30-06",
	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/3006.png",
	DisplayName = T(697162729896, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_3006 DisplayName]] "Патрон 30-06"),
	DisplayNamePlural = T(726631612816, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_3006 DisplayNamePlural]] "Патроны 30-06"),
	colorStyle = "AmmoBasicColor",
	Description = T(898567748151, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_3006 Description]] "Стандартный патрон калибра 30-06"),
	AdditionalHint = T(519576169841, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_3006 AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Обеспечивает уверенное поражение целей обладающих 3-м классом брони"),
	Cost = 100,
	CanAppearInShop = true,
	MaxStock = 30,
	RestockWeight = 50,
	CategoryPair = "3006",
	ShopStackSize = 30,
	MaxStacks = 40,
	Caliber = "JAZZ_Caliber_3006",
	Modifications = {
		PlaceObj('CaliberModification', {
			mod_add = 2,
			target_prop = "PenetrationClass",
		}),
	},
}

