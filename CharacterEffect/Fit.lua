UndefineClass('Fit')
DefineClass.Fit = {
	__parents = { "StatusEffect" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",

	object_class = "StatusEffect",
	Parameters = {
		PlaceObj('PresetParamNumber', {
			'Name', "ap_gain",
			'Value', 1,
			'Tag', "<ap_gain>",
		}),
		PlaceObj('PresetParamPercent', {
			'Name', "fm_mul",
			'Value', 120,
			'Tag', "<fm_mul>",
		}),
		PlaceObj('PresetParamNumber', {
			'Name', "opening_fm_turns",
			'Value', 1,
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
	DisplayName = T(890000000013100, --[[ModItemCharacterEffectCompositeDef Fit DisplayName]] "Fit"),
	Description = T(890000000013101, --[[ModItemCharacterEffectCompositeDef Fit Description]] "Maximum AP <em>+<ap_gain></em>. Free Move <em>x<fm_mul>%</em>. First <em><opening_fm_turns></em> combat turn(s): extra <em>+<opening_fm_bonus></em> Free Move."),
	AddEffectText = T(890000000013118, --[[ModItemCharacterEffectCompositeDef Fit AddEffectText]] "<em><DisplayName></em> feels fit"),
	type = "Buff",
	Icon = "Mod/e6L4ECj/Icons/StatusEffects/Fit.png",
	Shown = true,
	ShownSatelliteView = true,
	HasFloatingText = true,
}
