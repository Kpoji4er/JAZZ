UndefineClass('Winded')
DefineClass.Winded = {
	__parents = { "StatusEffect" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",

	object_class = "StatusEffect",
	Parameters = {
		PlaceObj('PresetParamPercent', {
			'Name', "fm_mul",
			'Value', 100,
			'Tag', "<fm_mul>",
		}),
	},
	unit_reactions = {
		PlaceObj('UnitReaction', {
			Event = "OnCalcFreeMove",
			Handler = function (self, target, data)
				data.mul = MulDivRound(data.mul or 100, self:ResolveValue("fm_mul") or 100, 100)
			end,
		}),
	},
	DisplayName = T(890000000013102, --[[ModItemCharacterEffectCompositeDef Winded DisplayName]] "Winded"),
	Description = T(890000000013103, --[[ModItemCharacterEffectCompositeDef Winded Description]] "Slightly worn from travel. Free Move at baseline (<em><fm_mul>%</em>). No AP penalty. Rest in Sat View to recover."),
	AddEffectText = T(890000000013119, --[[ModItemCharacterEffectCompositeDef Winded AddEffectText]] "<em><DisplayName></em> is winded"),
	type = "Debuff",
	Icon = "Mod/e6L4ECj/Icons/StatusEffects/Winded.png",
	Shown = true,
	ShownSatelliteView = true,
	HasFloatingText = true,
}
