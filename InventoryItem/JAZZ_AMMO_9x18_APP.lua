UndefineClass('JAZZ_AMMO_9x18_APP')
DefineClass.JAZZ_AMMO_9x18_APP = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/9x18APP.png",
	DisplayName = T(865245516789, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_9x18_APP DisplayName]] "9x18мм, 7н25 ББ+"),
	DisplayNamePlural = T(360885048478, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_9x18_APP DisplayNamePlural]] "9x18мм, 7н25 ББ+"),
	colorStyle = "AmmoAPPColor",
	Description = T(285060449915, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_9x18_APP Description]] "Бронебойный патрон 9х18, из которого выжали всё что могли, чтоб пробивать более или менее серьезную защиту. Бронебойность негативно сказывается на надежности, но положительно на эффективности."),
	Cost = 960,
	CanAppearInShop = true,
	Tier = "4",
	MaxStock = 50,
	RestockWeight = 10,
	CategoryPair = "9x18",
	ShopStackSize = 50,
	MaxStacks = 120,
	Caliber = "JAZZ_Caliber_9x18",
	Modifications = {
		PlaceObj('CaliberModification', {
			mod_mul = 2000,
			target_prop = "PenetrationClass",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 2,
			target_prop = "PenetrationBonus",
		}),
		PlaceObj('CaliberModification', {
			mod_mul = 850,
			target_prop = "Damage",
		}),
		PlaceObj('CaliberModification', {
			mod_add = -5,
			target_prop = "Reliability",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 40,
			target_prop = "BaseJamChance",
		}),
		PlaceObj('CaliberModification', {
			mod_mul = 950,
			target_prop = "Grouping",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 2,
			target_prop = "BulletDropRange",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 1,
			target_prop = "CritChance",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 2,
			target_prop = "Recoil",
		}),
	},
}

