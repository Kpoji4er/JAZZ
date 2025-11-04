UndefineClass('JazzArmor_Sunglasses')
DefineClass.JazzArmor_Sunglasses = {
	__parents = { "Armor" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Armor",
	ScrapParts = 2,
	Degradation = 92,
	Icon = "Mod/e6L4ECj/ArmorIcons/Sunglasses.png",
	DisplayName = T(720354025816, "Солнцезащитные очки"),
	DisplayNamePlural = T(611720425604, "Солнцезащитные очки"),
	Description = T(126940066148, "Красивые и модные солнцезащитные очки. Мало того, что в солнечных очках наемник выглядит круче, так еще и, в качестве бонуса, очки могут поймать шальной осколок, предназначавшийся глазу."),
	AdditionalHint = T(424825139337, "Улучшают видимость днем, но ухудшают ночью"),
	Cost = 300,
	CanAppearInShop = true,
	MaxStock = 1,
	RestockWeight = 5,
	Slot = "HeadGear",
	PenetrationClass = 2,
	AdditionalReduction = 20,
	ProtectedBodyParts = set( "Head" ),
	Coverage = 20,
	ArmorRating = 2,
	NightVision = -10,
	Vision = 10,
	StunGrenadeProtection = 20,
	ArmorResource = 50,
	Repairability = 90,
}

