UndefineClass('JazzArmor_NVG2')
DefineClass.JazzArmor_NVG2 = {
	__parents = { "NightVisionGoggles" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "NightVisionGoggles",
	Icon = "Mod/e6L4ECj/ArmorIcons/NVG2.png",
	DisplayName = T(641611416781, "AN/PVS-7"),
	DisplayNamePlural = T(314187072777, "AN/PVS-7"),
	Description = T(925462880253, "Прибор ночного видения второго поколения менее чувсвителен к паразитной засветке, и, к тому же, имеет встроенную инфракрасную подсветку, позволяющую получать изображения в отсутствие естественного света вовсе."),
	AdditionalHint = T(533537838532, "Прибор ночного зрения второго поколения"),
	Cost = 15000,
	CanAppearInShop = true,
	Tier = 3,
	RestockWeight = 1,
	PenetrationClass = 2,
	AdditionalReduction = 20,
	NightVision = 40,
	StunGrenadeProtection = -20,
	ArmorResource = 200,
}

