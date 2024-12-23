UndefineClass('ArmyCommando_Demolution')
DefineClass.ArmyCommando_Demolution = {
	__parents = { "UnitData" },
	__generated_by_class = "ModItemUnitDataCompositeDef",


	object_class = "UnitData",
	Health = 93,
	Agility = 90,
	Dexterity = 88,
	Strength = 48,
	Wisdom = 71,
	Leadership = 29,
	Marksmanship = 88,
	Mechanical = 72,
	Explosives = 99,
	Medical = 77,
	Portrait = "UI/EnemiesPortraits/ArmyRecon",
	Name = T(646387258267, --[[ModItemUnitDataCompositeDef ArmyCommando_Demolution Name]] "Разведчик Сапер"),
	Randomization = true,
	Affiliation = "Army",
	StartingLevel = 3,
	neutral_retaliate = true,
	AIKeywords = {
		"Flank",
		"RunAndGun",
	},
	archetype = "Skirmisher",
	role = "Recon",
	OpeningAttackType = "Overwatch",
	MaxAttacks = 2,
	MaxHitPoints = 50,
	StartingPerks = {
		"AutoWeapons",
	},
	AppearancesList = {
		PlaceObj('AppearanceWeight', {
			'Preset', "GrandChien_Recon",
		}),
	},
	Equipment = {
		"ArmyScout",
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

