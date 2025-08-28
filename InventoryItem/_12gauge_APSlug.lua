UndefineClass('_12gauge_APSlug')
DefineClass._12gauge_APSlug = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "Пуля ББ - 1 шт",
	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/TEST.png",
	DisplayName = T(519940407801, "12-й калибр, ББ Пуля"),
	DisplayNamePlural = T(282432572140, "12-й калибр, ББ Пуля"),
	colorStyle = "AmmoAPColor",
	Description = T(377537402679, "Бронебойная пуля 12-го калибра."),
	AdditionalHint = T(319080557737, "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> 1 пуля.\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Обеспечивает уверенное поражение целей обладающих 3-м классом брони\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Увеличенная дальность и урон, но меньше чем у обычной пули"),
	Cost = 500,
	Tier = 2,
	MaxStock = 5,
	RestockWeight = 80,
	ShopStackSize = 12,
	MaxStacks = 5000,
	Caliber = "12gauge",
	Modifications = {
		PlaceObj('CaliberModification', {
			mod_mul = 500,
			target_prop = "OverwatchAngle",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 10,
			target_prop = "WeaponRange",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 30,
			target_prop = "Damage",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 5,
			target_prop = "AimAccuracy",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 2,
			target_prop = "PenetrationClass",
		}),
		PlaceObj('CaliberModification', {
			mod_mul = 500,
			target_prop = "ObjDamageMod",
		}),
	},
	ammo_type_icon = "UI/Icons/Items/ta_ap.png",
}

