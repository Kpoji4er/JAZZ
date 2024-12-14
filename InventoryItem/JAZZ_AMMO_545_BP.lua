UndefineClass('JAZZ_AMMO_545_BP')
DefineClass.JAZZ_AMMO_545_BP = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "БП - Супербронебойные",
	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/545AP.png",
	DisplayName = T(157788838717, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_545_BP DisplayName]] "5,45 мм, БП"),
	DisplayNamePlural = T(972063049608, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_545_BP DisplayNamePlural]] "5,45 мм, БП"),
	colorStyle = "AmmoAPColor",
	Description = T(109043157088, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_545_BP Description]] "Бронебойный армейский патрон калибра 7Н22 5.45x39мм"),
	AdditionalHint = T(992250786186, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_545_BP AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Обеспечивает уверенное поражение целей обладающих 4-м классом брони"),
	CanAppearInShop = true,
	Tier = 3,
	RestockWeight = 25,
	CategoryPair = "545",
	ShopStackSize = 30,
	MaxStacks = 5000,
	Caliber = "JAZZ_Caliber_545",
	Modifications = {
		PlaceObj('CaliberModification', {
			mod_add = 3,
			target_prop = "PenetrationClass",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 1,
			target_prop = "WeaponRange",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 2,
			target_prop = "BulletDropRange",
		}),
	},
}

