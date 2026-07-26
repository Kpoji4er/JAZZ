UndefineClass('JAZZ_AMMO_762x25_JHP')
DefineClass.JAZZ_AMMO_762x25_JHP = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/762x25jhp.png",
	DisplayName = T(890000000000665, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_762x25_JHP DisplayName]] "7.62x25, Wolf JHP"),
	DisplayNamePlural = T(890000000001217, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_762x25_JHP DisplayNamePlural]] "7.62x25, Wolf JHP"),
	colorStyle = "AmmoJHPColor",
	Description = T(890000000000622, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_762x25_JHP Description]] "Экспансивный патрон, на сколько это вообще возможно, коммерческий дешевый, но какой есть. Тут надо брать не качеством, а количеством."),
	Cost = 234,
	CanAppearInShop = true,
	MaxStock = 50,
	RestockWeight = 10,
	CategoryPair = "762x25",
	ShopStackSize = 50,
	MaxStacks = 120,
	Caliber = "JAZZ_Caliber_762x25",
	Modifications = {
		PlaceObj('CaliberModification', {
			target_prop = "PenetrationClass",
		}),
		PlaceObj('CaliberModification', {
			target_prop = "PenetrationBonus",
		}),
		PlaceObj('CaliberModification', {
			mod_mul = 1200,
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
			mod_add = 20,
			target_prop = "CritChance",
		}),
		PlaceObj('CaliberModification', {
			mod_mul = 980,
			target_prop = "Grouping",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 100,
			target_prop = "BaseJamChance",
		}),
		PlaceObj('CaliberModification', {
			mod_add = -1,
			target_prop = "Recoil",
		}),
	},
	AppliedEffects = {
		"Bleeding",
	},
}

