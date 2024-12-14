UndefineClass('JAZZ_AMMO_762x54_BZT')
DefineClass.JAZZ_AMMO_762x54_BZT = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "БЗТ - Бронебойные и экспансивные",
	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/762x54RBZT.png",
	DisplayName = T(907828676418, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_762x54_BZT DisplayName]] "7,62x54R мм БЗТ"),
	DisplayNamePlural = T(968086694447, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_762x54_BZT DisplayNamePlural]] "7,62x54R мм БЗТ"),
	colorStyle = "AmmoAPColor",
	Description = T(273361512171, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_762x54_BZT Description]] "Советский винтовочный бронебойно-зажитательный трассирующий боеприпас калибра 7.62х54мм с пулей 57-БЗТ-322"),
	AdditionalHint = T(954557097094, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_762x54_BZT AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Обеспечивает уверенное поражение целей обладающих 4-м классом брони\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Увеличенный износ оружия и урон. Уменьшенная точность\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Пораженные цели получают статус «<color EmStyle>Вне укрытия</color>» и лишаются его преимуществ\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Вызывает <color EmStyle>горение</color>"),
	Cost = 1500,
	CanAppearInShop = true,
	Tier = 3,
	MaxStock = 5,
	RestockWeight = 10,
	CategoryPair = "762x54",
	ShopStackSize = 30,
	MaxStacks = 5000,
	Caliber = "JAZZ_Caliber_762x54R",
	Modifications = {
		PlaceObj('CaliberModification', {
			mod_add = 3,
			target_prop = "PenetrationClass",
		}),
		PlaceObj('CaliberModification', {
			mod_mul = 1300,
			target_prop = "Damage",
		}),
		PlaceObj('CaliberModification', {
			mod_add = -10,
			target_prop = "Reliability",
		}),
		PlaceObj('CaliberModification', {
			mod_mul = 1200,
			target_prop = "ObjDamageMod",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 50,
			target_prop = "BaseJamChance",
		}),
		PlaceObj('CaliberModification', {
			mod_mul = 800,
			target_prop = "Grouping",
		}),
	},
	AppliedEffects = {
		"Burning",
		"Bleeding",
	},
}

