UndefineClass('Tired')
DefineClass.Tired = {
	__parents = { "StatusEffect" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",

	object_class = "StatusEffect",
	Parameters = {
		PlaceObj('PresetParamNumber', {
			'Name', "ap_loss",
			'Value', -1,
			'Tag', "<ap_loss>",
		}),
		PlaceObj('PresetParamPercent', {
			'Name', "fm_mul",
			'Value', 50,
			'Tag', "<fm_mul>",
		}),
		PlaceObj('PresetParamNumber', {
			'Name', "duration",
			'Value', 12,
			'Tag', "<duration>",
		}),
	},
	unit_reactions = {
		PlaceObj('UnitReaction', {
			Event = "OnCalcStartTurnAP",
			Handler = function (self, target, value)
				return value + self:ResolveValue("ap_loss") * const.Scale.AP
			end,
		}),
		PlaceObj('UnitReaction', {
			Event = "OnCalcFreeMove",
			Handler = function (self, target, data)
				data.mul = MulDivRound(data.mul or 100, self:ResolveValue("fm_mul") or 50, 100)
			end,
		}),
	},
	DisplayName = T(299677471612, --[[ModItemCharacterEffectCompositeDef Tired DisplayName]] "Tired"),
	Description = T(890000000013106, --[[ModItemCharacterEffectCompositeDef Tired Description]] "Maximum AP <em><ap_loss></em>. Free Move <em><fm_mul>%</em>. Recover by resting in Sat View."),
	type = "Debuff",
	Icon = "UI/Hud/Status effects/tired",
	Shown = true,
	ShownSatelliteView = true,
	HasFloatingText = true,
}
