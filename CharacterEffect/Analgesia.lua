UndefineClass('Analgesia')
DefineClass.Analgesia = {
	__parents = { "StatusEffect" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",
	object_class = "StatusEffect",
	DisplayName = T(890000000010009, "Analgesia"),
	Description = T(890000000010010, "Clears Pain and suppresses new Pain stacks. Does not stop bleeding or heal injuries."),
	OnAdded = function(self, obj)
		local refund_ap = rawget(_G, "JazzRefundPainStartTurnAP")
		if type(refund_ap) == "function" then
			refund_ap(obj)
		end
		if obj and obj.RemoveStatusEffect then
			obj:RemoveStatusEffect("Pain", "all")
		end
		Msg("UnitAPChanged", obj)
	end,
	type = "Buff",
	Icon = "Mod/e6L4ECj/Icons/StatusEffects/Analgesia.png",
	RemoveOnEndCombat = true,
	Shown = true,
	ShownSatelliteView = true,
}
