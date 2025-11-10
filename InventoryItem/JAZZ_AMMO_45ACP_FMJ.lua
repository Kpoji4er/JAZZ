UndefineClass('JAZZ_AMMO_45ACP_FMJ')
DefineClass.JAZZ_AMMO_45ACP_FMJ = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/45ACP.png",
	DisplayName = T(270886313378, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_45ACP_FMJ DisplayName]] ".45ACP, FMJ"),
	DisplayNamePlural = T(136983924045, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_45ACP_FMJ DisplayNamePlural]] ".45ACP, FMJ"),
	colorStyle = "AmmoBasicColor",
	Description = T(654722607287, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_45ACP_FMJ Description]] "Базовый армейский патрон калибра .45, против брони он бессилен, зато способен нанести огромный урон, по мерка пистолетов. Это база."),
	AdditionalHint = "",
	Cost = 360,
	CanAppearInShop = true,
	MaxStock = 50,
	RestockWeight = 20,
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

