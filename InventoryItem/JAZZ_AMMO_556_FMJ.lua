UndefineClass('JAZZ_AMMO_556_FMJ')
DefineClass.JAZZ_AMMO_556_FMJ = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "FMJ - Плохого качества но массовые",
	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/556.png",
	DisplayName = T(574593171535, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_556_FMJ DisplayName]] "5,56мм, FMJ"),
	DisplayNamePlural = T(785279043850, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_556_FMJ DisplayNamePlural]] "5,56 мм, FMJ"),
	colorStyle = "AmmoBasicColor",
	Description = T(790646713962, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_556_FMJ Description]] "Стандартный боеприпас калибра 5.56x45мм."),
	AdditionalHint = T(733706073039, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_556_FMJ AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Обеспечивает уверенное поражение целей обладающих 2-м классом брони\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Патроны плохого качества: cниженный урон и повышенный износ"),
	Cost = 200,
	CanAppearInShop = true,
	Tier = 2,
	MaxStock = 5,
	RestockWeight = 50,
	CategoryPair = "556",
	ShopStackSize = 30,
	MaxStacks = 5000,
	Caliber = "JAZZ_Caliber_556",
	Modifications = {
		PlaceObj('CaliberModification', {
			mod_add = 1,
			target_prop = "PenetrationClass",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 1,
			mod_mul = 900,
			target_prop = "Damage",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 50,
			target_prop = "BaseJamChance",
		}),
		PlaceObj('CaliberModification', {
			mod_add = -2,
			target_prop = "WeaponRange",
		}),
		PlaceObj('CaliberModification', {
			mod_add = -1,
			target_prop = "BulletDropRange",
		}),
		PlaceObj('CaliberModification', {
			mod_mul = 800,
			target_prop = "Grouping",
		}),
	},
}

