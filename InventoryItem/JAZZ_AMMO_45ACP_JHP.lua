UndefineClass('JAZZ_AMMO_45ACP_JHP')
DefineClass.JAZZ_AMMO_45ACP_JHP = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/45ACPHP.png",
	DisplayName = T(587071959481, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_45ACP_JHP DisplayName]] ".45ACP, JHP"),
	DisplayNamePlural = T(993338998831, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_45ACP_JHP DisplayNamePlural]] ".45ACP, JHP"),
	colorStyle = "AmmoJHPColor",
	Description = T(582557259656, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_45ACP_JHP Description]] "Представьте что ваш пистолет стреляет 12 калибром, представили? Вот это почти тоже самое, станьте крушителем дынь, арбузов и африканских диктаторов."),
	AdditionalHint = "",
	Cost = 650,
	CanAppearInShop = true,
	Tier = 2,
	MaxStock = 5,
	RestockWeight = 75,
	CategoryPair = "45ACP",
	ShopStackSize = 50,
	MaxStacks = 80,
	Caliber = "JAZZ_Caliber_45ACP",
	Modifications = {
		PlaceObj('CaliberModification', {
			target_prop = "PenetrationClass",
		}),
		PlaceObj('CaliberModification', {
			mod_add = -3,
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
			mod_add = 30,
			target_prop = "CritChance",
		}),
		PlaceObj('CaliberModification', {
			mod_mul = 970,
			target_prop = "Grouping",
		}),
		PlaceObj('CaliberModification', {
			mod_add = -1,
			target_prop = "Recoil",
		}),
	},
	AppliedEffects = {
		"Bleeding",
	},
	ammo_type_icon = "UI/Icons/Items/ta_hp.png",
}

