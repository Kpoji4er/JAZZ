UndefineClass('AdonisSquadLeader_Elite')
DefineClass.AdonisSquadLeader_Elite = {
	__parents = { "UnitData" },
	__generated_by_class = "ModItemUnitDataCompositeDef",


	object_class = "UnitData",
	Health = 96,
	Agility = 90,
	Dexterity = 84,
	Strength = 85,
	Wisdom = 80,
	Leadership = 91,
	Marksmanship = 95,
	Mechanical = 80,
	Explosives = 84,
	Medical = 74,
	Portrait = "UI/EnemiesPortraits/AdonisOfficer",
	Name = T(840482939860, --[[ModItemUnitDataCompositeDef AdonisSquadLeader_Elite Name]] "Элитный командир"),
	Randomization = true,
	elite = true,
	eliteCategory = "Foreigners",
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

