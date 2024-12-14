UndefineClass('Headshot')
DefineClass.Headshot = {
	__parents = { "StatusEffect" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",


	object_class = "StatusEffect",
	msg_reactions = {},
	unit_reactions = {},
	DisplayName = T(664162876607, --[[ModItemCharacterEffectCompositeDef Headshot DisplayName]] "Ранение в голову"),
	Description = "",
	OnAdded = function (self, obj)
		if obj.TempHitPoints > 0 then return end
		local hp = obj.TempHitPoints + obj.HitPoints
		if obj:Random(hp) < 5  then
		obj:AddStatusEffect("Unconscious")
		elseif obj:Random(hp) < 20   then
		obj:AddStatusEffect("Blinded")
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

