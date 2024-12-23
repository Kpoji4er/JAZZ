UndefineClass('LegionSniper_Stronger')
DefineClass.LegionSniper_Stronger = {
	__parents = { "UnitData" },
	__generated_by_class = "ModItemUnitDataCompositeDef",


	object_class = "UnitData",
	Agility = 86,
	Dexterity = 80,
	Strength = 70,
	Wisdom = 35,
	Leadership = 33,
	Marksmanship = 90,
	Mechanical = 30,
	Explosives = 0,
	Medical = 0,
	Portrait = "UI/EnemiesPortraits/LegionSniper",
	BigPortrait = "UI/Enemies/LegionRaider",
	Name = T(650029540303, --[[ModItemUnitDataCompositeDef LegionSniper_Stronger Name]] "Опытный снайпер"),
	Randomization = true,
	Affiliation = "Legion",
	StartingLevel = 5,
	neutral_retaliate = true,
	AIKeywords = {
		"Sniper",
		"Control",
	},
	archetype = "Soldier_Sniper",
	role = "Marksman",
	AlwaysUseOpeningAttack = true,
	OpeningAttackType = "Overwatch",
	PickCustomArchetype = function (self, proto_context)  end,
	CustomEquipGear = function (self, items)
		self:TryEquip(items, "Handheld A", "Firearm")
		self:TryEquip(items, "Handheld B", "Firearm")
	end,
	MaxHitPoints = 50,
	StartingPerks = {
		"Deadeye",
		"DeathFromAbove",
		"Spiritual",
		"HitTheDeck",
	},
	AppearancesList = {
		PlaceObj('AppearanceWeight', {
			'Preset', "Legion_Marksman",
		}),
		PlaceObj('AppearanceWeight', {
			'Preset', "Legion_Marksman02",
		}),
		PlaceObj('AppearanceWeight', {
			'Preset', "Legion_Marksman03",
		}),
		PlaceObj('AppearanceWeight', {
			'Preset', "LegionSniper_Stronger",
			'Weight', 3,
		}),
		PlaceObj('AppearanceWeight', {
			'Preset', "LegionSniper_Stronger_alt",
			'Weight', 3,
		}),
		PlaceObj('AppearanceWeight', {
			'Preset', "LegionSniper_Stronger_alt_2",
			'Weight', 3,
		}),
	},
	Equipment = {
		"LegionSniper_Stronger",
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

