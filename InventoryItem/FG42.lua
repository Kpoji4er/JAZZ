UndefineClass('FG42')
DefineClass.FG42 = {
	__parents = { "BattleRifle" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "Tier 1-2",
	object_class = "BattleRifle",
	ScrapParts = 12,
	RepairCost = 3,
	Icon = "Mod/e6L4ECj/WeaponIcons/FG42.png",
	DisplayName = T(890000000000233, --[[ModItemInventoryItemCompositeDef FG42 DisplayName]] "FG42"),
	DisplayNamePlural = T(890000000000480, --[[ModItemInventoryItemCompositeDef FG42 DisplayNamePlural]] "FG42"),
	Description = T(890000000000764, --[[ModItemInventoryItemCompositeDef FG42 Description]] 'Оружие элиты вооруженных сил Германии в ВМВ - парашютистов Люфтваффе. Винтовка реализует концепцию "все свое ношу с собой" - тут и компоновка с магазином слева для компактности, и длинный ход поршня с поворотным затвором для надежности, и автоматический огонь для плотности, и оптический прицел для точности, и дульная мортирка для гранатометности, и сошки для лежкости, и даже штык для сувания в почку. И много-много рейхсмарок в смете.'),
	AdditionalHint = T(890000000000867, --[[ModItemInventoryItemCompositeDef FG42 AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Винтовка десантника \n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Ненадежный \n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Убойный"),
	LargeItem = 1,
	UnitStat = "Marksmanship",
	Cost = 3000,
	CanAppearInShop = true,
	Tier = 2,
	MaxStock = 1,
	RestockWeight = 40,
	CategoryPair = "AssaultRifles",
	CanAppearStandard = false,
	Caliber = "JAZZ_Caliber_792",
	Damage = 38,
	ObjDamageMod = 80,
	AimAccuracy = 8,
	MagazineSize = 20,
	WeaponRange = 53,
	OverwatchAngle = 960,
	Noise = 66,
	HandSlot = "TwoHanded",
	Entity = "FG42",
	ComponentSlots = {
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Bipod",
			'Modifiable', false,
			'AvailableComponents', {
				"JAZZ_Bipod",
			},
			'DefaultComponent', "JAZZ_Bipod",
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Scope",
			'AvailableComponents', {
				"JAZZ_Scope_ZF4",
				"JAZZ_IronSight",
			},
			'DefaultComponent', "JAZZ_IronSight",
		}),
	},
	HolsterSlot = "Shoulder",
	AvailableAttacks = {
		"BurstFire",
		"SingleShot",
		"AutoFire",
		"JAZZ_Salvo",
		"JAZZ_LargeAutoFire",
	},
	ShootAP = 7000,
	ReloadAP = 7000,
	Recoil = 30,
	AutoShots = 7,

	CloseRange = 8,

	CloseRangeFactor = 80,
	BulletDropRange = 15,
	Grouping = 42,
	WeaponResource = 6500,
}

