UndefineClass('JAZZ_AMMO_12gauge_APSlug')
DefineClass.JAZZ_AMMO_12gauge_APSlug = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "Пуля ББ - 1 шт",
	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/12gAPSLUG.png",
	DisplayName = T(900455292533, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_12gauge_APSlug DisplayName]] "12-й калибр, ББ Пуля"),
	DisplayNamePlural = T(527580122468, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_12gauge_APSlug DisplayNamePlural]] "12-й калибр, ББ Пуля"),
	colorStyle = "AmmoAPColor",
	Description = T(476217082330, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_12gauge_APSlug Description]] "Бронебойная пуля 12-го калибра."),
	AdditionalHint = T(772311577161, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_12gauge_APSlug AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> 1 пуля.\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Обеспечивает уверенное поражение целей обладающих 3-м классом брони\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Увеличенная дальность и урон, но меньше чем у обычной пули"),
	Cost = 500,
	CanAppearInShop = true,
	Tier = 2,
	MaxStock = 5,
	RestockWeight = 80,
	ShopStackSize = 12,
	MaxStacks = 5000,
	Caliber = "JAZZ_Caliber_12gauge",
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
			mod_add = 2,
			target_prop = "PenetrationClass",
		}),
		PlaceObj('CaliberModification', {
			mod_mul = 500,
			target_prop = "ObjDamageMod",
		}),
		PlaceObj('CaliberModification', {
			mod_mul = 3000,
			target_prop = "Grouping",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 5,
			mod_mul = 0,
			target_prop = "BulletDropRange",
		}),
	},
	ammo_type_icon = "UI/Icons/Items/ta_ap.png",
}

