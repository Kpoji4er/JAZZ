UndefineClass('BloodLoss20')
DefineClass.BloodLoss20 = {
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
	DisplayName = T(890000000010316, --[[ModItemCharacterEffectCompositeDef BloodLoss20 DisplayName]] "Heavy Blood Loss"),
	Description = T(890000000010317, --[[ModItemCharacterEffectCompositeDef BloodLoss20 Description]] "Blood loss: <color EmStyle>−<APLoss> AP</color> at the start of the turn. Below 20% HP. Clears only when HP rises."),
	type = "Debuff",
	Icon = "Mod/e6L4ECj/Icons/StatusEffects/BloodLoss20.png",
	Shown = true,
	ShownSatelliteView = true,
}

