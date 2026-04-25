UndefineClass('P220')
DefineClass.P220 = {
	__parents = { "Pistol" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "Tier3-1",
	object_class = "Pistol",
	ScrapParts = 6,
	RepairCost = 7,
	Reliability = 80,
	Icon = "Mod/e6L4ECj/WeaponIcons/P220.png",
	DisplayName = T(291513194954, --[[ModItemInventoryItemCompositeDef P220 DisplayName]] "P-220"),
	DisplayNamePlural = T(336303546958, --[[ModItemInventoryItemCompositeDef P220 DisplayNamePlural]] "P-220"),
	Description = T(977047112542, --[[ModItemInventoryItemCompositeDef P220 Description]] "Если вам требуется хороший пистолет, первым в очереди из претендентов всегда будет стоять пистолет из Швейцарии. Там принято делать простое и надежное оружие. Конечно, там еще принято делать простое и надежное дорогое оружие, но для себя не жаль никаких денег."),
	AdditionalHint = T(541758722141, --[[ModItemInventoryItemCompositeDef P220 AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Точный\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Удобный\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Надежный\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> И-иии все"),
	UnitStat = "Marksmanship",
	Cost = 2200,
	CanAppearInShop = true,
	CategoryPair = "Handguns",
	Caliber = "JAZZ_Caliber_45ACP",
	Damage = 30,
	ObjDamageMod = 25,
	AimAccuracy = 9,
	CritChanceScaled = 40,
	MagazineSize = 8,
	WeaponRange = 16,
	OverwatchAngle = 5400,
	Noise = 28,
	Entity = "P220",
	ComponentSlots = {
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Magazine",
			'AvailableComponents', {
				"MagNormal",
				"MagLarge_8_10",
			},
			'DefaultComponent', "MagNormal",
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Muzzle",
			'CanBeEmpty', true,
			'AvailableComponents', {
				"ImprovisedSuppressor",
				"PistolSuppressor",
			},
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Side",
			'CanBeEmpty', true,
			'AvailableComponents', {
				"Flashlight",
				"LaserDot",
				"UVDot",
				"FlashlightDot",
			},
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Scope",
			'AvailableComponents', {
				"Jazz_IronSight",
				"JAZZ_Reflex_Pistol",
			},
			'DefaultComponent', "Jazz_IronSight",
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Freeswap",
			'AvailableComponents', {
				"Freeswap",
			},
			'DefaultComponent', "Freeswap",
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
	ShootAP = 3000,
	ReloadAP = 3000,
	MaxAimActions = 2,
	Recoil = 1,
	AutoShots = 3,
	Handling = 20,
	BulletDropRange = 7,
	Grouping = 55,
	BaseJamChance = -20,
	WeaponResource = 1800,
}

