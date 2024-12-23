UndefineClass('LegionScout_Stronger_Elite')
DefineClass.LegionScout_Stronger_Elite = {
	__parents = { "UnitData" },
	__generated_by_class = "ModItemUnitDataCompositeDef",


	object_class = "UnitData",
	Health = 94,
	Agility = 90,
	Dexterity = 99,
	Strength = 75,
	Wisdom = 70,
	Leadership = 29,
	Marksmanship = 80,
	Mechanical = 80,
	Explosives = 55,
	Medical = 0,
	Portrait = "UI/EnemiesPortraits/LegionRecon",
	BigPortrait = "UI/Enemies/LegionRaider",
	Name = T(894403310975, --[[ModItemUnitDataCompositeDef LegionScout_Stronger_Elite Name]] "Элитный разведчик"),
	Randomization = true,
	elite = true,
	eliteCategory = "Legion",
	Affiliation = "Legion",
	StartingLevel = 7,
	neutral_retaliate = true,
	AIKeywords = {
		"Flank",
		"RunAndGun",
		"MobileShot",
		"Control",
		"Explosives",
		"Ordnance",
	},
	archetype = "Skirmisher",
	role = "Recon",
	OpeningAttackType = "Overwatch",
	MaxAttacks = 2,
	PickCustomArchetype = function (self, proto_context)  end,
	CustomEquipGear = function (self, items)  end,
	MaxHitPoints = 50,
	StartingPerks = {
		"RelentlessAdvance",
		"MinFreeMove",
		"Untraceable",
		"CQCTraining",
		"Flanker",
		"GruntyPerk",
	},
	AppearancesList = {
		PlaceObj('AppearanceWeight', {
			'Preset', "Legion_Recon02",
		}),
		PlaceObj('AppearanceWeight', {
			'Preset', "Legion_Recon03",
		}),
		PlaceObj('AppearanceWeight', {
			'Preset', "LegionScout_Stronger_Elite",
			'Weight', 3,
		}),
		PlaceObj('AppearanceWeight', {
			'Preset', "LegionScout_Stronger_Elite_alt",
			'Weight', 3,
		}),
		PlaceObj('AppearanceWeight', {
			'Preset', "LegionScout_Stronger_Elite_alt_2",
			'Weight', 3,
		}),
	},
	Equipment = {
		"LegionScout_Stronger_Elite",
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

