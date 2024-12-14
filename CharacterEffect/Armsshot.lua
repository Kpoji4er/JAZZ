UndefineClass('Armsshot')
DefineClass.Armsshot = {
	__parents = { "StatusEffect" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",


	object_class = "StatusEffect",
	msg_reactions = {},
	unit_reactions = {},
	DisplayName = T(564797563324, --[[ModItemCharacterEffectCompositeDef Armsshot DisplayName]] "Ранение в руки"),
	Description = "",
	OnAdded = function (self, obj)
		if obj.TempHitPoints > 0 then return end
		local hp = obj.TempHitPoints + obj.HitPoints
		--print(hp)
		if obj:Random(hp) < 30 then
		obj:AddStatusEffect("Numbness") end
		if obj:Random(hp) < 25 then
		obj:AddStatusEffect("Inaccurate") end
	end,
	OnRemoved = function (self, obj)  end,
	type = "Debuff",
	lifetime = "Until End of Turn",
	Icon = "UI/Hud/Status effects/wounded",
	RemoveOnEndCombat = true,
	RemoveOnSatViewTravel = true,
	RemoveOnCampaignTimeAdvance = true,
	HideOnBadge = true,
	HasFloatingText = true,
}

