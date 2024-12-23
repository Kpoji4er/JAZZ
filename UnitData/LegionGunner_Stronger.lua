UndefineClass('LegionGunner_Stronger')
DefineClass.LegionGunner_Stronger = {
	__parents = { "UnitData" },
	__generated_by_class = "ModItemUnitDataCompositeDef",


	object_class = "UnitData",
	Health = 90,
	Agility = 85,
	Dexterity = 90,
	Strength = 89,
	Wisdom = 25,
	Leadership = 55,
	Marksmanship = 86,
	Mechanical = 50,
	Explosives = 28,
	Medical = 35,
	Portrait = "UI/EnemiesPortraits/LegionHeavy",
	BigPortrait = "UI/Enemies/LegionRaider",
	Name = T(394818311379, --[[ModItemUnitDataCompositeDef LegionGunner_Stronger Name]] "Опытный пулемётчик"),
	Randomization = true,
	Affiliation = "Legion",
	StartingLevel = 6,
	neutral_retaliate = true,
	AIKeywords = {
		"Control",
		"Soldier",
		"Gunner",
		"Nova",
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

