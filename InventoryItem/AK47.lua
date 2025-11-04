UndefineClass('AK47')
DefineClass.AK47 = {
	__parents = { "AssaultRifle" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "Tier 2-3",
	object_class = "AssaultRifle",
	ScrapParts = 10,
	RepairCost = 5,
	Reliability = 95,
	Icon = "Mod/e6L4ECj/WeaponIcons/AK47.png",
	DisplayName = T(152496614613, "АК47"),
	DisplayNamePlural = T(949478428457, "АК47"),
	Description = T(891232355554, "Если где-то в мире случается конфликт, вы точно найдете там АК-47. Это аксиома. Старый-добрый «калаш» неприхотлив, прост в использовании, надежен и стоит гроши. Статистика утверждает, что в мире водится более 75 миллионов экземпляров этого зверя."),
	AdditionalHint = T(435712410326, "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Высокий урон\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Высокая надежность"),
	LargeItem = 1,
	UnitStat = "Marksmanship",
	Cost = 8500,
	MaxStock = 5,
	RestockWeight = 150,
	CategoryPair = "AssaultRifles",
	Caliber = "JAZZ_Caliber_762x39",
	Damage = 28,
	ObjDamageMod = 50,
	AimAccuracy = 21,
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
	Handling = 60,
	BulletDropRange = 14,
	Grouping = 240,
	BaseJamChance = -10,
	WeaponResource = 12000,
}

