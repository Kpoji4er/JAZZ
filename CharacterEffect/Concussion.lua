UndefineClass('Concussion')
DefineClass.Concussion = {
	__parents = { "StatusEffect" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",


	object_class = "StatusEffect",
	Parameters = {
		PlaceObj('PresetParamNumber', {
			'Name', "APLoss",
			'Value', 2,
			'Tag', "<APLoss>",
		}),
		PlaceObj('PresetParamPercent', {
			'Name', "cth_penalty",
			'Value', 15,
			'Tag', "<cth_penalty>%",
		}),
		PlaceObj('PresetParamNumber', {
			'Name', "move_ap_modifier",
			'Value', 30,
			'Tag', "<move_ap_modifier>",
		}),
	},
	unit_reactions = {
		PlaceObj('UnitReaction', {
			Event = "OnCalcStartTurnAP",
			Handler = function (self, target, value)
				return value - self:ResolveValue("APLoss") * const.Scale.AP
			end,
		}),
		PlaceObj('UnitReaction', {
			Event = "OnCalcChanceToHit",
			Handler = function (self, target, attacker, action, attack_target, weapon1, weapon2, data)
				if target == attacker then
					ApplyCthModifier_Add(self, data, -self:ResolveValue("cth_penalty"))
				end
			end,
		}),
		PlaceObj('UnitReaction', {
			Event = "OnCalcMoveModifier",
			Handler = function (self, target, value, action)
				return value + self:ResolveValue("move_ap_modifier")
			end,
		}),
		PlaceObj('UnitReaction', {
			Event = "OnCalcFreeMove",
			Handler = function (self, target, data)
				data.add = 0
				data.mul = 0
			end,
		}),
		PlaceObj('UnitReaction', {
			Event = "OnBeginTurn",
			Handler = function (self, target)
				target:RemoveStatusEffect("FreeMove")
			end,
		}),
		PlaceObj('UnitReaction', {
			Event = "OnEndTurn",
			Handler = function (self, target)
				local left = self:ResolveValue("jazz_conc_turns") or 1
				left = left - 1
				if left <= 0 then
					target:RemoveStatusEffect("Concussion", "all")
				else
					self:SetParameter("jazz_conc_turns", left)
				end
			end,
		}),
	},
	DisplayName = T(890000000010277, --[[ModItemCharacterEffectCompositeDef Concussion DisplayName]] "Concussion"),
	Description = T(890000000010278, --[[ModItemCharacterEffectCompositeDef Concussion Description]] "Disoriented by blast: <color EmStyle>−<APLoss> AP</color>, <color EmStyle>−<cth_penalty>% chance to hit</color>, move cost <color EmStyle>+<move_ap_modifier>%</color>, no Free Move. Lasts about 1–2 turns."),
	AddEffectText = T(890000000010279, --[[ModItemCharacterEffectCompositeDef Concussion AddEffectText]] "<color EmStyle><DisplayName></color> is concussed"),
	RemoveEffectText = T(890000000010280, --[[ModItemCharacterEffectCompositeDef Concussion RemoveEffectText]] "<color EmStyle><DisplayName></color> clears concussion"),
	OnAdded = function (self, obj)
		self:SetParameter("jazz_conc_turns", 2)
		Msg("UnitAPChanged", obj)
	end,
	OnRemoved = function (self, obj)
		Msg("UnitAPChanged", obj)
	end,
	type = "Debuff",
	Icon = "Mod/e6L4ECj/Icons/StatusEffects/Concussion.png",
	RemoveOnEndCombat = true,
	Shown = true,
	HasFloatingText = true,
}
