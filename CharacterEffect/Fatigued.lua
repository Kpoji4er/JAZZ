UndefineClass('Fatigued')
DefineClass.Fatigued = {
	__parents = { "StatusEffect" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",

	object_class = "StatusEffect",
	Parameters = {
		PlaceObj('PresetParamPercent', {
			'Name', "fm_mul",
			'Value', 75,
			'Tag', "<fm_mul>",
		}),
	},
	unit_reactions = {
		PlaceObj('UnitReaction', {
			Event = "OnCalcFreeMove",
			Handler = function (self, target, data)
				data.mul = MulDivRound(data.mul or 100, self:ResolveValue("fm_mul") or 75, 100)
			end,
		}),
	},
	DisplayName = T(890000000013104, --[[ModItemCharacterEffectCompositeDef Fatigued DisplayName]] "Fatigued"),
	Description = T(890000000013105, --[[ModItemCharacterEffectCompositeDef Fatigued Description]] "Free Move reduced to <em><fm_mul>%</em>. No AP penalty yet. Rest in Sat View to recover."),
	AddEffectText = T(890000000013120, --[[ModItemCharacterEffectCompositeDef Fatigued AddEffectText]] "<em><DisplayName></em> is fatigued"),
	type = "Debuff",
	Icon = "Mod/e6L4ECj/Icons/StatusEffects/Fatigued.png",
	Shown = true,
	ShownSatelliteView = true,
	HasFloatingText = true,
}
