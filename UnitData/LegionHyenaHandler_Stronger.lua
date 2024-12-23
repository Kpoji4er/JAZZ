UndefineClass('LegionHyenaHandler_Stronger')
DefineClass.LegionHyenaHandler_Stronger = {
	__parents = { "UnitData" },
	__generated_by_class = "ModItemUnitDataCompositeDef",


	comment = "Дрессировщик - Командир",
	object_class = "UnitData",
	Health = 90,
	Agility = 85,
	Dexterity = 55,
	Wisdom = 41,
	Leadership = 81,
	Marksmanship = 75,
	Mechanical = 50,
	Explosives = 10,
	Medical = 68,
	Portrait = "UI/EnemiesPortraits/LegionStormer",
	BigPortrait = "UI/Enemies/LegionRaider",
	Name = T(302888566713, --[[ModItemUnitDataCompositeDef LegionHyenaHandler_Stronger Name]] "Дрессировщик гиен"),
	Randomization = true,
	Affiliation = "Legion",
	StartingLevel = 5,
	neutral_retaliate = true,
	AIKeywords = {
		"Control",
		"Smoke",
		"Soldier",
		"Sniper",
	},
	role = "Commander",
	RepositionArchetype = "Skirmisher",
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
			'Preset', "LegionHyenaHandler_Stronger",
			'Weight', 3,
		}),
		PlaceObj('AppearanceWeight', {
			'Preset', "LegionHyenaHandler_Stronger_alt",
			'Weight', 3,
		}),
		PlaceObj('AppearanceWeight', {
			'Preset', "LegionHyenaHandler_Stronger_alt_2",
			'Weight', 3,
		}),
	},
	Equipment = {
		"LegionSentry",
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

