UndefineClass('JAZZ_AMMO_357_JHP')
DefineClass.JAZZ_AMMO_357_JHP = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/357JHP.png",
	DisplayName = T(890000000001189, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_357_JHP DisplayName]] ".357 Mag JHP"),
	DisplayNamePlural = T(890000000000412, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_357_JHP DisplayNamePlural]] ".357 Mag JHP"),
	colorStyle = "AmmoJHPColor",
	Description = T(890000000000282, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_357_JHP Description]] "Экспансивный патрон калибра .357, если вам мало мощи обычной пули, с броней он разумеется не справляется, зато откусить кому-то бочок можно легко."),
	Cost = 324,
	CanAppearInShop = true,
	MaxStock = 50,
	RestockWeight = 5,
	CategoryPair = "44CAL",
	ShopStackSize = 25,
	MaxStacks = 120,
	Caliber = "JAZZ_Caliber_357",
	Modifications = {
		PlaceObj('CaliberModification', {
			target_prop = "PenetrationClass",
		}),
		PlaceObj('CaliberModification', {
			mod_add = -2,
			target_prop = "PenetrationBonus",
		}),
		PlaceObj('CaliberModification', {
			mod_mul = 1300,
			target_prop = "Damage",
		}),
		PlaceObj('CaliberModification', {
			mod_add = -8,
			target_prop = "Reliability",
		}),
		PlaceObj('CaliberModification', {
			mod_add = -1,
			target_prop = "BulletDropRange",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 25,
			target_prop = "CritChance",
		}),
		PlaceObj('CaliberModification', {
			mod_mul = 960,
			target_prop = "Grouping",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 90,
			target_prop = "BaseJamChance",
		}),
	},
	AppliedEffects = {
		"Bleeding",
	},
}

