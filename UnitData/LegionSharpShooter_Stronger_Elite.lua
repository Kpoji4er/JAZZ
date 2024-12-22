UndefineClass('LegionSharpShooter_Stronger_Elite')
DefineClass.LegionSharpShooter_Stronger_Elite = {
	__parents = { "UnitData" },
	__generated_by_class = "ModItemUnitDataCompositeDef",


	object_class = "UnitData",
	Health = 80,
	Agility = 90,
	Dexterity = 73,
	Strength = 53,
	Wisdom = 58,
	Leadership = 10,
	Marksmanship = 86,
	Mechanical = 80,
	Explosives = 66,
	Medical = 30,
	Portrait = "UI/EnemiesPortraits/LegionRaider",
	BigPortrait = "UI/Enemies/LegionRaider",
	Name = T(251609051693, --[[ModItemUnitDataCompositeDef LegionSharpShooter_Stronger_Elite Name]] "Опытный Стрелок"),
	Randomization = true,
	elite = true,
	eliteCategory = "Legion",
	Affiliation = "Legion",
	StartingLevel = 4,
	neutral_retaliate = true,
	AIKeywords = {
		"Sniper",
		"Control",
		"Ordnance",
	},
	role = "Soldier",
	CustomEquipGear = function (self, items)  end,
	MaxHitPoints = 50,
	StartingPerks = {
		"Flanker",
		"Untraceable",
		"Deadeye",
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
			'Preset', "LegionSharpShooter_Stronger",
			'Weight', 3,
		}),
		PlaceObj('AppearanceWeight', {
			'Preset', "LegionSharpShooter_Stronger_alt",
			'Weight', 3,
		}),
		PlaceObj('AppearanceWeight', {
			'Preset', "LegionSharpShooter_Stronger_alt_2",
			'Weight', 3,
		}),
	},
	Equipment = {
		"LegionSharpShooter_Stronger",
	},
	AdditionalGroups = {
		PlaceObj('AdditionalGroup', {
			'Name', "LegionMale_2",
		}),
	},
	pollyvoice = "Joey",
	gender = "Male",
	VoiceResponseId = "LegionRaider",
}

