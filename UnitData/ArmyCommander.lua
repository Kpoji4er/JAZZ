UndefineClass('ArmyCommander')
DefineClass.ArmyCommander = {
	__parents = { "UnitData" },
	__generated_by_class = "ModItemUnitDataCompositeDef",


	object_class = "UnitData",
	Health = 90,
	Agility = 89,
	Dexterity = 85,
	Strength = 81,
	Wisdom = 89,
	Leadership = 93,
	Marksmanship = 90,
	Mechanical = 100,
	Explosives = 76,
	Medical = 45,
	Portrait = "UI/EnemiesPortraits/ArmyOfficer",
	Name = T(309190250480, --[[ModItemUnitDataCompositeDef ArmyCommander Name]] "Капитан"),
	Randomization = true,
	Affiliation = "Army",
	StartingLevel = 5,
	neutral_retaliate = true,
	AIKeywords = {
		"Control",
		"Flank",
		"Soldier",
	},
	archetype = "Skirmisher",
	role = "Commander",
	MaxAttacks = 2,
	PickCustomArchetype = function (self, proto_context)
		local enemy, dist = GetNearestEnemy(self)
		local archetype = self.archetype
		local weapon_class = "Firearm"
		
		if enemy and dist < 12*const.SlabSizeX then
			archetype = "Soldier"
			weapon_class = "Firearm"
			PlayVoiceResponse(self, "AIArchetypeAngry")
		end
		
		if not self:GetActiveWeapons(weapon_class) then
			AIPlayCombatAction("ChangeWeapon", self, 0)
		end
		
		return archetype
	end,
	MaxHitPoints = 80,
	StartingPerks = {
		"BeefedUp",
		"BunsPerk",
		"CQCTraining",
	},
	AppearancesList = {
		PlaceObj('AppearanceWeight', {
			'Preset', "GrandChien_Officer",
		}),
	},
	Equipment = {
		"ArmyCommander",
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
	Tier = "Elite",
	pollyvoice = "Joey",
	gender = "Male",
	VoiceResponseId = "ArmySoldier",
}

