UndefineClass('LegionRocketeer_Stronger')
DefineClass.LegionRocketeer_Stronger = {
	__parents = { "UnitData" },
	__generated_by_class = "ModItemUnitDataCompositeDef",


	comment = "РПГшник",
	object_class = "UnitData",
	Health = 90,
	Agility = 83,
	Strength = 88,
	Wisdom = 14,
	Leadership = 10,
	Marksmanship = 75,
	Mechanical = 40,
	Explosives = 75,
	Medical = 29,
	Portrait = "UI/EnemiesPortraits/LegionArtillery",
	BigPortrait = "UI/Enemies/LegionRaider",
	Name = T(834998812076, --[[ModItemUnitDataCompositeDef LegionRocketeer_Stronger Name]] "Гранатомётчик"),
	Randomization = true,
	Affiliation = "Legion",
	StartingLevel = 5,
	neutral_retaliate = true,
	AIKeywords = {
		"Ordnance",
		"Control",
		"Sniper",
	},
	archetype = "Artillery",
	role = "Artillery",
	CanManEmplacements = false,
	PickCustomArchetype = function (self, proto_context)  end,
	CustomEquipGear = function (self, items)
		self:TryEquip(items, "Handheld A", "HeavyWeapon")
		self:TryEquip(items, "Handheld B", "Firearm")
	end,
	MaxHitPoints = 50,
	StartingPerks = {
		"HeavyWeaponsTraining",
		"Hardened",
		"ShoulderToShoulder",
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
			'Preset', "LegionRoceteer_Stronger",
			'Weight', 2,
		}),
		PlaceObj('AppearanceWeight', {
			'Preset', "LegionRoceteer_Stronger_alt",
			'Weight', 2,
		}),
		PlaceObj('AppearanceWeight', {
			'Preset', "LegionRoceteer_Stronger_alt",
			'Weight', 2,
		}),
	},
	Equipment = {
		"LegionRocketeer",
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

