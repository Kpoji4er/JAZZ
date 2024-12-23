UndefineClass('ArmySoldier')
DefineClass.ArmySoldier = {
	__parents = { "UnitData" },
	__generated_by_class = "ModItemUnitDataCompositeDef",


	object_class = "UnitData",
	Health = 84,
	Agility = 82,
	Dexterity = 77,
	Strength = 53,
	Wisdom = 31,
	Leadership = 19,
	Marksmanship = 80,
	Mechanical = 40,
	Explosives = 0,
	Medical = 0,
	Portrait = "UI/EnemiesPortraits/ArmySoldier",
	Name = T(544120605675, --[[ModItemUnitDataCompositeDef ArmySoldier Name]] "Пехотинец"),
	Randomization = true,
	Affiliation = "Army",
	StartingLevel = 4,
	neutral_retaliate = true,
	AIKeywords = {
		"Soldier",
		"Explosives",
		"Smoke",
	},
	role = "Soldier",
	MaxAttacks = 2,
	MaxHitPoints = 50,
	StartingPerks = {
		"AutoWeapons",
		"MinFreeMove",
		"Hotblood",
	},
	AppearancesList = {
		PlaceObj('AppearanceWeight', {
			'Preset', "GrandChien_Soldier",
		}),
	},
	Equipment = {
		"ArmySoldier",
	},
	AdditionalGroups = {
		PlaceObj('AdditionalGroup', {
			'Weight', 50,
			'Exclusive', true,
			'Name', "ArmyMale_1",
		}),
		PlaceObj('AdditionalGroup', {
			'Weight', 50,
			'Exclusive', true,
			'Name', "ArmyMale_2",
		}),
	},
	Tier = "Elite",
	pollyvoice = "Joey",
	gender = "Male",
	VoiceResponseId = "ArmySoldier",
}

