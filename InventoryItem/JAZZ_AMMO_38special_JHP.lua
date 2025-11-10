UndefineClass('JAZZ_AMMO_38special_JHP')
DefineClass.JAZZ_AMMO_38special_JHP = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/38Sp.png",
	DisplayName = T(865245516789, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_38special_JHP DisplayName]] ".38 Special JHP"),
	DisplayNamePlural = T(360885048478, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_38special_JHP DisplayNamePlural]] ".38 Special JHP"),
	colorStyle = "AmmoJHPColor",
	Description = T(285060449915, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_38special_JHP Description]] "Стандартный патрон для дамских сверчков, но экспансивный, можно вытащить револьвер из носка и размозжить кому-то голову в упор."),
	Cost = 135,
	CanAppearInShop = true,
	MaxStock = 50,
	RestockWeight = 5,
	CategoryPair = "44CAL",
	ShopStackSize = 50,
	MaxStacks = 120,
	Caliber = "JAZZ_Caliber_38",
	Modifications = {
		PlaceObj('CaliberModification', {
			target_prop = "PenetrationClass",
		}),
		PlaceObj('CaliberModification', {
			mod_add = -3,
			target_prop = "PenetrationBonus",
		}),
		PlaceObj('CaliberModification', {
			mod_mul = 1200,
			target_prop = "Damage",
		}),
		PlaceObj('CaliberModification', {
			mod_add = -7,
			target_prop = "Reliability",
		}),
		PlaceObj('CaliberModification', {
			mod_add = -1,
			target_prop = "BulletDropRange",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 18,
			target_prop = "CritChance",
		}),
		PlaceObj('CaliberModification', {
			mod_mul = 970,
			target_prop = "Grouping",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 70,
			target_prop = "BaseJamChance",
		}),
	},
	AppliedEffects = {
		"Bleeding",
	},
}

