UndefineClass('JAZZ_AMMO_44CAL_FMJ')
DefineClass.JAZZ_AMMO_44CAL_FMJ = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/44FMJ.png",
	DisplayName = T(283758588700, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_44CAL_FMJ DisplayName]] ".44, FMJ"),
	DisplayNamePlural = T(124552577193, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_44CAL_FMJ DisplayNamePlural]] ".44, FMJ"),
	colorStyle = "AmmoBasicColor",
	Description = T(472698757891, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_44CAL_FMJ Description]] "Это Магнум, он не нуждается в представлении, им можно даже не попадать, все итак поймут кто тут папа."),
	AdditionalHint = "",
	Cost = 972,
	CanAppearInShop = true,
	MaxStock = 50,
	RestockWeight = 10,
	CategoryPair = "44CAL",
	ShopStackSize = 25,
	MaxStacks = 80,
	Caliber = "JAZZ_Caliber_44CAL",
	Modifications = {
		PlaceObj('CaliberModification', {
			target_prop = "PenetrationClass",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 5,
			target_prop = "PenetrationBonus",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 10,
			target_prop = "CritChance",
		}),
	},
}

