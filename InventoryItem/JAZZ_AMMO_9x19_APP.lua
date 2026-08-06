UndefineClass('JAZZ_AMMO_9x19_APP')
DefineClass.JAZZ_AMMO_9x19_APP = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/919APP.png",
	DisplayName = T(890000000000579, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_9x19_APP DisplayName]] "9х19 мм, 7н31 ББ+"),
	DisplayNamePlural = T(890000000001379, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_9x19_APP DisplayNamePlural]] "9х19 мм, 7н31 ББ+"),
	colorStyle = "AmmoAPPColor",
	Description = T(890000000000597, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_9x19_APP Description]] "Очень серьезный боеприпас, кроме шуток способен пробивать многие базовые бронежилеты, хорошая кучность, точность и настильность. Немного негативно сказывается на износе оружия, но вы же хотите наконец простреливать бронеплиты пистолетным патроном? Это ваш шанс."),
	AdditionalHint = "",
	Cost = 2200,
	CanAppearInShop = true,
	Tier = 3,
	MaxStock = 3,
	RestockWeight = 16,
	CategoryPair = "9mm",
	ShopStackSize = 50,
	MaxStacks = 120,
	Caliber = "JAZZ_Caliber_9x19",
	Modifications = {
		PlaceObj('CaliberModification', {
			mod_mul = 2000,
			target_prop = "PenetrationClass",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 3,
			target_prop = "PenetrationBonus",
		}),
		PlaceObj('CaliberModification', {
			mod_mul = 800,
			target_prop = "Damage",
		}),
		PlaceObj('CaliberModification', {
			mod_add = -5,
			target_prop = "Reliability",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 40,
			target_prop = "BaseJamChance",
		}),
		PlaceObj('CaliberModification', {
			mod_mul = 960,
			target_prop = "Grouping",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 4,
			target_prop = "BulletDropRange",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 1,
			target_prop = "CritChance",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 2,
			target_prop = "Recoil",
		}),
	},
	ammo_type_icon = "UI/Icons/Items/ta_ap.png",
}

