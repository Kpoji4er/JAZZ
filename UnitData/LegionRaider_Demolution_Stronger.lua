UndefineClass('LegionRaider_Demolution_Stronger')
DefineClass.LegionRaider_Demolution_Stronger = {
	__parents = { "UnitData" },
	__generated_by_class = "ModItemUnitDataCompositeDef",


	comment = "Стрелок базовый",
	object_class = "UnitData",
	Health = 86,
	Agility = 83,
	Dexterity = 70,
	Strength = 70,
	Wisdom = 40,
	Leadership = 25,
	Marksmanship = 73,
	Mechanical = 20,
	Explosives = 85,
	Medical = 0,
	Portrait = "UI/EnemiesPortraits/LegionSoldier",
	BigPortrait = "UI/Enemies/LegionRaider",
	Name = T(299155932040, --[[ModItemUnitDataCompositeDef LegionRaider_Demolution_Stronger Name]] "Мародёр"),
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
	RepositionArchetype = "HeavyGunner",
	OpeningAttackType = "Overwatch",
	PinnedDownChance = 40,
	CustomEquipGear = function (self, items)
		self:TryEquip(items, "Handheld A", "AssaultRifle")
		self:TryEquip(items, "Handheld A", "GrenadeLauncher")
	end,
	MaxHitPoints = 50,
	StartingPerks = {
		"TrueGrit",
		"Flanker",
		"Optimist",
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
			'Preset', "LegionRaider_Stronger",
			'Weight', 4,
		}),
		PlaceObj('AppearanceWeight', {
			'Preset', "LegionRaider_Stronger_alt",
			'Weight', 4,
		}),
		PlaceObj('AppearanceWeight', {
			'Preset', "LegionRaider_Stronger_alt_2",
			'Weight', 4,
		}),
		PlaceObj('AppearanceWeight', {
			'Preset', "LegionRaider_Stronger_alt_3",
			'Weight', 4,
		}),
	},
	Equipment = {
		"LegionRaider_Stronger_GL",
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

