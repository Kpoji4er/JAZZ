UndefineClass('LegionButcher_Stronger')
DefineClass.LegionButcher_Stronger = {
	__parents = { "UnitData" },
	__generated_by_class = "ModItemUnitDataCompositeDef",


	object_class = "UnitData",
	Health = 80,
	Agility = 90,
	Dexterity = 86,
	Strength = 85,
	Wisdom = 15,
	Leadership = 9,
	Marksmanship = 62,
	Mechanical = 20,
	Explosives = 47,
	Medical = 0,
	Portrait = "UI/EnemiesPortraits/LegionStormer",
	BigPortrait = "UI/Enemies/LegionRaider",
	Name = T(634940896034, --[[ModItemUnitDataCompositeDef LegionButcher_Stronger Name]] "Опытный мясник"),
	Randomization = true,
	Affiliation = "Legion",
	StartingLevel = 5,
	neutral_retaliate = true,
	AIKeywords = {
		"Explosives",
		"Smoke",
		"Flank",
		"RunAndGun",
		"MobileShot",
	},
	archetype = "Brute",
	role = "Stormer",
	CanManEmplacements = false,
	MaxAttacks = 2,
	PickCustomArchetype = function (self, proto_context)  end,
	CustomEquipGear = function (self, items)  end,
	MaxHitPoints = 60,
	StartingPerks = {
		"InstantAutopsy",
		"BeefedUp",
		"MeleeTraining",
		"Berserker",
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
			'Preset', "LegionButcher_Stronger",
			'Weight', 2,
		}),
		PlaceObj('AppearanceWeight', {
			'Preset', "LegionButcher_Stronger_alt",
			'Weight', 2,
		}),
		PlaceObj('AppearanceWeight', {
			'Preset', "LegionButcher_Stronger_alt_2",
			'Weight', 2,
		}),
	},
	Equipment = {
		"LegionMeleeFighter_Stronger",
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

