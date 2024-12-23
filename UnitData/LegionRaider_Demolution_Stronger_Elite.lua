UndefineClass('LegionRaider_Demolution_Stronger_Elite')
DefineClass.LegionRaider_Demolution_Stronger_Elite = {
	__parents = { "UnitData" },
	__generated_by_class = "ModItemUnitDataCompositeDef",


	object_class = "UnitData",
	Health = 81,
	Agility = 75,
	Dexterity = 70,
	Strength = 70,
	Wisdom = 40,
	Leadership = 25,
	Marksmanship = 73,
	Mechanical = 80,
	Explosives = 10,
	Medical = 0,
	Portrait = "UI/EnemiesPortraits/LegionSoldier",
	BigPortrait = "UI/Enemies/LegionRaider",
	Name = T(497659792215, --[[ModItemUnitDataCompositeDef LegionRaider_Demolution_Stronger_Elite Name]] "Мародёр"),
	Randomization = true,
	Affiliation = "Legion",
	StartingLevel = 4,
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
		"AutoWeapons",
		"RelentlessAdvance",
		"BunsPerk",
		"TakeAim",
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
			'Preset', "LegionRaider_Stronger_Elite",
			'Weight', 4,
		}),
		PlaceObj('AppearanceWeight', {
			'Preset', "LegionRaider_Stronger_Elite_alt",
			'Weight', 4,
		}),
		PlaceObj('AppearanceWeight', {
			'Preset', "LegionRaider_Stronger_Elite_alt_2",
			'Weight', 4,
		}),
	},
	Equipment = {
		"LegionRaider_Stronger_Elite_GL",
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

