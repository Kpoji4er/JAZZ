UndefineClass('JazzArmor_NVG1')
DefineClass.JazzArmor_NVG1 = {
	__parents = { "NightVisionGoggles" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "NightVisionGoggles",
	Icon = "Mod/e6L4ECj/ArmorIcons/NVG1.png",
	DisplayName = T(671049962372, "AN/PVS-5"),
	DisplayNamePlural = T(538496112994, "AN/PVS-5"),
	Description = T(142817437025, "Очки ночного зрения первого поколения, работающие на принципе усиления естественного освещения. Из-за чего при случайной засветке выключаются, чтоб не ослепить носителя."),
	AdditionalHint = T(506440911304, "Прибор ночного зрения первого поколения"),
	Cost = 5000,
	CanAppearInShop = true,
	RestockWeight = 1,
	PenetrationClass = 2,
	AdditionalReduction = 20,
	NightVision = 20,
	StunGrenadeProtection = -20,
	Repairability = 70,
}

