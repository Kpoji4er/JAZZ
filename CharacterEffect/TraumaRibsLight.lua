UndefineClass('TraumaRibsLight')
DefineClass.TraumaRibsLight = {
	__parents = { "JazzTraumaEffect" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",


	object_class = "JazzTraumaEffect",
	DisplayName = T(890000000010112, --[[ModItemCharacterEffectCompositeDef TraumaRibsLight DisplayName]] "Rib Trauma (Light)"),
	Description = T(890000000010113, --[[ModItemCharacterEffectCompositeDef TraumaRibsLight Description]] "Pain at the start of the turn."),
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
	Icon = "Mod/e6L4ECj/Icons/StatusEffects/TraumaRibsLight.png",
	Shown = true,
	ShownSatelliteView = true,
	HasFloatingText = true,
}

