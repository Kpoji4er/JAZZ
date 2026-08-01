UndefineClass('SWModel19')
DefineClass.SWModel19 = {
	__parents = { "Revolver" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "Tier 1-3",
	object_class = "Revolver",
	ScrapParts = 6,
	RepairCost = 2,
	Reliability = 95,
	Icon = "Mod/e6L4ECj/WeaponIcons/SWModel19.png",
	DisplayName = T(890000000000526, --[[ModItemInventoryItemCompositeDef SWModel19 DisplayName]] "S*W Model19 .357 Combat Magnum"),
	DisplayNamePlural = T(890000000000501, --[[ModItemInventoryItemCompositeDef SWModel19 DisplayNamePlural]] "SWModel19"),
	Description = T(890000000001231, --[[ModItemInventoryItemCompositeDef SWModel19 Description]] "Утяжеленная версия револьвера Miltary and Police, с упрочненной рамкой, необходимой для использования мощного патрона .357 Magnum. Выпускается с 1955 года. Это вам не кольтовский шлак, это оружие для настоящего дела.\n"),
	AdditionalHint = T(890000000000514, --[[ModItemInventoryItemCompositeDef SWModel19 AdditionalHint]] "Револьвер \n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Магнум \n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Точный"),
	UnitStat = "Marksmanship",
	Cost = 500,
	CanAppearInShop = true,
	CategoryPair = "Handguns",
	Caliber = "JAZZ_Caliber_357",
	Damage = 28,
	ObjDamageMod = 40,
	AimAccuracy = 16,
	CritChanceScaled = 30,
	MagazineSize = 6,
	WeaponRange = 17,
	OverwatchAngle = 5100,
	Noise = 28,
	Entity = "SW19",
	ComponentSlots = {
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Freeswap",
			'AvailableComponents', {
				"JAZZ_Freeswap",
			},
			'DefaultComponent', "JAZZ_Freeswap",
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Barrel",
			'AvailableComponents', {
				"JAZZ_BarrelLong",
				"JAZZ_BarrelNormal",
				"JAZZ_BarrelShort_Pistol",
			},
			'DefaultComponent', "JAZZ_BarrelNormal",
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
	},
	Color = "Default",
	HolsterSlot = "Leg",
	AvailableAttacks = {
		"SingleShot",
		"DualShot",
		"JAZZ_Fanning",
		"JAZZ_Bullseye",
	},
	ShootAP = 4000,
	ReloadAP = 5000,
	Recoil = 1,
	AutoShots = 3,
	BulletDropRange = 6,

	CloseRange = 0,

	CloseRangeFactor = 100,
	Grouping = 36,
	BaseJamChance = -100,
}

