UndefineClass('JAZZ_AMMO_50BMG_API_HEI')
DefineClass.JAZZ_AMMO_50BMG_API_HEI = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ammo",
	Icon = "UI/Icons/Items/50bmg_he",
	DisplayName = T(309974279653, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_50BMG_API_HEI DisplayName]] ".50, РАЗР"),
	DisplayNamePlural = T(322318596873, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_50BMG_API_HEI DisplayNamePlural]] ".50, РАЗР"),
	colorStyle = "AmmoHPColor",
	Description = T(642491927546, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_50BMG_API_HEI Description]] "Бронебойно зажигательная трассирующая пуля данного калибра наверное делалась для войны с другой солнечной системой, не понятно зачем вам такая мощь, но если надо, значит надо."),
	AdditionalHint = "",
	Cost = 13500,
	CanAppearInShop = true,
	Tier = "4",
	MaxStock = 5,
	RestockWeight = 1,
	CategoryPair = "50BMG",
	ShopStackSize = 5,
	Caliber = "JAZZ_Caliber_50BMG",
	Modifications = {
		PlaceObj('CaliberModification', {
			mod_mul = 3000,
			target_prop = "PenetrationClass",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 8,
			target_prop = "PenetrationBonus",
		}),
		PlaceObj('CaliberModification', {
			mod_add = -5,
			target_prop = "Reliability",
		}),
		PlaceObj('CaliberModification', {
			mod_mul = 800,
			target_prop = "Damage",
		}),
		PlaceObj('CaliberModification', {
			mod_mul = 980,
			target_prop = "Grouping",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 20,
			target_prop = "BaseJamChance",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 2,
			target_prop = "Recoil",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 4,
			target_prop = "BulletDropRange",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 10,
			target_prop = "CritChance",
		}),
	},
	AppliedEffects = {
		"Exposed",
	},
	ammo_type_icon = "UI/Icons/Items/ta_subsonic.png",
}

