UndefineClass('FRF2')
DefineClass.FRF2 = {
	__parents = { "SniperRifle" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "Tier 2-2",
	object_class = "SniperRifle",
	ScrapParts = 14,
	RepairCost = 5,
	Reliability = 75,
	Icon = "Mod/e6L4ECj/WeaponIcons/FRF2.png",
	DisplayName = T(799798287692, --[[ModItemInventoryItemCompositeDef FRF2 DisplayName]] "FR F2"),
	DisplayNamePlural = T(821596806678, --[[ModItemInventoryItemCompositeDef FRF2 DisplayNamePlural]] "FR F2"),
	Description = T(155102946917, --[[ModItemInventoryItemCompositeDef FRF2 Description]] 'Современная "болтовка" на вооружении ВС Франции. Представляет собой модернизированную винтовку FR F1 - измененная ложа, приклад, пластиковый теплоизолирующий кожух на стволе. Используется в разработке системы оружия солдата будущего FELIN. Винтовка будущих 1970-х...'),
	AdditionalHint = T(357652125031, --[[ModItemInventoryItemCompositeDef FRF2 AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Винтовка с ручным перезаряжанием \n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Неудобный \n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Медленно стреляет \n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Надежный \n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Точный"),
	LargeItem = 1,
	UnitStat = "Marksmanship",
	Cost = 12000,
	CanAppearInShop = true,
	Tier = 2,
	CategoryPair = "Rifles",
	Caliber = "JAZZ_Caliber_75French",
	Damage = 35,
	ObjDamageMod = 80,
	AimAccuracy = 16,
	CritChanceScaled = 50,
	MagazineSize = 10,
	WeaponRange = 75,
	OverwatchAngle = 420,
	Noise = 56,
	HandSlot = "TwoHanded",
	Entity = "FRF2",
	ComponentSlots = {
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Magazine",
			'Modifiable', false,
			'AvailableComponents', {
				"JAZZ_MagNormal",
			},
			'DefaultComponent', "JAZZ_MagNormal",
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Scope",
			'Modifiable', false,
			'AvailableComponents', {
				"JAZZ_Scope_8x_SCROME",
			},
			'DefaultComponent', "JAZZ_Scope_8x_SCROME",
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Muzzle",
			'CanBeEmpty', true,
			'AvailableComponents', {
				"JAZZ_SuppressorImproved",
			},
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Bipod",
			'Modifiable', false,
			'DefaultComponent', "JAZZ_Bipod",
		}),
	},
	HolsterSlot = "Shoulder",
	AvailableAttacks = {
		"SingleShot",
		"JAZZ_JokerShot",
		"JAZZ_Bullseye",
	},
	ShootAP = 8000,
	ReloadAP = 7000,
	BurstShots = 0,
	WeaponMass = 55,
	CyclicRPM = 0,
	WeaponSizeClass = "Long",
	BurstLimiter = 0,
	Recoil = 18,
	AutoShots = 0,

	CloseRange = 12,

	CloseRangeFactor = 70,
	BulletDropRange = 17,
	Grouping = 48,
	BaseJamChance = -10,
	WeaponResource = 6000,
}

