UndefineClass('_12gauge_Flechette')
DefineClass._12gauge_Flechette = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "Пуля - 1 шт",
	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/TEST.png",
	DisplayName = T(486298295383, "12-й калибр, Пуля"),
	DisplayNamePlural = T(316258835711, "12-й калибр, Пуля"),
	colorStyle = "AmmoMatchColor",
	Description = T(774674747916, "Пуля 12-го калибра."),
	AdditionalHint = T(634094190352, "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> 1 пуля.\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Обеспечивает уверенное поражение целей обладающих 2-м классом брони\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Увеличенная дальность и урон"),
	Cost = 120,
	MaxStock = 20,
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
			mod_add = 40,
			target_prop = "Damage",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 5,
			target_prop = "AimAccuracy",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 1,
			target_prop = "PenetrationClass",
		}),
		PlaceObj('CaliberModification', {
			mod_mul = 500,
			target_prop = "ObjDamageMod",
		}),
	},
	ammo_type_icon = "UI/Icons/Items/ta_match.png",
}

