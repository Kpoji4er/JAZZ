UndefineClass('LegionManiac_Stronger_Elite')
DefineClass.LegionManiac_Stronger_Elite = {
	__parents = { "UnitData" },
	__generated_by_class = "ModItemUnitDataCompositeDef",


	object_class = "UnitData",
	Health = 100,
	Agility = 92,
	Dexterity = 87,
	Strength = 95,
	Wisdom = 43,
	Leadership = 65,
	Marksmanship = 57,
	Mechanical = 80,
	Explosives = 54,
	Medical = 0,
	Portrait = "UI/EnemiesPortraits/LegionStormer",
	BigPortrait = "UI/Enemies/LegionRaider",
	Name = T(332974659860, --[[ModItemUnitDataCompositeDef LegionManiac_Stronger_Elite Name]] "Элитный громила"),
	Randomization = true,
	elite = true,
	eliteCategory = "Legion",
	Affiliation = "Legion",
	StartingLevel = 7,
	neutral_retaliate = true,
	AIKeywords = {
		"Control",
		"Explosives",
		"Flank",
		"RunAndGun",
		"MobileShot",
		"Stim",
	},
	archetype = "Brute",
	role = "Stormer",
	CanManEmplacements = false,
	MaxAttacks = 2,
	PickCustomArchetype = function (self, proto_context)  end,
	CustomEquipGear = function (self, items)  end,
	MaxHitPoints = 100,
	StartingPerks = {
		"BeefedUp",
		"Berserker",
		"Shatterhand",
		"CQCTraining",
		"NailsPerk",
	},
	AppearancesList = {
		PlaceObj('AppearanceWeight', {
			'Preset', "Legion_Stormer",
		}),
		PlaceObj('AppearanceWeight', {
			'Preset', "Legion_Stormer02",
		}),
		PlaceObj('AppearanceWeight', {
			'Preset', "Legion_Stormer03",
		}),
		PlaceObj('AppearanceWeight', {
			'Preset', "LegionManiac_Stronger_Elite",
			'Weight', 2,
		}),
		PlaceObj('AppearanceWeight', {
			'Preset', "LegionManiac_Stronger_Elite_alt",
			'Weight', 2,
		}),
		PlaceObj('AppearanceWeight', {
			'Preset', "LegionManiac_Stronger_alt_2",
			'Weight', 2,
		}),
	},
	Equipment = {
		"LegionBerserker_Stronger_Elite",
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

