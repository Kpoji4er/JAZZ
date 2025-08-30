UndefineClass('_556_HP')
DefineClass._556_HP = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "Mk 262 - Элитные с кучей бафов",
	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/TEST.png",
	DisplayName = T(492297603072, --[[ModItemInventoryItemCompositeDef _556_HP DisplayName]] "5,56 мм, Mk262"),
	DisplayNamePlural = T(591574262194, --[[ModItemInventoryItemCompositeDef _556_HP DisplayNamePlural]] "5,56 мм, Mk262"),
	colorStyle = "AmmoHPColor",
	Description = T(206632323405, --[[ModItemInventoryItemCompositeDef _556_HP Description]] "Специальный боеприпас калибра 5.56x45мм. Разработан для сил специального назначения"),
	AdditionalHint = T(895810063260, --[[ModItemInventoryItemCompositeDef _556_HP AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Обеспечивает уверенное поражение целей обладающих 3-м классом брони\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Высокий шанс критического попадания\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Повышенный урон\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Увеличенная эффективность прицеливания"),
	Cost = 1200,
	Tier = 3,
	CategoryPair = "556",
	ShopStackSize = 30,
	MaxStacks = 5000,
	Caliber = "556",
	Modifications = {
		PlaceObj('CaliberModification', {
			mod_add = 50,
			target_prop = "CritChance",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 1,
			mod_mul = 1100,
			target_prop = "Damage",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 3,
			target_prop = "PenetrationClass",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 2,
			target_prop = "AimAccuracy",
		}),
	},
	AppliedEffects = {
		"Bleeding",
	},
	ammo_type_icon = "UI/Icons/Items/ta_hp.png",
}

