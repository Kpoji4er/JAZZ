UndefineClass('LegionHyena_Stronger')
DefineClass.LegionHyena_Stronger = {
	__parents = { "UnitData" },
	__generated_by_class = "ModItemUnitDataCompositeDef",


	comment = "Гиена",
	object_class = "UnitData",
	Health = 40,
	Agility = 90,
	Dexterity = 77,
	Strength = 80,
	Wisdom = 10,
	Leadership = 0,
	Marksmanship = 0,
	Mechanical = 0,
	Explosives = 0,
	Medical = 0,
	Portrait = "UI/EnemiesPortraits/Hyena_Legion",
	Name = T(802337912455, --[[ModItemUnitDataCompositeDef LegionHyena_Stronger Name]] "Дрессированная гиена"),
	Randomization = true,
	Affiliation = "Legion",
	StartingLevel = 2,
	neutral_retaliate = true,
	archetype = "Beast_Hyena",
	role = "Beast",
	CanManEmplacements = false,
	MaxAttacks = 2,
	MaxHitPoints = 60,
	StartingPerks = {
		"MartialArts",
		"CQCTraining",
		"BattleFocus",
		"ColdHeart",
	},
	AppearancesList = {
		PlaceObj('AppearanceWeight', {
			'Preset', "Hyena_Base_2",
		}),
		PlaceObj('AppearanceWeight', {
			'Preset', "Hyena_Base_4",
		}),
		PlaceObj('AppearanceWeight', {
			'Preset', "Hyena_Base_5",
		}),
	},
	Equipment = {
		"Beast_Hyena",
	},
	AdditionalGroups = {},
	species = "Hyena",
	body_type = "Small animal",
}

