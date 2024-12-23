UndefineClass('LegionGunner')
DefineClass.LegionGunner = {
	__parents = { "UnitData" },
	__generated_by_class = "ModItemUnitDataCompositeDef",


	comment = "Пулеметчик | Контроль",
	object_class = "UnitData",
	Health = 76,
	Agility = 78,
	Dexterity = 80,
	Strength = 89,
	Wisdom = 23,
	Leadership = 20,
	Marksmanship = 70,
	Mechanical = 30,
	Explosives = 0,
	Medical = 0,
	Portrait = "UI/EnemiesPortraits/LegionHeavy",
	BigPortrait = "UI/Enemies/LegionRaider",
	Name = T(875645126950, --[[ModItemUnitDataCompositeDef LegionGunner Name]] "Пулемётчик"),
	Randomization = true,
	Affiliation = "Legion",
	StartingLevel = 2,
	neutral_retaliate = true,
	AIKeywords = {
		"Control",
		"Soldier",
		"Gunner",
	},
	archetype = "HeavyGunner",
	role = "Heavy",
	OpeningAttackType = "Overwatch",
	PickCustomArchetype = function (self, proto_context)  end,
	CustomEquipGear = function (self, items)
		self:TryEquip(items, "Handheld A", "Firearm")
		self:TryEquip(items, "Handheld B", "SMG")
	end,
	MaxHitPoints = 85,
	StartingPerks = {
		"TakeAim",
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
			'Preset', "LegionGunner",
			'Weight', 3,
		}),
		PlaceObj('AppearanceWeight', {
			'Preset', "LegionGunner_alt",
			'Weight', 3,
		}),
	},
	Equipment = {
		"LegionGunner",
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

