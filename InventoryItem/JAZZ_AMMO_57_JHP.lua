UndefineClass('JAZZ_AMMO_57_JHP')
DefineClass.JAZZ_AMMO_57_JHP = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/57JHP.png",
	DisplayName = T(890000000000882, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_57_JHP DisplayName]] "5,7 мм, SS197SR JHP"),
	DisplayNamePlural = T(890000000000255, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_57_JHP DisplayNamePlural]] "5,7 мм, SS197SR JHP"),
	colorStyle = "AmmoJHPColor",
	Description = T(890000000001011, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_57_JHP Description]] "Экспансивные патроны для редких бельгийских игрушек. Несмотря на экспансивную пулю патрон способен наносить урон базовой броне."),
	Cost = 2025,
	CanAppearInShop = true,
	Tier = 3,
	MaxStock = 5,
	RestockWeight = 5,
	CategoryPair = "57",
	ShopStackSize = 50,
	MaxStacks = 60,
	Caliber = "JAZZ_Caliber_57",
	Modifications = {
		PlaceObj('CaliberModification', {
			target_prop = "PenetrationClass",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 6,
			target_prop = "PenetrationBonus",
		}),
		PlaceObj('CaliberModification', {
			mod_mul = 1300,
			target_prop = "Damage",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 15,
			target_prop = "CritChance",
		}),
		PlaceObj('CaliberModification', {
			mod_mul = 990,
			target_prop = "Grouping",
		}),
	},
	AppliedEffects = {
		"Bleeding",
	},
}

