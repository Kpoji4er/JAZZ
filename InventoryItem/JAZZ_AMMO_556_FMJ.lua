UndefineClass('JAZZ_AMMO_556_FMJ')
DefineClass.JAZZ_AMMO_556_FMJ = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/556.png",
	DisplayName = T(890000000000738, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_556_FMJ DisplayName]] "5,56мм, FMJ"),
	DisplayNamePlural = T(890000000001037, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_556_FMJ DisplayNamePlural]] "5,56 мм, FMJ"),
	colorStyle = "AmmoBasicColor",
	Description = T(890000000001056, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_556_FMJ Description]] "Старый базовый патрон, повода для слез нет, как и выдающихся характеристик. Серая мышь в мире промежуточных патронов."),
	AdditionalHint = "",
	Cost = 1200,
	CanAppearInShop = true,
	Tier = 2,
	MaxStock = 8,
	RestockWeight = 100,
	CategoryPair = "556",
	ShopStackSize = 120,
	MaxStacks = 90,
	Caliber = "JAZZ_Caliber_556",
	Modifications = {
		PlaceObj('CaliberModification', {
			mod_mul = 2000,
			target_prop = "PenetrationClass",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 2,
			target_prop = "PenetrationBonus",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 5,
			target_prop = "CritChance",
		}),
	},
}

