UndefineClass('JAZZ_AMMO_44CAL_Match')
DefineClass.JAZZ_AMMO_44CAL_Match = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/44MATCH.png",
	DisplayName = T(189935598461, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_44CAL_Match DisplayName]] ".44, Match"),
	DisplayNamePlural = T(807918005698, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_44CAL_Match DisplayNamePlural]] ".44, Match"),
	colorStyle = "AmmoMatchColor",
	Description = T(821434202204, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_44CAL_Match Description]] "Коммерческий патрон увеличенной кучности, на случай если надо донести свою крутость на большее расстояние."),
	AdditionalHint = "",
	Cost = 1100,
	CanAppearInShop = true,
	Tier = 3,
	MaxStock = 3,
	RestockWeight = 18,
	CategoryPair = "44CAL",
	ShopStackSize = 25,
	MaxStacks = 80,
	Caliber = "JAZZ_Caliber_44CAL",
	Modifications = {
		PlaceObj('CaliberModification', {
			target_prop = "PenetrationClass",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 3,
			target_prop = "PenetrationBonus",
		}),
		PlaceObj('CaliberModification', {
			mod_mul = 900,
			target_prop = "Damage",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 3,
			target_prop = "Reliability",
		}),
		PlaceObj('CaliberModification', {
			mod_mul = 1200,
			target_prop = "Grouping",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 4,
			target_prop = "BulletDropRange",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 15,
			target_prop = "CritChance",
		}),
	},
	ammo_type_icon = "UI/Icons/Items/ta_match.png",
}

