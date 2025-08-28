UndefineClass('_556_Match')
DefineClass._556_Match = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "Disabled",
	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/TEST.png",
	DisplayName = T(122093727509, "556Match ОТКЛЮЧЕНО"),
	DisplayNamePlural = T(209259965707, "556Match ОТКЛЮЧЕНО"),
	colorStyle = "AmmoMatchColor",
	Description = T(227822258303, "Матчевый боеприпас для автоматов, пистолетов-пулеметов и пулеметов калибра 5,56 мм."),
	AdditionalHint = T(137980565501, "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Увеличенная эффективность прицеливания"),
	Cost = 180,
	Tier = 3,
	MaxStock = 5,
	RestockWeight = 25,
	CategoryPair = "556",
	ShopStackSize = 30,
	MaxStacks = 500,
	Caliber = "",
	Modifications = {
		PlaceObj('CaliberModification', {
			mod_mul = 0,
			target_prop = "Damage",
		}),
	},
	ammo_type_icon = "UI/Icons/Items/ta_match.png",
}

