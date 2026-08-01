UndefineClass('M700')
DefineClass.M700 = {
	__parents = { "SniperRifle" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "Tier 2-4",
	object_class = "SniperRifle",
	ScrapParts = 14,
	RepairCost = 5,
	Reliability = 85,
	Icon = "Mod/e6L4ECj/WeaponIcons/M700.png",
	DisplayName = T(539019407378, --[[ModItemInventoryItemCompositeDef M700 DisplayName]] "M700"),
	DisplayNamePlural = T(719067700493, --[[ModItemInventoryItemCompositeDef M700 DisplayNamePlural]] "M700"),
	Description = T(751666262115, --[[ModItemInventoryItemCompositeDef M700 Description]] "Гражданская версия точной и убойной винтовки со скользяще-поворотным затвором. Одна из самых популярных, если не самая болтовая винтовка в мире. В руках опытного снайпера способна нагнать страх, ужас, ад и Израиль на любое подразделение врага."),
	AdditionalHint = T(262854979930, --[[ModItemInventoryItemCompositeDef M700 AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Винтовка с ручным перезаряжанием \n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Неудобный \n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Медленно стреляет \n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Надежный \n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Точный"),
	LargeItem = 1,
	UnitStat = "Marksmanship",
	Cost = 10000,
	CanAppearInShop = true,
	Tier = 2,
	CategoryPair = "Rifles",
	Caliber = "JAZZ_Caliber_762x51",
	Damage = 36,
	ObjDamageMod = 80,
	AimAccuracy = 16,
	CritChanceScaled = 50,
	MagazineSize = 5,
	WeaponRange = 78,
	OverwatchAngle = 420,
	Noise = 46,
	HandSlot = "TwoHanded",
	Entity = "M700",
	ComponentSlots = {
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Scope",
			'Modifiable', false,
			'AvailableComponents', {
				"JAZZ_Scope_3x_9x",
			},
			'DefaultComponent', "JAZZ_Scope_3x_9x",
		}),
	},
	HolsterSlot = "Shoulder",
	ModifyRightHandGrip = true,
	AvailableAttacks = {
		"SingleShot",
		"JAZZ_JokerShot",
		"JAZZ_Bullseye",
	},
	ShootAP = 8000,
	ReloadAP = 8000,
	BurstShots = 1,
	AutoShots = 1,

	CloseRange = 12,

	CloseRangeFactor = 70,
	BulletDropRange = 19,
	Grouping = 48,
	BaseJamChance = -20,
	WeaponResource = 4500,
}

