UndefineClass('JAZZ_AMMO_762x51_M61')
DefineClass.JAZZ_AMMO_762x51_M61 = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "M61 - Бронебойные",
	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/762NATOM61.png",
	DisplayName = T(213865838245, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_762x51_M61 DisplayName]] "7.62х51мм НАТО, M61"),
	DisplayNamePlural = T(732360181829, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_762x51_M61 DisplayNamePlural]] "7.62х51мм НАТО, M61"),
	colorStyle = "AmmoAPColor",
	Description = T(134217744335, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_762x51_M61 Description]] "Бронебойный армейский патрон М61 калибра 7.62х51мм НАТО"),
	AdditionalHint = T(887338728380, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_762x51_M61 AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Повышенная бронебойность\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Обеспечивает уверенное поражение целей обладающих 4-м классом брони"),
	Cost = 200,
	CanAppearInShop = true,
	Tier = 3,
	MaxStock = 15,
	RestockWeight = 25,
	CategoryPair = "762NATO",
	ShopStackSize = 30,
	MaxStacks = 5000,
	Caliber = "JAZZ_Caliber_762x51",
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
			mod_add = 1,
			target_prop = "BulletDropRange",
		}),
	},
	ammo_type_icon = "UI/Icons/Items/ta_ap.png",
}

