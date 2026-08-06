UndefineClass('JAZZ_AMMO_9x39_JHP')
DefineClass.JAZZ_AMMO_9x39_JHP = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "СП5",
	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/939SP5.png",
	DisplayName = T(333998606847, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_9x39_JHP DisplayName]] "9x39 мм, СП-5 (экспансивный)"),
	DisplayNamePlural = T(542771498470, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_9x39_JHP DisplayNamePlural]] "9x39 мм, СП-5 (экспансивный)"),
	colorStyle = "AmmoJHPColor",
	Description = T(339244329275, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_9x39_JHP Description]] "Самый базовый специальный дозвуковой патрон, не очень силен на дистанции, не очень силен против брони, однако хорошо дрючит мягкие ткани."),
	Cost = 350,
	CanAppearInShop = true,
	Tier = 3,
	MaxStock = 5,
	RestockWeight = 75,
	CategoryPair = "556",
	ShopStackSize = 20,
	MaxStacks = 60,
	Caliber = "JAZZ_Caliber_9x39",
	Modifications = {
		PlaceObj('CaliberModification', {
			mod_mul = 2000,
			target_prop = "PenetrationClass",
		}),
		PlaceObj('CaliberModification', {
			mod_add = -2,
			target_prop = "PenetrationBonus",
		}),
		PlaceObj('CaliberModification', {
			mod_mul = 1100,
			target_prop = "Damage",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 100,
			target_prop = "BaseJamChance",
		}),
		PlaceObj('CaliberModification', {
			mod_add = -1,
			target_prop = "BulletDropRange",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 15,
			target_prop = "CritChance",
		}),
		PlaceObj('CaliberModification', {
			mod_mul = 1100,
			target_prop = "Grouping",
		}),
	},
}

