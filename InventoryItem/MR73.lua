UndefineClass('MR73')
DefineClass.MR73 = {
	__parents = { "Revolver" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "Tier 2-3",
	object_class = "Revolver",
	ScrapParts = 6,
	RepairCost = 6,
	Reliability = 95,
	Icon = "Mod/e6L4ECj/WeaponIcons/MR73.png",
	DisplayName = T(436628869426, --[[ModItemInventoryItemCompositeDef MR73 DisplayName]] "Manurhin MR 73"),
	DisplayNamePlural = T(427566606201, --[[ModItemInventoryItemCompositeDef MR73 DisplayNamePlural]] "Manurhin MR 73"),
	Description = T(878461703337, --[[ModItemInventoryItemCompositeDef MR73 Description]] "Штатный револьвер французской полиции и даже полицейского спезнаца. Качество изготовления ощутимо выше, чем у ширпотреба вроде револьверов Colt, так что на эту пушку вполен можно положиться в самый трудный момент."),
	AdditionalHint = T(434107786112, --[[ModItemInventoryItemCompositeDef MR73 AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Револьвер\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Магнум \n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Точный \n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Дальнобойный \n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Надежный \n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Удобный"),
	UnitStat = "Marksmanship",
	Cost = 500,
	CanAppearInShop = true,
	CategoryPair = "Handguns",
	Caliber = "JAZZ_Caliber_357",
	Damage = 29,
	ObjDamageMod = 40,
	AimAccuracy = 12,
	CritChanceScaled = 30,
	MagazineSize = 6,
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
	ReloadAP = 5000,
	Recoil = 1,
	AutoShots = 3,
	Handling = 17,
	BulletDropRange = 7,
	Grouping = 51,
	BaseJamChance = -100,
}

