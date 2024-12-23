UndefineClass('LegionMedic_Stronger')
DefineClass.LegionMedic_Stronger = {
	__parents = { "UnitData" },
	__generated_by_class = "ModItemUnitDataCompositeDef",


	object_class = "UnitData",
	Health = 80,
	Agility = 93,
	Dexterity = 96,
	Strength = 42,
	Wisdom = 85,
	Leadership = 50,
	Marksmanship = 74,
	Mechanical = 30,
	Explosives = 5,
	Medical = 93,
	Portrait = "UI/EnemiesPortraits/LegionMedic",
	BigPortrait = "UI/Enemies/LegionRaider",
	Name = T(391906391470, --[[ModItemUnitDataCompositeDef LegionMedic_Stronger Name]] "Опытный санитар"),
	Randomization = true,
	Affiliation = "Legion",
	StartingLevel = 5,
	neutral_retaliate = true,
	AIKeywords = {
		"Heal",
		"Smoke",
		"Control",
	},
	archetype = "Medic",
	role = "Medic",
	CanManEmplacements = false,
	MaxAttacks = 4,
	PickCustomArchetype = function (self, proto_context)  end,
	CustomEquipGear = function (self, items)  end,
	MaxHitPoints = 80,
	StartingPerks = {
		"Ambidextrous",
		"BeefedUp",
		"Savior",
	},
	AppearancesList = {
		PlaceObj('AppearanceWeight', {
			'Preset', "Legion_WitchDoctor",
		}),
		PlaceObj('AppearanceWeight', {
			'Preset', "Legion_WitchDoctor02",
		}),
		PlaceObj('AppearanceWeight', {
			'Preset', "Legion_WitchDoctor03",
		}),
		PlaceObj('AppearanceWeight', {
			'Preset', "LegionMedic_Stronger",
			'Weight', 4,
		}),
		PlaceObj('AppearanceWeight', {
			'Preset', "LegionMedic_Stronger_alt",
			'Weight', 4,
		}),
		PlaceObj('AppearanceWeight', {
			'Preset', "LegionMedic_Stronger_alt_2",
			'Weight', 4,
		}),
	},
	Equipment = {
		"LegionMedic_Stronger",
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
	pollyvoice = "Joey",
	gender = "Male",
	VoiceResponseId = "LegionRaider",
}

