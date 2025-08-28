UndefineClass('_9mm_AP')
DefineClass._9mm_AP = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/TEST.png",
	DisplayName = T(202438707540, "9х19 мм, ББ"),
	DisplayNamePlural = T(285785210544, "9х19 мм, ББ"),
	colorStyle = "AmmoEPRColor",
	Description = T(815815988039, "Бронебойный патрон калибра 9х19мм"),
	AdditionalHint = T(280553686223, "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Обеспечивает уверенное поражение целей обладающих 2-м классом брони"),
	Cost = 250,
	MaxStock = 20,
	RestockWeight = 25,
	CategoryPair = "9mm",
	ShopStackSize = 30,
	MaxStacks = 5000,
	Caliber = "9mm",
	Modifications = {
		PlaceObj('CaliberModification', {
			mod_add = 1,
			target_prop = "PenetrationClass",
		}),
	},
	ammo_type_icon = "UI/Icons/Items/ta_ap.png",
}

