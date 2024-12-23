UndefineClass('LegionGoon')
DefineClass.LegionGoon = {
	__parents = { "UnitData" },
	__generated_by_class = "ModItemUnitDataCompositeDef",


	comment = "Пистолетчик | Харасмент",
	object_class = "UnitData",
	Health = 67,
	Agility = 71,
	Dexterity = 80,
	Strength = 55,
	Wisdom = 40,
	Leadership = 20,
	Marksmanship = 68,
	Mechanical = 0,
	Explosives = 64,
	Medical = 0,
	Portrait = "UI/EnemiesPortraits/LegionRecon",
	BigPortrait = "UI/Enemies/LegionRaider",
	Name = T(281298678585, --[[ModItemUnitDataCompositeDef LegionGoon Name]] "Головорез"),
	Randomization = true,
	Affiliation = "Legion",
	StartingLevel = 2,
	neutral_retaliate = true,
	AIKeywords = {
		"MobileShot",
		"Control",
		"Flank",
		"Explosives",
	},
	archetype = "Skirmisher",
	role = "Recon",
	MaxAttacks = 2,
	PickCustomArchetype = function (self, proto_context)  end,
	CustomEquipGear = function (self, items)  end,
	MaxHitPoints = 50,
	StartingPerks = {
		"Ambidextrous",
		"Flanker",
	},
	AppearancesList = {
		PlaceObj('AppearanceWeight', {
			'Preset', "Legion_Recon",
		}),
		PlaceObj('AppearanceWeight', {
			'Preset', "Legion_Recon02",
		}),
		PlaceObj('AppearanceWeight', {
			'Preset', "Legion_Recon03",
		}),
		PlaceObj('AppearanceWeight', {
			'Preset', "LegionGoon",
			'Weight', 2,
		}),
		PlaceObj('AppearanceWeight', {
			'Preset', "LegionGoon_alt",
			'Weight', 2,
		}),
		PlaceObj('AppearanceWeight', {
			'Preset', "LegionGoon_alt_2",
			'Weight', 2,
		}),
		PlaceObj('AppearanceWeight', {
			'Preset', "LegionGoon_alt_3",
			'Weight', 2,
		}),
	},
	Equipment = {
		"LegionGoon",
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

