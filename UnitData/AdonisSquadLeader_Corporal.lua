UndefineClass('AdonisSquadLeader_Corporal')
DefineClass.AdonisSquadLeader_Corporal = {
	__parents = { "UnitData" },
	__generated_by_class = "ModItemUnitDataCompositeDef",


	object_class = "UnitData",
	Health = 88,
	Agility = 90,
	Dexterity = 75,
	Strength = 85,
	Wisdom = 80,
	Leadership = 62,
	Marksmanship = 95,
	Mechanical = 70,
	Explosives = 64,
	Medical = 49,
	Portrait = "UI/EnemiesPortraits/AdonisOfficer",
	Name = T(714452942798, --[[ModItemUnitDataCompositeDef AdonisSquadLeader_Corporal Name]] "Капрал"),
	Randomization = true,
	Affiliation = "Adonis",
	StartingLevel = 7,
	neutral_retaliate = true,
	AIKeywords = {
		"Control",
		"Explosives",
	},
	role = "Commander",
	AlwaysUseOpeningAttack = true,
	OpeningAttackType = "Overwatch",
	MaxAttacks = 2,
	unitPowerModifier = 75,
	MaxHitPoints = 80,
	StartingPerks = {
		"OpportunisticKiller",
		"AutoWeapons",
	},
	AppearancesList = {
		PlaceObj('AppearanceWeight', {
			'Preset', "Adonis_Officer",
		}),
	},
	Equipment = {
		"AdonisSquadLeader",
	},
	AdditionalGroups = {
		PlaceObj('AdditionalGroup', {
			'Weight', 50,
			'Exclusive', true,
			'Name', "AdonisMale_1",
		}),
		PlaceObj('AdditionalGroup', {
			'Weight', 50,
			'Exclusive', true,
			'Name', "AdonisMale_2",
		}),
	},
	Tier = "Elite",
	pollyvoice = "Joey",
	gender = "Male",
	VoiceResponseId = "AdonisAssault",
}

