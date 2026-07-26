UndefineClass('JAZZ_AMMO_762x25_FMJ')
DefineClass.JAZZ_AMMO_762x25_FMJ = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/762x25.png",
	DisplayName = T(890000000000663, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_762x25_FMJ DisplayName]] "7.62x25, 57-Н-134С (FMJ)"),
	DisplayNamePlural = T(890000000001215, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_762x25_FMJ DisplayNamePlural]] "7.62x25, 57-Н-134С (FMJ)"),
	colorStyle = "AmmoBasicColor",
	Description = T(890000000000620, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_762x25_FMJ Description]] "Базовый устаревший во всех смыслах пистолетный патрон, но это всё тот же паровозик, который смог."),
	Cost = 180,
	CanAppearInShop = true,
	MaxStock = 50,
	RestockWeight = 20,
	CategoryPair = "762x25",
	ShopStackSize = 50,
	MaxStacks = 120,
	Caliber = "JAZZ_Caliber_762x25",
	Modifications = {
		PlaceObj('CaliberModification', {
			target_prop = "PenetrationClass",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 2,
			target_prop = "PenetrationBonus",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 6,
			target_prop = "CritChance",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 1,
			target_prop = "BulletDropRange",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 1,
			target_prop = "Recoil",
		}),
	},
}

