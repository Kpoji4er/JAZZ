UndefineClass('JAZZ_AMMO_762x54_Match')
DefineClass.JAZZ_AMMO_762x54_Match = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/762x54RSNB.png",
	DisplayName = T(314555250393, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_762x54_Match DisplayName]] "7,62x54R мм СНБ (AP / match)"),
	DisplayNamePlural = T(299479740054, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_762x54_Match DisplayNamePlural]] "7,62x54R мм СНБ (AP / match)"),
	colorStyle = "AmmoMatchColor",
	Description = T(713481016841, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_762x54_Match Description]] "Снайперский бронебойный патрон, отстает по эффективности от собратьев из НАТО, но не сильно, а раз не сильно зачем платить больше!"),
	Cost = 4500,
	CanAppearInShop = true,
	Tier = "4",
	MaxStock = 1,
	RestockWeight = 5,
	CategoryPair = "762x54",
	ShopStackSize = 20,
	MaxStacks = 40,
	Caliber = "JAZZ_Caliber_762x54R",
	Modifications = {
		PlaceObj('CaliberModification', {
			mod_mul = 3000,
			target_prop = "PenetrationClass",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 2,
			target_prop = "PenetrationBonus",
		}),
		PlaceObj('CaliberModification', {
			mod_mul = 800,
			target_prop = "Damage",
		}),
		PlaceObj('CaliberModification', {
			mod_add = -4,
			target_prop = "Reliability",
		}),
		PlaceObj('CaliberModification', {
			mod_mul = 1200,
			target_prop = "Grouping",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 5,
			target_prop = "BulletDropRange",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 3,
			target_prop = "Recoil",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 6,
			target_prop = "CritChance",
		}),
	},
}

