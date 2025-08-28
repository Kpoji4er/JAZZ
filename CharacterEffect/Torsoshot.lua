UndefineClass('Torsoshot')
DefineClass.Torsoshot = {
	__parents = { "StatusEffect" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",


	object_class = "StatusEffect",
	msg_reactions = {},
	unit_reactions = {},
	DisplayName = T(147224231156, "Ранение в торс"),
	Description = "",
	OnAdded = function (self, obj)
		--print(obj.TempHitPoints)
		if obj.TempHitPoints > 0 then return end
		local hp = obj.TempHitPoints + obj.HitPoints
		if obj:Random(hp) < 1 then
		obj:AddStatusEffect("IncreaseTiredness") 
		end
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

