UndefineClass('Colt38Special')
DefineClass.Colt38Special = {
	__parents = { "Revolver" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "Tier 1-2",
	object_class = "Revolver",
	ScrapParts = 6,
	RepairCost = 1,
	Reliability = 95,
	Icon = "Mod/e6L4ECj/WeaponIcons/38sp.png",
	DisplayName = T(890000000000521, --[[ModItemInventoryItemCompositeDef Colt38Special DisplayName]] "Colt .38 Special"),
	DisplayNamePlural = T(890000000000497, --[[ModItemInventoryItemCompositeDef Colt38Special DisplayNamePlural]] "Colt .38 Special"),
	Description = T(563384549909, --[[ModItemInventoryItemCompositeDef Colt38Special Description]] "Компактный и легкий полицейский револьвер калибра 9мм. Стальная рамка, спуск двойного действия сделали его одним из самых популярных вариантов оружия для самообороны в США."),
	AdditionalHint = T(460566737568, --[[ModItemInventoryItemCompositeDef Colt38Special AdditionalHint]] "Револьвер \n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> .38 Special Компактный \n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Надежный"),
	UnitStat = "Marksmanship",
	Cost = 500,
	CanAppearInShop = true,
	CategoryPair = "Handguns",
	Caliber = "JAZZ_Caliber_38",
	Damage = 16,
	ObjDamageMod = 40,
	AimAccuracy = 10,
	CritChanceScaled = 30,
	MagazineSize = 6,
	WeaponRange = 15,
	OverwatchAngle = 5100,
	Noise = 12,
	Entity = "38Special",
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
				"JAZZ_BarrelShort_Pistol",
			},
			'DefaultComponent', "JAZZ_BarrelShort_Pistol",
		}),
	},
	HolsterSlot = "Leg",
	AvailableAttacks = {
		"SingleShot",
		"DualShot",
		"JAZZ_Fanning",
		"JAZZ_Bullseye",
	},
	ShootAP = 3000,
	ReloadAP = 5000,
	Recoil = 1,
	AutoShots = 3,

	CloseRange = 0,

	CloseRangeFactor = 100,
	BulletDropRange = 5,
	Grouping = 59,
	BaseJamChance = -100,
}

