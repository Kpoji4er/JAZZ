UndefineClass('JAZZ_AMMO_762x39_JHP')
DefineClass.JAZZ_AMMO_762x39_JHP = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ammo",
	RepairCost = 400,
	Icon = "Mod/e6L4ECj/Ammopics/762x39JHP.png",
	DisplayName = T(890000000000362, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_762x39_JHP DisplayName]] "7,62х39мм, ПС"),
	DisplayNamePlural = T(890000000001046, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_762x39_JHP DisplayNamePlural]] "7,62х39мм, ПС"),
	colorStyle = "AmmoJHPColor",
	Description = T(890000000000659, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_762x39_JHP Description]] "Коммерческий патрон, в отличии от FMJ раскрывается в цели, т.е. Экспансивный, хороший убой за низкую цену."),
	AdditionalHint = "",
	Cost = 1150,
	CanAppearInShop = true,
	Tier = 2,
	MaxStock = 5,
	RestockWeight = 75,
	CategoryPair = "762WP",
	ShopStackSize = 100,
	MaxStacks = 60,
	Caliber = "JAZZ_Caliber_762x39",
	Modifications = {
		PlaceObj('CaliberModification', {
			target_prop = "PenetrationClass",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 5,
			target_prop = "PenetrationBonus",
		}),
		PlaceObj('CaliberModification', {
			mod_mul = 1200,
			target_prop = "Damage",
		}),
		PlaceObj('CaliberModification', {
			mod_add = -8,
			target_prop = "Reliability",
		}),
		PlaceObj('CaliberModification', {
			mod_add = -2,
			target_prop = "BulletDropRange",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 20,
			target_prop = "CritChance",
		}),
		PlaceObj('CaliberModification', {
			mod_mul = 970,
			target_prop = "Grouping",
		}),
	},
	AppliedEffects = {
		"Bleeding",
	},
}

