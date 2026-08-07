UndefineClass('BloodLoss5')
DefineClass.BloodLoss5 = {
	__parents = { "StatusEffect" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",
	object_class = "StatusEffect",
	Parameters = {
		PlaceObj('PresetParamNumber', {
			'Name', "APLoss",
			'Value', 6,
			'Tag', "<APLoss>",
		}),
	},
	unit_reactions = {
		PlaceObj('UnitReaction', {
			Event = "OnCalcStartTurnAP",
			Handler = function(self, target, value)
				return value - self:ResolveValue("APLoss") * const.Scale.AP
			end,
		}),
	},
	DisplayName = T(890000000010320, "Near Collapse"),
	Description = T(890000000010321, "Blood loss: <color EmStyle>−<APLoss> AP</color> at the start of the turn. Below 5% HP. Clears only when HP rises."),
	type = "Debuff",
	Icon = "Mod/e6L4ECj/Icons/StatusEffects/BloodLoss5.png",
	Shown = true,
	ShownSatelliteView = true,
}
