UndefineClass('JAZZ_AMMO_556_MK262')
DefineClass.JAZZ_AMMO_556_MK262 = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "Mk 262 - Элитные с кучей бафов",
	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/556HP.png",
	DisplayName = T(685583532964, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_556_MK262 DisplayName]] "5,56 мм, Mk262"),
	DisplayNamePlural = T(563192097250, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_556_MK262 DisplayNamePlural]] "5,56 мм, Mk262"),
	colorStyle = "AmmoHPColor",
	Description = T(886365993358, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_556_MK262 Description]] "Специальный боеприпас калибра 5.56x45мм. Разработан для сил специального назначения"),
	AdditionalHint = T(402125498672, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_556_MK262 AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Обеспечивает уверенное поражение целей обладающих 3-м классом брони\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Высокий шанс критического попадания\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Повышенный урон\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Увеличенная эффективность прицеливания"),
	Cost = 1200,
	CanAppearInShop = true,
	Tier = 3,
	CategoryPair = "556",
	ShopStackSize = 30,
	MaxStacks = 5000,
	Caliber = "JAZZ_Caliber_556",
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
			mod_mul = 1200,
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

