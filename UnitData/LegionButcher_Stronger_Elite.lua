UndefineClass('LegionButcher_Stronger_Elite')
DefineClass.LegionButcher_Stronger_Elite = {
	__parents = { "UnitData" },
	__generated_by_class = "ModItemUnitDataCompositeDef",


	object_class = "UnitData",
	Health = 90,
	Agility = 96,
	Dexterity = 86,
	Strength = 90,
	Wisdom = 22,
	Leadership = 9,
	Marksmanship = 81,
	Mechanical = 80,
	Explosives = 72,
	Medical = 25,
	Portrait = "UI/EnemiesPortraits/LegionStormer",
	BigPortrait = "UI/Enemies/LegionRaider",
	Name = T(171574677173, --[[ModItemUnitDataCompositeDef LegionButcher_Stronger_Elite Name]] "Элитный мясник"),
	Randomization = true,
	elite = true,
	eliteCategory = "Legion",
	Affiliation = "Legion",
	StartingLevel = 8,
	neutral_retaliate = true,
	AIKeywords = {
		"Control",
		"Smoke",
		"Flank",
		"Explosives",
	},
	archetype = "Brute",
	role = "Stormer",
	CanManEmplacements = false,
	MaxAttacks = 4,
	PickCustomArchetype = function (self, proto_context)  end,
	CustomEquipGear = function (self, items)  end,
	MaxHitPoints = 60,
	StartingPerks = {
		"InstantAutopsy",
		"BeefedUp",
		"MeleeTraining",
		"Berserker",
		"TrueGrit",
		"LastWarning",
	},
	AppearancesList = {
		PlaceObj('AppearanceWeight', {
			'Preset', "Legion_Stormer03",
		}),
		PlaceObj('AppearanceWeight', {
			'Preset', "LegionButcher_Stronger_Elite",
			'Weight', 2,
		}),
		PlaceObj('AppearanceWeight', {
			'Preset', "LegionButcher_Stronger_Elite_alt",
			'Weight', 2,
		}),
		PlaceObj('AppearanceWeight', {
			'Preset', "LegionButcher_Stronger_Elite_alt_2",
			'Weight', 2,
		}),
	},
	Equipment = {
		"LegionMeleeFighter_Stronger_Elite",
	},
	AdditionalGroups = {
		PlaceObj('AdditionalGroup', {
			'Weight', 50,
			'Exclusive', true,
			'Name', "LegionMale_1",
		}),
		PlaceObj('AdditionalGroup', {
			'Weight', 50,
			'Exclusive', true,
			'Name', "LegionMale_2",
		}),
	},
	gender = "Male",
	VoiceResponseId = "LegionRaider",
}

