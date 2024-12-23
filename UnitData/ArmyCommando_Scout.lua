UndefineClass('ArmyCommando_Scout')
DefineClass.ArmyCommando_Scout = {
	__parents = { "UnitData" },
	__generated_by_class = "ModItemUnitDataCompositeDef",


	object_class = "UnitData",
	Health = 94,
	Agility = 95,
	Dexterity = 93,
	Strength = 82,
	Wisdom = 75,
	Leadership = 71,
	Marksmanship = 93,
	Mechanical = 75,
	Explosives = 75,
	Medical = 75,
	Portrait = "UI/EnemiesPortraits/ArmyRecon",
	Name = T(498170277650, --[[ModItemUnitDataCompositeDef ArmyCommando_Scout Name]] "Диверсант"),
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

