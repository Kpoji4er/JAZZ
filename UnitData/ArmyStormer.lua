UndefineClass('ArmyStormer')
DefineClass.ArmyStormer = {
	__parents = { "UnitData" },
	__generated_by_class = "ModItemUnitDataCompositeDef",


	object_class = "UnitData",
	Health = 95,
	Agility = 95,
	Dexterity = 73,
	Strength = 95,
	Leadership = 65,
	Marksmanship = 87,
	Mechanical = 40,
	Explosives = 81,
	Medical = 55,
	Portrait = "UI/EnemiesPortraits/ArmyStormer",
	BigPortrait = "UI/Enemies/LegionRaider",
	Name = T(828560012059, --[[ModItemUnitDataCompositeDef ArmyStormer Name]] "Штурмовик"),
	Randomization = true,
	Affiliation = "Army",
	StartingLevel = 5,
	neutral_retaliate = true,
	AIKeywords = {
		"Ordnance",
		"Explosives",
		"Soldier",
	},
	role = "Stormer",
	CanManEmplacements = false,
	MaxAttacks = 2,
	PickCustomArchetype = function (self, proto_context)  end,
	CustomEquipGear = function (self, items)
		self:TryEquip(items, "Handheld A", "AssaultRifle"--[[, "_762NATO_Tracer","_556_Basic","_556_HP","_762NATO_Basic","_545_EPR"]])
		self:TryEquip(items, "Handheld A", "GrenadeLauncher"--[[, "_40mmFlashbangGrenade","_40mmFragGrenade"]])
	end,
	MaxHitPoints = 100,
	StartingPerks = {
		"BeefedUp",
		"MeleeTraining",
		"MinFreeMove",
		"Shatterhand",
	},
	AppearancesList = {
		PlaceObj('AppearanceWeight', {
			'Preset', "GrandChien_Stormer",
		}),
	},
	Equipment = {
		"ArmyStormer",
	},
	AdditionalGroups = {
		PlaceObj('AdditionalGroup', {
			'Weight', 50,
			'Exclusive', true,
			'Name', "ArmyMale_1",
		}),
		PlaceObj('AdditionalGroup', {
			'Weight', 50,
			'Exclusive', true,
			'Name', "ArmyMale_2",
		}),
	},
	pollyvoice = "Joey",
	gender = "Male",
	VoiceResponseId = "ArmySoldier",
}

