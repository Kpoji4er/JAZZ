UndefineClass('HaveABlast')
DefineClass.HaveABlast = {
	__parents = { "Perk" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",


	object_class = "Perk",
	unit_reactions = {
		PlaceObj('UnitReaction', {
			Event = "OnCombatEnd",
			Handler = function (self, target)
				target:SetEffectValue("HaveABlast", nil)
			end,
		}),
		PlaceObj('UnitReaction', {
			Event = "OnCalcDamageAndEffects",
			Handler = function (self, owner, attacker, target, action, weapon, attack_args, hit, data)
				-- Incoming only, and only while the signature toggle is ON.
				-- (Outgoing grenade damage must never be scaled here.)
				if owner ~= target or not data then
					return
				end
				if not owner:GetEffectValue("HaveABlast") then
					return
				end
				local is_blast = (hit and (hit.explosion or hit.aoe or hit.explosion_center))
					or (attack_args and attack_args.explosion_pos)
					or IsKindOf(weapon, "Grenade")
					or IsKindOf(weapon, "Ordnance")
					or (weapon and weapon.class and string.find(weapon.class, "Grenade", 1, true))
				if not is_blast then
					return
				end
				-- Apply once; avoid re-entry / stacking with a second damage_percent pass to ~-90%.
				if data.jazz_haveablast_dr then
					return
				end
				data.jazz_haveablast_dr = true
				data.damage_percent = MulDivRound(data.damage_percent or 100, 50, 100)
			end,
		}),
	},
	DisplayName = T(890000000009873, --[[ModItemCharacterEffectCompositeDef HaveABlast DisplayName]] "Взрывной характер"),
	Description = T(890000000009874, --[[ModItemCharacterEffectCompositeDef HaveABlast Description]] "Переключатель. Пока активен: после атаки по себе (попадание или промах) отвечает гранатой (руки или из инвентаря); урон от взрывов по себе −50%. Выключен — без эффекта."),
	Icon = "UI/Icons/Perks/HaveABlast",
	Tier = "Personal",
}
