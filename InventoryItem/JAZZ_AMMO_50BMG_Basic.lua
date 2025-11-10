UndefineClass('JAZZ_AMMO_50BMG_Basic')
DefineClass.JAZZ_AMMO_50BMG_Basic = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ammo",
	Icon = "UI/Icons/Items/50bmg_basic",
	DisplayName = T(224747486019, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_50BMG_Basic DisplayName]] ".50, обычный"),
	DisplayNamePlural = T(272581385016, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_50BMG_Basic DisplayNamePlural]] ".50, обычные"),
	colorStyle = "AmmoBasicColor",
	Description = T(928449338739, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_50BMG_Basic Description]] "Обычный натовский палтишок, убивает гарантированно, но не всё, если не убивает, то делает очень больно."),
	Cost = 9000,
	CanAppearInShop = true,
	Tier = 3,
	MaxStock = 10,
	RestockWeight = 1,
	CategoryPair = "50BMG",
	ShopStackSize = 5,
	Caliber = "JAZZ_Caliber_50BMG",
	Modifications = {
		PlaceObj('CaliberModification', {
			mod_mul = 3000,
			target_prop = "PenetrationClass",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 5,
			target_prop = "PenetrationBonus",
		}),
	},
}

