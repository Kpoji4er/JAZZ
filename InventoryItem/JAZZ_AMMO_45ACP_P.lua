UndefineClass('JAZZ_AMMO_45ACP_P')
DefineClass.JAZZ_AMMO_45ACP_P = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/45ACPP.png",
	DisplayName = T(911933649700, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_45ACP_P DisplayName]] ".45ACP, +P"),
	DisplayNamePlural = T(399199708303, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_45ACP_P DisplayNamePlural]] ".45ACP, +P"),
	colorStyle = "AmmoAPColor",
	Description = T(191747956366, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_45ACP_P Description]] "Усиленный патрон калибра .45ACP"),
	AdditionalHint = T(407662943532, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_45ACP_P AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Обеспечивает уверенное поражение целей обладающих 2-м классом брони\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Усиленный патрон: Увеличенная дальность, отдача и износ оружия. Уменьшенный урон"),
	Cost = 400,
	CanAppearInShop = true,
	MaxStock = 15,
	RestockWeight = 25,
	CategoryPair = "45ACP",
	ShopStackSize = 30,
	MaxStacks = 5000,
	Caliber = "JAZZ_Caliber_45ACP",
	Modifications = {
		PlaceObj('CaliberModification', {
			mod_mul = 950,
			target_prop = "Damage",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 1,
			target_prop = "PenetrationClass",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 2,
			target_prop = "Recoil",
		}),
		PlaceObj('CaliberModification', {
			mod_add = -10,
			target_prop = "Reliability",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 25,
			target_prop = "BaseJamChance",
		}),
		PlaceObj('CaliberModification', {
			mod_mul = 900,
			target_prop = "Grouping",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 2,
			target_prop = "WeaponRange",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 1,
			target_prop = "BulletDropRange",
		}),
	},
	AppliedEffects = {
		"Bleeding",
	},
	ammo_type_icon = "UI/Icons/Items/ta_hp.png",
}

