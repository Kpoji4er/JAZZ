UndefineClass('AdonisFlanker_Elite')
DefineClass.AdonisFlanker_Elite = {
	__parents = { "UnitData" },
	__generated_by_class = "ModItemUnitDataCompositeDef",


	object_class = "UnitData",
	Health = 92,
	Agility = 99,
	Dexterity = 83,
	Strength = 47,
	Wisdom = 77,
	Leadership = 80,
	Marksmanship = 92,
	Mechanical = 80,
	Explosives = 77,
	Medical = 55,
	Portrait = "UI/EnemiesPortraits/AdonisRecon",
	Name = T(274375177180, --[[ModItemUnitDataCompositeDef AdonisFlanker_Elite Name]] "Элитный коммандос"),
	Randomization = true,
	elite = true,
	eliteCategory = "Foreigners",
	Affiliation = "Adonis",
	StartingLevel = 3,
	neutral_retaliate = true,
	AIKeywords = {
		"Flank",
		"RunAndGun",
	},
	archetype = "Skirmisher",
	role = "Recon",
	AlwaysUseOpeningAttack = true,
	MaxAttacks = 2,
	MaxHitPoints = 50,
	StartingPerks = {
		"AutoWeapons",
		"Hotblood",
		"NightOps",
		"RelentlessAdvance",
		"SteadyBreathing",
		"TrickShot",
	},
	AppearancesList = {
		PlaceObj('AppearanceWeight', {
			'Preset', "Adonis_Recon",
		}),
	},
	Equipment = {
		"AdonisFlanker",
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
	Tier = "Veteran",
	pollyvoice = "Joey",
	gender = "Male",
	VoiceResponseId = "AdonisAssault",
}

