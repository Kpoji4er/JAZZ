UndefineClass('LegionGrenadier')
DefineClass.LegionGrenadier = {
	__parents = { "UnitData" },
	__generated_by_class = "ModItemUnitDataCompositeDef",


	comment = "Гранатометчик | Метатель",
	object_class = "UnitData",
	Health = 80,
	Agility = 80,
	Dexterity = 45,
	Strength = 75,
	Wisdom = 14,
	Leadership = 14,
	Marksmanship = 63,
	Mechanical = 0,
	Explosives = 79,
	Medical = 0,
	Portrait = "UI/EnemiesPortraits/LegionDemo",
	BigPortrait = "UI/Enemies/LegionRaider",
	Name = T(685020204893, --[[ModItemUnitDataCompositeDef LegionGrenadier Name]] "Гранатомётчик"),
	Randomization = true,
	Affiliation = "Legion",
	StartingLevel = 2,
	neutral_retaliate = true,
	AIKeywords = {
		"Explosives",
		"MobileShot",
		"Flank",
		"RunAndGun",
		"Ordnance",
	},
	archetype = "Grenadier",
	role = "Demolitions",
	CanManEmplacements = false,
	MaxAttacks = 2,
	PickCustomArchetype = function (self, proto_context)  end,
	CustomEquipGear = function (self, items)  end,
	MaxHitPoints = 50,
	StartingPerks = {
		"Throwing",
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
			'Preset', "LegionGrenadir",
			'Weight', 2,
		}),
		PlaceObj('AppearanceWeight', {
			'Preset', "LegionGrenadir_alt",
			'Weight', 2,
		}),
		PlaceObj('AppearanceWeight', {
			'Preset', "LegionGrenadir_alt_2",
			'Weight', 2,
		}),
	},
	Equipment = {
		"LegionGrenadier",
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

