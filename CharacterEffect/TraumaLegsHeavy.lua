UndefineClass('TraumaLegsHeavy')
DefineClass.TraumaLegsHeavy = {
	__parents = { "JazzTraumaEffect" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",


	object_class = "JazzTraumaEffect",
	DisplayName = T(890000000010110, --[[ModItemCharacterEffectCompositeDef TraumaLegsHeavy DisplayName]] "Leg Trauma (Heavy)"),
	Description = T(890000000010111, --[[ModItemCharacterEffectCompositeDef TraumaLegsHeavy Description]] "Move cost <color EmStyle>+<move_ap_modifier>%</color>. Almost immobile. +3 Pain when moving; +1 Pain/turn if unused."),
	OnAdded = function (self, obj)
		if IsKindOf(obj, "Unit") then
			Msg("UnitAPChanged", obj)
		end
	end,
	OnRemoved = function (self, obj)
		if IsKindOf(obj, "Unit") then
			Msg("UnitAPChanged", obj)
		end
	end,
	type = "Debuff",
	Icon = "Mod/e6L4ECj/Icons/StatusEffects/TraumaLegsHeavy.png",
	Shown = true,
	ShownSatelliteView = true,
	HasFloatingText = true,
}

