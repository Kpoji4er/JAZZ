UndefineClass('M1Garand')
DefineClass.M1Garand = {
	__parents = { "BattleRifle" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "Tier 1-2",
	object_class = "BattleRifle",
	ScrapParts = 8,
	RepairCost = 6,
	Reliability = 60,
	Icon = "Mod/e6L4ECj/WeaponIcons/M1Garand.png",
	DisplayName = T(890000000000972, --[[ModItemInventoryItemCompositeDef M1Garand DisplayName]] "М1 Гаранд"),
	DisplayNamePlural = T(890000000001121, --[[ModItemInventoryItemCompositeDef M1Garand DisplayNamePlural]] "М1 Гаранд"),
	Description = T(890000000001052, --[[ModItemInventoryItemCompositeDef M1Garand Description]] "Американская винтовка М1 конструкции канадца Джона Гаранда занимает достойное место в истории стрелкового оружия как первая самозарядная немагазинная винтовка, принятая на вооружение в качестве основного индивидуального оружия пехоты."),
	AdditionalHint = T(890000000000694, --[[ModItemInventoryItemCompositeDef M1Garand AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Точный \n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Убойный \n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Неудобный \n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Гаранд бзынь!"),
	LargeItem = 1,
	UnitStat = "Marksmanship",
	Cost = 2000,
	CategoryPair = "Rifles",
	CanAppearStandard = false,
	Caliber = "JAZZ_Caliber_3006",
	Damage = 36,
	ObjDamageMod = 80,
	AimAccuracy = 14,
	CritChanceScaled = 30,
	MagazineSize = 8,
	WeaponRange = 60,
	OverwatchAngle = 900,
	Noise = 68,
	HandSlot = "TwoHanded",
	Entity = "Garand",
	ComponentSlots = {
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Scope",
			'AvailableComponents', {
				"JAZZ_Reflex_Garand",
				"JAZZ_Scope_Garand",
				"JAZZ_DefaultIronsight_AR15",
			},
			'DefaultComponent', "JAZZ_DefaultIronsight_AR15",
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Muzzle",
			'CanBeEmpty', true,
			'AvailableComponents', {
				"JAZZ_Suppressor",
			},
		}),
	},
	HolsterSlot = "Shoulder",
	ModifyRightHandGrip = true,
	AvailableAttacks = {
		"SingleShot",
		"JAZZ_Salvo",
	},
	ShootAP = 7000,
	ReloadAP = 5000,
	BurstShots = 1,
	AutoShots = 1,

	CloseRange = 8,

	CloseRangeFactor = 80,
	BulletDropRange = 15,
	Grouping = 37,
	WeaponResource = 4000,
}

