UndefineClass('JAZZ_AMMO_45ACP_FMJ')
DefineClass.JAZZ_AMMO_45ACP_FMJ = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/45ACP.png",
	DisplayName = T(890000000000237, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_45ACP_FMJ DisplayName]] ".45ACP, FMJ"),
	DisplayNamePlural = T(890000000000052, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_45ACP_FMJ DisplayNamePlural]] ".45ACP, FMJ"),
	colorStyle = "AmmoBasicColor",
	Description = T(890000000000859, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_45ACP_FMJ Description]] "Базовый армейский патрон калибра .45, против брони он бессилен, зато способен нанести огромный урон, по мерка пистолетов. Это база."),
	AdditionalHint = "",
	Cost = 450,
	CanAppearInShop = true,
	Tier = 1,
	MaxStock = 8,
	RestockWeight = 100,
	CategoryPair = "45ACP",
	ShopStackSize = 50,
	MaxStacks = 80,
	Caliber = "JAZZ_Caliber_45ACP",
	Modifications = {
		PlaceObj('CaliberModification', {
			target_prop = "PenetrationClass",
		}),
		PlaceObj('CaliberModification', {
			mod_add = -1,
			target_prop = "PenetrationBonus",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 10,
			target_prop = "CritChance",
		}),
	},
}

