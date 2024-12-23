UndefineClass('ArmyLeitenant')
DefineClass.ArmyLeitenant = {
	__parents = { "UnitData" },
	__generated_by_class = "ModItemUnitDataCompositeDef",


	object_class = "UnitData",
	Health = 90,
	Agility = 88,
	Dexterity = 86,
	Strength = 82,
	Wisdom = 73,
	Leadership = 88,
	Marksmanship = 80,
	Mechanical = 100,
	Explosives = 53,
	Medical = 0,
	Portrait = "UI/EnemiesPortraits/ArmySoldier",
	Name = T(164131088840, --[[ModItemUnitDataCompositeDef ArmyLeitenant Name]] "Лейтенант"),
	Randomization = true,
	Affiliation = "Army",
	StartingLevel = 4,
	neutral_retaliate = true,
	AIKeywords = {
		"Soldier",
		"Flank",
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

