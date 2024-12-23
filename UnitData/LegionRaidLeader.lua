UndefineClass('LegionRaidLeader')
DefineClass.LegionRaidLeader = {
	__parents = { "UnitData" },
	__generated_by_class = "ModItemUnitDataCompositeDef",


	comment = "Лидер / Оверватчер",
	object_class = "UnitData",
	Health = 80,
	Agility = 75,
	Dexterity = 82,
	Strength = 70,
	Wisdom = 70,
	Leadership = 81,
	Marksmanship = 75,
	Mechanical = 15,
	Explosives = 48,
	Medical = 47,
	Portrait = "UI/EnemiesPortraits/LegionOfficer",
	BigPortrait = "UI/Enemies/LegionRaider",
	Name = T(174256174654, --[[ModItemUnitDataCompositeDef LegionRaidLeader Name]] "Командир налётчиков"),
	Randomization = true,
	Affiliation = "Legion",
	StartingLevel = 3,
	neutral_retaliate = true,
	AIKeywords = {
		"Smoke",
		"Heal_Low",
		"Flank",
		"Soldier",
		"Explosives",
	},
	role = "Commander",
	OpeningAttackType = "Overwatch",
	PickCustomArchetype = function (self, proto_context)  end,
	CustomEquipGear = function (self, items)  end,
	MaxHitPoints = 80,
	StartingPerks = {
		"ShoulderToShoulder",
		"GruntyPerk",
		"BeefedUp",
		"BuildingConfidence",
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
			'Preset', "LegionRaidLeader",
			'Weight', 3,
		}),
		PlaceObj('AppearanceWeight', {
			'Preset', "LegionRaidLeader_alt",
			'Weight', 3,
		}),
		PlaceObj('AppearanceWeight', {
			'Preset', "LegionRaidLeader_alt_2",
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

