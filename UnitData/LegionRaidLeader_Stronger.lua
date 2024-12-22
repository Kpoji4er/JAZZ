UndefineClass('LegionRaidLeader_Stronger')
DefineClass.LegionRaidLeader_Stronger = {
	__parents = { "UnitData" },
	__generated_by_class = "ModItemUnitDataCompositeDef",


	object_class = "UnitData",
	Health = 91,
	Agility = 85,
	Dexterity = 80,
	Strength = 75,
	Wisdom = 80,
	Leadership = 81,
	Marksmanship = 85,
	Mechanical = 70,
	Explosives = 50,
	Medical = 71,
	Portrait = "UI/EnemiesPortraits/LegionOfficer",
	BigPortrait = "UI/Enemies/LegionRaider",
	Name = T(192759453415, --[[ModItemUnitDataCompositeDef LegionRaidLeader_Stronger Name]] "Опытный командир налётчиков"),
	Randomization = true,
	Affiliation = "Legion",
	StartingLevel = 7,
	neutral_retaliate = true,
	AIKeywords = {
		"Control",
		"Smoke",
		"Explosives",
		"Soldier",
		"Ordnance",
		"RunAndGun",
	},
	role = "Commander",
	AlwaysUseOpeningAttack = true,
	OpeningAttackType = "Overwatch",
	MaxAttacks = 4,
	PickCustomArchetype = function (self, proto_context)  end,
	CustomEquipGear = function (self, items)  end,
	MaxHitPoints = 80,
	StartingPerks = {
		"ShoulderToShoulder",
		"GruntyPerk",
		"BeefedUp",
		"BuildingConfidence",
		"LeadFromTheFront",
	},
	AppearancesList = {
		PlaceObj('AppearanceWeight', {
			'Preset', "Legion_Shaman",
		}),
		PlaceObj('AppearanceWeight', {
			'Preset', "Legion_Shaman02",
		}),
		PlaceObj('AppearanceWeight', {
			'Preset', "Legion_Shaman03",
		}),
		PlaceObj('AppearanceWeight', {
			'Preset', "LegionRaidLeader_Stronger",
			'Weight', 4,
		}),
		PlaceObj('AppearanceWeight', {
			'Preset', "LegionRaidLeader_Stronger_alt",
			'Weight', 4,
		}),
		PlaceObj('AppearanceWeight', {
			'Preset', "LegionRaidLeader_Stronger_alt_2",
			'Weight', 4,
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

