UndefineClass('FiveSeven')
DefineClass.FiveSeven = {
	__parents = { "Pistol" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "Tier 3-5",
	object_class = "Pistol",
	ScrapParts = 6,
	RepairCost = 16,
	Reliability = 75,
	Icon = "Mod/e6L4ECj/WeaponIcons/57.png",
	DisplayName = T(937403994879, --[[ModItemInventoryItemCompositeDef FiveSeven DisplayName]] "FiveSeven"),
	DisplayNamePlural = T(559078272887, --[[ModItemInventoryItemCompositeDef FiveSeven DisplayNamePlural]] "FiveSeven"),
	Description = T(459458404676, --[[ModItemInventoryItemCompositeDef FiveSeven Description]] 'Пистолет  Five-seveN был разработан для подразделений армии в первую очередь и во вторую для полиции, для борьбы с защищенным противником "в пару" в автомату P90. Патроны с бронебойной пулей, однако, к свободной продаже запрещены, что существенно снижает ценность как пистолета, так и автомата в руках наемника.'),
	AdditionalHint = T(467503861152, --[[ModItemInventoryItemCompositeDef FiveSeven AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Топовый"),
	UnitStat = "Marksmanship",
	Cost = 20000,
	CanAppearInShop = true,
	Tier = 2,
	CategoryPair = "Handguns",
	Caliber = "JAZZ_Caliber_57",
	Damage = 20,
	ObjDamageMod = 25,
	AimAccuracy = 14,
	CritChanceScaled = 45,
	MagazineSize = 20,
	WeaponRange = 23,
	OverwatchAngle = 5400,
	Noise = 25,
	Entity = "Five_Seven",
	ComponentSlots = {
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Muzzle",
			'CanBeEmpty', true,
			'AvailableComponents', {
				"JAZZ_ImprovisedSuppressor",
				"JAZZ_PistolSuppressor",
			},
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Side",
			'CanBeEmpty', true,
			'AvailableComponents', {
				"JAZZ_Flashlight",
				"JAZZ_LaserDot",
				"JAZZ_UVDot",
				"JAZZ_FlashlightDot",
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
	Recoil = 1,
	AutoShots = 3,

	CloseRange = 0,

	CloseRangeFactor = 100,
	BulletDropRange = 10,
	Grouping = 45,
	BaseJamChance = -20,
	WeaponResource = 1800,
	CanAppearUsed = false,
}

