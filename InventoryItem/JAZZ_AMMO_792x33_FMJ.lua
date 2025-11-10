UndefineClass('JAZZ_AMMO_792x33_FMJ')
DefineClass.JAZZ_AMMO_792x33_FMJ = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ammo",
	RepairCost = 400,
	Icon = "Mod/e6L4ECj/Ammopics/792x33.png",
	DisplayName = T(333321938927, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_792x33_FMJ DisplayName]] "792x33мм Pist. Patr. 43 Ball"),
	DisplayNamePlural = T(789710016757, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_792x33_FMJ DisplayNamePlural]] "792x33мм Pist. Patr. 43 Ball"),
	colorStyle = "AmmoBasicColor",
	Description = T(527669776671, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_792x33_FMJ Description]] "Исторический боевой патрон - массовый в своё время, сейчас встречается в коллекциях и специализированном применении. Надёжен, но устарел по современным меркам."),
	AdditionalHint = "",
	Cost = 600,
	CanAppearInShop = true,
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
			mod_mul = 0,
			target_prop = "PenetrationBonus",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 5,
			target_prop = "CritChance",
		}),
	},
}

