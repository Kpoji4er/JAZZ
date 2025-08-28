UndefineClass('_556_Basic')
DefineClass._556_Basic = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "FMJ - Плохого качества но массовые",
	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/TEST.png",
	DisplayName = T(712257416279, "5,56мм, FMJ"),
	DisplayNamePlural = T(581495951953, "5,56 мм, FMJ"),
	colorStyle = "AmmoBasicColor",
	Description = T(615590868211, "Стандартный боеприпас калибра 5.56x45мм."),
	AdditionalHint = T(279942058199, "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Обеспечивает уверенное поражение целей обладающих 2-м классом брони\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Патроны плохого качества: cниженный урон и повышенный износ"),
	Cost = 200,
	Tier = 2,
	MaxStock = 5,
	RestockWeight = 50,
	CategoryPair = "556",
	ShopStackSize = 30,
	MaxStacks = 5000,
	Caliber = "556",
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
			mod_add = -5,
			target_prop = "Reliability",
		}),
	},
}

