UndefineClass('LegionSergant_Stronger')
DefineClass.LegionSergant_Stronger = {
	__parents = { "UnitData" },
	__generated_by_class = "ModItemUnitDataCompositeDef",


	object_class = "UnitData",
	Health = 90,
	Agility = 86,
	Dexterity = 90,
	Strength = 70,
	Wisdom = 90,
	Leadership = 47,
	Marksmanship = 83,
	Mechanical = 50,
	Explosives = 90,
	Medical = 0,
	Portrait = "UI/EnemiesPortraits/LegionSniper",
	BigPortrait = "UI/Enemies/LegionRaider",
	Name = T(370478000653, --[[ModItemUnitDataCompositeDef LegionSergant_Stronger Name]] "Сержант"),
	Randomization = true,
	Affiliation = "Legion",
	StartingLevel = 6,
	neutral_retaliate = true,
	AIKeywords = {
		"Control",
		"Sniper",
		"Soldier",
		"Smoke",
		"Explosives",
	},
	role = "Marksman",
	OpeningAttackType = "Overwatch",
	PickCustomArchetype = function (self, proto_context)  end,
	CustomEquipGear = function (self, items)  end,
	MaxHitPoints = 50,
	StartingPerks = {
		"DeathFromAbove",
		"LightStep",
		"StressManagement",
		"ShoulderToShoulder",
		"BattleFocus",
	},
	AppearancesList = {
		PlaceObj('AppearanceWeight', {
			'Preset', "LegionSergant_Stronger",
		}),
		PlaceObj('AppearanceWeight', {
			'Preset', "LegionSergant_Stronger_alt",
		}),
		PlaceObj('AppearanceWeight', {
			'Preset', "LegionSergant_Stronger_alt_2",
		}),
	},
	Equipment = {
		"LegionSergeant_Stronger",
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

