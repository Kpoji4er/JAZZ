UndefineClass('JAZZ_AMMO_762x39_FMJ')
DefineClass.JAZZ_AMMO_762x39_FMJ = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "Китайские - чуть хуже по урону и пробитию",
	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/762x39CHN.png",
	DisplayName = T(403807663771, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_762x39_FMJ DisplayName]] "7,62х39мм, FMJ"),
	DisplayNamePlural = T(578647545074, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_762x39_FMJ DisplayNamePlural]] "7,62х39мм, FMJ"),
	colorStyle = "AmmoBasicColor",
	Description = T(296646736495, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_762x39_FMJ Description]] "Китайский патрон калибра 7.62х39. Уступает советским аналогам"),
	AdditionalHint = T(751436259794, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_762x39_FMJ AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Обеспечивает уверенное поражение целей обладающих 2-м классом брони\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Патроны низкого качества: пониженный урон, уменьшенная дальность, уменьшенная точность, увеличенный износ"),
	Cost = 100,
	CanAppearInShop = true,
	RestockWeight = 150,
	CategoryPair = "762WP",
	ShopStackSize = 30,
	MaxStacks = 5000,
	Caliber = "JAZZ_Caliber_762x39",
	Modifications = {
		PlaceObj('CaliberModification', {
			mod_mul = 850,
			target_prop = "Damage",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 1,
			target_prop = "PenetrationClass",
		}),
		PlaceObj('CaliberModification', {
			mod_add = -10,
			target_prop = "Reliability",
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
		"Bleeding",
	},
	ammo_type_icon = "UI/Icons/Items/ta_hp.png",
}

