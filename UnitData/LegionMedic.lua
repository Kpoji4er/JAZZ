UndefineClass('LegionMedic')
DefineClass.LegionMedic = {
	__parents = { "UnitData" },
	__generated_by_class = "ModItemUnitDataCompositeDef",


	comment = "Медик - Пистолетчик",
	object_class = "UnitData",
	Health = 75,
	Agility = 94,
	Dexterity = 100,
	Strength = 42,
	Wisdom = 80,
	Leadership = 45,
	Mechanical = 12,
	Explosives = 33,
	Medical = 85,
	Portrait = "UI/EnemiesPortraits/LegionMedic",
	BigPortrait = "UI/Enemies/LegionRaider",
	Name = T(105899703679, --[[ModItemUnitDataCompositeDef LegionMedic Name]] "Санитар"),
	Randomization = true,
	Affiliation = "Legion",
	neutral_retaliate = true,
	AIKeywords = {
		"Heal",
		"Smoke",
		"Nova",
		"MobileShot",
		"Explosives",
	},
	archetype = "Medic",
	role = "Medic",
	CanManEmplacements = false,
	MaxAttacks = 2,
	PickCustomArchetype = function (self, proto_context)  end,
	CustomEquipGear = function (self, items)  end,
	MaxHitPoints = 80,
	StartingPerks = {
		"BeefedUp",
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
			'Preset', "LegionMedic",
			'Weight', 3,
		}),
		PlaceObj('AppearanceWeight', {
			'Preset', "LegionMedic_alt",
			'Weight', 3,
		}),
	},
	Equipment = {
		"LegionMedic",
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

