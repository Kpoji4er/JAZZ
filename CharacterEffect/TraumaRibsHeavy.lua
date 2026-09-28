UndefineClass('TraumaRibsHeavy')
DefineClass.TraumaRibsHeavy = {
	__parents = { "JazzTraumaEffect" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",


	object_class = "JazzTraumaEffect",
	DisplayName = T(890000000010116, --[[ModItemCharacterEffectCompositeDef TraumaRibsHeavy DisplayName]] "Rib Trauma (Heavy)"),
	Description = T(890000000010117, --[[ModItemCharacterEffectCompositeDef TraumaRibsHeavy Description]] "Start-of-turn AP <color EmStyle>-<APLoss></color>. Combat-ineffective. +3 Pain at turn start; +1 Pain/turn if unused."),
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
	Icon = "Mod/e6L4ECj/Icons/StatusEffects/TraumaRibsHeavy.png",
	Shown = true,
	ShownSatelliteView = true,
	HasFloatingText = true,
}

