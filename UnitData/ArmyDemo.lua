UndefineClass('ArmyDemo')
DefineClass.ArmyDemo = {
	__parents = { "UnitData" },
	__generated_by_class = "ModItemUnitDataCompositeDef",


	object_class = "UnitData",
	Health = 75,
	Agility = 71,
	Dexterity = 30,
	Strength = 53,
	Wisdom = 14,
	Leadership = 14,
	Marksmanship = 43,
	Mechanical = 40,
	Explosives = 84,
	Medical = 0,
	Portrait = "UI/EnemiesPortraits/ArmyDemo",
	Name = T(515821906221, --[[ModItemUnitDataCompositeDef ArmyDemo Name]] "Сапёр"),
	Randomization = true,
	Affiliation = "Army",
	StartingLevel = 4,
	neutral_retaliate = true,
	AIKeywords = {
		"Explosives",
		"Flank",
		"Smoke",
	},
	archetype = "Skirmisher",
	role = "Demolitions",
	MaxAttacks = 1,
	MaxHitPoints = 50,
	StartingPerks = {
		"Throwing",
		"AutoWeapons",
	},
	AppearancesList = {
		PlaceObj('AppearanceWeight', {
			'Preset', "GrandChien_Demolition",
		}),
	},
	Equipment = {
		"ArmyDemo",
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
	pollyvoice = "Russell",
	gender = "Male",
	VoiceResponseId = "ArmySoldier",
}

