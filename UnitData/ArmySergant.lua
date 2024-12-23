UndefineClass('ArmySergant')
DefineClass.ArmySergant = {
	__parents = { "UnitData" },
	__generated_by_class = "ModItemUnitDataCompositeDef",


	object_class = "UnitData",
	Health = 78,
	Agility = 95,
	Dexterity = 90,
	Strength = 68,
	Wisdom = 47,
	Leadership = 74,
	Marksmanship = 80,
	Mechanical = 80,
	Explosives = 50,
	Medical = 55,
	Portrait = "UI/EnemiesPortraits/ArmySoldier",
	Name = T(817124274840, --[[ModItemUnitDataCompositeDef ArmySergant Name]] "Сержант"),
	Randomization = true,
	Affiliation = "Army",
	StartingLevel = 4,
	neutral_retaliate = true,
	AIKeywords = {
		"Soldier",
		"Control",
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

