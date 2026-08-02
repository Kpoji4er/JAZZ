UndefineClass('JAZZ_AMMO_12gauge_Birdshot')
DefineClass.JAZZ_AMMO_12gauge_Birdshot = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "Дробь - 20 частиц",
	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/12gBIRDSHOT.png",
	DisplayName = T(503250075758, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_12gauge_Birdshot DisplayName]] "12-й калибр, дробь"),
	DisplayNamePlural = T(408475040527, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_12gauge_Birdshot DisplayNamePlural]] "12-й калибр, дробь"),
	colorStyle = "AmmoBasicColor",
	Description = T(561107124860, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_12gauge_Birdshot Description]] "Вы держите в руках наглядное пособие по тому как сделать в цели максимально возможное количество дырок за минимальное время."),
	AdditionalHint = "",
	Cost = 375,
	CanAppearInShop = true,
	MaxStock = 50,
	RestockWeight = 30,
	ShopStackSize = 25,
	MaxStacks = 20,
	Caliber = "JAZZ_Caliber_12gauge",
	Modifications = {
		PlaceObj('CaliberModification', {
			mod_mul = 20000,
			target_prop = "BuckshotProjectiles",
		}),
		PlaceObj('CaliberModification', {
			mod_mul = 1250,
			target_prop = "Grouping",
		}),
		PlaceObj('CaliberModification', {
			target_prop = "PenetrationClass",
		}),
		PlaceObj('CaliberModification', {
			mod_add = -5,
			target_prop = "PenetrationBonus",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 3,
			target_prop = "CritChance",
		}),
	},
	AppliedEffects = {
		"BleedingChance",
	},
}

