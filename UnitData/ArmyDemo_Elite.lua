UndefineClass('ArmyDemo_Elite')
DefineClass.ArmyDemo_Elite = {
	__parents = { "UnitData" },
	__generated_by_class = "ModItemUnitDataCompositeDef",


	object_class = "UnitData",
	Health = 94,
	Agility = 83,
	Dexterity = 79,
	Strength = 69,
	Wisdom = 28,
	Leadership = 14,
	Marksmanship = 87,
	Explosives = 91,
	Medical = 0,
	Portrait = "UI/EnemiesPortraits/ArmyDemo",
	Name = T(618487624385, --[[ModItemUnitDataCompositeDef ArmyDemo_Elite Name]] "Элитный сапер"),
	Randomization = true,
	Affiliation = "Army",
	StartingLevel = 6,
	neutral_retaliate = true,
	AIKeywords = {
		"Explosives",
		"Flank",
	},
	archetype = "Skirmisher",
	role = "Demolitions",
	MaxAttacks = 1,
	MaxHitPoints = 50,
	StartingPerks = {
		"Throwing",
		"AutoWeapons",
		"BattleFocus",
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

