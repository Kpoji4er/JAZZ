UndefineClass('AR15')
DefineClass.AR15 = {
	__parents = { "AssaultRifle" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "Убираем",
	object_class = "AssaultRifle",
	ScrapParts = 10,
	Reliability = 80,
	Icon = "UI/Icons/Weapons/AR15",
	DisplayName = T(360984219999, --[[ModItemInventoryItemCompositeDef AR15 DisplayName]] "ОТКЛЮЧЕНО"),
	DisplayNamePlural = T(952797707968, --[[ModItemInventoryItemCompositeDef AR15 DisplayNamePlural]] "ОТКЛЮЧЕНО"),
	Description = T(436294294475, --[[ModItemInventoryItemCompositeDef AR15 Description]] "Created to ensure the highest constitutional rights of self-defense and the possibility to bear a weapon that's easy as hell to convert to a fully-automatic one because a law-abiding citizen always needs one."),
	AdditionalHint = T(439737820334, --[[ModItemInventoryItemCompositeDef AR15 AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Высокий шанс критического попадания\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Низкая цена атаки\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Большое количество модулей\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> При установке стандартного приклада нет автоматического огня"),
	LargeItem = 1,
	UnitStat = "Marksmanship",
	Cost = 4500,
	Tier = 2,
	CategoryPair = "AssaultRifles",
	Caliber = "556",
	AimAccuracy = 4,
	CritChanceScaled = 30,
	MagazineSize = 30,
	WeaponRange = 34,
	OverwatchAngle = 1440,
	HandSlot = "TwoHanded",
	Entity = "Weapon_AR15",
	ComponentSlots = {
				PlaceObj('WeaponComponentSlot', {
			'SlotType', "Scope",
			'AvailableComponents', {
				"JAZZ_DefaultIronsight_AR15",
				"JAZZ_ImprovedIronsight_AR15",
			},
			'DefaultComponent', "JAZZ_DefaultIronsight_AR15",
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Magazine",
			'AvailableComponents', {
				"JAZZ_MagNormal",
				"JAZZ_MagNormalFine",
				"JAZZ_MagLarge",
				"JAZZ_MagLargeFine",
				"JAZZ_MagQuick",
			},
			'DefaultComponent', "JAZZ_MagNormal",
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Barrel",
			'AvailableComponents', {
				"JAZZ_BarrelNormal",
				"JAZZ_BarrelNormalImproved",
				"JAZZ_BarrelShort",
				"JAZZ_BarrelShortImproved",
				"JAZZ_BarrelLong",
				"JAZZ_BarrelLongImproved",
			},
			'DefaultComponent', "JAZZ_BarrelNormal",
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Stock",
			'AvailableComponents', {
				"StockHeavy_AR_BurstOnly",
				"StockLight_AR_BurstOnly",
				"StockBump",
			},
			'DefaultComponent', "StockHeavy_AR_BurstOnly",
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Under",
			'CanBeEmpty', true,
			'AvailableComponents', {
				"JAZZ_GrenadeLauncher",
				"JAZZ_VerticalGrip",
				"JAZZ_TacGrip",
			},
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Side",
			'CanBeEmpty', true,
			'AvailableComponents', {
				"JAZZ_Flashlight",
				"JAZZ_FlashlightDot",
				"JAZZ_LaserDot",
				"JAZZ_UVDot",
			},
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Muzzle",
			'CanBeEmpty', true,
			'AvailableComponents', {
				"JAZZ_Compensator",
				"JAZZ_ImprovisedSuppressor",
				"JAZZ_Suppressor",
				"JAZZ_MuzzleBooster",
			},
			'DefaultComponent', "JAZZ_Compensator",
		}),
	},
	HolsterSlot = "Shoulder",
	AvailableAttacks = {
		"BurstFire",
		"SingleShot",
		"CancelShot",
	},
	ShootAP = 5000,
	ReloadAP = 3000,
}

