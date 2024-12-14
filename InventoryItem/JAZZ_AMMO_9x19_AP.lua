UndefineClass('JAZZ_AMMO_9x19_AP')
DefineClass.JAZZ_AMMO_9x19_AP = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/919AP.png",
	DisplayName = T(469395250369, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_9x19_AP DisplayName]] "9х19 мм, ББ"),
	DisplayNamePlural = T(997988678362, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_9x19_AP DisplayNamePlural]] "9х19 мм, ББ"),
	colorStyle = "AmmoEPRColor",
	Description = T(482446833075, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_9x19_AP Description]] "Бронебойный патрон калибра 9х19мм"),
	AdditionalHint = T(612023201301, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_9x19_AP AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Обеспечивает уверенное поражение целей обладающих 2-м классом брони"),
	Cost = 250,
	CanAppearInShop = true,
	MaxStock = 20,
	RestockWeight = 25,
	CategoryPair = "9mm",
	ShopStackSize = 30,
	MaxStacks = 5000,
	Caliber = "JAZZ_Caliber_9x19",
	Modifications = {
		PlaceObj('CaliberModification', {
			mod_add = 1,
			target_prop = "PenetrationClass",
		}),
	},
	ammo_type_icon = "UI/Icons/Items/ta_ap.png",
}

