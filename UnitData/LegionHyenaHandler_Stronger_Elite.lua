UndefineClass('LegionHyenaHandler_Stronger_Elite')
DefineClass.LegionHyenaHandler_Stronger_Elite = {
	__parents = { "UnitData" },
	__generated_by_class = "ModItemUnitDataCompositeDef",


	object_class = "UnitData",
	Health = 98,
	Agility = 96,
	Dexterity = 87,
	Strength = 83,
	Wisdom = 64,
	Leadership = 81,
	Marksmanship = 72,
	Mechanical = 80,
	Explosives = 68,
	Medical = 68,
	Portrait = "UI/EnemiesPortraits/LegionStormer",
	BigPortrait = "UI/Enemies/LegionRaider",
	Name = T(766068288172, --[[ModItemUnitDataCompositeDef LegionHyenaHandler_Stronger_Elite Name]] "Опытный дрессировщик"),
	Randomization = true,
	Affiliation = "Legion",
	StartingLevel = 7,
	neutral_retaliate = true,
	AIKeywords = {
		"Smoke",
		"Control",
		"Explosives",
		"Nova",
		"Ordnance",
	},
	role = "Commander",
	AlwaysUseOpeningAttack = true,
	OpeningAttackType = "Overwatch",
	MaxAttacks = 2,
	PickCustomArchetype = function (self, proto_context)  end,
	CustomEquipGear = function (self, items)  end,
	MaxHitPoints = 80,
	StartingPerks = {
		"BeefedUp",
		"Counterfire",
		"Hardened",
		"GruntyPerk",
		"Flanker",
		"TakeAim",
		"ShoulderToShoulder",
	},
	AppearancesList = {
		PlaceObj('AppearanceWeight', {
			'Preset', "Legion_Stormer03",
		}),
		PlaceObj('AppearanceWeight', {
			'Preset', "LegionHyenaHandler_Stronger_Elite",
			'Weight', 3,
		}),
		PlaceObj('AppearanceWeight', {
			'Preset', "LegionHyenaHandler_Stronger_Elite_alt",
			'Weight', 3,
		}),
	},
	Equipment = {
		"LegionSentry_Stronger",
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

