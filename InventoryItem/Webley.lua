UndefineClass('Webley')
DefineClass.Webley = {
	__parents = { "Revolver" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "Tier 2-1",
	object_class = "Revolver",
	ScrapParts = 6,
	RepairCost = 3,
	Reliability = 95,
	Icon = "Mod/e6L4ECj/WeaponIcons/Webley.png",
	DisplayName = T(890000000000528, --[[ModItemInventoryItemCompositeDef Webley DisplayName]] "Webley Mk VI"),
	DisplayNamePlural = T(890000000000504, --[[ModItemInventoryItemCompositeDef Webley DisplayNamePlural]] "Webley Mk VI"),
	Description = T(890000000001225, --[[ModItemInventoryItemCompositeDef Webley Description]] 'Основной револьвер британских вооруженных сил в период ПМВ и даже ВМВ. Имеет компоновку с "переламывающейся" рамкой, что конечно позволяет быстро и эффектно перезаряжаться, но снижает прочность конструкции. Так, что даже .38 й патрон для Вебли - крепковат.'),
	AdditionalHint = T(890000000000515, --[[ModItemInventoryItemCompositeDef Webley AdditionalHint]] "Револьвер \n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Сорок пятый \n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Британский"),
	UnitStat = "Marksmanship",
	Cost = 500,
	CanAppearInShop = true,
	CategoryPair = "Handguns",
	Caliber = "JAZZ_Caliber_45ACP",
	Damage = 27,
	ObjDamageMod = 40,
	AimAccuracy = 9,
	CritChanceScaled = 30,
	MagazineSize = 6,
	WeaponRange = 16,
	OverwatchAngle = 5100,
	Noise = 28,
	Entity = "Webleyf",
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
				"JAZZ_BarrelNormal",
				"JAZZ_BarrelLong",
			},
			'DefaultComponent', "JAZZ_BarrelNormal",
		}),
	},
	HolsterSlot = "Leg",
	AvailableAttacks = {
		"SingleShot",
		"DualShot",
		"JAZZ_Fanning",
		"JAZZ_Bullseye",
	},
	ShootAP = 4000,
	ReloadAP = 4000,
	Recoil = 1,
	AutoShots = 3,

	CloseRange = 0,

	CloseRangeFactor = 100,
	BulletDropRange = 4,
	Grouping = 88,
	BaseJamChance = -100,
}

