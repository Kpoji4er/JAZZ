UndefineClass('HaveABlast')
DefineClass.HaveABlast = {
	__parents = { "Perk" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",


	object_class = "Perk",
	unit_reactions = {
		PlaceObj('UnitReaction', {
			Event = "OnCalcDamageAndEffects",
			Handler = function (self, owner, attacker, target, action, weapon, attack_args, hit, data)
				if owner ~= target or not data then
					return
				end
				local self_blast = attacker == target
				if not self_blast and attack_args and attack_args.explosion_pos then
					self_blast = attacker == owner
				end
				if self_blast and (IsKindOf(weapon, "Grenade") or (action and action.ActionType == "Ranged Attack" and weapon and weapon.class and string.find(weapon.class, "Grenade"))) then
					data.damage_percent = MulDivRound(data.damage_percent or 100, 50, 100)
				end
			end,
		}),
	},
	DisplayName = T(890000000009873, --[[ModItemCharacterEffectCompositeDef HaveABlast DisplayName]] "Взрывной характер"),
	Description = T(890000000009874, --[[ModItemCharacterEffectCompositeDef HaveABlast Description]] "Переключатель: контратака гранатой. Получает только 50% урона от собственных взрывов."),
	Icon = "UI/Icons/Perks/HaveABlast",
	Tier = "Personal",
}
