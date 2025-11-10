UndefineClass('JAZZ_AMMO_12gauge_Slug')
DefineClass.JAZZ_AMMO_12gauge_Slug = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "Пуля - 1 шт",
	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/12gSLUG.png",
	DisplayName = T(456378254088, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_12gauge_Slug DisplayName]] "12-й калибр, Пуля"),
	DisplayNamePlural = T(924683101088, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_12gauge_Slug DisplayNamePlural]] "12-й калибр, Пуля"),
	colorStyle = "AmmoMatchColor",
	Description = T(267219596717, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_12gauge_Slug Description]] "Пуля 12-го калибра."),
	AdditionalHint = T(223088775151, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_12gauge_Slug AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> 1 пуля.\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Обеспечивает уверенное поражение целей обладающих 2-м классом брони\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Увеличенная дальность и урон"),
	Cost = 1800,
	CanAppearInShop = true,
	MaxStock = 20,
	RestockWeight = 10,
	ShopStackSize = 25,
	MaxStacks = 20,
	Caliber = "JAZZ_Caliber_12gauge",
	Modifications = {
		PlaceObj('CaliberModification', {
			mod_mul = 500,
			target_prop = "OverwatchAngle",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 15,
			target_prop = "WeaponRange",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 40,
			target_prop = "Damage",
		}),
		PlaceObj('CaliberModification', {
			mod_mul = 500,
			target_prop = "ObjDamageMod",
		}),
		PlaceObj('CaliberModification', {
			mod_mul = 2000,
			target_prop = "Grouping",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 8,
			mod_mul = 0,
			target_prop = "BulletDropRange",
		}),
		PlaceObj('CaliberModification', {
			target_prop = "PenetrationClass",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 5,
			target_prop = "PenetrationBonus",
		}),
		PlaceObj('CaliberModification', {
			mod_mul = 950,
			target_prop = "Grouping",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 25,
			target_prop = "CritChance",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 120,
			target_prop = "BaseJamChance",
		}),
	},
	ammo_type_icon = "UI/Icons/Items/ta_match.png",
}

