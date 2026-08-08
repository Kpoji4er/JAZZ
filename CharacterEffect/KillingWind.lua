UndefineClass('KillingWind')
DefineClass.KillingWind = {
	__parents = { "Perk" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",


	object_class = "Perk",
	unit_reactions = {
		PlaceObj('UnitReaction', {
			Event = "OnUnitAttack",
			Handler = function (self, target, attacker, action, attack_target, results, attack_args)
				if target ~= attacker or not results then
					return
				end
				local hit_units = {}
				for _, hit in ipairs(results.hits or empty_table) do
					local obj = hit and (hit.obj or hit.unit)
					if IsKindOf(obj, "Unit") and not obj:IsDead() then
						hit_units[obj] = true
					end
				end
				local n = 0
				for _ in pairs(hit_units) do
					n = n + 1
				end
				if n >= 2 then
					attacker:ApplyTempHitPoints(8)
				end
			end,
		}),
	},
	DisplayName = T(890000000009875, --[[ModItemCharacterEffectCompositeDef KillingWind DisplayName]] "Убийственный ветер"),
	Description = T(890000000009876, --[[ModItemCharacterEffectCompositeDef KillingWind Description]] "Если атака задевает ≥2 целей — +8 Grit. Тяжёлая броня даёт половину штрафа Free Move; громоздкое оружие не штрафует FM."),
	Icon = "UI/Icons/Perks/KillingWind",
	Tier = "Personal",
}
