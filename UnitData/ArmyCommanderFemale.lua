UndefineClass('ArmyCommanderFemale')
DefineClass.ArmyCommanderFemale = {
	__parents = { "UnitData" },
	__generated_by_class = "ModItemUnitDataCompositeDef",


	object_class = "UnitData",
	Health = 89,
	Agility = 90,
	Dexterity = 91,
	Strength = 63,
	Wisdom = 91,
	Leadership = 86,
	Marksmanship = 80,
	Mechanical = 100,
	Explosives = 57,
	Medical = 89,
	Portrait = "UI/EnemiesPortraits/ArmyOfficer",
	Name = T(156931867550, --[[ModItemUnitDataCompositeDef ArmyCommanderFemale Name]] "Лейтенант"),
	Randomization = true,
	Affiliation = "Army",
	StartingLevel = 5,
	neutral_retaliate = true,
	AIKeywords = {
		"Control",
		"Flank",
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
	},
	AppearancesList = {
		PlaceObj('AppearanceWeight', {
			'Preset', "GrandChien_CommanderFemale",
		}),
	},
	Equipment = {
		"ArmyCommander",
		"RefugeeCamp_Leiutenant",
	},
	AdditionalGroups = {},
	Tier = "Elite",
	pollyvoice = "Kendra",
	gender = "Female",
	VoiceResponseId = "AnneLeMitrailleur",
	FallbackMissingVR = "VillagerFemale",
}

