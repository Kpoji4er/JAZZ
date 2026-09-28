UndefineClass('TraumaLegsMedium')
DefineClass.TraumaLegsMedium = {
	__parents = { "JazzTraumaEffect" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",


	object_class = "JazzTraumaEffect",
	DisplayName = T(890000000010108, --[[ModItemCharacterEffectCompositeDef TraumaLegsMedium DisplayName]] "Leg Trauma (Medium)"),
	Description = T(890000000010109, --[[ModItemCharacterEffectCompositeDef TraumaLegsMedium Description]] "Move cost <color EmStyle>+<move_ap_modifier>%</color>. No Free Move / sprint. +2 Pain when moving."),
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
	Icon = "Mod/e6L4ECj/Icons/StatusEffects/TraumaLegsMedium.png",
	Shown = true,
	ShownSatelliteView = true,
	HasFloatingText = true,
}

