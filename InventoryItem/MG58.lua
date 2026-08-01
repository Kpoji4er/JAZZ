UndefineClass('MG58')
DefineClass.MG58 = {
	__parents = { "MachineGun" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "Tier 1-UNIQ",
	object_class = "MachineGun",
	ScrapParts = 12,
	RepairCost = 5,
	Reliability = 85,
	Icon = "UI/Icons/Weapons/MG58.png",
	DisplayName = T(195540713080, --[[ModItemInventoryItemCompositeDef MG58 DisplayName]] "MG58"),
	DisplayNamePlural = T(433453784311, --[[ModItemInventoryItemCompositeDef MG58 DisplayNamePlural]] "MG58s"),
	Description = T(740472863486, --[[ModItemInventoryItemCompositeDef MG58 Description]] "Modified MG42, fitted with a Kompositum 58 barrel, improved ironsights and some internal improvements. The MG58 is born. "),
	AdditionalHint = T(714045001218, --[[ModItemInventoryItemCompositeDef MG58 AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Единый пулемет \n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Обработан Композитумом для целкости \n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Тяжелый - ограничивает свободу движений"),
	LargeItem = 1,
	Cumbersome = 1,
	UnitStat = "Marksmanship",
	Valuable = 1,
	Cost = 5000,
	Caliber = "JAZZ_Caliber_792",
	Damage = 38,
	ObjDamageMod = 80,
	AimAccuracy = 22,
	MagazineSize = 50,
	WeaponRange = 56,
	OverwatchAngle = 600,
	Noise = 75,
	HandSlot = "TwoHanded",
	Entity = "Weapon_MG42",
	ComponentSlots = {
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Bipod",
			'Modifiable', false,
			'AvailableComponents', {
				"JAZZ_Bipod_MG42",
			},
			'DefaultComponent', "JAZZ_Bipod_MG42",
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Scope",
			'Modifiable', false,
			'AvailableComponents', {
				"JAZZ_ImprovedIronsight",
			},
			'DefaultComponent', "JAZZ_ImprovedIronsight",
		}),
	},
	HolsterSlot = "Shoulder",
	PreparedAttackType = "Machine Gun",
	AvailableAttacks = {
		"MGBurstFire",
		"JAZZ_MGSuppressionFire",
	},
	ShootAP = 9000,
	ReloadAP = 8000,
	Recoil = 12,

	CloseRange = 6,

	CloseRangeFactor = 85,
	BulletDropRange = 20,
	Grouping = 35,
	WeaponResource = 8000,
}

