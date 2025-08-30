UndefineClass('MP5')
DefineClass.MP5 = {
	__parents = { "SubmachineGun" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "Убираем",
	object_class = "SubmachineGun",
	ScrapParts = 8,
	Reliability = 85,
	Icon = "UI/Icons/Weapons/MP5",
	DisplayName = T(306337814252, --[[ModItemInventoryItemCompositeDef MP5 DisplayName]] "ОТКЛЮЧЕНО"),
	DisplayNamePlural = T(817935106307, --[[ModItemInventoryItemCompositeDef MP5 DisplayNamePlural]] "ОТКЛЮЧЕНО"),
	Description = T(505689462352, --[[ModItemInventoryItemCompositeDef MP5 Description]] "Пистолет-пулемет, которым пользуются контртеррористические подразделения и спецотряды полиции по всему миру. С момента выхода в серию в 60-х годах MP5 успел повидать многое, но широкая доступность бронежилетов и пистолетный 9-мм патрон постепенно снизили его популярность."),
	AdditionalHint = T(674835694740, --[[ModItemInventoryItemCompositeDef MP5 AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Увеличенная эффективность прицеливания\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Издает меньше шума"),
	LargeItem = 1,
	UnitStat = "Marksmanship",
	Cost = 2200,
	Tier = 2,
	RestockWeight = 60,
	CategoryPair = "SubmachineGuns",
	Caliber = "9mm",
	AimAccuracy = 5,
	MagazineSize = 30,
	WeaponRange = 22,
	OverwatchAngle = 1440,
	Noise = 10,
	HandSlot = "TwoHanded",
	Entity = "Weapon_MP5",
	ComponentSlots = {
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Under",
			'Modifiable', false,
			'AvailableComponents', {
				"MP5_Handguard",
			},
			'DefaultComponent', "MP5_Handguard",
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Barrel",
			'AvailableComponents', {
				"BarrelNormal",
				"BarrelLong",
			},
			'DefaultComponent', "BarrelNormal",
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Magazine",
			'AvailableComponents', {
				"MagNormal",
				"MagLarge",
				"MagQuick",
			},
			'DefaultComponent', "MagNormal",
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Stock",
			'AvailableComponents', {
				"StockNormal",
				"StockHeavy",
				"StockNo",
			},
			'DefaultComponent', "StockNormal",
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Side",
			'CanBeEmpty', true,
			'AvailableComponents', {
				"Flashlight",
				"LaserDot",
				"FlashlightDot",
			},
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Scope",
			'CanBeEmpty', true,
			'AvailableComponents', {
				"LROptics",
				"ReflexSight",
				"ReflexSightAdvanced",
				"ScopeCOG",
				"ScopeCOGQuick",
				"ThermalScope",
			},
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Muzzle",
			'CanBeEmpty', true,
			'AvailableComponents', {
				"Compensator",
				"Suppressor",
				"ImprovisedSuppressor",
			},
		}),
	},
	HolsterSlot = "Shoulder",
	AvailableAttacks = {
		"BurstFire",
		"AutoFire",
		"SingleShot",
		"RunAndGun",
		"CancelShot",
	},
	ShootAP = 5000,
	ReloadAP = 3000,
}

