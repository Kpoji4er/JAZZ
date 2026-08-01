UndefineClass('Glock17')
DefineClass.Glock17 = {
	__parents = { "Pistol" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "Tier 2-5",
	object_class = "Pistol",
	ScrapParts = 6,
	RepairCost = 12,
	Reliability = 95,
	Icon = "Mod/e6L4ECj/WeaponIcons/Glock17.png",
	DisplayName = T(464861298445, --[[ModItemInventoryItemCompositeDef Glock17 DisplayName]] "Glock 17"),
	DisplayNamePlural = T(134481114957, --[[ModItemInventoryItemCompositeDef Glock17 DisplayNamePlural]] "Glock 17"),
	Description = T(219478192607, --[[ModItemInventoryItemCompositeDef Glock17 Description]] "Пистолет, который, как мы знаем из голливудских фильмов, выдерживает падение с крыши 100 этажного дома, не ловится детекторами в аэропорту, может быть изготовлен в любом гараже на 3D принтере."),
	AdditionalHint = T(593063289584, --[[ModItemInventoryItemCompositeDef Glock17 AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Быстрый\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Компактный\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Удобный\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Прочный\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Из 1970-х"),
	UnitStat = "Marksmanship",
	Cost = 7000,
	CanAppearInShop = true,
	Tier = 2,
	RestockWeight = 40,
	CategoryPair = "Handguns",
	Caliber = "JAZZ_Caliber_9x19",
	Damage = 21,
	ObjDamageMod = 15,
	AimAccuracy = 3,
	MagazineSize = 17,
	WeaponRange = 19,
	OverwatchAngle = 5400,
	Noise = 22,
	Entity = "Glock_17",
	ComponentSlots = {
				PlaceObj('WeaponComponentSlot', {
			'SlotType', "Muzzle",
			'CanBeEmpty', true,
			'AvailableComponents', {
				"JAZZ_ImprovisedSuppressor",
				"JAZZ_PistolSuppressor",
				"JAZZ_Compensator",
			},
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Magazine",
			'AvailableComponents', {
				"JAZZ_MagLarge",
				"JAZZ_MagNormal",
				"JAZZ_MagNormalG18",
			},
			'DefaultComponent', "JAZZ_MagNormal",
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Side",
			'CanBeEmpty', true,
			'AvailableComponents', {
				"JAZZ_Flashlight",
				"JAZZ_LaserDot",
				"JAZZ_FlashlightDot",
				"JAZZ_UVDot",
			},
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Freeswap",
			'AvailableComponents', {
				"JAZZ_Freeswap",
			},
			'DefaultComponent', "JAZZ_Freeswap",
		}),
	},
	HolsterSlot = "Leg",
	AvailableAttacks = {
		"SingleShot",
		"DualShot",
		"MobileShot",
		"JAZZ_Mozambique",
		"JAZZ_DoubleTap",
	},
	ShootAP = 2000,
	ReloadAP = 3000,
	MaxAimActions = 2,
	Recoil = 9,
	BurstShots = 1,
	AutoShots = 1,

	CloseRange = 0,

	CloseRangeFactor = 100,
	BulletDropRange = 8,
	Grouping = 75,
	BaseJamChance = -20,
	WeaponResource = 2400,
	CanAppearUsed = false,
}

