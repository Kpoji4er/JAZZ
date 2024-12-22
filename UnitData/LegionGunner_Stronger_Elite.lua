UndefineClass('LegionGunner_Stronger_Elite')
DefineClass.LegionGunner_Stronger_Elite = {
	__parents = { "UnitData" },
	__generated_by_class = "ModItemUnitDataCompositeDef",


	object_class = "UnitData",
	Health = 90,
	Agility = 85,
	Dexterity = 90,
	Strength = 89,
	Wisdom = 73,
	Leadership = 55,
	Marksmanship = 90,
	Mechanical = 80,
	Explosives = 28,
	Medical = 35,
	Portrait = "UI/EnemiesPortraits/LegionHeavy",
	BigPortrait = "UI/Enemies/LegionRaider",
	Name = T(658547850911, --[[ModItemUnitDataCompositeDef LegionGunner_Stronger_Elite Name]] "Опытный пулемётчик"),
	Randomization = true,
	Affiliation = "Legion",
	StartingLevel = 9,
	neutral_retaliate = true,
	AIKeywords = {
		"Control",
		"Soldier",
		"Ordnance",
		"Gunner",
	},
	archetype = "HeavyGunner",
	role = "Heavy",
	MaxAttacks = 4,
	PickCustomArchetype = function (self, proto_context)  end,
	CustomEquipGear = function (self, items)
		self:TryEquip(items, "Handheld A", "Firearm")
		self:TryEquip(items, "Handheld B", "Firearm")
	end,
	MaxHitPoints = 85,
	StartingPerks = {
		"HeavyWeaponsTraining",
		"TakeAim",
		"OverwatchExpert",
		"Ironclad",
		"Counterfire",
	},
	AppearancesList = {
		PlaceObj('AppearanceWeight', {
			'Preset', "Legion_Heavy",
		}),
		PlaceObj('AppearanceWeight', {
			'Preset', "Legion_Heavy02",
		}),
		PlaceObj('AppearanceWeight', {
			'Preset', "Legion_Heavy03",
		}),
		PlaceObj('AppearanceWeight', {
			'Preset', "LegionGunner_Stronger",
			'Weight', 3,
		}),
		PlaceObj('AppearanceWeight', {
			'Preset', "LegionGunner_Stronger_alt",
			'Weight', 3,
		}),
		PlaceObj('AppearanceWeight', {
			'Preset', "LegionGunner_Stronger_alt_2",
			'Weight', 3,
		}),
		PlaceObj('AppearanceWeight', {
			'Preset', "LegionGunner_Stronger_Elite",
			'Weight', 5,
		}),
		PlaceObj('AppearanceWeight', {
			'Preset', "LegionGunner_Stronger_Elite_alt",
			'Weight', 5,
		}),
	},
	Equipment = {
		"LegionGunner_Stronger",
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

