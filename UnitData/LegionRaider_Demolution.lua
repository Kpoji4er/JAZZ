UndefineClass('LegionRaider_Demolution')
DefineClass.LegionRaider_Demolution = {
	__parents = { "UnitData" },
	__generated_by_class = "ModItemUnitDataCompositeDef",


	comment = "Стрелок базовый",
	object_class = "UnitData",
	Health = 81,
	Agility = 80,
	Dexterity = 70,
	Strength = 70,
	Wisdom = 40,
	Leadership = 25,
	Marksmanship = 73,
	Mechanical = 0,
	Explosives = 77,
	Medical = 0,
	Portrait = "UI/EnemiesPortraits/LegionSoldier",
	BigPortrait = "UI/Enemies/LegionRaider",
	Name = T(231149210996, --[[ModItemUnitDataCompositeDef LegionRaider_Demolution Name]] "Мародёр"),
	Randomization = true,
	Affiliation = "Legion",
	StartingLevel = 3,
	neutral_retaliate = true,
	AIKeywords = {
		"Soldier",
		"Explosives",
		"Ordnance",
	},
	role = "Soldier",
	OpeningAttackType = "Overwatch",
	PinnedDownChance = 40,
	CustomEquipGear = function (self, items)
		self:TryEquip(items, "Handheld A", "AssaultRifle")
		self:TryEquip(items, "Handheld A", "GrenadeLauncher")
	end,
	MaxHitPoints = 50,
	StartingPerks = {
		"Flanker",
		"RelentlessAdvance",
		"BunsPerk",
	},
	AppearancesList = {
		PlaceObj('AppearanceWeight', {
			'Preset', "Legion_Soldier",
		}),
		PlaceObj('AppearanceWeight', {
			'Preset', "Legion_Soldier02",
		}),
		PlaceObj('AppearanceWeight', {
			'Preset', "Legion_Soldier03",
		}),
		PlaceObj('AppearanceWeight', {
			'Preset', "Legion_Soldier04",
		}),
		PlaceObj('AppearanceWeight', {
			'Preset', "Legion_Soldier05",
		}),
		PlaceObj('AppearanceWeight', {
			'Preset', "Legion_Soldier06",
		}),
		PlaceObj('AppearanceWeight', {
			'Preset', "LegionRaider",
			'Weight', 3,
		}),
		PlaceObj('AppearanceWeight', {
			'Preset', "LegionRaider_alt",
			'Weight', 3,
		}),
		PlaceObj('AppearanceWeight', {
			'Preset', "LegionRaider_alt_2",
			'Weight', 3,
		}),
	},
	Equipment = {
		"LegionRaiders_GL",
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

