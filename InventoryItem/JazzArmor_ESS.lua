UndefineClass('JazzArmor_ESS')
DefineClass.JazzArmor_ESS = {
	__parents = { "Armor" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Armor",
	ScrapParts = 2,
	Degradation = 12,
	Icon = "Mod/e6L4ECj/ArmorIcons/ESS.png",
	DisplayName = T(818181029760, --[[ModItemInventoryItemCompositeDef JazzArmor_ESS DisplayName]] "Баллистические очки"),
	DisplayNamePlural = T(172943455971, --[[ModItemInventoryItemCompositeDef JazzArmor_ESS DisplayNamePlural]] "Баллистические очки"),
	Description = T(418612382041, --[[ModItemInventoryItemCompositeDef JazzArmor_ESS Description]] "Профессиональные баллистические противоосколочные очки. В бою или на полигоне, обеспечивают максимально возможную защиту для глаз. Помните, глаза у вас всего два, шансов на ошибку очень мало."),
	AdditionalHint = T(806826966692, --[[ModItemInventoryItemCompositeDef JazzArmor_ESS AdditionalHint]] "Защита для глаз во время песчанных бурь"),
	Cost = 1200,
	CanAppearInShop = true,
	Tier = 1,
	RestockWeight = 120,
	Slot = "HeadGear",
	AdditionalReduction = 20,
	ProtectedBodyParts = set( "Head" ),
	Coverage = 20,
	ArmorRating = 4,
	DustStormProtection = 30,
	StunGrenadeProtection = 80,
	Repairability = 60,
}

