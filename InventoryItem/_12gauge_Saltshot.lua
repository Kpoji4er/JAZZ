UndefineClass('_12gauge_Saltshot')
DefineClass._12gauge_Saltshot = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "Соль - 20 частиц",
	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/TEST.png",
	DisplayName = T(267395126102, --[[ModItemInventoryItemCompositeDef _12gauge_Saltshot DisplayName]] "12-gauge Saltshot"),
	DisplayNamePlural = T(598926526992, --[[ModItemInventoryItemCompositeDef _12gauge_Saltshot DisplayNamePlural]] "12-gauge Saltshot"),
	colorStyle = "AmmoHPColor",
	Description = T(920340970285, --[[ModItemInventoryItemCompositeDef _12gauge_Saltshot Description]] "Боеприпас с солью 12-го калибра."),
	AdditionalHint = T(237005758229, --[[ModItemInventoryItemCompositeDef _12gauge_Saltshot AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> очень низкий урон\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Сниженная дальнобойность\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Увеличенный сектор атаки\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Вызывает у цели <color EmStyle>случайные травмы</color>"),
	Cost = 100,
	MaxStock = 5,
	RestockWeight = 80,
	ShopStackSize = 12,
	MaxStacks = 20,
	Caliber = "12gauge",
	Modifications = {
		PlaceObj('CaliberModification', {
			mod_mul = 200,
			target_prop = "Damage",
		}),
		PlaceObj('CaliberModification', {
			mod_add = -2,
			target_prop = "AimAccuracy",
		}),
		PlaceObj('CaliberModification', {
			mod_mul = 700,
			target_prop = "WeaponRange",
		}),
		PlaceObj('CaliberModification', {
			mod_mul = 1700,
			target_prop = "OverwatchAngle",
		}),
		PlaceObj('CaliberModification', {
			mod_mul = 20000,
			target_prop = "AutoShots",
		}),
	},
	AppliedEffects = {
		"HeadshotTorsoshotArmsshotLegsshot",
	},
	ammo_type_icon = "UI/Icons/Items/ta_hp.png",
}

