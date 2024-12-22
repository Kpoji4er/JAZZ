UndefineClass('ArmySniper_Elite')
DefineClass.ArmySniper_Elite = {
	__parents = { "UnitData" },
	__generated_by_class = "ModItemUnitDataCompositeDef",


	object_class = "UnitData",
	Health = 84,
	Agility = 94,
	Dexterity = 94,
	Strength = 41,
	Wisdom = 48,
	Leadership = 33,
	Marksmanship = 95,
	Mechanical = 80,
	Explosives = 0,
	Medical = 0,
	Portrait = "UI/EnemiesPortraits/ArmySniper",
	BigPortrait = "UI/Enemies/LegionRaider",
	Name = T(409540308094, --[[ModItemUnitDataCompositeDef ArmySniper_Elite Name]] "Элитный снайпер"),
	Randomization = true,
	Affiliation = "Army",
	StartingLevel = 7,
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

