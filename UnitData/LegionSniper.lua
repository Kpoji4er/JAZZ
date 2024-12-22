UndefineClass('LegionSniper')
DefineClass.LegionSniper = {
	__parents = { "UnitData" },
	__generated_by_class = "ModItemUnitDataCompositeDef",


	comment = "Снайпер",
	object_class = "UnitData",
	Health = 65,
	Agility = 80,
	Dexterity = 76,
	Strength = 65,
	Wisdom = 70,
	Leadership = 33,
	Marksmanship = 78,
	Mechanical = 24,
	Explosives = 30,
	Medical = 6,
	Portrait = "UI/EnemiesPortraits/LegionSniper",
	BigPortrait = "UI/Enemies/LegionRaider",
	Name = T(762054446751, --[[ModItemUnitDataCompositeDef LegionSniper Name]] "Снайпер"),
	Randomization = true,
	Affiliation = "Legion",
	StartingLevel = 2,
	neutral_retaliate = true,
	AIKeywords = {
		"Sniper",
		"Flank",
		"Control",
	},
	archetype = "Soldier_Sniper",
	role = "Marksman",
	MaxAttacks = 2,
	PickCustomArchetype = function (self, proto_context)  end,
	CustomEquipGear = function (self, items)
		self:TryEquip(items, "Handheld A", "Firearm")
		self:TryEquip(items, "Handheld B", "Pistol")
	end,
	MaxHitPoints = 50,
	StartingPerks = {
		"Deadeye",
		"Spiritual",
		"DeathFromAbove",
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
			'Preset', "LegionSniper",
			'Weight', 3,
		}),
		PlaceObj('AppearanceWeight', {
			'Preset', "LegionSniper_alt",
			'Weight', 3,
		}),
		PlaceObj('AppearanceWeight', {
			'Preset', "LegionSniper_alt_2",
			'Weight', 3,
		}),
	},
	Equipment = {
		"LegionSniper",
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

