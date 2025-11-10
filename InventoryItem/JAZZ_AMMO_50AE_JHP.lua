UndefineClass('JAZZ_AMMO_50AE_JHP')
DefineClass.JAZZ_AMMO_50AE_JHP = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/50AEJHP.png",
	DisplayName = T(224747486019, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_50AE_JHP DisplayName]] ".50AE JHP"),
	DisplayNamePlural = T(272581385016, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_50AE_JHP DisplayNamePlural]] ".50AE JHP"),
	colorStyle = "AmmoBasicColor",
	Description = T(928449338739, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_50AE_JHP Description]] "Дорогой, даже дороже обычной версии патрона, экспансивный и бесполезный. Но крутость данного патрона не оспорима."),
	Cost = 1800,
	CanAppearInShop = true,
	MaxStock = 10,
	RestockWeight = 5,
	CategoryPair = "50BMG",
	ShopStackSize = 25,
	Caliber = "JAZZ_Caliber_50AE",
	Modifications = {
		PlaceObj('CaliberModification', {
			target_prop = "PenetrationClass",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 2,
			target_prop = "PenetrationBonus",
		}),
		PlaceObj('CaliberModification', {
			mod_mul = 1300,
			target_prop = "Damage",
		}),
		PlaceObj('CaliberModification', {
			mod_add = -10,
			target_prop = "Reliability",
		}),
		PlaceObj('CaliberModification', {
			mod_add = -2,
			target_prop = "BulletDropRange",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 30,
			target_prop = "CritChance",
		}),
		PlaceObj('CaliberModification', {
			mod_mul = 950,
			target_prop = "Grouping",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 120,
			target_prop = "BaseJamChance",
		}),
	},
	AppliedEffects = {
		"Bleeding",
	},
}

