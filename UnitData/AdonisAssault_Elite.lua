UndefineClass('AdonisAssault_Elite')
DefineClass.AdonisAssault_Elite = {
	__parents = { "UnitData" },
	__generated_by_class = "ModItemUnitDataCompositeDef",


	object_class = "UnitData",
	Health = 95,
	Agility = 92,
	Dexterity = 90,
	Strength = 85,
	Wisdom = 68,
	Leadership = 84,
	Marksmanship = 95,
	Mechanical = 80,
	Explosives = 77,
	Medical = 52,
	Portrait = "UI/EnemiesPortraits/AdonisSoldier",
	Name = T(706893505616, --[[ModItemUnitDataCompositeDef AdonisAssault_Elite Name]] "Элитный Тяжелый Штурмовик"),
	Randomization = true,
	elite = true,
	eliteCategory = "Foreigners",
	Affiliation = "Adonis",
	StartingLevel = 6,
	neutral_retaliate = true,
	AIKeywords = {
		"Soldier",
		"Ordnance",
		"Explosives",
	},
	role = "Soldier",
	MaxAttacks = 2,
	PickCustomArchetype = function (self, proto_context)  end,
	CustomEquipGear = function (self, items)
		self:TryEquip(items, "Handheld A", "AssaultRifle"--[[, "_762NATO_Tracer","_556_Basic","_556_HP","_762NATO_Basic","_545_EPR"]])
		self:TryEquip(items, "Handheld A", "GrenadeLauncher"--[[, "_40mmFlashbangGrenade","_40mmFragGrenade"]])
	end,
	MaxHitPoints = 50,
	StartingPerks = {
		"AutoWeapons",
		"LightningReactionNPC",
		"StressManagement",
	},
	AppearancesList = {
		PlaceObj('AppearanceWeight', {
			'Preset', "Adonis_Soldier",
		}),
	},
	Equipment = {
		"AdonisAssault_Elite",
	},
	AdditionalGroups = {
		PlaceObj('AdditionalGroup', {
			'Weight', 50,
			'Exclusive', true,
			'Name', "AdonisMale_1",
		}),
		PlaceObj('AdditionalGroup', {
			'Weight', 50,
			'Exclusive', true,
			'Name', "AdonisMale_2",
		}),
	},
	Tier = "Elite",
	pollyvoice = "Joey",
	gender = "Male",
	VoiceResponseId = "AdonisAssault",
}

