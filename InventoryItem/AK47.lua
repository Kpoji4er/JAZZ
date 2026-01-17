UndefineClass('AK47')
DefineClass.AK47 = {
	__parents = { "AssaultRifle" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "Tier 2-3",
	object_class = "AssaultRifle",
	ScrapParts = 10,
	RepairCost = 5,
	Reliability = 90,
	Icon = "Mod/e6L4ECj/WeaponIcons/AK47.png",
	DisplayName = T(152496614613, --[[ModItemInventoryItemCompositeDef AK47 DisplayName]] "АК47"),
	DisplayNamePlural = T(949478428457, --[[ModItemInventoryItemCompositeDef AK47 DisplayNamePlural]] "АК47"),
	Description = T(891232355554, --[[ModItemInventoryItemCompositeDef AK47 Description]] "Если где-то в мире случается конфликт, вы точно найдете там АК-47. Это аксиома. Старый-добрый «калаш» неприхотлив, прост в использовании, надежен и стоит гроши. Статистика утверждает, что в мире водится более 75 миллионов экземпляров этого зверя."),
	AdditionalHint = T(435712410326, --[[ModItemInventoryItemCompositeDef AK47 AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Убойный \n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Надежный \n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Это АК, АК-47"),
	LargeItem = 1,
	UnitStat = "Marksmanship",
	Cost = 8500,
	MaxStock = 5,
	RestockWeight = 150,
	CategoryPair = "AssaultRifles",
	Caliber = "JAZZ_Caliber_762x39",
	Damage = 28,
	ObjDamageMod = 50,
	AimAccuracy = 10,
	MagazineSize = 30,
	WeaponRange = 38,
	OverwatchAngle = 1320,
	Noise = 55,
	HandSlot = "TwoHanded",
	Entity = "J_AK47",
	ComponentSlots = {
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Bipod",
			'CanBeEmpty', true,
			'AvailableComponents', {
				"Bipod",
			},
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Under",
			'CanBeEmpty', true,
			'AvailableComponents', {
				"GP25",
			},
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Magazine",
			'AvailableComponents', {
				"MagNormal",
				"MagLarge",
				"MagQuick",
			},
			'DefaultComponent', "MagNormal",
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Muzzle",
			'Modifiable', false,
			'CanBeEmpty', true,
			'AvailableComponents', {
				"Compensator",
				"Suppressor",
			},
		}),
	},
	HolsterSlot = "Shoulder",
	AvailableAttacks = {
		"BurstFire",
		"AutoFire",
		"SingleShot",
		"CancelShot",
	},
	ShootAP = 6000,
	ReloadAP = 6000,
	Recoil = 15,
	AutoShots = 6,
	Handling = -10,
	BulletDropRange = 14,
	Grouping = 63,
	BaseJamChance = -10,
	WeaponResource = 12000,
}

