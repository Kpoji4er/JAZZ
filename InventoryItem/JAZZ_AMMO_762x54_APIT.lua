UndefineClass('JAZZ_AMMO_762x54_APIT')
DefineClass.JAZZ_AMMO_762x54_APIT = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/762x54RBZT.png",
	DisplayName = T(907828676418, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_762x54_APIT DisplayName]] "7,62x54R мм БЗТ (API-T)"),
	DisplayNamePlural = T(968086694447, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_762x54_APIT DisplayNamePlural]] "7,62x54R мм БЗТ (API-T)"),
	colorStyle = "AmmoAPPColor",
	Description = T(273361512171, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_762x54_APIT Description]] "Крышесносные патроны во всех смыслах, и пробьёт и подожжёт и даже путь укажет, при разработке данного боеприпаса однозначно использовалась божья длань."),
	Cost = 3600,
	CanAppearInShop = true,
	Tier = "5",
	MaxStock = 5,
	RestockWeight = 10,
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
			mod_add = 5,
			mod_mul = 0,
			target_prop = "PenetrationBonus",
		}),
		PlaceObj('CaliberModification', {
			mod_mul = 900,
			target_prop = "Damage",
		}),
		PlaceObj('CaliberModification', {
			mod_add = -5,
			target_prop = "Reliability",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 200,
			target_prop = "BaseJamChance",
		}),
		PlaceObj('CaliberModification', {
			mod_mul = 980,
			target_prop = "Grouping",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 3,
			target_prop = "BulletDropRange",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 10,
			target_prop = "CritChance",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 5,
			target_prop = "Recoil",
		}),
	},
	AppliedEffects = {
		"Burning",
		"Bleeding",
		"Exposed",
		"MarkedTraccers",
	},
}

