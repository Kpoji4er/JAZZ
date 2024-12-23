UndefineClass('LegionMortarman_Stronger')
DefineClass.LegionMortarman_Stronger = {
	__parents = { "UnitData" },
	__generated_by_class = "ModItemUnitDataCompositeDef",


	comment = "Минометчик",
	object_class = "UnitData",
	Health = 65,
	Agility = 81,
	Dexterity = 43,
	Strength = 96,
	Wisdom = 14,
	Leadership = 10,
	Marksmanship = 50,
	Mechanical = 30,
	Explosives = 90,
	Medical = 0,
	Portrait = "UI/EnemiesPortraits/LegionArtillery",
	BigPortrait = "UI/Enemies/LegionRaider",
	Name = T(603360674448, --[[ModItemUnitDataCompositeDef LegionMortarman_Stronger Name]] "Миномётчик"),
	Randomization = true,
	Affiliation = "Legion",
	StartingLevel = 5,
	neutral_retaliate = true,
	AIKeywords = {
		"Explosives",
		"Sniper",
	},
	archetype = "Artillery",
	role = "Artillery",
	CanManEmplacements = false,
	MaxAttacks = 2,
	PickCustomArchetype = function (self, proto_context)  end,
	CustomEquipGear = function (self, items)
		self:TryEquip(items, "Handheld A", "HeavyWeapon")
		self:TryEquip(items, "Handheld B", "AssaultRifle")
	end,
	MaxHitPoints = 50,
	StartingPerks = {
		"BattleFocus",
		"LightningReactionNPC",
		"TrueGrit",
	},
	AppearancesList = {
		PlaceObj('AppearanceWeight', {
			'Preset', "Legion_Artillery",
		}),
		PlaceObj('AppearanceWeight', {
			'Preset', "Legion_Artillery02",
		}),
		PlaceObj('AppearanceWeight', {
			'Preset', "Legion_Artillery03",
		}),
		PlaceObj('AppearanceWeight', {
			'Preset', "LegionMortalman_Stronger",
			'Weight', 3,
		}),
		PlaceObj('AppearanceWeight', {
			'Preset', "LegionMortalman_Stronger_alt",
			'Weight', 3,
		}),
		PlaceObj('AppearanceWeight', {
			'Preset', "LegionMortalman_Stronger_alt_2",
			'Weight', 3,
		}),
	},
	Equipment = {
		"LegionMortarman",
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

