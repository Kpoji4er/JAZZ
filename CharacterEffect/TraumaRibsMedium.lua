UndefineClass('TraumaRibsMedium')
DefineClass.TraumaRibsMedium = {
	__parents = { "JazzTraumaEffect" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",


	object_class = "JazzTraumaEffect",
	DisplayName = T(890000000010114, --[[ModItemCharacterEffectCompositeDef TraumaRibsMedium DisplayName]] "Rib Trauma (Medium)"),
	Description = T(890000000010115, --[[ModItemCharacterEffectCompositeDef TraumaRibsMedium Description]] "Start-of-turn AP <color EmStyle>-<APLoss></color>. No Free Move. +2 Pain at the start of the turn."),
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
	Icon = "Mod/e6L4ECj/Icons/StatusEffects/TraumaRibsMedium.png",
	Shown = true,
	ShownSatelliteView = true,
	HasFloatingText = true,
}

