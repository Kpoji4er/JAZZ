UndefineClass('JAZZ_AMMO_9x39_AP')
DefineClass.JAZZ_AMMO_9x39_AP = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "СП6",
	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/939SP6.png",
	DisplayName = T(890000000000642, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_9x39_AP DisplayName]] "9x39 мм, СП-6 (бронебойный)"),
	DisplayNamePlural = T(890000000000962, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_9x39_AP DisplayNamePlural]] "9x39 мм, СП-6 (бронебойный)"),
	colorStyle = "AmmoAPColor",
	Description = T(890000000000381, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_9x39_AP Description]] "Специальный бронебойный дозвуковой патрон, убойность, как водится, на высоте, сможете всех мочить в сортире без шума и лишнего внимания."),
	Cost = 1600,
	CanAppearInShop = true,
	Tier = 5,
	MaxStock = 2,
	RestockWeight = 8,
	CategoryPair = "556",
	ShopStackSize = 20,
	MaxStacks = 60,
	Caliber = "JAZZ_Caliber_9x39",
	Modifications = {
		PlaceObj('CaliberModification', {
			mod_mul = 3000,
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
			mod_add = 1,
			target_prop = "CritChance",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 1,
			target_prop = "Recoil",
		}),
	},
}

