UndefineClass('JAZZ_AMMO_44CAL_JHP')
DefineClass.JAZZ_AMMO_44CAL_JHP = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/44JHP.png",
	DisplayName = T(385574320141, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_44CAL_JHP DisplayName]] ".44, JHP"),
	DisplayNamePlural = T(560329197004, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_44CAL_JHP DisplayNamePlural]] ".44, JHP"),
	colorStyle = "AmmoJHPColor",
	Description = T(655933065301, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_44CAL_JHP Description]] "Экспансивная версия .44го, если хочется порвать кого-то на ошметки."),
	AdditionalHint = "",
	Cost = 1167,
	CanAppearInShop = true,
	MaxStock = 25,
	RestockWeight = 5,
	CategoryPair = "44CAL",
	ShopStackSize = 25,
	MaxStacks = 80,
	Caliber = "JAZZ_Caliber_44CAL",
	Modifications = {
		PlaceObj('CaliberModification', {
			target_prop = "PenetrationClass",
		}),
		PlaceObj('CaliberModification', {
			mod_add = -1,
			target_prop = "PenetrationBonus",
		}),
		PlaceObj('CaliberModification', {
			mod_mul = 1400,
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
	ammo_type_icon = "UI/Icons/Items/ta_hp.png",
}

