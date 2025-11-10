UndefineClass('JAZZ_AMMO_12gauge_Buckshot')
DefineClass.JAZZ_AMMO_12gauge_Buckshot = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "Картечь - 9 частиц",
	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/12gBUCKSHOT.png",
	DisplayName = T(365779430314, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_12gauge_Buckshot DisplayName]] "12-й калибр, Картечь"),
	DisplayNamePlural = T(789991711408, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_12gauge_Buckshot DisplayNamePlural]] "12-й калибр, Картечь"),
	colorStyle = "AmmoArmyColor",
	Description = T(569006389836, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_12gauge_Buckshot Description]] "Стандартный картечный боеприпас, бронебойности тут и не ночевало, дырок будет меньше, чем хотелось бы, однако они будут больше и возможно получится убить кого-то в одежде."),
	AdditionalHint = "",
	Cost = 600,
	CanAppearInShop = true,
	MaxStock = 30,
	RestockWeight = 20,
	ShopStackSize = 25,
	MaxStacks = 20,
	Caliber = "JAZZ_Caliber_12gauge",
	Modifications = {
		PlaceObj('CaliberModification', {
			mod_mul = 9000,
			target_prop = "AutoShots",
		}),
		PlaceObj('CaliberModification', {
			mod_mul = 4000,
			target_prop = "Damage",
		}),
		PlaceObj('CaliberModification', {
			target_prop = "PenetrationClass",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 2,
			target_prop = "PenetrationBonus",
		}),
		PlaceObj('CaliberModification', {
			mod_mul = 1120,
			target_prop = "Grouping",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 6,
			target_prop = "CritChance",
		}),
	},
}

