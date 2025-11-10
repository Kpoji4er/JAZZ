UndefineClass('JAZZ_AMMO_545_Poor')
DefineClass.JAZZ_AMMO_545_Poor = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/545SP.png",
	DisplayName = T(402352878282, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_545_Poor DisplayName]] "5,45 мм, Барнаул SP Substandard"),
	DisplayNamePlural = T(875634951024, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_545_Poor DisplayNamePlural]] "5,45 мм, Барнаул SP Substandard"),
	colorStyle = "AmmoSubstandardColor",
	Description = T(979485744753, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_545_Poor Description]] "Гражданский спортивно-охотничий патрон калибра 5.45x39мм."),
	Cost = 540,
	CanAppearInShop = true,
	Tier = 2,
	RestockWeight = 30,
	CategoryPair = "545",
	ShopStackSize = 120,
	MaxStacks = 90,
	Caliber = "JAZZ_Caliber_545",
	Modifications = {
		PlaceObj('CaliberModification', {
			target_prop = "PenetrationClass",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 4,
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
			mod_add = 100,
			target_prop = "BaseJamChance",
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
			mod_mul = 980,
			target_prop = "Grouping",
		}),
		PlaceObj('CaliberModification', {
			mod_add = -1,
			target_prop = "Recoil",
		}),
	},
	AppliedEffects = {
		"BleedingChance",
	},
}

