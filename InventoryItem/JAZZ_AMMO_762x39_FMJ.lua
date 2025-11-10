UndefineClass('JAZZ_AMMO_762x39_FMJ')
DefineClass.JAZZ_AMMO_762x39_FMJ = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/762x39CHN.png",
	DisplayName = T(403807663771, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_762x39_FMJ DisplayName]] "7,62х39мм, Norinco FMJ"),
	DisplayNamePlural = T(578647545074, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_762x39_FMJ DisplayNamePlural]] "7,62х39мм, Norinco FMJ"),
	colorStyle = "AmmoBasicColor",
	Description = T(296646736495, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_762x39_FMJ Description]] "Гражданский коммерческий патрон, из-за веса и калибра пуля всё равно имеет, хоть и посредственные, но какие никакие бронебойные качества."),
	AdditionalHint = "",
	Cost = 600,
	CanAppearInShop = true,
	Tier = 2,
	RestockWeight = 20,
	CategoryPair = "762WP",
	ShopStackSize = 100,
	MaxStacks = 60,
	Caliber = "JAZZ_Caliber_762x39",
	Modifications = {
		PlaceObj('CaliberModification', {
			mod_mul = 2000,
			target_prop = "PenetrationClass",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 1,
			target_prop = "PenetrationBonus",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 5,
			target_prop = "CritChance",
		}),
	},
	AppliedEffects = {
		"Bleeding",
	},
	ammo_type_icon = "UI/Icons/Items/ta_hp.png",
}

