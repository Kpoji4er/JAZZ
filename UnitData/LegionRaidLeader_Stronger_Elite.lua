UndefineClass('LegionRaidLeader_Stronger_Elite')
DefineClass.LegionRaidLeader_Stronger_Elite = {
	__parents = { "UnitData" },
	__generated_by_class = "ModItemUnitDataCompositeDef",


	object_class = "UnitData",
	Health = 100,
	Agility = 100,
	Dexterity = 95,
	Strength = 95,
	Wisdom = 85,
	Leadership = 81,
	Marksmanship = 94,
	Mechanical = 100,
	Explosives = 75,
	Medical = 43,
	Portrait = "UI/EnemiesPortraits/LegionOfficer",
	BigPortrait = "UI/Enemies/LegionRaider",
	Name = T(819132475338, --[[ModItemUnitDataCompositeDef LegionRaidLeader_Stronger_Elite Name]] "Элитный командир налётчиков"),
	Randomization = true,
	elite = true,
	eliteCategory = "Legion",
	Affiliation = "Legion",
	StartingLevel = 8,
	neutral_retaliate = true,
	AIKeywords = {
		"Smoke",
		"Soldier",
		"Flank",
		"Sniper",
	},
	role = "Commander",
	AlwaysUseOpeningAttack = true,
	OpeningAttackType = "Overwatch",
	MaxAttacks = 2,
	PickCustomArchetype = function (self, proto_context)  end,
	CustomEquipGear = function (self, items)  end,
	MaxHitPoints = 80,
	StartingPerks = {
		"ShoulderToShoulder",
		"GruntyPerk",
		"BeefedUp",
		"BuildingConfidence",
		"LeadFromTheFront",
		"LightningReactionNPC",
		"TrueGrit",
		"Berserker",
		"AutoWeapons",
	},
	AppearancesList = {
		PlaceObj('AppearanceWeight', {
			'Preset', "LegionRaidLeader_Stronger_Elite",
		}),
		PlaceObj('AppearanceWeight', {
			'Preset', "LegionRaidLeader_Stronger_Elite_alt",
		}),
	},
	Equipment = {
		"LegionSentry_Stronger_Elite",
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

