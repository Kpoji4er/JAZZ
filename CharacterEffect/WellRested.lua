UndefineClass('WellRested')
DefineClass.WellRested = {
	__parents = { "StatusEffect" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",

	object_class = "StatusEffect",
	Parameters = {
		PlaceObj('PresetParamNumber', {
			'Name', "ap_gain",
			'Value', 2,
			'Tag', "<ap_gain>",
		}),
		PlaceObj('PresetParamPercent', {
			'Name', "fm_mul",
			'Value', 120,
			'Tag', "<fm_mul>",
		}),
		PlaceObj('PresetParamNumber', {
			'Name', "opening_fm_turns",
			'Value', 3,
			'Tag', "<opening_fm_turns>",
		}),
		PlaceObj('PresetParamNumber', {
			'Name', "opening_fm_bonus",
			'Value', 2,
			'Tag', "<opening_fm_bonus>",
		}),
	},
	unit_reactions = {
		PlaceObj('UnitReaction', {
			Event = "OnCalcStartTurnAP",
			Handler = function (self, target, value)
				return value + self:ResolveValue("ap_gain") * const.Scale.AP
			end,
		}),
		PlaceObj('UnitReaction', {
			Event = "OnCalcFreeMove",
			Handler = function (self, target, data)
				data.mul = MulDivRound(data.mul or 100, self:ResolveValue("fm_mul") or 120, 100)
				local add = JazzEnergyOpeningFmBonus(target, self)
				if add > 0 then
					data.add = (data.add or 0) + add
				end
			end,
		}),
	},
	DisplayName = T(789783285719, --[[ModItemCharacterEffectCompositeDef WellRested DisplayName]] "Well Rested"),
	Description = T(890000000013108, --[[ModItemCharacterEffectCompositeDef WellRested Description]] "Maximum AP <em>+<ap_gain></em>. Free Move <em>x<fm_mul>%</em>. First <em><opening_fm_turns></em> combat turns: extra <em>+<opening_fm_bonus></em> Free Move."),
	AddEffectText = T(353089370853, --[[ModItemCharacterEffectCompositeDef WellRested AddEffectText]] "<em><DisplayName></em> is well rested"),
	RemoveEffectText = T(945859256424, --[[ModItemCharacterEffectCompositeDef WellRested RemoveEffectText]] "<em><DisplayName></em> is no longer well rested"),
	type = "Buff",
	Icon = "UI/Hud/Status effects/well_rested",
	Shown = true,
	ShownSatelliteView = true,
	HasFloatingText = true,
}
