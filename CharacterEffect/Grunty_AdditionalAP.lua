UndefineClass('Grunty_AdditionalAP')
DefineClass.Grunty_AdditionalAP = {
	__parents = { "CharacterEffect" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",


	object_class = "CharacterEffect",
	unit_reactions = {
		PlaceObj('UnitReaction', {
			Event = "OnCalcStartTurnAP",
			Handler = function (self, target, value)
				if not self:ResolveValue("applied") then
					local ap = target:GetMaxActionPoints()
					return value + DivRound(ap,2) 
				end
			end,
		}),
		PlaceObj('UnitReaction', {
			Event = "OnBeginTurn",
			Handler = function (self, target)
				local ap = target:GetMaxActionPoints()
				target:GainAP(DivRound(ap,2) )
			end,
		}),
	},
	Conditions = {
		PlaceObj('CheckExpression', {
			Expression = function (self, obj) return g_Combat and IsKindOf(obj, "Unit") end,
		}),
	},
	DisplayName = T(952338905331, --[[ModItemCharacterEffectCompositeDef Grunty_AdditionalAP DisplayName]] "Überraschung"),
	Description = T(912592808613, --[[ModItemCharacterEffectCompositeDef Grunty_AdditionalAP Description]] "Дает <em><bonus> ОД</em>."),
	OnAdded = function (self, obj)
		if g_Teams[g_CurrentTeam] == obj.team then
			local ap = obj:GetMaxActionPoints()
			obj:GainAP(DivRound(ap,2) )
			self:SetParameter("applied", true)
		end
	end,
	type = "Buff",
	lifetime = "Until End of Turn",
	Icon = "UI/Icons/Perks/GruntyPerk",
	RemoveOnEndCombat = true,
	Shown = true,
}

