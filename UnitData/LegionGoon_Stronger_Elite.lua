UndefineClass('LegionGoon_Stronger_Elite')
DefineClass.LegionGoon_Stronger_Elite = {
	__parents = { "UnitData" },
	__generated_by_class = "ModItemUnitDataCompositeDef",


	object_class = "UnitData",
	Health = 90,
	Agility = 96,
	Dexterity = 85,
	Strength = 65,
	Wisdom = 25,
	Leadership = 20,
	Marksmanship = 87,
	Mechanical = 80,
	Explosives = 52,
	Medical = 59,
	Portrait = "UI/EnemiesPortraits/LegionRecon",
	BigPortrait = "UI/Enemies/LegionRaider",
	Name = T(867761358013, --[[ModItemUnitDataCompositeDef LegionGoon_Stronger_Elite Name]] "Крутой головорез"),
	Randomization = true,
	elite = true,
	eliteCategory = "Legion",
	Affiliation = "Legion",
	StartingLevel = 7,
	neutral_retaliate = true,
	AIKeywords = {
		"MobileShot",
		"Flank",
		"Control",
		"Explosives",
	},
	archetype = "Skirmisher",
	role = "Recon",
	PinnedDownChance = 100,
	MaxAttacks = 8,
	PickCustomArchetype = function (self, proto_context)  end,
	CustomEquipGear = function (self, items)  end,
	MaxHitPoints = 50,
	StartingPerks = {
		"Ambidextrous",
		"Flanker",
		"CQCTraining",
		"RelentlessAdvance",
		"TrueGrit",
	},
	AppearancesList = {
		PlaceObj('AppearanceWeight', {
			'Preset', "Legion_Recon03",
		}),
		PlaceObj('AppearanceWeight', {
			'Preset', "LegionGoon_Stronger_Elite",
			'Weight', 2,
		}),
		PlaceObj('AppearanceWeight', {
			'Preset', "LegionGoon_Stronger_Elite_alt",
			'Weight', 2,
		}),
		PlaceObj('AppearanceWeight', {
			'Preset', "LegionGoon_Stronger_Elite_alt_2",
			'Weight', 2,
		}),
	},
	Equipment = {
		"LegionGoon_Stronger_Elite",
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

