UndefineClass('ArmyRPG')
DefineClass.ArmyRPG = {
	__parents = { "UnitData" },
	__generated_by_class = "ModItemUnitDataCompositeDef",


	object_class = "UnitData",
	Health = 81,
	Agility = 83,
	Dexterity = 83,
	Strength = 88,
	Wisdom = 44,
	Leadership = 56,
	Marksmanship = 12,
	Mechanical = 50,
	Explosives = 96,
	Medical = 0,
	Portrait = "UI/EnemiesPortraits/ArmyArtillery",
	Name = T(910183932410, --[[ModItemUnitDataCompositeDef ArmyRPG Name]] "Гранатомётчик"),
	Randomization = true,
	Affiliation = "Army",
	StartingLevel = 4,
	neutral_retaliate = true,
	AIKeywords = {
		"Ordnance",
		"Explosives",
	},
	role = "Artillery",
	CanManEmplacements = false,
	MaxAttacks = 1,
	MaxHitPoints = 50,
	AppearancesList = {
		PlaceObj('AppearanceWeight', {
			'Preset', "GrandChien_Artillery",
		}),
	},
	Equipment = {
		"ArmyRPG",
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
	pollyvoice = "Joey",
	gender = "Male",
	VoiceResponseId = "ArmySoldier",
}

