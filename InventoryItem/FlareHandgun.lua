UndefineClass('FlareHandgun')
DefineClass.FlareHandgun = {
	__parents = { "FlareGun" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "FlareGun",
	ScrapParts = 2,
	RepairCost = 70,
	Reliability = 20,
	Icon = "UI/Icons/Weapons/FlareGun",
	ItemType = "FlareGun",
	DisplayName = T(114247712853, --[[ModItemInventoryItemCompositeDef FlareHandgun DisplayName]] "Ракетница"),
	DisplayNamePlural = T(465389331930, --[[ModItemInventoryItemCompositeDef FlareHandgun DisplayNamePlural]] "Ракетницы"),
	Description = T(424779764491, --[[ModItemInventoryItemCompositeDef FlareHandgun Description]] "Казнозарядный однозарядный пистолет, которым можно освещать территорию."),
	AdditionalHint = T(323285392363, --[[ModItemInventoryItemCompositeDef FlareHandgun AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Освещает большую территорию\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Увеличенная дальность действия\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Бесшумное"),
	UnitStat = "Marksmanship",
	Valuable = 1,
	Cost = 600,
	CanAppearInShop = true,
	Tier = 2,
	Caliber = "Flare",
	ObjDamageMod = 0,
	CritChanceScaled = 0,
	WeaponRange = 35,
	OverwatchAngle = 2160,
	Noise = 3,
	Entity = "Weapon_FlareGun",
	HolsterSlot = "Leg",
	PreparedAttackType = "None",
	AvailableAttacks = {
		"FireFlare",
	},
	MinMishapChance = 20,
	MaxMishapChance = 60,
}

