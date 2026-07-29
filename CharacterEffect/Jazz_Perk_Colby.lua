UndefineClass('Jazz_Perk_Colby')
DefineClass.Jazz_Perk_Colby = {
	__parents = { "Perk" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",


	object_class = "Perk",
	unit_reactions = {
		PlaceObj('UnitReaction', {
			Event = "OnCalcDamageAndEffects",
			Handler = function (self, owner, attacker, target, action, weapon, attack_args, hit, data)
				-- only Colby's own reaction instance (fired on the attacker) should proc this
				if owner ~= attacker then
					return
				end
				if not hit or not (hit.aoe or hit.explosion) then
					return
				end
				if not IsKindOf(target, "Unit") or not attacker:IsOnEnemySide(target) then
					return
				end
				if not target:HasStatusEffect("Wounded") then
					return
				end
				if InteractionRand(100, "Jazz_Perk_Colby") < 20 then
					target:AddStatusEffect("Panicked")
				end
			end,
		}),
	},
	DisplayName = T(890000000001700, --[[ModItemCharacterEffectCompositeDef Jazz_Perk_Colby DisplayName]] "Цепная паника"),
	Description = T(890000000001701, --[[ModItemCharacterEffectCompositeDef Jazz_Perk_Colby Description]] "WIP — механика сигнатурного перка в разработке."),
	Icon = "Mod/e6L4ECj/Perks/Personal/Colby.png",
	Tier = "Personal",
}
