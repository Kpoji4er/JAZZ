UndefineClass('BloodLoss50')
DefineClass.BloodLoss50 = {
	__parents = { "StatusEffect" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",


	object_class = "StatusEffect",
	unit_reactions = {
		PlaceObj('UnitReaction', {
			Event = "OnCalcStartTurnAP",
			Handler = function (self, target, value)
				return value - self:ResolveValue("APLoss") * const.Scale.AP
			end,
		}),
	},
	DisplayName = T(890000000010310, --[[ModItemCharacterEffectCompositeDef BloodLoss50 DisplayName]] "Weakness"),
	Description = T(890000000010311, --[[ModItemCharacterEffectCompositeDef BloodLoss50 Description]] "Blood loss: <color EmStyle>−<APLoss> AP</color> at the start of the turn. Below 50% HP. Clears only when HP rises."),
	type = "Debuff",
	Icon = "Mod/e6L4ECj/Icons/StatusEffects/BloodLoss50.png",
	Shown = true,
	ShownSatelliteView = true,
}

