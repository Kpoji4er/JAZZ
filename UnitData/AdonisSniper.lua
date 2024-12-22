UndefineClass('AdonisSniper')
DefineClass.AdonisSniper = {
	__parents = { "UnitData" },
	__generated_by_class = "ModItemUnitDataCompositeDef",


	object_class = "UnitData",
	Health = 78,
	Agility = 90,
	Dexterity = 85,
	Strength = 85,
	Wisdom = 84,
	Leadership = 20,
	Marksmanship = 89,
	Explosives = 0,
	Medical = 25,
	Portrait = "UI/EnemiesPortraits/AdonisSniper",
	Name = T(103135217338, --[[ModItemUnitDataCompositeDef AdonisSniper Name]] "Тактический снайпер"),
	Randomization = true,
	Affiliation = "Adonis",
	StartingLevel = 5,
	neutral_retaliate = true,
	AIKeywords = {
		"Sniper",
	},
	role = "Marksman",
	AlwaysUseOpeningAttack = true,
	OpeningAttackType = "PinDown",
	MaxAttacks = 1,
	PickCustomArchetype = function (self, proto_context)
		local enemy, dist = GetNearestEnemy(self)
		local archetype = self.archetype
		local weapon_class = "Firearm"
		
		if enemy and dist < 5*const.SlabSizeX then
			archetype = "Skirmisher"
			weapon_class = "Revolver"
			PlayVoiceResponse(self, "AIArchetypeScared")
		end
		
		if not self:GetActiveWeapons(weapon_class) then
			AIPlayCombatAction("ChangeWeapon", self, 0)
		end
		
		return archetype
	end,
	CustomEquipGear = function (self, items)
		self:TryEquip(items, "Handheld A", "SniperRifle")
		self:TryEquip(items, "Handheld B", "Revolver")
	end,
	unitPowerModifier = 75,
	MaxHitPoints = 50,
	StartingPerks = {
		"SteadyBreathing",
		"Shatterhand",
	},
	AppearancesList = {
		PlaceObj('AppearanceWeight', {
			'Preset', "Adonis_Marksman",
		}),
	},
	Equipment = {
		"AdonisSniper",
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
	Tier = "Veteran",
	pollyvoice = "Joey",
	gender = "Male",
	VoiceResponseId = "AdonisAssault",
}

