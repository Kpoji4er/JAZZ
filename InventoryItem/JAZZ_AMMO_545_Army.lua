UndefineClass('JAZZ_AMMO_545_Army')
DefineClass.JAZZ_AMMO_545_Army = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/545.png",
	DisplayName = T(827774006254, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_545_Army DisplayName]] "5,45 мм, ПС Армейский"),
	DisplayNamePlural = T(138469521759, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_545_Army DisplayNamePlural]] "5,45 мм,ПС Армейский"),
	colorStyle = "AmmoArmyColor",
	Description = T(930854241886, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_545_Army Description]] "Стандартный армейский патрон, залетит в пятку, сделает сальто, вылетит через затылок. Патроны для садистов..."),
	AdditionalHint = "",
	Cost = 2300,
	CanAppearInShop = true,
	Tier = 3,
	MaxStock = 5,
	RestockWeight = 50,
	CategoryPair = "545",
	ShopStackSize = 120,
	MaxStacks = 90,
	Caliber = "JAZZ_Caliber_545",
	Modifications = {
		PlaceObj('CaliberModification', {
			mod_mul = 2000,
			target_prop = "PenetrationClass",
		}),
		PlaceObj('CaliberModification', {
			target_prop = "PenetrationBonus",
		}),
		PlaceObj('CaliberModification', {
			target_prop = "Damage",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 20,
			target_prop = "CritChance",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 1,
			target_prop = "Recoil",
		}),
	},
	AppliedEffects = {
		"BleedingChance",
	},
}

