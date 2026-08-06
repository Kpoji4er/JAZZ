UndefineClass('JAZZ_AMMO_556_Match')
DefineClass.JAZZ_AMMO_556_Match = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/556Match.png",
	DisplayName = T(685583532964, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_556_Match DisplayName]] "5,56 мм, Mk262"),
	DisplayNamePlural = T(563192097250, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_556_Match DisplayNamePlural]] "5,56 мм, Mk262"),
	colorStyle = "AmmoMatchColor",
	Description = T(886365993358, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_556_Match Description]] "Высокие технологии добрались и до нас, последние тренды войны здесь и сейчас, прямо в вашем кармане. Идеально откалиброванные патроны и сбалансированные характеристики. Дорого, и круто."),
	AdditionalHint = "",
	Cost = 2800,
	CanAppearInShop = true,
	Tier = 4,
	RestockWeight = 18,
	MaxStock = 3,
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
			mod_add = 6,
			target_prop = "PenetrationBonus",
		}),
		PlaceObj('CaliberModification', {
			target_prop = "Damage",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 10,
			target_prop = "Reliability",
		}),
		PlaceObj('CaliberModification', {
			mod_mul = 1180,
			target_prop = "Grouping",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 3,
			target_prop = "BulletDropRange",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 18,
			target_prop = "CritChance",
		}),
	},
	AppliedEffects = {
		"Bleeding",
	},
}

