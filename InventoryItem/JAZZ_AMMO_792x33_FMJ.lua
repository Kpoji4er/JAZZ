UndefineClass('JAZZ_AMMO_792x33_FMJ')
DefineClass.JAZZ_AMMO_792x33_FMJ = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ammo",
	RepairCost = 400,
	Icon = "Mod/e6L4ECj/Ammopics/792x33.png",
	DisplayName = T(890000000000364, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_792x33_FMJ DisplayName]] "792x33мм Pist. Patr. 43 Ball"),
	DisplayNamePlural = T(890000000001048, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_792x33_FMJ DisplayNamePlural]] "792x33мм Pist. Patr. 43 Ball"),
	colorStyle = "AmmoBasicColor",
	Description = T(890000000000660, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_792x33_FMJ Description]] "Конечно было бы не плохо сдать их в ломбард, но они ничерта не стоят, так что поливайте от души, это бесплатно. Стандартный армейский патрон."),
	AdditionalHint = "",
	Cost = 1000,
	CanAppearInShop = false,
	MaxStock = 10,
	RestockWeight = 1,
	CategoryPair = "762WP",
	ShopStackSize = 100,
	MaxStacks = 60,
	Caliber = "JAZZ_Caliber_792x33",
	Modifications = {
		PlaceObj('CaliberModification', {
			target_prop = "PenetrationClass",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 6,
			target_prop = "PenetrationBonus",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 5,
			target_prop = "CritChance",
		}),
	},
}

