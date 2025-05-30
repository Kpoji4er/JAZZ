UndefineClass('MR73')
DefineClass.MR73 = {
	__parents = { "Revolver" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "T1",
	object_class = "Revolver",
	ScrapParts = 6,
	RepairCost = 30,
	Reliability = 95,
	Icon = "Mod/e6L4ECj/WeaponIcons/ColtPeaceMaker.png",
	DisplayName = T(436628869426, --[[ModItemInventoryItemCompositeDef MR73 DisplayName]] "Manurhin MR 73"),
	DisplayNamePlural = T(427566606201, --[[ModItemInventoryItemCompositeDef MR73 DisplayNamePlural]] "Manurhin MR 73"),
	Description = T(878461703337, --[[ModItemInventoryItemCompositeDef MR73 Description]] "Старый, заслуженный револьвер одинарного действия, разработанный для армии США. Главное, носите c пустой каморой под курком, если не хотите лишиться ноги."),
	AdditionalHint = T(434107786112, --[[ModItemInventoryItemCompositeDef MR73 AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Револьвер - точный, надежный, но большие затраты ОД на выстрел и перезарядку"),
	UnitStat = "Marksmanship",
	Cost = 500,
	CanAppearInShop = true,
	CategoryPair = "Handguns",
	Caliber = "JAZZ_Caliber_38",
	Damage = 18,
	ObjDamageMod = 40,
	AimAccuracy = 8,
	CritChance = 5,
	CritChanceScaled = 30,
	MagazineSize = 6,
	WeaponRange = 15,
	OverwatchAngle = 5100,
	Noise = 32,
	Entity = "M73Base",
	ComponentSlots = {
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Freeswap",
			'AvailableComponents', {
				"Freeswap",
			},
			'DefaultComponent', "Freeswap",
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Barrel",
			'AvailableComponents', {
				"BarrelLong",
				"BarrelNormal",
			},
			'DefaultComponent', "BarrelNormal",
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Handgrip",
			'AvailableComponents', {
				"Handgrip_Default",
				"Handgrip_Ergo",
			},
			'DefaultComponent', "Handgrip_Default",
		}),
	},
	HolsterSlot = "Leg",
	AvailableAttacks = {
		"SingleShot",
		"DualShot",
		"CancelShot",
		"MobileShot",
	},
	ShootAP = 5000,
	ReloadAP = 8000,
	MaxAimActions = 2,
	Recoil = 1,
	AutoShots = 3,
	Handling = 94,
	BulletDropRange = 7,
	Grouping = 92,
	BaseJamChance = -100,
}

