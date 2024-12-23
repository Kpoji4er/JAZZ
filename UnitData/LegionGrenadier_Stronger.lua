UndefineClass('LegionGrenadier_Stronger')
DefineClass.LegionGrenadier_Stronger = {
	__parents = { "UnitData" },
	__generated_by_class = "ModItemUnitDataCompositeDef",


	object_class = "UnitData",
	Health = 84,
	Agility = 85,
	Dexterity = 62,
	Strength = 73,
	Wisdom = 17,
	Leadership = 14,
	Marksmanship = 66,
	Mechanical = 20,
	Explosives = 85,
	Medical = 0,
	Portrait = "UI/EnemiesPortraits/LegionDemo",
	BigPortrait = "UI/Enemies/LegionRaider",
	Name = T(167929106879, --[[ModItemUnitDataCompositeDef LegionGrenadier_Stronger Name]] "Опытный гранатомётчик"),
	Randomization = true,
	Affiliation = "Legion",
	StartingLevel = 2,
	neutral_retaliate = true,
	AIKeywords = {
		"Explosives",
		"MobileShot",
		"Control",
		"Soldier",
	},
	archetype = "Grenadier",
	role = "Demolitions",
	CanManEmplacements = false,
	MaxAttacks = 1,
	PickCustomArchetype = function (self, proto_context)  end,
	CustomEquipGear = function (self, items)  end,
	MaxHitPoints = 50,
	StartingPerks = {
		"Throwing",
		"MinFreeMove",
		"BreachAndClear",
		"RelentlessAdvance",
	},
	AppearancesList = {
		PlaceObj('AppearanceWeight', {
			'Preset', "Legion_Demolishion",
		}),
		PlaceObj('AppearanceWeight', {
			'Preset', "Legion_Demolishion02",
		}),
		PlaceObj('AppearanceWeight', {
			'Preset', "Legion_Demolishion03",
		}),
		PlaceObj('AppearanceWeight', {
			'Preset', "LegionGrenadir_Stronger",
			'Weight', 3,
		}),
		PlaceObj('AppearanceWeight', {
			'Preset', "LegionGrenadir_Stronger_alt",
			'Weight', 3,
		}),
		PlaceObj('AppearanceWeight', {
			'Preset', "LegionGrenadir_Stronger_alt_2",
			'Weight', 3,
		}),
	},
	Equipment = {
		"LegionGrenadier_Stronger",
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
	pollyvoice = "Russell",
	gender = "Male",
	VoiceResponseId = "LegionRaider",
}

