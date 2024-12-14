UndefineClass('_762WP_HP')
DefineClass._762WP_HP = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "Китайские - чуть хуже по урону и пробитию",
	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/TEST.png",
	DisplayName = T(312235744948, --[[ModItemInventoryItemCompositeDef _762WP_HP DisplayName]] "7,62х39мм, FMJ"),
	DisplayNamePlural = T(110534409348, --[[ModItemInventoryItemCompositeDef _762WP_HP DisplayNamePlural]] "7,62х39мм, FMJ"),
	colorStyle = "AmmoBasicColor",
	Description = T(336718135346, --[[ModItemInventoryItemCompositeDef _762WP_HP Description]] "Китайский патрон калибра 7.62х39. Уступает советским аналогам"),
	AdditionalHint = T(411537397746, --[[ModItemInventoryItemCompositeDef _762WP_HP AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Обеспечивает уверенное поражение целей обладающих 2-м классом брони\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Патроны низкого качества: пониженный урон, уменьшенная дальность, уменьшенная точность, увеличенный износ"),
	Cost = 100,
	RestockWeight = 150,
	CategoryPair = "762WP",
	ShopStackSize = 30,
	MaxStacks = 5000,
	Caliber = "762WP",
	Modifications = {
		PlaceObj('CaliberModification', {
			mod_mul = 850,
			target_prop = "Damage",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 1,
			target_prop = "PenetrationClass",
		}),
		PlaceObj('CaliberModification', {
			mod_add = -2,
			target_prop = "WeaponRange",
		}),
		PlaceObj('CaliberModification', {
			mod_add = -4,
			target_prop = "AimAccuracy",
		}),
		PlaceObj('CaliberModification', {
			mod_add = -20,
			target_prop = "Reliability",
		}),
	},
	AppliedEffects = {
		"Bleeding",
	},
	ammo_type_icon = "UI/Icons/Items/ta_hp.png",
}

