UndefineClass('Groinshot')
DefineClass.Groinshot = {
	__parents = { "StatusEffect" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",


	object_class = "StatusEffect",
	msg_reactions = {},
	unit_reactions = {},
	DisplayName = T(158615306685, "Ранение в пах"),
	Description = "",
	OnAdded = function (self, obj)
		if obj.TempHitPoints > 0 then return end
		local hp = obj.TempHitPoints + obj.HitPoints
		if obj:Random(hp) < 20  then
		obj:AddStatusEffect("Bleeding") end
		if obj:Random(hp) < 40   then
		obj:AddStatusEffect("Bleeding")
		end
		if obj:Random(hp) < 5   then
		obj:AddStatusEffect("Bleeding")
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

