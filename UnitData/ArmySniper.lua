UndefineClass('ArmySniper')
DefineClass.ArmySniper = {
	__parents = { "UnitData" },
	__generated_by_class = "ModItemUnitDataCompositeDef",


	object_class = "UnitData",
	Health = 78,
	Agility = 90,
	Dexterity = 90,
	Strength = 41,
	Wisdom = 48,
	Leadership = 33,
	Marksmanship = 90,
	Mechanical = 40,
	Explosives = 0,
	Medical = 0,
	Portrait = "UI/EnemiesPortraits/ArmySniper",
	Name = T(842711097729, --[[ModItemUnitDataCompositeDef ArmySniper Name]] "Снайпер"),
	Randomization = true,
	Affiliation = "Army",
	StartingLevel = 3,
	neutral_retaliate = true,
	AIKeywords = {
		"Sniper",
	},
	archetype = "Soldier_Sniper",
	role = "Marksman",
	AlwaysUseOpeningAttack = true,
	OpeningAttackType = "PinDown",
	MaxAttacks = 1,
	MaxHitPoints = 50,
	StartingPerks = {
		"HitTheDeck",
	},
	AppearancesList = {
		PlaceObj('AppearanceWeight', {
			'Preset', "GrandChien_Marksman",
		}),
	},
	Equipment = {
		"ArmySniper",
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

