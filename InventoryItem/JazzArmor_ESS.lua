UndefineClass('JazzArmor_ESS')
DefineClass.JazzArmor_ESS = {
	__parents = { "Armor" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Armor",
	ScrapParts = 2,
	Degradation = 12,
	Icon = "Mod/e6L4ECj/ArmorIcons/ESS.png",
	DisplayName = T(818181029760, "Баллистические очки"),
	DisplayNamePlural = T(172943455971, "Баллистические очки"),
	Description = T(418612382041, "Профессиональные баллистические противоосколочные очки. В бою или на полигоне, обеспечивают максимально возможную защиту для глаз. Помните, глаза у вас всего два, шансов на ошибку очень мало."),
	AdditionalHint = T(806826966692, "Защита для глаз во время песчанных бурь"),
	Cost = 3000,
	CanAppearInShop = true,
	Tier = 2,
	RestockWeight = 15,
	Slot = "HeadGear",
	AdditionalReduction = 20,
	ProtectedBodyParts = set( "Head" ),
	Coverage = 20,
	ArmorRating = 4,
	DustStormProtection = 30,
	StunGrenadeProtection = 80,
	Repairability = 60,
}

