UndefineClass('JAZZ_AMMO_545_EPR')
DefineClass.JAZZ_AMMO_545_EPR = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/545EPR.png",
	DisplayName = T(686371523176, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_545_EPR DisplayName]] "5,45 мм, ПП Повышенной Пробиваемости"),
	DisplayNamePlural = T(173908119871, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_545_EPR DisplayNamePlural]] "5,45 мм, ПП Повышенной Пробиваемости"),
	colorStyle = "AmmoHPColor",
	Description = T(706390057843, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_545_EPR Description]] "Это как базовый армейский патрон, только он может залетать в бронированную пятку и вылетать из бронированного затылка."),
	Cost = 1800,
	CanAppearInShop = true,
	Tier = "4",
	MaxStock = 10,
	RestockWeight = 10,
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
			mod_add = 5,
			target_prop = "PenetrationBonus",
		}),
		PlaceObj('CaliberModification', {
			mod_mul = 950,
			target_prop = "Damage",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 10,
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

