UndefineClass('TraumaLegsLight')
DefineClass.TraumaLegsLight = {
	__parents = { "JazzTraumaEffect" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",


	object_class = "JazzTraumaEffect",
	DisplayName = T(890000000010106, --[[ModItemCharacterEffectCompositeDef TraumaLegsLight DisplayName]] "Leg Trauma (Light)"),
	Description = T(890000000010107, --[[ModItemCharacterEffectCompositeDef TraumaLegsLight Description]] "Pain when moving. No direct move-cost penalty."),
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
	Icon = "Mod/e6L4ECj/Icons/StatusEffects/TraumaLegsLight.png",
	Shown = true,
	ShownSatelliteView = true,
	HasFloatingText = true,
}

