UndefineClass('_762WP_AP')
DefineClass._762WP_AP = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "Disabled",
	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/TEST.png",
	DisplayName = T(463284044008, --[[ModItemInventoryItemCompositeDef _762WP_AP DisplayName]] "7,62 мм СССР, Отключено"),
	DisplayNamePlural = T(521861768726, --[[ModItemInventoryItemCompositeDef _762WP_AP DisplayNamePlural]] "7,62 мм СССР, Отключено"),
	colorStyle = "AmmoAPColor",
	Description = T(910307381187, --[[ModItemInventoryItemCompositeDef _762WP_AP Description]] "7.62 Warsaw Pact ammo for Assault Rifles, SMGs, Machine Guns, and Rifles."),
	AdditionalHint = T(995857959547, --[[ModItemInventoryItemCompositeDef _762WP_AP AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Повышенная бронебойность"),
	Cost = 100,
	Tier = 2,
	MaxStock = 5,
	RestockWeight = 25,
	CategoryPair = "762WP",
	ShopStackSize = 30,
	MaxStacks = 60,
	Caliber = "",
	Modifications = {
		PlaceObj('CaliberModification', {
			mod_add = 2,
			target_prop = "PenetrationClass",
		}),
	},
	ammo_type_icon = "UI/Icons/Items/ta_ap.png",
}

