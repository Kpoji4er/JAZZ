UndefineClass('M1Garand')
DefineClass.M1Garand = {
	__parents = { "SniperRifle" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "T1+",
	object_class = "SniperRifle",
	ScrapParts = 8,
	Icon = "Mod/e6L4ECj/WeaponIcons/M1Garand.png",
	DisplayName = T(729447298300, --[[ModItemInventoryItemCompositeDef M1Garand DisplayName]] "М1 Гаранд"),
	DisplayNamePlural = T(830429456946, --[[ModItemInventoryItemCompositeDef M1Garand DisplayNamePlural]] "М1 Гаранд"),
	Description = T(789944142367, --[[ModItemInventoryItemCompositeDef M1Garand Description]] "Американская винтовка М1 конструкции канадца Джона Гаранда занимает достойное место в истории стрелкового оружия как первая самозарядная немагазинная винтовка, принятая на вооружение в качестве основного индивидуального оружия пехоты."),
	AdditionalHint = T(546051968989, --[[ModItemInventoryItemCompositeDef M1Garand AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Низкие од на выстрел\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Низкая точность прицельной стрельбы\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Возможность стрельбы на бегу"),
	LargeItem = 1,
	UnitStat = "Marksmanship",
	Cost = 2000,
	CategoryPair = "Rifles",
	CanAppearStandard = false,
	Caliber = "JAZZ_Caliber_3006",
	Damage = 38,
	ObjDamageMod = 80,
	AimAccuracy = 28,
	CritChanceScaled = 40,
	MagazineSize = 8,
	WeaponRange = 60,
	OverwatchAngle = 840,
	Noise = 58,
	HandSlot = "TwoHanded",
	Entity = "Garand",
	ComponentSlots = {
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Scope",
			'AvailableComponents', {
				"JAZZ_Reflex_Garand",
				"JAZZ_Scope_Garand",
				"DefaultIronsight_AR15",
			},
			'DefaultComponent', "DefaultIronsight_AR15",
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Muzzle",
			'CanBeEmpty', true,
			'AvailableComponents', {
				"Suppressor",
			},
		}),
	},
	HolsterSlot = "Shoulder",
	ModifyRightHandGrip = true,
	AvailableAttacks = {
		"SingleShot",
		"CancelShot",
		"MobileShot",
	},
	ShootAP = 5000,
	ReloadAP = 5000,
	BurstShots = 1,
	AutoShots = 1,
	Handling = 42,
	BulletDropRange = 23,
	Grouping = 220,
}

