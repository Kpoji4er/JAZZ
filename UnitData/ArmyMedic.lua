UndefineClass('ArmyMedic')
DefineClass.ArmyMedic = {
	__parents = { "UnitData" },
	__generated_by_class = "ModItemUnitDataCompositeDef",


	object_class = "UnitData",
	Health = 100,
	Agility = 99,
	Dexterity = 99,
	Strength = 65,
	Wisdom = 84,
	Leadership = 20,
	Marksmanship = 65,
	Mechanical = 50,
	Explosives = 5,
	Medical = 53,
	Portrait = "UI/EnemiesPortraits/ArmyMedic",
	Name = T(561617992746, --[[ModItemUnitDataCompositeDef ArmyMedic Name]] "Санитар"),
	Randomization = true,
	Affiliation = "Army",
	StartingLevel = 5,
	neutral_retaliate = true,
	AIKeywords = {
		"Heal",
		"Control",
	},
	archetype = "Medic",
	role = "Medic",
	MaxAttacks = 1,
	MaxHitPoints = 80,
	StartingPerks = {
		"MinFreeMove",
	},
	AppearancesList = {
		PlaceObj('AppearanceWeight', {
			'Preset', "GrandChien_Medic",
		}),
	},
	Equipment = {
		"ArmyMedic",
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
	Tier = "Veteran",
	pollyvoice = "Joey",
	gender = "Male",
	VoiceResponseId = "ArmySoldier",
}

