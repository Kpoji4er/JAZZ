UndefineClass('AdonisMortar')
DefineClass.AdonisMortar = {
	__parents = { "UnitData" },
	__generated_by_class = "ModItemUnitDataCompositeDef",


	object_class = "UnitData",
	Health = 77,
	Agility = 78,
	Dexterity = 75,
	Strength = 99,
	Wisdom = 48,
	Leadership = 31,
	Marksmanship = 50,
	Mechanical = 50,
	Explosives = 94,
	Medical = 0,
	Portrait = "UI/EnemiesPortraits/AdonisArtillery",
	BigPortrait = "UI/Enemies/LegionRaider",
	Name = T(916476324121, --[[ModItemUnitDataCompositeDef AdonisMortar Name]] "Эксперт-взрывотехник"),
	Randomization = true,
	Affiliation = "Adonis",
	StartingLevel = 6,
	neutral_retaliate = true,
	AIKeywords = {
		"Explosives",
	},
	archetype = "Artillery",
	role = "Artillery",
	MaxAttacks = 1,
	PickCustomArchetype = function (self, proto_context)
		local enemy, dist = GetNearestEnemy(self)
		local archetype = self.archetype
		local weapon_class = "Mortar"
		
		if GameState.Underground or enemy and dist < 7*const.SlabSizeX then
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
		self:TryEquip(items, "Handheld A", "Mortar")
		self:TryEquip(items, "Handheld B", "Revolver")
	end,
	unitPowerModifier = 75,
	MaxHitPoints = 50,
	StartingPerks = {
		"Throwing",
		"HeavyWeaponsTraining",
	},
	AppearancesList = {
		PlaceObj('AppearanceWeight', {
			'Preset', "Adonis_Artillery",
		}),
	},
	Equipment = {
		"AdonisMortar",
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

