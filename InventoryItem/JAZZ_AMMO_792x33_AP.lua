UndefineClass('JAZZ_AMMO_792x33_AP')
DefineClass.JAZZ_AMMO_792x33_AP = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ammo",
	RepairCost = 400,
	Icon = "Mod/e6L4ECj/Ammopics/792x33AP.png",
	DisplayName = T(890000000000365, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_792x33_AP DisplayName]] "792x33мм Pist. Patr. 43 m.E. (ББ)"),
	DisplayNamePlural = T(890000000001049, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_792x33_AP DisplayNamePlural]] "792x33мм Pist. Patr. 43 m.E. (ББ)"),
	colorStyle = "AmmoAPColor",
	Description = T(890000000000657, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_792x33_AP Description]] "Бронебойный вариант армейского патрона 7.92х33 FMJ, на сколько это вообще возможно, все кто может подтвердить умерли от старости."),
	AdditionalHint = "",
	Cost = 4200,
	CanAppearInShop = false,
	MaxStock = 10,
	RestockWeight = 1,
	CategoryPair = "762WP",
	ShopStackSize = 100,
	MaxStacks = 60,
	Caliber = "JAZZ_Caliber_792x33",
	Modifications = {
		PlaceObj('CaliberModification', {
			mod_mul = 2000,
			target_prop = "PenetrationClass",
		}),
		PlaceObj('CaliberModification', {
			target_prop = "PenetrationBonus",
		}),
		PlaceObj('CaliberModification', {
			mod_mul = 800,
			target_prop = "Damage",
		}),
		PlaceObj('CaliberModification', {
			mod_add = -3,
			target_prop = "Reliability",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 20,
			target_prop = "BaseJamChance",
		}),
		PlaceObj('CaliberModification', {
			mod_mul = 960,
			target_prop = "Grouping",
		}),
		PlaceObj('CaliberModification', {
			mod_add = -1,
			target_prop = "BulletDropRange",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 1,
			target_prop = "CritChance",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 1,
			target_prop = "Recoil",
		}),
	},
}

