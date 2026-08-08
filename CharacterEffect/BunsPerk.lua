UndefineClass('BunsPerk')
DefineClass.BunsPerk = {
	__parents = { "Perk" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",


	object_class = "Perk",
	unit_reactions = {
		PlaceObj('UnitReaction', {
			Event = "OnCalcChanceToHit",
			Handler = function (self, target, attacker, action, attack_target, weapon1, weapon2, data)
				if target ~= attacker then
					return
				end
				if type(Jazz_BunsTargetDamagedByAlly) == "function" and Jazz_BunsTargetDamagedByAlly(attacker, attack_target) then
					ApplyCthModifier_Add(self, data, 10)
				end
			end,
		}),
	},
	DisplayName = T(890000000009867, --[[ModItemCharacterEffectCompositeDef BunsPerk DisplayName]] "Добить"),
	Description = T(890000000009868, --[[ModItemCharacterEffectCompositeDef BunsPerk Description]] "+10% точности по целям, которых в этом ходу уже ранил союзник."),
	Icon = "UI/Icons/Perks/BunsPerk",
	Tier = "Personal",
}
