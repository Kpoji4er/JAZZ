UndefineClass('JAZZ_AMMO_762x39_Crafted')
DefineClass.JAZZ_AMMO_762x39_Crafted = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/762x39Crafted.png",
	DisplayName = T(403807663771, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_762x39_Crafted DisplayName]] "7,62х39мм, Кустарный"),
	DisplayNamePlural = T(578647545074, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_762x39_Crafted DisplayNamePlural]] "7,62х39мм, Кустарный"),
	colorStyle = "AmmoCraftedColor",
	Description = T(296646736495, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_762x39_Crafted Description]] "Сперва хочется сказать что он охотничий, но нет, он собран на коленке из старых гильз, мокрого пороха и фекалий местной фауны. Пользуется популярностью у местных, дешевизна берет своё!"),
	Cost = 100,
	RestockWeight = 150,
	CategoryPair = "762WP",
	ShopStackSize = 30,
	MaxStacks = 60,
	Caliber = "JAZZ_Caliber_762x39",
	Modifications = {
		PlaceObj('CaliberModification', {
			mod_mul = 2000,
			target_prop = "PenetrationClass",
		}),
		PlaceObj('CaliberModification', {
			target_prop = "PenetrationBonus",
		}),
		PlaceObj('CaliberModification', {
			mod_mul = 950,
			target_prop = "Damage",
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
			mod_add = 20,
			target_prop = "CritChance",
		}),
	},
	AppliedEffects = {
		"Bleeding",
	},
	ammo_type_icon = "UI/Icons/Items/ta_hp.png",
}

