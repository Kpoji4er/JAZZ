UndefineClass('RecklessAssault')
DefineClass.RecklessAssault = {
	__parents = { "Perk" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",


	object_class = "Perk",
	Parameters = {
		PlaceObj('PresetParamNumber', {
			'Name', "cth_bonus",
			'Value', 15,
			'Tag', "<cth_bonus>",
		}),
	},
	unit_reactions = {
		PlaceObj('UnitReaction', {
			Event = "OnCalcChanceToHit",
			Handler = function (self, target, attacker, action, attack_target, weapon1, weapon2, data)
				if target ~= attacker or not data or not action then
					return
				end
				if action.id ~= "RecklessAssault" then
					return
				end
				local bonus = self:ResolveValue("cth_bonus") or 15
				ApplyCthModifier_Add(self, data, bonus)
			end,
		}),
	},
	DisplayName = T(890000000009935, --[[ModItemCharacterEffectCompositeDef RecklessAssault DisplayName]] "Безрассудный натиск"),
	Description = T(890000000009936, --[[ModItemCharacterEffectCompositeDef RecklessAssault Description]] "Улучшенный <em>Run and Gun</em>: до <em>4</em> атак с пистолет-пулемётом, карабином или автоматом. <em>+<cth_bonus></em> к точности. Без потери <GameTerm('Energy')>. <color EmStyle>Заряжается после убийства другим способом.</color>"),
	Icon = "UI/Icons/Perks/RecklessAssault",
	Tier = "Personal",
}
