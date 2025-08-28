UndefineClass('_762WP_Match')
DefineClass._762WP_Match = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "Disabled",
	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/TEST.png",
	DisplayName = T(547619038333, "7,62 мм СССР, МТЧ"),
	DisplayNamePlural = T(229974779565, "7,62 мм СССР, МТЧ"),
	colorStyle = "AmmoMatchColor",
	Description = T(233053065977, "Матчевый боеприпас советского образца для автоматов, пистолетов-пулеметов, пулеметов и винтовок калибра 7,62 мм."),
	AdditionalHint = T(664395917370, "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Увеличенная эффективность прицеливания"),
	Cost = 100,
	Tier = 3,
	MaxStock = 5,
	RestockWeight = 25,
	CategoryPair = "762WP",
	ShopStackSize = 30,
	MaxStacks = 5000,
	Caliber = "",
	Modifications = {
		PlaceObj('CaliberModification', {
			mod_mul = 0,
			target_prop = "Damage",
		}),
	},
	ammo_type_icon = "UI/Icons/Items/ta_match.png",
}

