UndefineClass('BleedingChance')
DefineClass.BleedingChance = {
	__parents = { "StatusEffect" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",


	object_class = "StatusEffect",
	msg_reactions = {},
	unit_reactions = {},
	DisplayName = T(757391949802, --[[ModItemCharacterEffectCompositeDef BleedingChance DisplayName]] "Шанс получить кровотечение"),
	Description = "",
	OnAdded = function (self, obj)
		-- MED-001: pierce bleed is rolled centrally in JazzTryRollBleedFromHit.
		-- Keep ID so ammo AppliedEffects lists stay valid without double-rolling.
	end,
	OnRemoved = function (self, obj)  end,
	type = "Debuff",
	lifetime = "Until End of Turn",
	Icon = "UI/Hud/Status effects/wounded",
	RemoveOnEndCombat = true,
	RemoveOnSatViewTravel = true,
	RemoveOnCampaignTimeAdvance = true,
	HideOnBadge = true,
}
