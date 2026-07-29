UndefineClass('_762WP_Subsonic')
DefineClass._762WP_Subsonic = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "Дозвуковые - меньше отдача и шум",
	object_class = "Ammo",
	RepairCost = 200,
	Icon = "Mod/e6L4ECj/Ammopics/TEST.png",
	DisplayName = T(705582625224, --[[ModItemInventoryItemCompositeDef _762WP_Subsonic DisplayName]] "7,62х39мм, УС"),
	DisplayNamePlural = T(194372616955, --[[ModItemInventoryItemCompositeDef _762WP_Subsonic DisplayNamePlural]] "7,62х39мм, УС"),
	colorStyle = "AmmoBasicColor",
	Description = T(337151148241, --[[ModItemInventoryItemCompositeDef _762WP_Subsonic Description]] "Специальный советский дозвуковой патрон УС калибра 7.62х39мм"),
	AdditionalHint = T(468738881554, --[[ModItemInventoryItemCompositeDef _762WP_Subsonic AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Обеспечивает уверенное поражение целей обладающих 2-м классом брони\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Дозвуковые: пониженный урон, уменьшенная дальность, уменьшенная точность, уменьшенная громкость выстрела, увеличенная надежность"),
	Cost = 350,
	RestockWeight = 25,
	CategoryPair = "762WP",
	ShopStackSize = 30,
	MaxStacks = 60,
	Caliber = "762WP",
	Modifications = {
		PlaceObj('CaliberModification', {
			mod_mul = 900,
			target_prop = "Damage",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 1,
			target_prop = "PenetrationClass",
		}),
		PlaceObj('CaliberModification', {
			mod_mul = 900,
			target_prop = "WeaponRange",
		}),
		PlaceObj('CaliberModification', {
			mod_add = -1,
			target_prop = "AimAccuracy",
		}),
		PlaceObj('CaliberModification', {
			mod_add = -3,
			target_prop = "Recoil",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 10,
			target_prop = "Reliability",
		}),
		PlaceObj('CaliberModification', {
			mod_mul = 800,
			target_prop = "ObjDamageMod",
		}),
	},
	AppliedEffects = {
		"Bleeding",
	},
	ammo_type_icon = "UI/Icons/Items/ta_hp.png",
}

