UndefineClass('ArmyCommando_Sergant')
DefineClass.ArmyCommando_Sergant = {
	__parents = { "UnitData" },
	__generated_by_class = "ModItemUnitDataCompositeDef",


	object_class = "UnitData",
	Health = 93,
	Agility = 90,
	Dexterity = 96,
	Strength = 48,
	Wisdom = 71,
	Leadership = 100,
	Marksmanship = 88,
	Mechanical = 87,
	Explosives = 89,
	Medical = 85,
	Portrait = "UI/EnemiesPortraits/ArmyRecon",
	Name = T(601232154908, --[[ModItemUnitDataCompositeDef ArmyCommando_Sergant Name]] "Сержант Разведчик"),
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

