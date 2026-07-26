UndefineClass('JAZZ_AMMO_46_JHP')
DefineClass.JAZZ_AMMO_46_JHP = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/46JHP.png",
	DisplayName = T(890000000000022, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_46_JHP DisplayName]] "4,6 мм, V-Max JHP"),
	DisplayNamePlural = T(890000000000092, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_46_JHP DisplayNamePlural]] "4,6 мм, V-Max JHP"),
	colorStyle = "AmmoJHPColor",
	Description = T(890000000000575, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_46_JHP Description]] "Экспансивная версия патрона для МП-7, разумеется это не обычный пистолетный патрон, так что и экспансивность не на высоте, но и в бронепробитии данный патрон не сильно потерял."),
	AdditionalHint = "",
	Cost = 1440,
	CanAppearInShop = true,
	Tier = 3,
	MaxStock = 5,
	RestockWeight = 1005,
	CategoryPair = "57",
	ShopStackSize = 50,
	MaxStacks = 60,
	Caliber = "JAZZ_Caliber_46",
	Modifications = {
		PlaceObj('CaliberModification', {
			target_prop = "PenetrationClass",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 9,
			target_prop = "PenetrationBonus",
		}),
		PlaceObj('CaliberModification', {
			mod_mul = 1300,
			target_prop = "Damage",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 16,
			target_prop = "CritChance",
		}),
		PlaceObj('CaliberModification', {
			mod_mul = 980,
			target_prop = "Grouping",
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
	AppliedEffects = {
		"Bleeding",
	},
}

