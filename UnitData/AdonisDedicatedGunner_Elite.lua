UndefineClass('AdonisDedicatedGunner_Elite')
DefineClass.AdonisDedicatedGunner_Elite = {
	__parents = { "UnitData" },
	__generated_by_class = "ModItemUnitDataCompositeDef",


	object_class = "UnitData",
	Health = 94,
	Agility = 91,
	Dexterity = 89,
	Strength = 95,
	Wisdom = 71,
	Leadership = 72,
	Marksmanship = 90,
	Mechanical = 80,
	Explosives = 81,
	Medical = 52,
	Portrait = "UI/EnemiesPortraits/AdonisHeavy",
	Name = T(895703228903, --[[ModItemUnitDataCompositeDef AdonisDedicatedGunner_Elite Name]] "Пулеметчик"),
	Randomization = true,
	elite = true,
	eliteCategory = "Foreigners",
	Affiliation = "Adonis",
	StartingLevel = 6,
	neutral_retaliate = true,
	role = "Heavy",
	MaxAttacks = 4,
	MaxHitPoints = 50,
	StartingPerks = {
		"AutoWeapons",
		"HeavyWeaponsTraining",
		"CollateralDamage",
	},
	AppearancesList = {
		PlaceObj('AppearanceWeight', {
			'Preset', "Adonis_Soldier",
		}),
	},
	Equipment = {
		"AdonisAssault_Elite",
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

