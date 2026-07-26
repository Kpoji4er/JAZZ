UndefineClass('FlareHandgun')
DefineClass.FlareHandgun = {
	__parents = { "FlareGun" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "FlareGun",
	ScrapParts = 2,
	RepairCost = 10,
	Reliability = 20,
	Icon = "UI/Icons/Weapons/FlareGun",
	ItemType = "FlareGun",
	DisplayName = T(335515845100, --[[ModItemInventoryItemCompositeDef FlareHandgun DisplayName]] "Flare Gun"),
	DisplayNamePlural = T(989166829697, --[[ModItemInventoryItemCompositeDef FlareHandgun DisplayNamePlural]] "Flare Guns"),
	Description = T(323491634965, --[[ModItemInventoryItemCompositeDef FlareHandgun Description]] "Single-shot breech-loading pistol you can use to light up the sky. "),
	AdditionalHint = T(323285392363, --[[ModItemInventoryItemCompositeDef FlareHandgun AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Освещает большую территорию\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Увеличенная дальность действия\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Бесшумное"),
	UnitStat = "Marksmanship",
	Valuable = 1,
	Cost = 600,
	CanAppearInShop = true,
	Tier = 2,
	Caliber = "JAZZ_Caliber_Flare",
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

