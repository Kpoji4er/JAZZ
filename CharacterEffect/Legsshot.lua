UndefineClass('Legsshot')
DefineClass.Legsshot = {
	__parents = { "StatusEffect" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",


	object_class = "StatusEffect",
	msg_reactions = {},
	unit_reactions = {},
	DisplayName = T(844850890619, "Ранение в ноги"),
	Description = "",
	OnAdded = function (self, obj)
		if obj.TempHitPoints > 0 then return end
		local hp = obj.TempHitPoints + obj.HitPoints
		if obj:Random(hp) < 20  then
		obj:AddStatusEffect("Slowed")
		end
	end,
	OnRemoved = function (self, obj)  end,
	type = "Debuff",
	lifetime = "Until End of Turn",
	Icon = "UI/Hud/Status effects/wounded",
	max_stacks = 2,
	HideOnBadge = true,
	HasFloatingText = true,
}

