UndefineClass('LegionGrenadier_Stronger_Elite')
DefineClass.LegionGrenadier_Stronger_Elite = {
	__parents = { "UnitData" },
	__generated_by_class = "ModItemUnitDataCompositeDef",


	object_class = "UnitData",
	Health = 85,
	Agility = 90,
	Dexterity = 65,
	Strength = 78,
	Wisdom = 23,
	Leadership = 14,
	Marksmanship = 70,
	Mechanical = 80,
	Explosives = 30,
	Medical = 0,
	Portrait = "UI/EnemiesPortraits/LegionDemo",
	BigPortrait = "UI/Enemies/LegionRaider",
	Name = T(853894759815, --[[ModItemUnitDataCompositeDef LegionGrenadier_Stronger_Elite Name]] "Элитный гранатомётчик"),
	Randomization = true,
	elite = true,
	eliteCategory = "Legion",
	Affiliation = "Legion",
	StartingLevel = 7,
	neutral_retaliate = true,
	AIKeywords = {
		"Explosives",
		"MobileShot",
		"Ordnance",
		"RunAndGun",
		"Control",
	},
	archetype = "Grenadier",
	role = "Demolitions",
	CanManEmplacements = false,
	MaxAttacks = 5,
	PickCustomArchetype = function (self, proto_context)  end,
	CustomEquipGear = function (self, items)  end,
	MaxHitPoints = 50,
	StartingPerks = {
		"TrueGrit",
		"Throwing",
		"RelentlessAdvance",
		"MinFreeMove",
		"BreachAndClear",
		"HitTheDeck",
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
			'Preset', "LegionGrenadir_Stronger_Elite",
			'Weight', 3,
		}),
		PlaceObj('AppearanceWeight', {
			'Preset', "LegionGrenadir_Stronger_Elite_alt",
			'Weight', 3,
		}),
	},
	Equipment = {
		"LegionGrenadier_Stronger_Elite",
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

