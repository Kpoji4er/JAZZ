UndefineClass('Jazz_OrderAP')
DefineClass.Jazz_OrderAP = {
	__parents = { "StatusEffect" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",

	object_class = "StatusEffect",
	Parameters = {
		PlaceObj('PresetParamNumber', {
			'Name', "ap_bonus",
			'Value', 3,
			'Tag', "<ap_bonus>",
		}),
	},
	unit_reactions = {
		PlaceObj('UnitReaction', {
			Event = "OnBeginTurn",
			Handler = function (self, target)
				if not self:ResolveValue("applied") then
					target:GainAP((self:ResolveValue("ap_bonus") or 3) * const.Scale.AP)
					self:SetParameter("applied", true)
				end
			end,
		}),
	},
	DisplayName = T(890000000006218, --[[ModItemCharacterEffectCompositeDef Jazz_OrderAP DisplayName]] "Приказ: ОД"),
	Description = T(890000000006219, --[[ModItemCharacterEffectCompositeDef Jazz_OrderAP Description]] "+3 ОД на этот ход от полевого командира."),
	OnAdded = function (self, obj)
		if g_Combat and g_Teams and g_Teams[g_CurrentTeam] == obj.team then
			obj:GainAP((self:ResolveValue("ap_bonus") or 3) * const.Scale.AP)
			self:SetParameter("applied", true)
		end
	end,
	type = "Buff",
	lifetime = "Until End of Turn",
	Icon = "UI/Hud/Status effects/accuracy",
	RemoveOnEndCombat = true,
	Shown = true,
}
