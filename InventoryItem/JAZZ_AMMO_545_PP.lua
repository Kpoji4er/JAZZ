UndefineClass('JAZZ_AMMO_545_PP')
DefineClass.JAZZ_AMMO_545_PP = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "ПП - Бронебойные",
	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/545EPR.png",
	DisplayName = T(686371523176, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_545_PP DisplayName]] "5,45 мм, ПП"),
	DisplayNamePlural = T(173908119871, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_545_PP DisplayNamePlural]] "5,45 мм, ПП"),
	colorStyle = "AmmoEPRColor",
	Description = T(706390057843, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_545_PP Description]] "Российский патрон 7Н10 повышенной пробиваемости калибра 5.45x39мм"),
	AdditionalHint = T(230069004422, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_545_PP AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Обеспечивает уверенное поражение целей обладающих 3-м классом брони"),
	Cost = 700,
	CanAppearInShop = true,
	Tier = 2,
	MaxStock = 10,
	RestockWeight = 25,
	CategoryPair = "545",
	ShopStackSize = 30,
	MaxStacks = 90,
	Caliber = "JAZZ_Caliber_545",
	Modifications = {
		PlaceObj('CaliberModification', {
			mod_add = 2,
			target_prop = "PenetrationClass",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 1,
			target_prop = "WeaponRange",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 1,
			target_prop = "BulletDropRange",
		}),
	},
}

