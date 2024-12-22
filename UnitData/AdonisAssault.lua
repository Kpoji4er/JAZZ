UndefineClass('AdonisAssault')
DefineClass.AdonisAssault = {
	__parents = { "UnitData" },
	__generated_by_class = "ModItemUnitDataCompositeDef",


	object_class = "UnitData",
	Health = 91,
	Agility = 85,
	Dexterity = 85,
	Strength = 85,
	Wisdom = 70,
	Leadership = 50,
	Marksmanship = 84,
	Explosives = 0,
	Medical = 0,
	Portrait = "UI/EnemiesPortraits/AdonisSoldier",
	Name = T(422952821275, --[[ModItemUnitDataCompositeDef AdonisAssault Name]] "Тяжелый Штурмовик"),
	Randomization = true,
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
	CustomEquipGear = function (self, items)
		self:TryEquip(items, "Handheld A", "AssaultRifle"--[[, "_762NATO_Tracer","_556_Basic","_556_HP","_762NATO_Basic","_545_EPR"]])
		self:TryEquip(items, "Handheld A", "GrenadeLauncher"--[[, "_40mmFlashbangGrenade","_40mmFragGrenade"]])
	end,
	unitPowerModifier = 75,
	MaxHitPoints = 50,
	StartingPerks = {
		"AutoWeapons",
		"LightningReactionNPC",
	},
	AppearancesList = {
		PlaceObj('AppearanceWeight', {
			'Preset', "Adonis_Soldier",
		}),
	},
	Equipment = {
		"AdonisAssault",
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

