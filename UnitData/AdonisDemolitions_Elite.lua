UndefineClass('AdonisDemolitions_Elite')
DefineClass.AdonisDemolitions_Elite = {
	__parents = { "UnitData" },
	__generated_by_class = "ModItemUnitDataCompositeDef",


	object_class = "UnitData",
	Health = 87,
	Agility = 87,
	Dexterity = 84,
	Strength = 90,
	Wisdom = 61,
	Leadership = 31,
	Marksmanship = 87,
	Mechanical = 80,
	Explosives = 98,
	Medical = 34,
	Portrait = "UI/EnemiesPortraits/AdonisDemo",
	Name = T(516222648054, --[[ModItemUnitDataCompositeDef AdonisDemolitions_Elite Name]] "Мастер-взрывотехник"),
	Randomization = true,
	elite = true,
	eliteCategory = "Foreigners",
	Affiliation = "Adonis",
	StartingLevel = 6,
	neutral_retaliate = true,
	AIKeywords = {
		"Ordnance",
		"Explosives",
	},
	role = "Artillery",
	MaxAttacks = 2,
	PickCustomArchetype = function (self, proto_context)
		local enemy, dist = GetNearestEnemy(self)
		local archetype = self.archetype
		local weapon_class = "GrenadeLauncher"
		
		if enemy and dist < 7*const.SlabSizeX then
			archetype = "Skirmisher"
			weapon_class = "Firearm"
			PlayVoiceResponse(self, "AIArchetypeScared")
		end
		
		if not self:GetActiveWeapons(weapon_class) then
			AIPlayCombatAction("ChangeWeapon", self, 0)
		end
		
		return archetype
	end,
	CustomEquipGear = function (self, items)
		self:TryEquip(items, "Handheld A", "GrenadeLauncher")
		self:TryEquip(items, "Handheld B", "Firearm")
	end,
	MaxHitPoints = 50,
	StartingPerks = {
		"Throwing",
		"Berserker",
	},
	AppearancesList = {
		PlaceObj('AppearanceWeight', {
			'Preset', "Adonis_Demolition",
		}),
	},
	Equipment = {
		"AdonisDemolitions",
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
	pollyvoice = "Russell",
	gender = "Male",
	VoiceResponseId = "AdonisAssault",
}

