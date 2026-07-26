UndefineClass('JAZZ_AMMO_762x51_FMJ')
DefineClass.JAZZ_AMMO_762x51_FMJ = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/762NATO.png",
	DisplayName = T(890000000001098, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_762x51_FMJ DisplayName]] "7.62х51мм НАТО, FMJ"),
	DisplayNamePlural = T(890000000001034, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_762x51_FMJ DisplayNamePlural]] "7.62х51мм НАТО, FMJ"),
	colorStyle = "AmmoBasicColor",
	Description = T(890000000001210, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_762x51_FMJ Description]] "Какой-то не выдающийся патрон, просто работает, кого-то убивает, зачем-то существует. Скучно, без изюминки."),
	AdditionalHint = "",
	Cost = 1500,
	CanAppearInShop = true,
	Tier = 2,
	MaxStock = 50,
	RestockWeight = 20,
	CategoryPair = "762NATO",
	ShopStackSize = 20,
	MaxStacks = 40,
	Caliber = "JAZZ_Caliber_762x51",
	Modifications = {
		PlaceObj('CaliberModification', {
			mod_mul = 2000,
			target_prop = "PenetrationClass",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 2,
			target_prop = "PenetrationBonus",
		}),
	},
	AppliedEffects = {
		"Bleeding",
	},
	ammo_type_icon = "UI/Icons/Items/ta_hp.png",
}

