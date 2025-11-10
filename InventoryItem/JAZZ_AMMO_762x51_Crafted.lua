UndefineClass('JAZZ_AMMO_762x51_Crafted')
DefineClass.JAZZ_AMMO_762x51_Crafted = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/762NATOCrafted.png",
	DisplayName = T(816293484485, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_762x51_Crafted DisplayName]] "7.62х51мм НАТО, FMJ"),
	DisplayNamePlural = T(784212637278, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_762x51_Crafted DisplayNamePlural]] "7.62х51мм НАТО, FMJ"),
	colorStyle = "AmmoCraftedColor",
	Description = T(868039456416, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_762x51_Crafted Description]] "Поздравляем, вы собрали на коленке довольно эффективный боеприпас, вас порадует его бюджетность относительно эффективности ровно до того момента, когда он убьет вас, а не цель."),
	AdditionalHint = "",
	Cost = 200,
	Tier = 2,
	MaxStock = 50,
	RestockWeight = 150,
	CategoryPair = "762NATO",
	ShopStackSize = 30,
	MaxStacks = 40,
	Caliber = "JAZZ_Caliber_762x51",
	Modifications = {
		PlaceObj('CaliberModification', {
			mod_mul = 2000,
			target_prop = "PenetrationClass",
		}),
		PlaceObj('CaliberModification', {
			mod_mul = 4000,
			target_prop = "PenetrationBonus",
		}),
		PlaceObj('CaliberModification', {
			mod_add = -25,
			target_prop = "Reliability",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 200,
			target_prop = "BaseJamChance",
		}),
		PlaceObj('CaliberModification', {
			mod_mul = 850,
			target_prop = "Grouping",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 15,
			target_prop = "CritChance",
		}),
	},
	AppliedEffects = {
		"Bleeding",
	},
	ammo_type_icon = "UI/Icons/Items/ta_hp.png",
}

