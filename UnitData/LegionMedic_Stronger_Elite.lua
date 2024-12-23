UndefineClass('LegionMedic_Stronger_Elite')
DefineClass.LegionMedic_Stronger_Elite = {
	__parents = { "UnitData" },
	__generated_by_class = "ModItemUnitDataCompositeDef",


	object_class = "UnitData",
	Health = 100,
	Agility = 93,
	Dexterity = 98,
	Strength = 66,
	Wisdom = 78,
	Leadership = 64,
	Marksmanship = 74,
	Mechanical = 80,
	Explosives = 5,
	Medical = 93,
	Portrait = "UI/EnemiesPortraits/LegionMedic",
	BigPortrait = "UI/Enemies/LegionRaider",
	Name = T(799448736839, --[[ModItemUnitDataCompositeDef LegionMedic_Stronger_Elite Name]] "Опытный санитар"),
	Randomization = true,
	Affiliation = "Legion",
	StartingLevel = 7,
	neutral_retaliate = true,
	AIKeywords = {
		"Heal",
		"Control",
	},
	archetype = "Medic",
	role = "Medic",
	CanManEmplacements = false,
	RepositionArchetype = "HeavyGunner",
	PickCustomArchetype = function (self, proto_context)  end,
	MaxHitPoints = 80,
	StartingPerks = {
		"BeefedUp",
		"Ambidextrous",
		"Savior",
		"ShoulderToShoulder",
		"CQCTraining",
	},
	AppearancesList = {
		PlaceObj('AppearanceWeight', {
			'Preset', "LegionMedic_Stronger_Elite",
		}),
		PlaceObj('AppearanceWeight', {
			'Preset', "LegionMedic_Stronger_Elite_alt",
		}),
		PlaceObj('AppearanceWeight', {
			'Preset', "LegionMedic_Stronger_alt_2",
		}),
		PlaceObj('AppearanceWeight', {
			'Preset', "LegionMedic_Stronger_alt",
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

