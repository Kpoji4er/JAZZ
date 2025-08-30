UndefineClass('_9mm_HP')
DefineClass._9mm_HP = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/TEST.png",
	DisplayName = T(930357114539, --[[ModItemInventoryItemCompositeDef _9mm_HP DisplayName]] "9х19 мм, JHP"),
	DisplayNamePlural = T(730329528081, --[[ModItemInventoryItemCompositeDef _9mm_HP DisplayNamePlural]] "9х19 мм, JHP"),
	colorStyle = "AmmoHPColor",
	Description = T(190364811329, --[[ModItemInventoryItemCompositeDef _9mm_HP Description]] "Экспансивный патрон калибра 9х19мм"),
	AdditionalHint = T(769968102370, --[[ModItemInventoryItemCompositeDef _9mm_HP AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Нулевая бронебойность\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Повышенный урон\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Повышенный шанс критического попадания\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Вызывает <color EmStyle>кровотечение</color>"),
	Cost = 120,
	MaxStock = 15,
	RestockWeight = 25,
	CategoryPair = "9mm",
	ShopStackSize = 30,
	MaxStacks = 5000,
	Caliber = "9mm",
	Modifications = {
		PlaceObj('CaliberModification', {
			mod_mul = 1200,
			target_prop = "Damage",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 15,
			target_prop = "CritChance",
		}),
		PlaceObj('CaliberModification', {
			mod_add = -4,
			target_prop = "PenetrationClass",
		}),
	},
	AppliedEffects = {
		"Bleeding",
	},
	ammo_type_icon = "UI/Icons/Items/ta_hp.png",
}

