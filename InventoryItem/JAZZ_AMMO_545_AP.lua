UndefineClass('JAZZ_AMMO_545_AP')
DefineClass.JAZZ_AMMO_545_AP = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/545AP.png",
	DisplayName = T(157788838717, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_545_AP DisplayName]] "5,45 мм, БП Бронебойный"),
	DisplayNamePlural = T(972063049608, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_545_AP DisplayNamePlural]] "5,45 мм, БП Бронебойный"),
	colorStyle = "AmmoAPColor",
	Description = T(109043157088, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_545_AP Description]] "Бронебойный армейский патрон калибра 7Н22 5.45x39мм"),
	AdditionalHint = "",
	Cost = 2700,
	CanAppearInShop = true,
	Tier = "5",
	RestockWeight = 5,
	CategoryPair = "545",
	ShopStackSize = 120,
	MaxStacks = 90,
	Caliber = "JAZZ_Caliber_545",
	Modifications = {
		PlaceObj('CaliberModification', {
			mod_mul = 3000,
			target_prop = "PenetrationClass",
		}),
		PlaceObj('CaliberModification', {
			mod_mul = 0,
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
			mod_add = 4,
			target_prop = "BaseJamChance",
		}),
		PlaceObj('CaliberModification', {
			mod_mul = 980,
			target_prop = "Grouping",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 2,
			target_prop = "BulletDropRange",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 8,
			target_prop = "CritChance",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 3,
			target_prop = "Recoil",
		}),
	},
}

