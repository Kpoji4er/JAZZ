UndefineClass('JAZZ_AMMO_50AE_FMJ')
DefineClass.JAZZ_AMMO_50AE_FMJ = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/50AE.png",
	DisplayName = T(224747486019, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_50AE_FMJ DisplayName]] ".50AE FMJ"),
	DisplayNamePlural = T(272581385016, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_50AE_FMJ DisplayNamePlural]] ".50AE FMJ"),
	colorStyle = "AmmoBasicColor",
	Description = T(928449338739, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_50AE_FMJ Description]] "Дорогой, мощный и бесполезный, подходит для боевиков, но не для войны."),
	Cost = 1200,
	CanAppearInShop = true,
	MaxStock = 10,
	RestockWeight = 10,
	CategoryPair = "50BMG",
	ShopStackSize = 25,
	Caliber = "JAZZ_Caliber_50AE",
	Modifications = {
		PlaceObj('CaliberModification', {
			target_prop = "PenetrationClass",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 6,
			target_prop = "PenetrationBonus",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 12,
			target_prop = "CritChance",
		}),
	},
}

