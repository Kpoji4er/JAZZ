UndefineClass('BloodLoss1')
DefineClass.BloodLoss1 = {
	__parents = { "StatusEffect" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",
	object_class = "StatusEffect",
	Parameters = {
		PlaceObj('PresetParamNumber', {
			'Name', "APLoss",
			'Value', 7,
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
	DisplayName = T(890000000010322, "Critical Blood Loss"),
	Description = T(890000000010323, "Critical blood loss: <color EmStyle>−<APLoss> AP</color> at the start of the turn. Below 1% HP — still conscious. Clears only when HP rises."),
	type = "Debuff",
	Icon = "Mod/e6L4ECj/Icons/StatusEffects/BloodLoss1.png",
	Shown = true,
	ShownSatelliteView = true,
}
