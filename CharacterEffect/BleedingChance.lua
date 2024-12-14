UndefineClass('BleedingChance')
DefineClass.BleedingChance = {
	__parents = { "StatusEffect" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",


	object_class = "StatusEffect",
	msg_reactions = {},
	unit_reactions = {},
	DisplayName = T(757391949802, --[[ModItemCharacterEffectCompositeDef BleedingChance DisplayName]] "Ранение в пах"),
	Description = "",
	OnAdded = function (self, obj)
		if obj.TempHitPoints > 0 then return end
		local hp = obj.TempHitPoints + obj.HitPoints
		if obj:Random(hp) < 20  then
		obj:AddStatusEffect("Bleeding") end
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

